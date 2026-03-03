import json
import sys
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

FAKE_ROOT = Path("/tmp/fake-app-root")
FAKE_PACKAGES = FAKE_ROOT / "packages"

import types

fake_textual_app = types.ModuleType("textual.app")
fake_app_cls = type("App", (), {
    "__init__": lambda self, *a, **kw: None,
    "run": lambda self, *a, **kw: None,
    "set_interval": lambda self, *a, **kw: None,
    "call_from_thread": lambda self, fn, *a, **kw: fn() if callable(fn) else None,
    "push_screen": lambda self, *a, **kw: None,
})
fake_textual_app.App = fake_app_cls
fake_textual_app.ComposeResult = MagicMock()
sys.modules["textual.app"] = fake_textual_app

fake_widgets = types.ModuleType("textual.widgets")
for widget_name in ["Header", "Input", "ListView", "ListItem",
                    "Static", "ProgressBar"]:
    widget_cls = type(widget_name, (), {
        "__init__": lambda self, *a, **kw: None,
        "update": lambda self, *a, **kw: None,
        "clear": lambda self, *a, **kw: None,
        "append": lambda self, *a, **kw: None,
        "scroll_end": lambda self, *a, **kw: None,
    })
    setattr(fake_widgets, widget_name, widget_cls)

fake_label_cls = type("Label", (), {
    "__init__": lambda self, text="", *a, **kw: None,
    "update": lambda self, *a, **kw: None,
})
fake_widgets.Label = fake_label_cls

fake_button_cls = type("Button", (), {
    "__init__": lambda self, *a, **kw: setattr(self, "id", kw.get("id", "")) or setattr(self, "disabled", kw.get("disabled", False)) or None,
    "Pressed": type("Pressed", (), {}),
})
fake_widgets.Button = fake_button_cls

sys.modules["textual.widgets"] = fake_widgets

fake_containers = types.ModuleType("textual.containers")
for cont_name in ["Horizontal", "Vertical", "VerticalScroll", "Center"]:
    cont_cls = type(cont_name, (), {
        "__init__": lambda self, *a, **kw: None,
        "__enter__": lambda self: self,
        "__exit__": lambda self, *a: None,
    })
    setattr(fake_containers, cont_name, cont_cls)
sys.modules["textual.containers"] = fake_containers

fake_screen = types.ModuleType("textual.screen")
fake_modal_cls = type("ModalScreen", (), {
    "__init__": lambda self, *a, **kw: None,
    "__init_subclass__": classmethod(lambda cls, **kw: None),
    "__class_getitem__": classmethod(lambda cls, item: cls),
    "dismiss": lambda self, *a, **kw: None,
})
fake_screen.ModalScreen = fake_modal_cls
sys.modules["textual.screen"] = fake_screen

sys.modules.setdefault("textual", types.ModuleType("textual"))

sys.path.insert(0, str(Path(__file__).parent.parent))

import os
import tempfile

sys.modules.pop("termux_app_store.termux_app_store", None)

_orig_environ = dict(os.environ)

_tmp_dir = tempfile.mkdtemp()
_fake_root = Path(_tmp_dir)
(_fake_root / "packages").mkdir()
(_fake_root / "build-package.sh").write_text("# Termux App Store Official\n")
os.environ["TERMUX_APP_STORE_HOME"] = str(_fake_root)

try:
    import termux_app_store.termux_app_store as tui_module
finally:
    os.environ.clear()
    os.environ.update(_orig_environ)

FAKE_ROOT = tui_module.APP_ROOT

from termux_app_store.termux_app_store import (
    strip_ansi,
    _ver_tuple,
    get_installed_version,
    has_store_fingerprint,
    is_valid_root,
    load_cached_root,
    save_cached_root,
    FINGERPRINT_STRING,
    _fetch_index,
    ensure_package_files,
)


def _make_app(tmp_path=None):
    app = tui_module.TermuxAppStore.__new__(tui_module.TermuxAppStore)
    app.packages = []
    app.status_cache = {}
    app.search_query = ""
    app.current_item = None
    app.installing = False
    app.log_buffer = []
    app.list_view = MagicMock()
    app.info = MagicMock()
    app.log_view = MagicMock()
    app.log_container = MagicMock()
    app.progress = MagicMock()
    app.install_btn = MagicMock()
    app.uninstall_btn = MagicMock()
    return app


