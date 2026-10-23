from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path

PACKAGES_DIR = Path("packages")
CHANGELOG = Path("CHANGELOG.md")

USER_AGENT = "termux-app-store-auto-update/1.0"
API_TIMEOUT = 20
DOWNLOAD_TIMEOUT = 120
MAX_DOWNLOAD_BYTES = 300 * 1024 * 1024
RETRIES = 3

NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._+-]*$")
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
VERSION_RE = re.compile(r"^[0-9][0-9A-Za-z.+~_-]*$")
PRERELEASE_RE = re.compile(r"alpha|beta|rc|pre|dev|nightly|snapshot|canary|preview", re.I)
COMMIT_VERSION_RE = re.compile(r"^0\.0\.0\+([0-9a-f]{7,40})$")

COMMIT_ARCHIVE_RE = re.compile(r"^https://github\.com/([^/]+)/([^/]+)/archive/([0-9a-f]{40})(\.tar\.gz|\.zip)$")
GITHUB_RE = re.compile(r"^https://github\.com/([^/]+)/([^/]+)/(?:archive/|releases/download/)")
GITHUB_API_RE = re.compile(r"^https://api\.github\.com/repos/([^/]+)/([^/]+)/(?:tarball|zipball)/")
NPM_RE = re.compile(r"^https://registry\.npmjs\.org/((?:@[^/]+/)?[^/]+)/-/")

ALLOWED_DOWNLOAD_HOSTS = (
    "https://github.com/",
    "https://api.github.com/",
    "https://registry.npmjs.org/",
)

SKIP_REPOS = {("djunekz", "archive")}


@dataclass
class Result:
    name: str
    status: str = "current"
    old: str = ""
    new: str = ""
    reason: str = ""
    new_srcurl: str = ""
    new_sha256: str = ""


@dataclass
class Source:
    kind: str
    owner: str = ""
    repo: str = ""
    npm_name: str = ""
    prefix_len: int = 0
    ext: str = ""
    sha: str = ""


class RateLimited(Exception):
    pass


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def read_var(text: str, var: str) -> str | None:
    m = re.search(rf"^{var}=(.*)$", text, re.MULTILINE)
    return _unquote(m.group(1)) if m else None


def set_var(text: str, var: str, new_value: str) -> tuple[str, bool]:
    pattern = re.compile(rf"^({var}=)(.*)$", re.MULTILINE)

    def repl(m: re.Match) -> str:
        old = m.group(2).strip()
        quote = old[0] if len(old) >= 2 and old[0] == old[-1] and old[0] in "\"'" else ""
        return f"{m.group(1)}{quote}{new_value}{quote}"

    new_text, n = pattern.subn(repl, text, count=1)
    return new_text, n == 1


def expand(url: str, version: str) -> str:
    return url.replace("${TERMUX_PKG_VERSION}", version).replace("$TERMUX_PKG_VERSION", version)


def normalize_tag(tag: str) -> str:
    return re.sub(r"^[vV]\.?", "", tag.strip())


def version_key(version: str) -> tuple[int, ...]:
    return tuple(int(x) for x in re.findall(r"\d+", version))


def is_newer(new: str, old: str) -> bool:
    kn, ko = version_key(new), version_key(old)
    if not kn:
        return False
    width = max(len(kn), len(ko))
    kn += (0,) * (width - len(kn))
    ko += (0,) * (width - len(ko))
    return kn > ko


class Fetcher:
    def __init__(self, token: str | None):
        self.token = token
        self._cache: dict[str, object] = {}

    def get_json(self, url: str):
        if url in self._cache:
            return self._cache[url]
        headers = {
            "User-Agent": USER_AGENT,
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token and url.startswith("https://api.github.com/"):
            headers["Authorization"] = f"Bearer {self.token}"

        last = "unknown error"
        for attempt in range(RETRIES):
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=API_TIMEOUT) as r:
                    data = json.loads(r.read().decode("utf-8", errors="replace"))
                self._cache[url] = data
                return data
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    self._cache[url] = None
                    return None
                if e.code in (403, 429) and (
                    e.headers.get("X-RateLimit-Remaining") == "0" or e.headers.get("Retry-After")
                ):
                    raise RateLimited(f"rate limited by {url}")
                last = f"HTTP {e.code}"
                if e.code < 500:
                    break
            except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as e:
                last = str(e)
            time.sleep(2 * (attempt + 1))
        raise RuntimeError(f"request failed ({last}): {url}")

    @staticmethod
    def sha256_of(url: str) -> tuple[str, int]:
        if not url.startswith(ALLOWED_DOWNLOAD_HOSTS):
            raise RuntimeError(f"refusing to download from unexpected host: {url}")
        last = "unknown error"
        for attempt in range(RETRIES):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
                digest, size = hashlib.sha256(), 0
                with urllib.request.urlopen(req, timeout=DOWNLOAD_TIMEOUT) as r:
                    while True:
                        chunk = r.read(65536)
                        if not chunk:
                            break
                        size += len(chunk)
                        if size > MAX_DOWNLOAD_BYTES:
                            raise RuntimeError("download exceeds size limit")
                        digest.update(chunk)
                if size == 0:
                    raise RuntimeError("empty download")
                return digest.hexdigest(), size
            except urllib.error.HTTPError as e:
                last = f"HTTP {e.code}"
                if e.code < 500:
                    break
            except (urllib.error.URLError, TimeoutError, OSError) as e:
                last = str(e)
            time.sleep(2 * (attempt + 1))
        raise RuntimeError(f"download failed ({last}): {url}")


