import asyncio
import contextlib
import stat
from unittest.mock import patch

import pytest

pytest.importorskip("textual")

import termux_app_store.termux_app_store as tui

PACKAGES = [
    {
        "package": "aaa",
        "version": "1.0",
        "description": "first",
        "maintainer": "m",
        "license": "MIT",
        "download_size": "Unknown",
        "depends": [],
    },
    {
        "package": "bbb",
        "version": "2.0",
        "description": "second",
        "maintainer": "m",
        "license": "GPL-3.0",
        "download_size": "1.5 MB",
        "depends": ["x"],
    },
    {
        "package": "ccc",
        "version": "3.0",
        "description": "third",
        "maintainer": "m",
        "license": "Apache-2.0",
        "download_size": "Unknown",
        "depends": [],
    },
]
INSTALLED = {"aaa": None, "bbb": "2.0", "ccc": "2.0"}


def _run(coro_fn, executables=("bbb", "bbb-extra")):
    async def main():
        with (
            patch.object(tui, "get_packages", lambda *a, **k: [tui.normalize_pkg(p) for p in PACKAGES]),
            patch.object(tui, "fetch_index_from_github", lambda: []),
            patch.object(tui, "get_installed_version", lambda n: INSTALLED[n]),
            patch.object(tui, "get_remote_deb_size", lambda n, v, a: 123456 if n == "aaa" else None),
            patch.object(tui, "get_package_executables", lambda n: list(executables)),
        ):
            app = tui.TermuxAppStore()
            async with app.run_test(size=(120, 40)) as pilot:
                await pilot.pause(0.5)
                return await coro_fn(app, pilot)

    return asyncio.run(main())


def _info(app):
    return str(app.info.content)


def test_primary_button_label_follows_status():
    async def scenario(app, pilot):
        labels = {}
        for index, name in enumerate(["aaa", "bbb", "ccc"]):
            app.list_view.index = index
            await pilot.pause(0.4)
            labels[name] = (str(app.install_btn.label), str(app.install_btn.variant))
        return labels

    labels = _run(scenario)
    assert labels["aaa"] == ("Install", "primary")
    assert labels["bbb"] == ("Open", "success")
    assert labels["ccc"] == ("Update", "warning")


def test_detail_panel_shows_license_and_size():
    async def scenario(app, pilot):
        app.list_view.index = 1
        await pilot.pause(0.4)
        known = _info(app)
        app.list_view.index = 0
        await pilot.pause(0.8)
        looked_up = _info(app)
        app.list_view.index = 2
        await pilot.pause(0.8)
        unknown = _info(app)
        return known, looked_up, unknown

    known, looked_up, unknown = _run(scenario)
    assert "License    : GPL-3.0" in known
    assert "Size       : 1.5 MB" in known
    assert "License    : MIT" in looked_up
    assert "Size       : 120.6 KB" in looked_up
    assert "Size       : Unknown" in unknown


def test_open_dialog_does_not_leak_typing_into_search():
    async def scenario(app, pilot):
        app.list_view.index = 1
        await pilot.pause(0.4)
        await pilot.click("#install")
        await pilot.pause(0.8)
        opened = type(app.screen).__name__
        await pilot.press("a", "b", "c")
        await pilot.pause(0.2)
        query = app.search_query
        count = len(app.list_view.children)
        await pilot.press("escape")
        await pilot.pause(0.3)
        return opened, query, count, type(app.screen).__name__

    opened, query, count, after = _run(scenario)
    assert opened == "RunScreen"
    assert query == ""
    assert count == 3
    assert after != "RunScreen"


def test_open_without_executables_shows_message():
    async def scenario(app, pilot):
        app.list_view.index = 1
        await pilot.pause(0.4)
        await pilot.click("#install")
        await pilot.pause(0.5)
        return type(app.screen).__name__, str(app.status_bar.content)

    screen, status = _run(scenario, executables=())
    assert screen != "RunScreen"
    assert "no command" in status


def test_run_external_invokes_command_with_args():
    async def scenario(app, pilot):
        calls = []
        with (
            patch.object(tui.TermuxAppStore, "suspend", lambda self: contextlib.nullcontext()),
            patch.object(tui.subprocess, "call", lambda argv: calls.append(argv) or 0),
            patch("builtins.input", lambda: ""),
        ):
            app.run_external("bbb", "--flag 'two words'")
            await pilot.pause(0.3)
        return calls, str(app.status_bar.content)

    calls, status = _run(scenario)
    assert calls == [["bbb", "--flag", "two words"]]
    assert "exited with code 0" in status


def test_run_external_rejects_unbalanced_quotes():
    async def scenario(app, pilot):
        app.run_external("bbb", "'oops")
        await pilot.pause(0.2)
        return str(app.status_bar.content)

    assert "Invalid arguments" in _run(scenario)


def test_get_package_executables_prefers_package_name(tmp_path, monkeypatch):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    for name in ("zzz", "tool", "aaa"):
        path = bin_dir / name
        path.write_text("#!/bin/sh\n")
        path.chmod(path.stat().st_mode | stat.S_IXUSR)
    (bin_dir / "notexec").write_text("data")
    listing = "\n".join(
        [str(tmp_path), str(bin_dir)] + [str(bin_dir / n) for n in ("zzz", "tool", "aaa", "notexec")] + ["/usr/share/x"]
    )
    monkeypatch.setenv("PREFIX", str(tmp_path))
    monkeypatch.setattr(tui.subprocess, "check_output", lambda *a, **k: listing)
    assert tui.get_package_executables("tool") == ["tool", "aaa", "zzz"]
    assert tui.get_package_executables("other") == ["aaa", "tool", "zzz"]


def test_get_package_executables_handles_missing_dpkg(monkeypatch):
    def boom(*a, **k):
        raise FileNotFoundError

    monkeypatch.setattr(tui.subprocess, "check_output", boom)
    assert tui.get_package_executables("x") == []


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("Unknown", None),
        ("-", None),
        ("", None),
        (None, None),
        ("1.5 MB", "1.5 MB"),
        (2048, "2.0 KB"),
        (0, None),
    ],
)
def test_size_text_from_index(raw, expected):
    assert tui.size_text_from_index({"download_size": raw}) == expected


def test_normalize_pkg_carries_license_size_and_homepage():
    result = tui.normalize_pkg(
        {"package": "p", "version": "1", "license": "MIT", "download_size": "2 MB", "homepage": "https://x"}
    )
    assert result["license"] == "MIT"
    assert result["download_size"] == "2 MB"
    assert result["homepage"] == "https://x"
    bare = tui.normalize_pkg({"package": "p", "version": "1"})
    assert bare["license"] == "-" and bare["download_size"] == "-" and "homepage" not in bare


def test_progress_bar_estimates_eta_from_percent_rate():
    bar = tui.SimpleProgressBar(total=100)
    bar._samples = [(0.0, 10.0), (10.0, 30.0)]
    assert bar._estimate_from_samples(10.0) == pytest.approx(35.0)
    bar._samples = [(0.0, 10.0), (1.0, 30.0)]
    assert bar._estimate_from_samples(1.0) == 0.0
    bar._samples = [(0.0, 10.0), (10.0, 10.5)]
    assert bar._estimate_from_samples(10.0) == 0.0
    bar._samples = [(0.0, 10.0), (10.0, 100.0)]
    assert bar._estimate_from_samples(10.0) == 0.0
