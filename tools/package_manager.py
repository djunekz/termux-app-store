#!/usr/bin/env python3
import json
import os
import subprocess
import urllib.request
import urllib.error
import time
import platform
from pathlib import Path
from typing import Dict, List, Optional, Tuple

APP_VERSION = "0.1.6"

# Allow forks/mirrors without editing the code.
GITHUB_REPO = os.getenv("TERMUX_APP_STORE_GITHUB_REPO", "djunekz/termux-app-store")
GITHUB_API_LATEST = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"

# Default to master for compatibility with this repository, but fall back to main.
_INDEX_BRANCHES = [
    os.getenv("TERMUX_APP_STORE_INDEX_BRANCH", "master"),
    "main",
]

_INDEX_URL_OVERRIDE = os.getenv("TERMUX_APP_STORE_INDEX_URL")
if _INDEX_URL_OVERRIDE:
    GITHUB_INDEX_URLS = [_INDEX_URL_OVERRIDE]
else:
    GITHUB_INDEX_URLS = [
        f"https://raw.githubusercontent.com/{GITHUB_REPO}/{branch}/tools/index.json"
        for branch in _INDEX_BRANCHES
        if branch
    ]

CACHE_DIR = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "termux-app-store"
CACHE_FILE = CACHE_DIR / "index.json"
CACHE_TTL = 6 * 3600

PREFIX = os.environ.get("PREFIX", "/data/data/com.termux/files/usr")

def get_architecture() -> str:
    arch = platform.machine().lower()
    arch_map = {
        'aarch64': 'aarch64',
        'armv7l': 'arm',
        'armv8l': 'arm',
        'x86_64': 'x86_64',
        'i686': 'i686',
        'i386': 'i686',
    }
    return arch_map.get(arch, 'unknown')


def download_file(url: str, destination: Path, timeout: int = 30) -> bool:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "termux-app-store"})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = response.read()
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
            return True
    except Exception as e:
        print(f"[ERROR] Download failed: {e}")
        return False


def fetch_json(url: str, timeout: int = 10) -> Optional[Dict]:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "termux-app-store"})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"[ERROR] Failed to fetch JSON: {e}")
        return None


def parse_version(version: str) -> Tuple[int, ...]:
    """Best-effort version parsing.

    Handles:
      - v1.2.3
      - 1.2
      - 1.2.3-beta (pre-release ignored for ordering)
      - 1.2.3+meta (build metadata ignored)
    """
    v = (version or "").strip().lstrip("v")
    # Drop pre-release/build metadata
    v = v.split("+", 1)[0].split("-", 1)[0]
    parts = []
    for p in v.split("."):
        try:
            parts.append(int(p))
        except Exception:
            parts.append(0)
    # Normalize length
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts[:6])


def compare_versions(current: str, latest: str) -> int:
    current_tuple = parse_version(current)
    latest_tuple = parse_version(latest)

    if current_tuple < latest_tuple:
        return -1
    elif current_tuple > latest_tuple:
        return 1
    else:
        return 0


class PackageSource:
    @staticmethod
    def detect_mode(packages_dir: Optional[Path] = None) -> str:
        if mode := os.getenv("TERMUX_APP_STORE_MODE"):
            return mode.lower()

        if packages_dir and packages_dir.exists() and packages_dir.is_dir():
            if any((packages_dir / d / "build.sh").exists() for d in packages_dir.iterdir() if d.is_dir()):
                return "local"

        return "remote"


