#!/usr/bin/env python3
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional, Callable

try:
    from termux_app_store import store_common as _common
except ImportError:
    try:
        import store_common as _common
    except ImportError:
        import importlib.util as _ilu
        _spec = _ilu.spec_from_file_location(
            "store_common", Path(__file__).resolve().with_name("store_common.py")
        )
        _common = _ilu.module_from_spec(_spec)
        sys.modules["store_common"] = _common
        _spec.loader.exec_module(_common)

GITHUB_REPO   = _common.GITHUB_REPO
CACHE_BASE    = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "termux-app-store"
DEB_CACHE_DIR = CACHE_BASE / "debs"
MIRROR_CACHE  = CACHE_BASE / "best-mirror.json"
INDEX_CACHE   = CACHE_BASE / "index.json"

MIRROR_TTL    = 86400   # 24 hours
DEB_TTL       = 604800  # 7 days
INDEX_TTL     = 3600    # 1 hours

MIRRORS = _common.MIRRORS

DEB_PATH_PATTERN = "pool/main/{pkg}_{version}_{arch}.deb"

SHA256_SIDECAR_URL = (
    f"https://raw.githubusercontent.com/{GITHUB_REPO}/gh-pages/pool/main/"
    "{pkg}_{version}_{arch}.deb.sha256"
)

_SAFE_PKG   = _common.PKG_NAME_RE
_SAFE_VER   = re.compile(r"^[A-Za-z0-9][A-Za-z0-9.+~:-]*$")
_SAFE_ARCH  = re.compile(r"^[a-z0-9_]+$")
_SHA256_RE  = re.compile(r"^[0-9a-f]{64}$")

INDEX_URLS = _common.index_urls()

CACHE_BASE.mkdir(parents=True, exist_ok=True)
DEB_CACHE_DIR.mkdir(parents=True, exist_ok=True)

def _valid_ident(pkg: str, version: str, arch: str) -> bool:
    return bool(
        isinstance(pkg, str) and isinstance(version, str) and isinstance(arch, str)
        and _SAFE_PKG.match(pkg) and _SAFE_VER.match(version) and _SAFE_ARCH.match(arch)
    )

def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

_normalize_sha256 = _common.normalize_sha256

def _valid_index(data) -> bool:
    if not isinstance(data, dict):
        return False
    pkgs = data.get("packages")
    if not isinstance(pkgs, list):
        return False
    return all(isinstance(p, dict) and _SAFE_PKG.match(str(p.get("package", ""))) for p in pkgs)

def _load_cached_index() -> Optional[list]:
    try:
        with open(INDEX_CACHE) as f:
            data = json.load(f)
    except (OSError, ValueError):
        return None
    if _valid_index(data):
        return data["packages"]
    return None

def get_arch() -> str:
    raw = os.uname().machine
    return {
        "aarch64": "aarch64",
        "armv7l":  "arm",
        "armv8l":  "arm",
        "x86_64":  "x86_64",
        "i686":    "i686",
    }.get(raw, raw)

def _ping_mirror(mirror: dict, timeout: int = 4) -> Optional[float]:
    url = f"{mirror['base_url']}/dists/termux/Release"
    try:
        start = time.time()
        req = urllib.request.Request(url, method="HEAD",
                                     headers={"User-Agent": "termux-app-store"})
        with urllib.request.urlopen(req, timeout=timeout):
            return (time.time() - start) * 1000
    except Exception:
        return None

def get_best_mirror(force: bool = False) -> dict:
    if not force and MIRROR_CACHE.exists():
        try:
            age = time.time() - MIRROR_CACHE.stat().st_mtime
            if age < MIRROR_TTL:
                with open(MIRROR_CACHE) as f:
                    return json.load(f)
        except Exception:
            pass

    results = []
    lock = threading.Lock()

    def probe(m):
        latency = _ping_mirror(m)
        with lock:
            results.append({**m, "latency": latency, "online": latency is not None})

    threads = [threading.Thread(target=probe, args=(m,)) for m in MIRRORS]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=6)

    online = [r for r in results if r["online"]]
    online.sort(key=lambda x: x["latency"])

    best = online[0] if online else MIRRORS[0]

    try:
        with open(MIRROR_CACHE, "w") as f:
            json.dump(best, f)
    except Exception:
        pass

    return best

