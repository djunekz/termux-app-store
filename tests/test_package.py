import json
import sys
import time
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))
from package_manager import (
    get_architecture,
    download_file,
    fetch_json,
    parse_version,
    compare_versions,
    PackageSource,
    PackageManager,
    AppUpdateChecker,
    APP_VERSION,
)


class TestGetArchitecture:

    def test_aarch64(self):
        with patch("platform.machine", return_value="aarch64"):
            assert get_architecture() == "aarch64"

    def test_armv7l(self):
        with patch("platform.machine", return_value="armv7l"):
            assert get_architecture() == "arm"

    def test_armv8l(self):
        with patch("platform.machine", return_value="armv8l"):
            assert get_architecture() == "arm"

    def test_x86_64(self):
        with patch("platform.machine", return_value="x86_64"):
            assert get_architecture() == "x86_64"

    def test_i686(self):
        with patch("platform.machine", return_value="i686"):
            assert get_architecture() == "i686"

    def test_i386(self):
        with patch("platform.machine", return_value="i386"):
            assert get_architecture() == "i686"

    def test_unknown(self):
        with patch("platform.machine", return_value="mips64"):
            assert get_architecture() == "unknown"

    def test_uppercase_normalized(self):
        with patch("platform.machine", return_value="AARCH64"):
            assert get_architecture() == "aarch64"


class TestDownloadFile:

    def test_success(self, tmp_path):
        dest = tmp_path / "file.bin"
        mock_response = MagicMock()
        mock_response.read.return_value = b"binary data"
        mock_response.__enter__ = lambda s: s
        mock_response.__exit__ = MagicMock(return_value=False)

        with patch("urllib.request.urlopen", return_value=mock_response):
            result = download_file("https://example.com/file", dest)

        assert result is True
        assert dest.read_bytes() == b"binary data"

    def test_creates_parent_dirs(self, tmp_path):
        dest = tmp_path / "deep" / "nested" / "file.bin"
        mock_response = MagicMock()
        mock_response.read.return_value = b"data"
        mock_response.__enter__ = lambda s: s
        mock_response.__exit__ = MagicMock(return_value=False)

        with patch("urllib.request.urlopen", return_value=mock_response):
            result = download_file("https://example.com/file", dest)

        assert result is True
        assert dest.exists()

    def test_failure_returns_false(self, tmp_path):
        dest = tmp_path / "file.bin"
        with patch("urllib.request.urlopen", side_effect=Exception("timeout")):
            result = download_file("https://example.com/file", dest)

        assert result is False

    def test_network_error_returns_false(self, tmp_path):
        import urllib.error
        dest = tmp_path / "file.bin"
        with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("no network")):
            result = download_file("https://example.com/file", dest)

        assert result is False


class TestFetchJson:

    def test_success(self):
        payload = {"packages": [{"package": "bower", "version": "1.8.12"}]}
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(payload).encode()
        mock_response.__enter__ = lambda s: s
        mock_response.__exit__ = MagicMock(return_value=False)

        with patch("urllib.request.urlopen", return_value=mock_response):
            result = fetch_json("https://example.com/index.json")

        assert result == payload

    def test_failure_returns_none(self):
        with patch("urllib.request.urlopen", side_effect=Exception("timeout")):
            result = fetch_json("https://example.com/index.json")

        assert result is None

    def test_invalid_json_returns_none(self):
        mock_response = MagicMock()
        mock_response.read.return_value = b"not json {{{"
        mock_response.__enter__ = lambda s: s
        mock_response.__exit__ = MagicMock(return_value=False)

        with patch("urllib.request.urlopen", return_value=mock_response):
            result = fetch_json("https://example.com/index.json")

        assert result is None


class TestParseVersion:

    def test_simple(self):
        assert parse_version("1.2.3") == (1, 2, 3)

    def test_v_prefix(self):
        assert parse_version("v2.0.0") == (2, 0, 0)

    def test_two_parts(self):
        assert parse_version("1.2") == (1, 2, 0)

    def test_pre_release_stripped(self):
        assert parse_version("1.2.3-beta") == (1, 2, 3)

    def test_build_meta_stripped(self):
        assert parse_version("1.2.3+build") == (1, 2, 3)

    def test_empty(self):
        assert parse_version("") == (0, 0, 0)

    def test_non_numeric(self):
        assert parse_version("1.abc.3") == (1, 0, 3)

    def test_max_6_parts(self):
        assert parse_version("1.2.3.4.5.6.7.8") == (1, 2, 3, 4, 5, 6)


class TestCompareVersions:

    def test_equal(self):
        assert compare_versions("1.0.0", "1.0.0") == 0

    def test_older(self):
        assert compare_versions("1.0.0", "1.0.1") == -1

    def test_newer(self):
        assert compare_versions("1.0.1", "1.0.0") == 1

    def test_v_prefix(self):
        assert compare_versions("v1.2.3", "1.2.3") == 0


