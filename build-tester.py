#!/usr/bin/env python3
# Termux App Store -- Build Tester (Dry-run)
# github.com/djunekz/termux-app-store

import os
import sys
import re
import shutil
import textwrap
import subprocess
import urllib.request
import urllib.error
import hashlib
import json
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
BG_BRED = "\033[101m"
BG_BGRN = "\033[102m"
BG_BYLW = "\033[103m"

_PREFIX     = os.environ.get("PREFIX", "/data/data/com.termux/files/usr")
TIMEOUT_NET = 10
TIMEOUT_DL  = 60

REQUIRED_FIELDS = [
    "TERMUX_PKG_HOMEPAGE",
    "TERMUX_PKG_DESCRIPTION",
    "TERMUX_PKG_LICENSE",
    "TERMUX_PKG_MAINTAINER",
    "TERMUX_PKG_VERSION",
    "TERMUX_PKG_SRCURL",
    "TERMUX_PKG_SHA256",
]

FORBIDDEN_PATTERNS = [
    (r"\bsudo\b",                       "sudo usage detected (not allowed in Termux)"),
    (r"\bapt install\b",                "use 'pkg install' instead of 'apt install'"),
    (r"\bapt-get\b",                    "use 'pkg' instead of 'apt-get'"),
    (r"\bdpkg -i\b",                    "dpkg -i not allowed inside termux_step_make_install()"),
    (r"/usr/bin(?!/env)",               "hardcoded /usr/bin (use $TERMUX_PREFIX/bin or #!/usr/bin/env)"),
    (r"/usr/local",                     "hardcoded /usr/local (use $TERMUX_PREFIX)"),
    (r"/home/[a-z]",                    "hardcoded /home/ path (use $HOME or $TERMUX_HOME)"),
    (r"\bchown\b",                      "chown not available in Termux user-space"),
    (r"\bchmod 777\b",                  "chmod 777 is a security risk"),
    (r"rm -rf /",                       "dangerous: rm -rf / or similar"),
    (r"TERMUX_PKG_VERSION=v\d",         "version starts with 'v' (remove the 'v' prefix)"),
]

KNOWN_PKG_DEPS = {
    "python", "python-pip", "python-setuptools", "python-wheel",
    "nodejs", "npm", "rust", "golang", "ruby", "perl", "php",
    "git", "curl", "wget", "jq", "zip", "unzip", "tar",
    "openssl", "libcurl", "libffi", "zlib", "sqlite",
    "clang", "cmake", "ninja", "make", "automake", "autoconf",
    "dpkg", "dpkg-dev", "dpkg-deb",
    "lua54", "figlet", "ffmpeg", "imagemagick", "nmap",
    "openssh", "libssh", "libssh2",
    "libandroid-support", "termux-tools",
    "glib", "glib-dev", "libxml2", "libxml2-dev",
}

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

def ok(msg):    print(f"  {BGRN}{B}OK{R}  {msg}")
def warn(msg):  print(f"  {BYLW}{B}!!{R}  {msg}")
def err(msg):   print(f"  {BRED}{B}XX{R}  {msg}")
def info(msg):  print(f"      {DIM}{msg}{R}")
def log(msg):   print(f"  {BCYN}{B}::{R} {msg}")
def sep():      rule("─", DIM)

def kv(label, value, lw=26, vc=BCYN):
    print(f"  {DIM}{label:<{lw}}{R}  {vc}{value}{R}")

def code_line(cmd, indent=4):
    print(f"{' ' * indent}{BYLW}${R} {BCYN}{cmd}{R}")

