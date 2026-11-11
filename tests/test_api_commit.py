import base64
import importlib.util
import os
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("api_commit_under_test", ROOT / "ci" / "api_commit.py")
ac = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ac)

REPO = "owner/name"
HEAD = "a" * 40


def sh(cwd, *args):
    subprocess.run(args, cwd=cwd, check=True, capture_output=True)


@pytest.fixture
def work(tmp_path, monkeypatch):
    sh(tmp_path, "git", "init", "-q")
    sh(tmp_path, "git", "config", "user.email", "t@example.com")
    sh(tmp_path, "git", "config", "user.name", "t")
    (tmp_path / "packages" / "one").mkdir(parents=True)
    (tmp_path / "packages" / "one" / "build.sh").write_text("v=1\n")
    os.chmod(tmp_path / "packages" / "one" / "build.sh", 0o700)
    (tmp_path / "packages" / "two").mkdir(parents=True)
    (tmp_path / "packages" / "two" / "build.sh").write_text("v=1\n")
    (tmp_path / "CHANGELOG.md").write_text("# c\n")
    sh(tmp_path, "git", "add", "-A")
    sh(tmp_path, "git", "commit", "-q", "-m", "init")
    monkeypatch.chdir(tmp_path)
    (tmp_path / "msg.txt").write_text("chore: update\n\nbody\n")
    return tmp_path


class FakeApi:
    def __init__(self, local_head, remote=None, compare=None, ref_missing=False, stale=False):
        self.calls = []
        self.local_head = local_head
        self.remote = remote or local_head
        self.compare = compare
        self.ref_missing = ref_missing
        self.stale = stale

    def __call__(self, method, path, body=None):
        self.calls.append((method, path, body))
        if method == "GET" and "/git/ref/heads/" in path:
            if self.ref_missing:
                raise ac.ApiError(404, "missing")
            return {"object": {"sha": self.remote}}
        if method == "GET" and "/compare/" in path:
            return self.compare
        if method == "GET" and "/git/commits/" in path:
            return {"tree": {"sha": "t" * 40}}
        if method == "POST" and path.endswith("/git/blobs"):
            return {"sha": "b" * 40}
        if method == "POST" and path.endswith("/git/trees"):
            return {"sha": "e" * 40}
        if method == "POST" and path.endswith("/git/commits"):
            return {"sha": "c" * 40}
        if method == "PATCH" and self.stale:
            raise ac.ApiError(422, "not a fast forward")
        return {}

    def find(self, method, suffix):
        return [c for c in self.calls if c[0] == method and c[1].endswith(suffix)]


def local_head(work):
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=work, capture_output=True, text=True).stdout.strip()


def invoke(monkeypatch, fake, *extra, paths=("packages/*/build.sh", "CHANGELOG.md")):
    monkeypatch.setattr(ac, "api", fake)
    return ac.main(["--repo", REPO, "--branch", "master", "--message-file", "msg.txt", *extra, "--", *paths])


def test_nothing_to_commit(work, monkeypatch):
    fake = FakeApi(local_head(work))
    assert invoke(monkeypatch, fake) == ac.EXIT_NOTHING
    assert fake.calls == []


def test_modified_files_keep_mode_and_commit_has_no_author(work, monkeypatch):
    (work / "packages" / "one" / "build.sh").write_text("v=2\n")
    (work / "CHANGELOG.md").write_text("# c\nnew\n")
    fake = FakeApi(local_head(work))
    assert invoke(monkeypatch, fake) == 0
    tree = fake.find("POST", "/git/trees")[0][2]
    modes = {e["path"]: e["mode"] for e in tree["tree"]}
    assert modes == {"packages/one/build.sh": "100755", "CHANGELOG.md": "100644"}
    commit = fake.find("POST", "/git/commits")[0][2]
    assert "author" not in commit and "committer" not in commit
    assert commit["message"] == "chore: update\n\nbody\n"
    assert commit["parents"] == [local_head(work)]
    blobs = {base64.b64decode(c[2]["content"]) for c in fake.find("POST", "/git/blobs")}
    assert blobs == {b"v=2\n", b"# c\nnew\n"}
    patch = fake.find("PATCH", "/git/refs/heads/master")[0][2]
    assert patch == {"sha": "c" * 40, "force": False}


