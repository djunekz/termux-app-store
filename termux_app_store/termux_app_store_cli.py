"""
termux-app-store

USAGE:
  termux-app-store                     Open TUI
  termux-app-store list  | -l | -L     List packages + status
  termux-app-store install | i | -i    Install a package
  termux-app-store uninstall           Uninstall a package
  termux-app-store show                Show package details
  termux-app-store update              Sync index.json terbaru + tampilkan yang ada update
  termux-app-store upgrade             Upgrade all outdated packages
  termux-app-store upgrade <pkg>       Upgrade a specific package
  termux-app-store version | -v        Show app version
  termux-app-store help | -h | --help  Show help
"""

import subprocess
import sys
import os
import json
import re
import urllib.request
import urllib.error
import shutil
from pathlib import Path

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

# Self-update: URL raw file di GitHub
_SELF_FILES = {
    "termux_app_store_cli.py": f"https://raw.githubusercontent.com/{GITHUB_REPO}/master/termux_app_store_cli.py",
    "termux_app_store.py":     f"https://raw.githubusercontent.com/{GITHUB_REPO}/master/termux_app_store.py",
}

# Install dir (sama dengan yang di install.sh)
_INSTALL_DIR = Path(os.environ.get("PREFIX", "/data/data/com.termux/files/usr")) / "lib" / ".tas"

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

    base = (
        Path(sys.executable).resolve().parent
        if getattr(sys, "frozen", False)
        else Path(__file__).resolve().parent
    )

    if is_valid_root(base):
        save_cached_root(base)
        return base

    print(f"{RED}[!] Cannot find termux-app-store root.{R}")
    print(f"    Set: {CYAN}export TERMUX_APP_STORE_HOME=/path/to/termux-app-store{R}")
    sys.exit(1)


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
    return {
        "name":       raw.get("package", raw.get("name", "?")),
        "desc":       raw.get("description", raw.get("desc", "-")),
        "version":    raw.get("version", "?"),
        "deps":       deps,
        "maintainer": raw.get("maintainer", "-"),
        "homepage":   raw.get("homepage", "-"),
        "license":    raw.get("license", "-"),
    }


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
        status_part, _, version_part = out.partition("\t")
        if "installed" in status_part:
            return version_part.strip() or None
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


def cleanup_package_files(name: str) -> int:
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
    print(f"\n{DIM}[*] Loading package list...{R}")
    pkgs = load_all_packages(packages_dir)
    if not pkgs:
        print(f"{YELLOW}[!] No packages found.{R}")
        return

    print(f"\n{B}{CYAN}{'PACKAGE':<22} {'VERSION':<12} STATUS{R}")
    print(f"{DIM}{'─'*55}{R}")

    for p in pkgs:
        _, label = get_status(p["name"], p["version"])
        print(f"{B}{p['name']:<22}{R} {CYAN}{p['version']:<12}{R} {label}")

    print(f"\n{DIM}Total: {len(pkgs)} package(s){R}\n")


def cmd_show(packages_dir: Path, name: str):
    pkgs = load_all_packages(packages_dir)
    p = next((x for x in pkgs if x["name"] == name), None)

    if not p:
        print(f"{RED}[!] Package '{name}' not found.{R}")
        print(f"    Run {CYAN}termux-app-store list{R} to see available packages.")
        sys.exit(1)

    _, label = get_status(p["name"], p["version"])
    deps = p.get("deps", "-")
    if isinstance(deps, list):
        deps_str = ", ".join(deps) if deps else "-"
    else:
        deps_str = deps if deps and deps != "-" else "-"

    print(f"""
{B}{CYAN}{'━'*42}{R}
{B}  {p['name']}{R}   {label}
{B}{CYAN}{'━'*42}{R}

  {B}Description :{R} {p['desc']}
  {B}Version     :{R} {CYAN}{p['version']}{R}
  {B}Maintainer  :{R} {p['maintainer']}
  {B}License     :{R} {p.get('license', '-')}
  {B}Homepage    :{R} {p.get('homepage', '-')}
  {B}Dependencies:{R} {YELLOW}{deps_str}{R}

{B}{CYAN}{'━'*42}{R}
""")


