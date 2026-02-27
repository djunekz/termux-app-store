import json
import sys
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, call

sys.path.insert(0, str(Path(__file__).parent.parent))
from termux_app_store.termux_app_store_cli import (
    _ver_tuple,
    is_installed_newer_or_equal,
    has_store_fingerprint,
    is_valid_root,
    load_cached_root,
    save_cached_root,
    load_package,
    load_all_packages,
    get_installed_version,
    get_status,
    fetch_latest_tag,
    hold_package,
    unhold_package,
    cleanup_package_files,
    cmd_list,
    cmd_show,
    cmd_install,
    cmd_uninstall,
    cmd_update,
    cmd_upgrade,
    cmd_version,
    cmd_help,
    run_cli,
    FINGERPRINT_STRING,
)


class TestVerTuple:

    def test_simple(self):
        assert _ver_tuple("1.2.3") == (1, 2, 3, 0)

    def test_with_revision(self):
        assert _ver_tuple("4.10-2") == (4, 10, 2)

    def test_non_numeric_segment(self):
        assert _ver_tuple("1.alpha.3") == (1, 0, 3, 0)

    def test_non_numeric_revision(self):
        assert _ver_tuple("1.2.3-beta") == (1, 2, 3, 0)

    def test_ordering(self):
        assert _ver_tuple("1.9.0") < _ver_tuple("1.10.0")


class TestIsInstalledNewerOrEqual:

    def test_equal(self):
        assert is_installed_newer_or_equal("1.0.0", "1.0.0") is True

    def test_newer(self):
        assert is_installed_newer_or_equal("2.0.0", "1.9.9") is True

    def test_older(self):
        assert is_installed_newer_or_equal("1.0.0", "1.0.1") is False


class TestHasStoreFingerprint:

    def test_with_fingerprint(self, tmp_path):
        (tmp_path / "build-package.sh").write_text(f"# {FINGERPRINT_STRING}\nset -e\n")
        assert has_store_fingerprint(tmp_path) is True

    def test_without_fingerprint(self, tmp_path):
        (tmp_path / "build-package.sh").write_text("# some other script\nset -e\n")
        assert has_store_fingerprint(tmp_path) is False

    def test_no_file(self, tmp_path):
        assert has_store_fingerprint(tmp_path) is False

    def test_fingerprint_after_20_lines(self, tmp_path):
        lines = ["# line\n"] * 25 + [f"# {FINGERPRINT_STRING}\n"]
        (tmp_path / "build-package.sh").write_text("".join(lines))
        assert has_store_fingerprint(tmp_path) is False


class TestIsValidRoot:

    def test_valid(self, tmp_path):
        (tmp_path / "packages").mkdir()
        (tmp_path / "build-package.sh").write_text(f"# {FINGERPRINT_STRING}\n")
        assert is_valid_root(tmp_path) is True

    def test_missing_packages(self, tmp_path):
        (tmp_path / "build-package.sh").write_text(f"# {FINGERPRINT_STRING}\n")
        assert is_valid_root(tmp_path) is False

    def test_missing_build_package_sh(self, tmp_path):
        (tmp_path / "packages").mkdir()
        assert is_valid_root(tmp_path) is False

    def test_not_a_dir(self, tmp_path):
        assert is_valid_root(tmp_path / "nonexistent") is False


class TestCacheRoot:

    def test_save_and_load(self, tmp_path):
        cache = tmp_path / "cache.json"
        root = tmp_path / "root"
        root.mkdir()
        (root / "packages").mkdir()
        (root / "build-package.sh").write_text(f"# {FINGERPRINT_STRING}\n")

        with patch("termux_app_store.termux_app_store_cli.CACHE_FILE", cache):
            save_cached_root(root)
            assert cache.exists()
            result = load_cached_root()

        assert result == root.resolve()

    def test_load_invalid_path(self, tmp_path):
        cache = tmp_path / "cache.json"
        cache.write_text(json.dumps({"app_root": "/nonexistent/path"}))
        with patch("termux_app_store.termux_app_store_cli.CACHE_FILE", cache):
            assert load_cached_root() is None

    def test_load_missing_cache(self, tmp_path):
        cache = tmp_path / "nonexistent.json"
        with patch("termux_app_store.termux_app_store_cli.CACHE_FILE", cache):
            assert load_cached_root() is None

    def test_load_corrupt_cache(self, tmp_path):
        cache = tmp_path / "cache.json"
        cache.write_text("{ broken {{{")
        with patch("termux_app_store.termux_app_store_cli.CACHE_FILE", cache):
            assert load_cached_root() is None

    def test_save_creates_parent_dirs(self, tmp_path):
        cache = tmp_path / "deep" / "nested" / "cache.json"
        with patch("termux_app_store.termux_app_store_cli.CACHE_FILE", cache):
            save_cached_root(tmp_path)
        assert cache.exists()