def callout(label, text, style="note"):
    styles = {
        "note":    (BYLW, "CATATAN"),
        "tip":     (BGRN, "TIP"),
        "warning": (BRED, "WARNING"),
        "pass":    (BGRN, "PASS"),
        "fail":    (BRED, "FAIL"),
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
    print(vcenter(f"{BWHT}{B}Termux App Store{R}  {DIM}--  Build Tester{R}", w))
    print(vcenter(f"{DIM}Dry-run validation before building or submitting PR{R}", w))
    blank()
    thick_rule(BCYN, w)
    blank()

PASS = "PASS"
WARN = "WARN"
FAIL = "FAIL"
INFO = "INFO"
SKIP = "SKIP"

class Issue:
    def __init__(self, level, category, message, line=None, hint=None):
        self.level    = level
        self.category = category
        self.message  = message
        self.line     = line
        self.hint     = hint

    def print_line(self, indent=2):
        badge = {
            PASS: f"{BGRN}{B}  OK  {R}",
            WARN: f"{BYLW}{B}  !!  {R}",
            FAIL: f"{BRED}{B}  XX  {R}",
            INFO: f"{BCYN}{B}  --  {R}",
            SKIP: f"{DIM}  --  {R}",
        }.get(self.level, f"{DIM}  ??  {R}")

        loc = f" {DIM}(line {self.line}){R}" if self.line else ""
        print(f"{' ' * indent}{badge}  {self.message}{loc}")
        if self.hint and self.level in (FAIL, WARN):
            for ln in textwrap.wrap(self.hint, W() - 12) or []:
                print(f"{' ' * 12}{DIM}{IT}{ln}{R}")

    def to_dict(self):
        return {
            "level":    self.level,
            "category": self.category,
            "message":  self.message,
            "line":     self.line,
            "hint":     self.hint,
        }


def parse_build_sh(path: Path) -> dict:
    values = {}
    lines  = path.read_text(errors="replace").splitlines()

    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r'^(TERMUX_PKG_\w+)=(.*)$', line)
        if not m:
            continue
        key = m.group(1)
        val = m.group(2).strip()
        if (val.startswith('"') and val.endswith('"')) or \
           (val.startswith("'") and val.endswith("'")):
            val = val[1:-1]
        values[key] = val

    ver = values.get("TERMUX_PKG_VERSION", "")
    if ver:
        for k, v in values.items():
            values[k] = v.replace("${TERMUX_PKG_VERSION}", ver)

    return values

def get_all_lines(path: Path) -> list:
    return path.read_text(errors="replace").splitlines()


def test_file_exists(build_sh: Path) -> list:
    if build_sh.exists():
        return [Issue(PASS, "File", f"build.sh found: {build_sh}")]
    return [Issue(FAIL, "File", f"build.sh not found: {build_sh}",
                  hint=f"Create it with: python3 pkg-scaffold.py {build_sh.parent.name}")]

def test_required_fields(values: dict, lines: list) -> list:
    issues = []
    for field in REQUIRED_FIELDS:
        val = values.get(field, "")
        if not val:
            lineno = None
            for i, ln in enumerate(lines, 1):
                if ln.strip().startswith(field):
                    lineno = i
                    break
            if field not in values:
                issues.append(Issue(
                    FAIL, "Fields",
                    f"{field} is missing",
                    line=lineno,
                    hint=f"Add {field}=... to build.sh",
                ))
            else:
                issues.append(Issue(
                    FAIL, "Fields",
                    f"{field} is empty",
                    line=lineno,
                    hint=f"Fill in a value for {field}",
                ))
        else:
            issues.append(Issue(PASS, "Fields", f"{field} is set"))
    return issues

def test_version_format(values: dict, lines: list) -> list:
    ver = values.get("TERMUX_PKG_VERSION", "")
    if not ver:
        return []
    if ver.startswith("v") and re.match(r"^v\d", ver):
        lineno = next((i+1 for i, ln in enumerate(lines)
                       if "TERMUX_PKG_VERSION" in ln), None)
        return [Issue(
            FAIL, "Version",
            f"Version '{ver}' starts with 'v' (not allowed)",
            line=lineno,
            hint=f"Change to TERMUX_PKG_VERSION={ver[1:]}",
        )]
    if not VERSION_RE.match(ver):
        return [Issue(
            WARN, "Version",
            f"Unusual version format: '{ver}'",
            hint="Version should start with a digit (e.g. 1.0.0, 2.3.4-rc1)",
        )]
    return [Issue(PASS, "Version", f"Version format OK: {ver}")]

