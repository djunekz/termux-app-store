import hashlib
import importlib.util
import os
import sys
import time
from pathlib import Path

import pytest

_FI_PATH = Path(__file__).resolve().parent.parent / "termux_app_store" / "fast_install.py"
_spec = importlib.util.spec_from_file_location("tas_fast_install_under_test", str(_FI_PATH))
fi = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = fi
_spec.loader.exec_module(fi)


@pytest.fixture
def cache(tmp_path, monkeypatch):
    monkeypatch.setattr(fi, "DEB_CACHE_DIR", tmp_path)
    return tmp_path


def _write(cache, data=b"deb-bytes"):
    path = cache / "pkg_1.0_aarch64.deb"
    path.write_bytes(data)
    return path, hashlib.sha256(data).hexdigest()


def test_cache_without_checksum_is_rejected(cache):
    _write(cache)
    assert fi.get_cached_deb("pkg", "1.0", "aarch64", sha256=None) is None
    assert fi.get_cached_deb("pkg", "1.0", "aarch64", sha256="") is None


def test_cache_with_wrong_checksum_is_deleted(cache):
    path, _ = _write(cache)
    assert fi.get_cached_deb("pkg", "1.0", "aarch64", sha256="0" * 64) is None
    assert not path.exists()


def test_cache_with_valid_checksum_is_returned(cache):
    path, digest = _write(cache)
    assert fi.get_cached_deb("pkg", "1.0", "aarch64", sha256=digest) == path


def test_expired_cache_is_removed(cache):
    path, digest = _write(cache)
    old = time.time() - fi.DEB_TTL - 10
    os.utime(path, (old, old))
    assert fi.get_cached_deb("pkg", "1.0", "aarch64", sha256=digest) is None
    assert not path.exists()


@pytest.mark.parametrize("pkg,ver,arch", [
    ("../x", "1.0", "aarch64"),
    ("pkg", "1.0/../../x", "aarch64"),
    ("pkg", "1.0", "a b"),
    ("", "1.0", "aarch64"),
])
def test_invalid_identifiers_rejected(cache, pkg, ver, arch):
    assert fi.get_cached_deb(pkg, ver, arch, sha256="0" * 64) is None
    assert not fi._valid_ident(pkg, ver, arch)


def test_malformed_index_rejected():
    assert not fi._valid_index([])
    assert not fi._valid_index({"packages": "x"})
    assert not fi._valid_index({"packages": [{"package": "../evil"}]})
    assert fi._valid_index({"packages": [{"package": "ok-pkg"}]})


def test_fast_install_refuses_without_trusted_checksum(monkeypatch, cache):
    monkeypatch.setattr(fi, "get_arch", lambda: "aarch64")
    monkeypatch.setattr(fi, "get_pkg_info", lambda name: {"package": "pkg", "version": "1.0"})
    monkeypatch.setattr(fi, "fetch_published_sha256", lambda *a, **k: "")
    called = {}
    monkeypatch.setattr(fi, "download_deb", lambda **k: called.setdefault("dl", True))
    monkeypatch.setattr(fi, "_fallback_build_from_source", lambda *a, **k: "fallback")
    assert fi.fast_install("pkg") == "fallback"
    assert "dl" not in called


def test_unpinned_build_script_refused(monkeypatch, tmp_path):
    class Resp:
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def read(self): return b"echo hi\n"
    monkeypatch.setattr(fi, "_get_app_root", lambda: tmp_path)
    monkeypatch.setattr(fi, "_packaged_build_script", lambda: None)
    monkeypatch.setattr(fi.urllib.request, "urlopen", lambda *a, **k: Resp())
    monkeypatch.delenv("TERMUX_APP_STORE_BUILD_SH_SHA256", raising=False)
    monkeypatch.delenv("TERMUX_APP_STORE_ALLOW_UNVERIFIED_BUILD_SH", raising=False)
    assert fi._fallback_build_from_source("pkg") is False
    assert not (tmp_path / "build-package.sh").exists()


ROOT = Path(__file__).resolve().parent.parent


def test_packaged_build_script_matches_repo_script():
    packaged = ROOT / "termux_app_store" / "data" / "build-package.sh"
    assert packaged.is_file()
    assert packaged.read_bytes() == (ROOT / "build-package.sh").read_bytes()


