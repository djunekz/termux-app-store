#!/usr/bin/env python3
import asyncio
import subprocess
import sys
import os
import json
import re
import urllib.request
from pathlib import Path

try:
    from termux_app_store.fast_install import FastInstaller
    from termux_app_store.core.package import Package
    _BINARY_CACHE_AVAILABLE = True
except ImportError:
    _BINARY_CACHE_AVAILABLE = False

try:
    from termux_app_store.fast_install import fast_install, check_mirrors, cache_info, clear_deb_cache
    _FAST_INSTALL_AVAILABLE = True
except ImportError:
    try:
        from fast_install import fast_install, check_mirrors, cache_info, clear_deb_cache
        _FAST_INSTALL_AVAILABLE = True
    except ImportError:
        _FAST_INSTALL_AVAILABLE = False

try:
    from textual.app import App, ComposeResult, SystemCommand
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
    from textual.containers import Horizontal, Vertical, VerticalScroll
    from textual.reactive import reactive
    from textual.widget import Widget

    class SimpleProgressBar(Widget):
        DEFAULT_CSS = """
        SimpleProgressBar {
            height: 1;
            margin-top: 1;
        }
        """
        progress: reactive[float] = reactive(0.0)

        def __init__(self, total: float = 100, **kwargs):
            super().__init__(**kwargs)
            self.total = total
            self._eta_seconds: float = 0.0
            self._start_time: float = 0.0
            self._last_pct: float = 0.0

        def on_mount(self):
            def _tick():
                if self._eta_seconds > 0 and self.get_remaining() > 0:
                    self.refresh()
            self.set_interval(1.0, _tick)

        def set_eta(self, seconds: float):
            self._eta_seconds = max(0.0, seconds)
            self._start_time = __import__("time").monotonic()
            self._last_pct = self.progress

        def get_remaining(self) -> float:
            if self._eta_seconds <= 0:
                return 0.0
            elapsed = __import__("time").monotonic() - self._start_time
            return max(0.0, self._eta_seconds - elapsed)

        def render(self):
            pct = min(100, max(0, int(self.progress / self.total * 100)))
            remaining = self.get_remaining()

            if remaining > 0 and pct < 100:
                mins = int(remaining) // 60
                secs = int(remaining) % 60
                eta_str = f"{mins:02d}:{secs:02d}"
            else:
                eta_str = "--:--"

            suffix = f" {pct:3d}% {eta_str}"
            width = self.size.width - len(suffix)
            if width < 1:
                width = 1
            filled = int(width * pct / 100)
            bar = "━" * filled + "─" * (width - filled)
            return f"{bar}{suffix}"

    _TEXTUAL_AVAILABLE = True
except ImportError:
    App = object  # type: ignore
    ComposeResult = None  # type: ignore
    _TEXTUAL_AVAILABLE = False

    class _Stub:
        class Pressed: pass
        class Changed: pass
        class Highlighted: pass
    Header = Input = ListView = ListItem = Label = _Stub
    Static = Button = ProgressBar = SimpleProgressBar = _Stub
    Horizontal = Vertical = VerticalScroll = _Stub

CACHE_FILE = (
    Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
    / "termux-app-store"
    / "path.json"
)

INDEX_CACHE_FILE = (
    Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
    / "termux-app-store"
    / "index.json"
)

FINGERPRINT_STRING = "Termux App Store Official"
GITHUB_REPO        = "djunekz/termux-app-store"
INDEX_URL          = f"https://raw.githubusercontent.com/{GITHUB_REPO}/master/tools/index.json"

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
    if not path.is_dir():
        return False
    if not (path / "packages").is_dir():
        return False
    pip_home = Path.home() / ".termux-app-store"
    if path.resolve() == pip_home.resolve():
        return True
    return (path / "build-package.sh").is_file() and has_store_fingerprint(path)

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

    if getattr(sys, "frozen", False):
        base = Path(sys.executable).resolve().parent
        if is_valid_root(base):
            save_cached_root(base)
            return base

    source_base = Path(__file__).resolve().parent.parent
    if is_valid_root(source_base):
        save_cached_root(source_base)
        return source_base

    pip_home = Path.home() / ".termux-app-store"
    pip_home.mkdir(parents=True, exist_ok=True)
    (pip_home / "packages").mkdir(exist_ok=True)
    save_cached_root(pip_home)
    return pip_home

