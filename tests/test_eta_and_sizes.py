import importlib.util
import io
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
from _loader import load_store_common

sc = load_store_common()

_FI_PATH = Path(__file__).resolve().parent.parent / "termux_app_store" / "fast_install.py"
_spec = importlib.util.spec_from_file_location("tas_fast_install_eta_under_test", str(_FI_PATH))
fi = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = fi
_spec.loader.exec_module(fi)


@pytest.mark.parametrize(
    "value,expected",
    [
        (0, "0 B"),
        (1023, "1023 B"),
        (1536, "1.5 KB"),
        (5 * 1024 * 1024, "5.0 MB"),
        (3 * 1024**3, "3.0 GB"),
        ("abc", "Unknown"),
        (None, "Unknown"),
        (-5, "Unknown"),
    ],
)
def test_format_size(value, expected):
    assert sc.format_size(value) == expected


def test_rate_tracker_converges_on_steady_speed():
    tracker = sc.RateTracker()
    for i in range(1, 40):
        tracker.add(i * 100_000, now=i * 0.2)
    assert tracker.rate == pytest.approx(500_000, rel=0.05)
    assert tracker.remaining(10_000_000, 3_900_000, 1) == pytest.approx(12.2, rel=0.1)


def test_rate_tracker_adapts_when_speed_drops():
    tracker = sc.RateTracker()
    done = 0.0
    now = 0.0
    for _ in range(30):
        now += 0.2
        done += 100_000
        tracker.add(done, now)
    fast = tracker.rate
    for _ in range(60):
        now += 0.2
        done += 10_000
        tracker.add(done, now)
    assert tracker.rate < fast / 3


def test_rate_tracker_uses_fallback_before_samples():
    tracker = sc.RateTracker()
    assert tracker.remaining(1000, 0, fallback_rate=100) == 10
    assert tracker.remaining(1000, 0) == 0
    assert tracker.remaining(1000, 1000, fallback_rate=100) == 0


def test_speed_stats_roundtrip_and_smoothing(tmp_path):
    stats = sc.SpeedStats(tmp_path / "nested" / "speed.json")
    assert stats.get("download_bps", 123.0) == 123.0
    stats.update("download_bps", 1000)
    assert stats.get("download_bps", 0) == 1000
    stats.update("download_bps", 2000)
    assert 1000 < stats.get("download_bps", 0) < 2000


def test_speed_stats_ignores_bad_values_and_corrupt_file(tmp_path):
    path = tmp_path / "speed.json"
    stats = sc.SpeedStats(path)
    stats.update("k", 0)
    stats.update("k", -3)
    stats.update("k", "x")
    assert not path.exists()
    path.write_text("not json")
    assert stats.get("k", 7.0) == 7.0
    stats.update("k", 5)
    assert stats.get("k", 0) == 5


@pytest.fixture
def isolated(tmp_path, monkeypatch):
    monkeypatch.setattr(fi, "SPEED_STATS", sc.SpeedStats(tmp_path / "speed.json"))
    monkeypatch.setattr(fi, "SIZE_CACHE", tmp_path / "sizes.json")
    return tmp_path


def test_install_estimate_grows_with_size_and_learns(isolated):
    small = fi.estimate_install_seconds(1024 * 1024)
    large = fi.estimate_install_seconds(20 * 1024 * 1024)
    assert large > small >= fi.INSTALL_BASE_SECONDS
    fi._learn_install_speed(10 * 1024 * 1024, fi.INSTALL_BASE_SECONDS + 1.0)
    assert fi.SPEED_STATS.get("install_spm", 0) < fi.DEFAULT_INSTALL_SECONDS_PER_MB


def test_learn_install_speed_ignores_tiny_or_instant(isolated):
    fi._learn_install_speed(1000, 5.0)
    fi._learn_install_speed(10 * 1024 * 1024, 0.5)
    assert fi.SPEED_STATS.get("install_spm", -1) == -1


class _FakeResponse:
    def __init__(self, payload: bytes, clock, step: float):
        self._buf = io.BytesIO(payload)
        self.headers = {"Content-Length": str(len(payload))}
        self._clock = clock
        self._step = step

    def read(self, n):
        self._clock["t"] += self._step
        return self._buf.read(n)

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def test_download_reports_decreasing_eta_and_learns_speed(isolated, monkeypatch):
    clock = {"t": 100.0}
    payload = b"x" * (65536 * 40)
    monkeypatch.setattr(fi, "time", SimpleNamespace(monotonic=lambda: clock["t"], time=lambda: clock["t"]))
    monkeypatch.setattr(fi, "get_best_mirror", lambda force=False: fi.MIRRORS[0])
    monkeypatch.setattr(fi.urllib.request, "urlopen", lambda req, timeout=0: _FakeResponse(payload, clock, 0.25))

    etas = []
    pcts = []
    dest = isolated / "pkg_1.0_aarch64.deb"
    ok = fi.download_deb("pkg", "1.0", "aarch64", dest, progress_fn=pcts.append, eta_fn=etas.append)

    assert ok and dest.exists()
    assert pcts[-1] == 80
    mid = etas[len(etas) // 2]
    assert etas[1] > mid > etas[-2]
    assert fi.SPEED_STATS.get("download_bps", 0) == pytest.approx(65536 / 0.25, rel=0.05)


def test_install_deb_emits_estimate_then_zero(isolated, monkeypatch):
    deb = isolated / "pkg.deb"
    deb.write_bytes(b"x" * (4 * 1024 * 1024))

    class FakeProc:
        def __init__(self, *a, **k):
            self.stdout = io.BytesIO(b"Setting up pkg\n")
            self.returncode = 0

        def wait(self):
            return 0

    monkeypatch.setattr(fi.subprocess, "Popen", FakeProc)
    etas = []
    pcts = []
    assert fi.install_deb(deb, progress_fn=pcts.append, eta_fn=etas.append)
    assert etas[0] == pytest.approx(fi.estimate_install_seconds(deb.stat().st_size))
    assert etas[-1] == 0
    assert pcts[0] == 85 and pcts[-1] == 100


def test_remote_size_uses_cache_and_validates(isolated, monkeypatch):
    calls = []

    class Head:
        headers = {"Content-Length": "2048"}

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    def fake_urlopen(req, timeout=0):
        calls.append(req.full_url)
        return Head()

    monkeypatch.setattr(fi, "get_best_mirror", lambda force=False: fi.MIRRORS[0])
    monkeypatch.setattr(fi.urllib.request, "urlopen", fake_urlopen)
    assert fi.get_remote_deb_size("pkg", "1.0", "aarch64") == 2048
    assert fi.get_remote_deb_size("pkg", "1.0", "aarch64") == 2048
    assert len(calls) == 1
    assert fi.get_remote_deb_size("../bad", "1.0", "aarch64") is None


def test_remote_size_none_when_all_mirrors_fail(isolated, monkeypatch):
    def boom(req, timeout=0):
        raise OSError("down")

    monkeypatch.setattr(fi, "get_best_mirror", lambda force=False: fi.MIRRORS[0])
    monkeypatch.setattr(fi.urllib.request, "urlopen", boom)
    assert fi.get_remote_deb_size("pkg", "1.0", "aarch64") is None