def ensure_package_files(packages_dir: Path, name: str) -> bool:
    """Download build.sh dari GitHub jika belum ada lokal."""
    pkg_dir = packages_dir / name
    build_sh = pkg_dir / "build.sh"

    if build_sh.exists():
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
                build_sh.write_bytes(raw)
                return True
    except Exception:
        pass
    return False


def cmd_install(app_root: Path, packages_dir: Path, name: str, silent: bool = False) -> bool:
    pkgs = load_all_packages(packages_dir)
    p = next((x for x in pkgs if x["name"] == name), None)

    if not p:
        print(f"{RED}[!] Package '{name}' not found.{R}")
        print(f"    Run {CYAN}termux-app-store list{R} to see available packages.")
        sys.exit(1)

    status, _ = get_status(name, p["version"])

    if status == "INSTALLED" and not silent:
        print(f"{GREEN}[✔] '{name}' is already up-to-date ({p['version']}).{R}")
        return True

    print(f"\n{B}[*] Installing {CYAN}{name}{R}{B} v{p['version']}...{R}\n")

    if not ensure_package_files(packages_dir, name):
        print(f"{RED}[✗] Failed to download build files for '{name}'.{R}")
        print(f"    Check your internet connection or try again later.")
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

    if proc.returncode == 0:
        hold_package(name)
        print(f"\n{GREEN}{B}[✔] '{name}' installed successfully!{R}\n")
        return True
    else:
        print(f"\n{RED}[✗] Install failed (exit code {proc.returncode}).{R}\n")
        return False


def cmd_uninstall(name: str):
    installed = get_installed_version(name)
    if installed is None:
        print(f"{YELLOW}[!] '{name}' is not installed.{R}")
        return

    print(f"\n{B}[*] Uninstalling {CYAN}{name}{R}{B}...{R}\n")

    prefix = os.environ.get("PREFIX", "/data/data/com.termux/files/usr")
    cleanup_paths = [
        Path(prefix) / "lib" / name,
        Path(prefix) / "share" / "doc" / name,
        Path(prefix) / "share" / name,
    ]

    print(f"{DIM}[*] Pre-cleaning cache files...{R}")
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
        print(f"\n{GREEN}{B}[✔] '{name}' uninstalled successfully!{R}\n")
    else:
        hold_package(name)
        print(f"\n{RED}[✗] Uninstall failed.{R}\n")
        sys.exit(ret)


def cmd_update(packages_dir: Path):
    print(f"\n{B}[*] Syncing package index from GitHub...{R}")

    # Cek & update file inti (cli/tui) dari GitHub
    cmd_self_update(silent=False)

    raw = fetch_index()
    if raw:
        print(f"{GREEN}[✔] Index updated — {len(raw)} packages found.{R}\n")
        pkgs = [normalize_pkg(p) for p in raw]
    else:
        print(f"{YELLOW}[!] Could not reach GitHub. Using cached index.{R}\n")
        pkgs = get_packages(packages_dir, online=False)

    if not pkgs:
        print(f"{YELLOW}[!] No packages found.{R}")
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

    print(f"{B}{CYAN}{'PACKAGE':<22} {'INSTALLED':<14} LATEST{R}")
    print(f"{DIM}{'─'*55}{R}")

    if not outdated:
        print(f"{GREEN}  All {installed_count} installed package(s) are up-to-date! ✔{R}")
    else:
        for name, inst, latest in outdated:
            print(
                f"{B}{name:<22}{R} "
                f"{DIM}{inst:<14}{R} "
                f"{GREEN}{latest:<12}{R}  {YELLOW}↑ update available{R}"
            )
        print(
            f"\n{YELLOW}[!] {len(outdated)} update(s) available.{R} "
            f"Run {CYAN}termux-app-store upgrade{R} to apply."
        )

    print(f"\n{DIM}Checked: {installed_count} installed package(s){R}\n")


