"""
termux-app-store

USAGE:
  termux-app-store                     Open TUI
  termux-app-store list  | -l | -L     List packages + status
  termux-app-store install | i | -i    Install a package
  termux-app-store uninstall           Uninstall a package
  termux-app-store show                Show package details
  termux-app-store update              Update core and checks update packages
  termux-app-store upgrade             Upgrade all outdated packages
  termux-app-store upgrade <pkg>       Upgrade a specific package
  termux-app-store version | -v        Show app version
  termux-app-store help | -h | --help  Show help
"""

# Open Contributor
# https://github.com/djunekz/termux-app-store

import subprocess
import sys
import os
import json
import re
import hashlib
import urllib.request
import urllib.error
import shutil
from pathlib import Path
from typing import Optional

try:
    from termux_app_store.fast_install import FastInstaller
    from termux_app_store.core.package import Package
    _BINARY_CACHE_AVAILABLE = True
except ImportError:
    _BINARY_CACHE_AVAILABLE = False

try:
    from termux_app_store.fast_install import fast_install, check_mirrors, cache_info, clear_deb_cache, MIRRORS
    _FAST_INSTALL_AVAILABLE = True
except ImportError:
    try:
        from fast_install import fast_install, check_mirrors, cache_info, clear_deb_cache, MIRRORS
        _FAST_INSTALL_AVAILABLE = True
    except ImportError:
        _FAST_INSTALL_AVAILABLE = False
        MIRRORS = [
            {"name": "GitHub Pages",  "base_url": "https://djunekz.github.io/termux-app-store"},
            {"name": "Cloudflare CDN","base_url": "https://termux-app-store.pages.dev"},
            {"name": "jsDelivr CDN",  "base_url": "https://cdn.jsdelivr.net/gh/djunekz/termux-app-store@gh-pages"},
            {"name": "Github Raw",    "base_url": "https://raw.githubusercontent.com/djunekz/termux-app-store/gh-pages"},
        ]

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
GITHUB_API_TAG     = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
INDEX_URL          = f"https://raw.githubusercontent.com/{GITHUB_REPO}/master/tools/index.json"

_SELF_FILES = {
    "termux_app_store_cli.py": f"https://raw.githubusercontent.com/{GITHUB_REPO}/master/termux_app_store/termux_app_store_cli.py",
    "termux_app_store.py":     f"https://raw.githubusercontent.com/{GITHUB_REPO}/master/termux_app_store/termux_app_store.py",
}

_INSTALL_DIR = Path(os.environ.get("PREFIX", "/data/data/com.termux/files/usr")) / "lib" / ".tas"


def _is_pip_mode() -> bool:
    try:
        import importlib.util
        spec = importlib.util.find_spec("termux_app_store")
        if spec and spec.origin:
            return "site-packages" in str(spec.origin)
    except Exception:
        pass
    return False


R       = "\033[0m"
B       = "\033[1m"
RED     = "\033[31m"
GREEN   = "\033[32m"
YELLOW  = "\033[33m"
CYAN    = "\033[36m"
MAGENTA = "\033[35m"
DIM     = "\033[2m"


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
        CACHE_FILE.write_text(json.dumps({"app_root": str(path)}, indent=2))
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



def _verify_downloaded_script(raw: bytes, env_sha256_var: str) -> bool:
    if not raw:
        return False

    expected_sha256 = os.environ.get(env_sha256_var, "")
    if expected_sha256:
        actual_sha256 = hashlib.sha256(raw).hexdigest()
        if actual_sha256 != expected_sha256:
            return False

    syntax_check = subprocess.run(
        ["bash", "-n"], input=raw, capture_output=True
    )
    return syntax_check.returncode == 0