class TestLoadPackage:

    def test_all_fields(self, tmp_path):
        pkg = tmp_path / "bower"
        pkg.mkdir()
        (pkg / "build.sh").write_text(
            'TERMUX_PKG_DESCRIPTION="A package manager"\n'
            'TERMUX_PKG_VERSION="1.8.12"\n'
            'TERMUX_PKG_DEPENDS="nodejs"\n'
            'TERMUX_PKG_MAINTAINER="@djunekz"\n'
            'TERMUX_PKG_HOMEPAGE="https://bower.io"\n'
            'TERMUX_PKG_LICENSE="MIT"\n'
        )
        p = load_package(pkg)
        assert p["name"] == "bower"
        assert p["version"] == "1.8.12"
        assert p["desc"] == "A package manager"
        assert p["deps"] == "nodejs"
        assert p["maintainer"] == "@djunekz"
        assert p["homepage"] == "https://bower.io"
        assert p["license"] == "MIT"

    def test_defaults_when_no_build_sh(self, tmp_path):
        pkg = tmp_path / "empty"
        pkg.mkdir()
        p = load_package(pkg)
        assert p["version"] == "?"
        assert p["desc"] == "-"

    def test_defaults_when_empty_build_sh(self, tmp_path):
        pkg = tmp_path / "empty"
        pkg.mkdir()
        (pkg / "build.sh").write_text("")
        p = load_package(pkg)
        assert p["version"] == "?"


class TestLoadAllPackages:

    def test_loads_multiple(self, tmp_path):
        for name in ["aaa", "zzz", "mmm"]:
            (tmp_path / name).mkdir()
            (tmp_path / name / "build.sh").write_text(f'TERMUX_PKG_VERSION="1.0"\n')
        pkgs = load_all_packages(tmp_path)
        assert len(pkgs) == 3
        assert pkgs[0]["name"] == "aaa"

    def test_skips_without_build_sh(self, tmp_path):
        (tmp_path / "nosh").mkdir()
        pkgs = load_all_packages(tmp_path)
        assert pkgs == []


class TestGetInstalledVersion:

    def test_installed(self):
        with patch("subprocess.check_output", return_value="install ok installed\t1.8.12"):
            assert get_installed_version("bower") == "1.8.12"

    def test_not_installed_status(self):
        with patch("subprocess.check_output", return_value="deinstall ok config-files\t"):
            assert get_installed_version("bower") is None

    def test_empty_output(self):
        with patch("subprocess.check_output", return_value=""):
            assert get_installed_version("bower") is None

    def test_exception(self):
        with patch("subprocess.check_output", side_effect=Exception("not found")):
            assert get_installed_version("bower") is None


class TestGetStatus:

    def test_not_installed(self):
        with patch("termux_app_store.termux_app_store_cli.get_installed_version", return_value=None):
            status, label = get_status("bower", "1.8.12")
        assert status == "NOT INSTALLED"

    def test_installed_up_to_date(self):
        with patch("termux_app_store.termux_app_store_cli.get_installed_version", return_value="1.8.12"):
            status, label = get_status("bower", "1.8.12")
        assert status == "INSTALLED"

    def test_update_available(self):
        with patch("termux_app_store.termux_app_store_cli.get_installed_version", return_value="1.8.11"):
            status, label = get_status("bower", "1.8.12")
        assert status == "UPDATE"


class TestFetchLatestTag:

    def test_success(self):
        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps({"tag_name": "v0.1.6"}).encode()
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)
        with patch("urllib.request.urlopen", return_value=mock_resp):
            assert fetch_latest_tag() == "v0.1.6"

    def test_failure(self):
        with patch("urllib.request.urlopen", side_effect=Exception("timeout")):
            assert fetch_latest_tag() is None


class TestHoldUnhold:

    def test_hold(self):
        with patch("subprocess.call") as mock_call:
            hold_package("bower")
            mock_call.assert_called_once()

    def test_unhold(self):
        with patch("subprocess.call") as mock_call:
            unhold_package("bower")
            mock_call.assert_called_once()

    def test_hold_exception(self):
        with patch("subprocess.call", side_effect=Exception("no apt-mark")):
            hold_package("bower")  # should not raise

    def test_unhold_exception(self):
        with patch("subprocess.call", side_effect=Exception("no apt-mark")):
            unhold_package("bower")  # should not raise


