import hashlib
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
import urllib.request
from collections import deque
from pathlib import Path
from typing import Callable, Optional

GITHUB_REPO = "djunekz/termux-app-store"
FINGERPRINT_STRING = "Termux App Store Official"
RAW_BASE = f"https://raw.githubusercontent.com/{GITHUB_REPO}/master"
INDEX_URL = f"{RAW_BASE}/tools/index.json"

MIRRORS = [
    {
        "id": "cloudflare",
        "name": "Cloudflare CDN",
        "base_url": "https://termux-app-store.pages.dev",
        "priority": 1,
        "index": True,
    },
    {
        "id": "github-pages",
        "name": "GitHub Pages",
        "base_url": "https://djunekz.github.io/termux-app-store",
        "priority": 2,
        "index": True,
    },
    {
        "id": "jsdelivr",
        "name": "jsDelivr CDN",
        "base_url": "https://cdn.jsdelivr.net/gh/djunekz/termux-app-store@gh-pages",
        "priority": 3,
        "index": False,
    },
]

PKG_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._+-]*$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")

LogFn = Callable[[str, str], None]


def index_urls() -> list:
    return [INDEX_URL] + [f"{m['base_url']}/tools/index.json" for m in MIRRORS if m.get("index")]


def _cache_dir() -> Path:
    return Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "termux-app-store"


CACHE_FILE = _cache_dir() / "path.json"
INDEX_CACHE_FILE = _cache_dir() / "index.json"


def format_size(num) -> str:
    try:
        value = float(num)
    except (TypeError, ValueError):
        return "Unknown"
    if value < 0:
        return "Unknown"
    if value < 1024:
        return f"{int(value)} B"
    for unit in ("KB", "MB", "GB"):
        value /= 1024
        if value < 1024 or unit == "GB":
            return f"{value:.1f} {unit}"
    return "Unknown"


class RateTracker:
    def __init__(self, window: float = 4.0, alpha: float = 0.3):
        self.window = window
        self.alpha = alpha
        self._samples: deque = deque()
        self._ema = 0.0

    def add(self, done: float, now: Optional[float] = None) -> None:
        now = time.monotonic() if now is None else now
        self._samples.append((now, done))
        while len(self._samples) > 2 and now - self._samples[0][0] > self.window:
            self._samples.popleft()
        first_time, first_done = self._samples[0]
        span = now - first_time
        if span >= 0.4 and done > first_done:
            instant = (done - first_done) / span
            self._ema = instant if self._ema <= 0 else self._ema + self.alpha * (instant - self._ema)

    @property
    def rate(self) -> float:
        return self._ema

    def remaining(self, total: float, done: float, fallback_rate: float = 0.0) -> float:
        rate = self._ema if self._ema > 0 else fallback_rate
        if rate <= 0 or total <= done:
            return 0.0
        return (total - done) / rate


def write_json_atomic(path: Path, data) -> bool:
    tmp_name = None
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_name = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(data, handle)
        os.replace(tmp_name, path)
        return True
    except Exception:
        if tmp_name:
            try:
                os.unlink(tmp_name)
            except OSError:
                pass
        return False


def read_json(path: Path, expected: type):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return expected()
    return data if isinstance(data, expected) else expected()


class SpeedStats:
    def __init__(self, path: Path):
        self.path = path

    def get(self, key: str, default: float) -> float:
        value = read_json(self.path, dict).get(key)
        if isinstance(value, (int, float)) and value > 0:
            return float(value)
        return default

    def update(self, key: str, value: float, alpha: float = 0.4) -> None:
        if not isinstance(value, (int, float)) or value <= 0:
            return
        data = read_json(self.path, dict)
        old = data.get(key)
        if isinstance(old, (int, float)) and old > 0:
            value = old + alpha * (value - old)
        data[key] = round(float(value), 4)
        write_json_atomic(self.path, data)


class Settings:
    def __init__(self, path: Path, defaults: Optional[dict] = None):
        self.path = path
        self.defaults = dict(defaults or {})

    def get(self, key: str, default=None):
        data = read_json(self.path, dict)
        if key in data:
            return data[key]
        return self.defaults.get(key, default)

    def set(self, key: str, value) -> None:
        data = read_json(self.path, dict)
        data[key] = value
        write_json_atomic(self.path, data)


