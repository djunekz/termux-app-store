#!/usr/bin/env python3
# Termux App Store -- Package Scaffold Wizard
# Semi-Auto create build.sh
# github.com/djunekz/termux-app-store

import os
import sys
import re
import shutil
import textwrap
import urllib.request
import urllib.error
import json
import hashlib
from pathlib import Path

R    = "\033[0m"
B    = "\033[1m"
DIM  = "\033[2m"
IT   = "\033[3m"

BRED = "\033[91m"
BGRN = "\033[92m"
BYLW = "\033[93m"
BCYN = "\033[96m"
BWHT = "\033[97m"

BG_BBLK = "\033[100m"
BG_BBLU = "\033[104m"

_PREFIX     = os.environ.get("PREFIX", "/data/data/com.termux/files/usr")
TIMEOUT     = 10

VALID_LICENSES = [
    "MIT", "Apache-2.0", "GPL-2.0", "GPL-3.0", "LGPL-2.1", "LGPL-3.0",
    "BSD-2-Clause", "BSD-3-Clause", "ISC", "MPL-2.0", "AGPL-3.0",
    "Unlicense", "CC0-1.0", "UNKNOWN",
]

BUILD_METHODS = [
    ("python-script", "Python script (copy + wrapper)"),
    ("pip",           "Python package (pip install)"),
    ("shell",         "Shell script (bash/sh)"),
    ("npm",           "Node.js (npm install)"),
    ("cargo",         "Rust (cargo build)"),
    ("go",            "Go (go build)"),
    ("make",          "Makefile (make install)"),
    ("cmake",         "CMake project"),
    ("ruby",          "Ruby (gem)"),
    ("perl",          "Perl script"),
    ("lua",           "Lua script"),
    ("php",           "PHP script"),
    ("unknown",       "Other / manual"),
]

VERSION_RE = re.compile(r"^\d[\w.\-+]*$")

def TW(): return shutil.get_terminal_size((72, 24)).columns
def W():  return min(TW(), 76)

def strip_ansi(s):
    out, i = "", 0
    while i < len(s):
        if s[i] == "\033":
            while i < len(s) and s[i] != "m": i += 1
        else:
            out += s[i]
        i += 1
    return out

def vlen(s): return len(strip_ansi(s))

