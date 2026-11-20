import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "ci" / "publish_gh_pages.sh"


def git(cwd, *args, check=True):
    return subprocess.run(
        ["git", "-c", "user.email=t@example.com", "-c", "user.name=t", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=check,
    )


def make_remote(tmp_path, commits=4):
    remote = tmp_path / "remote.git"
    subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True)
    seed = tmp_path / "seed"
    subprocess.run(["git", "clone", "-q", str(remote), str(seed)], check=True, capture_output=True)
    git(seed, "checkout", "-q", "-b", "gh-pages")
    (seed / "pool").mkdir()
    for i in range(commits):
        (seed / "pool" / f"p{i}.deb").write_bytes(bytes([i]) * 2048)
        git(seed, "add", "-A")
        git(seed, "commit", "-q", "-m", f"c{i}")
    git(seed, "push", "-q", "origin", "gh-pages")
    return remote


def clone(tmp_path, remote, name):
    work = tmp_path / name
    subprocess.run(
        ["git", "clone", "-q", "--depth", "1", "-b", "gh-pages", f"file://{remote}", str(work)],
        check=True,
        capture_output=True,
    )
    return work


def publish(work, message):
    env = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@e", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@e"}
    import os

    return subprocess.run(
        ["bash", str(SCRIPT), str(work), message],
        capture_output=True,
        text=True,
        env={**os.environ, **env},
    )


def count(remote):
    out = subprocess.run(
        ["git", "--git-dir", str(remote), "rev-list", "--count", "gh-pages"], capture_output=True, text=True
    )
    return int(out.stdout.strip())


def files(remote):
    out = subprocess.run(
        ["git", "--git-dir", str(remote), "ls-tree", "-r", "--name-only", "gh-pages"], capture_output=True, text=True
    )
    return set(out.stdout.split())


def test_script_has_valid_syntax():
    assert subprocess.run(["bash", "-n", str(SCRIPT)]).returncode == 0


def test_publish_collapses_history_into_one_commit(tmp_path):
    remote = make_remote(tmp_path)
    assert count(remote) == 4
    work = clone(tmp_path, remote, "w1")
    (work / "pool" / "p0.deb").unlink()
    (work / "pool" / "new.deb").write_bytes(b"n" * 2048)
    result = publish(work, "pkg: update pool")
    assert result.returncode == 0, result.stderr
    assert count(remote) == 1
    assert files(remote) == {"pool/p1.deb", "pool/p2.deb", "pool/p3.deb", "pool/new.deb"}


def test_publish_does_nothing_without_changes(tmp_path):
    remote = make_remote(tmp_path)
    work = clone(tmp_path, remote, "w1")
    result = publish(work, "noop")
    assert result.returncode == 0
    assert "Nothing to commit" in result.stdout
    assert count(remote) == 4


def test_publish_refuses_to_overwrite_a_newer_remote(tmp_path):
    remote = make_remote(tmp_path)
    late = clone(tmp_path, remote, "late")
    (late / "pool" / "late.txt").write_text("late", encoding="utf-8")
    early = clone(tmp_path, remote, "early")
    (early / "pool" / "early.txt").write_text("early", encoding="utf-8")
    assert publish(early, "early").returncode == 0
    result = publish(late, "late")
    assert result.returncode != 0
    assert "pool/early.txt" in files(remote)
    assert "pool/late.txt" not in files(remote)


def test_publish_creates_the_branch_when_it_does_not_exist(tmp_path):
    import os

    remote = tmp_path / "empty.git"
    subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True)
    work = tmp_path / "w"
    work.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=work, check=True)
    subprocess.run(["git", "remote", "add", "origin", f"file://{remote}"], cwd=work, check=True)
    subprocess.run(["git", "checkout", "-q", "--orphan", "gh-pages"], cwd=work, check=True)
    (work / "index.html").write_text("hi", encoding="utf-8")
    env = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@e", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@e"}
    result = subprocess.run(
        ["bash", str(SCRIPT), str(work), "init"], capture_output=True, text=True, env={**os.environ, **env}
    )
    assert result.returncode == 0, result.stderr
    assert count(remote) == 1


def test_both_workflows_publish_through_the_script():
    for name in ("build-packages-debs.yml", "build-termux-repo.yml"):
        text = (ROOT / ".github" / "workflows" / name).read_text(encoding="utf-8")
        assert "bash ci/publish_gh_pages.sh gh-pages" in text
        assert "git push origin HEAD:gh-pages" not in text
