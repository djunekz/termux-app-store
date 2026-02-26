"""
Tests untuk package loading, fingerprint detection, dan root validation.
"""

import pytest
from pathlib import Path
from tests.conftest import make_build_sh, make_valid_root


# ── Fungsi yang ditest (copy dari termux_app_store_cli.py) ───────────────────

FINGERPRINT_STRING = "Termux App Store Official"


def has_store_fingerprint(path: Path) -> bool:
    build = path / "build-package.sh"
    if not build.exists():
        return False
    try:
        with build.open(errors="ignore") as f:
            for _ in range(20):
                line = f.readline()
                if not line:
                    break
                if FINGERPRINT_STRING in line:
                    return True
    except Exception:
        pass
    return False


def is_valid_root(path: Path) -> bool:
    return (
        path.is_dir()
        and (path / "packages").is_dir()
        and (path / "build-package.sh").is_file()
        and has_store_fingerprint(path)
    )


def load_package(pkg_dir: Path) -> dict:
    data = {
        "name":       pkg_dir.name,
        "desc":       "-",
        "version":    "?",
        "deps":       "-",
        "maintainer": "-",
        "homepage":   "-",
        "license":    "-",
    }
    build = pkg_dir / "build.sh"
    if not build.exists():
        return data
    with build.open(errors="ignore") as f:
        for line in f:
            for key, field in [
                ("TERMUX_PKG_DESCRIPTION=", "desc"),
                ("TERMUX_PKG_VERSION=",     "version"),
                ("TERMUX_PKG_DEPENDS=",     "deps"),
                ("TERMUX_PKG_MAINTAINER=",  "maintainer"),
                ("TERMUX_PKG_HOMEPAGE=",    "homepage"),
                ("TERMUX_PKG_LICENSE=",     "license"),
            ]:
                if line.startswith(key):
                    data[field] = line.split("=", 1)[1].strip().strip('"')
    return data


def load_all_packages(packages_dir: Path) -> list:
    pkgs = []
    for pkg_dir in sorted(packages_dir.iterdir()):
        if (pkg_dir / "build.sh").exists():
            pkgs.append(load_package(pkg_dir))
    return pkgs


# ── Tests: has_store_fingerprint ─────────────────────────────────────────────

class TestHasStoreFingerprint:

    def test_valid_fingerprint(self, tmp_path):
        make_valid_root(tmp_path, with_fingerprint=True)
        assert has_store_fingerprint(tmp_path) is True

    def test_missing_fingerprint(self, tmp_path):
        make_valid_root(tmp_path, with_fingerprint=False)
        assert has_store_fingerprint(tmp_path) is False

    def test_no_build_package_sh(self, tmp_path):
        assert has_store_fingerprint(tmp_path) is False

    def test_fingerprint_on_line_1(self, tmp_path):
        (tmp_path / "build-package.sh").write_text("# Termux App Store Official\n")
        assert has_store_fingerprint(tmp_path) is True

    def test_fingerprint_on_line_19(self, tmp_path):
        lines = ["# padding\n"] * 18 + ["# Termux App Store Official\n"]
        (tmp_path / "build-package.sh").write_text("".join(lines))
        assert has_store_fingerprint(tmp_path) is True

    def test_fingerprint_beyond_line_20(self, tmp_path):
        lines = ["# padding\n"] * 25 + ["# Termux App Store Official\n"]
        (tmp_path / "build-package.sh").write_text("".join(lines))
        assert has_store_fingerprint(tmp_path) is False

    def test_empty_file(self, tmp_path):
        (tmp_path / "build-package.sh").write_text("")
        assert has_store_fingerprint(tmp_path) is False


# ── Tests: is_valid_root ──────────────────────────────────────────────────────

class TestIsValidRoot:

    def test_fully_valid(self, tmp_path):
        make_valid_root(tmp_path)
        assert is_valid_root(tmp_path) is True

    def test_missing_packages_dir(self, tmp_path):
        (tmp_path / "build-package.sh").write_text("# Termux App Store Official\n")
        assert is_valid_root(tmp_path) is False

    def test_missing_build_package_sh(self, tmp_path):
        (tmp_path / "packages").mkdir()
        assert is_valid_root(tmp_path) is False

    def test_wrong_fingerprint(self, tmp_path):
        (tmp_path / "packages").mkdir()
        (tmp_path / "build-package.sh").write_text("# unrelated script\n")
        assert is_valid_root(tmp_path) is False

    def test_nonexistent_path(self, tmp_path):
        assert is_valid_root(tmp_path / "does_not_exist") is False

    def test_file_not_dir(self, tmp_path):
        f = tmp_path / "somefile"
        f.write_text("hello")
        assert is_valid_root(f) is False


# ── Tests: load_package ───────────────────────────────────────────────────────