def cmd_upgrade(app_root: Path, packages_dir: Path, target=None):
    pkgs = load_all_packages(packages_dir)

    if target:
        p = next((x for x in pkgs if x["name"] == target), None)
        if not p:
            print(f"{RED}[!] Package '{target}' not found.{R}")
            sys.exit(1)
        status, _ = get_status(target, p["version"])
        if status == "NOT INSTALLED":
            print(f"{YELLOW}[!] '{target}' is not installed.{R}")
            print(f"    Use {CYAN}termux-app-store install {target}{R} instead.")
            return
        if status == "INSTALLED":
            print(f"{GREEN}[✔] '{target}' is already up-to-date ({p['version']}).{R}")
            return
        cmd_install(app_root, packages_dir, target, silent=True)
        return

    to_upgrade = []
    for p in pkgs:
        status, _ = get_status(p["name"], p["version"])
        if status == "UPDATE":
            to_upgrade.append(p)

    if not to_upgrade:
        print(f"\n{GREEN}[✔] All installed packages are already up-to-date!{R}\n")
        return

    print(f"\n{B}{YELLOW}[*] {len(to_upgrade)} package(s) will be upgraded:{R}")
    for p in to_upgrade:
        inst = get_installed_version(p["name"])
        print(f"    {CYAN}{p['name']:<22}{R} {DIM}{inst}{R} → {GREEN}{p['version']}{R}")
    print()

    ok = 0
    fail = 0
    for p in to_upgrade:
        success = cmd_install(app_root, packages_dir, p["name"], silent=True)
        if success:
            ok += 1
        else:
            fail += 1

    print(f"\n{B}Upgrade summary:{R} {GREEN}{ok} succeeded{R}", end="")
    if fail:
        print(f"  {RED}{fail} failed{R}", end="")
    print("\n")


def _fetch_remote_content(url: str):
    """Fetch raw bytes dari URL. Return None jika gagal."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "termux-app-store-cli"})
        with urllib.request.urlopen(req, timeout=12) as resp:
            return resp.read()
    except Exception:
        return None


def _files_differ(local_path: "Path", remote_bytes: bytes) -> bool:
    """True jika konten file lokal berbeda dengan remote."""
    try:
        return local_path.read_bytes() != remote_bytes
    except Exception:
        return True


def cmd_self_update(silent: bool = False) -> bool:
    """
    Cek & update file inti (termux_app_store_cli.py + termux_app_store.py)
    langsung dari GitHub tanpa perlu bash install.sh.

    Return True jika ada file yang diupdate, False jika sudah up-to-date.
    """
    if not silent:
        print(f"\n{B}[*] Checking for core file updates...{R}")

    install_dir = None

    env_home = os.environ.get("TERMUX_APP_STORE_HOME")
    if env_home:
        p = Path(env_home).expanduser().resolve()
        if p.is_dir():
            install_dir = p

    if install_dir is None and _INSTALL_DIR.is_dir():
        install_dir = _INSTALL_DIR

    if install_dir is None:
        install_dir = Path(__file__).resolve().parent

    updated = []
    failed  = []

    for filename, url in _SELF_FILES.items():
        local_path = install_dir / filename
        if not silent:
            print(f"  {DIM}Checking {filename}...{R}", end=" ", flush=True)

        remote = _fetch_remote_content(url)

        if remote is None:
            if not silent:
                print(f"{YELLOW}(network error, skipped){R}")
            failed.append(filename)
            continue

        if not _files_differ(local_path, remote):
            if not silent:
                print(f"{GREEN}up-to-date{R}")
            continue

        # Ada perubahan — overwrite
        try:
            import shutil as _shutil
            backup = local_path.with_suffix(".py.bak")
            if local_path.exists():
                _shutil.copy2(local_path, backup)

            local_path.write_bytes(remote)
            if not silent:
                print(f"{GREEN}{B}updated!{R}")
            updated.append(filename)
        except Exception as e:
            if not silent:
                print(f"{RED}write error: {e}{R}")
            failed.append(filename)

    if updated:
        print(f"\n{GREEN}{B}[✔] {len(updated)} core file(s) updated: {', '.join(updated)}{R}")
        print(f"    {DIM}Backups saved as *.py.bak in {install_dir}{R}\n")
    elif not failed and not silent:
        print(f"\n{GREEN}[✔] Core files are already up-to-date.{R}\n")

    if failed and not silent:
        print(f"{YELLOW}[!] Could not update: {', '.join(failed)} (check internet){R}\n")

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
        for f in [
            INSTALL_DIR / "termux_app_store" / "main.py",
            INSTALL_DIR / "termux_app_store" / "termux_app_store_cli.py",
            Path(__file__).resolve().parent / "main.py",
        ]:
            if f.exists():
                try:
                    m = re.search(r'APP_VERSION\s*=\s*"([0-9.]+)"', f.read_text())
                    if m:
                        local_ver = m.group(1)
                        break
                except Exception:
                    pass

    print(f"\n{B}[*] Fetching latest version from GitHub...{R}")
    remote_tag = fetch_latest_tag()
    remote_ver = remote_tag.lstrip("v") if remote_tag else None

    print(f"\n  {B}Termux App Store{R}")
    print(f"  {B}Official :{R} {CYAN}https://github.com/{GITHUB_REPO}{R}")

    if local_ver:
        print(f"  {B}Installed:{R} {GREEN}{B}v{local_ver}{R}")
    else:
        print(f"  {B}Installed:{R} {YELLOW}unknown{R}")

    if remote_ver:
        print(f"  {B}Latest   :{R} {GREEN}{B}v{remote_ver}{R}")
        if local_ver and _ver_tuple(remote_ver) > _ver_tuple(local_ver):
            print(f"\n  {YELLOW}{B}⬆  New version available: v{remote_ver}{R}")
            print(f"  {DIM}Run: {CYAN}termux-app-store upgrade{R}{DIM} to update{R}")
        else:
            print(f"\n  {GREEN}{B}✔  This is the latest version{R}")
    else:
        print(f"  {B}Latest   :{R} {YELLOW}(Could not fetch — check internet){R}")
        if local_ver:
            print(f"\n  {DIM}Cannot determine if update is available{R}")

    print()


def cmd_help():
    print(f"""
{B}{CYAN}Termux App Store  {DIM}Official Developer @djunekz{R}