def vcenter(text, width=None):
    if width is None: width = W()
    pad = max(0, (width - vlen(text)) // 2)
    return " " * pad + text

def rule(char="─", color=DIM, width=None):
    if width is None: width = W()
    print(f"{color}{char * width}{R}")

def thick_rule(color=BCYN, width=None):
    if width is None: width = W()
    print(f"{color}{'━' * width}{R}")

def blank(): print()

def header_bar(title, width=None):
    if width is None: width = W()
    plain = f"  {title}  "
    pad   = max(0, width - len(plain))
    print(f"{BCYN}{'▄' * width}{R}")
    print(f"{BG_BBLU}{BWHT}{B}  {title}  {R}{BG_BBLU}{' ' * pad}{R}")
    print(f"{BCYN}{'▀' * width}{R}")

def subsection(title):
    blank()
    print(f"  {BCYN}{B}>{R} {B}{BWHT}{title}{R}")
    print(f"  {DIM}{'─' * (W() - 2)}{R}")

def info(msg):  print(f"      {DIM}{msg}{R}")
def ok(msg):    print(f"  {BGRN}{B}OK{R}  {msg}")
def warn(msg):  print(f"  {BYLW}{B}!!{R}  {msg}")
def err(msg):   print(f"  {BRED}{B}XX{R}  {msg}", file=sys.stderr)
def log(msg):   print(f"  {BCYN}{B}::{R} {msg}")

def sep(): rule("─", DIM)

def code_line(cmd, indent=4):
    print(f"{' ' * indent}{BYLW}${R} {BCYN}{cmd}{R}")

def callout(label, text, style="note"):
    styles = {
        "note":    (BYLW, "CATATAN"),
        "tip":     (BGRN, "TIP"),
        "warning": (BRED, "WARNING"),
    }
    col, default_lbl = styles.get(style, styles["note"])
    lbl  = label or default_lbl
    w    = W() - 4
    fill = max(0, w - len(lbl) - 5)
    print(f"  {col}╭─[ {B}{lbl}{R}{col} ]{'─' * fill}╮{R}")
    for ln in textwrap.wrap(text, w - 4) or [""]:
        pad = max(0, w - 4 - len(ln))
        print(f"  {col}│{R}  {ln}{' ' * pad}  {col}│{R}")
    print(f"  {col}╰{'─' * w}╯{R}")

def path_box(label, path, color=BCYN):
    w      = W() - 6
    dash_w = w + 2
    lbl    = f" {label} "
    fill   = max(0, dash_w - len(lbl))
    pad    = max(0, w - len(path))
    print(f"  {DIM}┌{lbl}{'─' * fill}┐{R}")
    print(f"  {DIM}│{R} {color}{path}{R}{' ' * pad} {DIM}│{R}")
    print(f"  {DIM}└{'─' * dash_w}┘{R}")

_LOGO = """\
 ████████╗ █████╗ ███████╗
    ██╔══╝██╔══██╗██╔════╝
    ██║   ███████║███████╗
    ██║   ██╔══██║╚════██║
    ██║   ██║  ██║███████║
    ╚═╝   ╚═╝  ╚═╝╚══════╝"""

def banner():
    w = W()
    thick_rule(BCYN, w)
    blank()
    for line in _LOGO.splitlines():
        print(vcenter(f"{BCYN}{B}{line}{R}", w))
    blank()
    print(vcenter(f"{BWHT}{B}Termux App Store{R}  {DIM}--  Package Scaffold Wizard{R}", w))
    print(vcenter(f"{DIM}Create a new build.sh step by step{R}", w))
    blank()
    thick_rule(BCYN, w)
    blank()

def ask(prompt, default="", validator=None, hint=""):
    while True:
        if hint:
            print(f" {DIM}{IT}{hint}{R}")
        if default:
            display = f"{BCYN}{B}•{R}  {prompt} {DIM}[{default}]{R} "
        else:
            display = f"{BCYN}{B}•{R}  {prompt}: "
        print(display, end="", flush=True)
        try:
            val = input().strip()
        except (EOFError, KeyboardInterrupt):
            blank()
            sys.exit(130)
        if not val and default:
            val = default
        if not val:
            print(f" {BRED}This field is required.{R}")
            continue
        if validator:
            err_msg = validator(val)
            if err_msg:
                print(f" {BRED}{err_msg}{R}")
                continue
        return val

def ask_optional(prompt, default="", hint=""):
    if hint:
        print(f" {DIM}{IT}{hint}{R}")
    if default:
        display = f"{BCYN}{B}•{R}  {prompt} {DIM}[{default}]{R} {DIM}(Enter to skip){R} "
    else:
        display = f"{BCYN}{B}•{R}  {prompt}: {DIM}(Enter to skip){R} "
    print(display, end="", flush=True)
    try:
        val = input().strip()
    except (EOFError, KeyboardInterrupt):
        blank()
        sys.exit(130)
    return val if val else default

def ask_choice(prompt, choices, default_idx=0):
    blank()
    print(f"  {BCYN}{B}?{R}  {prompt}")
    blank()
    for i, (key, label) in enumerate(choices, 1):
        marker = f"{BGRN}{B}>{R}" if i - 1 == default_idx else " "
        print(f"    {marker} {BCYN}{i:>2}.{R}  {label}")
    blank()
    sep()
    while True:
        print(f"  {DIM}Enter number [{default_idx + 1}]:{R} ", end="", flush=True)
        try:
            val = input().strip()
        except (EOFError, KeyboardInterrupt):
            blank()
            sys.exit(130)
        if not val:
            return choices[default_idx][0]
        try:
            idx = int(val) - 1
            if 0 <= idx < len(choices):
                return choices[idx][0]
        except ValueError:
            pass
        print(f"      {BRED}Enter a number between 1 and {len(choices)}{R}")

def ask_license(default="MIT"):
    blank()
    print(f"  {BCYN}{B}?{R}  License")
    blank()
    for i, lic in enumerate(VALID_LICENSES, 1):
        marker = f"{BGRN}{B}>{R}" if lic == default else " "
        print(f"    {marker} {BCYN}{i:>2}.{R}  {lic}")
    blank()
    print(f"      {DIM}or type a custom license identifier{R}")
    sep()
    while True:
        print(f"  {DIM}Enter number or license [{default}]:{R} ", end="", flush=True)
        try:
            val = input().strip()
        except (EOFError, KeyboardInterrupt):
            blank()
            sys.exit(130)
        if not val:
            return default
        try:
            idx = int(val) - 1
            if 0 <= idx < len(VALID_LICENSES):
                return VALID_LICENSES[idx]
        except ValueError:
            if val:
                return val
        print(f"      {BRED}Invalid choice{R}")

def ask_yn(prompt, default_yes=True):
    hint = f"{BWHT}Y{R}{DIM}/n{R}" if default_yes else f"{DIM}y/{R}{BWHT}N{R}"
    print(f"\n  {DIM}[{hint}]{R} {prompt} ", end="", flush=True)
    try:
        val = input().strip().lower()
    except (EOFError, KeyboardInterrupt):
        blank()
        sys.exit(130)
    if default_yes:
        return val not in ("n", "no")
    return val in ("y", "yes")

def validate_pkg_name(val):
    if not re.match(r"^[a-z0-9][a-z0-9\-]*$", val):
        return "Package name must be lowercase letters, numbers, and hyphens only."
    if len(val) < 2:
        return "Package name must be at least 2 characters."
    return None

def validate_version(val):
    if not VERSION_RE.match(val):
        return "Version must start with a digit (e.g. 1.0.0, 2.3.4-rc1). No 'v' prefix."
    return None

def validate_url(val):
    if not (val.startswith("http://") or val.startswith("https://")):
        return "URL must start with http:// or https://"
    return None

def validate_sha256(val):
    if val.upper() == "SKIP":
        return None
    if not re.match(r"^[0-9a-fA-F]{64}$", val):
        return "SHA256 must be 64 hex characters or 'SKIP'."
    return None

def _http_get(url, timeout=TIMEOUT):
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "tas-scaffold/1.0",
                     "Accept": "application/vnd.github+json"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception:
        return None

def fetch_github_meta(repo_url):
    m = re.match(r"https://github\.com/([^/]+)/([^/\s]+?)(?:\.git)?$", repo_url)
    if not m:
        return {}

    owner, repo = m.group(1), m.group(2)
    log(f"Fetching GitHub metadata for {owner}/{repo}...")

    api = f"https://api.github.com/repos/{owner}/{repo}"
    body = _http_get(api)
    if not body:
        warn("Could not reach GitHub API (offline?).")
        return {}

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return {}

    result = {}
    result["name"]        = re.sub(r"[^a-z0-9\-]", "-",
                                   data.get("name", repo).lower()).strip("-")
    result["description"] = data.get("description") or ""
    result["homepage"]    = data.get("homepage") or repo_url
    if not result["homepage"] or result["homepage"] == "null":
        result["homepage"] = repo_url

    lic = data.get("license") or {}
    result["license"] = lic.get("spdx_id") or lic.get("key") or "UNKNOWN"
    if result["license"] in ("NOASSERTION", "null", ""):
        result["license"] = "UNKNOWN"

    default_branch = data.get("default_branch", "main")

    rel_body = _http_get(f"{api}/releases/latest")
    if rel_body:
        try:
            rel = json.loads(rel_body)
            tag = rel.get("tag_name", "")
            if tag:
                result["version"] = tag.lstrip("v")
                result["srcurl"]  = f"{repo_url}/archive/refs/tags/{tag}.tar.gz"
                ok(f"Latest release: {tag}")
                return result
        except Exception:
            pass

    tags_body = _http_get(f"{api}/tags")
    if tags_body:
        try:
            tags = json.loads(tags_body)
            if isinstance(tags, list) and tags:
                tag = tags[0].get("name", "")
                if tag:
                    result["version"] = tag.lstrip("v")
                    result["srcurl"]  = f"{repo_url}/archive/refs/tags/{tag}.tar.gz"
                    ok(f"No release found, using latest tag: {tag}")
                    return result
        except Exception:
            pass

    warn(f"No release or tag found — pinning to current commit on {default_branch}")
    commit_body = _http_get(f"{api}/commits/{default_branch}")
    if commit_body:
        try:
            commit = json.loads(commit_body)
            sha = commit.get("sha", "")
            commit_date = (commit.get("commit", {}) or {}).get("author", {}).get("date", "")
            if sha:
                date_tag = commit_date[:10].replace("-", "") if commit_date else "unknown"
                result["version"] = f"0.0.0+{sha[:7]}"
                result["srcurl"]  = f"{repo_url}/archive/{sha}.tar.gz"
                info(f"Pinned to commit {sha[:7]} ({date_tag})")
                return result
        except Exception:
            pass

    result["version"] = "0.0.0"
    result["srcurl"]  = f"{repo_url}/archive/refs/heads/{default_branch}.tar.gz"
    warn(f"Could not resolve a release, tag, or commit SHA — "
         f"falling back to floating branch '{default_branch}'.")
    warn("This package will need manual re-pinning before it's safe to trust long-term.")

    return result

def compute_sha256_from_url(url):
    log(f"Downloading to compute SHA256...")
    info(url)
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "tas-scaffold/1.0"}
        )
        h = hashlib.sha256()
        total = 0
        with urllib.request.urlopen(req, timeout=30) as r:
            while True:
                chunk = r.read(65536)
                if not chunk:
                    break
                h.update(chunk)
                total += len(chunk)
                print(f"\r  {DIM}Downloaded {total // 1024} KB...{R}   ", end="", flush=True)
        print(f"\r{' ' * 40}\r", end="")
        return h.hexdigest()
    except Exception as e:
        print(f"\r{' ' * 40}\r", end="")
        warn(f"Download failed: {e}")
        return None