class TestLoadPackage:

    def test_all_fields_present(self, tmp_path):
        pkg_dir = make_build_sh(tmp_path, "mytool", {
            "TERMUX_PKG_DESCRIPTION": "My cool tool",
            "TERMUX_PKG_VERSION":     "1.2.3",
            "TERMUX_PKG_DEPENDS":     "nodejs,python",
            "TERMUX_PKG_MAINTAINER":  "@djunekz",
            "TERMUX_PKG_HOMEPAGE":    "https://example.com",
            "TERMUX_PKG_LICENSE":     "MIT",
        })
        p = load_package(pkg_dir)
        assert p["name"]       == "mytool"
        assert p["desc"]       == "My cool tool"
        assert p["version"]    == "1.2.3"
        assert p["deps"]       == "nodejs,python"
        assert p["maintainer"] == "@djunekz"
        assert p["homepage"]   == "https://example.com"
        assert p["license"]    == "MIT"

    def test_no_build_sh_returns_defaults(self, tmp_path):
        pkg_dir = tmp_path / "packages" / "ghostpkg"
        pkg_dir.mkdir(parents=True)
        p = load_package(pkg_dir)
        assert p["name"]    == "ghostpkg"
        assert p["version"] == "?"
        assert p["desc"]    == "-"
        assert p["deps"]    == "-"

    def test_partial_fields(self, tmp_path):
        pkg_dir = make_build_sh(tmp_path, "partial", {
            "TERMUX_PKG_VERSION": "2.0",
        })
        p = load_package(pkg_dir)
        assert p["version"] == "2.0"
        assert p["desc"]    == "-"
        assert p["deps"]    == "-"

    def test_name_from_dirname(self, tmp_path):
        pkg_dir = make_build_sh(tmp_path, "my-tool-v2", {
            "TERMUX_PKG_VERSION": "1.0",
        })
        assert load_package(pkg_dir)["name"] == "my-tool-v2"

    def test_quoted_values_stripped(self, tmp_path):
        pkg_dir = tmp_path / "packages" / "quoted"
        pkg_dir.mkdir(parents=True)
        (pkg_dir / "build.sh").write_text(
            'TERMUX_PKG_VERSION="3.0.1"\n'
            'TERMUX_PKG_DESCRIPTION="A tool with spaces"\n'
        )
        p = load_package(pkg_dir)
        assert p["version"] == "3.0.1"
        assert p["desc"]    == "A tool with spaces"

    def test_real_package_bower(self, tmp_path):
        pkg_dir = make_build_sh(tmp_path, "bower", {
            "TERMUX_PKG_DESCRIPTION": "A package manager for the web",
            "TERMUX_PKG_VERSION":     "1.8.12",
            "TERMUX_PKG_DEPENDS":     "nodejs",
            "TERMUX_PKG_LICENSE":     "MIT",
            "TERMUX_PKG_HOMEPAGE":    "https://github.com/bower/bower",
        })
        p = load_package(pkg_dir)
        assert p["name"]    == "bower"
        assert p["version"] == "1.8.12"
        assert p["deps"]    == "nodejs"

    def test_real_package_tuifimanager(self, tmp_path):
        pkg_dir = make_build_sh(tmp_path, "tuifimanager", {
            "TERMUX_PKG_VERSION": "5.2.6",
            "TERMUX_PKG_DEPENDS": "python",
            "TERMUX_PKG_LICENSE": "MIT",
        })
        p = load_package(pkg_dir)
        assert p["version"] == "5.2.6"
        assert p["deps"]    == "python"


# ── Tests: load_all_packages ──────────────────────────────────────────────────

class TestLoadAllPackages:

    def test_returns_sorted_by_name(self, tmp_path):
        make_valid_root(tmp_path)
        for name in ["zx", "aircrack-ng", "bower", "tuifimanager"]:
            make_build_sh(tmp_path, name, {"TERMUX_PKG_VERSION": "1.0"})
        pkgs = load_all_packages(tmp_path / "packages")
        names = [p["name"] for p in pkgs]
        assert names == sorted(names)

    def test_skips_dirs_without_build_sh(self, tmp_path):
        make_valid_root(tmp_path)
        make_build_sh(tmp_path, "validpkg", {"TERMUX_PKG_VERSION": "1.0"})
        (tmp_path / "packages" / "nodotbuildsh").mkdir()
        pkgs = load_all_packages(tmp_path / "packages")
        names = [p["name"] for p in pkgs]
        assert "validpkg" in names
        assert "nodotbuildsh" not in names

    def test_empty_packages_dir(self, tmp_path):
        make_valid_root(tmp_path)
        assert load_all_packages(tmp_path / "packages") == []

    def test_correct_count(self, tmp_path):
        make_valid_root(tmp_path)
        for i in range(6):
            make_build_sh(tmp_path, f"pkg{i:02d}", {"TERMUX_PKG_VERSION": f"1.{i}"})
        pkgs = load_all_packages(tmp_path / "packages")
        assert len(pkgs) == 6

    def test_all_packages_have_required_keys(self, tmp_path):
        make_valid_root(tmp_path)
        make_build_sh(tmp_path, "tool", {"TERMUX_PKG_VERSION": "1.0"})
        pkgs = load_all_packages(tmp_path / "packages")
        required = {"name", "desc", "version", "deps", "maintainer", "homepage", "license"}
        for p in pkgs:
            assert required.issubset(p.keys())