def test_deleted_file_has_null_sha(work, monkeypatch):
    (work / "packages" / "two" / "build.sh").unlink()
    fake = FakeApi(local_head(work))
    assert invoke(monkeypatch, fake) == 0
    entry = fake.find("POST", "/git/trees")[0][2]["tree"][0]
    assert entry["path"] == "packages/two/build.sh" and entry["sha"] is None


def test_new_executable_file_gets_executable_mode(work, monkeypatch):
    new = work / "packages" / "three"
    new.mkdir()
    (new / "build.sh").write_text("v=1\n")
    os.chmod(new / "build.sh", 0o700)
    fake = FakeApi(local_head(work))
    assert invoke(monkeypatch, fake) == 0
    entry = fake.find("POST", "/git/trees")[0][2]["tree"][0]
    assert entry["mode"] == "100755"


def test_symlink_is_refused(work, monkeypatch):
    os.symlink("CHANGELOG.md", work / "packages" / "link.sh")
    fake = FakeApi(local_head(work))
    assert invoke(monkeypatch, fake, paths=("packages/link.sh",)) == ac.EXIT_UNSUPPORTED
    assert fake.find("POST", "/git/commits") == []


def test_reset_branch_forces_existing_ref(work, monkeypatch):
    (work / "CHANGELOG.md").write_text("# c\nx\n")
    fake = FakeApi(local_head(work))
    assert invoke(monkeypatch, fake, "--reset-branch") == 0
    patch = fake.find("PATCH", "/git/refs/heads/master")[0][2]
    assert patch["force"] is True
    assert fake.find("POST", "/git/refs") == []


def test_reset_branch_creates_missing_ref(work, monkeypatch):
    (work / "CHANGELOG.md").write_text("# c\nx\n")
    fake = FakeApi(local_head(work), ref_missing=True)
    assert invoke(monkeypatch, fake, "--reset-branch") == 0
    created = fake.find("POST", "/git/refs")[0][2]
    assert created == {"ref": "refs/heads/master", "sha": "c" * 40}


def test_remote_moved_on_other_files_is_allowed(work, monkeypatch):
    (work / "CHANGELOG.md").write_text("# c\nx\n")
    compare = {"status": "ahead", "files": [{"filename": "README.md"}]}
    fake = FakeApi(local_head(work), remote="d" * 40, compare=compare)
    assert invoke(monkeypatch, fake) == 0
    assert fake.find("POST", "/git/commits")[0][2]["parents"] == ["d" * 40]


def test_remote_moved_on_same_file_is_a_conflict(work, monkeypatch):
    (work / "CHANGELOG.md").write_text("# c\nx\n")
    compare = {"status": "ahead", "files": [{"filename": "CHANGELOG.md"}]}
    fake = FakeApi(local_head(work), remote="d" * 40, compare=compare)
    assert invoke(monkeypatch, fake) == ac.EXIT_CONFLICT
    assert fake.find("POST", "/git/commits") == []


def test_diverged_remote_is_a_conflict(work, monkeypatch):
    (work / "CHANGELOG.md").write_text("# c\nx\n")
    fake = FakeApi(local_head(work), remote="d" * 40, compare={"status": "diverged", "files": []})
    assert invoke(monkeypatch, fake) == ac.EXIT_CONFLICT


def test_fast_forward_rejection_is_reported_as_stale(work, monkeypatch):
    (work / "CHANGELOG.md").write_text("# c\nx\n")
    fake = FakeApi(local_head(work), stale=True)
    assert invoke(monkeypatch, fake) == ac.EXIT_STALE


def test_other_api_errors_return_one(work, monkeypatch):
    (work / "CHANGELOG.md").write_text("# c\nx\n")

    def boom(method, path, body=None):
        raise ac.ApiError(500, "server error")

    monkeypatch.setattr(ac, "api", boom)
    assert ac.main(["--repo", REPO, "--branch", "master", "--message-file", "msg.txt", "--", "CHANGELOG.md"]) == 1