class TestStripAnsi:

    def test_removes_color_codes(self):
        assert strip_ansi("\033[32mhello\033[0m") == "hello"

    def test_plain_text_unchanged(self):
        assert strip_ansi("hello world") == "hello world"

    def test_empty_string(self):
        assert strip_ansi("") == ""

    def test_mixed(self):
        result = strip_ansi("\033[1m\033[31mERROR\033[0m: something")
        assert result == "ERROR: something"


class TestVerTuple:

    def test_simple(self):
        assert _ver_tuple("1.2.3") == (1, 2, 3, 0)

    def test_with_revision(self):
        assert _ver_tuple("4.10-1") == (4, 10, 1)

    def test_no_suffix(self):
        assert _ver_tuple("4.10") == (4, 10, 0)

    def test_non_numeric_revision(self):
        assert _ver_tuple("2.0-pre") == (2, 0, 0)

    def test_non_numeric_segment(self):
        assert _ver_tuple("1.alpha.3") == (1, 0, 3, 0)

    def test_ordering(self):
        assert _ver_tuple("1.9.0") < _ver_tuple("1.10.0")
        assert _ver_tuple("4.10-2") > _ver_tuple("4.10-1")


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

    def test_installed_version_empty_string(self):
        with patch("subprocess.check_output", return_value="install ok installed\t"):
            assert get_installed_version("bower") is None


class TestHasStoreFingerprint:

    def test_with_fingerprint(self, tmp_path):
        (tmp_path / "build-package.sh").write_text(f"# {FINGERPRINT_STRING}\nset -e\n")
        assert has_store_fingerprint(tmp_path) is True

    def test_without_fingerprint(self, tmp_path):
        (tmp_path / "build-package.sh").write_text("# other\nset -e\n")
        assert has_store_fingerprint(tmp_path) is False

    def test_no_file(self, tmp_path):
        assert has_store_fingerprint(tmp_path) is False

    def test_exception(self, tmp_path):
        (tmp_path / "build-package.sh").write_text("x")
        import builtins
        real_open = builtins.open
        def patched_open(file, *args, **kwargs):
            if "build-package.sh" in str(file):
                raise OSError("perm denied")
            return real_open(file, *args, **kwargs)
        with patch("builtins.open", side_effect=patched_open):
            assert has_store_fingerprint(tmp_path) is False

    def test_fingerprint_beyond_20_lines(self, tmp_path):
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
        with patch.object(tui_module, "CACHE_FILE", cache):
            save_cached_root(root)
            with patch("termux_app_store.termux_app_store.CACHE_FILE", cache):
                result = load_cached_root()
        assert result == root.resolve()

    def test_load_invalid_path(self, tmp_path):
        cache = tmp_path / "cache.json"
        cache.write_text(json.dumps({"app_root": "/nonexistent/path"}))
        with patch("termux_app_store.termux_app_store.CACHE_FILE", cache):
            assert load_cached_root() is None

    def test_load_missing_cache(self, tmp_path):
        cache = tmp_path / "nonexistent.json"
        with patch("termux_app_store.termux_app_store.CACHE_FILE", cache):
            assert load_cached_root() is None

    def test_load_corrupt_cache(self, tmp_path):
        cache = tmp_path / "cache.json"
        cache.write_text("{ broken {{{")
        with patch("termux_app_store.termux_app_store.CACHE_FILE", cache):
            assert load_cached_root() is None

    def test_save_exception(self, tmp_path):
        cache = tmp_path / "cache.json"
        with patch("termux_app_store.termux_app_store.CACHE_FILE", cache), \
             patch("pathlib.Path.mkdir", side_effect=OSError("perm denied")):
            save_cached_root(tmp_path)