class TestPackageSource:

    def test_env_override(self):
        with patch.dict("os.environ", {"TERMUX_APP_STORE_MODE": "LOCAL"}):
            assert PackageSource.detect_mode() == "local"

    def test_local_when_build_sh_exists(self, tmp_path):
        pkg = tmp_path / "bower"
        pkg.mkdir()
        (pkg / "build.sh").write_text('TERMUX_PKG_VERSION="1.0"\n')
        assert PackageSource.detect_mode(tmp_path) == "local"

    def test_remote_when_no_build_sh(self, tmp_path):
        pkg = tmp_path / "empty"
        pkg.mkdir()
        assert PackageSource.detect_mode(tmp_path) == "remote"

    def test_remote_when_no_dir(self):
        assert PackageSource.detect_mode(None) == "remote"

    def test_remote_when_dir_not_exist(self, tmp_path):
        assert PackageSource.detect_mode(tmp_path / "nonexistent") == "remote"


class TestPackageManagerCache:

    def test_cache_invalid_when_missing(self, tmp_path):
        pm = PackageManager()
        pm.cache_file = tmp_path / "index.json"
        assert pm._is_cache_valid() is False

    def test_cache_valid_fresh(self, tmp_path):
        cache = tmp_path / "index.json"
        cache.write_text(json.dumps({"packages": []}))
        pm = PackageManager()
        pm.cache_file = cache
        pm.cache_ttl = 3600
        assert pm._is_cache_valid() is True

    def test_cache_invalid_expired(self, tmp_path):
        cache = tmp_path / "index.json"
        cache.write_text(json.dumps({"packages": []}))
        pm = PackageManager()
        pm.cache_file = cache
        pm.cache_ttl = 0
        assert pm._is_cache_valid() is False

    def test_save_and_load_cache(self, tmp_path):
        pm = PackageManager()
        pm.cache_file = tmp_path / "cache" / "index.json"
        data = {"packages": [{"package": "bower"}]}
        pm._save_cache(data)
        loaded = pm._load_cache()
        assert loaded == data

    def test_load_cache_missing(self, tmp_path):
        pm = PackageManager()
        pm.cache_file = tmp_path / "nonexistent.json"
        assert pm._load_cache() is None

    def test_load_cache_corrupt(self, tmp_path):
        cache = tmp_path / "index.json"
        cache.write_text("{ broken {{")
        pm = PackageManager()
        pm.cache_file = cache
        assert pm._load_cache() is None

    def test_clear_cache(self, tmp_path):
        cache = tmp_path / "index.json"
        cache.write_text("{}")
        pm = PackageManager()
        pm.cache_file = cache
        pm.clear_cache()
        assert not cache.exists()

    def test_clear_cache_noop_when_missing(self, tmp_path):
        pm = PackageManager()
        pm.cache_file = tmp_path / "nonexistent.json"
        pm.clear_cache()


class TestPackageManagerLocal:

    def _make_pkg(self, root, name, content):
        pkg = root / name
        pkg.mkdir()
        (pkg / "build.sh").write_text(content)
        return pkg

    def test_load_local_basic(self, tmp_path):
        self._make_pkg(tmp_path, "bower", 'TERMUX_PKG_VERSION="1.8.12"\n')
        pm = PackageManager(tmp_path)
        pm.mode = "local"
        pkgs = pm.load_packages()
        assert len(pkgs) == 1
        assert pkgs[0]["name"] == "bower"
        assert pkgs[0]["version"] == "1.8.12"

    def test_load_local_skips_files(self, tmp_path):
        (tmp_path / "not_a_dir.txt").write_text("x")
        self._make_pkg(tmp_path, "bower", 'TERMUX_PKG_VERSION="1.0"\n')
        pm = PackageManager(tmp_path)
        pm.mode = "local"
        pkgs = pm.load_packages()
        assert len(pkgs) == 1

    def test_load_local_skips_dir_without_build_sh(self, tmp_path):
        (tmp_path / "emptypkg").mkdir()
        pm = PackageManager(tmp_path)
        pm.mode = "local"
        pkgs = pm.load_packages()
        assert pkgs == []

    def test_load_local_empty_dir(self, tmp_path):
        pm = PackageManager(tmp_path)
        pm.mode = "local"
        assert pm.load_packages() == []

    def test_load_local_none_dir(self):
        pm = PackageManager(None)
        pm.mode = "local"
        assert pm.load_packages() == []

    def test_parse_build_sh_all_fields(self, tmp_path):
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
        pkg_dir = tmp_path / "mytool"
        pkg_dir.mkdir()
        (pkg_dir / "build.sh").write_text(content)
        pm = PackageManager(tmp_path)
        data = pm._parse_build_sh(pkg_dir)
        assert data["desc"] == "A cool tool"
        assert data["version"] == "2.0.1"
        assert data["depends"] == ["nodejs", "python"]
        assert data["maintainer"] == "@djunekz"
        assert data["homepage"] == "https://example.com"
        assert data["license"] == "MIT"
        assert data["srcurl"] == "https://example.com/src.tar.gz"
        assert data["sha256"] == "abc123"

    def test_parse_build_sh_defaults(self, tmp_path):
        pkg_dir = tmp_path / "empty"
        pkg_dir.mkdir()
        (pkg_dir / "build.sh").write_text("")
        pm = PackageManager(tmp_path)
        data = pm._parse_build_sh(pkg_dir)
        assert data["version"] == "?"
        assert data["desc"] == "-"
        assert data["depends"] == []

    def test_multiple_packages_sorted(self, tmp_path):
        self._make_pkg(tmp_path, "zzz", 'TERMUX_PKG_VERSION="1.0"\n')
        self._make_pkg(tmp_path, "aaa", 'TERMUX_PKG_VERSION="2.0"\n')
        pm = PackageManager(tmp_path)
        pm.mode = "local"
        pkgs = pm.load_packages()
        assert pkgs[0]["name"] == "aaa"
        assert pkgs[1]["name"] == "zzz"


