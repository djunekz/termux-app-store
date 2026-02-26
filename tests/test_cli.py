"""
Tests untuk CLI status logic, command aliases, dan cache handling.
"""

import re
import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


# ── Fungsi yang ditest ────────────────────────────────────────────────────────

def _ver_tuple(v: str):
    v = v.strip()
    parts = v.split("-", 1)
    base = parts[0]
    rev_str = parts[1] if len(parts) > 1 else "0"
    base_parts = []
    for seg in re.split(r"[._]", base):
        try:
            base_parts.append(int(seg))
        except ValueError:
            base_parts.append(0)
    try:
        rev = int(rev_str)
    except ValueError:
        rev = 0
    return tuple(base_parts) + (rev,)


def is_installed_newer_or_equal(installed: str, store: str) -> bool:
    return _ver_tuple(installed) >= _ver_tuple(store)


def get_status_pure(installed_version, store_version: str) -> str:
    """Pure logic dari get_status() tanpa ANSI color codes."""
    if installed_version is None:
        return "NOT INSTALLED"
    if is_installed_newer_or_equal(installed_version, store_version):
        return "INSTALLED"
    return "UPDATE"


CMD_ALIASES = {
    "list":      "list",
    "-l":        "list",
    "-L":        "list",
    "install":   "install",
    "i":         "install",
    "-i":        "install",
    "uninstall": "uninstall",
    "show":      "show",
    "update":    "update",
    "upgrade":   "upgrade",
    "version":   "version",
    "-v":        "version",
    "help":      "help",
    "-h":        "help",
    "--help":    "help",
}


# ── Tests: get_status logic ───────────────────────────────────────────────────

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

    # Real package scenarios
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


# ── Tests: CMD_ALIASES ────────────────────────────────────────────────────────

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
        assert CMD_ALIASES.get("unknown")   is None
        assert CMD_ALIASES.get("")          is None
        assert CMD_ALIASES.get("INSTALL")   is None
        assert CMD_ALIASES.get("LIST")      is None
        assert CMD_ALIASES.get("--version") is None

    def test_all_targets_are_valid(self):
        valid = {"list", "install", "uninstall", "show", "update", "upgrade", "version", "help"}
        for alias, target in CMD_ALIASES.items():
            assert target in valid, f"'{alias}' → unknown target '{target}'"

    def test_total_alias_count(self):
        assert len(CMD_ALIASES) == 15


# ── Tests: cache JSON handling ────────────────────────────────────────────────

class TestCacheHandling:

    def test_write_and_read_cache(self, tmp_path):
        cache_file = tmp_path / "path.json"
        app_root = tmp_path / "termux-app-store"

        cache_file.write_text(json.dumps({"app_root": str(app_root)}, indent=2))

        data = json.loads(cache_file.read_text())
        assert data["app_root"] == str(app_root)

    def test_cache_creates_parent_dirs(self, tmp_path):
        cache_file = tmp_path / "deep" / "nested" / "path.json"
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        cache_file.write_text(json.dumps({"app_root": "/some/path"}))
        assert cache_file.exists()

    def test_cache_invalid_json_returns_none(self, tmp_path):
        cache_file = tmp_path / "path.json"
        cache_file.write_text("{ invalid json {{")
        result = None
        try:
            data = json.loads(cache_file.read_text())
            result = data.get("app_root")
        except Exception:
            result = None
        assert result is None

    def test_cache_missing_key_returns_empty(self, tmp_path):
        cache_file = tmp_path / "path.json"
        cache_file.write_text(json.dumps({"other_key": "value"}))
        data = json.loads(cache_file.read_text())
        assert data.get("app_root", "") == ""

    def test_cache_nonexistent_file(self, tmp_path):
        cache_file = tmp_path / "nonexistent.json"
        assert not cache_file.exists()
        result = None
        try:
            data = json.loads(cache_file.read_text())
            result = data.get("app_root")
        except Exception:
            result = None
        assert result is None

    def test_cache_overwrite(self, tmp_path):
        cache_file = tmp_path / "path.json"
        cache_file.write_text(json.dumps({"app_root": "/old/path"}))
        cache_file.write_text(json.dumps({"app_root": "/new/path"}))
        data = json.loads(cache_file.read_text())
        assert data["app_root"] == "/new/path"