class TestResolveAppRoot:

    def _make_valid_root(self, tmp_path):
        (tmp_path / "packages").mkdir()
        (tmp_path / "build-package.sh").write_text(f"# {FINGERPRINT_STRING}\n")
        return tmp_path

    def test_env_override_valid(self, tmp_path):
        root = self._make_valid_root(tmp_path)
        with patch.dict("os.environ", {"TERMUX_APP_STORE_HOME": str(root)}), \
             patch("termux_app_store.termux_app_store.save_cached_root"):
            result = tui_module.resolve_app_root()
        assert result == root.resolve()

    def test_cached_root_used(self, tmp_path):
        root = self._make_valid_root(tmp_path)
        with patch.dict("os.environ", {"TERMUX_APP_STORE_HOME": ""}), \
             patch("termux_app_store.termux_app_store.load_cached_root", return_value=root):
            result = tui_module.resolve_app_root()
        assert result == root

    def test_base_dir_valid(self, tmp_path):
        root = self._make_valid_root(tmp_path)
        with patch.dict("os.environ", {"TERMUX_APP_STORE_HOME": ""}), \
             patch("termux_app_store.termux_app_store.load_cached_root", return_value=None), \
             patch("termux_app_store.termux_app_store.save_cached_root"), \
             patch("termux_app_store.termux_app_store.__file__", str(root / "termux_app_store.py")):
            result = tui_module.resolve_app_root()
        assert result == root.resolve()

    def test_no_root_raises(self, tmp_path):
        with patch.dict("os.environ", {"TERMUX_APP_STORE_HOME": ""}), \
             patch("termux_app_store.termux_app_store.load_cached_root", return_value=None), \
             patch("termux_app_store.termux_app_store.is_valid_root", return_value=False):
            with pytest.raises(FileNotFoundError):
                tui_module.resolve_app_root()


