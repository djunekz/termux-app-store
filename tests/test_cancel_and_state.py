import importlib.util
import io
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest
from _loader import load_store_common

sc = load_store_common()

_FI_PATH = Path(__file__).resolve().parent.parent / "termux_app_store" / "fast_install.py"
_spec = importlib.util.spec_from_file_location("tas_fast_install_cancel_under_test", str(_FI_PATH))
fi = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = fi
_spec.loader.exec_module(fi)


def test_activity_log_keeps_newest_first_and_respects_limit(tmp_path):
    log = sc.ActivityLog(tmp_path / "h.json", limit=3)
    for i in range(5):
        log.add("install", f"p{i}", "1.0", "ok", i, now=1000.0 + i)
    names = [e["package"] for e in log.recent(10)]
    assert names == ["p4", "p3", "p2"]
    assert [e["package"] for e in log.recent(2)] == ["p4", "p3"]
    assert log.recent(0) == []


def test_activity_log_filters_by_package_and_returns_last(tmp_path):
    log = sc.ActivityLog(tmp_path / "h.json")
    log.add("install", "a", "1", "ok", now=1.0)
    log.add("install", "b", "1", "ok", now=2.0)
    log.add("update", "a", "2", "failed", 3.5, "boom", now=3.0)
    assert [e["action"] for e in log.recent(10, "a")] == ["update", "install"]
    last = log.last_for("a")
    assert last["result"] == "failed" and last["detail"] == "boom" and last["seconds"] == 3.5
    assert log.last_for("missing") is None


def test_activity_log_trims_detail_and_survives_corrupt_file(tmp_path):
    path = tmp_path / "h.json"
    log = sc.ActivityLog(path)
    path.write_text("not json")
    assert log.recent(5) == []
    log.add("install", "a", detail="x" * 5000)
    assert len(log.last_for("a")["detail"]) == 1500
    path.write_text('{"not": "a list"}')
    assert log.recent(5) == []


def test_settings_defaults_overrides_and_corruption(tmp_path):
    path = tmp_path / "s.json"
    settings = sc.Settings(path, {"notify": True})
    assert settings.get("notify") is True
    assert settings.get("missing", 5) == 5
    settings.set("notify", False)
    settings.set("sort", "status")
    assert settings.get("notify") is False and settings.get("sort") == "status"
    path.write_text("garbage")
    assert settings.get("notify") is True


def test_settings_write_failure_is_silent(tmp_path):
    blocker = tmp_path / "file"
    blocker.write_text("x")
    settings = sc.Settings(blocker / "sub" / "s.json")
    settings.set("a", 1)
    assert settings.get("a") is None


@pytest.mark.parametrize(
    "delta,expected",
    [
        (-5, "just now"),
        (10, "just now"),
        (120, "2m ago"),
        (7300, "2h ago"),
        (86400 * 3, "3d ago"),
        (86400 * 65, "2mo ago"),
    ],
)
def test_format_ago(delta, expected):
    assert sc.format_ago(1000.0, now=1000.0 + delta) == expected


def test_terminate_process_tree_kills_children_too():
    proc = subprocess.Popen(["bash", "-c", "sleep 60 & sleep 60; wait"], start_new_session=True)
    time.sleep(0.3)
    started = time.monotonic()
    sc.terminate_process_tree(proc, grace=3)
    assert proc.poll() is not None
    assert time.monotonic() - started < 4


def test_terminate_process_tree_on_finished_process_is_harmless():
    proc = subprocess.Popen(["true"], start_new_session=True)
    proc.wait()
    sc.terminate_process_tree(proc)


def test_terminate_without_new_session_never_kills_own_group():
    proc = subprocess.Popen(["sleep", "60"])
    sc.terminate_process_tree(proc, grace=3)
    assert proc.poll() is not None


def test_watch_cancel_stops_a_running_process():
    proc = subprocess.Popen(["sleep", "60"], start_new_session=True)
    cancel = threading.Event()
    thread = sc.watch_cancel(proc, cancel)
    time.sleep(0.2)
    assert proc.poll() is None
    cancel.set()
    thread.join(timeout=8)
    assert proc.poll() is not None


def test_watch_cancel_exits_when_process_finishes_on_its_own():
    proc = subprocess.Popen(["true"], start_new_session=True)
    thread = sc.watch_cancel(proc, threading.Event())
    thread.join(timeout=3)
    assert not thread.is_alive()


class _Response:
    def __init__(self, cancel, cancel_after):
        self._buf = io.BytesIO(b"x" * 65536 * 10)
        self.headers = {"Content-Length": str(65536 * 10)}
        self._cancel = cancel
        self._reads = 0
        self._after = cancel_after

    def read(self, n):
        self._reads += 1
        if self._reads == self._after:
            self._cancel.set()
        return self._buf.read(n)

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


