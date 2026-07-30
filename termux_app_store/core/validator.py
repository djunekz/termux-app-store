import json
from pathlib import Path
from typing import Dict, List, Tuple

import logging

logger = logging.getLogger(__name__)


class PackageValidator:

    REQUIRED_FIELDS = ["name", "version", "maintainer", "source"]

    def validate(self, index_path: Path) -> Tuple[bool, List[str]]:
        errors = []

        try:
            with open(index_path, "r", encoding="utf-8") as f:
                data: Dict = json.load(f)
        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON format: {e}")
            return False, errors
        except Exception as e:
            errors.append(f"Failed to read file: {e}")
            return False, errors

        for field in self.REQUIRED_FIELDS:
            if field not in data or not str(data[field]).strip():
                errors.append(f"Required field '{field}' is missing or empty")

        version = data.get("version", "")
        if version and not version[0].isdigit():
            errors.append("TERMUX_PKG_VERSION must start with a digit (e.g., 1.0.0)")

        binary_support = data.get("binary_support", False)
        prebuilt = data.get("prebuilt", {})

        if binary_support:
            if not prebuilt:
                errors.append("binary_support=True but 'prebuilt' section is empty or missing")

            archs = data.get("arch", ["aarch64"])
            for arch in archs:
                if arch in prebuilt:
                    info = prebuilt[arch]
                    if not isinstance(info, dict):
                        errors.append(f"prebuilt.{arch} must be an object")
                        continue

                    if "sha256" not in info or len(info.get("sha256", "")) != 64:
                        errors.append(f"prebuilt.{arch}.sha256 must be a valid SHA256 hash (64 characters)")

                    if "size" not in info:
                        errors.append(f"prebuilt.{arch}.size is required")
                else:
                    logger.warning(f"Binary support enabled but prebuilt info for {arch} is missing")

        source = data.get("source", {})
        if "url" not in source or not source.get("url"):
            errors.append("source.url is required")
        source_sha256 = source.get("sha256", "")
        if source_sha256 != "SKIP" and not source_sha256:
            errors.append("source.sha256 is required (use SKIP if trusted)")

        if "dependencies" in data and not isinstance(data["dependencies"], list):
            errors.append("dependencies must be an array/list")

        if errors:
            logger.error(f"Validation failed for {index_path.name}: {len(errors)} error(s)")
            return False, errors

        logger.info(f"✅ {index_path.name} is valid")
        return True, []


async def validate_package(package_dir: Path) -> bool:
    index_file = package_dir / "index.json"

    if not index_file.exists():
        logger.error(f"index.json not found in {package_dir}")
        return False

    validator = PackageValidator()
    success, errors = validator.validate(index_file)

    if success:
        print(f"✓ Package valid: {package_dir.name}")
        return True
    else:
        print(f"✗ Package invalid: {package_dir.name}")
        for err in errors:
            print(f"   • {err}")
        return False