class TestCleanupPackageFiles:

    def test_removes_existing(self, tmp_path):
        lib = tmp_path / "lib" / "bower"
        lib.mkdir(parents=True)
        (lib / "file.txt").write_text("x")
        with patch.dict("os.environ", {"PREFIX": str(tmp_path)}):
            count = cleanup_package_files("bower")
        assert count >= 1
        assert not lib.exists()

    def test_nothing_to_remove(self, tmp_path):
        with patch.dict("os.environ", {"PREFIX": str(tmp_path)}):
            count = cleanup_package_files("nonexistent")
        assert count == 0


class TestCmdList:

    def test_empty(self, tmp_path, capsys):
        cmd_list(tmp_path)
        out = capsys.readouterr().out
        assert "No packages found" in out

    def test_with_packages(self, tmp_path, capsys):
        (tmp_path / "bower").mkdir()
        (tmp_path / "bower" / "build.sh").write_text('TERMUX_PKG_VERSION="1.8.12"\n')
        with patch("termux_app_store.termux_app_store_cli.get_status", return_value=("INSTALLED", "up-to-date")):
            cmd_list(tmp_path)
        out = capsys.readouterr().out
        assert "bower" in out


class TestCmdShow:

    def test_not_found(self, tmp_path):
        with pytest.raises(SystemExit):
            cmd_show(tmp_path, "nonexistent")

    def test_found(self, tmp_path, capsys):
        (tmp_path / "bower").mkdir()
        (tmp_path / "bower" / "build.sh").write_text('TERMUX_PKG_VERSION="1.8.12"\n')
        with patch("termux_app_store.termux_app_store_cli.get_status", return_value=("INSTALLED", "up-to-date")):
            cmd_show(tmp_path, "bower")
        out = capsys.readouterr().out
        assert "bower" in out
        assert "1.8.12" in out


class TestCmdInstall:

    def _make_pkg(self, root, name, version="1.0.0"):
        (root / name).mkdir(parents=True, exist_ok=True)
        (root / name / "build.sh").write_text(f'TERMUX_PKG_VERSION="{version}"\n')

    def test_not_found(self, tmp_path):
        with pytest.raises(SystemExit):
            cmd_install(tmp_path, tmp_path, "nonexistent")

    def test_already_installed(self, tmp_path, capsys):
        self._make_pkg(tmp_path, "bower", "1.8.12")
        with patch("termux_app_store.termux_app_store_cli.get_status", return_value=("INSTALLED", "up-to-date")):
            result = cmd_install(tmp_path, tmp_path, "bower")
        assert result is True

    def test_install_success(self, tmp_path):
        self._make_pkg(tmp_path, "bower")
        mock_proc = MagicMock()
        mock_proc.stdout = iter([b"Installing...\n"])
        mock_proc.returncode = 0
        mock_proc.wait = MagicMock()
        with patch("termux_app_store.termux_app_store_cli.get_status", return_value=("NOT INSTALLED", "")), \
             patch("subprocess.Popen", return_value=mock_proc), \
             patch("termux_app_store.termux_app_store_cli.hold_package"):
            result = cmd_install(tmp_path, tmp_path, "bower")
        assert result is True

    def test_install_fail(self, tmp_path):
        self._make_pkg(tmp_path, "bower")
        mock_proc = MagicMock()
        mock_proc.stdout = iter([])
        mock_proc.returncode = 1
        mock_proc.wait = MagicMock()
        with patch("termux_app_store.termux_app_store_cli.get_status", return_value=("NOT INSTALLED", "")), \
             patch("subprocess.Popen", return_value=mock_proc):
            result = cmd_install(tmp_path, tmp_path, "bower")
        assert result is False


class TestCmdUninstall:

    def test_not_installed(self, tmp_path, capsys):
        with patch("termux_app_store.termux_app_store_cli.get_installed_version", return_value=None):
            cmd_uninstall("bower")
        out = capsys.readouterr().out
        assert "not installed" in out

    def test_uninstall_success(self, tmp_path):
        with patch("termux_app_store.termux_app_store_cli.get_installed_version", return_value="1.8.12"), \
             patch("subprocess.call", return_value=0), \
             patch("termux_app_store.termux_app_store_cli.unhold_package"), \
             patch("termux_app_store.termux_app_store_cli.cleanup_package_files", return_value=0), \
             patch.dict("os.environ", {"PREFIX": str(tmp_path)}):
            cmd_uninstall("bower")

    def test_uninstall_fail(self, tmp_path):
        with patch("termux_app_store.termux_app_store_cli.get_installed_version", return_value="1.8.12"), \
             patch("subprocess.call", return_value=1), \
             patch("termux_app_store.termux_app_store_cli.unhold_package"), \
             patch("termux_app_store.termux_app_store_cli.hold_package"), \
             patch.dict("os.environ", {"PREFIX": str(tmp_path)}):
            with pytest.raises(SystemExit):
                cmd_uninstall("bower")