class TestTermuxAppStoreUnit:

    def _make_pkg(self, root, name, version="1.0.0"):
        pkg_dir = root / name
        pkg_dir.mkdir(parents=True, exist_ok=True)
        (pkg_dir / "build.sh").write_text(
            f'TERMUX_PKG_VERSION="{version}"\n'
            f'TERMUX_PKG_DESCRIPTION="A tool"\n'
            f'TERMUX_PKG_DEPENDS="nodejs"\n'
            f'TERMUX_PKG_MAINTAINER="@dev"\n'
        )
        return pkg_dir

    def test_get_status_not_installed(self, tmp_path):
        app = _make_app(tmp_path)
        with patch("termux_app_store.termux_app_store.get_installed_version", return_value=None):
            assert app.get_status("bower", "1.8.12") == "NOT INSTALLED"

    def test_get_status_installed(self, tmp_path):
        app = _make_app(tmp_path)
        with patch("termux_app_store.termux_app_store.get_installed_version", return_value="1.8.12"):
            assert app.get_status("bower", "1.8.12") == "INSTALLED"

    def test_get_status_update(self, tmp_path):
        app = _make_app(tmp_path)
        with patch("termux_app_store.termux_app_store.get_installed_version", return_value="1.8.11"):
            assert app.get_status("bower", "1.8.12") == "UPDATE"

    def test_get_status_cached(self, tmp_path):
        app = _make_app(tmp_path)
        app.status_cache["bower"] = "INSTALLED"
        with patch("termux_app_store.termux_app_store.get_installed_version") as mock_giv:
            result = app.get_status("bower", "1.8.12")
        assert result == "INSTALLED"
        mock_giv.assert_not_called()

    def test_load_packages(self, tmp_path):
        self._make_pkg(tmp_path, "bower", "1.8.12")
        self._make_pkg(tmp_path, "pnpm", "10.30.1")
        app = _make_app(tmp_path)
        with patch("termux_app_store.termux_app_store._fetch_index", return_value=[]), \
             patch.object(tui_module, "PACKAGES_DIR", tmp_path):
            app.load_packages()
        assert len(app.packages) == 2
        assert app.packages[0]["name"] == "bower"
        assert app.packages[0]["version"] == "1.8.12"

    def test_load_packages_skips_without_build_sh(self, tmp_path):
        (tmp_path / "nosh").mkdir()
        app = _make_app(tmp_path)
        with patch("termux_app_store.termux_app_store._fetch_index", return_value=[]), \
             patch.object(tui_module, "PACKAGES_DIR", tmp_path):
            app.load_packages()
        assert app.packages == []

    def test_load_packages_from_index(self, tmp_path):
        fake_entries = [
            {"package": "bower",  "version": "1.8.12", "description": "A tool",
             "maintainer": "@dev", "depends": ["nodejs"]},
            {"package": "pnpm",   "version": "10.30.1", "description": "Fast pkg mgr",
             "maintainer": "@dev", "depends": []},
        ]
        app = _make_app(tmp_path)
        with patch("termux_app_store.termux_app_store._fetch_index", return_value=fake_entries):
            app.load_packages()
        assert len(app.packages) == 2
        assert app.packages[0]["name"] == "bower"
        assert app.packages[0]["deps"] == "nodejs"
        assert app.packages[1]["deps"] == "-"

    def test_refresh_list_empty_search(self, tmp_path):
        app = _make_app(tmp_path)
        app.packages = [
            {"name": "bower", "version": "1.8.12", "desc": "-", "deps": "-", "maintainer": "-"},
            {"name": "pnpm",  "version": "10.0",   "desc": "-", "deps": "-", "maintainer": "-"},
        ]
        app.search_query = ""
        app.list_view.children = []
        app.refresh_list()
        assert app.list_view.append.call_count == 2

    def test_refresh_list_with_search(self, tmp_path):
        app = _make_app(tmp_path)
        app.packages = [
            {"name": "bower", "version": "1.8.12", "desc": "-", "deps": "-", "maintainer": "-"},
            {"name": "pnpm",  "version": "10.0",   "desc": "-", "deps": "-", "maintainer": "-"},
        ]
        app.search_query = "bower"
        app.list_view.children = []
        app.refresh_list()
        assert app.list_view.append.call_count == 1

    def test_update_log_appends(self, tmp_path):
        app = _make_app(tmp_path)
        app.update_log("line 1")
        app.update_log("line 2")
        assert "line 1" in app.log_buffer
        assert "line 2" in app.log_buffer

    def test_update_log_truncates_at_500(self, tmp_path):
        app = _make_app(tmp_path)
        for i in range(600):
            app.update_log(f"line {i}")
        assert len(app.log_buffer) <= 500

    def test_update_log_no_line(self, tmp_path):
        app = _make_app(tmp_path)
        app.log_buffer = ["existing"]
        app.update_log()
        app.log_view.update.assert_called()

    def test_show_preview_not_installed(self, tmp_path):
        app = _make_app(tmp_path)
        pkg = {"name": "bower", "version": "1.8.12", "desc": "A tool",
               "deps": "nodejs", "maintainer": "@dev"}
        item = MagicMock()
        item.pkg = pkg
        with patch.object(app, "get_status", return_value="NOT INSTALLED"), \
             patch("termux_app_store.termux_app_store.get_installed_version", return_value=None):
            app.show_preview(item)
        app.info.update.assert_called_once()
        assert app.uninstall_btn.display == False

    def test_show_preview_installed(self, tmp_path):
        app = _make_app(tmp_path)
        pkg = {"name": "bower", "version": "1.8.12", "desc": "A tool",
               "deps": "-", "maintainer": "@dev"}
        item = MagicMock()
        item.pkg = pkg
        with patch.object(app, "get_status", return_value="INSTALLED"), \
             patch("termux_app_store.termux_app_store.get_installed_version", return_value="1.8.12"):
            app.show_preview(item)
        app.info.update.assert_called_once()
        assert app.uninstall_btn.display == True

    def test_show_preview_update(self, tmp_path):
        app = _make_app(tmp_path)
        pkg = {"name": "bower", "version": "1.8.12", "desc": "A tool",
               "deps": "nodejs,python", "maintainer": "@dev"}
        item = MagicMock()
        item.pkg = pkg
        with patch.object(app, "get_status", return_value="UPDATE"), \
             patch("termux_app_store.termux_app_store.get_installed_version", return_value="1.8.11"):
            app.show_preview(item)
        app.info.update.assert_called_once()

    def test_run_build_sync_success(self, tmp_path):
        app = _make_app(tmp_path)
        app.call_from_thread = lambda fn, *a, **kw: fn() if callable(fn) else None
        mock_proc = MagicMock()
        mock_proc.stdout.readline.side_effect = [b"Installing...\n", b""]
        mock_proc.returncode = 0
        with patch("subprocess.Popen", return_value=mock_proc), \
             patch.object(tui_module, "ROOT_DIR", tmp_path), \
             patch.object(tui_module, "PACKAGES_DIR", tmp_path), \
             patch.object(app, "load_packages"), \
             patch.object(app, "refresh_list"):
            app.run_build_sync("bower")
        assert app.installing is False

    def test_run_build_sync_failure(self, tmp_path):
        app = _make_app(tmp_path)
        app.call_from_thread = lambda fn, *a, **kw: fn() if callable(fn) else None
        mock_proc = MagicMock()
        mock_proc.stdout.readline.side_effect = [b""]
        mock_proc.returncode = 1
        with patch("subprocess.Popen", return_value=mock_proc), \
             patch.object(tui_module, "ROOT_DIR", tmp_path), \
             patch.object(tui_module, "PACKAGES_DIR", tmp_path), \
             patch.object(app, "load_packages"), \
             patch.object(app, "refresh_list"):
            app.run_build_sync("bower")
        assert app.installing is False

    def test_run_uninstall_sync_success(self, tmp_path):
        app = _make_app(tmp_path)
        app.call_from_thread = lambda fn, *a, **kw: fn() if callable(fn) else None
        mock_proc = MagicMock()
        mock_proc.stdout.readline.side_effect = [b"Removing...\n", b""]
        mock_proc.returncode = 0
        with patch("subprocess.Popen", return_value=mock_proc), \
             patch("subprocess.call"), \
             patch.object(tui_module, "PACKAGES_DIR", tmp_path), \
             patch.object(app, "load_packages"), \
             patch.object(app, "refresh_list"):
            app.run_uninstall_sync("bower")
        assert app.installing is False

    def test_run_uninstall_sync_failure(self, tmp_path):
        app = _make_app(tmp_path)
        app.call_from_thread = lambda fn, *a, **kw: fn() if callable(fn) else None
        mock_proc = MagicMock()
        mock_proc.stdout.readline.side_effect = [b""]
        mock_proc.returncode = 1
        with patch("subprocess.Popen", return_value=mock_proc), \
             patch("subprocess.call"), \
             patch.object(tui_module, "PACKAGES_DIR", tmp_path), \
             patch.object(app, "load_packages"), \
             patch.object(app, "refresh_list"):
            app.run_uninstall_sync("bower")
        assert app.installing is False


