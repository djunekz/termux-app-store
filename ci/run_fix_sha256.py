#!/usr/bin/env python3
"""
ci/fix_sha256.py
Auto-fix TERMUX_PKG_SHA256 in packages/*/build.sh when validate-build.sh
reports a mismatch.

Unlike the old version, this script never pushes directly to the default
branch. It only touches packages whose TERMUX_PKG_SRCURL is pinned to an
immutable ref (a Git tag or a full commit SHA) — for those, it opens a PR
for human review and never merges it. A hash mismatch on a tag is exactly what
a moved or tampered tag looks like, so the new hash must be checked against
upstream before it is accepted. Packages that
are still pinned to a floating branch (archive/refs/heads/...) are left
alone: their source can change silently upstream, so a SHA256 mismatch
there needs a human to re-pin the package to a tag/commit first, not a bot
quietly accepting whatever is currently on that branch.

Usage:
  python ci/run_fix_sha256.py                   # scan all packages
  python ci/run_fix_sha256.py neovim aichat     # scan specific packages
"""

import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

PACKAGES_DIR = Path("packages")

R = "\033[0m"
B = "\033[1m"
DIM = "\033[2m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RED = "\033[91m"

FLOATING_BRANCH_RE = re.compile(r"/archive/refs/heads/")

GITHUB_API = "https://api.github.com"


def ok(msg):
    print(f"  {GREEN}✓{R}  {msg}")


def info(msg):
    print(f"  {CYAN}→{R}  {msg}")


def warn(msg):
    print(f"  {YELLOW}!{R}  {msg}")


def err(msg):
    print(f"  {RED}✗{R}  {msg}")


def header(msg):
    print(f"\n{CYAN}{B}{'─' * 50}{R}\n{B}{msg}{R}")


def parse_var(build_sh: Path, var: str) -> str:
    pattern = re.compile(rf"^{var}=(.+)$", re.MULTILINE)
    content = build_sh.read_text(encoding="utf-8")
    m = pattern.search(content)
    if not m:
        return ""
    val = m.group(1).strip().strip('"').strip("'")
    return val


def resolve_srcurl(build_sh: Path) -> str:
    version = parse_var(build_sh, "TERMUX_PKG_VERSION")
    srcurl_raw = parse_var(build_sh, "TERMUX_PKG_SRCURL")

    if not srcurl_raw:
        return ""

    url = srcurl_raw
    url = url.replace("${TERMUX_PKG_VERSION}", version)
    url = url.replace("$TERMUX_PKG_VERSION", version)

    return url


def is_floating_source(srcurl: str) -> bool:
    return bool(FLOATING_BRANCH_RE.search(srcurl))


def compute_sha256(url: str) -> tuple[str, int]:
    info(f"Downloading: {DIM}{url}{R}")
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "termux-app-store-ci/1.0"},
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            h = hashlib.sha256()
            size = 0
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                while True:
                    chunk = resp.read(65536)
                    if not chunk:
                        break
                    h.update(chunk)
                    tmp.write(chunk)
                    size += len(chunk)
            return h.hexdigest(), size

    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {url}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"URL error: {e.reason}")
    except Exception as e:
        raise RuntimeError(str(e))


def update_sha256_in_build_sh(build_sh: Path, new_sha256: str) -> bool:
    content = build_sh.read_text(encoding="utf-8")
    pattern = re.compile(r"^(TERMUX_PKG_SHA256=)(.+)$", re.MULTILINE)

    m = pattern.search(content)
    if not m:
        err(f"TERMUX_PKG_SHA256 not found in {build_sh}")
        return False

    old_sha = m.group(2).strip().strip('"').strip("'")
    if old_sha == new_sha256:
        ok(f"SHA256 already up-to-date: {new_sha256[:16]}...")
        return False

    original_line = m.group(0)
    if '"' in original_line:
        new_line = f'TERMUX_PKG_SHA256="{new_sha256}"'
    elif "'" in original_line:
        new_line = f"TERMUX_PKG_SHA256='{new_sha256}'"
    else:
        new_line = f"TERMUX_PKG_SHA256={new_sha256}"

    new_content = pattern.sub(new_line, content, count=1)
    build_sh.write_text(new_content, encoding="utf-8")

    info("Updated SHA256:")
    print(f"    {DIM}Old: {old_sha}{R}")
    print(f"    {GREEN}New: {new_sha256}{R}")
    return True