def test_packaged_build_script_is_declared_for_the_wheel():
    assert "data/build-package.sh" in (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert "build-package.sh" in (ROOT / "MANIFEST.in").read_text(encoding="utf-8")


class _Stdout:
    def readline(self):
        return b""


class _Proc:
    returncode = 0

    def __init__(self, *a, **k):
        self.stdout = _Stdout()

    def wait(self):
        return 0


def test_fallback_uses_packaged_script_without_network(monkeypatch, tmp_path):
    monkeypatch.setattr(fi, "_get_app_root", lambda: tmp_path)
    monkeypatch.setattr(fi, "_ensure_recipe", lambda *a, **k: True)
    monkeypatch.setattr(fi.subprocess, "Popen", _Proc)

    def no_network(*a, **k):
        raise AssertionError("network must not be used")

    monkeypatch.setattr(fi.urllib.request, "urlopen", no_network)
    monkeypatch.delenv("TERMUX_APP_STORE_BUILD_SH_SHA256", raising=False)
    monkeypatch.delenv("TERMUX_APP_STORE_ALLOW_UNVERIFIED_BUILD_SH", raising=False)
    assert fi._fallback_build_from_source("pkg") is True
    assert (tmp_path / "build-package.sh").read_bytes() == (ROOT / "build-package.sh").read_bytes()


def _recipe_env(monkeypatch, tmp_path, body, recipe_sha):
    class Resp:
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def read(self): return body
    monkeypatch.setattr(fi.urllib.request, "urlopen", lambda *a, **k: Resp())
    monkeypatch.setattr(fi, "get_pkg_info", lambda name: {"package": name, "recipe_sha256": recipe_sha})


def test_recipe_downloaded_only_when_it_matches_index_checksum(monkeypatch, tmp_path):
    body = b"TERMUX_PKG_VERSION=1\n"
    _recipe_env(monkeypatch, tmp_path, body, hashlib.sha256(body).hexdigest())
    assert fi._ensure_recipe("pkg", tmp_path, lambda m: None) is True
    assert (tmp_path / "packages" / "pkg" / "build.sh").read_bytes() == body


def test_recipe_with_wrong_checksum_is_refused(monkeypatch, tmp_path):
    _recipe_env(monkeypatch, tmp_path, b"evil\n", "0" * 64)
    assert fi._ensure_recipe("pkg", tmp_path, lambda m: None) is False
    assert not (tmp_path / "packages" / "pkg" / "build.sh").exists()


def test_recipe_without_index_checksum_is_refused(monkeypatch, tmp_path):
    _recipe_env(monkeypatch, tmp_path, b"x\n", "")
    assert fi._ensure_recipe("pkg", tmp_path, lambda m: None) is False


def test_index_entries_carry_recipe_checksum(tmp_path):
    spec = importlib.util.spec_from_file_location("tas_build_under_test", str(ROOT / "tools" / "build.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    pkg = tmp_path / "packages" / "demo"
    pkg.mkdir(parents=True)
    recipe = (
        "TERMUX_PKG_HOMEPAGE=https://example.com\n"
        "TERMUX_PKG_DESCRIPTION=\"d\"\n"
        "TERMUX_PKG_LICENSE=\"MIT\"\n"
        "TERMUX_PKG_MAINTAINER=\"@m\"\n"
        "TERMUX_PKG_VERSION=1.0\n"
        "TERMUX_PKG_SRCURL=https://example.com/a.tar.gz\n"
        "TERMUX_PKG_SHA256=" + "a" * 64 + "\n"
    )
    (pkg / "build.sh").write_text(recipe, encoding="utf-8")
    generator = mod.PackageIndexGenerator(str(tmp_path / "packages"), str(tmp_path / "index.json"))
    entry = generator._create_package_entry(pkg)
    assert entry["recipe_sha256"] == hashlib.sha256(recipe.encode()).hexdigest()


def test_build_workflow_uses_full_checksums_and_fails_closed():
    text = (ROOT / ".github" / "workflows" / "build-packages-debs.yml").read_text(encoding="utf-8")
    assert "cut -c1-16 ||" not in text
    assert '"$GOTSUM" == "$SHA256"*' not in text
    assert "source \"$BUILD_SH\" 2>/dev/null || true" not in text
    assert "termux_step_make_install) || true" not in text
    assert "if-no-files-found: error" in text
    assert "matrix.recipe" in text
