import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class Mirror:
    id: str
    name: str
    url: str
    type: str = "apt"
    region: str = "global"
    priority: int = 999
    enabled: bool = True
    cdn: bool = False


class MirrorManager:
    def __init__(self):
        self.mirrors: List[Mirror] = []
        self.binary_config: Dict = {}
        self.primary = None
        self.load_config()

    def load_config(self) -> None:
        mirrors_path = Path(__file__).parent.parent.parent / "tools" / "mirrors.json"

        if not mirrors_path.exists():
            logger.warning(f"mirrors.json not found at: {mirrors_path}")
            self._set_default_config()
            return

        try:
            with open(mirrors_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.binary_config = data.get("binary_cache", {})

            primary = data.get("primary")
            if primary:
                self.primary = Mirror(
                    id="primary",
                    name=primary.get("name", "Primary"),
                    url=primary.get("url", ""),
                    type=primary.get("type", "apt"),
                    region=primary.get("region", "global"),
                    priority=1,
                    enabled=primary.get("enabled", True),
                )

            self.mirrors = []
            for m in data.get("mirrors", []):
                self.mirrors.append(
                    Mirror(
                        id=m.get("id", ""),
                        name=m.get("name", ""),
                        url=m.get("url", ""),
                        type=m.get("type", "apt"),
                        region=m.get("region", "global"),
                        priority=m.get("priority", 999),
                        enabled=m.get("enabled", True),
                        cdn=m.get("cdn", False),
                    )
                )

            self.mirrors.sort(key=lambda x: x.priority)

            if self.primary:
                self.mirrors.insert(0, self.primary)

            logger.info(f"Loaded {len(self.mirrors)} mirrors from mirrors.json")

        except Exception as e:
            logger.error(f"Failed to read mirrors.json: {e}")
            self._set_default_config()

    def _set_default_config(self):
        self.mirrors = [
            Mirror(
                id="github-pages",
                name="GitHub Pages",
                url="https://djunekz.github.io/termux-app-store",
                priority=1,
                enabled=True,
            ),
            Mirror(
                id="cloudflare",
                name="Cloudflare CDN",
                url="https://termux-app-store.pages.dev",
                priority=2,
                enabled=True,
                cdn=True,
            ),
        ]
        self.binary_config = {
            "enabled": True,
            "cache_dir": "~/.cache/termux-app-store/binaries",
            "verify_sha256": True,
        }

    def get_all_mirrors(self) -> List[Mirror]:
        return self.mirrors

    def get_enabled_mirrors(self) -> List[Mirror]:
        return [m for m in self.mirrors if m.enabled]

    def get_binary_cache_config(self) -> Dict:
        return self.binary_config

    def get_best_mirror(self) -> Optional[Mirror]:
        enabled = self.get_enabled_mirrors()
        return enabled[0] if enabled else None