def _wrap_quoted(val):
    if " " in val:
        return f'"{val}"'
    return val

INSTALL_TEMPLATES = {
    "python-script": '''\
termux_step_make_install() {{
    local libdir="$TERMUX_PREFIX/lib/{pkg}"
    mkdir -p "$libdir"
    cp -r . "$libdir/"

    find "$libdir" -type d | while read -r _dir; do
        ls "$_dir"/*.py &>/dev/null 2>&1 && [ ! -f "$_dir/__init__.py" ] && \\
            touch "$_dir/__init__.py"
    done

    cat > "$TERMUX_PREFIX/bin/{pkg}" <<\'WRAPPER\'
#!/data/data/com.termux/files/usr/bin/bash
cd "/data/data/com.termux/files/usr/lib/{pkg}" || exit 1
exec python3 "/data/data/com.termux/files/usr/lib/{pkg}/{entrypoint}" "$@"
WRAPPER
    chmod 0755 "$TERMUX_PREFIX/bin/{pkg}"
}}''',

    "pip": '''\
termux_step_make_install() {{
    pip install --quiet setuptools wheel --break-system-packages 2>/dev/null || true
    pip install . --prefix="$TERMUX_PREFIX" --no-deps --break-system-packages 2>/dev/null \\
        || pip install . --prefix="$TERMUX_PREFIX" --no-deps --no-build-isolation \\
               --break-system-packages
}}''',

    "shell": '''\
termux_step_make_install() {{
    local libdir="$TERMUX_PREFIX/lib/{pkg}"
    mkdir -p "$libdir"
    cp -r . "$libdir/"
    chmod 0755 "$libdir/{entrypoint}"

    cat > "$TERMUX_PREFIX/bin/{pkg}" <<\'WRAPPER\'
#!/data/data/com.termux/files/usr/bin/bash
exec bash "/data/data/com.termux/files/usr/lib/{pkg}/{entrypoint}" "$@"
WRAPPER
    chmod 0755 "$TERMUX_PREFIX/bin/{pkg}"
}}''',

    "npm": '''\
termux_step_make_install() {{
    npm install --prefix "$TERMUX_PREFIX" -g .
}}''',

    "cargo": '''\
termux_step_make_install() {{
    cargo install --locked --path . --root "$TERMUX_PREFIX"
}}''',

    "go": '''\
termux_step_make_install() {{
    export GOPATH="$PWD/gopath"
    export GOPROXY="https://proxy.golang.org,direct"
    go mod tidy 2>/dev/null || true
    go build -v -o "$TERMUX_PREFIX/bin/{pkg}" .
}}''',

    "make": '''\
termux_step_make() {{
    make -j"$(nproc)" PREFIX="$TERMUX_PREFIX"
}}

termux_step_make_install() {{
    make install PREFIX="$TERMUX_PREFIX"
}}''',

    "cmake": '''\
TERMUX_PKG_EXTRA_CONFIGURE_ARGS="
    -DCMAKE_BUILD_TYPE=Release
    -DCMAKE_INSTALL_PREFIX=$TERMUX_PREFIX
"''',

    "ruby": '''\
termux_step_make_install() {{
    ls *.gemspec 2>/dev/null && gem build *.gemspec && gem install --local *.gem --no-document \\
        || {{ mkdir -p "$TERMUX_PREFIX/lib/{pkg}"; cp -r . "$TERMUX_PREFIX/lib/{pkg}/"; }}
}}''',

    "perl": '''\
termux_step_make_install() {{
    local libdir="$TERMUX_PREFIX/lib/{pkg}"
    mkdir -p "$libdir"
    cp -r . "$libdir/"
    cat > "$TERMUX_PREFIX/bin/{pkg}" <<\'WRAPPER\'
#!/data/data/com.termux/files/usr/bin/bash
exec perl "/data/data/com.termux/files/usr/lib/{pkg}/{entrypoint}" "$@"
WRAPPER
    chmod 0755 "$TERMUX_PREFIX/bin/{pkg}"
}}''',

    "lua": '''\
termux_step_make_install() {{
    install -Dm755 "{entrypoint}" "$TERMUX_PREFIX/bin/{pkg}"
}}''',

    "php": '''\
termux_step_make_install() {{
    mkdir -p "$TERMUX_PREFIX/lib/{pkg}"
    cp -r . "$TERMUX_PREFIX/lib/{pkg}/"
    cat > "$TERMUX_PREFIX/bin/{pkg}" <<\'WRAPPER\'
#!/usr/bin/env bash
exec php "/data/data/com.termux/files/usr/lib/{pkg}/{entrypoint}" "$@"
WRAPPER
    chmod 0755 "$TERMUX_PREFIX/bin/{pkg}"
}}''',

    "unknown": '''\
termux_step_make_install() {{
    # TODO: implement install steps
    echo "Placeholder -- edit this function"
    mkdir -p "$TERMUX_PREFIX/lib/{pkg}"
    cp -r . "$TERMUX_PREFIX/lib/{pkg}/"
}}''',
}