def test_description(values: dict) -> list:
    desc = values.get("TERMUX_PKG_DESCRIPTION", "")
    if not desc:
        return []
    issues = []
    if len(desc) > 100:
        issues.append(Issue(
            WARN, "Description",
            f"Description is long ({len(desc)} chars, recommended < 100)",
            hint="Keep description short and single-line.",
        ))
    if desc[0].islower():
        issues.append(Issue(
            WARN, "Description",
            "Description should start with a capital letter",
        ))
    if desc.endswith("."):
        issues.append(Issue(
            WARN, "Description",
            "Description should not end with a period",
        ))
    if not issues:
        issues.append(Issue(PASS, "Description", f"Description OK ({len(desc)} chars)"))
    return issues

def test_homepage(values: dict) -> list:
    hp = values.get("TERMUX_PKG_HOMEPAGE", "")
    if not hp:
        return []
    if not (hp.startswith("http://") or hp.startswith("https://")):
        return [Issue(
            FAIL, "Homepage",
            f"Homepage is not a valid URL: {hp}",
            hint="Must start with https://",
        )]
    return [Issue(PASS, "Homepage", f"URL format OK")]

def test_maintainer(values: dict) -> list:
    maint = values.get("TERMUX_PKG_MAINTAINER", "")
    if not maint:
        return []
    if not maint.startswith("@"):
        return [Issue(
            WARN, "Maintainer",
            f"Maintainer '{maint}' does not start with '@'",
            hint="Use your GitHub username with @ prefix, e.g. @djunekz",
        )]
    return [Issue(PASS, "Maintainer", f"Maintainer format OK: {maint}")]

def test_srcurl(values: dict) -> list:
    src = values.get("TERMUX_PKG_SRCURL", "")
    if not src:
        return []
    issues = []
    if not (src.startswith("http://") or src.startswith("https://")):
        issues.append(Issue(
            FAIL, "SRCURL",
            f"SRCURL is not a valid URL: {src[:60]}",
            hint="Must start with https://",
        ))
        return issues
    if "${" in src:
        issues.append(Issue(
            WARN, "SRCURL",
            "SRCURL contains unexpanded shell variable (may be intentional)",
            hint="Ensure variable is defined before SRCURL in build.sh",
        ))
    ext_ok = any(src.endswith(e) for e in
                 (".tar.gz", ".tar.bz2", ".tar.xz", ".tgz", ".zip", ".tar.zst"))
    if not ext_ok:
        issues.append(Issue(
            WARN, "SRCURL",
            "SRCURL does not end with a recognised archive extension",
            hint="Expected: .tar.gz / .zip / .tar.bz2 / .tar.xz / .tar.zst",
        ))
    else:
        issues.append(Issue(PASS, "SRCURL", "URL format OK"))
    return issues

def test_sha256(values: dict) -> list:
    sha = values.get("TERMUX_PKG_SHA256", "")
    if not sha:
        return []
    if sha.upper() == "SKIP":
        return [Issue(
            WARN, "SHA256",
            "SHA256=SKIP disables checksum verification",
            hint="Set a real SHA256 before submitting a PR.",
        )]
    if not re.match(r"^[0-9a-fA-F]{64}$", sha):
        return [Issue(
            FAIL, "SHA256",
            f"SHA256 is not a valid 64-char hex string: {sha[:20]}...",
            hint="Run: python3 build-tester.py <pkg> --deep  to compute it.",
        )]
    return [Issue(PASS, "SHA256", f"{sha[:16]}... (64 chars)")]

def test_license(values: dict) -> list:
    lic = values.get("TERMUX_PKG_LICENSE", "")
    if not lic:
        return []
    bad_values = {"UNKNOWN", "TODO", "", "?", "NOASSERTION"}
    if lic.upper() in bad_values:
        return [Issue(
            WARN, "License",
            f"License is '{lic}' -- please specify a real SPDX identifier",
            hint="e.g. MIT, Apache-2.0, GPL-3.0, BSD-2-Clause",
        )]
    return [Issue(PASS, "License", f"{lic}")]