class ActivityLog:
    def __init__(self, path: Path, limit: int = 300):
        self.path = path
        self.limit = limit

    def add(
        self,
        action: str,
        package: str,
        version: str = "",
        result: str = "ok",
        seconds: float = 0.0,
        detail: str = "",
        now: Optional[float] = None,
    ) -> None:
        entries = read_json(self.path, list)
        entries.append(
            {
                "time": time.time() if now is None else now,
                "action": action,
                "package": package,
                "version": version,
                "result": result,
                "seconds": round(float(seconds), 1),
                "detail": detail[-1500:],
            }
        )
        write_json_atomic(self.path, entries[-self.limit :])

    def recent(self, limit: int = 50, package: Optional[str] = None) -> list:
        entries = [e for e in read_json(self.path, list) if isinstance(e, dict)]
        if package is not None:
            entries = [e for e in entries if e.get("package") == package]
        return list(reversed(entries[-limit:])) if limit > 0 else []

    def last_for(self, package: str) -> Optional[dict]:
        found = self.recent(1, package)
        return found[0] if found else None


def format_ago(then: float, now: Optional[float] = None) -> str:
    delta = (time.time() if now is None else now) - then
    if delta < 0:
        delta = 0
    if delta < 60:
        return "just now"
    if delta < 3600:
        return f"{int(delta // 60)}m ago"
    if delta < 86400:
        return f"{int(delta // 3600)}h ago"
    if delta < 86400 * 30:
        return f"{int(delta // 86400)}d ago"
    return f"{int(delta // (86400 * 30))}mo ago"


class InstallCancelled(Exception):
    pass


def terminate_process_tree(proc, grace: float = 5.0) -> None:
    try:
        own_group = os.getpgid(0)
        group = os.getpgid(proc.pid)
    except OSError:
        return
    try:
        if group == own_group:
            proc.terminate()
        else:
            os.killpg(group, signal.SIGTERM)
    except OSError:
        return
    try:
        proc.wait(timeout=grace)
    except subprocess.TimeoutExpired:
        try:
            if group == own_group:
                proc.kill()
            else:
                os.killpg(group, signal.SIGKILL)
        except OSError:
            pass


def watch_cancel(proc, cancel) -> threading.Thread:
    def _run():
        while proc.poll() is None:
            if cancel.wait(0.5):
                terminate_process_tree(proc)
                return

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()
    return thread


def _silent(kind: str, message: str) -> None:
    return None


def ver_tuple(v: str):
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


def is_safe_pkg_name(name: str) -> bool:
    return bool(name) and bool(PKG_NAME_RE.match(name)) and ".." not in name


def normalize_sha256(value) -> str:
    if not isinstance(value, str):
        return ""
    value = value.strip().lower()
    return value if SHA256_RE.match(value) else ""


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
    except OSError:
        return False
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


def load_cached_root(cache_file: Optional[Path] = None) -> Optional[Path]:
    cache_file = cache_file or CACHE_FILE
    try:
        if cache_file.exists():
            data = json.loads(cache_file.read_text())
            raw = data.get("app_root")
            if not raw or not isinstance(raw, str):
                return None
            p = Path(raw).expanduser()
            if is_valid_root(p):
                return p.resolve()
    except (OSError, ValueError, AttributeError):
        return None
    return None


def save_cached_root(path: Path, cache_file: Optional[Path] = None) -> None:
    cache_file = cache_file or CACHE_FILE
    try:
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        cache_file.write_text(json.dumps({"app_root": str(path)}, indent=2))
    except OSError:
        return None


def resolve_app_root(module_file: str, cache_file: Optional[Path] = None) -> Path:
    env = os.environ.get("TERMUX_APP_STORE_HOME")
    if env:
        p = Path(env).expanduser().resolve()
        if is_valid_root(p):
            save_cached_root(p, cache_file)
            return p

    cached = load_cached_root(cache_file)
    if cached:
        return cached

    if getattr(sys, "frozen", False):
        base = Path(sys.executable).resolve().parent
        if is_valid_root(base):
            save_cached_root(base, cache_file)
            return base

    source_base = Path(module_file).resolve().parent.parent
    if is_valid_root(source_base):
        save_cached_root(source_base, cache_file)
        return source_base

    pip_home = Path.home() / ".termux-app-store"
    pip_home.mkdir(parents=True, exist_ok=True)
    (pip_home / "packages").mkdir(exist_ok=True)
    save_cached_root(pip_home, cache_file)
    return pip_home