class TestPackageManagerRemote:

    def test_load_remote_from_network(self, tmp_path):
        payload = {"packages": [{"package": "bower", "version": "1.8.12"}]}
        pm = PackageManager()
        pm.cache_file = tmp_path / "index.json"
        pm.cache_ttl = 0

        with patch("package_manager.fetch_json", return_value=payload):
            pkgs = pm._load_remote()

        assert len(pkgs) == 1
        assert pkgs[0]["name"] == "bower"

    def test_load_remote_from_cache(self, tmp_path):
        payload = {"packages": [{"package": "pnpm", "version": "10.30.1"}]}
        cache = tmp_path / "index.json"
        cache.write_text(json.dumps(payload))

        pm = PackageManager()
        pm.cache_file = cache
        pm.cache_ttl = 9999

        pkgs = pm._load_remote()
        assert pkgs[0]["package"] == "pnpm"
        assert pkgs[0]["version"] == "10.30.1"

    def test_load_remote_fallback_to_cache_on_failure(self, tmp_path):
        payload = {"packages": [{"package": "git", "version": "2.0"}]}
        cache = tmp_path / "index.json"
        cache.write_text(json.dumps(payload))

        pm = PackageManager()
        pm.cache_file = cache
        pm.cache_ttl = 0

        with patch("package_manager.fetch_json", return_value=None):
            pkgs = pm._load_remote()

        assert pkgs[0]["name"] == "git"

    def test_load_remote_empty_when_all_fail(self, tmp_path):
        pm = PackageManager()
        pm.cache_file = tmp_path / "nonexistent.json"
        pm.cache_ttl = 0

        with patch("package_manager.fetch_json", return_value=None):
            pkgs = pm._load_remote()

        assert pkgs == []

    def test_normalize_remote_pkg_name_from_package(self):
        pkg = PackageManager._normalize_remote_pkg({"package": "bower"})
        assert pkg["name"] == "bower"

    def test_normalize_remote_pkg_desc_fallback(self):
        pkg = PackageManager._normalize_remote_pkg({})
        assert pkg["desc"] == "-"

    def test_normalize_remote_pkg_depends_string(self):
        pkg = PackageManager._normalize_remote_pkg({"depends": "nodejs, python"})
        assert pkg["depends"] == ["nodejs", "python"]

    def test_load_packages_remote_mode(self, tmp_path):
        payload = {"packages": [{"package": "bower", "version": "1.8.12"}]}
        pm = PackageManager()
        pm.mode = "remote"
        pm.cache_file = tmp_path / "index.json"
        pm.cache_ttl = 0

        with patch("package_manager.fetch_json", return_value=payload):
            pkgs = pm.load_packages()

        assert len(pkgs) == 1


class TestGetPackage:

    def test_found_by_package_key(self, tmp_path):
        (tmp_path / "bower").mkdir()
        (tmp_path / "bower" / "build.sh").write_text('TERMUX_PKG_VERSION="1.8.12"\n')
        pm = PackageManager(tmp_path)
        pm.mode = "local"
        pkg = pm.get_package("bower")
        assert pkg is not None
        assert pkg["version"] == "1.8.12"

    def test_not_found(self, tmp_path):
        pm = PackageManager(tmp_path)
        pm.mode = "local"
        assert pm.get_package("nonexistent") is None