def ensure_build_package_sh(app_root: Path) -> bool:
    build_pkg = app_root / "build-package.sh"
    if build_pkg.exists():
        return True
    url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/master/build-package.sh"
    try:
        print(f"  {DIM}Downloading build-package.sh...{R}")
        req = urllib.request.Request(url, headers={"User-Agent": "termux-app-store-cli"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read()
            if raw and _verify_downloaded_script(raw, "TERMUX_APP_STORE_BUILD_SH_SHA256"):
                build_pkg.write_bytes(raw)
                build_pkg.chmod(0o755)
                print(f"  {GREEN}✔  build-package.sh ready.{R}")
                return True
            elif raw:
                print(f"  {RED}✗  build-package.sh failed verification — refusing to use it{R}")
    except Exception as e:
        print(f"  {RED}✗  Failed to download build-package.sh: {e}{R}")
    return False


def fetch_index() -> list:
    try:
        req = urllib.request.Request(
            INDEX_URL,
            headers={"User-Agent": "termux-app-store-cli"},
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


fetch_index_from_github = fetch_index


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
            "homepage": "-",
            "license": "-",
        }
        with build.open(errors="ignore") as f:
            for line in f:
                for key, field in [
                    ("TERMUX_PKG_DESCRIPTION=", "description"),
                    ("TERMUX_PKG_VERSION=",     "version"),
                    ("TERMUX_PKG_MAINTAINER=",  "maintainer"),
                    ("TERMUX_PKG_HOMEPAGE=",    "homepage"),
                    ("TERMUX_PKG_LICENSE=",     "license"),
                ]:
                    if line.startswith(key):
                        data[field] = line.split("=", 1)[1].strip().strip('"')
                if line.startswith("TERMUX_PKG_DEPENDS="):
                    deps_str = line.split("=", 1)[1].strip().strip('"')
                    data["depends"] = [d.strip() for d in deps_str.split(",") if d.strip()]
        pkgs.append(data)
    return pkgs


def normalize_pkg(raw: dict) -> dict:
    deps = raw.get("depends", raw.get("deps", "-"))
    if isinstance(deps, list):
        deps = ",".join(deps) if deps else "-"
    elif not deps:
        deps = "-"
    result = {
        "name":       raw.get("package", raw.get("name", "?")),
        "desc":       raw.get("description", raw.get("desc", "-")),
        "version":    raw.get("version", "?"),
        "deps":       deps,
        "maintainer": raw.get("maintainer", "-"),
        "homepage":   raw.get("homepage", "-"),
        "license":    raw.get("license", "-"),
    }
    if "sha256" in raw:
        result["sha256"] = raw["sha256"]
    if "sha256_by_arch" in raw:
        result["sha256_by_arch"] = raw["sha256_by_arch"]
    return result


def get_packages(packages_dir: Path, online: bool = True) -> list:
    if online:
        raw = fetch_index()
        if raw:
            return [normalize_pkg(p) for p in raw]

    cached = load_index_cache()
    if cached:
        return [normalize_pkg(p) for p in cached]

    raw = load_packages_from_local(packages_dir)
    return [normalize_pkg(p) for p in raw]


def get_installed_version(name: str):
    try:
        out = subprocess.check_output(
            ["dpkg-query", "-W", "-f=${Status}\t${Version}\n", name],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        if not out:
            return None
        for line in out.splitlines():
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) < 2:
                continue
            status_part = parts[0].strip()
            version_part = parts[1].strip()
            if "ok installed" in status_part and version_part:
                return version_part
    except Exception:
        pass
    return None


def get_status(name: str, store_version: str):
    installed = get_installed_version(name)
    if installed is None:
        return "NOT INSTALLED", f"{RED}✗ not installed{R}"
    if is_installed_newer_or_equal(installed, store_version):
        return "INSTALLED", f"{GREEN}✔ up-to-date{R}       {DIM}{installed}{R}"
    else:
        return "UPDATE", (
            f"{YELLOW}↑ update available{R}  "
            f"{DIM}{installed}{R} → {GREEN}{store_version}{R}"
        )


def fetch_latest_tag():
    try:
        req = urllib.request.Request(
            GITHUB_API_TAG,
            headers={"User-Agent": "termux-app-store-cli"},
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            return data.get("tag_name", "unknown")
    except Exception:
        return None


def hold_package(name: str):
    try:
        subprocess.call(
            ["apt-mark", "hold", name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        pass


def unhold_package(name: str):
    try:
        subprocess.call(
            ["apt-mark", "unhold", name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        pass


_PKG_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._+-]*$")

def is_safe_pkg_name(name: str) -> bool:
    return bool(name) and bool(_PKG_NAME_RE.match(name)) and ".." not in name


def cleanup_package_files(name: str) -> int:
    if not is_safe_pkg_name(name):
        return 0

    prefix = os.environ.get("PREFIX", "/data/data/com.termux/files/usr")
    cleanup_paths = [
        Path(prefix) / "lib" / name,
        Path(prefix) / "share" / "doc" / name,
        Path(prefix) / "share" / name,
    ]
    removed_count = 0
    for path in cleanup_paths:
        if path.exists():
            try:
                shutil.rmtree(path)
                removed_count += 1
                print(f"{DIM}  ✓ Removed: {path}{R}")
            except Exception as e:
                print(f"{YELLOW}  ! Could not remove {path}: {e}{R}")
    return removed_count


def cmd_list(packages_dir: Path):
    print(f"\n  {DIM}Fetching package index...{R}")
    pkgs = load_all_packages(packages_dir)
    if not pkgs:
        print(f"\n  {YELLOW}  No packages found.{R}\n")
        return

    W = 24
    print(f"\n  {B}{CYAN}{'PACKAGE':<{W}} {'VERSION':<12} STATUS{R}")
    print(f"  {DIM}{'─'*62}{R}")

    for p in pkgs:
        _, label = get_status(p["name"], p["version"])
        print(f"  {B}{p['name']:<{W}}{R} {CYAN}{p['version']:<12}{R} {label}")

    print(f"\n  {DIM}{'─'*62}{R}")
    print(f"  {DIM}{len(pkgs)} package(s) total{R}\n")

def cmd_show(packages_dir: Path, name: str):
    pkgs = load_all_packages(packages_dir)
    p = next((x for x in pkgs if x["name"] == name), None)

    if not p:
        print(f"\n  {RED}✗  Package '{name}' not found.{R}\n  {DIM}Run: {CYAN}termux-app-store list{R}")
        sys.exit(1)

    _, label = get_status(p["name"], p["version"])
    deps = p.get("deps", "-")
    if isinstance(deps, list):
        deps_str = ", ".join(deps) if deps else "-"
    else:
        deps_str = deps if deps and deps != "-" else "-"

    W = 46
    print(f"\n  {B}{CYAN}{'━'*W}{R}")
    print(f"  {B}  {p['name']}{R}")
    print(f"  {DIM}  {label}{R}")
    print(f"  {B}{CYAN}{'━'*W}{R}\n")
    print(f"  {B}Description{R}   {p['desc']}")
    print(f"  {B}Version    {R}   {CYAN}{p['version']}{R}")
    print(f"  {B}Maintainer {R}   {p['maintainer']}")
    print(f"  {B}License    {R}   {p.get('license', '-')}")
    print(f"  {B}Homepage   {R}   {DIM}{p.get('homepage', '-')}{R}")
    print(f"  {B}Depends    {R}   {YELLOW}{deps_str}{R}")
    print(f"\n  {B}{CYAN}{'━'*W}{R}\n")


def ensure_package_files(packages_dir: Path, name: str, force_update: bool = False) -> bool:
    if not is_safe_pkg_name(name):
        return False

    pkg_dir = packages_dir / name
    build_sh = pkg_dir / "build.sh"

    if build_sh.exists() and not force_update:
        return True

    url = (
        f"https://raw.githubusercontent.com/{GITHUB_REPO}/master/packages/{name}/build.sh"
    )
    try:
        pkg_dir.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(url, headers={"User-Agent": "termux-app-store-cli"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read()
            if raw:
                syntax_check = subprocess.run(
                    ["bash", "-n"], input=raw, capture_output=True
                )
                if syntax_check.returncode != 0:
                    return False
                build_sh.write_bytes(raw)
                return True
    except Exception:
        pass
    return False


def _get_arch() -> str:
    try:
        out = subprocess.check_output(["uname", "-m"], text=True).strip()
        mapping = {"aarch64": "aarch64", "armv7l": "arm", "armv8l": "arm",
                   "x86_64": "x86_64", "i686": "i686", "i386": "i686"}
        return mapping.get(out, out)
    except Exception:
        return "aarch64"


def _direct_deb_install(name: str, version: str, pkg_info: Optional[dict] = None, log_fn=None) -> bool:
    def _log(msg):
        if log_fn:
            log_fn(msg)
        else:
            print(f"  {msg}")

    arch = _get_arch()
    fname = f"{name}_{version}_{arch}.deb"

    expected_sha = None
    if pkg_info:
        sha_by_arch = pkg_info.get("sha256_by_arch", {})
        expected_sha = sha_by_arch.get(arch)

    import tempfile
    _log(f"  Trying direct .deb download: {fname}")

    for mirror in MIRRORS:
        url = f"{mirror['base_url']}/pool/main/{fname}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "termux-app-store-cli"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                deb_bytes = resp.read()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                continue
            _log(f"  ✗ HTTP {e.code} from {mirror['name']}")
            continue
        except Exception as e:
            _log(f"  ✗ Error: {e}")
            continue

        if not deb_bytes:
            continue

        actual_sha = hashlib.sha256(deb_bytes).hexdigest()
        if expected_sha and actual_sha != expected_sha:
            _log(f"  ✗ SHA256 mismatch from {mirror['name']} — skipping (file corrupt/outdated)")
            _log(f"    Expected: {expected_sha[:32]}...")
            _log(f"    Got:      {actual_sha[:32]}...")
            continue

        with tempfile.NamedTemporaryFile(suffix=".deb", delete=False) as tmp:
            tmp.write(deb_bytes)
            tmp_path = tmp.name

        try:
            ret = subprocess.call(["dpkg", "-i", tmp_path],
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if ret == 0:
                _log(f"  ✔ Installed via dpkg: {fname}")
                return True
            else:
                _log(f"  ✗ dpkg -i failed (exit {ret})")
                return False
        except Exception as e:
            _log(f"  ✗ dpkg error: {e}")
            return False
        finally:
            try:
                os.unlink(tmp_path)
            except Exception:
                pass

    _log(f"  ✗ Not available in any mirror")
    return False


def cmd_install(app_root: Path, packages_dir: Path, name: str, silent: bool = False, force_update: bool = False, force_source: bool = False) -> bool:
    pkgs = load_all_packages(packages_dir)
    p = next((x for x in pkgs if x["name"] == name), None)

    if not p:
        print(f"\n  {RED}✗  Package '{name}' not found.{R}\n  {DIM}Run: {CYAN}termux-app-store list{R}")
        return False

    status, _ = get_status(name, p["version"])

    if status == "INSTALLED" and not silent:
        print(f"  {GREEN}✔  '{name}' is already up-to-date  {DIM}v{p['version']}{R}")
        return True

    print(f"\n  {DIM}{'─'*46}{R}")
    print(f"  {B}  Installing {CYAN}{name}{R}{B}  {DIM}v{p['version']}{R}")
    print(f"  {DIM}{'─'*46}{R}\n")

    success = False

    if _BINARY_CACHE_AVAILABLE and not force_source:
        print(f"  {DIM}Trying Binary Cache + Fast Install...{R}")
        try:
            installer = FastInstaller()
            import asyncio
            success = asyncio.run(installer.install(name, force_source=force_source))
        except Exception as e:
            print(f"  {YELLOW}Binary cache failed: {e}{R}")

    if not success and _FAST_INSTALL_AVAILABLE:
        _last_pct = [0]

        def _log(msg):
            print(f"  {msg}")

        def _progress(pct):
            if pct != _last_pct[0]:
                bar = "█" * (pct // 5) + "░" * (20 - pct // 5)
                print(f"\r  [{bar}] {pct}%", end="", flush=True)
                if pct >= 100:
                    print()
                _last_pct[0] = pct

        success = fast_install(
            pkg_name=name,
            log_fn=_log,
            progress_fn=_progress,
        )

        if not success:
            print(f"  {DIM}Fast install failed — trying direct .deb from pool...{R}")
            success = _direct_deb_install(name, p["version"], pkg_info=p)

        if not success:
                if not ensure_package_files(packages_dir, name, force_update):
                    print(f"{RED}[✗] Failed to prepare package files.{R}")
                    return False

                if not ensure_build_package_sh(app_root):
                    return False

                proc = subprocess.Popen(
                    ["bash", "build-package.sh", name],
                    cwd=str(app_root),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                )
                for line in iter(proc.stdout.readline, b""):
                    print(" ", line.decode(errors="ignore").rstrip())
                proc.wait()
                success = proc.returncode == 0
        if success:
            hold_package(name)
            print(f"\n  {GREEN}{B}✔  '{name}' installed successfully!{R}\n")
            return True
        else:
            print(f"\n  {RED}✗  Installation failed.{R}")
            print(f"  {DIM}The downloaded .deb may be corrupt or unavailable for your architecture.{R}")
            print(f"  {YELLOW}↳ Try:{R} {B}{CYAN}tas --fix-install {name}{DIM} or{R}{B}{CYAN} termux-app-store fix-install {name}{R}")
            print(f"  {DIM}  (Forces a clean rebuild from source, bypassing cache){R}\n")
            return False

    else:
        print(f"  {DIM}Fast install unavailable — trying direct .deb from pool...{R}")
        success = _direct_deb_install(name, p["version"], pkg_info=p)

    if not success:
        print(f"  {DIM}Pre-built .deb not available — building from source...{R}\n")

        if not ensure_package_files(packages_dir, name, force_update=force_update):
            print(f"{RED}[✗] Failed to download build files for '{name}'.{R}")
            print(f"    Check your internet connection or try again later.")
            return False

        if not ensure_build_package_sh(app_root):
            print(f"{RED}[✗] Cannot proceed without build-package.sh.{R}")
            return False

        proc = subprocess.Popen(
            ["bash", "build-package.sh", name],
            cwd=str(app_root),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        for line in iter(proc.stdout.readline, b""):
            print(" ", line.decode(errors="ignore").rstrip())
        proc.wait()
        success = proc.returncode == 0

    if success:
        hold_package(name)
        print(f"\n  {GREEN}{B}✔  '{name}' installed successfully!{R}\n")
        return True
    else:
        print(f"\n  {RED}✗  Install failed{R}")
        print(f"  {DIM}The .deb package may be corrupt or your architecture is unsupported.{R}")
        print(f"  {YELLOW}↳ Try:{R} {B}{CYAN}tas fix-install {name}{R}")
        print(f"  {DIM}  (Forces a clean rebuild from source, bypassing cache){R}\n")
        return False


def cmd_uninstall(name: str):
    if not is_safe_pkg_name(name):
        print(f"{RED}[✗] Invalid package name: '{name}'{R}")
        return

    installed = get_installed_version(name)
    if installed is None:
        print(f"{YELLOW}[!] '{name}' is not installed.{R}")
        return

    print(f"\n  {DIM}{'─'*46}{R}")
    print(f"  {B}  Uninstalling {CYAN}{name}{R}")
    print(f"  {DIM}{'─'*46}{R}\n")

    prefix = os.environ.get("PREFIX", "/data/data/com.termux/files/usr")
    cleanup_paths = [
        Path(prefix) / "lib" / name,
        Path(prefix) / "share" / "doc" / name,
        Path(prefix) / "share" / name,
    ]

    print(f"  {DIM}Cleaning cache files...{R}")
    for base_path in cleanup_paths:
        if base_path.exists():
            for root, dirs, files in os.walk(base_path, topdown=False):
                if '__pycache__' in dirs:
                    pycache_path = Path(root) / '__pycache__'
                    try:
                        shutil.rmtree(pycache_path)
                        print(f"{DIM}  ✓ Removed: {pycache_path}{R}")
                    except Exception:
                        pass
                for file in files:
                    if file.endswith('.pyc') or file.endswith('.pyo'):
                        file_path = Path(root) / file
                        try:
                            file_path.unlink()
                        except Exception:
                            pass

    unhold_package(name)

    ret = subprocess.call(["apt", "remove", "-y", name])

    if ret == 0:
        print(f"\n{DIM}[*] Final cleanup...{R}")
        removed_count = cleanup_package_files(name)
        if removed_count > 0:
            print(f"{GREEN}[✔] Cleaned up {removed_count} leftover director{'y' if removed_count == 1 else 'ies'}.{R}")
        print(f"\n  {GREEN}{B}✔  '{name}' uninstalled successfully!{R}\n")
    else:
        hold_package(name)
        print(f"\n{RED}[✗] Uninstall failed.{R}\n")
        sys.exit(ret)


def cmd_update(packages_dir: Path):
    print(f"\n{DIM}[*] Checking for app file index updates...{R}")

    print(f"  {DIM}Checking core files...{R}")
    cmd_self_update(silent=False)

    raw = fetch_index()
    if raw:
        print(f"  {GREEN}✔  Index updated  {DIM}({len(raw)} packages){R}\n")
        pkgs = [normalize_pkg(p) for p in raw]

        if packages_dir.exists():
            import shutil as _shutil
            index_names = {p.get("package", p.get("name", "")) for p in raw}
            removed_local = []
            for pkg_dir in sorted(packages_dir.iterdir()):
                if pkg_dir.is_dir() and pkg_dir.name not in index_names:
                    try:
                        _shutil.rmtree(pkg_dir)
                        removed_local.append(pkg_dir.name)
                    except Exception:
                        pass
            if removed_local:
                print(f"{DIM}[*] Removed {len(removed_local)} obsolete local package(s): {', '.join(removed_local)}{R}\n")
    else:
        print(f"  {YELLOW}  Offline — using cached index.{R}\n")
        pkgs = get_packages(packages_dir, online=False)

    if not pkgs:
        print(f"\n  {YELLOW}  No packages found.{R}\n")
        return

    outdated = []
    installed_count = 0

    for p in pkgs:
        status, _ = get_status(p["name"], p["version"])
        if status == "NOT INSTALLED":
            continue
        installed_count += 1
        if status == "UPDATE":
            inst = get_installed_version(p["name"])
            outdated.append((p["name"], inst, p["version"]))

    print(f"\n  {B}{CYAN}{'PACKAGE':<24} {'INSTALLED':<14} LATEST{R}")
    print(f"  {DIM}{'─'*60}{R}")

    if not outdated:
        print(f"  {GREEN}✔  All {installed_count} installed package(s) are up-to-date!{R}")
    else:
        for name, inst, latest in outdated:
            print(
                f"  {B}{name:<24}{R} "
                f"{DIM}{inst:<14}{R} "
                f"{GREEN}{latest:<12}{R}  {YELLOW}↑{R}"
            )
        print(
            f"\n  {YELLOW}{len(outdated)} update(s) available.{R}  "
            f"{DIM}Run: {CYAN}termux-app-store upgrade{R}"
        )

    print(f"\n  {DIM}Checked {installed_count} installed package(s){R}\n")


def cmd_upgrade(app_root: Path, packages_dir: Path, target=None):
    pkgs = load_all_packages(packages_dir)

    if target:
        p = next((x for x in pkgs if x["name"] == target), None)
        if not p:
            print(f"\n  {RED}✗  Package '{target}' not found.{R}")
            sys.exit(1)
        status, _ = get_status(target, p["version"])
        if status == "NOT INSTALLED":
            print(f"{YELLOW}[!] '{target}' is not installed.{R}")
            print(f"    Use {CYAN}termux-app-store install {target}{R} instead.")
            return
        if status == "INSTALLED":
            print(f"  {GREEN}✔  '{target}' is already up-to-date  {DIM}v{p['version']}{R}")
            return
        cmd_install(app_root, packages_dir, target, silent=True, force_update=True)
        return

    to_upgrade = []
    for p in pkgs:
        status, _ = get_status(p["name"], p["version"])
        if status == "UPDATE":
            to_upgrade.append(p)

    if not to_upgrade:
        print(f"\n  {GREEN}✔  All installed packages are up-to-date!{R}\n")
        return

    print(f"\n  {DIM}{'─'*46}{R}")
    print(f"  {B}{YELLOW}  {len(to_upgrade)} package(s) to upgrade{R}")
    print(f"  {DIM}{'─'*46}{R}\n")
    for p in to_upgrade:
        inst = get_installed_version(p["name"])
        print(f"  {CYAN}{p['name']:<24}{R} {DIM}{inst}{R} → {GREEN}{p['version']}{R}")
    print()

    ok = 0
    fail = 0
    for p in to_upgrade:
        success = cmd_install(app_root, packages_dir, p["name"], silent=True, force_update=True)
        if success:
            ok += 1
        else:
            fail += 1

    print(f"\n  {DIM}{'─'*46}{R}")
    print(f"  {B}  Upgrade summary{R}   {GREEN}{ok} succeeded{R}", end="")
    if fail:
        print(f"  {RED}{fail} failed{R}", end="")
    print(f"\n  {DIM}{'─'*46}{R}\n")


def _fetch_remote_content(url: str):
    import time
    sep = "&" if "?" in url else "?"
    bust_url = f"{url}{sep}_cb={int(time.time())}"
    try:
        req = urllib.request.Request(
            bust_url,
            headers={
                "User-Agent": "termux-app-store-cli",
                "Cache-Control": "no-cache, no-store",
                "Pragma": "no-cache",
            },
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
            return data if data else None
    except Exception:
        return None


def _files_differ(local_path: "Path", remote_bytes: bytes) -> bool:
    try:
        return local_path.read_bytes() != remote_bytes
    except Exception:
        return True


def cmd_self_update(silent: bool = False) -> bool:
    import shutil as _shutil

    if _is_pip_mode():
        if not silent:
            print(f"{DIM}[*] Pip mode detected — upgrading via pip...{R}")
        ret = subprocess.call(
            [sys.executable, "-m", "pip", "install", "--upgrade",
             "termux-app-store", "--break-system-packages"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        if ret == 0:
            try:
                import importlib.metadata
                new_ver = importlib.metadata.version("termux-app-store")
            except Exception:
                new_ver = None

            if new_ver:
                sentinel = _INSTALL_DIR / ".installed"
                if sentinel.exists():
                    try:
                        lines = sentinel.read_text().splitlines()
                        new_lines = []
                        for line in lines:
                            if line.startswith("version="):
                                new_lines.append(f"version={new_ver}")
                            elif line.startswith("mode="):
                                new_lines.append("mode=pip")
                            else:
                                new_lines.append(line)
                        sentinel.write_text("\n".join(new_lines) + "\n")
                    except Exception:
                        pass

                wrapper = Path(os.environ.get("PREFIX", "/data/data/com.termux/files/usr")) / "bin" / "termux-app-store"
                if wrapper.exists():
                    try:
                        content = wrapper.read_text()
                        import re as _re
                        content = _re.sub(
                            r'export TERMUX_APP_STORE_VERSION="[^"]*"',
                            f'export TERMUX_APP_STORE_VERSION="{new_ver}"',
                            content,
                        )
                        wrapper.write_text(content)
                    except Exception:
                        pass

            if not silent:
                ver_str = f" v{new_ver}" if new_ver else ""
                print(f"{GREEN}[✔] termux-app-store upgraded via pip{ver_str}.{R}")
            return True
        else:
            if not silent:
                print(f"{RED}[✗] pip upgrade failed.{R}")
            return False

    this_file   = Path(__file__).resolve()
    app_dir     = this_file.parent

    updated   = []
    has_error = False

    for filename, url in _SELF_FILES.items():
        local_path = app_dir / filename

        remote = _fetch_remote_content(url)
        if remote is None:
            has_error = True
            if not silent:
                print(f"{YELLOW}[!] Could not fetch {filename} from GitHub.{R}")
            continue

        if not _files_differ(local_path, remote):
            continue

        try:
            backup = local_path.with_suffix(".py.bak")
            if local_path.exists():
                _shutil.copy2(local_path, backup)
            local_path.write_bytes(remote)
            updated.append(filename)
            if not silent:
                print(f"{DIM}[*] Repacking {filename.replace('.py','')}... Done{R}")
        except PermissionError:
            has_error = True
            if not silent:
                print(f"{RED}[✗] Permission denied updating {filename}.{R}")
                print(f"    Fix: {CYAN}chmod u+w {local_path}{R}")
        except Exception as e:
            has_error = True
            if not silent:
                print(f"{RED}[✗] Failed to update {filename}: {e}{R}")

    if not updated and not has_error and not silent:
        pass
    elif updated and not silent:
        print(f"{DIM}[*] Rebuild termux-app-store... Done{R}")
        print(f"{GREEN}[✔] termux-app-store updated to new version{R}")

    return bool(updated)


def cmd_version():
    INSTALL_DIR = Path(os.environ.get("PREFIX", "/data/data/com.termux/files/usr")) / "lib" / ".tas"
    SENTINEL = INSTALL_DIR / ".installed"

    local_ver = None
    if SENTINEL.exists():
        try:
            for line in SENTINEL.read_text().splitlines():
                if line.startswith("version="):
                    local_ver = line.split("=", 1)[1].strip()
                    break
        except Exception:
            pass

    if not local_ver:
        try:
            from termux_app_store import __version__
            if __version__:
                local_ver = __version__
        except Exception:
            pass

    if not local_ver:
        for f in [
            INSTALL_DIR / "termux_app_store" / "__init__.py",
            Path(__file__).resolve().parent / "__init__.py",
        ]:
            if f.exists():
                try:
                    m = re.search(r'^__version__\s*=\s*"([0-9.]+)"', f.read_text(), re.MULTILINE)
                    if m:
                        local_ver = m.group(1)
                        break
                except Exception:
                    pass

    if not local_ver:
        for f in [
            INSTALL_DIR / "pyproject.toml",
            Path(__file__).resolve().parent.parent / "pyproject.toml",
        ]:
            if f.exists():
                try:
                    m = re.search(r'^version\s*=\s*"([0-9.]+)"', f.read_text(), re.MULTILINE)
                    if m:
                        local_ver = m.group(1)
                        break
                except Exception:
                    pass

    print(f"\n  {DIM}Fetching version info...{R}")
    remote_tag = fetch_latest_tag()
    remote_ver = remote_tag.lstrip("v") if remote_tag else None

    W = 46
    print(f"\n  {B}{CYAN}{'━'*W}{R}")
    print(f"  {B}   Termux App Store{R}")
    print(f"  {CYAN}{DIM}   https://github.com/{GITHUB_REPO}{R}")
    print(f"  {B}{CYAN}{'━'*W}{R}\n")

    if local_ver:
        print(f"  {B}  Installed {R}  {GREEN}{B}v{local_ver}{R}")
    else:
        print(f"  {B}  Installed {R}  {YELLOW}unknown{R}")

    if remote_ver:
        print(f"  {B}  Latest    {R}  {GREEN}{B}v{remote_ver}{R}")
        if local_ver and _ver_tuple(remote_ver) > _ver_tuple(local_ver):
            print(f"\n  {YELLOW}  ↑  New version available: v{remote_ver}{R}")
            print(f"  {DIM}     Run: {CYAN}termux-app-store update{R}")
        else:
            print(f"\n  {GREEN}  ✔  You are on the latest version{R}")
    else:
        print(f"  {B}  Latest    {R}  {YELLOW}unavailable  {DIM}(check internet){R}")
        if local_ver:
            print(f"\n  {DIM}  Cannot determine if update is available{R}")

    print(f"\n  {B}{CYAN}{'━'*W}{R}\n")


def cmd_search(packages_dir: Path, query: str):
    query_lower = query.lower()
    pkgs = load_all_packages(packages_dir)
    results = [
        p for p in pkgs
        if query_lower in p.get("name", "").lower()
        or query_lower in p.get("desc", "").lower()
    ]
    if not results:
        print(f"\n  {YELLOW}No packages found matching '{query}'{R}\n")
        return
    print(f"\n  {CYAN}{B}Search results for '{query}' — {len(results)} found:{R}\n")
    sep = "─"
    print(f"  {'Package':<28} {'Version':<12} {'Status':<12} Description")
    print(f"  {sep*28} {sep*12} {sep*12} {sep*30}")
    for p in results:
        name    = p.get("name", "")
        version = p.get("version", "?")
        desc    = p.get("desc", "-")[:40]
        status, _ = get_status(name, version)
        if status == "INSTALLED":
            st_color = f"{GREEN}✔ installed{R}"
        elif status == "OUTDATED":
            st_color = f"{YELLOW}↑ outdated{R}"
        else:
            st_color = f"{DIM}○ available{R}"
        print(f"  {CYAN}{name:<28}{R} {DIM}{version:<12}{R} {st_color:<22} {DIM}{desc}{R}")
    print()


def cmd_fix_install(app_root: Path, packages_dir: Path, name: str):
    pkgs = load_all_packages(packages_dir)
    p = next((x for x in pkgs if x["name"] == name), None)
    if not p:
        print(f"\n  {RED}✗  Package '{name}' not found.{R}\n")
        sys.exit(1)
    sep = "─"
    print(f"\n  {DIM}{sep*46}{R}")
    print(f"  {B}  Fix Install {CYAN}{name}{R}{B}  {DIM}v{p['version']}{R}")
    print(f"  {DIM}(using build-package.sh){R}")
    print(f"  {DIM}{sep*46}{R}\n")
    if not ensure_package_files(packages_dir, name, force_update=True):
        print(f"  {RED}✗  Failed to download build files.{R}\n")
        return
    if not ensure_build_package_sh(app_root):
        print(f"  {RED}✗  build-package.sh not found.{R}\n")
        return
    proc = subprocess.Popen(
        ["bash", "build-package.sh", name],
        cwd=str(app_root),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    for line in iter(proc.stdout.readline, b""):
        print(" ", line.decode(errors="ignore").rstrip())
    proc.wait()
    if proc.returncode == 0:
        hold_package(name)
        print(f"\n  {GREEN}{B}✔  '{name}' installed via build-package.sh!{R}\n")
    else:
        print(f"\n  {RED}✗  Fix install failed (exit {proc.returncode}){R}\n")
        sys.exit(proc.returncode)


def cmd_install_multi(app_root: Path, packages_dir: Path, names: list):
    if len(names) == 1:
        cmd_install(app_root, packages_dir, names[0])
        return
    print(f"\n  {CYAN}{B}Installing {len(names)} packages: {', '.join(names)}{R}\n")
    success_list, failed_list = [], []
    for name in names:
        ok = cmd_install(app_root, packages_dir, name, silent=False)
        (success_list if ok else failed_list).append(name)
    sep = "─"
    print(f"\n  {DIM}{sep*46}{R}")
    print(f"  {CYAN}{B}Summary:{R}")
    if success_list:
        print(f"  {GREEN}✔  Installed ({len(success_list)}): {', '.join(success_list)}{R}")
    if failed_list:
        print(f"  {RED}✗  Failed ({len(failed_list)}): {', '.join(failed_list)}{R}")
    print()


def cmd_uninstall_multi(names: list):
    if len(names) == 1:
        cmd_uninstall(names[0])
        return
    print(f"\n  {CYAN}{B}Uninstalling {len(names)} packages: {', '.join(names)}{R}\n")
    success_list, failed_list = [], []
    for name in names:
        if get_installed_version(name) is None:
            print(f"  {YELLOW}[!] '{name}' not installed — skipping{R}\n")
            failed_list.append(name)
            continue
        try:
            cmd_uninstall(name)
            success_list.append(name)
        except SystemExit:
            failed_list.append(name)
    sep = "─"
    print(f"\n  {DIM}{sep*46}{R}")
    print(f"  {CYAN}{B}Summary:{R}")
    if success_list:
        print(f"  {GREEN}✔  Uninstalled ({len(success_list)}): {', '.join(success_list)}{R}")
    if failed_list:
        print(f"  {RED}✗  Failed/skipped ({len(failed_list)}): {', '.join(failed_list)}{R}")
    print()


def cmd_help():
    print(f"""
{B}{CYAN}Termux App Store  {DIM}Official Developer @djunekz{R}

{B}USAGE:{R}
  {CYAN}termux-app-store{R}            Open TUI interface

{B}PACKAGE COMMANDS:{R}
  {CYAN}list{R}  {DIM}| -l | -L{R}             List all packages + status
  {CYAN}search{R} {DIM}| find{R} {B}<query>{R}       Search packages by name or description
  {CYAN}install{R} {DIM}| i | -i{R} {B}<pkg>{R}      Install packages {DIM}(fast — pre-built .deb){R}
  {CYAN}uninstall{R} {DIM}| remove{R} {B}<pkg>{R}    Uninstall packages
  {CYAN}fix-install{R} {B}<package>{R}       Force install using build-package.sh
  {CYAN}show{R} {B}<package>{R}              Show package details

{B}UPDATE COMMANDS:{R}
  {CYAN}update{R}                      Update core and check package updates
  {CYAN}upgrade{R}                     Upgrade all outdated packages
  {CYAN}upgrade{R} {B}<package>{R}           Upgrade a specific package

{B}MIRROR & CACHE:{R}
  {CYAN}mirrors{R}                     Check speed of all download mirrors
  {CYAN}cache info{R}                  Show local .deb cache info
  {CYAN}cache clear{R}                 Clear local .deb cache

{B}INFO:{R}
  {CYAN}version{R} {DIM}| -v{R}                Show app version
  {CYAN}help{R}    {DIM}| -h | --help{R}       Show this help message

{B}EXAMPLES:{R}
  {DIM}termux-app-store search python{R}
  {DIM}termux-app-store install neovim{R}
  {DIM}termux-app-store install tdoc ttyper aichat{R}
  {DIM}termux-app-store uninstall tdoc ttyper{R}
  {DIM}termux-app-store fix-install neovim{R}
  {DIM}termux-app-store upgrade{R}
  {DIM}termux-app-store mirrors{R}
  {DIM}termux-app-store cache info{R}
  {DIM}termux-app-store -l{R}
""")

CMD_ALIASES = {
    "list":         "list",
    "-l":           "list",
    "-L":           "list",
    "search":       "search",
    "find":         "search",
    "-f":           "search",
    "-s":           "search",
    "install":      "install",
    "i":            "install",
    "-i":           "install",
    "uninstall":    "uninstall",
    "un":           "uninstall",
    "remove":       "uninstall",
    "fix-install":  "fix-install",
    "--fix-install":"fix-install",
    "-fi":          "fix-install",
    "show":         "show",
    "update":       "update",
    "upgrade":      "upgrade",
    "version":      "version",
    "-v":           "version",
    "mirrors":      "mirrors",
    "-m":           "mirrors",
    "cache":        "cache",
    "-c":           "cache",
    "help":         "help",
    "-h":           "help",
    "--help":       "help",
}


INDEX_CACHE = INDEX_CACHE_FILE

def _load_package_from_disk(pkg_dir: Path) -> dict:
    name = pkg_dir.name
    build = pkg_dir / "build.sh"
    data = {
        "name": name,
        "desc": "-",
        "version": "?",
        "deps": "-",
        "maintainer": "-",
        "homepage": "-",
        "license": "-",
    }
    if not build.exists():
        return data
    with build.open(errors="ignore") as f:
        for line in f:
            for key, field in [
                ("TERMUX_PKG_DESCRIPTION=", "desc"),
                ("TERMUX_PKG_VERSION=",     "version"),
                ("TERMUX_PKG_MAINTAINER=",  "maintainer"),
                ("TERMUX_PKG_HOMEPAGE=",    "homepage"),
                ("TERMUX_PKG_LICENSE=",     "license"),
            ]:
                if line.startswith(key):
                    data[field] = line.split("=", 1)[1].strip().strip('"')
            if line.startswith("TERMUX_PKG_DEPENDS="):
                data["deps"] = line.split("=", 1)[1].strip().strip('"')
    return data


def load_package(pkg_dir: Path) -> dict:
    name = pkg_dir.name
    raw_index = fetch_index()
    if raw_index:
        match = next((p for p in raw_index if p.get("package") == name), None)
        if match:
            return normalize_pkg(match)
    build = pkg_dir / "build.sh"
    if not build.exists():
        return {
            "name": name,
            "desc": "-",
            "version": "?",
            "deps": "-",
            "maintainer": "-",
            "homepage": "-",
            "license": "-",
        }
    data = {
        "name": name,
        "desc": "-",
        "version": "?",
        "deps": "-",
        "maintainer": "-",
        "homepage": "-",
        "license": "-",
    }
    with build.open(errors="ignore") as f:
        for line in f:
            for key, field in [
                ("TERMUX_PKG_DESCRIPTION=", "desc"),
                ("TERMUX_PKG_VERSION=",     "version"),
                ("TERMUX_PKG_MAINTAINER=",  "maintainer"),
                ("TERMUX_PKG_HOMEPAGE=",    "homepage"),
                ("TERMUX_PKG_LICENSE=",     "license"),
            ]:
                if line.startswith(key):
                    data[field] = line.split("=", 1)[1].strip().strip('"')
            if line.startswith("TERMUX_PKG_DEPENDS="):
                data["deps"] = line.split("=", 1)[1].strip().strip('"')
    return data


def load_all_packages(packages_dir: Path) -> list:
    raw_index = fetch_index()
    if raw_index:
        return [normalize_pkg(p) for p in raw_index]
    pkgs = []
    if not packages_dir.exists():
        return pkgs
    for pkg_dir in sorted(packages_dir.iterdir()):
        if not pkg_dir.is_dir():
            continue
        if not (pkg_dir / "build.sh").exists():
            continue
        pkgs.append(_load_package_from_disk(pkg_dir))
    return pkgs


def run_cli():
    args = sys.argv[1:]

    if not args:
        try:
            from termux_app_store.termux_app_store import run_tui
            run_tui()
        except ImportError:
            print(f"{RED}[!] commamd not found.{R}")
            print(f"{RED}[!] Usage: termux-app-store help")
            cmd_help()
        return

    raw_cmd = args[0]
    cmd = CMD_ALIASES.get(raw_cmd)

    if cmd is None:
        print(f"{RED}[!] Unknown command: '{raw_cmd}'{R}")
        print(f"    Run {CYAN}termux-app-store help{R} to see available commands.")
        sys.exit(1)

    if cmd == "help":
        cmd_help()
        return

    if cmd == "version":
        cmd_version()
        return

    APP_ROOT     = resolve_app_root()
    PACKAGES_DIR = APP_ROOT / "packages"

    if cmd == "list":
        cmd_list(PACKAGES_DIR)

    elif cmd == "show":
        if len(args) < 2:
            print(f"{RED}[!] Usage: termux-app-store show <package>{R}")
            sys.exit(1)
        cmd_show(PACKAGES_DIR, args[1])

    elif cmd == "search":
        if len(args) < 2:
            print(f"{RED}[!] Usage: termux-app-store search <query>{R}")
            sys.exit(1)
        cmd_search(PACKAGES_DIR, args[1])

    elif cmd == "install":
        if len(args) < 2:
            print(f"{RED}[!] Usage: termux-app-store install <package...>{R}")
            sys.exit(1)
        cmd_install_multi(APP_ROOT, PACKAGES_DIR, args[1:])

    elif cmd == "uninstall":
        if len(args) < 2:
            print(f"{RED}[!] Usage: termux-app-store uninstall <package...>{R}")
            sys.exit(1)
        cmd_uninstall_multi(args[1:])

    elif cmd == "fix-install":
        if len(args) < 2:
            print(f"{RED}[!] Usage: termux-app-store fix-install <package>{R}")
            sys.exit(1)
        cmd_fix_install(APP_ROOT, PACKAGES_DIR, args[1])

    elif cmd == "update":
        cmd_update(PACKAGES_DIR)

    elif cmd == "upgrade":
        target = args[1] if len(args) >= 2 else None
        cmd_upgrade(APP_ROOT, PACKAGES_DIR, target)

    elif cmd == "mirrors":
        print(f"\n  {DIM}Checking all mirrors...{R}\n")
        if _FAST_INSTALL_AVAILABLE:
            results = check_mirrors(log_fn=lambda m: print(f"  {m}"))
            online = sum(1 for r in results if r["online"])
            print(f"\n  {online}/{len(results)} mirrors online\n")
        else:
            print(f"  {YELLOW}Fast install module not available.{R}\n")

    elif cmd == "cache":
        sub = args[1] if len(args) >= 2 else "info"
        if sub == "info":
            if _FAST_INSTALL_AVAILABLE:
                print()
                cache_info(log_fn=lambda m: print(f"  {m}"))
            else:
                print(f"  {YELLOW}Fast install module not available.{R}\n")
        elif sub == "clear":
            if _FAST_INSTALL_AVAILABLE:
                clear_deb_cache(log_fn=lambda m: print(f"  {m}"))
            else:
                print(f"  {YELLOW}Fast install module not available.{R}\n")
        else:
            print(f"  {RED}Unknown cache subcommand: '{sub}'{R}")
            print(f"  Usage: termux-app-store cache [info|clear]")


if __name__ == "__main__":
    run_cli()

# Open Contributor
# https://github.com/djunekz/termux-app-store