DEPENDS_FOR_METHOD = {
    "python-script": "python",
    "pip":           "python, python-pip",
    "npm":           "nodejs",
    "cargo":         "rust",
    "go":            "golang",
    "ruby":          "ruby",
    "perl":          "perl",
    "lua":           "lua54",
    "php":           "php",
    "cmake":         "libandroid-support",
}

_METHOD_SIGNALS = [
    ("Cargo.toml",      "cargo"),
    ("go.mod",          "go"),
    ("package.json",    "npm"),
    ("pyproject.toml",  "pip"),
    ("setup.py",        "pip"),
    ("setup.cfg",       "pip"),
    ("CMakeLists.txt",  "cmake"),
    ("Makefile",        "make"),
    ("makefile",        "make"),
    ("GNUmakefile",     "make"),
    ("Gemfile",         "ruby"),
    ("*.gemspec",       "ruby"),
]

_SCRIPT_EXT = {
    ".py":  "python-script",
    ".sh":  "shell",
    ".bash": "shell",
    ".pl":  "perl",
    ".lua": "lua",
    ".php": "php",
}

_SHEBANG_METHOD = [
    ("python", "python-script"),
    ("bash",   "shell"),
    ("/sh",    "shell"),
    ("env sh", "shell"),
    ("perl",   "perl"),
    ("lua",    "lua"),
    ("php",    "php"),
]

