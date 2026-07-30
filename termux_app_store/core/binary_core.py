import hashlib
import logging
import time
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional, Dict

from .mirrors import MirrorManager

logger = logging.getLogger(__name__)


def _verify_sha256(path: Path, expected: str) -> bool:
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            while chunk := f.read(65536):
                h.update(chunk)
        return h.hexdigest() == expected
    except Exception:
        return False


class BinaryCache:

    def __init__(self):
        self.mirror_manager = MirrorManager()
        self.cache_dir: Path = self._get_cache_dir()
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.config = self.mirror_manager.get_binary_cache_config()
        self.enabled = self.config.get("enabled", True)

        logger.info(f"Binary Cache initialized (enabled: {self.enabled})")
        logger.debug(f"Cache directory: {self.cache_dir}")

    def _get_cache_dir(self) -> Path:
        cache_path = self.mirror_manager.binary_config.get(
            "cache_dir", "~/.cache/termux-app-store/binaries"
        )
        return Path(cache_path).expanduser()

    def get_cache_path(self, pkg_name: str, version: str, arch: str) -> Path:
        filename = f"{pkg_name}_{version}_{arch}.deb"
        return self.cache_dir / filename

    def has_local_binary(self, pkg_name: str, version: str, arch: str) -> bool:
        path = self.get_cache_path(pkg_name, version, arch)
        if not path.exists():
            return False
        age = time.time() - path.stat().st_mtime
        return age < 604800

    def download_from_mirror(
        self,
        pkg_name: str,
        version: str,
        arch: str,
        mirror_url: str,
        sha256: str,
    ) -> Optional[Path]:
        if not sha256:
            logger.error(
                f"Refusing to download {pkg_name}-{version} ({arch}): no SHA256 "
                f"provided for verification"
            )
            return None

        cache_path = self.get_cache_path(pkg_name, version, arch)
        url = f"{mirror_url.rstrip('/')}/pool/main/{pkg_name}_{version}_{arch}.deb"
        tmp_path = cache_path.with_suffix(".tmp")

        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "termux-app-store"}
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                with open(tmp_path, "wb") as f:
                    while chunk := resp.read(65536):
                        f.write(chunk)

            if not _verify_sha256(tmp_path, sha256):
                tmp_path.unlink(missing_ok=True)
                logger.error(f"SHA256 mismatch for {pkg_name}-{version}")
                return None

            tmp_path.rename(cache_path)
            logger.info(f"Cached: {pkg_name} {version} ({arch})")
            return cache_path

        except urllib.error.HTTPError as e:
            if e.code == 404:
                logger.debug(f"Not found at {mirror_url}: {pkg_name}_{version}_{arch}.deb")
            else:
                logger.error(f"HTTP {e.code} from {url}")
            tmp_path.unlink(missing_ok=True)
            return None
        except Exception as e:
            logger.error(f"Download failed from {url}: {e}")
            tmp_path.unlink(missing_ok=True)
            return None

    def get_best_binary(
        self,
        pkg_name: str,
        version: str,
        arch: str,
        sha256: str = "",
    ) -> Optional[Path]:
        if not self.enabled:
            return None

        if self.has_local_binary(pkg_name, version, arch):
            cache_path = self.get_cache_path(pkg_name, version, arch)
            if sha256 and not _verify_sha256(cache_path, sha256):
                logger.error(f"Cached binary for {pkg_name} failed SHA256 check — discarding")
                cache_path.unlink(missing_ok=True)
            else:
                logger.info(f"Cache HIT: {pkg_name}")
                return cache_path

        for mirror in self.mirror_manager.get_enabled_mirrors():
            result = self.download_from_mirror(
                pkg_name, version, arch, mirror.url, sha256
            )
            if result:
                return result

        logger.info(f"No prebuilt binary found for {pkg_name} {version} ({arch})")
        return None

    def clean_old_cache(self, max_age_days: int = 30) -> int:
        now = time.time()
        cleaned = 0
        for file in self.cache_dir.glob("*.deb"):
            if (now - file.stat().st_mtime) / 86400 > max_age_days:
                file.unlink(missing_ok=True)
                cleaned += 1
        if cleaned > 0:
            logger.info(f"Cleaned {cleaned} old binary cache files")
        return cleaned
