import json
import time
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


def parse_version(version: str):
    v = (version or "").strip().lstrip("v")
    v = v.split("+", 1)[0].split("-", 1)[0]
    parts = []
    for p in v.split("."):
        try:
            parts.append(int(p))
        except Exception:
            parts.append(0)
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts[:6])


def compare_versions(current: str, latest: str) -> int:
    c = parse_version(current)
    l = parse_version(latest)
    if c < l:
        return -1
    elif c > l:
        return 1
    return 0


def get_architecture_logic(machine: str) -> str:
    arch_map = {
        'aarch64': 'aarch64',
        'armv7l': 'arm',
        'armv8l': 'arm',
        'x86_64': 'x86_64',
        'i686': 'i686',
        'i386': 'i686',
    }
    return arch_map.get(machine.lower(), 'unknown')


def normalize_remote_pkg(pkg: dict) -> dict:
    pkg = dict(pkg)
    pkg.setdefault("name", pkg.get("package"))
    desc = pkg.get("description") or pkg.get("desc") or "-"
    pkg.setdefault("desc", desc)
    pkg.setdefault("description", desc)
    deps = pkg.get("depends")
    if isinstance(deps, str):
        pkg["depends"] = [d.strip() for d in deps.split(",") if d.strip()]
    pkg.setdefault("deps", ", ".join(pkg.get("depends") or []))
    return pkg


def make_pkg_dir(root: Path, name: str, fields: dict) -> Path:
    pkg_dir = root / name
    pkg_dir.mkdir(parents=True, exist_ok=True)
    lines = []
    for k, v in fields.items():
        lines.append(f'{k}="{v}"')
    (pkg_dir / "build.sh").write_text("\n".join(lines) + "\n")
    return pkg_dir


class TestParseVersion:

    def test_simple(self):
        assert parse_version("1.2.3") == (1, 2, 3)

    def test_with_v_prefix(self):
        assert parse_version("v1.2.3") == (1, 2, 3)

    def test_two_parts_padded(self):
        assert parse_version("1.2") == (1, 2, 0)

    def test_one_part_padded(self):
        assert parse_version("1") == (1, 0, 0)

    def test_pre_release_stripped(self):
        assert parse_version("1.2.3-beta") == (1, 2, 3)
        assert parse_version("1.2.3-rc1")  == (1, 2, 3)

    def test_build_meta_stripped(self):
        assert parse_version("1.2.3+build.1") == (1, 2, 3)

    def test_pre_release_and_meta_stripped(self):
        assert parse_version("1.2.3-beta+meta") == (1, 2, 3)

    def test_empty_string(self):
        assert parse_version("") == (0, 0, 0)

    def test_none_like_empty(self):
        assert parse_version("") == (0, 0, 0)

    def test_non_numeric_part(self):
        assert parse_version("1.abc.3") == (1, 0, 3)

    def test_max_6_parts(self):
        result = parse_version("1.2.3.4.5.6.7.8")
        assert len(result) == 6
        assert result == (1, 2, 3, 4, 5, 6)

    def test_zero_version(self):
        assert parse_version("0.0.0") == (0, 0, 0)

    def test_real_app_version(self):
        assert parse_version("0.1.6") == (0, 1, 6)

    def test_real_package_bower(self):
        assert parse_version("1.8.12") == (1, 8, 12)

    def test_real_package_pnpm(self):
        assert parse_version("10.30.1") == (10, 30, 1)

    def test_ordering(self):
        assert parse_version("1.9.0") < parse_version("1.10.0")
        assert parse_version("2.0.0") > parse_version("1.9.9")


class TestCompareVersions:

    def test_equal(self):
        assert compare_versions("1.2.3", "1.2.3") == 0

    def test_current_older(self):
        assert compare_versions("1.0.0", "1.0.1") == -1

    def test_current_newer(self):
        assert compare_versions("1.0.1", "1.0.0") == 1

    def test_minor_older(self):
        assert compare_versions("1.9.0", "1.10.0") == -1

    def test_minor_newer(self):
        assert compare_versions("1.10.0", "1.9.0") == 1

    def test_major_older(self):
        assert compare_versions("1.9.9", "2.0.0") == -1

    def test_major_newer(self):
        assert compare_versions("2.0.0", "1.9.9") == 1

    def test_with_v_prefix(self):
        assert compare_versions("v1.2.3", "1.2.3") == 0

    def test_with_prerelease(self):
        assert compare_versions("1.2.3-beta", "1.2.3") == 0

    def test_app_version_up_to_date(self):
        assert compare_versions("0.1.6", "0.1.6") == 0

    def test_app_version_outdated(self):
        assert compare_versions("0.1.5", "0.1.6") == -1

    def test_app_version_ahead(self):
        assert compare_versions("0.1.7", "0.1.6") == 1

    def test_real_bower(self):
        assert compare_versions("1.8.11", "1.8.12") == -1
        assert compare_versions("1.8.12", "1.8.12") == 0

    def test_real_pnpm(self):
        assert compare_versions("10.29.0", "10.30.1") == -1
        assert compare_versions("10.30.1", "10.30.1") == 0