def _repo_parts(repo_url):
    m = re.match(r"https://github\.com/([^/]+)/([^/\s]+?)(?:\.git)?/?$", repo_url)
    return (m.group(1), m.group(2)) if m else (None, None)

def fetch_repo_tree(repo_url, default_branch="main"):
    owner, repo = _repo_parts(repo_url)
    if not owner:
        return None
    body = _http_get(
        f"https://api.github.com/repos/{owner}/{repo}/git/trees/{default_branch}")
    if not body:
        return None
    try:
        tree = json.loads(body).get("tree", [])
    except Exception:
        return None
    return [{"path": t["path"], "size": t.get("size", 0)}
            for t in tree if t.get("type") == "blob"]

def _sniff_shebang(repo_url, branch, path):
    owner, repo = _repo_parts(repo_url)
    body = _http_get(f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}")
    if not body:
        return None
    first = body.split("\n", 1)[0]
    if not first.startswith("#!"):
        return None
    for needle, method in _SHEBANG_METHOD:
        if needle in first:
            return method
    return None

def detect_entrypoints(repo_url, branch, files):
    found = []
    for f in files:
        name = f["path"]
        ext = os.path.splitext(name)[1].lower()
        if ext in _SCRIPT_EXT:
            found.append((name, _SCRIPT_EXT[ext]))
        elif ext == "" and name.isascii() and 0 < f["size"] < 500_000 \
                and not name.upper().startswith(("LICENSE", "README", "MAKEFILE",
                                                 "DOCKERFILE", "CHANGELOG",
                                                 "AUTHORS", "CODEOWNERS")):
            m = _sniff_shebang(repo_url, branch, name)
            if m:
                found.append((name, m))
    return found

def rank_entrypoints(found, pkg):
    preferred = [f"{pkg}", f"{pkg}.py", f"{pkg}.sh", "main.py", "main.sh",
                 "run", "run.sh", "start", "start.sh", "app.py", "cli.py"]
    def score(item):
        n = item[0]
        for i, p in enumerate(preferred):
            if n == p:
                return i
        if n.lower() in ("setup.py", "install", "install.sh", "uninstall.sh",
                         "conftest.py"):
            return 900
        return 100
    return sorted(found, key=score)