@pytest.fixture
def isolated(tmp_path, monkeypatch):
    monkeypatch.setattr(fi, "SPEED_STATS", sc.SpeedStats(tmp_path / "speed.json"))
    monkeypatch.setattr(fi, "get_best_mirror", lambda force=False: fi.MIRRORS[0])
    return tmp_path


def test_download_stops_at_next_chunk_when_cancelled(isolated, monkeypatch):
    cancel = threading.Event()
    opened = []

    def fake_urlopen(req, timeout=0):
        opened.append(req.full_url)
        return _Response(cancel, cancel_after=2)

    monkeypatch.setattr(fi.urllib.request, "urlopen", fake_urlopen)
    logs = []
    dest = isolated / "pkg_1.0_aarch64.deb"
    assert fi.download_deb("pkg", "1.0", "aarch64", dest, log_fn=logs.append, cancel=cancel) is False
    assert len(opened) == 1
    assert not dest.exists() and not dest.with_suffix(".tmp").exists()
    assert "Download cancelled" in logs


def test_download_without_cancel_token_still_works(isolated, monkeypatch):
    monkeypatch.setattr(fi.urllib.request, "urlopen", lambda req, timeout=0: _Response(threading.Event(), 0))
    dest = isolated / "pkg_1.0_aarch64.deb"
    assert fi.download_deb("pkg", "1.0", "aarch64", dest) is True


def test_install_deb_refuses_to_start_when_already_cancelled(isolated, monkeypatch):
    deb = isolated / "pkg.deb"
    deb.write_bytes(b"x")
    cancel = threading.Event()
    cancel.set()

    def boom(*a, **k):
        raise AssertionError("dpkg must not start")

    monkeypatch.setattr(fi.subprocess, "Popen", boom)
    logs = []
    assert fi.install_deb(deb, log_fn=logs.append, cancel=cancel) is False
    assert any("cancelled" in line for line in logs)


def _prepare_fast_install(monkeypatch, tmp_path, download):
    monkeypatch.setattr(fi, "get_arch", lambda: "aarch64")
    monkeypatch.setattr(fi, "get_pkg_info", lambda name: {"version": "1.0", "sha256_by_arch": {"aarch64": "a" * 64}})
    monkeypatch.setattr(fi, "get_cached_deb", lambda *a, **k: None)
    monkeypatch.setattr(fi, "download_deb", download)
    built = []
    monkeypatch.setattr(fi, "_fallback_build_from_source", lambda *a, **k: built.append(k) or True)
    return built


def test_fast_install_cancelled_during_download_skips_source_build(tmp_path, monkeypatch):
    cancel = threading.Event()

    def download(**kwargs):
        cancel.set()
        return False

    built = _prepare_fast_install(monkeypatch, tmp_path, download)
    logs = []
    assert fi.fast_install("pkg", log_fn=logs.append, cancel=cancel) is False
    assert built == []
    assert any("cancelled" in line for line in logs)


def test_fast_install_failure_without_cancel_still_falls_back_to_source(tmp_path, monkeypatch):
    built = _prepare_fast_install(monkeypatch, tmp_path, lambda **kwargs: False)
    cancel = threading.Event()
    assert fi.fast_install("pkg", cancel=cancel) is True
    assert len(built) == 1 and built[0]["cancel"] is cancel


def test_fast_install_cancelled_before_missing_checksum_fallback(tmp_path, monkeypatch):
    built = _prepare_fast_install(monkeypatch, tmp_path, lambda **kwargs: False)
    monkeypatch.setattr(fi, "get_pkg_info", lambda name: {"version": "1.0"})
    monkeypatch.setattr(fi, "fetch_published_sha256", lambda *a, **k: "")
    cancel = threading.Event()
    cancel.set()
    assert fi.fast_install("pkg", cancel=cancel) is False
    assert built == []


def test_fallback_build_is_terminated_on_cancel(tmp_path, monkeypatch):
    script = tmp_path / "build-package.sh"
    script.write_text("#!/bin/bash\necho start\nsleep 60\n")
    monkeypatch.setattr(fi, "_get_app_root", lambda: tmp_path)
    monkeypatch.setattr(fi, "_ensure_recipe", lambda *a, **k: True)
    cancel = threading.Event()
    logs = []
    threading.Timer(0.8, cancel.set).start()
    started = time.monotonic()
    assert fi._fallback_build_from_source("pkg", log_fn=logs.append, cancel=cancel) is False
    assert time.monotonic() - started < 15
    assert "✗ Build cancelled" in logs