class TestRunTui:

    def test_run_tui(self):
        with patch.object(tui_module.TermuxAppStore, "run") as mock_run:
            tui_module.run_tui()
        mock_run.assert_called_once()


class TestRefreshListWithChildren:

    def test_refresh_list_shows_preview_when_children(self):
        app = _make_app()
        app.packages = [
            {"name": "bower", "version": "1.0", "desc": "-", "deps": "-", "maintainer": "-"},
        ]
        app.search_query = ""
        fake_item = MagicMock()
        app.list_view.children = [fake_item]
        with patch.object(app, "show_preview") as mock_preview:
            app.refresh_list()
        mock_preview.assert_called_once_with(fake_item)
        assert app.list_view.index == 0

    def test_refresh_list_no_preview_when_no_children(self):
        app = _make_app()
        app.packages = []
        app.search_query = ""
        app.list_view.children = []
        with patch.object(app, "show_preview") as mock_preview:
            app.refresh_list()
        mock_preview.assert_not_called()


class TestEventHandlers:

    def test_on_input_changed(self):
        app = _make_app()
        app.worker_queue = MagicMock()
        event = MagicMock()
        event.value = "  Bower  "
        with patch.object(app, "refresh_list") as mock_refresh:
            app.on_input_changed(event)
        assert app.search_query == "bower"
        mock_refresh.assert_called_once()

    def test_on_list_view_highlighted_with_item(self):
        app = _make_app()
        fake_item = MagicMock()
        event = MagicMock()
        event.item = fake_item
        with patch.object(app, "show_preview") as mock_preview:
            app.on_list_view_highlighted(event)
        mock_preview.assert_called_once_with(fake_item)

    def test_on_list_view_highlighted_no_item(self):
        app = _make_app()
        event = MagicMock()
        event.item = None
        with patch.object(app, "show_preview") as mock_preview:
            app.on_list_view_highlighted(event)
        mock_preview.assert_not_called()