def test_depends(values: dict) -> list:
    deps_raw = values.get("TERMUX_PKG_DEPENDS", "")
    if not deps_raw:
        return [Issue(INFO, "Depends", "No TERMUX_PKG_DEPENDS set (may be intentional)")]
    issues = []
    deps = [d.strip().split()[0] for d in deps_raw.split(",") if d.strip()]
    for dep in deps:
        if dep not in KNOWN_PKG_DEPS:
            issues.append(Issue(
                WARN, "Depends",
                f"Unknown dependency: '{dep}'",
                hint=f"Verify '{dep}' is installable via: pkg info {dep}",
            ))
    if not issues:
        issues.append(Issue(PASS, "Depends", f"{len(deps)} dep(s): {', '.join(deps)}"))
    return issues

def test_forbidden_patterns(lines: list) -> list:
    issues = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        for pattern, message in FORBIDDEN_PATTERNS:
            if re.search(pattern, line):
                issues.append(Issue(
                    FAIL if "not allowed" in message or "dangerous" in message else WARN,
                    "Lint",
                    message,
                    line=i,
                    hint=f"Line {i}: {line.strip()[:60]}",
                ))
    if not issues:
        issues.append(Issue(PASS, "Lint", "No forbidden patterns found"))
    return issues

def test_install_function(lines: list, values: dict) -> list:
    issues = []
    full_text = "\n".join(lines)
    has_make_install = "termux_step_make_install()" in full_text

    depends    = values.get("TERMUX_PKG_DEPENDS", "").lower()
    build_in   = "TERMUX_PKG_BUILD_IN_SRC" in full_text
    has_extra  = "TERMUX_PKG_EXTRA_CONFIGURE_ARGS" in full_text
    skip_methods = {"cargo", "cmake", "golang", "rust", "make", "autotools"}

    method_needs_fn = True
    if any(k in depends for k in skip_methods):
        method_needs_fn = False
    if has_extra:
        method_needs_fn = False
    if not build_in and not has_make_install:
        lang_deps = {"python", "nodejs", "ruby", "perl", "php", "lua54"}
        if not any(k in depends for k in lang_deps):
            method_needs_fn = False

    if not has_make_install and method_needs_fn:
        issues.append(Issue(
            WARN, "Install function",
            "termux_step_make_install() not found",
            hint="Most packages need a custom install function. "
                 "Add termux_step_make_install() { ... } to build.sh",
        ))
    elif has_make_install:
        issues.append(Issue(PASS, "Install function", "termux_step_make_install() found"))
    else:
        issues.append(Issue(INFO, "Install function",
                            "No install function (using default build flow)"))

    if has_make_install and not build_in:
        issues.append(Issue(
            WARN, "Build in src",
            "TERMUX_PKG_BUILD_IN_SRC not set",
            hint="Most script-based packages need: TERMUX_PKG_BUILD_IN_SRC=true",
        ))
    elif "TERMUX_PKG_BUILD_IN_SRC=true" in full_text:
        issues.append(Issue(PASS, "Build in src", "TERMUX_PKG_BUILD_IN_SRC=true"))

    return issues

def test_prefix_usage(lines: list) -> list:
    issues  = []
    hardcoded  = re.compile(r'/data/data/com\.termux/files/usr(?!/bin/env)')
    heredoc_re = re.compile(r"<<\s*['\"]?(\w+)['\"]?")

    in_heredoc  = False
    heredoc_end = ""

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        if not in_heredoc:
            m = heredoc_re.search(line)
            if m:
                in_heredoc  = True
                heredoc_end = m.group(1)
                continue

        if in_heredoc:
            if stripped == heredoc_end:
                in_heredoc  = False
                heredoc_end = ""
            continue

        if stripped.startswith("#"):
            continue

        if hardcoded.search(line):
            issues.append(Issue(
                WARN, "Prefix",
                "Hardcoded Termux prefix path detected (outside wrapper)",
                line=i,
                hint="Use $TERMUX_PREFIX instead of /data/data/com.termux/files/usr",
            ))

    if not issues:
        issues.append(Issue(PASS, "Prefix",
                            "No hardcoded prefix paths outside wrapper blocks"))
    return issues

def test_wrapper_script(lines: list, values: dict) -> list:
    pkg = values.get("TERMUX_PKG_HOMEPAGE", "").rstrip("/").split("/")[-1]
    full_text = "\n".join(lines)
    if "WRAPPER" not in full_text:
        return [Issue(INFO, "Wrapper", "No wrapper script found (may be intentional)")]
