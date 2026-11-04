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


@pytest.fixture(autouse=True)
def isolated_state(tmp_path, monkeypatch):
    monkeypatch.setattr(tui, "ACTIVITY", tui._store.ActivityLog(tmp_path / "history.json"))
    monkeypatch.setattr(tui, "SETTINGS", tui._store.Settings(tmp_path / "settings.json", dict(tui.SETTINGS.defaults)))
    monkeypatch.setattr(tui, "NOTIFY_MIN_SECONDS", 1000)


def _installed_map(installed=None):
    source = INSTALLED if installed is None else installed
    return {name: version for name, version in source.items() if version}


def _run(coro_fn, executables=("bbb", "bbb-extra"), installed=None):
    async def main():
        with (
            patch.object(tui, "get_packages", lambda *a, **k: [tui.normalize_pkg(p) for p in PACKAGES]),
            patch.object(tui, "fetch_index_from_github", lambda: []),
            patch.object(tui, "get_installed_version", lambda n: (INSTALLED if installed is None else installed)[n]),
            patch.object(tui, "get_installed_versions", lambda: _installed_map(installed)),
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


def _names(app):
    return [child.pkg["name"] for child in app.list_view.children]


def test_update_banner_lists_outdated_packages():
    async def scenario(app, pilot):
        return app.banner.display, str(app.banner_text.content)

    shown, text = _run(scenario)
    assert shown is True
    assert "1 update available: ccc" in text


def test_update_banner_hidden_when_everything_is_current():
    async def scenario(app, pilot):
        return app.banner.display

    assert _run(scenario, installed={"aaa": None, "bbb": "2.0", "ccc": "3.0"}) is False


def test_banner_upgrade_all_queues_each_outdated_package_once():
    async def noop(self):
        return None

    async def scenario(app, pilot):
        await pilot.click("#banner-upgrade")
        await pilot.pause(0.3)
        await pilot.click("#banner-upgrade")
        await pilot.pause(0.3)
        queued = []
        while not app.worker_queue.empty():
            queued.append(app.worker_queue.get_nowait())
        return queued

    with patch.object(tui.TermuxAppStore, "consume_worker_queue", noop):
        assert _run(scenario) == [("install", "ccc")]


def test_search_with_no_match_shows_message_and_recovers():
    async def scenario(app, pilot):
        app.search_input.focus()
        await pilot.press("z", "z", "z")
        await pilot.pause(0.5)
        empty = (_names(app), str(app.info.content))
        for _ in range(3):
            await pilot.press("backspace")
        await pilot.pause(0.5)
        return empty, _names(app)

    empty, later = _run(scenario)
    assert empty[0] == []
    assert "No packages match" in empty[1]
    assert later == ["aaa", "bbb", "ccc"]


def test_search_keeps_working_while_banner_is_visible():
    async def scenario(app, pilot):
        app.search_input.focus()
        await pilot.press("c", "c")
        await pilot.pause(0.4)
        return _names(app), app.banner.display

    assert _run(scenario) == (["ccc"], True)


def test_show_installed_lists_only_installed_and_refresh_restores_all():
    async def scenario(app, pilot):
        app.action_show_installed()
        await pilot.pause(0.5)
        installed_only = _names(app)
        app.action_refresh()
        await pilot.pause(0.5)
        return installed_only, _names(app)

    assert _run(scenario) == (["bbb", "ccc"], ["aaa", "bbb", "ccc"])


def _fake_installer(result, wait_for_cancel=False, log="downloading"):
    def fake(name, log_fn, progress_fn, eta_fn, cancel=None):
        log_fn(log)
        if wait_for_cancel:
            cancel.wait(5)
        return result

    return fake


def test_cancel_button_stops_install_and_skips_source_build():
    built = []

    async def scenario(app, pilot):
        app.worker_queue.put_nowait(("install", "aaa"))
        for _ in range(30):
            await pilot.pause(0.1)
            if app.installing:
                break
        visible = app.cancel_btn.display
        await pilot.click("#cancel-install")
        for _ in range(40):
            await pilot.pause(0.1)
            if not app.installing:
                break
        return visible, app.cancel_btn.display, app.installing, "\n".join(app.log_buffer)

    with (
        patch.object(tui, "fast_install", _fake_installer(False, wait_for_cancel=True)),
        patch.object(tui.TermuxAppStore, "_build_from_source_with_progress", lambda self, n: built.append(n) or True),
    ):
        visible, hidden, installing, log = _run(scenario)
    assert visible is True and hidden is False and installing is False
    assert "cancelled" in log
    assert built == []
    assert tui.ACTIVITY.recent(1)[0]["result"] == "cancelled"


def test_cancel_removes_queued_tasks():
    async def scenario(app, pilot):
        app.worker_queue.put_nowait(("install", "aaa"))
        for _ in range(30):
            await pilot.pause(0.1)
            if app.installing:
                break
        app.worker_queue.put_nowait(("install", "ccc"))
        app.queued_names.add("ccc")
        app.request_cancel()
        for _ in range(40):
            await pilot.pause(0.1)
            if not app.installing:
                break
        return app.worker_queue.qsize(), set(app.queued_names), "\n".join(app.log_buffer)

    with patch.object(tui, "fast_install", _fake_installer(False, wait_for_cancel=True)):
        size, queued, log = _run(scenario)
    assert size == 0 and queued == set()
    assert "1 queued task(s) removed" in log


def test_request_cancel_without_running_install_only_reports():
    async def scenario(app, pilot):
        app.request_cancel()
        await pilot.pause(0.2)
        return str(app.status_bar.content)

    assert "Nothing to cancel" in _run(scenario)


def test_successful_install_is_recorded_and_notified_when_long():
    sent = []

    async def scenario(app, pilot):
        app.worker_queue.put_nowait(("install", "aaa"))
        for _ in range(40):
            await pilot.pause(0.1)
            if tui.ACTIVITY.recent(1):
                break
        await pilot.pause(0.3)
        return tui.ACTIVITY.recent(1)[0]

    with (
        patch.object(tui, "fast_install", _fake_installer(True)),
        patch.object(tui, "NOTIFY_MIN_SECONDS", 0),
        patch.object(
            tui, "notify_done", lambda title, content, vibrate=True: sent.append((title, content, vibrate)) or True
        ),
    ):
        entry = _run(scenario)
    assert entry["action"] == "install" and entry["package"] == "aaa" and entry["result"] == "ok"
    assert entry["version"] == "1.0"
    assert sent == [("Termux App Store", "aaa installed", True)]


def test_short_install_does_not_notify_and_notifications_can_be_disabled():
    sent = []

    async def scenario(app, pilot):
        app.worker_queue.put_nowait(("install", "aaa"))
        for _ in range(40):
            await pilot.pause(0.1)
            if tui.ACTIVITY.recent(1):
                break
        await pilot.pause(0.3)
        tui.SETTINGS.set("notify", False)
        with patch.object(tui, "NOTIFY_MIN_SECONDS", 0):
            app.finish_notice("x", 5)
        return len(sent)

    with (
        patch.object(tui, "fast_install", _fake_installer(True)),
        patch.object(tui, "notify_done", lambda *a, **k: sent.append(a) or True),
    ):
        assert _run(scenario) == 0


def test_failed_install_keeps_log_tail_for_bug_reports():
    async def scenario(app, pilot):
        app.worker_queue.put_nowait(("install", "aaa"))
        for _ in range(40):
            await pilot.pause(0.1)
            if tui.ACTIVITY.recent(1):
                break
        await pilot.pause(0.3)
        return tui.ACTIVITY.recent(1)[0]

    with (
        patch.object(tui, "fast_install", _fake_installer(False, log="E: boom happened")),
        patch.object(tui.TermuxAppStore, "_build_from_source_with_progress", lambda self, n: False),
    ):
        entry = _run(scenario)
    assert entry["result"] == "failed"
    assert "E: boom happened" in entry["detail"]


def test_detail_panel_shows_last_activity():
    async def scenario(app, pilot):
        tui.ACTIVITY.add("install", "aaa", "1.0", "ok", 3.0)
        app.refresh_current_preview()
        await pilot.pause(0.3)
        return str(app.info.content)

    assert "Last       : installed just now" in _run(scenario)


def test_history_screen_lists_activity_and_closes():
    async def scenario(app, pilot):
        tui.ACTIVITY.add("install", "aaa", "1.0", "ok", 3.0)
        tui.ACTIVITY.add("uninstall", "bbb", "2.0", "failed", 1.0)
        await pilot.press("f4")
        await pilot.pause(0.5)
        opened = type(app.screen).__name__
        body = str(app.screen.query_one("#history-body").content)
        await pilot.press("escape")
        await pilot.pause(0.3)
        return opened, body, type(app.screen).__name__

    opened, body, after = _run(scenario)
    assert opened == "HistoryScreen"
    assert "install   aaa 1.0" in body and "✗ uninstall bbb 2.0" in body
    assert body.index("bbb") < body.index("aaa")
    assert after != "HistoryScreen"


def test_history_screen_without_entries():
    async def scenario(app, pilot):
        await pilot.press("f4")
        await pilot.pause(0.5)
        return str(app.screen.query_one("#history-body").content)

    assert _run(scenario) == "No activity yet."


def test_report_issue_opens_prefilled_url_with_current_log():
    calls = []

    async def scenario(app, pilot):
        app.list_view.index = 1
        await pilot.pause(0.4)
        app.log_buffer[:] = ["line one", "E: something broke"]
        with (
            patch.object(tui.subprocess, "Popen", lambda argv, **k: calls.append(argv)),
            patch.object(
                tui,
                "collect_environment",
                lambda: {
                    "app_version": "9.9.9",
                    "arch": "aarch64",
                    "android": "14",
                    "python": "3.12.1",
                    "textual": "8.0",
                    "termux_version": "0.118",
                },
            ),
        ):
            await pilot.press("f5")
            await pilot.pause(0.3)
        return str(app.status_bar.content)

    status = _run(scenario)
    assert "browser" in status
    assert calls[0][0] == "termux-open-url"
    url = calls[0][1]
    assert url.startswith("https://github.com/djunekz/termux-app-store/issues/new?template=bug_report.yml")
    assert "bbb%202.0" in url and "E%3A%20something%20broke" in url and "9.9.9" in url


def test_report_issue_falls_back_to_last_failed_install_log():
    calls = []

    async def scenario(app, pilot):
        tui.ACTIVITY.add("install", "aaa", "1.0", "failed", 2.0, "old failure line")
        app.list_view.index = 0
        await pilot.pause(0.3)
        app.log_buffer.clear()
        with (
            patch.object(tui.subprocess, "Popen", lambda argv, **k: calls.append(argv)),
            patch.object(tui, "collect_environment", lambda: {}),
        ):
            app.action_report_issue()
        return calls[0][1]

    assert "old%20failure%20line" in _run(scenario)


def test_report_issue_without_browser_command_reports_it():
    async def scenario(app, pilot):
        def boom(*a, **k):
            raise FileNotFoundError

        with patch.object(tui.subprocess, "Popen", boom):
            app.action_report_issue()
        return str(app.status_bar.content)

    assert "termux-open-url not found" in _run(scenario)


def test_shortcut_button_creates_shortcut_from_dialog():
    created = []

    async def scenario(app, pilot):
        app.list_view.index = 1
        await pilot.pause(0.4)
        await pilot.click("#install")
        await pilot.pause(0.8)
        await pilot.press("-", "-", "x")
        await pilot.click("#run-shortcut")
        await pilot.pause(0.6)
        return type(app.screen).__name__, str(app.status_bar.content)

    with patch.object(
        tui, "create_shortcut", lambda exe, args: created.append((exe, args)) or (True, "/home/.shortcuts/bbb")
    ):
        screen, status = _run(scenario)
    assert created == [("bbb", "--x")]
    assert screen != "RunScreen"
    assert "Shortcut saved: /home/.shortcuts/bbb" in status


def test_run_records_activity_for_open():
    async def scenario(app, pilot):
        with (
            patch.object(tui.TermuxAppStore, "suspend", lambda self: contextlib.nullcontext()),
            patch.object(tui.subprocess, "call", lambda argv: 3),
            patch("builtins.input", lambda: ""),
        ):
            app.run_external("bbb", "", "bbb")
            await pilot.pause(0.2)
        return tui.ACTIVITY.recent(1)[0]

    entry = _run(scenario)
    assert entry["action"] == "open" and entry["result"] == "failed" and entry["detail"] == "exit 3"


def test_toggle_notifications_updates_setting_and_hints_about_termux_api():
    async def scenario(app, pilot):
        with patch.object(tui.shutil, "which", lambda name: None):
            app.action_toggle_notify()
            off = (tui.SETTINGS.get("notify"), str(app.status_bar.content))
            app.action_toggle_notify()
            on = (tui.SETTINGS.get("notify"), str(app.status_bar.content))
        return off, on

    off, on = _run(scenario)
    assert off == (False, "Completion notifications: OFF")
    assert on[0] is True and "pkg install termux-api" in on[1]


@pytest.mark.parametrize(
    "installed,store,expected",
    [
        (None, "1.0", "NOT INSTALLED"),
        ("1.0", "1.0", "INSTALLED"),
        ("2.0", "1.0", "INSTALLED"),
        ("1.0", "1.1", "UPDATE"),
    ],
)
def test_compute_status(installed, store, expected):
    assert tui.compute_status(installed, store) == expected


def test_get_installed_versions_parses_only_fully_installed(monkeypatch):
    sample = "\n".join(
        [
            "bash\tinstall ok installed\t5.2",
            "half\tinstall ok half-installed\t1.0",
            "gone\tdeinstall ok config-files\t1.0",
            "empty\tinstall ok installed\t",
            "broken line",
            "tool\tinstall ok installed\t2.1-3",
        ]
    )
    monkeypatch.setattr(tui.subprocess, "check_output", lambda *a, **k: sample)
    assert tui.get_installed_versions() == {"bash": "5.2", "tool": "2.1-3"}


def test_get_installed_versions_without_dpkg(monkeypatch):
    def boom(*a, **k):
        raise FileNotFoundError

    monkeypatch.setattr(tui.subprocess, "check_output", boom)
    assert tui.get_installed_versions() == {}


def test_build_issue_url_maps_architecture_and_fits_the_limit():
    env = {
        "app_version": "1.0",
        "arch": "arm",
        "android": "13",
        "python": "3.12.1",
        "textual": "8",
        "termux_version": "",
    }
    long_log = [f"line {i} " + "x" * 190 for i in range(30)]
    url = tui.build_issue_url(env, "tool", "1.2", long_log, max_len=3000)
    assert len(url) <= 3000
    assert "architecture=armv7l" in url
    assert "package_feature=tool" in url
    assert "line%2029" in url


def test_build_issue_url_drops_logs_when_nothing_fits_and_handles_no_package():
    env = {"arch": "i686"}
    url = tui.build_issue_url(env, "", "", ["x" * 190] * 30, max_len=700)
    assert len(url) <= 700
    assert "architecture=Other" in url
    assert "package_feature=TUI" in url
    assert "title=%5BBUG%5D%20TUI" in url


def test_notify_done_uses_termux_api_when_present(monkeypatch):
    calls = []
    tools = {"termux-notification": "/bin/n", "termux-vibrate": "/bin/v"}
    monkeypatch.setattr(tui.shutil, "which", lambda name: tools.get(name))
    monkeypatch.setattr(tui.subprocess, "Popen", lambda argv, **k: calls.append(argv))
    assert tui.notify_done("T", "body") is True
    assert calls[0][:5] == ["/bin/n", "--title", "T", "--content", "body"]
    assert calls[1] == ["/bin/v", "-d", "150"]
    calls.clear()
    assert tui.notify_done("T", "body", vibrate=False) is True
    assert len(calls) == 1


def test_notify_done_without_termux_api(monkeypatch):
    monkeypatch.setattr(tui.shutil, "which", lambda name: None)
    assert tui.notify_done("T", "body") is False


def test_create_shortcut_writes_runnable_script(tmp_path):
    ok, path = tui.create_shortcut("btop", "--utf-force 'a b'", tmp_path)
    assert ok
    script = tmp_path / "btop-utf-force-a-b"
    assert str(script) == path and script.stat().st_mode & 0o111
    lines = script.read_text().splitlines()
    assert lines[0].endswith("/bin/bash")
    assert lines[1] == "btop --utf-force 'a b'"
    assert "Press Enter to close..." in script.read_text()


def test_create_shortcut_refuses_to_overwrite_foreign_file_but_updates_own(tmp_path):
    (tmp_path / "tool").write_text("#!/bin/sh\necho mine\n")
    ok, message = tui.create_shortcut("tool", "", tmp_path)
    assert not ok and "already exists" in message
    assert (tmp_path / "tool").read_text() == "#!/bin/sh\necho mine\n"
    assert tui.create_shortcut("other", "", tmp_path)[0]
    assert tui.create_shortcut("other", "", tmp_path)[0]


def test_create_shortcut_rejects_bad_arguments_and_unwritable_folder(tmp_path):
    ok, message = tui.create_shortcut("tool", "'oops", tmp_path)
    assert not ok and "Invalid arguments" in message
    blocker = tmp_path / "file"
    blocker.write_text("x")
    ok, message = tui.create_shortcut("tool", "", blocker / "sub")
    assert not ok and "Cannot write shortcut" in message


@pytest.mark.parametrize(
    "exe,args,expected",
    [("btop", "", "btop"), ("a/b", "", "a-b"), ("tool", "--x=1 y", "tool-x-1-y"), ("///", "", "tool")],
)
def test_shortcut_name(exe, args, expected):
    assert tui.shortcut_name(exe, args) == expected


def test_history_line_formats_entries():
    entry = {"time": 1000.0, "action": "install", "package": "aaa", "version": "1.0", "result": "ok", "seconds": 12.5}
    assert tui.history_line(entry, now=1000.0 + 7200) == "  2h ago  ✔ install   aaa 1.0  12.5s"
    bare = {"time": 1000.0, "action": "open", "package": "bbb", "result": "cancelled"}
    assert tui.history_line(bare, now=1000.0) == "just now  ⊘ open      bbb"
