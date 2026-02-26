#!/usr/bin/env python3
"""tools/build.py

Generate tools/index.json for Termux App Store.

The index is consumed by the app in **remote mode** (offline-first with cache).
It is intentionally simple JSON so it can be fetched via raw.githubusercontent.
"""

import os
import re
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional
import subprocess

class BuildShParser:

    def __init__(self, build_sh_path: str):
        self.path = build_sh_path
        self.content = self._read_file()

    def _read_file(self) -> str:
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"[ERROR] Gagal membaca {self.path}: {e}")
            return ""

    def _extract_var(self, var_name: str) -> Optional[str]:
        patterns = [
            rf'{var_name}="([^"]*)"',
            rf"{var_name}='([^']*)'",
            rf'{var_name}=([^\s\n]+)'
        ]

        for pattern in patterns:
            match = re.search(pattern, self.content)
            if match:
                return match.group(1).strip()
        return None

    def parse(self) -> Dict:
        data = {
            'homepage': self._extract_var('TERMUX_PKG_HOMEPAGE') or '',
            'description': self._extract_var('TERMUX_PKG_DESCRIPTION') or '',
            'license': self._extract_var('TERMUX_PKG_LICENSE') or '',
            'maintainer': self._extract_var('TERMUX_PKG_MAINTAINER') or '',
            'version': self._extract_var('TERMUX_PKG_VERSION') or '',
            'srcurl': self._extract_var('TERMUX_PKG_SRCURL') or '',
            'sha256': self._extract_var('TERMUX_PKG_SHA256') or '',
            'depends': self._parse_depends(),
            'platform_independent': (self._extract_var('TERMUX_PKG_PLATFORM_INDEPENDENT') or '').lower() == 'true',
            # Optional metadata (safe to omit)
            'category': self._extract_var('TERMUX_PKG_CATEGORY') or '',
            'tags': self._parse_csv(self._extract_var('TERMUX_PKG_TAGS')),
        }
        return data

    def _parse_csv(self, value: Optional[str]) -> List[str]:
        if not value:
            return []
        return [x.strip() for x in value.split(',') if x.strip()]

    def _parse_depends(self) -> List[str]:
        depends_str = self._extract_var('TERMUX_PKG_DEPENDS')
        if not depends_str:
            return []

        deps = [dep.strip() for dep in depends_str.split(',')]
        return [dep for dep in deps if dep]


class PackageIndexGenerator:

    def __init__(self, packages_dir: str = "packages", output_file: str = "tools/index.json"):
        self.packages_dir = Path(packages_dir)
        self.output_file = Path(output_file)
        self.repo_source = "https://github.com/djunekz/termux-app-store"

    def _get_package_dirs(self) -> List[Path]:
        if not self.packages_dir.exists():
            print(f"[ERROR] Directory {self.packages_dir} tidak ditemukan!")
            return []

        package_dirs = []
        for item in self.packages_dir.iterdir():
            if item.is_dir() and (item / "build.sh").exists():
                package_dirs.append(item)

        return sorted(package_dirs)

    def _estimate_download_size(self, srcurl: str) -> str:
        return "Unknown"

    def _estimate_installed_size(self, package_name: str) -> str:
        return "Unknown"

    def _create_package_entry(self, package_dir: Path) -> Dict:
        package_name = package_dir.name
        build_sh_path = package_dir / "build.sh"

        print(f"[*] Processing: {package_name}")

        parser = BuildShParser(str(build_sh_path))
        metadata = parser.parse()

        entry = {
            "package": package_name,
            "name": package_name,
            "version": metadata['version'],
            "maintainer": metadata['maintainer'],
            "desc": metadata['description'],
            "description": metadata['description'],
            "homepage": metadata['homepage'],
            "license": metadata['license'],
            "download_size": self._estimate_download_size(metadata['srcurl']),
            "installed_size": self._estimate_installed_size(package_name),
            "source": self.repo_source,
            "srcurl": metadata['srcurl'],
            "sha256": metadata['sha256'],
            "platform_independent": metadata['platform_independent'],
            "category": metadata.get('category') or "",
            "tags": metadata.get('tags') or [],
        }

        if metadata['depends']:
            entry['depends'] = metadata['depends']

        return entry

    def generate(self) -> Dict:
        print("[*] Scanning packages directory...")
        package_dirs = self._get_package_dirs()

        if not package_dirs:
            print("[WARNING] Tidak ada package ditemukan!")
            return {"packages": [], "total": 0}

        print(f"[*] Found {len(package_dirs)} packages")

        packages = []
        for pkg_dir in package_dirs:
            try:
                entry = self._create_package_entry(pkg_dir)
                packages.append(entry)
            except Exception as e:
                print(f"[ERROR] Failed to process {pkg_dir.name}: {e}")
                continue

        packages.sort(key=lambda x: x['package'])

        index_data = {
            "version": "1.0",
            "repository": self.repo_source,
            "generated_at": self._get_timestamp(),
            "total": len(packages),
            "packages": packages
        }

        return index_data

    def _get_timestamp(self) -> str:
        from datetime import datetime, timezone
        return datetime.now(timezone.utc).isoformat()

    def save(self, data: Dict):
        self.output_file.parent.mkdir(parents=True, exist_ok=True)

        print(f"[*] Writing to {self.output_file}...")
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"[✔] index.json generated successfully!")
        print(f"    Total packages: {data['total']}")
        print(f"    Output: {self.output_file}")

    def run(self):
        print("=" * 60)
        print("termux-app-store Index Generator")
        print("=" * 60)

        data = self.generate()
        self.save(data)

        print("\n[✔] Done!")


def main():
    if Path("packages").exists():
        packages_dir = "packages"
        output_file = "tools/index.json"
    elif Path("../packages").exists():
        packages_dir = "../packages"
        output_file = "index.json"
    else:
        print("[ERROR] Cannot find packages directory!")
        print("Please run this script from project root or tools/ directory")
        return 1
    generator = PackageIndexGenerator(packages_dir, output_file)
    generator.run()
    return 0


if __name__ == "__main__":
    exit(main())
