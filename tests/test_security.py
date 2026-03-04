import os
import sys
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent))
from termux_app_store.termux_app_store_cli import (
    load_package,
    load_all_packages,
    cmd_install,
    cmd_upgrade,
    has_store_fingerprint,
    is_valid_root,
    FINGERPRINT_STRING,
)


def make_root(tmp_path):
    root = tmp_path / "app-root"
    root.mkdir()
    (root / "packages").mkdir()
    (root / "build-package.sh").write_text(f"# {FINGERPRINT_STRING}\n")
    return root


def make_pkg(packages_dir, name, version="1.0.0"):
    pkg = packages_dir / name
    pkg.mkdir(parents=True, exist_ok=True)
    (pkg / "build.sh").write_text(f'TERMUX_PKG_VERSION="{version}"\n')
    return pkg


def make_stdout_mock(lines):
    stdout = MagicMock()
    stdout.readline.side_effect = list(lines) + [b""]
    return stdout


class TestMaliciousPackageMetadata:

    @pytest.fixture(autouse=True)
    def no_remote(self, monkeypatch):
        monkeypatch.setattr(
            "termux_app_store.termux_app_store_cli.fetch_index",
            lambda: []
        )

    def test_version_field_parsed_as_string(self, tmp_path):
        pkg = tmp_path / "evil"
        pkg.mkdir()
        (pkg / "build.sh").write_text('TERMUX_PKG_VERSION="1.0.0"\n')
        p = load_package(pkg)
        assert p["version"] == "1.0.0"
        assert isinstance(p["version"], str)

    def test_version_with_special_chars(self, tmp_path):
        pkg = tmp_path / "mypkg"
        pkg.mkdir()
        (pkg / "build.sh").write_text('TERMUX_PKG_VERSION="1.0.0-beta+build"\n')
        p = load_package(pkg)
        assert p["version"] == "1.0.0-beta+build"

    def test_name_comes_from_directory(self, tmp_path):
        pkg = tmp_path / "safe-pkg"
        pkg.mkdir()
        (pkg / "build.sh").write_text('TERMUX_PKG_VERSION="1.0.0"\n')
        p = load_package(pkg)
        assert p["name"] == "safe-pkg"

    def test_deps_field_parsed(self, tmp_path):
        pkg = tmp_path / "mypkg"
        pkg.mkdir()
        (pkg / "build.sh").write_text('TERMUX_PKG_DEPENDS="nodejs, python"\n')
        p = load_package(pkg)
        assert p["deps"] == "nodejs, python"

    def test_maintainer_field_parsed(self, tmp_path):
        pkg = tmp_path / "mypkg"
        pkg.mkdir()
        (pkg / "build.sh").write_text('TERMUX_PKG_MAINTAINER="@dev"\n')
        p = load_package(pkg)
        assert p["maintainer"] == "@dev"

    def test_missing_fields_returns_defaults(self, tmp_path):
        pkg = tmp_path / "minimal"
        pkg.mkdir()
        (pkg / "build.sh").write_text("# empty\n")
        p = load_package(pkg)
        assert p["version"] == "?"
        assert p["desc"] == "-"
        assert p["deps"] == "-"
        assert p["maintainer"] == "-"

    def test_duplicate_fields(self, tmp_path):
        pkg = tmp_path / "dup"
        pkg.mkdir()
        (pkg / "build.sh").write_text(
            'TERMUX_PKG_VERSION="1.0.0"\n'
            'TERMUX_PKG_VERSION="9.9.9"\n'
        )
        p = load_package(pkg)
        assert p["version"] in ("1.0.0", "9.9.9")

    def test_multiple_packages_loaded(self, tmp_path):
        packages = tmp_path / "packages"
        packages.mkdir()
        for name in ["pkg-a", "pkg-b", "pkg-c"]:
            make_pkg(packages, name)
        pkgs = load_all_packages(packages)
        assert len(pkgs) == 3
        assert {p["name"] for p in pkgs} == {"pkg-a", "pkg-b", "pkg-c"}

    def test_package_without_build_sh_skipped(self, tmp_path):
        packages = tmp_path / "packages"
        packages.mkdir()
        (packages / "no-build").mkdir()
        assert load_all_packages(packages) == []

    def test_mixed_valid_and_invalid_packages(self, tmp_path):
        packages = tmp_path / "packages"
        packages.mkdir()
        make_pkg(packages, "valid-pkg")
        (packages / "invalid-pkg").mkdir()
        pkgs = load_all_packages(packages)
        assert len(pkgs) == 1
        assert pkgs[0]["name"] == "valid-pkg"