def load_index_cache(index_cache_file: Optional[Path] = None) -> list:
    index_cache_file = index_cache_file or INDEX_CACHE_FILE
    try:
        if index_cache_file.exists():
            data = json.loads(index_cache_file.read_text())
            return data.get("packages", [])
    except (OSError, ValueError, AttributeError):
        return []
    return []


def lookup_recipe_sha256(name: str, index_cache_file: Optional[Path] = None) -> str:
    for entry in load_index_cache(index_cache_file):
        if isinstance(entry, dict) and entry.get("package") == name:
            return normalize_sha256(entry.get("recipe_sha256"))
    return ""


def packaged_build_script() -> Optional[Path]:
    candidate = Path(__file__).resolve().parent / "data" / "build-package.sh"
    return candidate if candidate.is_file() else None


def _bash_syntax_ok(raw: bytes) -> bool:
    return subprocess.run(["bash", "-n"], input=raw, capture_output=True).returncode == 0


def verify_downloaded_script(raw: bytes, env_sha256_var: str, log: Optional[LogFn] = None) -> bool:
    log = log or _silent
    if not raw:
        return False

    expected = os.environ.get(env_sha256_var, "").strip().lower()
    actual = hashlib.sha256(raw).hexdigest()
    if expected:
        if actual != expected:
            return False
    elif os.environ.get("TERMUX_APP_STORE_ALLOW_UNVERIFIED_BUILD_SH") != "1":
        log("error", "No pinned checksum for downloaded build-package.sh")
        log("dim", f"SHA256 of download: {actual}")
        log("dim", f"Review it, then export {env_sha256_var}=<sha256> or clone the repository.")
        return False

    return _bash_syntax_ok(raw)


def ensure_build_package_sh(
    app_root: Path,
    log: Optional[LogFn] = None,
    user_agent: str = "termux-app-store",
) -> bool:
    log = log or _silent
    build_pkg = app_root / "build-package.sh"
    if build_pkg.exists():
        return True

    packaged = packaged_build_script()
    if packaged is not None:
        try:
            shutil.copy2(packaged, build_pkg)
            build_pkg.chmod(0o755)
            return True
        except OSError:
            return False

    url = f"{RAW_BASE}/build-package.sh"
    try:
        log("dim", "Downloading build-package.sh...")
        req = urllib.request.Request(url, headers={"User-Agent": user_agent})
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read()
        if raw and verify_downloaded_script(raw, "TERMUX_APP_STORE_BUILD_SH_SHA256", log):
            build_pkg.write_bytes(raw)
            build_pkg.chmod(0o755)
            log("ok", "build-package.sh ready.")
            return True
        if raw:
            log("error", "build-package.sh failed verification — refusing to use it")
    except Exception as e:
        log("error", f"Failed to download build-package.sh: {e}")
    return False


def download_recipe(
    packages_dir: Path,
    name: str,
    expected_sha256: str,
    force_update: bool = False,
    log: Optional[LogFn] = None,
    user_agent: str = "termux-app-store",
) -> bool:
    log = log or _silent
    if not is_safe_pkg_name(name):
        return False

    pkg_dir = packages_dir / name
    build_sh = pkg_dir / "build.sh"
    if build_sh.exists() and not force_update:
        return True

    expected = normalize_sha256(expected_sha256)
    if not expected and os.environ.get("TERMUX_APP_STORE_ALLOW_UNVERIFIED_RECIPE") != "1":
        log("error", f"No recipe checksum in the index for {name} — refusing to download its build.sh")
        log(
            "dim",
            "Refresh the package index, or set TERMUX_APP_STORE_ALLOW_UNVERIFIED_RECIPE=1 after reviewing the recipe.",
        )
        return False

    url = f"{RAW_BASE}/packages/{name}/build.sh"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": user_agent})
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read()
    except Exception as e:
        log("error", f"Failed to download the recipe for {name}: {e}")
        return False

    if not raw:
        return False

    actual = hashlib.sha256(raw).hexdigest()
    if expected and actual != expected:
        log("error", "Recipe SHA256 does not match the index — refusing to use it")
        log("dim", f"Expected: {expected}")
        log("dim", f"Got:      {actual}")
        return False

    if not _bash_syntax_ok(raw):
        log("error", "Downloaded recipe has a bash syntax error — refusing to use it")
        return False

    try:
        pkg_dir.mkdir(parents=True, exist_ok=True)
        tmp = build_sh.with_suffix(".part")
        tmp.write_bytes(raw)
        os.replace(tmp, build_sh)
    except OSError:
        return False
    return True
