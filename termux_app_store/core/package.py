from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Package:

    name: str
    version: str
    description: str = ""
    maintainer: str = ""
    license: str = "Unknown"

    arch: List[str] = field(default_factory=lambda: ["aarch64"])

    binary_support: bool = False
    prebuilt: Dict[str, Dict] = field(default_factory=dict)

    source: Dict = field(default_factory=dict)

    dependencies: List[str] = field(default_factory=list)
    category: str = "misc"
    tags: List[str] = field(default_factory=list)
    status: str = "stable"

    installed: bool = False
    installed_version: Optional[str] = None
    build_date: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict) -> 'Package':
        return cls(
            name=data.get("name", ""),
            version=data.get("version", ""),
            description=data.get("description", ""),
            maintainer=data.get("maintainer", ""),
            license=data.get("license", "Unknown"),
            arch=data.get("arch", ["aarch64"]),

            binary_support=data.get("binary_support", False),
            prebuilt=data.get("prebuilt", {}),

            source=data.get("source", {}),
            dependencies=data.get("dependencies", []),
            category=data.get("category", "misc"),
            tags=data.get("tags", []),
            status=data.get("status", "stable"),
            build_date=data.get("build_date")
        )

    def has_prebuilt_for_arch(self, arch: str) -> bool:
        if not self.binary_support or not self.prebuilt:
            return False
        return arch in self.prebuilt

    def get_prebuilt_info(self, arch: str) -> Optional[Dict]:
        if self.has_prebuilt_for_arch(arch):
            return self.prebuilt[arch]
        return None

    def is_binary_ready(self, arch: str) -> bool:
        return self.binary_support and self.has_prebuilt_for_arch(arch)

    @property
    def supported_archs(self) -> List[str]:
        return self.arch

    def __str__(self):
        status = " [BINARY]" if self.binary_support else ""
        return f"{self.name} v{self.version}{status} ({self.category})"