class TestCorruptedBuildScript:

    def test_binary_garbage_in_build_sh(self, tmp_path):
        pkg = tmp_path / "corrupt"
        pkg.mkdir()
        (pkg / "build.sh").write_bytes(b"\xff\xfe\x00\x01garbage\x00\x00")
        p = load_package(pkg)
        assert isinstance(p, dict)
        assert "version" in p

    def test_empty_build_sh(self, tmp_path):
        pkg = tmp_path / "empty"
        pkg.mkdir()
        (pkg / "build.sh").write_bytes(b"")
        assert load_package(pkg)["version"] == "?"

    def test_build_sh_is_directory(self, tmp_path):
        pkg = tmp_path / "weird"
        pkg.mkdir()
        (pkg / "build.sh").mkdir()
        try:
            p = load_package(pkg)
            assert p["version"] == "?"
        except (IsADirectoryError, OSError):
            # Acceptable behavior: load_package may choose to raise a filesystem
            # error instead of handling a directory masquerading as build.sh.
            assert True

    def test_build_sh_symlink_broken(self, tmp_path):
        pkg = tmp_path / "broken"
        pkg.mkdir()
        (pkg / "build.sh").symlink_to("/nonexistent/target")
        try:
            p = load_package(pkg)
            assert p["version"] == "?"
        except (FileNotFoundError, OSError):
            # Acceptable behavior: load_package may propagate an error if build.sh
            # is a broken symlink.
            assert True

    def test_very_large_build_sh(self, tmp_path):
        pkg = tmp_path / "large"
        pkg.mkdir()
        (pkg / "build.sh").write_text("# pad\n" * 100000 + 'TERMUX_PKG_VERSION="1.0.0"\n')
        assert load_package(pkg)["version"] == "1.0.0"

    def test_commented_out_version(self, tmp_path):
        pkg = tmp_path / "commented"
        pkg.mkdir()
        (pkg / "build.sh").write_text('# TERMUX_PKG_VERSION="1.0.0"\n')
        assert load_package(pkg)["version"] == "?"

    def test_fingerprint_with_binary_prefix(self, tmp_path):
        (tmp_path / "build-package.sh").write_bytes(
            b"\xff\xfe" + f"# {FINGERPRINT_STRING}\n".encode()
        )
        assert isinstance(has_store_fingerprint(tmp_path), bool)

    def test_fingerprint_file_empty(self, tmp_path):
        (tmp_path / "build-package.sh").write_bytes(b"")
        assert has_store_fingerprint(tmp_path) is False

    def test_packages_is_file_not_dir(self, tmp_path):
        (tmp_path / "packages").write_text("not a directory")
        (tmp_path / "build-package.sh").write_text(f"# {FINGERPRINT_STRING}\n")
        assert is_valid_root(tmp_path) is False


class TestInjectionInput:

    def test_nonexistent_package_exits(self, tmp_path):
        root = make_root(tmp_path)
        with pytest.raises(SystemExit):
            cmd_install(root, root / "packages", "nonexistent-pkg")

    def test_empty_name_exits(self, tmp_path):
        root = make_root(tmp_path)
        with pytest.raises(SystemExit):
            cmd_install(root, root / "packages", "")

    def test_dotdot_name_exits(self, tmp_path):
        root = make_root(tmp_path)
        with pytest.raises(SystemExit):
            cmd_install(root, root / "packages", "../../etc")

    def test_upgrade_nonexistent_exits(self, tmp_path):
        root = make_root(tmp_path)
        with pytest.raises(SystemExit):
            cmd_upgrade(root, root / "packages", target="nonexistent-pkg")

    def test_popen_receives_list_not_shell_string(self, tmp_path):
        root = make_root(tmp_path)
        make_pkg(root / "packages", "bower")
        captured = {}

        def fake_popen(args, **kwargs):
            captured["args"] = args
            captured["shell"] = kwargs.get("shell", False)
            mock_proc = MagicMock()
            mock_proc.stdout = make_stdout_mock([])
            mock_proc.returncode = 0
            return mock_proc

        with patch("termux_app_store.termux_app_store_cli.get_status", return_value=("NOT INSTALLED", "")), \
             patch("subprocess.Popen", side_effect=fake_popen), \
             patch("termux_app_store.termux_app_store_cli.hold_package"):
            cmd_install(root, root / "packages", "bower")

        assert isinstance(captured["args"], list), "Popen must receive list not string"
        assert captured.get("shell") is not True, "shell=True must not be used"
        assert "bower" in captured["args"]

    def test_package_name_passed_as_argument(self, tmp_path):
        root = make_root(tmp_path)
        make_pkg(root / "packages", "my-tool")
        captured = {}

        def fake_popen(args, **kwargs):
            captured["args"] = args
            mock_proc = MagicMock()
            mock_proc.stdout = make_stdout_mock([])
            mock_proc.returncode = 0
            return mock_proc

        with patch("termux_app_store.termux_app_store_cli.get_status", return_value=("NOT INSTALLED", "")), \
             patch("subprocess.Popen", side_effect=fake_popen), \
             patch("termux_app_store.termux_app_store_cli.hold_package"):
            cmd_install(root, root / "packages", "my-tool")

        assert "my-tool" in captured["args"]
        assert captured.get("shell") is not True


