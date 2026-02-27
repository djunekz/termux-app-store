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


# ── Tests for conftest helpers ────────────────────────────────────────────────

class TestMakeBuildSh:

    def test_creates_pkg_dir(self, tmp_path):
        pkg_dir = make_build_sh(tmp_path, "mypkg", {})
        assert pkg_dir.exists()
        assert pkg_dir == tmp_path / "packages" / "mypkg"

    def test_creates_build_sh(self, tmp_path):
        make_build_sh(tmp_path, "mypkg", {"TERMUX_PKG_VERSION": "1.0.0"})
        build_sh = tmp_path / "packages" / "mypkg" / "build.sh"
        assert build_sh.exists()

    def test_fields_written_to_build_sh(self, tmp_path):
        make_build_sh(tmp_path, "mypkg", {
            "TERMUX_PKG_VERSION": "2.0.0",
            "TERMUX_PKG_DESCRIPTION": "A cool tool",
        })
        content = (tmp_path / "packages" / "mypkg" / "build.sh").read_text()
        assert 'TERMUX_PKG_VERSION="2.0.0"' in content
        assert 'TERMUX_PKG_DESCRIPTION="A cool tool"' in content

    def test_empty_fields(self, tmp_path):
        pkg_dir = make_build_sh(tmp_path, "emptypkg", {})
        content = (pkg_dir / "build.sh").read_text()
        assert content == "\n"

    def test_nested_pkg_name(self, tmp_path):
        pkg_dir = make_build_sh(tmp_path, "nested/pkg", {})
        assert pkg_dir.exists()

    def test_idempotent(self, tmp_path):
        make_build_sh(tmp_path, "mypkg", {"TERMUX_PKG_VERSION": "1.0.0"})
        make_build_sh(tmp_path, "mypkg", {"TERMUX_PKG_VERSION": "2.0.0"})
        content = (tmp_path / "packages" / "mypkg" / "build.sh").read_text()
        assert 'TERMUX_PKG_VERSION="2.0.0"' in content


class TestMakeValidRoot:

    def test_creates_packages_dir(self, tmp_path):
        make_valid_root(tmp_path)
        assert (tmp_path / "packages").exists()

    def test_creates_build_package_sh(self, tmp_path):
        make_valid_root(tmp_path)
        assert (tmp_path / "build-package.sh").exists()

    def test_with_fingerprint(self, tmp_path):
        make_valid_root(tmp_path, with_fingerprint=True)
        content = (tmp_path / "build-package.sh").read_text()
        assert "# Termux App Store Official" in content

    def test_without_fingerprint(self, tmp_path):
        make_valid_root(tmp_path, with_fingerprint=False)
        content = (tmp_path / "build-package.sh").read_text()
        assert "# other script" in content
        assert "# Termux App Store Official" not in content

    def test_returns_root(self, tmp_path):
        result = make_valid_root(tmp_path)
        assert result == tmp_path

    def test_idempotent(self, tmp_path):
        make_valid_root(tmp_path)
        make_valid_root(tmp_path)
        assert (tmp_path / "packages").exists()


class TestFixtures:

    def test_tmp_root_fixture(self, tmp_root):
        assert (tmp_root / "packages").exists()
        assert (tmp_root / "build-package.sh").exists()

    def test_pkg_factory_fixture(self, pkg_factory):
        root, make = pkg_factory
        pkg_dir = make("bower", TERMUX_PKG_VERSION="1.8.12")
        assert pkg_dir.exists()
        content = (pkg_dir / "build.sh").read_text()
        assert 'TERMUX_PKG_VERSION="1.8.12"' in content

    def test_pkg_factory_multiple_packages(self, pkg_factory):
        root, make = pkg_factory
        make("bower", TERMUX_PKG_VERSION="1.8.12")
        make("pnpm", TERMUX_PKG_VERSION="10.30.1")
        assert (root / "packages" / "bower").exists()
        assert (root / "packages" / "pnpm").exists()