def detect_method_from_github(repo_url, default_branch="main", files=None):
    if files is None:
        files = fetch_repo_tree(repo_url, default_branch)
    if files is None:
        return None, None

    filenames = {f["path"] for f in files}

    for sig, method in _METHOD_SIGNALS:
        if sig.startswith("*"):
            ext = sig[1:]
            if any(f.endswith(ext) for f in filenames):
                return method, sig
        else:
            if sig in filenames:
                return method, sig

    return None, None


def build_sh_content(data):
    pkg        = data["name"]
    method     = data["method"]
    entrypoint = data.get("entrypoint", f"{pkg}.py")

    template   = INSTALL_TEMPLATES.get(method, INSTALL_TEMPLATES["unknown"])
    install_fn = template.format(pkg=pkg, entrypoint=entrypoint)

    base_dep = DEPENDS_FOR_METHOD.get(method, "")
    extra_dep = data.get("depends", "").strip()
    if base_dep and extra_dep:
        all_deps = f"{base_dep}, {extra_dep}"
    elif base_dep:
        all_deps = base_dep
    else:
        all_deps = extra_dep

    lines = []
    lines.append(f"TERMUX_PKG_HOMEPAGE={data['homepage']}")
    lines.append(f'TERMUX_PKG_DESCRIPTION="{data["description"]}"')
    lines.append(f'TERMUX_PKG_LICENSE="{data["license"]}"')
    lines.append(f'TERMUX_PKG_MAINTAINER="{data["maintainer"]}"')
    lines.append(f"TERMUX_PKG_VERSION={data['version']}")
    lines.append(f"TERMUX_PKG_SRCURL={data['srcurl']}")
    lines.append(f"TERMUX_PKG_SHA256={data['sha256']}")

    if all_deps:
        lines.append(f'TERMUX_PKG_DEPENDS="{all_deps}"')

    if method in ("python-script", "pip", "shell", "npm", "ruby", "perl",
                  "lua", "php", "unknown"):
        lines.append("TERMUX_PKG_BUILD_IN_SRC=true")

    lines.append("")
    lines.append(install_fn)

    return "\n".join(lines) + "\n"

def find_packages_dir():
    candidates = [
        Path("packages"),
        Path(__file__).parent / "packages",
        Path(os.environ.get("PREFIX", "")) / "lib/.tas/packages",
    ]
    for p in candidates:
        if p.is_dir():
            return p
    return Path("packages")

