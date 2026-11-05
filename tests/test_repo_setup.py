import hashlib
import os
import time

import pytest

from termux_app_store import repo_setup


def make_key(extra=b""):
    body = bytes([4]) + b"\x00\x00\x00\x01" + bytes([1]) + b"\x00\x08\xff" + extra
    packet = bytes([0x99]) + len(body).to_bytes(2, "big") + body
    fpr = hashlib.sha1(b"\x99" + len(body).to_bytes(2, "big") + body).hexdigest().upper()
    return packet, fpr


@pytest.fixture
def termux(tmp_path, monkeypatch):
    prefix = tmp_path / "com.termux" / "usr"
    (prefix / "etc/apt").mkdir(parents=True)
    monkeypatch.setenv("PREFIX", str(prefix))
    monkeypatch.delenv("TAS_NO_AUTO_REPO", raising=False)
    data, fpr = make_key()
    monkeypatch.setenv("TAS_KEY_FPR", fpr)
    monkeypatch.setattr(repo_setup, "_download_key", lambda timeout: data)
    return prefix


def test_ensure_repo_adds_signed_entry(termux):
    msgs = []
    assert repo_setup.ensure_repo(msgs.append) is True
    p = repo_setup.paths()
    line = open(p["sources_file"]).read().strip()
    assert line == f"deb [signed-by={p['keyring']}] {repo_setup.REPO_URL} termux main"
    assert "trusted=yes" not in line
    assert os.path.exists(p["keyring"])
    assert "pkg update" in msgs[0]


def test_ensure_repo_is_idempotent(termux):
    assert repo_setup.ensure_repo(lambda m: None) is True
    assert repo_setup.ensure_repo(lambda m: None) is False


def test_wrong_fingerprint_writes_nothing(termux, monkeypatch):
    monkeypatch.setenv("TAS_KEY_FPR", "0" * 40)
    assert repo_setup.ensure_repo(lambda m: None) is False
    assert not os.path.exists(repo_setup.paths()["sources_file"])
    assert not os.path.exists(repo_setup.paths()["keyring"])


def test_env_opt_out(termux, monkeypatch):
    monkeypatch.setenv("TAS_NO_AUTO_REPO", "1")
    assert repo_setup.ensure_repo(lambda m: None) is False
    assert not os.path.exists(repo_setup.paths()["sources_file"])


def test_remove_repo_disables_auto_readd(termux):
    repo_setup.ensure_repo(lambda m: None)
    assert len(repo_setup.remove_repo()) == 2
    assert repo_setup.ensure_repo(lambda m: None) is False
    ok, _ = repo_setup.add_repo()
    assert ok and repo_setup.repo_is_configured()


def test_legacy_trusted_yes_entry_is_replaced(termux):
    p = repo_setup.paths()
    os.makedirs(p["sources_dir"])
    open(p["sources_file"], "w").write(f"deb [trusted=yes] {repo_setup.REPO_URL} termux main\n")
    assert repo_setup.ensure_repo(lambda m: None) is True
    assert "trusted=yes" not in open(p["sources_file"]).read()


def test_download_failure_never_raises_and_backs_off(termux, monkeypatch):
    calls = []

    def boom(timeout):
        calls.append(1)
        raise OSError("offline")

    monkeypatch.setattr(repo_setup, "_download_key", boom)
    assert repo_setup.ensure_repo(lambda m: None) is False
    assert repo_setup.ensure_repo(lambda m: None) is False
    assert len(calls) == 1
    old = time.time() - repo_setup.RETRY_AFTER_SECONDS - 10
    os.utime(repo_setup.paths()["retry"], (old, old))
    repo_setup.ensure_repo(lambda m: None)
    assert len(calls) == 2


def test_not_termux_is_noop(tmp_path, monkeypatch):
    monkeypatch.setenv("PREFIX", str(tmp_path / "usr"))
    assert repo_setup.ensure_repo(lambda m: None) is False
