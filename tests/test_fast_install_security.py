import hashlib
import time

import pytest

from termux_app_store import fast_install as fi


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
    import os
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
    monkeypatch.setattr(fi.urllib.request, "urlopen", lambda *a, **k: Resp())
    monkeypatch.delenv("TERMUX_APP_STORE_BUILD_SH_SHA256", raising=False)
    monkeypatch.delenv("TERMUX_APP_STORE_ALLOW_UNVERIFIED_BUILD_SH", raising=False)
    assert fi._fallback_build_from_source("pkg") is False
    assert not (tmp_path / "build-package.sh").exists()