def ensure_build_package_sh() -> bool:
    app_root = get_app_root()
    build_pkg = app_root / "build-package.sh"
    if build_pkg.exists():
        return True
    url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/master/build-package.sh"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "termux-app-store"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read()
            if raw:
                build_pkg.write_bytes(raw)
                build_pkg.chmod(0o755)
                return True
    except Exception:
        pass
    return False


def fetch_index_from_github() -> list:
    try:
        req = urllib.request.Request(
            INDEX_URL,
            headers={"User-Agent": "termux-app-store"},
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode())
            pkgs = data.get("packages", [])
            try:
                INDEX_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
                INDEX_CACHE_FILE.write_text(json.dumps(data, indent=2))
            except Exception:
                pass
            return pkgs
    except Exception:
        if INDEX_CACHE_FILE.exists():
            try:
                data = json.loads(INDEX_CACHE_FILE.read_text())
                return data.get("packages", [])
            except Exception:
                pass
        return []




_PKG_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._+-]*$")

def is_safe_pkg_name(name: str) -> bool:
    return bool(name) and bool(_PKG_NAME_RE.match(name)) and ".." not in name

def ensure_package_files(name: str) -> bool:
    if not is_safe_pkg_name(name):
        return False

    pkg_dir = get_packages_dir() / name
    build_sh = pkg_dir / "build.sh"

    if build_sh.exists():
        return True

    url = (
        f"https://raw.githubusercontent.com/{GITHUB_REPO}/master/packages/{name}/build.sh"
    )
    try:
        pkg_dir.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(url, headers={"User-Agent": "termux-app-store"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read()
            if raw:
                build_sh.write_bytes(raw)
                return True
    except Exception:
        pass
    return False

def load_index_cache() -> list:
    try:
        if INDEX_CACHE_FILE.exists():
            data = json.loads(INDEX_CACHE_FILE.read_text())
            return data.get("packages", [])
    except Exception:
        pass
    return []

def load_packages_from_local(packages_dir: Path) -> list:
    pkgs = []
    if not packages_dir.exists():
        return pkgs
    for pkg_dir in sorted(packages_dir.iterdir()):
        build = pkg_dir / "build.sh"
        if not build.exists():
            continue
        data = {
            "package": pkg_dir.name,
            "description": "-",
            "version": "?",
            "depends": [],
            "maintainer": "-",
        }
        with build.open(errors="ignore") as f:
            for line in f:
                if line.startswith("TERMUX_PKG_DESCRIPTION="):
                    data["description"] = line.split("=", 1)[1].strip().strip('"')
                elif line.startswith("TERMUX_PKG_VERSION="):
                    data["version"] = line.split("=", 1)[1].strip().strip('"')
                elif line.startswith("TERMUX_PKG_DEPENDS="):
                    deps_str = line.split("=", 1)[1].strip().strip('"')
                    data["depends"] = [d.strip() for d in deps_str.split(",") if d.strip()]
                elif line.startswith("TERMUX_PKG_MAINTAINER="):
                    data["maintainer"] = line.split("=", 1)[1].strip().strip('"')
        pkgs.append(data)
    return pkgs

def normalize_pkg(raw: dict) -> dict:
    deps = raw.get("depends", [])
    if isinstance(deps, str):
        deps = [d.strip() for d in deps.split(",") if d.strip()]
    result = {
        "name":       raw.get("package", raw.get("name", "?")),
        "desc":       raw.get("description", raw.get("desc", "-")),
        "version":    raw.get("version", "?"),
        "deps":       deps,
        "maintainer": raw.get("maintainer", "-"),
    }
    if "sha256" in raw:
        result["sha256"] = raw["sha256"]
    if "sha256_by_arch" in raw:
        result["sha256_by_arch"] = raw["sha256_by_arch"]
    return result

def get_packages(packages_dir: Path, online: bool = True) -> list:
    if online:
        raw = fetch_index_from_github()
        if raw:
            return [normalize_pkg(p) for p in raw]

    cached = load_index_cache()
    if cached:
        return [normalize_pkg(p) for p in cached]

    raw = load_packages_from_local(packages_dir)
    return [normalize_pkg(p) for p in raw]


_APP_ROOT = None

def get_app_root() -> Path:
    global _APP_ROOT
    if _APP_ROOT is None:
        _APP_ROOT = resolve_app_root()
    return _APP_ROOT

def get_packages_dir() -> Path:
    return get_app_root() / "packages"


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

    def on_button_pressed(self, event) -> None: # pragma: no cover
        if event.button.id == "btn-cancel":
            self.dismiss(False)
        elif event.button.id == "btn-confirm-uninstall":
            self.dismiss(True)



class AboutScreen(_ModalScreen):

    DEFAULT_CSS = """
    AboutScreen {
        align: center middle;
    }
    #about-dialog {
        width: 70;
        height: auto;
        border: heavy #6272a4;
        background: #282a36;
        padding: 2 4;
    }
    #about-title {
        text-align: center;
        color: #50fa7b;
        text-style: bold;
        margin-bottom: 1;
    }
    #about-body {
        color: #f8f8f2;
        margin-bottom: 2;
    }
    #about-disclaimer {
        color: #ffb86c;
        text-style: italic;
        margin-bottom: 2;
    }
    #about-close-row {
        align: center middle;
        height: auto;
    }
    """

    def compose(self) -> ComposeResult:  # pragma: no cover
        import importlib.metadata as _meta
        import sys as _sys
        from pathlib import Path as _Path

        app_version = "unknown"
        try:
            init_candidates = [
                _Path(__file__).resolve().parent / "__init__.py",
                _Path(__file__).resolve().parent.parent / "__init__.py",
            ]
            for _p in init_candidates:
                if _p.exists():
                    for _line in _p.read_text(errors="ignore").splitlines():
                        if _line.strip().startswith("__version__"):
                            app_version = _line.split("=", 1)[1].strip().strip("\"' ")
                            break
                if app_version != "unknown":
                    break
        except Exception:
            pass

        try:
            textual_ver = _meta.version("textual")
        except Exception:
            textual_ver = "unknown"

        py_ver = _sys.version.split()[0]

        with Vertical(id="about-dialog"):
            yield Static("📦  Termux App Store", id="about-title")
            yield Static(
                f"[b]Version[/b]       : {app_version}\n"
                f"[b]Official Repo[/b] : github.com/djunekz/termux-app-store\n"
                f"[b]Developer[/b]     : Djunekz\n"
                f"[b]License[/b]       : MIT\n"
                f"\n"
                f"[b]Built with[/b]    : Textual v{textual_ver}\n"
                f"[b]Runtime[/b]       : Python {py_ver} on Termux (Android)\n"
                f"\n"
                "Termux App Store is a community-driven package manager\n"
                "for Termux — providing easy installation of tools and apps\n"
                "not available in the official Termux repository.",
                id="about-body",
            )
            yield Static(
                "⚠ [b]DISCLAIMER![/b]\n"
                "If this app was NOT obtained from\n"
                "[b]https://github.com/djunekz/termux-app-store[/b]\n"
                "it is NOT the original version and may contain\n"
                "modified or malicious code. Use at your own risk.",
                id="about-disclaimer",
            )
            with Horizontal(id="about-close-row"):
                yield Button("Close", id="about-close")

    def on_button_pressed(self, event) -> None:  # pragma: no cover
        if event.button.id == "about-close":
            self.dismiss()


class ContactScreen(_ModalScreen):

    DEFAULT_CSS = """
    ContactScreen {
        align: center middle;
    }
    #contact-dialog {
        width: 70;
        height: auto;
        max-height: 90vh;
        border: heavy #8be9fd;
        background: #282a36;
        padding: 1 3 2 3;
        overflow-y: auto;
    }
    #contact-title {
        text-align: center;
        color: #8be9fd;
        text-style: bold;
        margin-bottom: 1;
    }
    .contact-section {
        color: #50fa7b;
        text-style: bold;
        margin-top: 1;
    }
    .contact-row {
        color: #f8f8f2;
        padding-left: 1;
    }
    .contact-spacer {
        height: 0;
    }
    #contact-disclaimer {
        color: #ffb86c;
        margin-top: 1;
        padding-left: 1;
    }
    #contact-close-row {
        align: center middle;
        height: auto;
        margin-top: 2;
    }
    #btn-open-issue {
        margin-right: 2;
        background: #6272a4;
        color: #f8f8f2;
    }
    #btn-open-issue:hover { background: #7b88b8; }
    #btn-close-contact {
        background: #44475a;
        color: #f8f8f2;
    }
    #btn-close-contact:hover { background: #6272a4; }
    """

    def compose(self) -> ComposeResult:  # pragma: no cover
        with Vertical(id="contact-dialog"):
            yield Static(" Contact & Support", id="contact-title")

            yield Static("[b]Official Repo[/b]      : github.com/djunekz/termux-app-store", classes="contact-row")
            yield Static("[b]Official Developer[/b] : Djunekz", classes="contact-row")
            yield Static("[b]License[/b]            : MIT", classes="contact-row")
            yield Static("[b]Website[/b]            : djunekz.github.io/termux-app-store", classes="contact-row")

            yield Static("", classes="contact-spacer")
            yield Static("[b]GitHub Issues[/b]", classes="contact-section")
            yield Static(
                "  Report bugs or request features:\n"
                "  github.com/djunekz/termux-app-store/issues",
                classes="contact-row",
            )

            yield Static("", classes="contact-spacer")
            yield Static("[b]GitHub Discussions[/b]", classes="contact-section")
            yield Static(
                "  Community help & general questions:\n"
                "  github.com/djunekz/termux-app-store/discussions",
                classes="contact-row",
            )

            yield Static("", classes="contact-spacer")
            yield Static("[b]Email[/b]", classes="contact-section")
            yield Static("  gab288.gab288@passinbox.com", classes="contact-row")

            yield Static("", classes="contact-spacer")
            yield Static(
                "⚠ [b]DISCLAIMER![/b]\n"
                "  Only content from\n"
                "  [b]github.com/djunekz/termux-app-store[/b]\n"
                "  is considered official.\n"
                "  Redistribution from other sources is [b]NOT original[/b]\n"
                "  and may have been tampered with.",
                id="contact-disclaimer",
            )
            with Horizontal(id="contact-close-row"):
                yield Button("Open GitHub Issues", id="btn-open-issue")
                yield Button("Close", id="btn-close-contact")

    def on_button_pressed(self, event) -> None:  # pragma: no cover
        if event.button.id == "btn-open-issue":
            try:
                import subprocess as _sp
                _sp.Popen(
                    ["termux-open-url",
                     "https://github.com/djunekz/termux-app-store/issues"],
                    stdout=_sp.DEVNULL, stderr=_sp.DEVNULL,
                )
            except Exception:
                pass
            self.dismiss()
        elif event.button.id == "btn-close-contact":
            self.dismiss()


class TermuxAppStore(App):

    BINDINGS = [
        ("ctrl+r", "refresh", "Refresh packages"),
        ("ctrl+i", "install_selected", "Install selected"),
        ("ctrl+q", "quit", "Quit"),
    ]

    CSS = """
    Screen {
        background: #282a36;
        color: #f8f8f2;
        layout: vertical;
    }
    #body {
        layout: horizontal;
        height: 1fr;
        width: 100%;
    }
    #left {
        width: 35%;
        border: heavy #6272a4;
        padding: 0 1 1 1;
        layout: vertical;
    }
    #search {
        height: 3;
        margin-bottom: 1;
    }
    #pkg-list {
        height: 1fr;
    }
    #right {
        width: 65%;
        border: heavy #6272a4;
        padding: 1;
        layout: vertical;
    }
    ListItem.--highlight { background: #44475a; color: #50fa7b; }
    #footer { height: 1; content-align: center middle; color: #6272a4; }
    #log-scroll { height: 1fr; border: solid #6272a4; margin-top: 1; }
    #btn-row { height: auto; margin-top: 1; }
    #install { margin-right: 1; }
    #uninstall { background: #ff5555; color: #f8f8f2; display: none; }
    #uninstall:hover { background: #ff6e6e; }
    #uninstall:disabled { background: #44475a; color: #6272a4; }
    #status-bar { height: 1; content-align: left middle; color: #6272a4; padding-left: 1; }
    """

    async def on_mount(self): # pragma: no cover
        self.packages = []
        self.status_cache = {}
        self.search_query = ""
        self.current_item = None
        self.installing = False
        self.log_buffer = []
        self.worker_queue = asyncio.Queue()

        self.set_interval(0.1, self.consume_worker_queue)

        self.load_packages(online=False)
        self.refresh_list()

        self.run_worker(self._fetch_online_worker(), exclusive=False)

        self.binary_installer = FastInstaller() if _BINARY_CACHE_AVAILABLE else None

    async def _fetch_online_worker(self): # pragma: no cover
        try:
            raw = await asyncio.to_thread(fetch_index_from_github)
            if not raw:
                return

            new_packages = [normalize_pkg(p) for p in raw]

            old_names = {p["name"] for p in self.packages}
            new_names = {p["name"] for p in new_packages}
            if old_names == new_names:
                return

            self.packages = new_packages
            self.status_cache.clear()
            self.refresh_list(preserve_selection=True)
        except Exception:
            pass

    async def run_install(self, name: str):
        if self.installing:
            return

        self.installing = True
        self.install_btn.disabled = True
        self.uninstall_btn.disabled = True

        self.log_buffer.clear()
        self.update_log(f"Starting installation: {name}\n")
        self.progress.progress = 5
        self.progress.set_eta(0)

        success = False

        def _progress(p):
            self.progress.progress = p

        def _eta(seconds):
            self.progress.set_eta(seconds)

        try:
            if _FAST_INSTALL_AVAILABLE:
                self.update_log("⚙ Fast Install...\n")
                success = await asyncio.to_thread(
                    fast_install,
                    name,
                    self.update_log,
                    _progress,
                    _eta,
                )

            if not success:
                self.update_log("Building from source...\n")
                success = await asyncio.to_thread(self._build_from_source_with_progress, name)

        except Exception as e:
            self.update_log(f"❌ Error: {e}\n")

        if success:
            self.progress.progress = 100
            self.progress.set_eta(0)
            self.update_log(f"\n✅ {name} installed successfully!")
        else:
            self.update_log(f"\n❌ Failed to install {name}")

        self.installing = False
        self.install_btn.disabled = False
        self.uninstall_btn.disabled = False
        self.status_cache.clear()
        self.refresh_list()

    def _build_from_source_with_progress(self, name: str) -> bool:
        app_root = get_app_root()
        build_sh = app_root / "build-package.sh"

        if not build_sh.exists():
            self.update_log("build-package.sh not found!")
            return False

        STAGE_FLOORS = [
            ("Downloading",          15),
            ("Checksum",             20),
            ("Extracting",           25),
            ("Source root",          30),
            ("Installing Files",     40),
            ("termux_step_make",     50),
            ("Generating Package",   70),
            ("Control file",         72),
            ("Building .deb",        75),
            ("Running dpkg-deb",     78),
            ("built successfully",   82),
            ("Installing Package",   85),
            ("Running dpkg",         87),
            ("Selecting previously", 88),
            ("Unpacking",            90),
            ("Setting up",           94),
        ]

        current_pct = [10]

        def _set_progress(pct):
            if pct > current_pct[0]:
                current_pct[0] = pct
                self.call_from_thread(
                    lambda p=pct: setattr(self.progress, "progress", p)
                )

        self.call_from_thread(lambda: self.progress.set_eta(180))
        _set_progress(10)

        proc = subprocess.Popen(
            ["bash", str(build_sh), name],
            cwd=str(app_root),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        for line in iter(proc.stdout.readline, b""):
            clean = strip_ansi(line.decode(errors="ignore").rstrip())
            if not clean:
                continue
            self.update_log(clean)
            for keyword, floor in STAGE_FLOORS:
                if keyword.lower() in clean.lower():
                    _set_progress(floor)
                    break

        proc.wait()
        _set_progress(95)
        return proc.returncode == 0


    def _build_from_source(self, name: str):
        app_root = get_app_root()
        build_sh = app_root / "build-package.sh"

        if not build_sh.exists():
            self.update_log("build-package.sh not found!")
            return False

        proc = subprocess.Popen(
            ["bash", str(build_sh), name],
            cwd=str(app_root),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        for line in iter(proc.stdout.readline, b""):
            clean = strip_ansi(line.decode(errors="ignore").rstrip())
            if clean:
                self.update_log(clean)

        proc.wait()
        return proc.returncode == 0

    def compose(self) -> ComposeResult: # pragma: no cover
        yield Header()

        with Horizontal(id="body"):
            with Vertical(id="left"):
                self.search_input = Input(placeholder="Search package...", id="search")
                yield self.search_input

                self.list_view = ListView(id="pkg-list")
                yield self.list_view

            with Vertical(id="right"):
                self.info = Static("Select a package", id="info")
                yield self.info

                with VerticalScroll(id="log-scroll") as self.log_container:
                    self.log_view = Static("", markup=False)
                    yield self.log_view

                self.progress = SimpleProgressBar(total=100)
                yield self.progress

                with Horizontal(id="btn-row"):
                    self.install_btn = Button("Install / Update", id="install")
                    yield self.install_btn

                    self.uninstall_btn = Button("Uninstall", id="uninstall")
                    self.uninstall_btn.display = False
                    yield self.uninstall_btn

        self.status_bar = Static("", id="status-bar")
        yield self.status_bar
        yield Static("Official Developer @djunekz | Termux App Store", id="footer")

    def load_packages(self, online: bool = False):
        self.packages = get_packages(get_packages_dir(), online=online)
        self.status_cache.clear()

    def refresh_list(self, preserve_selection: bool = False):
        current_name = None
        if preserve_selection and self.current_item:
            current_name = self.current_item.pkg.get("name")

        self.list_view.clear()
        q = self.search_query

        restored = False
        for pkg in self.packages:
            if q == "" or q in pkg["name"].lower() or q in pkg["desc"].lower():
                self.list_view.append(PackageItem(pkg))

        if self.list_view.children:
            if current_name:
                for i, child in enumerate(self.list_view.children):
                    if hasattr(child, "pkg") and child.pkg.get("name") == current_name:
                        self.list_view.index = i
                        restored = True
                        break

            if not restored:
                self.list_view.index = 0
                first = self.list_view.query(PackageItem).first(PackageItem)
                if first:
                    self.show_preview(first)

    def on_input_changed(self, message):
        self.search_query = message.value.lower().strip()
        self.refresh_list()

    def on_list_view_highlighted(self, event):
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

        deps = p.get("deps", [])
        if isinstance(deps, list):
            deps_str = "\n".join(f"• {d}" for d in deps) if deps else "-"
        else:
            deps_str = "\n".join(f"• {d.strip()}" for d in deps.split(",") if d.strip()) if deps != "-" else "-"

        self.info.update(
            f"[b]{p['name']}[/b]  {badge}\n\n"
            f"{ver_line}\n"
            f"Maintainer : {p['maintainer']}\n\n"
            f"[b]Dependencies[/b]\n{deps_str}\n\n"
            f"{p['desc']}"
        )

        self.log_buffer.clear()
        self.log_view.update("")
        self.progress.progress = 0

        is_installed = status in ("INSTALLED", "UPDATE")
        self.uninstall_btn.display = is_installed

    async def on_button_pressed(self, event):
        if self.installing:
            return

        if event.button.id == "install" and self.current_item:
            await self.worker_queue.put(("install", self.current_item.pkg["name"]))

        elif event.button.id == "uninstall" and self.current_item:
            name = self.current_item.pkg["name"]
            def handle_confirm(confirmed: bool) -> None: # pragma: no cover
                if confirmed:
                    asyncio.get_running_loop().call_soon_threadsafe(
                        lambda: self.worker_queue.put_nowait(("uninstall", name))
                    )
            self.push_screen(ConfirmUninstall(name), handle_confirm)

    async def consume_worker_queue(self):
        if self.installing or self.worker_queue.empty():
            return
        action, name = await self.worker_queue.get()
        if action == "install":
            await self.run_install(name)
        elif action == "uninstall":
            await asyncio.to_thread(self.run_uninstall_sync, name)

    def run_build_sync(self, name: str):
        self.installing = True
        self.call_from_thread(lambda: setattr(self.install_btn, "disabled", True))
        self.call_from_thread(lambda: setattr(self.uninstall_btn, "disabled", True))
        self.log_buffer.clear()
        self.call_from_thread(lambda: setattr(self.progress, "progress", 0))
        self.call_from_thread(lambda: self.update_log(f"Installing {name}...\n"))

        success = False

        if _FAST_INSTALL_AVAILABLE:
            def _log(msg):
                self.call_from_thread(lambda t=msg: self.update_log(t))

            def _progress(pct):
                self.call_from_thread(
                    lambda p=pct: setattr(self.progress, "progress", p)
                )

            success = fast_install(
                pkg_name=name,
                log_fn=_log,
                progress_fn=_progress,
            )
        else:
            self.call_from_thread(lambda: self.update_log(
                "Fast install unavailable — building from source...\n"
            ))

            if not ensure_package_files(name):
                self.call_from_thread(
                    lambda: self.update_log(f"\n✗ Failed to download build files for {name}.")
                )
            elif not ensure_build_package_sh():
                self.call_from_thread(
                    lambda: self.update_log("\n✗ Failed to download build-package.sh.")
                )
            else:
                proc = subprocess.Popen(
                    ["bash", "build-package.sh", name],
                    cwd=str(get_app_root()),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                )
                for line in iter(proc.stdout.readline, b""):
                    clean_line = strip_ansi(line.decode(errors="ignore").rstrip())
                    if clean_line:
                        self.call_from_thread(lambda t=clean_line: self.update_log(t))
                proc.wait()
                success = proc.returncode == 0

        if success:
            self.call_from_thread(lambda: setattr(self.progress, "progress", 100))
            self.call_from_thread(
                lambda: self.update_log("\n✔ Installation completed successfully!")
            )
        else:
            self.call_from_thread(
                lambda: self.update_log("\n✗ Installation failed.")
            )

        self.installing = False
        self.status_cache.clear()
        self.load_packages(online=False)

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
        self.load_packages(online=False)

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

    def action_check_mirrors(self):  # pragma: no cover
        if not _FAST_INSTALL_AVAILABLE:
            self.status_bar.update("Fast install not available.")
            return
        self.log_buffer.clear()
        self.update_log("Checking mirrors...\n")
        def _run():
            check_mirrors(log_fn=lambda m: self.call_from_thread(lambda t=m: self.update_log(t)))
        import threading
        threading.Thread(target=_run, daemon=True).start()

    def action_cache_info(self):  # pragma: no cover
        if not _FAST_INSTALL_AVAILABLE:
            self.status_bar.update("Fast install not available.")
            return
        self.log_buffer.clear()
        cache_info(log_fn=lambda m: self.update_log(m))

    def action_clear_cache(self):  # pragma: no cover
        if not _FAST_INSTALL_AVAILABLE:
            self.status_bar.update("Fast install not available.")
            return
        clear_deb_cache(log_fn=lambda m: self.update_log(m))
        self.status_bar.update("Cache cleared.")

    def action_refresh(self):  # pragma: no cover
        self.status_bar.update("🔄 Refreshing package list...")
        self.run_worker(self._fetch_online_worker(), exclusive=False)

    def action_focus_search(self):  # pragma: no cover
        self.query_one("#search", Input).focus()

    def action_about(self):  # pragma: no cover
        self.push_screen(AboutScreen())

    def action_contact(self):  # pragma: no cover
        self.push_screen(ContactScreen())

    def action_install_selected(self):  # pragma: no cover
        if self.current_item and not self.installing:
            self.worker_queue.put_nowait(("install", self.current_item.pkg["name"]))

    def action_clear_log(self):  # pragma: no cover
        self.log_buffer.clear()
        self.log_view.update("")
        self.status_bar.update("Log cleared.")

    def action_copy_pkg_name(self):  # pragma: no cover
        if self.current_item:
            name = self.current_item.pkg["name"]
            try:
                subprocess.run(["termux-clipboard-set", name],
                               capture_output=True, timeout=3)
                self.status_bar.update(f"Copied: {name}")
            except Exception:
                self.status_bar.update(f"Package name: {name}  (clipboard unavailable)")

    def action_open_homepage(self):  # pragma: no cover
        if self.current_item:
            pkg = self.current_item.pkg
            url = pkg.get("url") or f"https://github.com/search?q={pkg['name']}"
            try:
                subprocess.Popen(["termux-open-url", url],
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                self.status_bar.update(f"Opening: {url}")
            except Exception:
                self.status_bar.update(f"URL: {url}")

    def action_show_installed(self):  # pragma: no cover
        self.search_query = "__installed__"
        self.list_view.clear()
        for pkg in self.packages:
            installed = get_installed_version(pkg["name"])
            if installed is not None:
                self.list_view.append(PackageItem(pkg))
        self.status_bar.update("Showing installed packages only. Press Ctrl+F to reset.")

    def action_update_all(self):  # pragma: no cover
        updates = []
        for pkg in self.packages:
            installed = get_installed_version(pkg["name"])
            if installed and _ver_tuple(installed) < _ver_tuple(pkg["version"]):
                updates.append(pkg["name"])
        if not updates:
            self.status_bar.update("✔ All packages are up to date.")
            return
        self.status_bar.update(f"Queuing {len(updates)} update(s)...")
        for name in updates:
            self.worker_queue.put_nowait(("install", name))

    def get_system_commands(self, screen):  # pragma: no cover
        yield SystemCommand(
            "Check mirrors",
            "Check speed of all download mirrors",
            self.action_check_mirrors,
        )
        yield SystemCommand(
            "Cache info",
            "Show downloaded .deb cache info",
            self.action_cache_info,
        )
        yield SystemCommand(
            "Clear cache",
            "Delete all cached .deb files",
            self.action_clear_cache,
        )
        yield SystemCommand(
            "Refresh packages",
            "Fetch the latest package list from GitHub",
            self.action_refresh,
        )
        yield SystemCommand(
            "Contact Support",
            "GitHub Issues, Discussions, email, and official disclaimer",
            self.action_contact,
        )
        yield SystemCommand(
            "Install selected package",
            "Install or update the currently highlighted package",
            self.action_install_selected,
        )
        yield SystemCommand(
            "Show installed packages",
            "Filter list to only packages already installed",
            self.action_show_installed,
        )
        yield SystemCommand(
            "Update all packages",
            "Queue an update for every package that has a newer version",
            self.action_update_all,
        )
        yield SystemCommand(
            "About",
            "App version, Textual info, and disclaimer",
            self.action_about,
        )
        yield SystemCommand(
            "Open homepage",
            "Open the selected package's GitHub page in browser",
            self.action_open_homepage,
        )
        yield SystemCommand(
            "Clear log",
            "Clear the install/uninstall log output",
            self.action_clear_log,
        )
        yield SystemCommand(
            "Quit",
            "Exit Termux App Store",
            self.action_quit,
        )

def run_tui():
    get_app_root()
    TermuxAppStore().run()

if __name__ == "__main__": # pragma: no cover
    run_tui()
