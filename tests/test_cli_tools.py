import subprocess
import sys
from pathlib import Path

import pytest
from _loader import load_cli

_cli = load_cli()
ROOT = Path(__file__).resolve().parent.parent

PACKAGES = [
    {"name": "alpha", "version": "1.0.0"},
    {"name": "beta", "version": "2.0.0"},
    {"name": "gamma", "version": "3.0.0"},
]
INSTALLED = {"alpha": "1.0.0", "beta": "1.0.0", "gamma": None}


@pytest.fixture
def store(monkeypatch):
    monkeypatch.setattr(_cli, "load_all_packages", lambda packages_dir: PACKAGES)
    monkeypatch.setattr(_cli, "get_installed_version", lambda name: INSTALLED[name])


def names_in(output: str) -> list:
    return [n for n in ("alpha", "beta", "gamma") if n in output]


def test_list_without_filter_shows_everything(store, capsys):
    _cli.cmd_list(Path("."))
    out = capsys.readouterr().out
    assert names_in(out) == ["alpha", "beta", "gamma"]
    assert "3 package(s) total" in out


def test_list_installed_hides_missing_packages(store, capsys):
    _cli.cmd_list(Path("."), "installed")
    out = capsys.readouterr().out
    assert names_in(out) == ["alpha", "beta"]
    assert "2 package(s) installed" in out


def test_list_outdated_shows_only_updates(store, capsys):
    _cli.cmd_list(Path("."), "outdated")
    out = capsys.readouterr().out
    assert names_in(out) == ["beta"]
    assert "1 package(s) outdated" in out


def test_list_outdated_when_all_current(store, monkeypatch, capsys):
    monkeypatch.setattr(_cli, "get_installed_version", lambda name: "9.0.0")
    _cli.cmd_list(Path("."), "outdated")
    assert "Everything is up to date." in capsys.readouterr().out


def test_list_installed_when_none_installed(store, monkeypatch, capsys):
    monkeypatch.setattr(_cli, "get_installed_version", lambda name: None)
    _cli.cmd_list(Path("."), "installed")
    assert "No packages from the store are installed." in capsys.readouterr().out


@pytest.mark.parametrize(
    "argv,expected",
    [
        (["list"], None),
        (["-l"], None),
        (["list", "--installed"], "installed"),
        (["list", "--outdated"], "outdated"),
        (["--installed"], "installed"),
        (["--outdated"], "outdated"),
        (["list", "--installed", "--outdated"], "outdated"),
    ],
)
def test_run_cli_passes_the_filter(monkeypatch, argv, expected):
    calls = []
    monkeypatch.setattr(sys, "argv", ["tas", *argv])
    monkeypatch.setattr(_cli, "resolve_app_root", lambda: Path("."))
    monkeypatch.setattr(_cli, "cmd_list", lambda packages_dir, only=None: calls.append(only))
    _cli.run_cli()
    assert calls == [expected]


def test_doctor_forwards_its_arguments(monkeypatch):
    from termux_app_store import doctor

    seen = []
    monkeypatch.setattr(doctor, "run", lambda: seen.append(list(sys.argv)))
    monkeypatch.setattr(sys, "argv", ["tas", "doctor", "--brief"])
    _cli.run_cli()
    assert seen == [["doctor", "--brief"]]


def test_guide_opens_the_full_menu(monkeypatch):
    from termux_app_store import guidebook

    seen = []
    monkeypatch.setattr(guidebook, "run", lambda lang=None: seen.append(lang))
    monkeypatch.setattr(sys, "argv", ["tas", "guide"])
    _cli.run_cli()
    monkeypatch.setattr(sys, "argv", ["tas", "guidebook", "--lang", "id"])
    _cli.run_cli()
    assert seen == [None, "id"]


@pytest.mark.parametrize("extra", [["--lang"], ["--lang", "xx"]])
def test_guide_rejects_a_bad_language(monkeypatch, extra, capsys):
    from termux_app_store import guidebook

    monkeypatch.setattr(guidebook, "run", lambda lang=None: pytest.fail("must not open the guide"))
    monkeypatch.setattr(sys, "argv", ["tas", "guide", *extra])
    with pytest.raises(SystemExit) as exc:
        _cli.run_cli()
    assert exc.value.code == 1
    assert "Usage: termux-app-store guide" in capsys.readouterr().out


def test_help_lists_the_new_commands(capsys):
    _cli.cmd_help()
    out = capsys.readouterr().out
    for word in ("list --installed", "list --outdated", "doctor", "guide"):
        assert word in out


def run_script(*args, stdin=""):
    return subprocess.run([sys.executable, *args], cwd=ROOT, input=stdin, capture_output=True, text=True, timeout=60)


def test_root_doctor_script_still_works():
    result = run_script("doctor.py", "--help")
    assert result.returncode == 0
    assert "SMART DOCTOR" in result.stdout
    assert "tas doctor" in result.stdout


def test_package_doctor_module_runs_with_json():
    result = run_script("-m", "termux_app_store.doctor", "--json")
    assert result.returncode == 0
    assert '"checks"' in result.stdout


def test_root_guidebook_script_still_works():
    result = run_script("guidebook.py", stdin="q\n")
    assert result.returncode == 0
    assert "Goodbye" in result.stdout


def test_guide_with_language_skips_the_language_prompt():
    result = run_script(
        "-c",
        "import sys; sys.argv=['tas','guide','--lang','en']; from termux_app_store.main import main; main()",
        stdin="q\n",
    )
    assert result.returncode == 0
    assert "Select language" not in result.stdout
    assert "Choose a topic" in result.stdout


def test_doctor_runs_through_the_real_entry_point():
    result = run_script(
        "-c", "import sys; sys.argv=['tas','doctor','--help']; from termux_app_store.main import main; main()"
    )
    assert result.returncode == 0
    assert "SMART DOCTOR" in result.stdout


def test_find_root_resolves_the_project_from_inside_the_package():
    from termux_app_store import doctor

    assert doctor._find_root() is not None