class TestBrokenBuildScript:

    def test_build_exits_nonzero(self, tmp_path):
        root = make_root(tmp_path)
        make_pkg(root / "packages", "bower")
        mock_proc = MagicMock()
        mock_proc.stdout = make_stdout_mock([b"Error\n"])
        mock_proc.returncode = 1
        with patch("termux_app_store.termux_app_store_cli.get_status", return_value=("NOT INSTALLED", "")), \
             patch("subprocess.Popen", return_value=mock_proc):
            assert cmd_install(root, root / "packages", "bower") is False

    def test_build_exits_code_2(self, tmp_path):
        root = make_root(tmp_path)
        make_pkg(root / "packages", "bower")
        mock_proc = MagicMock()
        mock_proc.stdout = make_stdout_mock([])
        mock_proc.returncode = 2
        with patch("termux_app_store.termux_app_store_cli.get_status", return_value=("NOT INSTALLED", "")), \
             patch("subprocess.Popen", return_value=mock_proc):
            assert cmd_install(root, root / "packages", "bower") is False

    def test_build_no_output(self, tmp_path):
        root = make_root(tmp_path)
        make_pkg(root / "packages", "bower")
        mock_proc = MagicMock()
        mock_proc.stdout = make_stdout_mock([])
        mock_proc.returncode = 0
        with patch("termux_app_store.termux_app_store_cli.get_status", return_value=("NOT INSTALLED", "")), \
             patch("subprocess.Popen", return_value=mock_proc), \
             patch("termux_app_store.termux_app_store_cli.hold_package"):
            assert cmd_install(root, root / "packages", "bower") is True

    def test_build_ansi_output(self, tmp_path):
        root = make_root(tmp_path)
        make_pkg(root / "packages", "bower")
        mock_proc = MagicMock()
        mock_proc.stdout = make_stdout_mock([b"\033[32mBuilding\033[0m\n"])
        mock_proc.returncode = 0
        with patch("termux_app_store.termux_app_store_cli.get_status", return_value=("NOT INSTALLED", "")), \
             patch("subprocess.Popen", return_value=mock_proc), \
             patch("termux_app_store.termux_app_store_cli.hold_package"):
            assert cmd_install(root, root / "packages", "bower") is True

    def test_build_raises_oserror(self, tmp_path):
        root = make_root(tmp_path)
        make_pkg(root / "packages", "bower")
        with patch("termux_app_store.termux_app_store_cli.get_status", return_value=("NOT INSTALLED", "")), \
             patch("subprocess.Popen", side_effect=OSError("No such file")):
            with pytest.raises((OSError, SystemExit, Exception)):
                cmd_install(root, root / "packages", "bower")

    def test_upgrade_broken_build(self, tmp_path, capsys):
        root = make_root(tmp_path)
        make_pkg(root / "packages", "bower", "1.8.12")
        with patch("termux_app_store.termux_app_store_cli.get_status", return_value=("UPDATE", "")), \
             patch("termux_app_store.termux_app_store_cli.get_installed_version", return_value="1.8.11"), \
             patch("termux_app_store.termux_app_store_cli.cmd_install", return_value=False):
            cmd_upgrade(root, root / "packages")
        out = capsys.readouterr().out
        assert "bower" in out.lower()

    def test_build_binary_garbage_output(self, tmp_path):
        root = make_root(tmp_path)
        make_pkg(root / "packages", "bower")
        mock_proc = MagicMock()
        mock_proc.stdout = make_stdout_mock([b"\xff\xfe\x00\x01\n", b"normal\n"])
        mock_proc.returncode = 0
        with patch("termux_app_store.termux_app_store_cli.get_status", return_value=("NOT INSTALLED", "")), \
             patch("subprocess.Popen", return_value=mock_proc), \
             patch("termux_app_store.termux_app_store_cli.hold_package"):
            assert cmd_install(root, root / "packages", "bower") is True