def check_sha256_mismatch(build_sh: Path) -> tuple[bool, str, str]:
    try:
        result = subprocess.run(
            ["bash", "tools/validate-build.sh", str(build_sh)],
            capture_output=True,
            text=True,
            timeout=120,
        )
        output = result.stdout + result.stderr

        if result.returncode == 0:
            return False, "", ""

        expected_match = re.search(r"Expected:\s*([a-f0-9]{64})", output)
        got_match = re.search(r"Got\s*:\s*([a-f0-9]{64})", output)

        if expected_match and got_match:
            return True, expected_match.group(1), got_match.group(1)

        if "SHA256 mismatch" in output or "mismatch" in output.lower():
            return True, "", ""

        return False, "", ""

    except subprocess.TimeoutExpired:
        warn("validate-build.sh timed out")
        return False, "", ""
    except FileNotFoundError:
        warn("tools/validate-build.sh not found — skipping mismatch check")
        return False, "", ""


def process_package(pkg_name: str) -> str:
    build_sh = PACKAGES_DIR / pkg_name / "build.sh"

    if not build_sh.exists():
        err(f"build.sh not found: {build_sh}")
        return "no_sh"

    srcurl = resolve_srcurl(build_sh)
    declared_sha = parse_var(build_sh, "TERMUX_PKG_SHA256")
    version = parse_var(build_sh, "TERMUX_PKG_VERSION")

    if not srcurl:
        warn(f"{pkg_name}: no TERMUX_PKG_SRCURL — skipping")
        return "skipped"

    if not declared_sha:
        warn(f"{pkg_name}: no TERMUX_PKG_SHA256 declared — skipping")
        return "skipped"

    if srcurl.lower().endswith(".deb"):
        info(f"{pkg_name}: pre-built .deb source — skip SHA256 auto-fix")
        return "skipped"

    info(f"Checking {B}{pkg_name}{R} v{version}")
    info(f"URL: {DIM}{srcurl}{R}")
    info(f"Declared SHA256: {DIM}{declared_sha[:32]}...{R}")

    if is_floating_source(srcurl):
        warn(f"{pkg_name}: SRCURL is a floating branch tarball ({srcurl})")
        warn(
            f"{pkg_name}: refusing to auto-fix — upstream content may have "
            f"genuinely changed. Re-pin this package to a tag or commit SHA "
            f"(e.g. via pkg-scaffold.py) and review the diff manually."
        )
        return "floating_needs_review"

    try:
        actual_sha, file_size = compute_sha256(srcurl)
    except RuntimeError as e:
        err(f"{pkg_name}: download failed — {e}")
        return "error"

    if actual_sha == declared_sha:
        ok(f"{pkg_name}: SHA256 OK ({file_size:,} bytes)")
        return "ok"

    warn(f"{pkg_name}: SHA256 mismatch on a pinned (tag/commit) source!")
    print(f"    {DIM}Declared: {declared_sha}{R}")
    print(f"    {YELLOW}Actual  : {actual_sha}{R}")
    print(f"    {DIM}Size    : {file_size:,} bytes{R}")

    updated = update_sha256_in_build_sh(build_sh, actual_sha)
    if updated:
        ok(f"{pkg_name}: build.sh updated with correct SHA256")
        return "fixed"
    return "ok"


def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kwargs)