def main():
    args = sys.argv[1:]

    banner()

    prefill_url  = ""
    prefill_name = ""
    if "--from" in args:
        idx = args.index("--from")
        if idx + 1 < len(args):
            prefill_url = args[idx + 1]
    elif args and not args[0].startswith("-"):
        prefill_name = args[0]

    subsection("Step 1  --  Source Repository (optional)")
    blank()

    callout("TIP",
            "If you provide a GitHub URL, metadata (description, license, "
            "version, SHA256) will be fetched automatically.",
            "tip")
    blank()

    github_url = ask_optional(
        "GitHub / GitLab / Codeberg URL",
        default=prefill_url,
        hint="e.g. https://github.com/user/repo (leave blank to fill manually)",
    )

    meta = {}
    if github_url:
        blank()
        meta = fetch_github_meta(github_url)
        if meta:
            blank()
            ok("Metadata fetched:")
            for k, v in meta.items():
                if k not in ("srcurl",):
                    print(f"{DIM}{k:<15}{R}  {BCYN}{v}{R}")
        else:
            warn("Could not fetch metadata. Fill in manually.")
        blank()

    subsection("Step 2  --  Package Information")
    blank()

    pkg_name = ask(
        "Package name",
        default=prefill_name or meta.get("name", ""),
        validator=validate_pkg_name,
        hint="lowercase letters, numbers, hyphens only (e.g. my-tool)",
    )
    blank()

    description = ask(
        "Description",
        default=meta.get("description", ""),
        hint="short single-line description of what the tool does",
    )
    blank()

    homepage = ask(
        "Homepage URL",
        default=meta.get("homepage") or github_url or "",
        validator=validate_url,
        hint="GitHub repo or project website",
    )
    blank()

    license_ = ask_license(default=meta.get("license", "MIT"))
    blank()

    maintainer = ask(
        "Maintainer",
        default="@termux-app-store",
        hint="your GitHub username with @  (e.g. @djunekz)",
    )
    blank()

    version = ask(
        "Version",
        default=meta.get("version", "1.0.0"),
        validator=validate_version,
        hint="must start with a digit, no 'v' prefix (e.g. 1.0.0, 2.3.4-rc1)",
    )
    blank()

    srcurl = ask(
        "SRCURL (source download URL)",
        default=meta.get("srcurl", ""),
        validator=validate_url,
        hint="URL to .tar.gz or .zip. You may use ${TERMUX_PKG_VERSION} as placeholder.",
    )
    blank()

    subsection("Step 3  --  SHA256 Checksum")
    blank()

    sha256 = ""
    want_auto = ask_yn("Compute SHA256 automatically by downloading the source?", default_yes=True)
    blank()

    if want_auto:
        actual_url = srcurl.replace("${TERMUX_PKG_VERSION}", version)
        computed   = compute_sha256_from_url(actual_url)
        if computed:
            ok(f"SHA256: {computed}")
            sha256 = computed
        else:
            warn("Auto-compute failed. Enter SHA256 manually.")
            sha256 = ask(
                "SHA256",
                validator=validate_sha256,
                hint="64-character hex string, or 'SKIP' to bypass verification",
            )
    else:
        sha256 = ask(
            "SHA256",
            default="SKIP",
            validator=validate_sha256,
            hint="64-character hex string, or 'SKIP' to bypass verification",
        )
    blank()

    subsection("Step 4  --  Build Method")

    _detected_method = None
    _detected_signal = None
    _default_branch  = "main"
    _repo_files      = None
    _candidates      = []
    if github_url and meta:
        _owner, _repo = _repo_parts(github_url)
        if _owner:
            _raw = _http_get(f"https://api.github.com/repos/{_owner}/{_repo}")
            if _raw:
                try:
                    _default_branch = json.loads(_raw).get("default_branch", "main")
                except (ValueError, AttributeError):
                    _default_branch = "main"

            log("Scanning repo files to detect how to build it...")
            _repo_files = fetch_repo_tree(github_url, _default_branch)
            if _repo_files is not None:
                _detected_method, _detected_signal = detect_method_from_github(
                    github_url, _default_branch, files=_repo_files)
                if _detected_method:
                    ok(f"Detected: {BCYN}{_detected_method}{R}  {DIM}(found {_detected_signal}){R}")
                else:
                    _candidates = rank_entrypoints(
                        detect_entrypoints(github_url, _default_branch, _repo_files),
                        pkg_name)
                    if _candidates:
                        _detected_method = _candidates[0][1]
                        ok(f"Detected: {BCYN}{_detected_method}{R}  "
                           f"{DIM}(found script {_candidates[0][0]}){R}")
                    else:
                        warn("No build files or runnable script found in the repo root.")
                        info("Files in repo root: " +
                             ", ".join(f["path"] for f in _repo_files[:12]))
                        info("Choose 'Other / manual' and edit build.sh afterwards.")
            else:
                warn("Could not read the repo file list — pick the method manually.")
            blank()

    _default_idx = len(BUILD_METHODS) - 1
    if _detected_method:
        for i, (k, _) in enumerate(BUILD_METHODS):
            if k == _detected_method:
                _default_idx = i
                break
    elif not github_url or not meta:
        _default_idx = 0

    method = ask_choice(
        "How should this package be built / installed?",
        BUILD_METHODS,
        default_idx=_default_idx,
    )
    blank()

    entrypoint = ""
    _needs_entrypoint = method in ("python-script", "shell", "perl", "lua", "php")
    if _needs_entrypoint:
        subsection("Step 5  --  Entrypoint File")
        blank()
        ext_map = {
            "python-script": f"{pkg_name}.py",
            "shell":         f"{pkg_name}.sh",
            "perl":          f"{pkg_name}.pl",
            "lua":           f"{pkg_name}.lua",
            "php":           f"{pkg_name}.php",
        }

        if _repo_files is not None and not _candidates:
            _candidates = rank_entrypoints(
                detect_entrypoints(github_url, _default_branch, _repo_files),
                pkg_name)
        _same = [c for c in _candidates if c[1] == method] or _candidates

        _default_entry = ext_map.get(method, f"{pkg_name}")
        if _same:
            print(f"  {DIM}Runnable files found in the repo root:{R}")
            for n, m in _same[:8]:
                print(f"      {BCYN}{n}{R}  {DIM}({m}){R}")
            blank()
            _default_entry = _same[0][0]

        _root_names = {f["path"] for f in _repo_files} if _repo_files else None
        while True:
            entrypoint = ask(
                "Main entrypoint file",
                default=_default_entry,
                hint="filename relative to source root that starts the program",
            )
            if _root_names is None or entrypoint in _root_names:
                break
            warn(f"'{entrypoint}' does NOT exist in the repo root — "
                 "the build would fail.")
            if not ask_yn("Use it anyway? (e.g. file is in a subfolder)",
                          default_yes=False):
                blank()
                continue
            break
    else:
        entrypoint = f"{pkg_name}"
        if method in ("cargo", "go", "npm", "cmake", "make", "pip"):
            print(f"  {DIM}  Step 5 skipped — entrypoint not needed for {BCYN}{method}{DIM} builds.{R}")
            blank()
        elif method == "unknown":
            callout("NOTE",
                    "build.sh will contain a placeholder install step. Open "
                    f"packages/{pkg_name}/build.sh and edit "
                    "termux_step_make_install() before building.",
                    "warning")
            blank()

    subsection("Step 6  --  Additional Dependencies (optional)")
    blank()

    base_dep = DEPENDS_FOR_METHOD.get(method, "")
    if base_dep:
        print(f"  {DIM}Base dependency for {method}:{R}  {BCYN}{base_dep}{R}")
        blank()

    extra_dep = ask_optional(
        "Extra TERMUX_PKG_DEPENDS",
        hint="comma-separated pkg names (e.g. curl, git)  leave blank if none",
    )

    subsection("Review")
    blank()

    fields = [
        ("name",        pkg_name),
        ("description", description),
        ("homepage",    homepage),
        ("license",     license_),
        ("maintainer",  maintainer),
        ("version",     version),
        ("srcurl",      srcurl),
        ("sha256",      sha256[:16] + "..." if len(sha256) == 64 else sha256),
        ("method",      method),
        ("entrypoint",  entrypoint),
        ("extra deps",  extra_dep or "(none)"),
    ]
    lw = max(len(f[0]) for f in fields) + 2
    print(f"  {DIM}┌{'─' * (W() - 4)}┐{R}")
    for label, val in fields:
        pad = max(0, W() - 4 - 2 - lw - 2 - len(val))
        print(f"  {DIM}│{R} {DIM}{label:<{lw}}{R}  {BCYN}{val}{R}{' ' * pad} {DIM}│{R}")
    print(f"  {DIM}└{'─' * (W() - 4)}┘{R}")
    blank()

    if not ask_yn("Write build.sh?", default_yes=True):
        blank()
        warn("Aborted. No files written.")
        blank()
        sys.exit(0)

    data = {
        "name":        pkg_name,
        "description": description,
        "homepage":    homepage,
        "license":     license_,
        "maintainer":  maintainer,
        "version":     version,
        "srcurl":      srcurl,
        "sha256":      sha256,
        "method":      method,
        "entrypoint":  entrypoint,
        "depends":     extra_dep,
    }

    packages_dir = find_packages_dir()
    pkg_dir      = packages_dir / pkg_name
    build_sh     = pkg_dir / "build.sh"

    pkg_dir.mkdir(parents=True, exist_ok=True)
    content = build_sh_content(data)

    build_sh.write_text(content)
    build_sh.chmod(0o755)

    blank()
    thick_rule(BGRN)
    print(vcenter(f"{BGRN}{B}build.sh created{R}", W()))
    thick_rule(BGRN)
    blank()
    path_box("file", str(build_sh))
    blank()

    subsection("build.sh preview")
    blank()
    w      = W() - 6
    dash_w = w + 2
    print(f"  {DIM}┌ build.sh {'─' * (dash_w - 10)}┐{R}")
    for line in content.splitlines():
        if line.startswith("TERMUX_PKG_"):
            key, _, val = line.partition("=")
            display = f"{BCYN}{key}{R}={BYLW}{val}{R}"
        elif line.startswith("termux_step_"):
            display = f"{BGRN}{line}{R}"
        elif line.startswith("#"):
            display = f"{DIM}{line}{R}"
        else:
            display = line
        pad = max(0, w - len(strip_ansi(display)))
        print(f"  {DIM}│{R} {display}{' ' * pad} {DIM}│{R}")
    print(f"  {DIM}└{'─' * dash_w}┘{R}")
    blank()

    subsection("Next steps")
    blank()
    code_line(f"./termux-build lint {pkg_name}")
    code_line(f"./termux-build check-pr {pkg_name}")
    code_line(f"./build-package.sh {pkg_name}")
    blank()
    callout("TIP",
            "Run './termux-build lint <name>' to validate your build.sh before submitting a PR.",
            "tip")
    if method in ("python-script", "shell", "perl", "lua", "php"):
        callout("WARNING",
                f"Make sure \'{entrypoint}\' actually exists in the repo root. "
                "If the build fails, the entrypoint may be wrong or the repo uses "
                "a different build system (e.g. \'cargo\' for Rust, \'pip\' for Python packages).",
                "warning")
        blank()

    blank()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        blank()
        rule("─", DIM)
        print(f"  {BYLW}Cancelled.{R}")
        rule("─", DIM)
        blank()
        sys.exit(130)
