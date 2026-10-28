import json
from unittest.mock import patch

import pytest
from _loader import load_cli
from conftest import make_valid_root

_cli = load_cli()
_ver_tuple = _cli._ver_tuple
is_installed_newer_or_equal = _cli.is_installed_newer_or_equal
CMD_ALIASES = _cli.CMD_ALIASES


def get_status_pure(installed_version, store_version: str) -> str:
    with patch.object(_cli, "get_installed_version", return_value=installed_version):
        return _cli.get_status("pkg", store_version)[0]


class TestGetStatusLogic:
    def test_not_installed(self):
        assert get_status_pure(None, "1.0.0") == "NOT INSTALLED"

    def test_not_installed_any_version(self):
        for v in ["0.1", "5.2.6", "10.30.1"]:
            assert get_status_pure(None, v) == "NOT INSTALLED"

    def test_installed_same_version(self):
        assert get_status_pure("1.0.0", "1.0.0") == "INSTALLED"

    def test_installed_newer_patch(self):
        assert get_status_pure("1.0.2", "1.0.1") == "INSTALLED"

    def test_installed_newer_minor(self):
        assert get_status_pure("1.10.0", "1.9.0") == "INSTALLED"

    def test_installed_newer_major(self):
        assert get_status_pure("2.0.0", "1.9.9") == "INSTALLED"

    def test_update_patch(self):
        assert get_status_pure("1.0.0", "1.0.1") == "UPDATE"

    def test_update_minor(self):
        assert get_status_pure("1.9.0", "1.10.0") == "UPDATE"

    def test_update_major(self):
        assert get_status_pure("1.9.9", "2.0.0") == "UPDATE"

    def test_installed_with_revision(self):
        assert get_status_pure("4.10-2", "4.10-1") == "INSTALLED"

    def test_update_with_revision(self):
        assert get_status_pure("4.10-1", "4.10-2") == "UPDATE"

    def test_bower_installed(self):
        assert get_status_pure("1.8.12", "1.8.12") == "INSTALLED"

    def test_bower_needs_update(self):
        assert get_status_pure("1.8.11", "1.8.12") == "UPDATE"

    def test_pnpm_installed(self):
        assert get_status_pure("10.30.1", "10.30.1") == "INSTALLED"

    def test_pnpm_needs_update(self):
        assert get_status_pure("10.29.0", "10.30.1") == "UPDATE"

    def test_ani_cli_installed(self):
        assert get_status_pure("4.10", "4.10") == "INSTALLED"

    def test_ani_cli_needs_update(self):
        assert get_status_pure("4.9", "4.10") == "UPDATE"

    def test_tuifimanager_installed(self):
        assert get_status_pure("5.2.6", "5.2.6") == "INSTALLED"

    def test_tuifimanager_needs_update(self):
        assert get_status_pure("5.2.5", "5.2.6") == "UPDATE"

    def test_uv_installed(self):
        assert get_status_pure("0.10.4", "0.10.4") == "INSTALLED"

    def test_uv_needs_update(self):
        assert get_status_pure("0.10.3", "0.10.4") == "UPDATE"


class TestVerTuple:
    def test_non_numeric_base_segment(self):
        result = _ver_tuple("1.alpha.3")
        assert result == (1, 0, 3, 0)

    def test_non_numeric_revision(self):
        result = _ver_tuple("1.2.3-beta")
        assert result == (1, 2, 3, 0)

    def test_non_numeric_both(self):
        result = _ver_tuple("1.abc.3-rc1")
        assert result == (1, 0, 3, 0)