def github_api(method: str, path: str, token: str, body: dict | None = None) -> dict:
    url = f"{GITHUB_API}{path}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def open_review_pr(fixed_packages: list[str]) -> None:
    if not fixed_packages:
        return

    token = os.environ.get("PAT_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")
    base_branch = os.environ.get("GITHUB_BASE_REF") or os.environ.get("GITHUB_REF_NAME", "master")

    if not token or not repo:
        err(
            "PAT_TOKEN or GITHUB_REPOSITORY not set — cannot open PR. "
            "build.sh files were updated locally but not pushed."
        )
        return

    branch = f"ci/sha256-fix-{int(time.time())}"
    files_to_add = [f"packages/{pkg}/build.sh" for pkg in fixed_packages]

    print(f"\n{CYAN}{B}Opening PR for SHA256 fixes...{R}")

    try:
        run(["git", "config", "user.email", "258516621+termux-app-store@users.noreply.github.com"])
        run(["git", "config", "user.name", "Termux App Store"])
        run(["git", "checkout", "-b", branch])
        run(["git", "add"] + files_to_add)

        staged = run(["git", "diff", "--staged", "--name-only"])
        if not staged.stdout.strip():
            info("Nothing to commit (files unchanged after update)")
            return

        pkg_list = ", ".join(fixed_packages)
        commit_msg = f"fix(sha256): auto-update SHA256 for {pkg_list}"
        run(["git", "commit", "-m", commit_msg])
        run(["git", "remote", "set-url", "origin", f"https://x-access-token:{token}@github.com/{repo}.git"])
        run(["git", "push", "-u", "origin", branch])
        ok(f"Pushed branch: {branch}")

    except subprocess.CalledProcessError as e:
        err(f"Git operation failed: {e.stderr or e}")
        return

    try:
        pr = github_api(
            "POST",
            f"/repos/{repo}/pulls",
            token,
            {
                "title": f"fix(sha256): auto-update SHA256 for {len(fixed_packages)} package(s)",
                "head": branch,
                "base": base_branch,
                "body": (
                    "Automated SHA256 fix for the following tag/commit-pinned "
                    "packages, opened by `ci/run_fix_sha256.py`:\n\n"
                    + "\n".join(f"- `{p}`" for p in fixed_packages)
                    + "\n\n**This PR is not auto-merged.** A SHA256 mismatch on a "
                    "tag or commit-pinned source can mean the upstream tag was "
                    "moved or tampered with. Before merging, compare the new hash "
                    "against the upstream release and review the content change. "
                    "Floating-branch sources are never auto-fixed and are "
                    "reported separately for manual review."
                ),
            },
        )
        pr_number = pr["number"]
        ok(f"Opened PR #{pr_number}")
    except Exception as e:
        err(f"Failed to open PR: {e}")
        return

    warn(f"PR #{pr_number} is open and requires manual review before merging.")


def main():
    if len(sys.argv) > 1:
        pkg_names = sys.argv[1:]
    else:
        if not PACKAGES_DIR.is_dir():
            err("packages/ directory not found")
            sys.exit(1)
        pkg_names = sorted(d for d in os.listdir(PACKAGES_DIR) if (PACKAGES_DIR / d).is_dir())

    print(f"\n{CYAN}{B}SHA256 Auto-Fix{R}")
    print(f"{DIM}Checking {len(pkg_names)} package(s)...{R}\n")

    results = {
        "ok": [],
        "fixed": [],
        "skipped": [],
        "error": [],
        "no_sh": [],
        "floating_needs_review": [],
    }

    for pkg in pkg_names:
        header(f"Package: {pkg}")
        status = process_package(pkg)
        results[status].append(pkg)

    print(f"\n{CYAN}{B}{'═' * 25}{R}")
    print(f"{CYAN}{B}Summary{R}")
    print(f"{'─' * 25}")
    print(f"  {GREEN}✓  OK      : {len(results['ok'])}{R}")
    print(f"  {GREEN}✓  Fixed   : {len(results['fixed'])}{R}")
    if results["fixed"]:
        for p in results["fixed"]:
            print(f"      {DIM}• {p}{R}")
    print(f"  {DIM}○  Skipped : {len(results['skipped'])}{R}")
    print(f"  {YELLOW}!  Needs manual re-pin (floating source): {len(results['floating_needs_review'])}{R}")
    if results["floating_needs_review"]:
        for p in results["floating_needs_review"]:
            print(f"      {DIM}• {p}{R}")
    print(f"  {RED}✗  Error   : {len(results['error'])}{R}")
    if results["error"]:
        for p in results["error"]:
            print(f"      {DIM}• {p}{R}")

    if results["fixed"]:
        open_review_pr(results["fixed"])

    if results["floating_needs_review"]:
        print(
            f"\n{YELLOW}{len(results['floating_needs_review'])} package(s) have a "
            f"SHA256 mismatch on a floating source and were NOT auto-fixed.{R}"
        )
        print(f"{YELLOW}Re-pin them to a tag or commit SHA and review the content change before updating SHA256.{R}\n")

    if results["error"]:
        print(f"\n{RED}Some packages had download errors — check URLs{R}\n")
        sys.exit(1)

    print(f"\n{GREEN}{B}Done!{R}\n")
    sys.exit(0)


if __name__ == "__main__":
    main()