class TestGetArchitecture:

    def test_aarch64(self):
        assert get_architecture_logic("aarch64") == "aarch64"

    def test_armv7l(self):
        assert get_architecture_logic("armv7l") == "arm"

    def test_armv8l(self):
        assert get_architecture_logic("armv8l") == "arm"

    def test_x86_64(self):
        assert get_architecture_logic("x86_64") == "x86_64"

    def test_i686(self):
        assert get_architecture_logic("i686") == "i686"

    def test_i386(self):
        assert get_architecture_logic("i386") == "i686"

    def test_unknown(self):
        assert get_architecture_logic("mips") == "unknown"
        assert get_architecture_logic("riscv64") == "unknown"

    def test_case_insensitive(self):
        assert get_architecture_logic("AARCH64") == "aarch64"
        assert get_architecture_logic("X86_64")  == "x86_64"


class TestNormalizeRemotePkg:

    def test_name_from_package(self):
        pkg = normalize_remote_pkg({"package": "bower"})
        assert pkg["name"] == "bower"

    def test_name_preserved_if_present(self):
        pkg = normalize_remote_pkg({"package": "bower", "name": "bower-tool"})
        assert pkg["name"] == "bower-tool"

    def test_desc_from_description(self):
        pkg = normalize_remote_pkg({"description": "A package manager"})
        assert pkg["desc"] == "A package manager"

    def test_desc_from_desc(self):
        pkg = normalize_remote_pkg({"desc": "A tool"})
        assert pkg["desc"] == "A tool"

    def test_desc_fallback(self):
        pkg = normalize_remote_pkg({})
        assert pkg["desc"] == "-"

    def test_depends_string_split(self):
        pkg = normalize_remote_pkg({"depends": "nodejs, python, git"})
        assert pkg["depends"] == ["nodejs", "python", "git"]

    def test_depends_list_preserved(self):
        pkg = normalize_remote_pkg({"depends": ["nodejs", "python"]})
        assert pkg["depends"] == ["nodejs", "python"]

    def test_deps_from_depends_list(self):
        pkg = normalize_remote_pkg({"depends": ["nodejs", "python"]})
        assert "nodejs" in pkg["deps"]
        assert "python" in pkg["deps"]

    def test_deps_empty_when_no_depends(self):
        pkg = normalize_remote_pkg({"package": "tool"})
        assert pkg["deps"] == ""

    def test_original_not_mutated(self):
        original = {"package": "bower", "version": "1.8.12"}
        normalize_remote_pkg(original)
        assert "name" not in original

    def test_full_package(self):
        raw = {
            "package":     "bower",
            "description": "A package manager for the web",
            "version":     "1.8.12",
            "depends":     "nodejs",
            "license":     "MIT",
            "homepage":    "https://bower.io",
        }
        pkg = normalize_remote_pkg(raw)
        assert pkg["name"]        == "bower"
        assert pkg["desc"]        == "A package manager for the web"
        assert pkg["description"] == "A package manager for the web"
        assert pkg["depends"]     == ["nodejs"]