class PackageManager:

    def __init__(self, packages_dir: Optional[Path] = None):
        self.packages_dir = packages_dir
        self.mode = PackageSource.detect_mode(packages_dir)
        self.cache_file = CACHE_FILE
        self.cache_ttl = CACHE_TTL

    def _is_cache_valid(self) -> bool:
        if not self.cache_file.exists():
            return False
        age = time.time() - self.cache_file.stat().st_mtime
        return age < self.cache_ttl

    def _save_cache(self, data: Dict):
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        self.cache_file.write_text(json.dumps(data, indent=2))

    def _load_cache(self) -> Optional[Dict]:
        try:
            if self.cache_file.exists():
                return json.loads(self.cache_file.read_text())
        except Exception as e:
            print(f"[ERROR] Failed to load cache: {e}")
        return None

    def clear_cache(self):
        if self.cache_file.exists():
            self.cache_file.unlink()

    def load_packages(self) -> List[Dict]:
        if self.mode == "local":
            return self._load_local()
        else:
            return self._load_remote()

    def _load_local(self) -> List[Dict]:
        if not self.packages_dir or not self.packages_dir.exists():
            return []

        packages = []
        for pkg_dir in sorted(self.packages_dir.iterdir()):
            if not pkg_dir.is_dir():
                continue

            build_sh = pkg_dir / "build.sh"
            if not build_sh.exists():
                continue

            pkg_data = self._parse_build_sh(pkg_dir)
            packages.append(pkg_data)

        return packages

    def _parse_build_sh(self, pkg_dir: Path) -> Dict:
        data = {
            "package": pkg_dir.name,
            "name": pkg_dir.name,
            "desc": "-",
            "description": "-",
            "version": "?",
            "deps": "-",
            "depends": [],
            "maintainer": "-",
            "homepage": "-",
            "license": "-",
            "srcurl": "",
            "sha256": "",
        }

        build_sh = pkg_dir / "build.sh"
        try:
            with build_sh.open(errors="ignore") as f:
                for line in f:
                    line = line.strip()

                    if line.startswith("TERMUX_PKG_DESCRIPTION="):
                        val = line.split("=", 1)[1].strip().strip('"\'')
                        data["desc"] = val
                        data["description"] = val

                    elif line.startswith("TERMUX_PKG_VERSION="):
                        data["version"] = line.split("=", 1)[1].strip().strip('"\'')

                    elif line.startswith("TERMUX_PKG_DEPENDS="):
                        deps_str = line.split("=", 1)[1].strip().strip('"\'')
                        data["deps"] = deps_str
                        data["depends"] = [d.strip() for d in deps_str.split(",") if d.strip()]

                    elif line.startswith("TERMUX_PKG_MAINTAINER="):
                        data["maintainer"] = line.split("=", 1)[1].strip().strip('"\'')

                    elif line.startswith("TERMUX_PKG_HOMEPAGE="):
                        data["homepage"] = line.split("=", 1)[1].strip().strip('"\'')

                    elif line.startswith("TERMUX_PKG_LICENSE="):
                        data["license"] = line.split("=", 1)[1].strip().strip('"\'')

                    elif line.startswith("TERMUX_PKG_SRCURL="):
                        data["srcurl"] = line.split("=", 1)[1].strip().strip('"\'')

                    elif line.startswith("TERMUX_PKG_SHA256="):
                        data["sha256"] = line.split("=", 1)[1].strip().strip('"\'')

        except Exception as e:
            print(f"[WARNING] Failed to parse {build_sh}: {e}")

        return data

    def _load_remote(self) -> List[Dict]:
        if self._is_cache_valid():
            cached = self._load_cache()
            if cached and "packages" in cached:
                return cached["packages"]

        print("[*] Fetching package index from GitHub...")
        data = None
        for url in GITHUB_INDEX_URLS:
            data = fetch_json(url)
            if data and "packages" in data:
                break

        if data and "packages" in data:
            self._save_cache(data)
            return [self._normalize_remote_pkg(p) for p in data["packages"]]

        cached = self._load_cache()
        if cached and "packages" in cached:
            print("[!] Using cached data (offline mode)")
            return [self._normalize_remote_pkg(p) for p in cached["packages"]]

        return []

    @staticmethod
    def _normalize_remote_pkg(pkg: Dict) -> Dict:
        """Normalize the remote index schema to match the local parser."""
        pkg = dict(pkg)
        pkg.setdefault("name", pkg.get("package"))
        desc = pkg.get("description") or pkg.get("desc") or "-"
        pkg.setdefault("desc", desc)
        pkg.setdefault("description", desc)
        # Keep older keys compatible
        deps = pkg.get("depends")
        if isinstance(deps, str):
            pkg["depends"] = [d.strip() for d in deps.split(",") if d.strip()]
        pkg.setdefault("deps", ", ".join(pkg.get("depends") or []))
        return pkg

    def get_package(self, name: str) -> Optional[Dict]:
        packages = self.load_packages()
        for pkg in packages:
            if pkg.get("package") == name or pkg.get("name") == name:
                return pkg
        return None

    def get_installed_version(self, name: str) -> Optional[str]:
        # Termux's `pkg info` is best, but not always available.
        try:
            out = subprocess.check_output(
                ["pkg", "info", name],
                stderr=subprocess.DEVNULL,
                text=True,
            )
            for line in out.splitlines():
                if line.startswith("Version:"):
                    return line.split(":", 1)[1].strip()
        except Exception:
            pass

        # Fallback to dpkg-query.
        try:
            out = subprocess.check_output(
                ["dpkg-query", "-W", "-f=${Version}", name],
                stderr=subprocess.DEVNULL,
                text=True,
            ).strip()
            return out or None
        except Exception:
            pass
        return None

    def get_status(self, name: str, version: str) -> Tuple[str, str]:
        installed = self.get_installed_version(name)

        if installed is None:
            return "NOT_INSTALLED", "not installed"

        if compare_versions(installed, version) < 0:
            return "UPDATE", f"update available ({installed} → {version})"

        return "INSTALLED", f"up-to-date ({version})"


class AppUpdateChecker:
    @staticmethod
    def get_latest_version() -> Optional[str]:
        data = fetch_json(GITHUB_API_LATEST)
        if data and "tag_name" in data:
            return data["tag_name"].lstrip('v')
        return None

    @staticmethod
    def check_update() -> Tuple[bool, Optional[str]]:
        latest = AppUpdateChecker.get_latest_version()
        if not latest:
            return False, None

        comparison = compare_versions(APP_VERSION, latest)
        return comparison < 0, latest

    @staticmethod
    def get_download_url(version: str) -> str:

        arch = get_architecture()
        return f"https://github.com/{GITHUB_REPO}/releases/download/v{version}/termux-app-store-{arch}"

    @staticmethod
    def upgrade_app(latest_version: str) -> bool:
        print(f"\n[*] Downloading termux-app-store v{latest_version}...")

        url = AppUpdateChecker.get_download_url(latest_version)
        temp_file = Path("/tmp/termux-app-store-new")

        if not download_file(url, temp_file):
            print("[ERROR] Download failed")
            return False

        temp_file.chmod(0o755)

        target = Path(PREFIX) / "bin" / "termux-app-store"
        try:
            import shutil
            shutil.move(str(temp_file), str(target))
            print(f"[✔] Successfully upgraded to v{latest_version}!")
            print(f"    Restart termux-app-store to use the new version.")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to install: {e}")
            return False

__all__ = [
    'PackageManager',
    'AppUpdateChecker',
    'APP_VERSION',
    'compare_versions',
]