class TestGetInstalledVersion:

    def test_pkg_info_success(self):
        pm = PackageManager()
        with patch("subprocess.check_output", return_value="Name: bower\nVersion: 1.8.12\n"):
            assert pm.get_installed_version("bower") == "1.8.12"

    def test_pkg_info_fails_dpkg_success(self):
        pm = PackageManager()
        def side_effect(cmd, **kwargs):
            if cmd[0] == "pkg":
                raise Exception("not found")
            return "1.8.12"
        with patch("subprocess.check_output", side_effect=side_effect):
            assert pm.get_installed_version("bower") == "1.8.12"

    def test_both_fail_returns_none(self):
        pm = PackageManager()
        with patch("subprocess.check_output", side_effect=Exception("not found")):
            assert pm.get_installed_version("bower") is None

    def test_dpkg_empty_returns_none(self):
        pm = PackageManager()
        def side_effect(cmd, **kwargs):
            if cmd[0] == "pkg":
                raise Exception("not found")
            return ""
        with patch("subprocess.check_output", side_effect=side_effect):
            assert pm.get_installed_version("bower") is None


class TestGetStatus:

    def test_not_installed(self):
        pm = PackageManager()
        with patch.object(pm, "get_installed_version", return_value=None):
            status, msg = pm.get_status("bower", "1.8.12")
        assert status == "NOT_INSTALLED"

    def test_installed_up_to_date(self):
        pm = PackageManager()
        with patch.object(pm, "get_installed_version", return_value="1.8.12"):
            status, msg = pm.get_status("bower", "1.8.12")
        assert status == "INSTALLED"

    def test_update_available(self):
        pm = PackageManager()
        with patch.object(pm, "get_installed_version", return_value="1.8.11"):
            status, msg = pm.get_status("bower", "1.8.12")
        assert status == "UPDATE"
        assert "1.8.11" in msg
        assert "1.8.12" in msg


class TestAppUpdateChecker:

    def test_get_latest_version_success(self):
        with patch("package_manager.fetch_json", return_value={"tag_name": "v0.2.0"}):
            assert AppUpdateChecker.get_latest_version() == "0.2.0"

    def test_get_latest_version_failure(self):
        with patch("package_manager.fetch_json", return_value=None):
            assert AppUpdateChecker.get_latest_version() is None

    def test_get_latest_version_no_tag(self):
        with patch("package_manager.fetch_json", return_value={"other": "data"}):
            assert AppUpdateChecker.get_latest_version() is None

    def test_check_update_available(self):
        with patch.object(AppUpdateChecker, "get_latest_version", return_value="9.9.9"):
            has_update, latest = AppUpdateChecker.check_update()
        assert has_update is True
        assert latest == "9.9.9"

    def test_check_update_up_to_date(self):
        with patch.object(AppUpdateChecker, "get_latest_version", return_value=APP_VERSION):
            has_update, latest = AppUpdateChecker.check_update()
        assert has_update is False

    def test_check_update_no_latest(self):
        with patch.object(AppUpdateChecker, "get_latest_version", return_value=None):
            has_update, latest = AppUpdateChecker.check_update()
        assert has_update is False
        assert latest is None

    def test_get_download_url(self):
        with patch("package_manager.get_architecture", return_value="aarch64"):
            url = AppUpdateChecker.get_download_url("0.2.0")
        assert "0.2.0" in url
        assert "aarch64" in url


    def test_upgrade_app_success(self, tmp_path):
        with patch("package_manager.download_file", side_effect=lambda url, dest, **kw: [dest.parent.mkdir(parents=True, exist_ok=True), dest.write_bytes(b"binary"), True][-1]), \
             patch("package_manager.get_architecture", return_value="aarch64"), \
             patch("shutil.move"), \
             patch("package_manager.PREFIX", str(tmp_path)):
            (tmp_path / "bin").mkdir(parents=True, exist_ok=True)
            with patch("package_manager.Path", side_effect=lambda p: tmp_path / "termux-app-store-new" if str(p) == "/tmp/termux-app-store-new" else Path(p)):
                result = AppUpdateChecker.upgrade_app("0.2.0")
        assert result is True

    def test_upgrade_app_download_fails(self, tmp_path):
        with patch("package_manager.download_file", return_value=False):
            result = AppUpdateChecker.upgrade_app("0.2.0")
        assert result is False

    def test_upgrade_app_install_fails(self, tmp_path):
        with patch("package_manager.download_file", side_effect=lambda url, dest, **kw: [dest.parent.mkdir(parents=True, exist_ok=True), dest.write_bytes(b"binary"), True][-1]), \
             patch("package_manager.get_architecture", return_value="aarch64"), \
             patch("shutil.move", side_effect=Exception("permission denied")):
            with patch("package_manager.Path", side_effect=lambda p: tmp_path / "termux-app-store-new" if str(p) == "/tmp/termux-app-store-new" else Path(p)):
                result = AppUpdateChecker.upgrade_app("0.2.0")
        assert result is False