class TestCmdAliases:
    def test_list_primary(self):
        assert CMD_ALIASES["list"] == "list"

    def test_list_short_lower(self):
        assert CMD_ALIASES["-l"] == "list"

    def test_list_short_upper(self):
        assert CMD_ALIASES["-L"] == "list"

    def test_install_primary(self):
        assert CMD_ALIASES["install"] == "install"

    def test_install_short_letter(self):
        assert CMD_ALIASES["i"] == "install"

    def test_install_short_flag(self):
        assert CMD_ALIASES["-i"] == "install"

    def test_uninstall(self):
        assert CMD_ALIASES["uninstall"] == "uninstall"

    def test_show(self):
        assert CMD_ALIASES["show"] == "show"

    def test_update(self):
        assert CMD_ALIASES["update"] == "update"

    def test_upgrade(self):
        assert CMD_ALIASES["upgrade"] == "upgrade"

    def test_version_primary(self):
        assert CMD_ALIASES["version"] == "version"

    def test_version_short(self):
        assert CMD_ALIASES["-v"] == "version"

    def test_help_primary(self):
        assert CMD_ALIASES["help"] == "help"

    def test_help_short(self):
        assert CMD_ALIASES["-h"] == "help"

    def test_help_long(self):
        assert CMD_ALIASES["--help"] == "help"

    def test_unknown_returns_none(self):
        assert CMD_ALIASES.get("unknown") is None
        assert CMD_ALIASES.get("") is None
        assert CMD_ALIASES.get("INSTALL") is None
        assert CMD_ALIASES.get("LIST") is None
        assert CMD_ALIASES.get("--version") is None

    def test_all_targets_are_valid(self):
        valid = {
            "list",
            "search",
            "install",
            "uninstall",
            "fix-install",
            "show",
            "update",
            "upgrade",
            "version",
            "mirrors",
            "cache",
            "help",
        }
        for alias, target in CMD_ALIASES.items():
            assert target in valid, f"'{alias}' → unknown target '{target}'"

    def test_total_alias_count(self):
        assert len(CMD_ALIASES) == 28

    @pytest.mark.parametrize(
        "alias,target",
        [
            ("search", "search"),
            ("find", "search"),
            ("-f", "search"),
            ("-s", "search"),
            ("un", "uninstall"),
            ("remove", "uninstall"),
            ("fix-install", "fix-install"),
            ("--fix-install", "fix-install"),
            ("-fi", "fix-install"),
            ("mirrors", "mirrors"),
            ("-m", "mirrors"),
            ("cache", "cache"),
            ("-c", "cache"),
        ],
    )
    def test_aliases_missing_from_the_old_copy(self, alias, target):
        assert CMD_ALIASES[alias] == target


class TestCacheHandling:
    def test_write_and_read_cache(self, tmp_path, monkeypatch):
        monkeypatch.setenv("HOME", str(tmp_path / "home"))
        monkeypatch.setattr(_cli, "CACHE_FILE", tmp_path / "path.json")
        root = make_valid_root(tmp_path / "termux-app-store")
        _cli.save_cached_root(root)
        assert json.loads((tmp_path / "path.json").read_text())["app_root"] == str(root)
        assert _cli.load_cached_root() == root.resolve()

    def test_cache_creates_parent_dirs(self, tmp_path, monkeypatch):
        monkeypatch.setenv("HOME", str(tmp_path / "home"))
        monkeypatch.setattr(_cli, "CACHE_FILE", tmp_path / "deep" / "nested" / "path.json")
        _cli.save_cached_root(make_valid_root(tmp_path / "root"))
        assert (tmp_path / "deep" / "nested" / "path.json").exists()

    def test_cache_invalid_json_returns_none(self, tmp_path, monkeypatch):
        monkeypatch.setattr(_cli, "CACHE_FILE", tmp_path / "path.json")
        (tmp_path / "path.json").write_text("{ invalid json {{")
        assert _cli.load_cached_root() is None

    def test_cache_missing_key_returns_none(self, tmp_path, monkeypatch):
        monkeypatch.setattr(_cli, "CACHE_FILE", tmp_path / "path.json")
        (tmp_path / "path.json").write_text(json.dumps({"other_key": "value"}))
        assert _cli.load_cached_root() is None

    def test_cache_missing_key_is_not_treated_as_the_current_directory(self, tmp_path, monkeypatch):
        monkeypatch.setenv("HOME", str(tmp_path / "home"))
        monkeypatch.chdir(make_valid_root(tmp_path / "cwd_is_a_valid_root"))
        monkeypatch.setattr(_cli, "CACHE_FILE", tmp_path / "path.json")
        (tmp_path / "path.json").write_text(json.dumps({"app_root": ""}))
        assert _cli.load_cached_root() is None

    def test_cache_nonexistent_file(self, tmp_path, monkeypatch):
        monkeypatch.setattr(_cli, "CACHE_FILE", tmp_path / "nonexistent.json")
        assert _cli.load_cached_root() is None

    def test_cache_overwrite(self, tmp_path, monkeypatch):
        monkeypatch.setenv("HOME", str(tmp_path / "home"))
        monkeypatch.setattr(_cli, "CACHE_FILE", tmp_path / "path.json")
        first = make_valid_root(tmp_path / "old")
        second = make_valid_root(tmp_path / "new")
        _cli.save_cached_root(first)
        _cli.save_cached_root(second)
        assert _cli.load_cached_root() == second.resolve()