{B}USAGE:{R}
  {CYAN}termux-app-store{R}            Open TUI interface

{B}PACKAGE COMMANDS:{R}
  {CYAN}list{R}  {DIM}| -l | -L{R}             List all packages + status
  {CYAN}install{R} {DIM}| i | -i{R} {B}<package>{R}  Install a package
  {CYAN}uninstall{R} {B}<package>{R}         Uninstall a package
  {CYAN}show{R} {B}<package>{R}              Show package details

{B}UPDATE COMMANDS:{R}
  {CYAN}update{R}                      Sync index, update core files + check package updates
  {CYAN}upgrade{R}                     Upgrade all outdated packages
  {CYAN}upgrade{R} {B}<package>{R}           Upgrade a specific package

{B}INFO:{R}
  {CYAN}version{R} {DIM}| -v{R}                Show app version
  {CYAN}help{R}    {DIM}| -h | --help{R}       Show this help message

{B}EXAMPLES:{R}
  {DIM}termux-app-store install impulse{R}
  {DIM}termux-app-store -i impulse{R}
  {DIM}termux-app-store upgrade webshake{R}
  {DIM}termux-app-store upgrade{R}
  {DIM}termux-app-store update{R}
  {DIM}termux-app-store -l{R}
  {DIM}termux-app-store -v{R}
""")


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


def run_cli():
    args = sys.argv[1:]

    if not args:
        try:
            from termux_app_store import TermuxAppStore
            TermuxAppStore().run()
        except ImportError:
            print(f"{RED}[!] TUI module not found.{R}")
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

    elif cmd == "install":
        if len(args) < 2:
            print(f"{RED}[!] Usage: termux-app-store install <package>{R}")
            sys.exit(1)
        cmd_install(APP_ROOT, PACKAGES_DIR, args[1])

    elif cmd == "uninstall":
        if len(args) < 2:
            print(f"{RED}[!] Usage: termux-app-store uninstall <package>{R}")
            sys.exit(1)
        cmd_uninstall(args[1])

    elif cmd == "update":
        cmd_update(PACKAGES_DIR)

    elif cmd == "upgrade":
        target = args[1] if len(args) >= 2 else None
        cmd_upgrade(APP_ROOT, PACKAGES_DIR, target)



if __name__ == "__main__":
    run_cli()


INDEX_CACHE  = INDEX_CACHE_FILE

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
        index_names = {p.get("package", p.get("name", "")) for p in raw_index}
        pkgs = [normalize_pkg(p) for p in raw_index]
        if packages_dir.exists():
            for pkg_dir in sorted(packages_dir.iterdir()):
                if not pkg_dir.is_dir():
                    continue
                if not (pkg_dir / "build.sh").exists():
                    continue
                if pkg_dir.name not in index_names:
                    pkgs.append(_load_package_from_disk(pkg_dir))
        return pkgs
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