class TestCmdUpdate:

    def test_all_up_to_date(self, tmp_path, capsys):
        (tmp_path / "bower").mkdir()
        (tmp_path / "bower" / "build.sh").write_text('TERMUX_PKG_VERSION="1.8.12"\n')
        with patch("termux_app_store.termux_app_store_cli.get_status", return_value=("INSTALLED", "")):
            cmd_update(tmp_path)
        out = capsys.readouterr().out
        assert "up-to-date" in out

    def test_with_updates(self, tmp_path, capsys):
        (tmp_path / "bower").mkdir()
        (tmp_path / "bower" / "build.sh").write_text('TERMUX_PKG_VERSION="1.8.12"\n')

        def mock_status(name, version):
            return ("UPDATE", "update available")

        with patch("termux_app_store.termux_app_store_cli.get_status", side_effect=mock_status), \
             patch("termux_app_store.termux_app_store_cli.get_installed_version", return_value="1.8.11"):
            cmd_update(tmp_path)
        out = capsys.readouterr().out
        assert "update" in out.lower()

    def test_skips_not_installed(self, tmp_path, capsys):
        (tmp_path / "bower").mkdir()
        (tmp_path / "bower" / "build.sh").write_text('TERMUX_PKG_VERSION="1.8.12"\n')
        with patch("termux_app_store.termux_app_store_cli.get_status", return_value=("NOT INSTALLED", "")):
            cmd_update(tmp_path)


class TestCmdUpgrade:

    def _make_pkg(self, root, name, version="1.0.0"):
        (root / name).mkdir(parents=True, exist_ok=True)
        (root / name / "build.sh").write_text(f'TERMUX_PKG_VERSION="{version}"\n')

    def test_nothing_to_upgrade(self, tmp_path, capsys):
        self._make_pkg(tmp_path, "bower")
        with patch("termux_app_store.termux_app_store_cli.get_status", return_value=("INSTALLED", "")):
            cmd_upgrade(tmp_path, tmp_path)
        out = capsys.readouterr().out
        assert "up-to-date" in out

    def test_upgrade_all(self, tmp_path, capsys):
        self._make_pkg(tmp_path, "bower", "1.8.12")
        with patch("termux_app_store.termux_app_store_cli.get_status", return_value=("UPDATE", "")), \
             patch("termux_app_store.termux_app_store_cli.get_installed_version", return_value="1.8.11"), \
             patch("termux_app_store.termux_app_store_cli.cmd_install", return_value=True):
            cmd_upgrade(tmp_path, tmp_path)
        out = capsys.readouterr().out
        assert "bower" in out

    def test_upgrade_specific_not_found(self, tmp_path):
        with pytest.raises(SystemExit):
            cmd_upgrade(tmp_path, tmp_path, target="nonexistent")

    def test_upgrade_specific_not_installed(self, tmp_path, capsys):
        self._make_pkg(tmp_path, "bower")
        with patch("termux_app_store.termux_app_store_cli.get_status", return_value=("NOT INSTALLED", "")):
            cmd_upgrade(tmp_path, tmp_path, target="bower")
        out = capsys.readouterr().out
        assert "not installed" in out.lower()

    def test_upgrade_specific_already_up_to_date(self, tmp_path, capsys):
        self._make_pkg(tmp_path, "bower")
        with patch("termux_app_store.termux_app_store_cli.get_status", return_value=("INSTALLED", "")):
            cmd_upgrade(tmp_path, tmp_path, target="bower")
        out = capsys.readouterr().out
        assert "up-to-date" in out

    def test_upgrade_specific_do_upgrade(self, tmp_path):
        self._make_pkg(tmp_path, "bower", "1.8.12")
        with patch("termux_app_store.termux_app_store_cli.get_status", return_value=("UPDATE", "")), \
             patch("termux_app_store.termux_app_store_cli.cmd_install", return_value=True) as mock_install:
            cmd_upgrade(tmp_path, tmp_path, target="bower")
        mock_install.assert_called_once()

    def test_upgrade_with_failure(self, tmp_path, capsys):
        self._make_pkg(tmp_path, "bower", "1.8.12")
        with patch("termux_app_store.termux_app_store_cli.get_status", return_value=("UPDATE", "")), \
             patch("termux_app_store.termux_app_store_cli.get_installed_version", return_value="1.8.11"), \
             patch("termux_app_store.termux_app_store_cli.cmd_install", return_value=False):
            cmd_upgrade(tmp_path, tmp_path)
        out = capsys.readouterr().out
        assert "failed" in out.lower()