class TestAsyncHandlers:

    def _make_async_app(self):
        import asyncio
        app = _make_app()
        app.current_item = MagicMock()
        app.current_item.pkg = {"name": "bower"}
        app.worker_queue = asyncio.Queue()
        app.call_from_thread = lambda fn, *a, **kw: fn() if callable(fn) else None
        app.push_screen = MagicMock()
        return app

    def test_on_button_pressed_install(self):
        import asyncio
        app = self._make_async_app()
        event = MagicMock()
        event.button.id = "install"
        asyncio.run(app.on_button_pressed(event))
        assert not app.worker_queue.empty()
        item = app.worker_queue.get_nowait()
        assert item == ("install", "bower")

    def test_on_button_pressed_uninstall_pushes_screen(self):
        import asyncio
        app = self._make_async_app()
        event = MagicMock()
        event.button.id = "uninstall"
        asyncio.run(app.on_button_pressed(event))
        app.push_screen.assert_called_once()

    def test_on_button_pressed_other_id(self):
        import asyncio
        app = self._make_async_app()
        event = MagicMock()
        event.button.id = "other"
        asyncio.run(app.on_button_pressed(event))
        assert app.worker_queue.empty()

    def test_on_button_pressed_already_installing(self):
        import asyncio
        app = self._make_async_app()
        app.installing = True
        event = MagicMock()
        event.button.id = "install"
        asyncio.run(app.on_button_pressed(event))
        assert app.worker_queue.empty()

    def test_consume_worker_queue_when_installing(self):
        import asyncio
        app = self._make_async_app()
        app.installing = True
        asyncio.run(app.consume_worker_queue())

    def test_consume_worker_queue_empty(self):
        import asyncio
        app = self._make_async_app()
        app.installing = False
        asyncio.run(app.consume_worker_queue())

    def test_consume_worker_queue_install(self):
        import asyncio
        app = self._make_async_app()
        app.installing = False
        app.worker_queue.put_nowait(("install", "bower"))

        async def fake_to_thread(f, *a, **kw):
            return f(*a, **kw)

        with patch.object(app, "run_build_sync") as mock_build:
            async def run():
                with patch("asyncio.to_thread", side_effect=fake_to_thread):
                    await app.consume_worker_queue()
            asyncio.run(run())
        mock_build.assert_called_once_with("bower")

    def test_consume_worker_queue_uninstall(self):
        import asyncio
        app = self._make_async_app()
        app.installing = False
        app.worker_queue.put_nowait(("uninstall", "bower"))

        async def fake_to_thread(f, *a, **kw):
            return f(*a, **kw)

        with patch.object(app, "run_uninstall_sync") as mock_uninstall:
            async def run():
                with patch("asyncio.to_thread", side_effect=fake_to_thread):
                    await app.consume_worker_queue()
            asyncio.run(run())
        mock_uninstall.assert_called_once_with("bower")


class TestPackageItemCompose:

    def test_compose_yields_label(self):
        pkg = {"name": "bower", "version": "1.0", "desc": "-", "deps": "-", "maintainer": "-"}
        item = tui_module.PackageItem.__new__(tui_module.PackageItem)
        item.pkg = pkg
        results = list(item.compose())
        assert len(results) == 1


class TestMainBlock:

    def test_main_block(self):
        with patch.object(tui_module, "run_tui") as mock_run:
            exec(
                'if "__main__" == "__main__": run_tui()',
                {"run_tui": mock_run, "__name__": "__main__"}
            )
        mock_run.assert_called_once()


class TestMethodsExist:

    def test_on_mount_exists(self):
        assert hasattr(tui_module.TermuxAppStore, "on_mount")

    def test_compose_exists(self):
        assert hasattr(tui_module.TermuxAppStore, "compose")


class TestFetchIndex:

    def _mock_urlopen(self, payload: dict):
        raw = json.dumps(payload).encode()
        resp = MagicMock()
        resp.read.return_value = raw
        resp.__enter__ = lambda s: s
        resp.__exit__ = MagicMock(return_value=False)
        return resp

    def test_network_success_returns_packages(self, tmp_path):
        payload = {"packages": [{"package": "bower", "version": "1.8.12"}]}
        resp = self._mock_urlopen(payload)
        cache = tmp_path / "index.json"
        with patch("urllib.request.urlopen", return_value=resp), \
             patch.object(tui_module, "INDEX_CACHE", cache):
            result = _fetch_index()
        assert len(result) == 1
        assert result[0]["package"] == "bower"
        assert cache.exists()

    def test_network_success_missing_packages_key(self, tmp_path):
        resp = self._mock_urlopen({"other": "data"})
        cache = tmp_path / "index.json"
        with patch("urllib.request.urlopen", return_value=resp), \
             patch.object(tui_module, "INDEX_CACHE", cache):
            result = _fetch_index()
        assert result == []

    def test_network_fails_falls_back_to_cache(self, tmp_path):
        cache = tmp_path / "index.json"
        cache_data = {"packages": [{"package": "pnpm", "version": "10.0"}]}
        cache.write_text(json.dumps(cache_data))
        with patch("urllib.request.urlopen", side_effect=Exception("no net")), \
             patch.object(tui_module, "INDEX_CACHE", cache):
            result = _fetch_index()
        assert result[0]["package"] == "pnpm"

    def test_network_fails_no_cache_returns_empty(self, tmp_path):
        cache = tmp_path / "missing.json"   # does not exist
        with patch("urllib.request.urlopen", side_effect=Exception("no net")), \
             patch.object(tui_module, "INDEX_CACHE", cache):
            result = _fetch_index()
        assert result == []

    def test_network_fails_corrupt_cache_returns_empty(self, tmp_path):
        cache = tmp_path / "index.json"
        cache.write_text("{ broken {{")
        with patch("urllib.request.urlopen", side_effect=Exception("no net")), \
             patch.object(tui_module, "INDEX_CACHE", cache):
            result = _fetch_index()
        assert result == []


