import pytest
from pathlib import Path


def make_build_sh(root: Path, pkg_name: str, fields: dict) -> Path:
    pkg_dir = root / "packages" / pkg_name
    pkg_dir.mkdir(parents=True, exist_ok=True)
    lines = []
    for key, val in fields.items():
        lines.append(f'{key}="{val}"')
    (pkg_dir / "build.sh").write_text("\n".join(lines) + "\n")
    return pkg_dir


def make_valid_root(root: Path, with_fingerprint: bool = True) -> Path:
    (root / "packages").mkdir(parents=True, exist_ok=True)
    fingerprint = "# Termux App Store Official" if with_fingerprint else "# other script"
    (root / "build-package.sh").write_text(fingerprint + "\nset -euo pipefail\n")
    return root


@pytest.fixture
def tmp_root(tmp_path):
    return make_valid_root(tmp_path)


@pytest.fixture
def pkg_factory(tmp_path):
    make_valid_root(tmp_path)

    def _make(name, **fields):
        return make_build_sh(tmp_path, name, fields)

    return tmp_path, _make