class TestCmdVersion:

    def test_success(self, capsys):
        with patch("termux_app_store.termux_app_store_cli.fetch_latest_tag", return_value="v0.1.6"):
            cmd_version()
        out = capsys.readouterr().out
        assert "v0.1.6" in out

    def test_failure(self, capsys):
        with patch("termux_app_store.termux_app_store_cli.fetch_latest_tag", return_value=None):
            cmd_version()
        out = capsys.readouterr().out
        assert "Could not fetch" in out


class TestCmdHelp:

    def test_prints_help(self, capsys):
        cmd_help()
        out = capsys.readouterr().out
        assert "USAGE" in out
        assert "install" in out


class TestRunCli:

    def test_unknown_command(self):
        with patch("sys.argv", ["termux-app-store", "badcmd"]):
            with pytest.raises(SystemExit):
                run_cli()

    def test_help(self, capsys):
        with patch("sys.argv", ["termux-app-store", "help"]):
            run_cli()
        assert "USAGE" in capsys.readouterr().out

    def test_version(self, capsys):
        with patch("sys.argv", ["termux-app-store", "version"]), \
             patch("termux_app_store.termux_app_store_cli.fetch_latest_tag", return_value="v0.1.6"):
            run_cli()
        assert "v0.1.6" in capsys.readouterr().out

    def test_no_args_tui(self):
        mock_tui = MagicMock()
        with patch("sys.argv", ["termux-app-store"]), \
             patch.dict("sys.modules", {"termux_app_store": MagicMock(TermuxAppStore=mock_tui)}):
            run_cli()

    def test_no_args_import_error(self, capsys):
        with patch("sys.argv", ["termux-app-store"]), \
             patch("builtins.__import__", side_effect=ImportError("no tui")):
            run_cli()

    def _make_valid_root(self, tmp_path):
        (tmp_path / "packages").mkdir()
        (tmp_path / "build-package.sh").write_text(f"# {FINGERPRINT_STRING}\n")
        return tmp_path

    def test_list(self, tmp_path, capsys):
        root = self._make_valid_root(tmp_path)
        with patch("sys.argv", ["termux-app-store", "list"]), \
             patch("termux_app_store.termux_app_store_cli.resolve_app_root", return_value=root):
            run_cli()
        assert "No packages found" in capsys.readouterr().out

    def test_show_missing_arg(self, tmp_path):
        root = self._make_valid_root(tmp_path)
        with patch("sys.argv", ["termux-app-store", "show"]), \
             patch("termux_app_store.termux_app_store_cli.resolve_app_root", return_value=root):
            with pytest.raises(SystemExit):
                run_cli()

    def test_install_missing_arg(self, tmp_path):
        root = self._make_valid_root(tmp_path)
        with patch("sys.argv", ["termux-app-store", "install"]), \
             patch("termux_app_store.termux_app_store_cli.resolve_app_root", return_value=root):
            with pytest.raises(SystemExit):
                run_cli()

    def test_uninstall_missing_arg(self, tmp_path):
        root = self._make_valid_root(tmp_path)
        with patch("sys.argv", ["termux-app-store", "uninstall"]), \
             patch("termux_app_store.termux_app_store_cli.resolve_app_root", return_value=root):
            with pytest.raises(SystemExit):
                run_cli()

    def test_update(self, tmp_path, capsys):
        root = self._make_valid_root(tmp_path)
        with patch("sys.argv", ["termux-app-store", "update"]), \
             patch("termux_app_store.termux_app_store_cli.resolve_app_root", return_value=root):
            run_cli()

    def test_upgrade_no_target(self, tmp_path, capsys):
        root = self._make_valid_root(tmp_path)
        with patch("sys.argv", ["termux-app-store", "upgrade"]), \
             patch("termux_app_store.termux_app_store_cli.resolve_app_root", return_value=root):
            run_cli()

    def test_upgrade_with_target(self, tmp_path):
        root = self._make_valid_root(tmp_path)
        with patch("sys.argv", ["termux-app-store", "upgrade", "bower"]), \
             patch("termux_app_store.termux_app_store_cli.resolve_app_root", return_value=root):
            with pytest.raises(SystemExit):
                run_cli()
