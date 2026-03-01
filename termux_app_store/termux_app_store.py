#!/usr/bin/env python3
import asyncio
import subprocess
import time
import sys
import os
import json
import re
from pathlib import Path

try:
    from textual.app import App, ComposeResult
    from textual.widgets import (
        Header,
        Input,
        ListView,
        ListItem,
        Label,
        Static,
        Button,
        ProgressBar,
    )
    from textual.containers import Horizontal, Vertical, VerticalScroll, Center
    _TEXTUAL_AVAILABLE = True
except ImportError:
    App = object  # type: ignore
    ComposeResult = None  # type: ignore
    _TEXTUAL_AVAILABLE = False

CACHE_FILE = (
    Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
    / "termux-app-store"
    / "path.json"
)

FINGERPRINT_STRING = "Termux App Store Official"

ANSI_ESCAPE = re.compile(r'\x1b\[[0-9;]*[mGKHf]')

def strip_ansi(text: str) -> str:
    return ANSI_ESCAPE.sub('', text)

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

def get_installed_version(name: str):
    try:
        out = subprocess.check_output(
            ["dpkg-query", "-W", "-f=${Status}\t${Version}\n", name],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        if not out:
            return None
        status_part, _, version_part = out.partition("\t")
        if "installed" in status_part:
            return version_part.strip() or None
    except Exception:
        pass
    return None

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
    except Exception: # pragma: no cover
        pass # pragma: no cover
    return False

def is_valid_root(path: Path) -> bool:
    return (
        path.is_dir()
        and (path / "packages").is_dir()
        and (path / "build-package.sh").is_file()
        and has_store_fingerprint(path)
    )

def load_cached_root():
    try:
        if CACHE_FILE.exists():
            data = json.loads(CACHE_FILE.read_text())
            p = Path(data.get("app_root", "")).expanduser()
            if is_valid_root(p):
                return p.resolve()
    except Exception:
        pass
    return None

def save_cached_root(path: Path):
    try:
        CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        CACHE_FILE.write_text(
            json.dumps({"app_root": str(path)}, indent=2)
        )
    except Exception:
        pass

def resolve_app_root() -> Path:
    env = os.environ.get("TERMUX_APP_STORE_HOME")
    if env:
        p = Path(env).expanduser().resolve()
        if is_valid_root(p):
            save_cached_root(p)
            return p

    cached = load_cached_root()
    if cached:
        return cached

    base = (
        Path(sys.executable).resolve().parent
        if getattr(sys, "frozen", False)
        else Path(__file__).resolve().parent
    )

    if is_valid_root(base):
        save_cached_root(base)
        return base

    raise FileNotFoundError(
        "export TERMUX_APP_STORE_HOME=/path/to/termux-app-store"
    )

APP_ROOT = resolve_app_root()
PACKAGES_DIR = APP_ROOT / "packages"
ROOT_DIR = APP_ROOT

class PackageItem(ListItem):
    def __init__(self, pkg: dict):
        super().__init__()
        self.pkg = pkg

    def compose(self) -> ComposeResult:
        yield Label(self.pkg["name"])


try:
    from textual.screen import ModalScreen as _ModalScreen
except ImportError:
    _ModalScreen = object  # type: ignore

class ConfirmUninstall(_ModalScreen):

    DEFAULT_CSS = """
    ConfirmUninstall {
        align: center middle;
    }
    #dialog {
        width: 60;
        height: auto;
        border: heavy #ff5555;
        background: #282a36;
        padding: 2 4;
    }
    #dialog-title {
        text-align: center;
        color: #ff5555;
        text-style: bold;
        margin-bottom: 1;
    }
    #dialog-msg {
        text-align: center;
        color: #f8f8f2;
        margin-bottom: 2;
    }
    #dialog-btns {
        align: center middle;
        height: auto;
    }
    #btn-cancel {
        margin-right: 2;
        background: #44475a;
        color: #f8f8f2;
    }
    #btn-cancel:hover { background: #6272a4; }
    #btn-confirm-uninstall {
        background: #ff5555;
        color: #f8f8f2;
    }
    #btn-confirm-uninstall:hover { background: #ff6e6e; }
    """

    def __init__(self, package_name: str):
        super().__init__()
        self.package_name = package_name

    def compose(self) -> ComposeResult: # pragma: no cover
        with Vertical(id="dialog"):
            yield Static("⚠  Confirm Uninstall", id="dialog-title")
            yield Static(
                f"Are you sure you want to uninstall\n[b]{self.package_name}[/b]?",
                id="dialog-msg",
            )
            with Horizontal(id="dialog-btns"):
                yield Button("Cancel", id="btn-cancel")
                yield Button("Uninstall", id="btn-confirm-uninstall")

    def on_button_pressed(self, event: Button.Pressed) -> None: # pragma: no cover
        if event.button.id == "btn-cancel":
            self.dismiss(False)
        elif event.button.id == "btn-confirm-uninstall":
            self.dismiss(True)


class TermuxAppStore(App):

    CSS = """
    Screen { background: #282a36; color: #f8f8f2; }
    #body { layout: horizontal; height: 1fr; }
    #left { width: 35%; border: heavy #6272a4; padding: 1; }
    #right { width: 65%; border: heavy #6272a4; padding: 1; }
    ListItem.-highlight { background: #44475a; color: #50fa7b; }
    ProgressBar { height: 1; }
    #footer { height: 1; content-align: center middle; color: #6272a4; }
    #log-scroll { height: 1fr; border: solid #6272a4; }
    #btn-row { height: auto; margin-top: 1; }
    #install { margin-right: 1; }
    #uninstall { background: #ff5555; color: #f8f8f2; display: none; }
    #uninstall:hover { background: #ff6e6e; }
    #uninstall:disabled { background: #44475a; color: #6272a4; }
    """

    def on_mount(self): # pragma: no cover
        self.packages = []
        self.status_cache = {}
        self.search_query = ""
        self.current_item = None
        self.installing = False
        self.log_buffer = []
        self.worker_queue = asyncio.Queue()

        self.set_interval(0.1, self.consume_worker_queue)

        self.load_packages()
        self.refresh_list()

    def compose(self) -> ComposeResult: # pragma: no cover
        yield Header(show_clock=True)
        yield Input(placeholder="Search package...", id="search")

        with Horizontal(id="body"):
            with Vertical(id="left"):
                self.list_view = ListView()
                yield self.list_view

            with Vertical(id="right"):
                self.info = Static("Select a package")
                yield self.info

                with VerticalScroll(id="log-scroll") as self.log_container:
                    self.log_view = Static("", markup=False)
                    yield self.log_view

                self.progress = ProgressBar(total=100)
                yield self.progress

                with Horizontal(id="btn-row"):
                    self.install_btn = Button("Install / Update", id="install")
                    yield self.install_btn

                    self.uninstall_btn = Button("Uninstall", id="uninstall")
                    self.uninstall_btn.display = False
                    yield self.uninstall_btn

        yield Static("Official Developer @djunekz | Termux App Store", id="footer")

    def load_packages(self):
        self.packages.clear()

        for pkg_dir in sorted(PACKAGES_DIR.iterdir()):
            build = pkg_dir / "build.sh"
            if not build.exists():
                continue

            data = {
                "name": pkg_dir.name,
                "desc": "-",
                "version": "?",
                "deps": "-",
                "maintainer": "-",
            }

            with build.open(errors="ignore") as f:
                for line in f:
                    if line.startswith("TERMUX_PKG_DESCRIPTION="):
                        data["desc"] = line.split("=", 1)[1].strip().strip('"')
                    elif line.startswith("TERMUX_PKG_VERSION="):
                        data["version"] = line.split("=", 1)[1].strip().strip('"')
                    elif line.startswith("TERMUX_PKG_DEPENDS="):
                        data["deps"] = line.split("=", 1)[1].strip().strip('"')
                    elif line.startswith("TERMUX_PKG_MAINTAINER="):
                        data["maintainer"] = line.split("=", 1)[1].strip().strip('"')

            self.packages.append(data)

    def refresh_list(self):
        self.list_view.clear()
        q = self.search_query

        for pkg in self.packages:
            if q == "" or q in pkg["name"]:
                self.list_view.append(PackageItem(pkg))

        if self.list_view.children:
            self.list_view.index = 0
            self.show_preview(self.list_view.children[0])

    def on_input_changed(self, message: Input.Changed):
        self.search_query = message.value.lower().strip()
        self.refresh_list()

    def on_list_view_highlighted(self, event: ListView.Highlighted):
        if event.item:
            self.show_preview(event.item)

    def get_status(self, name: str, store_version: str) -> str:
        if name in self.status_cache:
            return self.status_cache[name]

        installed = get_installed_version(name)

        if installed is None:
            status = "NOT INSTALLED"
        elif _ver_tuple(installed) >= _ver_tuple(store_version):
            status = "INSTALLED"
        else:
            status = "UPDATE"

        self.status_cache[name] = status
        return status

    def show_preview(self, item: PackageItem):
        self.current_item = item
        p = item.pkg

        status = self.get_status(p["name"], p["version"])
        installed_ver = get_installed_version(p["name"])

        if status == "UPDATE":
            badge = "[yellow]UPDATE[/yellow]"
            ver_line = f"Version    : {p['version']}  [dim](installed: {installed_ver})[/dim]"
        elif status == "INSTALLED":
            badge = "[green]INSTALLED[/green]"
            ver_line = f"Version    : {installed_ver}"
        else:
            badge = "[red]NOT INSTALLED[/red]"
            ver_line = f"Version    : {p['version']}"

        deps = (
            "\n".join(f"• {d.strip()}" for d in p["deps"].split(","))
            if p["deps"] != "-"
            else "-"
        )

        self.info.update(
            f"[b]{p['name']}[/b]  {badge}\n\n"
            f"{ver_line}\n"
            f"Maintainer : {p['maintainer']}\n\n"
            f"[b]Dependencies[/b]\n{deps}\n\n"
            f"{p['desc']}"
        )

        self.log_buffer.clear()
        self.log_view.update("")
        self.progress.progress = 0

        is_installed = status in ("INSTALLED", "UPDATE")
        self.uninstall_btn.display = is_installed

    async def on_button_pressed(self, event: Button.Pressed):
        if self.installing:
            return

        if event.button.id == "install" and self.current_item:
            await self.worker_queue.put(("install", self.current_item.pkg["name"]))

        elif event.button.id == "uninstall" and self.current_item:
            name = self.current_item.pkg["name"]
            def handle_confirm(confirmed: bool) -> None: # pragma: no cover
                if confirmed:
                    asyncio.get_event_loop().call_soon_threadsafe(
                        lambda: self.worker_queue.put_nowait(("uninstall", name))
                    )
            self.push_screen(ConfirmUninstall(name), handle_confirm)

    async def consume_worker_queue(self):
        if self.installing or self.worker_queue.empty():
            return
        action, name = await self.worker_queue.get()
        if action == "install":
            await asyncio.to_thread(self.run_build_sync, name)
        elif action == "uninstall":
            await asyncio.to_thread(self.run_uninstall_sync, name)

    def run_build_sync(self, name: str):
        self.installing = True
        self.call_from_thread(lambda: setattr(self.install_btn, "disabled", True))
        self.call_from_thread(lambda: setattr(self.uninstall_btn, "disabled", True))
        self.log_buffer.clear()
        self.call_from_thread(lambda: setattr(self.progress, "progress", 0))
        self.call_from_thread(lambda: self.update_log(f"Installing {name}...\n"))

        proc = subprocess.Popen(
            ["bash", "build-package.sh", name],
            cwd=str(ROOT_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        for line in iter(proc.stdout.readline, b""):
            clean_line = strip_ansi(line.decode(errors="ignore").rstrip())
            if clean_line:
                self.call_from_thread(
                    lambda t=clean_line: self.update_log(t)
                )

        proc.wait()

        if proc.returncode == 0:
            self.call_from_thread(lambda: setattr(self.progress, "progress", 100))
            self.call_from_thread(lambda: self.update_log("\n✔ Installation completed successfully!"))
        else:
            self.call_from_thread(lambda: self.update_log(f"\n✗ Installation failed (exit code {proc.returncode})"))

        self.installing = False
        self.status_cache.clear()
        self.load_packages()

        def _finalize_install():
            self.install_btn.disabled = False
            self.uninstall_btn.disabled = False
            self.refresh_list()

        self.call_from_thread(_finalize_install)

    def run_uninstall_sync(self, name: str):
        self.installing = True
        self.call_from_thread(lambda: setattr(self.install_btn, "disabled", True))
        self.call_from_thread(lambda: setattr(self.uninstall_btn, "disabled", True))
        self.log_buffer.clear()
        self.call_from_thread(lambda: self.update_log(f"Uninstalling {name}...\n"))

        try:
            subprocess.call(["apt-mark", "unhold", name],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass

        proc = subprocess.Popen(
            ["apt-get", "remove", "-y", name],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        for line in iter(proc.stdout.readline, b""):
            clean_line = strip_ansi(line.decode(errors="ignore").rstrip())
            if clean_line:
                self.call_from_thread(
                    lambda t=clean_line: self.update_log(t)
                )

        proc.wait()

        if proc.returncode == 0:
            self.call_from_thread(lambda: self.update_log(f"\n✔ {name} uninstalled successfully!"))
        else:
            self.call_from_thread(lambda: self.update_log(f"\n✗ Uninstall failed (exit code {proc.returncode})"))

        self.installing = False
        self.status_cache.clear()
        self.load_packages()

        def _finalize_uninstall():
            self.install_btn.disabled = False
            self.uninstall_btn.disabled = False
            self.refresh_list()

        self.call_from_thread(_finalize_uninstall)

    def update_log(self, line=None):
        if line:
            self.log_buffer.append(line)
            self.log_buffer = self.log_buffer[-500:]
        self.log_view.update("\n".join(self.log_buffer))
        self.log_container.scroll_end(animate=False)

def run_tui():
    TermuxAppStore().run()

if __name__ == "__main__": # pragma: no cover
    run_tui()