def classify(raw_url: str, version: str) -> Source | None:
    m = COMMIT_ARCHIVE_RE.match(raw_url)
    if m and COMMIT_VERSION_RE.match(version):
        return Source("commit", m.group(1), m.group(2), prefix_len=m.end(), ext=m.group(4), sha=m.group(3))
    m = GITHUB_RE.match(raw_url) or GITHUB_API_RE.match(raw_url)
    if m:
        return Source("github", m.group(1), m.group(2), prefix_len=m.end())
    m = NPM_RE.match(raw_url)
    if m:
        return Source("npm", npm_name=m.group(1), prefix_len=m.end())
    return None


def latest_github_tag(api: Fetcher, owner: str, repo: str) -> str | None:
    base = f"https://api.github.com/repos/{owner}/{repo}"
    release = api.get_json(f"{base}/releases/latest")
    if isinstance(release, dict) and release.get("tag_name"):
        return release["tag_name"]

    tags = api.get_json(f"{base}/tags?per_page=100")
    best: tuple[tuple[int, ...], str] | None = None
    for t in tags or []:
        tag = (t or {}).get("name", "")
        ver = normalize_tag(tag)
        if not VERSION_RE.match(ver) or PRERELEASE_RE.search(ver):
            continue
        key = version_key(ver)
        if best is None or is_newer(ver, normalize_tag(best[1])):
            best = (key, tag)
    return best[1] if best else None


def latest_npm_version(api: Fetcher, name: str) -> str | None:
    data = api.get_json(f"https://registry.npmjs.org/{name}/latest")
    return data.get("version") if isinstance(data, dict) else None


def head_commit(api: Fetcher, owner: str, repo: str) -> str | None:
    base = f"https://api.github.com/repos/{owner}/{repo}"
    info = api.get_json(base)
    if not isinstance(info, dict):
        return None
    commit = api.get_json(f"{base}/commits/{info.get('default_branch', 'main')}")
    sha = commit.get("sha") if isinstance(commit, dict) else None
    return sha if sha and re.fullmatch(r"[0-9a-f]{40}", sha) else None


def rebuild_srcurl(raw_url: str, prefix_len: int, old: str, new: str) -> str | None:
    head, tail = raw_url[:prefix_len], raw_url[prefix_len:]
    new_tail = tail.replace(old, new)
    uses_variable = "TERMUX_PKG_VERSION" in tail
    if new_tail == tail and not uses_variable:
        return None
    return head + new_tail