if re.search(r'exec (python3?|bash|node|perl|php|ruby)\s+["\']?/data/', full_text):
        return [Issue(PASS, "Wrapper", "Wrapper uses absolute path (correct for .deb)")]
if re.search(r'exec (python3?|bash|node|perl|php|ruby)\s+["\']?\$TERMUX_PREFIX', full_text):
        return [Issue(
            WARN, "Wrapper",
            "$TERMUX_PREFIX in wrapper — will NOT expand after dpkg install",
            hint="Use absolute path /data/data/com.termux/files/usr/... in wrapper scripts",
        )]
    return [Issue(INFO, "Wrapper", "Wrapper found (verify paths are absolute)")]


def test_url_reachable(values: dict) -> list:
    src = values.get("TERMUX_PKG_SRCURL", "")
    if not src or not src.startswith("http"):
        return [Issue(SKIP, "Network", "SRCURL not a network URL")]
    if "${" in src:
        return [Issue(SKIP, "Network", "SRCURL contains unexpanded variable, skipping network test")]

    log(f"Checking URL reachability...")
    info(src[:60] + ("..." if len(src) > 60 else ""))

    try:
        req = urllib.request.Request(
            src, headers={"User-Agent": "tas-build-tester/1.0"}, method="HEAD"
        )
        with urllib.request.urlopen(req, timeout=TIMEOUT_NET) as r:
            code = r.getcode()
            size = r.headers.get("Content-Length", "?")
        if code == 200:
            size_str = f"{int(size) // 1024} KB" if str(size).isdigit() else "? KB"
            return [Issue(PASS, "Network", f"URL reachable (HTTP 200, size={size_str})")]
        return [Issue(WARN, "Network", f"Unexpected HTTP {code}")]
    except urllib.error.HTTPError as e:
        level = WARN if e.code in (403, 405) else FAIL
        return [Issue(level, "Network",
                      f"HTTP {e.code} {e.reason} (URL may still be valid)",
                      hint="GitHub often blocks HEAD requests. Use --deep to verify.")]
    except urllib.error.URLError as e:
        return [Issue(WARN, "Network", f"URL unreachable: {e.reason}",
                      hint="Check your internet connection or try again later.")]
    except Exception as e:
        return [Issue(WARN, "Network", f"Connection error: {e}")]

def test_sha256_deep(values: dict) -> list:
    src      = values.get("TERMUX_PKG_SRCURL", "")
    expected = values.get("TERMUX_PKG_SHA256", "")

    if not src or not src.startswith("http"):
        return [Issue(SKIP, "SHA256 verify", "No network URL to verify")]
    if "${" in src:
        return [Issue(SKIP, "SHA256 verify", "URL has unexpanded variable")]
    if expected.upper() == "SKIP":
        return [Issue(SKIP, "SHA256 verify", "SHA256=SKIP, skipping deep check")]
    if not re.match(r"^[0-9a-fA-F]{64}$", expected):
        return [Issue(SKIP, "SHA256 verify", "SHA256 is not valid, skipping download")]

    log("Downloading source for SHA256 verification...")
    info(f"URL: {src[:60]}")

    try:
        req = urllib.request.Request(src, headers={"User-Agent": "tas-build-tester/1.0"})
        h = hashlib.sha256()
        total = 0
        with urllib.request.urlopen(req, timeout=TIMEOUT_DL) as r:
            while True:
                chunk = r.read(65536)
                if not chunk:
                    break
                h.update(chunk)
                total += len(chunk)
                print(f"\r      {DIM}Downloaded {total // 1024} KB...{R}   ", end="", flush=True)
        print(f"\r{' ' * 44}\r", end="")
        actual = h.hexdigest()

        if actual == expected.lower():
            return [Issue(PASS, "SHA256 verify",
                         f"SHA256 matches ({total // 1024} KB)")]
        return [Issue(
            FAIL, "SHA256 verify",
            "SHA256 MISMATCH",
            hint=f"Expected: {expected}\nActual:   {actual}\n"
                 f"Update TERMUX_PKG_SHA256={actual}",
        )]
    except Exception as e:
        print(f"\r{' ' * 44}\r", end="")
        return [Issue(WARN, "SHA256 verify", f"Download failed: {e}")]


