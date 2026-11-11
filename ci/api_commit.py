#!/usr/bin/env python3
import argparse
import base64
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

API = "https://api.github.com"
EXIT_NOTHING = 2
EXIT_STALE = 3
EXIT_CONFLICT = 4
EXIT_UNSUPPORTED = 5
SUPPORTED_MODES = ("100644", "100755")


class ApiError(Exception):
    def __init__(self, status, message):
        super().__init__(f"HTTP {status}: {message}")
        self.status = status


def api(method, path, body=None):
    token = os.environ["GH_TOKEN"]
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        API + path,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "tas-api-commit",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read()
    except urllib.error.HTTPError as e:
        raise ApiError(e.code, e.read().decode(errors="replace")[:500])
    return json.loads(raw) if raw else {}


def git(*args):
    return subprocess.run(["git", *args], check=True, capture_output=True).stdout


def changed_files(pathspecs):
    out = git("status", "--porcelain=v1", "-z", "--no-renames", "--untracked-files=all", "--", *pathspecs)
    entries = []
    for item in out.split(b"\0"):
        if not item:
            continue
        code, path = item[:2].decode(), item[3:].decode()
        entries.append((path, "D" in code))
    return entries


def file_mode(path):
    listed = git("ls-files", "-s", "--", path).decode().split()
    if listed:
        return listed[0]
    return "100755" if os.stat(path).st_mode & 0o111 else "100644"


def remote_head(repo, branch):
    return api("GET", f"/repos/{repo}/git/ref/heads/{branch}")["object"]["sha"]


def ref_exists(repo, branch):
    try:
        remote_head(repo, branch)
        return True
    except ApiError as e:
        if e.status == 404:
            return False
        raise


def overlaps_remote_changes(repo, local_head, remote, paths):
    cmp = api("GET", f"/repos/{repo}/compare/{local_head}...{remote}")
    if cmp.get("status") != "ahead":
        return True
    files = cmp.get("files", [])
    if len(files) >= 300:
        return True
    touched = set()
    for f in files:
        touched.add(f["filename"])
        if f.get("previous_filename"):
            touched.add(f["previous_filename"])
    return bool(touched & set(paths))


def build_tree_entries(repo, changes):
    entries = []
    for path, deleted in changes:
        if deleted:
            entries.append({"path": path, "mode": "100644", "type": "blob", "sha": None})
            continue
        if os.path.islink(path):
            raise ValueError(f"{path} is a symlink, which cannot be committed through the API")
        mode = file_mode(path)
        if mode not in SUPPORTED_MODES:
            raise ValueError(f"{path} has unsupported file mode {mode}")
        with open(path, "rb") as f:
            content = base64.b64encode(f.read()).decode()
        blob = api("POST", f"/repos/{repo}/git/blobs", {"content": content, "encoding": "base64"})
        entries.append({"path": path, "mode": mode, "type": "blob", "sha": blob["sha"]})
    return entries


def update_ref(repo, branch, sha, reset):
    if reset:
        if ref_exists(repo, branch):
            api("PATCH", f"/repos/{repo}/git/refs/heads/{branch}", {"sha": sha, "force": True})
        else:
            api("POST", f"/repos/{repo}/git/refs", {"ref": f"refs/heads/{branch}", "sha": sha})
        return
    api("PATCH", f"/repos/{repo}/git/refs/heads/{branch}", {"sha": sha, "force": False})


def run(args):
    changes = changed_files(args.paths)
    if not changes:
        print("Nothing to commit")
        return EXIT_NOTHING

    local_head = git("rev-parse", "HEAD").decode().strip()
    if args.reset_branch:
        base = local_head
    else:
        base = remote_head(args.repo, args.branch)
        if base != local_head and overlaps_remote_changes(args.repo, local_head, base, [p for p, _ in changes]):
            print(f"{args.branch} changed the same files since this job started, re-run the workflow", file=sys.stderr)
            return EXIT_CONFLICT

    try:
        entries = build_tree_entries(args.repo, changes)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return EXIT_UNSUPPORTED

    with open(args.message_file, encoding="utf-8") as f:
        message = f.read()
    base_tree = api("GET", f"/repos/{args.repo}/git/commits/{base}")["tree"]["sha"]
    tree = api("POST", f"/repos/{args.repo}/git/trees", {"base_tree": base_tree, "tree": entries})
    commit = api(
        "POST",
        f"/repos/{args.repo}/git/commits",
        {"message": message, "tree": tree["sha"], "parents": [base]},
    )

    try:
        update_ref(args.repo, args.branch, commit["sha"], args.reset_branch)
    except ApiError as e:
        if e.status == 422 and not args.reset_branch:
            print(f"{args.branch} moved while committing: {e}", file=sys.stderr)
            return EXIT_STALE
        raise

    print(f"Committed {commit['sha']} to {args.branch} ({len(changes)} file(s))")
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a") as f:
            f.write(f"commit={commit['sha']}\n")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--branch", required=True)
    parser.add_argument("--message-file", required=True)
    parser.add_argument("--reset-branch", action="store_true")
    parser.add_argument("paths", nargs="+")
    args = parser.parse_args(argv)
    try:
        return run(args)
    except ApiError as e:
        print(f"GitHub API error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