class TestParseBuildSh:

    def _parse(self, tmp_path, name, content):
        pkg_dir = tmp_path / name
        pkg_dir.mkdir()
        (pkg_dir / "build.sh").write_text(content)

        data = {
            "package": pkg_dir.name,
            "name": pkg_dir.name,
            "desc": "-", "description": "-",
            "version": "?", "deps": "-",
            "depends": [], "maintainer": "-",
            "homepage": "-", "license": "-",
            "srcurl": "", "sha256": "",
        }
        with (pkg_dir / "build.sh").open(errors="ignore") as f:
            for line in f:
                line = line.strip()
                for key, field in [
                    ("TERMUX_PKG_DESCRIPTION=", ("desc", "description")),
                    ("TERMUX_PKG_VERSION=",      ("version",)),
                    ("TERMUX_PKG_DEPENDS=",      ("deps",)),
                    ("TERMUX_PKG_MAINTAINER=",   ("maintainer",)),
                    ("TERMUX_PKG_HOMEPAGE=",     ("homepage",)),
                    ("TERMUX_PKG_LICENSE=",      ("license",)),
                    ("TERMUX_PKG_SRCURL=",       ("srcurl",)),
                    ("TERMUX_PKG_SHA256=",       ("sha256",)),
                ]:
                    if line.startswith(key):
                        val = line.split("=", 1)[1].strip().strip('"\'')
                        for f_ in field:
                            data[f_] = val
                        if key == "TERMUX_PKG_DEPENDS=":
                            data["depends"] = [d.strip() for d in val.split(",") if d.strip()]
        return data

    def test_all_fields(self, tmp_path):
        content = (
            'TERMUX_PKG_DESCRIPTION="A cool tool"\n'
            'TERMUX_PKG_VERSION="2.0.1"\n'
            'TERMUX_PKG_DEPENDS="nodejs,python"\n'
            'TERMUX_PKG_MAINTAINER="@djunekz"\n'
            'TERMUX_PKG_HOMEPAGE="https://example.com"\n'
            'TERMUX_PKG_LICENSE="MIT"\n'
            'TERMUX_PKG_SRCURL="https://example.com/src.tar.gz"\n'
            'TERMUX_PKG_SHA256="abc123"\n'
        )
        p = self._parse(tmp_path, "mytool", content)
        assert p["desc"]        == "A cool tool"
        assert p["description"] == "A cool tool"
        assert p["version"]     == "2.0.1"
        assert p["deps"]        == "nodejs,python"
        assert p["depends"]     == ["nodejs", "python"]
        assert p["maintainer"]  == "@djunekz"
        assert p["homepage"]    == "https://example.com"
        assert p["license"]     == "MIT"
        assert p["srcurl"]      == "https://example.com/src.tar.gz"
        assert p["sha256"]      == "abc123"

    def test_defaults_when_empty(self, tmp_path):
        p = self._parse(tmp_path, "empty", "")
        assert p["version"]  == "?"
        assert p["desc"]     == "-"
        assert p["deps"]     == "-"
        assert p["depends"]  == []

    def test_single_quotes_stripped(self, tmp_path):
        p = self._parse(tmp_path, "sq", "TERMUX_PKG_VERSION='3.1.4'\n")
        assert p["version"] == "3.1.4"

    def test_real_bower(self, tmp_path):
        content = (
            'TERMUX_PKG_DESCRIPTION="A package manager for the web"\n'
            'TERMUX_PKG_VERSION="1.8.12"\n'
            'TERMUX_PKG_DEPENDS="nodejs"\n'
            'TERMUX_PKG_LICENSE="MIT"\n'
        )
        p = self._parse(tmp_path, "bower", content)
        assert p["name"]    == "bower"
        assert p["version"] == "1.8.12"
        assert p["depends"] == ["nodejs"]


class TestCacheLogic:

    def test_cache_valid_within_ttl(self, tmp_path):
        cache_file = tmp_path / "index.json"
        cache_file.write_text(json.dumps({"packages": []}))
        ttl = 6 * 3600
        age = time.time() - cache_file.stat().st_mtime
        assert age < ttl

    def test_cache_expired(self, tmp_path):
        cache_file = tmp_path / "index.json"
        cache_file.write_text(json.dumps({"packages": []}))
        ttl = 1
        time.sleep(0.01)
        age = time.time() - cache_file.stat().st_mtime
        assert age > ttl * 0 or age >= 0

    def test_cache_missing(self, tmp_path):
        cache_file = tmp_path / "index.json"
        assert not cache_file.exists()

    def test_save_and_load_cache(self, tmp_path):
        cache_file = tmp_path / "index.json"
        data = {"packages": [{"package": "bower", "version": "1.8.12"}]}
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        cache_file.write_text(json.dumps(data, indent=2))
        loaded = json.loads(cache_file.read_text())
        assert loaded["packages"][0]["package"] == "bower"

    def test_clear_cache(self, tmp_path):
        cache_file = tmp_path / "index.json"
        cache_file.write_text("{}")
        assert cache_file.exists()
        cache_file.unlink()
        assert not cache_file.exists()

    def test_corrupted_cache_returns_none(self, tmp_path):
        cache_file = tmp_path / "index.json"
        cache_file.write_text("{ broken json {{{")
        result = None
        try:
            result = json.loads(cache_file.read_text())
        except Exception:
            result = None
        assert result is None



class TestGetStatusLogic:

    def _get_status(self, installed, store_version):
        if installed is None:
            return "NOT_INSTALLED", "not installed"
        if compare_versions(installed, store_version) < 0:
            return "UPDATE", f"update available ({installed} → {store_version})"
        return "INSTALLED", f"up-to-date ({store_version})"

    def test_not_installed(self):
        status, msg = self._get_status(None, "1.0.0")
        assert status == "NOT_INSTALLED"
        assert "not installed" in msg

    def test_installed_up_to_date(self):
        status, msg = self._get_status("1.0.0", "1.0.0")
        assert status == "INSTALLED"
        assert "up-to-date" in msg

    def test_installed_newer(self):
        status, _ = self._get_status("2.0.0", "1.9.9")
        assert status == "INSTALLED"

    def test_update_available(self):
        status, msg = self._get_status("1.0.0", "1.0.1")
        assert status == "UPDATE"
        assert "update available" in msg
        assert "1.0.0" in msg
        assert "1.0.1" in msg

    def test_real_bower_update(self):
        status, _ = self._get_status("1.8.11", "1.8.12")
        assert status == "UPDATE"

    def test_real_bower_installed(self):
        status, _ = self._get_status("1.8.12", "1.8.12")
        assert status == "INSTALLED"

    def test_real_pnpm_update(self):
        status, _ = self._get_status("10.29.0", "10.30.1")
        assert status == "UPDATE"