def test_deps_available(values: dict) -> list:
    deps_raw = values.get("TERMUX_PKG_DEPENDS", "")
    if not deps_raw:
        return []

    if not shutil.which("pkg"):
        return [Issue(INFO, "Dep availability", "pkg not found, skipping dep check")]

    deps = [d.strip().split()[0] for d in deps_raw.split(",") if d.strip()]
    issues = []
    for dep in deps:
        try:
            result = subprocess.run(
                ["pkg", "info", dep],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                ver_m = re.search(r"Version\s*:\s*(\S+)", result.stdout)
                ver = ver_m.group(1) if ver_m else "?"
                issues.append(Issue(PASS, "Dep availability", f"{dep} available ({ver})"))
            else:
                issues.append(Issue(
                    WARN, "Dep availability",
                    f"'{dep}' not found via pkg",
                    hint=f"Verify: pkg info {dep}  -- may need a different package name",
                ))
        except subprocess.TimeoutExpired:
            issues.append(Issue(WARN, "Dep availability", f"Timeout checking {dep}"))
        except Exception as e:
            issues.append(Issue(INFO, "Dep availability", f"Could not check {dep}: {e}"))
    return issues


class PackageResult:
    def __init__(self, pkg_name, build_sh):
        self.pkg_name = pkg_name
        self.build_sh = build_sh
        self.issues   = []

    def add(self, new_issues):
        self.issues.extend(new_issues)

    @property
    def n_pass(self):  return sum(1 for i in self.issues if i.level == PASS)
    @property
    def n_warn(self):  return sum(1 for i in self.issues if i.level == WARN)
    @property
    def n_fail(self):  return sum(1 for i in self.issues if i.level == FAIL)
    @property
    def verdict(self):
        if self.n_fail > 0: return FAIL
        if self.n_warn > 0: return WARN
        return PASS

    def to_dict(self):
        return {
            "package": self.pkg_name,
            "verdict": self.verdict,
            "pass":    self.n_pass,
            "warn":    self.n_warn,
            "fail":    self.n_fail,
            "issues":  [i.to_dict() for i in self.issues],
        }


def run_tests(pkg_name, build_sh: Path, deep=False, check_deps=False) -> PackageResult:
    result = PackageResult(pkg_name, build_sh)

    file_issues = test_file_exists(build_sh)
    result.add(file_issues)
    if any(i.level == FAIL for i in file_issues):
        return result

    try:
        values = parse_build_sh(build_sh)
        lines  = get_all_lines(build_sh)
    except Exception as e:
        result.add([Issue(FAIL, "Parse", f"Failed to read build.sh: {e}")])
        return result

    result.add(test_required_fields(values, lines))

    result.add(test_version_format(values, lines))
    result.add(test_description(values))
    result.add(test_homepage(values))
    result.add(test_maintainer(values))
    result.add(test_srcurl(values))
    result.add(test_sha256(values))
    result.add(test_license(values))
    result.add(test_depends(values))

    result.add(test_forbidden_patterns(lines))
    result.add(test_prefix_usage(lines))
    result.add(test_install_function(lines, values))
    result.add(test_wrapper_script(lines, values))

    result.add(test_url_reachable(values))

    if check_deps:
        result.add(test_deps_available(values))

    if deep:
        result.add(test_sha256_deep(values))

    return result


def print_result(result: PackageResult, verbose=True):
    w = W()

    verdict_col = {PASS: BGRN, WARN: BYLW, FAIL: BRED}.get(result.verdict, DIM)
    pkg_label   = f"  {result.pkg_name}  "
    verdict_lbl = f"  {result.verdict}  "
    pad         = max(0, w - len(pkg_label) - len(verdict_lbl))
    print(f"{BG_BBLK}{BWHT}{B}{pkg_label}{R}{BG_BBLK}{' ' * pad}{verdict_col}{B}{verdict_lbl}{R}")
    blank()

    if not verbose:
        print(f"  {BGRN}pass={result.n_pass}{R}  "
              f"{BYLW}warn={result.n_warn}{R}  "
              f"{BRED}fail={result.n_fail}{R}")
        blank()
        return

    categories = {}
    for issue in result.issues:
        categories.setdefault(issue.category, []).append(issue)

    for cat, issues in categories.items():
        n_fail = sum(1 for i in issues if i.level == FAIL)
        n_warn = sum(1 for i in issues if i.level == WARN)
        cat_col = BRED if n_fail else (BYLW if n_warn else DIM)
        print(f"  {cat_col}{DIM}{cat}{R}")
        for issue in issues:
            issue.print_line(indent=4)
        blank()

    sep()
    print(f"  {DIM}{'pass':<6}{R} {BGRN}{B}{result.n_pass:<4}{R}  "
          f"{DIM}{'warn':<6}{R} {BYLW}{B}{result.n_warn:<4}{R}  "
          f"{DIM}{'fail':<6}{R} {BRED}{B}{result.n_fail:<4}{R}")
    sep()


def print_multi_summary(results: list):
    blank()
    header_bar("BATCH RESULTS SUMMARY")
    blank()

    w      = W() - 6
    dash_w = w + 2
    lw     = max(len(r.pkg_name) for r in results) + 2

    print(f" {DIM}┌{'─' * (w + 2)}┐{R}")
    for r in results:
        col = {PASS: BGRN, WARN: BYLW, FAIL: BRED}.get(r.verdict, DIM)
        verdict_str = f"{col}{B}{r.verdict:<4}{R}"
        counts = f"pass={r.n_pass} warn={r.n_warn} fail={r.n_fail}"
        name_s = f"{r.pkg_name:<{lw}}"
        line   = f"  {verdict_str}  {name_s}  {DIM}{counts}{R}"
        pad    = max(0, w - 4 - lw - 2 - len(counts))
        print(f" {DIM}│{R} {col}{B}{r.verdict:<4}{R} {name_s} {DIM}{counts}{R}{' ' * pad} {DIM}│{R}")
    print(f" {DIM}└{'─' * (w + 2)}┘{R}")
    blank()

    total   = len(results)
    n_pass  = sum(1 for r in results if r.verdict == PASS)
    n_warn  = sum(1 for r in results if r.verdict == WARN)
    n_fail  = sum(1 for r in results if r.verdict == FAIL)

    if n_fail:
        thick_rule(BRED)
        print(vcenter(f"{BRED}{B}FAIL  --  {n_fail}/{total} package(s) have errors{R}", W()))
        thick_rule(BRED)
    elif n_warn:
        thick_rule(BYLW)
        print(vcenter(f"{BYLW}{B}WARN  --  {n_warn}/{total} package(s) have warnings{R}", W()))
        thick_rule(BYLW)
    else:
        thick_rule(BGRN)
        print(vcenter(f"{BGRN}{B}ALL PASS  --  {total}/{total} packages clean{R}", W()))
        thick_rule(BGRN)
    blank()


def find_packages_dir() -> Path:
    candidates = [
        Path("packages"),
        Path(__file__).parent / "packages",
        Path(_PREFIX) / "lib/.tas/packages",
    ]
    for p in candidates:
        if p.is_dir():
            return p
    return None

def find_build_sh(pkg_name: str) -> Path:
    pkg_dir = find_packages_dir()
    if pkg_dir:
        p = pkg_dir / pkg_name / "build.sh"
        if p.exists():
            return p
    direct = Path(pkg_name) / "build.sh"
    if direct.exists():
        return direct
    return Path("packages") / pkg_name / "build.sh"

def list_all_packages() -> list:
    pkg_dir = find_packages_dir()
    if not pkg_dir:
        return []
    return sorted([
        d.name for d in pkg_dir.iterdir()
        if d.is_dir() and (d / "build.sh").exists()
    ])


def print_help():
    blank()
    header_bar("BUILD TESTER -- HELP")
    blank()
    rows = [
        ("<package>",          "Test a single package"),
        ("<package> --deep",   "Test + download & verify SHA256"),
        ("<package> --deps",   "Test + check deps via pkg info"),
        ("--all",              "Test all packages in packages/"),
        ("--all --brief",      "Test all, one line per package"),
        ("<package> --json",   "Output results as JSON"),
        ("--help",             "Show this help"),
    ]
    w  = W() - 6
    lw = max(len(r[0]) for r in rows) + 2
    print(f"  {DIM}┌{'─' * (w + 2)}┐{R}")
    for cmd, desc in rows:
        pad = max(0, w - 2 - lw - 2 - len(desc))
        print(f"  {DIM}│{R} {BCYN}{cmd:<{lw}}{R}  {desc}{' ' * pad} {DIM}│{R}")
    print(f"  {DIM}└{'─' * (w + 2)}┘{R}")
    blank()
    print(f"  {DIM}Examples:{R}")
    blank()
    code_line("python3 build-tester.py baxter")
    code_line("python3 build-tester.py baxter --deep")
    code_line("python3 build-tester.py --all --brief")
    code_line("python3 build-tester.py aura --json")
    blank()


def main():
    args = sys.argv[1:]

    mode_all   = "--all"   in args
    mode_deep  = "--deep"  in args
    mode_json  = "--json"  in args
    mode_brief = "--brief" in args
    mode_deps  = "--deps"  in args
    mode_help  = "--help"  in args or "-h" in args

    pkg_args = [a for a in args if not a.startswith("-")]

    if not mode_json:
        banner()

    if mode_help or (not pkg_args and not mode_all):
        print_help()
        sys.exit(0)

    if not mode_all:
        pkg_name = pkg_args[0]
        build_sh = find_build_sh(pkg_name)

        if not mode_json:
            subsection(f"Testing: {pkg_name}")
            blank()
            kv("build.sh", str(build_sh))
            kv("Mode", ("deep (download + SHA256)" if mode_deep else "standard"))
            blank()

        result = run_tests(pkg_name, build_sh, deep=mode_deep, check_deps=mode_deps)

        if mode_json:
            print(json.dumps(result.to_dict(), indent=2))
            sys.exit(0 if result.verdict == PASS else 1)

        print_result(result, verbose=not mode_brief)
        blank()

        if result.verdict == PASS:
            callout("PASS", f"Package '{pkg_name}' passed all checks.", "pass")
        elif result.verdict == WARN:
            callout("WARN", f"Package '{pkg_name}' has warnings. Review before submitting PR.", "note")
        else:
            callout("FAIL", f"Package '{pkg_name}' has errors that must be fixed.", "fail")
        blank()

        sys.exit(0 if result.verdict != FAIL else 1)

    pkgs = list_all_packages()
    if not pkgs:
        err("No packages found in packages/ directory.")
        info("Run from inside the termux-app-store repo directory.")
        blank()
        sys.exit(1)

    if not mode_json:
        log(f"Found {len(pkgs)} package(s)")
        blank()

    all_results = []
    for pkg_name in pkgs:
        build_sh = find_build_sh(pkg_name)
        result   = run_tests(pkg_name, build_sh, deep=False, check_deps=mode_deps)
        all_results.append(result)

        if mode_json:
            continue

        if mode_brief:
            col = {PASS: BGRN, WARN: BYLW, FAIL: BRED}.get(result.verdict, DIM)
            print(f"  {col}{B}{result.verdict:<4}{R}  {pkg_name:<28}  "
                  f"{DIM}pass={result.n_pass} warn={result.n_warn} fail={result.n_fail}{R}")
        else:
            print_result(result, verbose=True)
            sep()

    if mode_json:
        out = {
            "total":   len(all_results),
            "passed":  sum(1 for r in all_results if r.verdict == PASS),
            "warned":  sum(1 for r in all_results if r.verdict == WARN),
            "failed":  sum(1 for r in all_results if r.verdict == FAIL),
            "packages": [r.to_dict() for r in all_results],
        }
        print(json.dumps(out, indent=2))
    else:
        print_multi_summary(all_results)

    n_fail = sum(1 for r in all_results if r.verdict == FAIL)
    sys.exit(1 if n_fail else 0)


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