def get_index(log_fn: Optional[Callable] = None) -> list:
    def _log(msg):
        if log_fn:
            log_fn(msg)

    if INDEX_CACHE.exists():
        age = time.time() - INDEX_CACHE.stat().st_mtime
        if age < INDEX_TTL:
            cached_index = _load_cached_index()
            if cached_index is not None:
                return cached_index

    for url in INDEX_URLS:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "termux-app-store"})
            with urllib.request.urlopen(req, timeout=8) as resp:
                data = json.loads(resp.read())
            if not _valid_index(data):
                _log(f"Rejected malformed index from {url}")
                continue
            tmp_cache = INDEX_CACHE.with_suffix(".tmp")
            with open(tmp_cache, "w") as f:
                json.dump(data, f)
            os.replace(tmp_cache, INDEX_CACHE)
            return data["packages"]
        except Exception:
            continue

    stale_index = _load_cached_index()
    if stale_index is not None:
        return stale_index

    return []

def get_pkg_info(pkg_name: str, index: Optional[list] = None) -> Optional[dict]:
    pkgs = index if index is not None else get_index()
    for p in pkgs:
        if p.get("package") == pkg_name:
            return p
    return None

def _deb_cache_path(pkg: str, version: str, arch: str) -> Path:
    return DEB_CACHE_DIR / f"{pkg}_{version}_{arch}.deb"

def get_cached_deb(pkg: str, version: str, arch: str,
                   sha256: Optional[str] = None) -> Optional[Path]:
    expected = _normalize_sha256(sha256)
    if not expected or not _valid_ident(pkg, version, arch):
        return None

    path = _deb_cache_path(pkg, version, arch)
    if not path.is_file() or path.is_symlink():
        return None

    age = time.time() - path.stat().st_mtime
    if age > DEB_TTL:
        path.unlink(missing_ok=True)
        return None

    if _sha256_file(path) != expected:
        path.unlink(missing_ok=True)
        return None

    return path

def save_deb_cache(src: Path, pkg: str, version: str, arch: str) -> Path:
    dest = _deb_cache_path(pkg, version, arch)
    tmp = dest.with_suffix(".part")
    shutil.copy2(src, tmp)
    os.replace(tmp, dest)
    return dest

def fetch_published_sha256(pkg: str, version: str, arch: str,
                           log_fn: Optional[Callable] = None) -> str:
    if not _valid_ident(pkg, version, arch):
        return ""
    url = SHA256_SIDECAR_URL.format(pkg=pkg, version=version, arch=arch)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "termux-app-store"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            line = resp.read(4096).decode("utf-8", errors="ignore").strip()
    except Exception as e:
        if log_fn:
            log_fn(f"Could not fetch published checksum: {e}")
        return ""
    token = line.split()[0] if line else ""
    return _normalize_sha256(token)

def download_deb(pkg: str, version: str, arch: str,
                 dest: Path,
                 log_fn: Optional[Callable] = None,
                 progress_fn: Optional[Callable] = None,
                 eta_fn: Optional[Callable] = None) -> bool:
    def _log(msg):
        if log_fn:
            log_fn(msg)

    def _progress(pct):
        if progress_fn:
            progress_fn(pct)

    def _eta(seconds):
        if eta_fn:
            eta_fn(seconds)

    if not _valid_ident(pkg, version, arch):
        _log("Invalid package name, version or architecture")
        return False

    mirror = get_best_mirror()
    deb_path = DEB_PATH_PATTERN.format(pkg=pkg, version=version, arch=arch)

    urls = [f"{mirror['base_url']}/{deb_path}"]
    for m in MIRRORS:
        if m["base_url"] != mirror["base_url"]:
            urls.append(f"{m['base_url']}/{deb_path}")

    _log(f"Mirror: {mirror['name']}")
    _log(f"Downloading {pkg}_{version}_{arch}.deb...")
    _progress(5)

    tmp = dest.with_suffix(".tmp")

    for url in urls:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "termux-app-store"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                total = int(resp.headers.get("Content-Length", 0))
                downloaded = 0
                dl_start = time.time()

                if total > 0:
                    _eta(total / (200 * 1024))

                with open(tmp, "wb") as f:
                    while True:
                        chunk = resp.read(65536)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total > 0:
                            pct = 5 + int(downloaded * 75 / total)
                            _progress(pct)
                            elapsed = time.time() - dl_start
                            if elapsed > 0.5 and downloaded > 0:
                                speed = downloaded / elapsed
                                remaining_bytes = total - downloaded
                                install_est = total / (500 * 1024)
                                _eta(remaining_bytes / speed + install_est)

            tmp.rename(dest)
            size_kb = dest.stat().st_size // 1024
            _log(f"Downloaded {size_kb}KB")
            _progress(80)
            file_size = dest.stat().st_size
            _eta(file_size / (500 * 1024))
            return True

        except urllib.error.HTTPError as e:
            if e.code == 404:
                continue
            _log(f"HTTP {e.code} from {url}")
            continue
        except Exception as e:
            _log(f"Download error: {e}")
            continue
        finally:
            if tmp.exists():
                tmp.unlink(missing_ok=True)

    return False

