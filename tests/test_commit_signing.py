import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "ci" / "setup_commit_signing.sh"
WORKFLOWS = sorted((ROOT / ".github" / "workflows").glob("*.yml"))
EMAIL = "258522831+termuxappstore@users.noreply.github.com"


def _git_supports_ssh_signing() -> bool:
    if not shutil.which("git") or not shutil.which("ssh-keygen") or not shutil.which("bash"):
        return False
    out = subprocess.run(["git", "--version"], capture_output=True, text=True).stdout
    match = re.search(r"(\d+)\.(\d+)", out)
    return bool(match) and (int(match.group(1)), int(match.group(2))) >= (2, 34)


needs_tools = pytest.mark.skipif(not _git_supports_ssh_signing(), reason="git 2.34+ and ssh-keygen are required")


def _keygen(path: Path, passphrase: str = "") -> str:
    subprocess.run(
        ["ssh-keygen", "-q", "-t", "ed25519", "-N", passphrase, "-C", "test", "-f", str(path)],
        check=True,
        stdin=subprocess.DEVNULL,
    )
    return path.with_name(path.name + ".pub").read_text().strip()


def _env(home: Path, **extra) -> dict:
    env = {
        "PATH": os.environ["PATH"],
        "HOME": str(home),
        "RUNNER_TEMP": str(home),
        "GIT_CONFIG_NOSYSTEM": "1",
    }
    env.update(extra)
    return env


def _run_script(home: Path, key: str | None):
    env = _env(home)
    if key is not None:
        env["BOT_SIGNING_KEY"] = key
    return subprocess.run(
        ["bash", str(SCRIPT)],
        env=env,
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
        start_new_session=True,
        timeout=30,
    )


def _global(home: Path, name: str) -> str:
    result = subprocess.run(
        ["git", "config", "--global", "--get", name],
        env=_env(home),
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


@pytest.fixture
def home(tmp_path):
    path = tmp_path / "home"
    path.mkdir()
    return path


@needs_tools
def test_valid_key_configures_git_and_commits_verify(tmp_path, home):
    private = tmp_path / "bot"
    public = _keygen(private)
    result = _run_script(home, private.read_text())
    assert result.returncode == 0, result.stderr
    assert "Commit signing enabled" in result.stdout
    assert _global(home, "gpg.format") == "ssh"
    assert _global(home, "commit.gpgsign") == "true"

    stored = Path(_global(home, "user.signingkey"))
    assert stored.exists() and stored.stat().st_mode & 0o777 == 0o600

    repo = tmp_path / "repo"
    repo.mkdir()
    env = _env(home)
    subprocess.run(["git", "init", "-q"], cwd=repo, env=env, check=True)
    subprocess.run(["git", "config", "user.email", EMAIL], cwd=repo, env=env, check=True)
    subprocess.run(["git", "config", "user.name", "Termux App Store"], cwd=repo, env=env, check=True)
    (repo / "a.txt").write_text("x")
    subprocess.run(["git", "add", "a.txt"], cwd=repo, env=env, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "signed"], cwd=repo, env=env, check=True, stdin=subprocess.DEVNULL)

    allowed = tmp_path / "allowed"
    allowed.write_text(f'{EMAIL} namespaces="git" {public}\n')
    status = subprocess.run(
        ["git", "-c", f"gpg.ssh.allowedSignersFile={allowed}", "log", "-1", "--format=%G?"],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
    ).stdout.strip()
    assert status == "G"


@needs_tools
@pytest.mark.parametrize("key", [None, ""])
def test_missing_key_is_a_notice_and_changes_nothing(home, key):
    result = _run_script(home, key)
    assert result.returncode == 0
    assert "::notice::BOT_SIGNING_KEY is not set" in result.stdout
    assert _global(home, "commit.gpgsign") == ""
    assert not (home / "tas_commit_signing").exists()


@needs_tools
def test_garbage_key_is_a_warning_and_is_removed(home):
    result = _run_script(home, "this is not a key")
    assert result.returncode == 0
    assert "::warning::" in result.stdout
    assert _global(home, "commit.gpgsign") == ""
    assert not (home / "tas_commit_signing").exists()


@needs_tools
def test_encrypted_key_is_rejected_without_hanging(tmp_path, home):
    private = tmp_path / "locked"
    _keygen(private, passphrase="secret-passphrase")
    result = _run_script(home, private.read_text())
    assert result.returncode == 0
    assert "::warning::" in result.stdout
    assert _global(home, "commit.gpgsign") == ""


@needs_tools
def test_key_without_trailing_newline_still_works(tmp_path, home):
    private = tmp_path / "bot"
    _keygen(private)
    result = _run_script(home, private.read_text().rstrip("\n"))
    assert result.returncode == 0
    assert "Commit signing enabled" in result.stdout


JOB_START = re.compile(r"^  [A-Za-z0-9_-]+:\s*$")
STEP_START = re.compile(r"^      - ")
SETUP_CALL = "bash ci/setup_commit_signing.sh"


def _jobs(path: Path) -> list:
    jobs: list = []
    inside = False
    steps = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("jobs:"):
            inside = True
            continue
        if not inside:
            continue
        if JOB_START.match(line):
            steps = []
            jobs.append(steps)
        elif steps is not None and STEP_START.match(line):
            steps.append([line])
        elif steps:
            steps[-1].append(line)
    return [["\n".join(step) for step in job] for job in jobs]


def _commits(step: str) -> bool:
    return "git commit" in step


def _condition(step: str):
    match = re.search(r"(?m)^        if: (.+)$", step)
    return match.group(1) if match else None


def _committing_workflows() -> list:
    return [p for p in WORKFLOWS if any(_commits(step) for job in _jobs(p) for step in job)]


def test_all_expected_workflows_are_detected_as_committing():
    assert {p.name for p in _committing_workflows()} >= {
        "auto-release.yml",
        "auto-update-packages.yml",
        "build-packages-debs.yml",
        "build-termux-repo.yml",
        "repin-floating-sources.yml",
        "update_index.yml",
        "update_log.yml",
    }


@pytest.mark.parametrize("path", _committing_workflows(), ids=lambda p: p.name)
def test_every_workflow_that_commits_sets_up_signing_first(path):
    for steps in _jobs(path):
        committing = [i for i, step in enumerate(steps) if _commits(step)]
        if not committing:
            continue
        setup = [i for i, step in enumerate(steps) if SETUP_CALL in step]
        assert setup, f"{path.name} commits without setting up signing"
        assert setup[0] < committing[0]
        assert "BOT_SIGNING_KEY: ${{ secrets.BOT_SIGNING_KEY }}" in steps[setup[0]]


@pytest.mark.parametrize("path", _committing_workflows(), ids=lambda p: p.name)
def test_signing_step_condition_matches_the_commit_step_condition(path):
    for steps in _jobs(path):
        for i, step in enumerate(steps):
            if SETUP_CALL in step:
                following = next(s for s in steps[i + 1 :] if _commits(s))
                assert _condition(step) == _condition(following)


def test_script_never_prints_the_key():
    text = SCRIPT.read_text()
    assert 'echo "$BOT_SIGNING_KEY"' not in text
    assert "set -x" not in text
    assert "#" not in "\n".join(line for line in text.splitlines() if not line.startswith("#!") and "::" not in line)