def process_package(name: str, api: Fetcher, include_commit_pinned: bool) -> Result:
    res = Result(name)
    path = PACKAGES_DIR / name / "build.sh"
    try:
        text = path.read_bytes().decode("utf-8")
    except (OSError, UnicodeDecodeError) as e:
        res.status, res.reason = "error", f"cannot read build.sh: {e}"
        return res

    version = read_var(text, "TERMUX_PKG_VERSION") or ""
    raw_url = read_var(text, "TERMUX_PKG_SRCURL") or ""
    cur_sha = read_var(text, "TERMUX_PKG_SHA256")
    res.old = version

    if (read_var(text, "TERMUX_PKG_AUTO_UPDATE") or "").lower() == "false":
        res.status, res.reason = "skipped", "TERMUX_PKG_AUTO_UPDATE=false"
        return res
    if not version or not raw_url or cur_sha is None:
        res.status, res.reason = "error", "TERMUX_PKG_VERSION/SRCURL/SHA256 missing"
        return res
    if "/archive/refs/heads/" in raw_url:
        res.status, res.reason = "skipped", "floating branch source (re-pin it first)"
        return res

    src = classify(raw_url, version)
    if src is None:
        res.status, res.reason = "skipped", "unsupported source host"
        return res
    if src.kind in ("github", "commit") and (src.owner.lower(), src.repo.lower()) in SKIP_REPOS:
        res.status, res.reason = "skipped", "shared source repository"
        return res
    if src.kind == "commit" and not include_commit_pinned:
        res.status, res.reason = "skipped", "pinned to a commit"
        return res

    try:
        if src.kind == "commit":
            sha = head_commit(api, src.owner, src.repo)
            if not sha:
                res.status, res.reason = "error", "cannot resolve default branch HEAD"
                return res
            if sha == src.sha or sha.startswith(src.sha):
                return res
            new_version = f"0.0.0+{sha[:7]}"
            new_raw = f"https://github.com/{src.owner}/{src.repo}/archive/{sha}{src.ext}"
        else:
            if src.kind == "github":
                tag = latest_github_tag(api, src.owner, src.repo)
                upstream = normalize_tag(tag) if tag else None
            else:
                upstream = latest_npm_version(api, src.npm_name)
            if not upstream:
                res.status, res.reason = "error", "no upstream release or tag found"
                return res
            if not VERSION_RE.match(upstream):
                res.status, res.reason = "error", f"unrecognised upstream version '{upstream}'"
                return res
            if not is_newer(upstream, version):
                return res
            new_version = upstream
            new_raw = rebuild_srcurl(raw_url, src.prefix_len, version, new_version)
            if new_raw is None:
                res.status, res.reason = "error", "cannot locate the version inside TERMUX_PKG_SRCURL"
                return res

        res.new = new_version
        res.new_srcurl = new_raw
        new_sha, _size = api.sha256_of(expand(new_raw, new_version))
    except RateLimited:
        raise
    except RuntimeError as e:
        res.status, res.reason = "error", str(e)
        return res

    if not SHA_RE.match(new_sha):
        res.status, res.reason = "error", "computed SHA256 is malformed"
        return res
    if new_sha == cur_sha:
        res.status = "error"
        res.reason = "new SHA256 equals the old one (the URL did not change the file)"
        return res

    res.new_sha256 = new_sha
    res.status = "update"
    return res


def write_update(res: Result) -> None:
    if res.status != "update" or not (res.new and res.new_srcurl and res.new_sha256):
        raise RuntimeError(f"{res.name}: nothing to write")
    path = PACKAGES_DIR / res.name / "build.sh"
    text = path.read_bytes().decode("utf-8")
    for var, value in (
        ("TERMUX_PKG_VERSION", res.new),
        ("TERMUX_PKG_SRCURL", res.new_srcurl),
        ("TERMUX_PKG_SHA256", res.new_sha256),
    ):
        text, ok = set_var(text, var, value)
        if not ok:
            raise RuntimeError(f"{res.name}: {var} not found while writing")
    path.write_bytes(text.encode("utf-8"))
    res.status = "updated"


def update_changelog(path: Path, changes: list[tuple[str, str, str]]) -> None:
    if not changes:
        return
    lines = path.read_text(encoding="utf-8").split("\n")

    start = next((i for i, l in enumerate(lines) if re.match(r"^## \[Unreleased\]", l)), None)
    if start is None:
        raise RuntimeError("`## [Unreleased]` not found in CHANGELOG.md")
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("---") or re.match(r"^## \[", lines[i]):
            end = i
            break

    def entry(name: str, old: str, new: str) -> str:
        return f"- Package `{name}` v{old} → v{new}"

    header = next((i for i in range(start + 1, end) if re.match(r"^### Update\s*$", lines[i])), None)

    if header is None:
        insert_at = end
        while insert_at - 1 > start and lines[insert_at - 1].strip() == "":
            insert_at -= 1
        section = ["", "### Update"] + [entry(*c) for c in changes] + [""]
        lines[insert_at:end] = section
    else:
        for name, old, new in changes:
            sec_end = end
            for i in range(header + 1, end):
                if lines[i].startswith("### "):
                    sec_end = i
                    break
            pattern = re.compile(rf"^- Package `{re.escape(name)}` v(.+?) → v(.+)$")
            hit = next((i for i in range(header + 1, sec_end) if pattern.match(lines[i])), None)
            if hit is not None:
                first_old = pattern.match(lines[hit]).group(1)
                lines[hit] = entry(name, first_old, new)
            else:
                last = header
                for i in range(header + 1, sec_end):
                    if lines[i].strip():
                        last = i
                lines.insert(last + 1, entry(name, old, new))
                end += 1

    path.write_text("\n".join(lines), encoding="utf-8")