def install_deb(deb_path: Path,
                log_fn: Optional[Callable] = None,
                progress_fn: Optional[Callable] = None) -> bool:
    def _log(msg):
        if log_fn:
            log_fn(msg)

    def _progress(pct):
        if progress_fn:
            progress_fn(pct)

    _log("Installing with dpkg...")
    _progress(85)

    try:
        proc = subprocess.Popen(
            ["dpkg", "-i", str(deb_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        for line in iter(proc.stdout.readline, b""):
            clean = line.decode(errors="ignore").rstrip()
            if clean:
                _log(clean)
        proc.wait()

        if proc.returncode == 0:
            _progress(100)
            return True
        else:
            _log("Fixing dependencies...")
            fix = subprocess.run(
                ["apt-get", "install", "-f", "-y"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            if fix.returncode != 0:
                return False
            retry = subprocess.run(
                ["dpkg", "-i", str(deb_path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            if retry.returncode == 0:
                _progress(100)
                return True
            return False

    except FileNotFoundError:
        _log("dpkg not found, trying apt...")
        result = subprocess.run(
            ["apt", "install", "-y", str(deb_path)],
            capture_output=True,
        )
        return result.returncode == 0

def fast_install(pkg_name: str,
                 log_fn:      Optional[Callable] = None,
                 progress_fn: Optional[Callable] = None,
                 eta_fn:      Optional[Callable] = None) -> bool:

    _current_pct = [0]

    def _log(msg):
        if log_fn:
            log_fn(msg)

    def _progress(pct):
        pct = int(pct)
        if pct >= _current_pct[0]:
            _current_pct[0] = pct
            if progress_fn:
                progress_fn(pct)

    def _eta(seconds):
        if eta_fn:
            eta_fn(seconds)

    arch = get_arch()
    start_time = time.time()

    _log(f"► Fast Install: {pkg_name}")
    _log(f"  Architecture: {arch}")
    _progress(5)

    _log("Fetching package info...")
    pkg_info = get_pkg_info(pkg_name)

    if not pkg_info:
        _log(f"✗ Package '{pkg_name}' not found in index")
        return False

    version = str(pkg_info.get("version", ""))

    if not _valid_ident(pkg_name, version, arch):
        _log("✗ Invalid package name, version or architecture in index")
        return False

    sha256_by_arch = pkg_info.get("sha256_by_arch")
    deb_sha256 = ""
    if isinstance(sha256_by_arch, dict):
        deb_sha256 = _normalize_sha256(sha256_by_arch.get(arch, ""))
    if not deb_sha256:
        _log("  Checksum not in index — fetching published checksum...")
        deb_sha256 = fetch_published_sha256(pkg_name, version, arch, log_fn=log_fn)

    _log(f"  Version: {version}")
    _progress(8)

    if not deb_sha256:
        _log("✗ No trusted SHA256 available for this package/arch")
        _log("  Refusing to install an unverified binary")
        _log("")
        _log("Falling back to build from source...")
        _log("(This will take longer)")
        _log("")
        return _fallback_build_from_source(pkg_name, log_fn=log_fn, progress_fn=_progress)

    _log("Checking local cache...")
    cached = get_cached_deb(pkg_name, version, arch, sha256=deb_sha256)

    if cached:
        elapsed = time.time() - start_time
        _log(f"✓ Cache HIT (checksum verified) — {cached.name} ({elapsed:.1f}s)")
        _progress(80)
        _eta(cached.stat().st_size / (500 * 1024))

        ok = install_deb(cached, log_fn=log_fn, progress_fn=_progress)
        if ok:
            elapsed = time.time() - start_time
            _log(f"✔ Installed from cache in {elapsed:.1f}s!")
        else:
            _log("✗ Cached .deb could not be installed — removing from cache")
            cached.unlink(missing_ok=True)
            _log(f"  → Run: tas --fix-install {pkg_name}  (force rebuild from source)")
        return ok

    _log("  Cache miss — will download")
    _progress(10)

    with tempfile.TemporaryDirectory() as tmp_dir:
        deb_dest = Path(tmp_dir) / f"{pkg_name}_{version}_{arch}.deb"

        downloaded = download_deb(
            pkg=pkg_name,
            version=version,
            arch=arch,
            dest=deb_dest,
            log_fn=log_fn,
            progress_fn=_progress,
            eta_fn=eta_fn,
        )

        if downloaded:
            _log("Verifying checksum...")
            actual = _sha256_file(deb_dest)
            if actual != deb_sha256:
                _log("✗ SHA256 mismatch — file corrupt or tampered")
                _log(f"  Expected: {deb_sha256[:32]}...")
                _log(f"  Got:      {actual[:32]}...")
            else:
                _log("✓ Checksum OK")
                save_deb_cache(deb_dest, pkg_name, version, arch)
                ok = install_deb(deb_dest, log_fn=log_fn, progress_fn=_progress)
                if ok:
                    elapsed = time.time() - start_time
                    _log(f"✔ Installed in {elapsed:.1f}s!")
                    return True
                _log("✗ dpkg install failed")
                return False

    _log("")
    _log("Verified pre-built .deb not available for this package/arch")
    _log("Falling back to build from source...")
    _log("(This will take longer)")
    _log("")
    return _fallback_build_from_source(pkg_name, log_fn=log_fn, progress_fn=_progress)

def _fallback_build_from_source(pkg_name: str,
                                  log_fn:      Optional[Callable] = None,
                                  progress_fn: Optional[Callable] = None) -> bool:
    def _log(msg):
        if log_fn:
            log_fn(msg)
    def _progress(pct):
        if progress_fn:
            progress_fn(pct)

    if not _SAFE_PKG.match(pkg_name or ""):
        _log("✗ Invalid package name")
        return False

    app_root = _get_app_root()
    build_sh = app_root / "build-package.sh"

    if not build_sh.exists():
        packaged = _packaged_build_script()
        if packaged is not None:
            _log("Using the build-package.sh shipped with this installation")
            tmp_copy = build_sh.with_suffix(".part")
            shutil.copy2(packaged, tmp_copy)
            tmp_copy.chmod(0o755)
            os.replace(tmp_copy, build_sh)

    if not build_sh.exists():
        _log("Downloading build-package.sh...")
        url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/master/build-package.sh"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "termux-app-store"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                downloaded_bytes = resp.read()
        except Exception as e:
            _log(f"✗ Failed to download build-package.sh: {e}")
            return False

        expected_sha256 = os.environ.get("TERMUX_APP_STORE_BUILD_SH_SHA256", "").strip().lower()
        allow_unverified = os.environ.get("TERMUX_APP_STORE_ALLOW_UNVERIFIED_BUILD_SH") == "1"
        actual_sha256 = hashlib.sha256(downloaded_bytes).hexdigest()
        if expected_sha256:
            if actual_sha256 != expected_sha256:
                _log("✗ build-package.sh SHA256 mismatch — refusing to run it")
                _log(f"  Expected: {expected_sha256}")
                _log(f"  Got:      {actual_sha256}")
                return False
        elif allow_unverified:
            _log("⚠ Running build-package.sh WITHOUT checksum pinning (explicitly allowed)")
            _log(f"  Downloaded SHA256: {actual_sha256}")
        else:
            _log("✗ Refusing to run a downloaded build-package.sh without a pinned checksum")
            _log(f"  Downloaded SHA256: {actual_sha256}")
            _log("  Review the script, then set TERMUX_APP_STORE_BUILD_SH_SHA256 to this value")
            _log("  or clone the repository so a local build-package.sh is used")
            return False

        syntax_check = subprocess.run(
            ["bash", "-n"], input=downloaded_bytes, capture_output=True
        )
        if syntax_check.returncode != 0:
            _log("✗ build-package.sh failed bash syntax check — refusing to run it")
            _log(syntax_check.stderr.decode(errors="ignore"))
            return False

        tmp_build = build_sh.with_suffix(".part")
        tmp_build.write_bytes(downloaded_bytes)
        tmp_build.chmod(0o755)
        os.replace(tmp_build, build_sh)

    if not _ensure_recipe(pkg_name, app_root, _log):
        return False

    proc = subprocess.Popen(
        ["bash", str(build_sh), pkg_name],
        cwd=str(app_root),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    ANSI = re.compile(r'\x1b\[[0-9;]*[mGKHf]')

    for line in iter(proc.stdout.readline, b""):
        clean = ANSI.sub("", line.decode(errors="ignore").rstrip())
        if clean:
            _log(clean)

    proc.wait()
    _progress(100 if proc.returncode == 0 else 0)
    return proc.returncode == 0

def _packaged_build_script() -> Optional[Path]:
    return _common.packaged_build_script()

def _ensure_recipe(pkg_name: str, app_root: Path, _log: Callable) -> bool:
    if (app_root / "packages" / pkg_name / "build.sh").is_file():
        return True

    info = get_pkg_info(pkg_name) or {}
    expected = _normalize_sha256(info.get("recipe_sha256"))

    def adapter(kind: str, message: str) -> None:
        _log(f"✗ {message}" if kind == "error" else message)

    return _common.download_recipe(app_root / "packages", pkg_name, expected, False, adapter)

def _get_app_root() -> Path:
    env = os.environ.get("TERMUX_APP_STORE_HOME")
    if env:
        return Path(env).expanduser().resolve()
    return Path(__file__).resolve().parent.parent

def check_mirrors(log_fn: Optional[Callable] = None) -> list:
    def _log(msg):
        if log_fn:
            log_fn(msg)

    results = []
    lock = threading.Lock()

    def probe(m):
        latency = _ping_mirror(m)
        with lock:
            results.append({**m, "latency": latency, "online": latency is not None})
        status = f"✓ {m['name']}: {latency:.0f}ms" if latency else f"✗ {m['name']}: unreachable"
        _log(status)

    threads = [threading.Thread(target=probe, args=(m,)) for m in MIRRORS]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=8)

    results.sort(key=lambda x: (not x["online"], x["latency"] or 9999))
    return results

def clear_deb_cache(log_fn: Optional[Callable] = None):
    def _log(msg):
        if log_fn:
            log_fn(msg)

    count = 0
    freed = 0
    for f in DEB_CACHE_DIR.glob("*.deb"):
        freed += f.stat().st_size
        f.unlink()
        count += 1

    _log(f"Cleared {count} cached .deb files ({freed // 1024}KB freed)")

def cache_info(log_fn: Optional[Callable] = None):
    def _log(msg):
        if log_fn:
            log_fn(msg)

    debs = list(DEB_CACHE_DIR.glob("*.deb"))
    total = sum(f.stat().st_size for f in debs)
    _log(f"Cached .deb files : {len(debs)}")
    _log(f"Cache size        : {total // 1024}KB")
    _log(f"Cache location    : {DEB_CACHE_DIR}")
    for deb in sorted(debs):
        age_h = int((time.time() - deb.stat().st_mtime) / 3600)
        _log(f"  • {deb.name} ({age_h}h ago)")

class FastInstaller:
    async def install(
        self,
        pkg_name: str,
        force_source: bool = False,
        log_fn: Optional[Callable] = None,
        progress_fn: Optional[Callable] = None,
    ) -> bool:
        import asyncio

        if force_source:
            return await asyncio.to_thread(
                _fallback_build_from_source, pkg_name,
                log_fn, progress_fn
            )
        return await asyncio.to_thread(
            fast_install, pkg_name, log_fn, progress_fn
        )


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Termux App Store - Fast Install Engine")
    parser.add_argument("--install",       metavar="PKG",  help="Install package")
    parser.add_argument("--check-mirrors", action="store_true")
    parser.add_argument("--cache-info",    action="store_true")
    parser.add_argument("--clear-cache",   action="store_true")
    args = parser.parse_args()

    if args.install:
        ok = fast_install(args.install, log_fn=print, progress_fn=lambda p: None)
        sys.exit(0 if ok else 1)
    elif args.check_mirrors:
        check_mirrors(log_fn=print)
    elif args.cache_info:
        cache_info(log_fn=print)
    elif args.clear_cache:
        clear_deb_cache(log_fn=print)
    else:
        parser.print_help()