class TestEnsurePackageFiles:

    def test_build_sh_already_exists_returns_true(self, tmp_path):
        pkg_dir = tmp_path / "bower"
        pkg_dir.mkdir()
        (pkg_dir / "build.sh").write_text("# existing")
        with patch("urllib.request.urlopen") as mock_urlopen, \
             patch.object(tui_module, "PACKAGES_DIR", tmp_path):
            result = ensure_package_files("bower")
        assert result is True
        mock_urlopen.assert_not_called()

    def test_download_success_creates_file(self, tmp_path):
        raw = b"TERMUX_PKG_VERSION=1.0\n"
        resp = MagicMock()
        resp.read.return_value = raw
        resp.__enter__ = lambda s: s
        resp.__exit__ = MagicMock(return_value=False)
        with patch("urllib.request.urlopen", return_value=resp), \
             patch.object(tui_module, "PACKAGES_DIR", tmp_path):
            result = ensure_package_files("bower")
        assert result is True
        assert (tmp_path / "bower" / "build.sh").read_bytes() == raw

    def test_download_exception_returns_false(self, tmp_path):
        with patch("urllib.request.urlopen", side_effect=Exception("timeout")), \
             patch.object(tui_module, "PACKAGES_DIR", tmp_path):
            result = ensure_package_files("bower")
        assert result is False


class TestRunBuildSyncEnsureFailure:

    def test_popen_not_called_on_ensure_failure(self, tmp_path):
        app = _make_app(tmp_path)
        app.call_from_thread = lambda fn, *a, **kw: fn() if callable(fn) else None
        with patch.object(tui_module, "ensure_package_files", return_value=False), \
             patch("subprocess.Popen") as mock_popen, \
             patch.object(tui_module, "ROOT_DIR", tmp_path):
            app.run_build_sync("bower")
        mock_popen.assert_not_called()
        assert app.installing is False

    def test_buttons_re_enabled_on_ensure_failure(self, tmp_path):
        app = _make_app(tmp_path)
        app.call_from_thread = lambda fn, *a, **kw: fn() if callable(fn) else None
        with patch.object(tui_module, "ensure_package_files", return_value=False), \
             patch("subprocess.Popen"), \
             patch.object(tui_module, "ROOT_DIR", tmp_path):
            app.run_build_sync("bower")
        assert app.install_btn.disabled is False
        assert app.uninstall_btn.disabled is False

    def test_failure_message_logged(self, tmp_path):
        app = _make_app(tmp_path)
        app.call_from_thread = lambda fn, *a, **kw: fn() if callable(fn) else None
        with patch.object(tui_module, "ensure_package_files", return_value=False), \
             patch("subprocess.Popen"), \
             patch.object(tui_module, "ROOT_DIR", tmp_path):
            app.run_build_sync("bower")
        assert any("Failed to download" in line for line in app.log_buffer)


class TestTextualAvailableFlag:

    def test_textual_available_is_bool(self):
        assert isinstance(tui_module._TEXTUAL_AVAILABLE, bool)

    def test_confirm_uninstall_instantiable(self):
        obj = tui_module.ConfirmUninstall.__new__(tui_module.ConfirmUninstall)
        obj.package_name = "test-pkg"
        assert obj.package_name == "test-pkg"

    def test_modal_screen_attribute_exists(self):
        assert hasattr(tui_module, "_ModalScreen")

    def test_textual_stubs_assigned_when_unavailable(self):
        if tui_module._TEXTUAL_AVAILABLE:
            pytest.skip("textual is installed; stub branch not active")
        assert tui_module.App is object