def build_summary(results: list[Result], applied: bool) -> str:
    changed = [r for r in results if r.status in ("update", "updated")]
    errors = [r for r in results if r.status == "error"]
    skipped = [r for r in results if r.status == "skipped"]
    current = [r for r in results if r.status == "current"]

    out = ["## 📦 Auto Update Packages", ""]
    out.append(
        f"Checked **{len(results)}** packages — "
        f"**{len(changed)}** {'updated' if applied else 'would be updated'}, "
        f"{len(current)} up to date, {len(skipped)} skipped, {len(errors)} errors."
    )
    if not applied:
        out.append("\n_Dry run: nothing was written._")
    if changed:
        out += ["", "### Update", "", "| Package | Old | New |", "|---|---|---|"]
        out += [f"| `{r.name}` | {r.old} | {r.new} |" for r in changed]
    if errors:
        out += ["", "### ⚠️ Errors", ""]
        out += [f"- `{r.name}` — {r.reason}" for r in errors]
    if skipped:
        by_reason: dict[str, list[str]] = {}
        for r in skipped:
            by_reason.setdefault(r.reason, []).append(r.name)
        out += ["", "<details><summary>Skipped packages</summary>", ""]
        for reason, names in sorted(by_reason.items()):
            out.append(f"- **{reason}** ({len(names)}): " + ", ".join(f"`{n}`" for n in names))
        out += ["", "</details>"]
    return "\n".join(out) + "\n"


def build_commit_message(results: list[Result]) -> str:
    done = [r for r in results if r.status == "updated"]
    subject = f"chore(packages): auto-update {len(done)} package{'s' if len(done) != 1 else ''}"
    body = "\n".join(f"- {r.name}: {r.old} -> {r.new}" for r in done)
    return f"{subject}\n\n{body}\n"


def write_github_output(results: list[Result]) -> None:
    target = os.environ.get("GITHUB_OUTPUT")
    if not target:
        return
    done = [r.name for r in results if r.status == "updated"]
    with open(target, "a", encoding="utf-8") as f:
        f.write(f"changed={'true' if done else 'false'}\n")
        f.write(f"updated_count={len(done)}\n")
        f.write(f"updated_names={' '.join(done)}\n")


def main() -> int:
    ap = argparse.ArgumentParser(description="Check packages against upstream and update build.sh and CHANGELOG.md")
    ap.add_argument("packages", nargs="*", help="package names (default: all)")
    ap.add_argument("--apply", action="store_true", help="write build.sh and CHANGELOG.md")
    ap.add_argument(
        "--include-commit-pinned",
        action="store_true",
        help="also follow packages pinned to a commit (version 0.0.0+sha)",
    )
    ap.add_argument("--out-dir", help="write report.json, summary.md, commit-message.txt here")
    args = ap.parse_args()

    if not PACKAGES_DIR.is_dir():
        print("packages/ not found — run from the repository root", file=sys.stderr)
        return 2

    available = sorted(p.name for p in PACKAGES_DIR.iterdir() if (p / "build.sh").is_file())
    names = args.packages or available
    for n in names:
        if not NAME_RE.match(n) or n not in available:
            print(f"unknown or invalid package name: {n!r}", file=sys.stderr)
            return 2

    api = Fetcher(os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN"))
    results: list[Result] = []

    for i, name in enumerate(names):
        try:
            res = process_package(name, api, args.include_commit_pinned)
        except RateLimited as e:
            print(f"! {e}; stopping, remaining packages not checked", file=sys.stderr)
            results.append(Result(name, "error", reason="GitHub API rate limit reached"))
            results += [Result(n, "skipped", reason="not checked (rate limit)") for n in names[i + 1 :]]
            break
        if res.status == "update" and args.apply:
            write_update(res)
        results.append(res)
        marker = {"current": "=", "update": "↑", "updated": "↑", "skipped": "-", "error": "✗"}[res.status]
        detail = f"{res.old} → {res.new}" if res.new else (res.reason or res.old)
        print(f"{marker} {name}: {detail}", flush=True)

    applied_changes = [(r.name, r.old, r.new) for r in results if r.status == "updated"]
    if args.apply:
        update_changelog(CHANGELOG, applied_changes)

    summary = build_summary(results, args.apply)
    print("\n" + summary)

    if args.out_dir:
        out = Path(args.out_dir)
        out.mkdir(parents=True, exist_ok=True)
        (out / "summary.md").write_text(summary, encoding="utf-8")
        (out / "report.json").write_text(json.dumps([asdict(r) for r in results], indent=2), encoding="utf-8")
        (out / "commit-message.txt").write_text(build_commit_message(results), encoding="utf-8")
    write_github_output(results)
    return 0


if __name__ == "__main__":
    sys.exit(main())
