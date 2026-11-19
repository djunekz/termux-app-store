#!/usr/bin/env python3
# Termux App Store -- Smart Doctor
# github.com/djunekz/termux-app-store

import ast
import hashlib
import importlib.machinery
import importlib.util
import json
import os
import platform
import re
import shlex
import shutil
import subprocess
import sys
import textwrap
import urllib.error
import urllib.request
from pathlib import Path

R = "\033[0m"
B = "\033[1m"
DIM = "\033[2m"
IT = "\033[3m"
BRED = "\033[91m"
BGRN = "\033[92m"
BYLW = "\033[93m"
BCYN = "\033[96m"
BWHT = "\033[97m"
BG_BBLK = "\033[100m"
BG_BBLU = "\033[104m"

_PFX = os.environ.get("PREFIX", "/data/data/com.termux/files/usr")
INSTALL_DIR = os.path.join(_PFX, "lib/.tas")
SENTINEL = os.path.join(INSTALL_DIR, ".installed")
BIN_TAS = os.path.join(_PFX, "bin/termux-app-store")
BIN_TASCTL = os.path.join(_PFX, "bin/tasctl")
SOURCES_DIR = os.path.join(_PFX, "etc/apt/sources.list.d")
SOURCES_FILE = os.path.join(SOURCES_DIR, "tas.list")
MAIN_SOURCES = os.path.join(_PFX, "etc/apt/sources.list")
APT_LISTS = os.path.join(_PFX, "var/lib/apt/lists")
REPO_URL = "https://djunekz.github.io/termux-app-store"
KEY_URL = REPO_URL + "/termux-app-store.gpg"
KEYRING_FILE = os.path.join(_PFX, "etc/apt/keyrings/termux-app-store.gpg")
REPO_ENTRY = f"deb [signed-by={KEYRING_FILE}] {REPO_URL} termux main"
PINNED_FINGERPRINTS = ("D39134A177717A5BEBEEAE7105D70CDBB6D80295",)
ARCH_OK = {"aarch64", "armv7l", "arm", "x86_64", "i686"}
MIN_PYTHON = (3, 9)
MIN_TEXTUAL = (8, 0, 0)
VERSION = "2.0.0"


def TW():
    return shutil.get_terminal_size((72, 24)).columns


def W():
    return min(TW(), 76)


def _strip(s):
    out, i = "", 0
    while i < len(s):
        if s[i] == "\033":
            while i < len(s) and s[i] != "m":
                i += 1
        else:
            out += s[i]
        i += 1
    return out


def vlen(s):
    return len(_strip(s))


def vcenter(t, w=None):
    w = w or W()
    return " " * max(0, (w - vlen(t)) // 2) + t


def blank():
    print()


def rule(c="─", col=DIM, w=None):
    print(f"{col}{c * (w or W())}{R}")


def thick_rule(col=BCYN, w=None):
    print(f"{col}{'━' * (w or W())}{R}")


def header_bar(title, w=None):
    w = w or W()
    pad = max(0, w - len(f"  {title}  "))
    print(f"{BCYN}{'▄' * w}{R}")
    print(f"{BG_BBLU}{BWHT}{B}  {title}  {R}{BG_BBLU}{' ' * pad}{R}")
    print(f"{BCYN}{'▀' * w}{R}")


def section(title):
    blank()
    print(f"  {BCYN}{B}>{R} {B}{BWHT}{title}{R}")
    print(f"  {DIM}{'─' * (W() - 2)}{R}")


def code(cmd, indent=4):
    print(f"{' ' * indent}{BYLW}${R} {BCYN}{cmd}{R}")


def callout(label, text, style="note"):
    S = {
        "note": (BYLW, "CATATAN"),
        "tip": (BGRN, "TIP"),
        "warning": (BRED, "WARNING"),
        "pass": (BGRN, "PASS"),
        "fail": (BRED, "FAIL"),
    }
    col, lbl0 = S.get(style, S["note"])
    lbl = label or lbl0
    w = W() - 4
    print(f"  {col}╭─[ {B}{lbl}{R}{col} ]{'─' * max(0, w - len(lbl) - 5)}╮{R}")
    for ln in textwrap.wrap(text, w - 4) or [""]:
        print(f"  {col}│{R}  {ln}{' ' * max(0, w - 4 - len(ln))}  {col}│{R}")
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
    for ln in _LOGO.splitlines():
        print(vcenter(f"{BCYN}{B}{ln}{R}", w))
    blank()
    print(vcenter(f"{BWHT}{B}Termux App Store{R}  {DIM}--  Smart Doctor{R}", w))
    print(vcenter(f"{DIM}Diagnoses & fixes environment, build.sh, and tool issues{R}", w))
    blank()
    thick_rule(BCYN, w)
    blank()


PASS, WARN, FAIL, INFO, SKIP = "PASS", "WARN", "FAIL", "INFO", "SKIP"


class Check:
    def __init__(self, name, status, detail="", fix_cmd=None, fix_hint=None, fix_fn=None, category=""):
        self.name = name
        self.status = status
        self.detail = detail
        self.fix_cmd = fix_cmd
        self.fix_hint = fix_hint
        self.fix_fn = fix_fn
        self.category = category

    def print_line(self):
        badge = {
            PASS: f"{BGRN}{B}  OK  {R}",
            WARN: f"{BYLW}{B}  !!  {R}",
            FAIL: f"{BRED}{B}  XX  {R}",
            INFO: f"{BCYN}{B}  --  {R}",
            SKIP: f"{DIM}  --  {R}",
        }.get(self.status, f"{DIM}  ??  {R}")
        nw = 32
        print(f"  {badge}  {B}{self.name:<{nw}}{R}  {DIM}{self.detail}{R}")
        if self.fix_hint and self.status in (FAIL, WARN):
            for ln in textwrap.wrap(self.fix_hint, W() - 14) or []:
                print(f"              {DIM}{IT}{ln}{R}")

    def to_dict(self):
        return {
            "name": self.name,
            "status": self.status,
            "detail": self.detail,
            "fix_cmd": self.fix_cmd,
            "fix_hint": self.fix_hint,
            "category": self.category,
        }


def _sh(cmd, timeout=6):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip(), r.returncode
    except Exception:
        return "", 1


def _which(p):
    return shutil.which(p) is not None


def chk_termux():
    inside = "com.termux" in _PFX or Path("/data/data/com.termux").exists()
    if inside:
        return Check("Termux environment", PASS, f"PREFIX={_PFX}", category="System")
    return Check(
        "Termux environment",
        WARN,
        f"non-Termux (PREFIX={_PFX})",
        fix_hint="Run inside Termux on Android for full functionality.",
        category="System",
    )


def chk_arch():
    arch = platform.machine()
    if arch in ARCH_OK:
        return Check("CPU architecture", PASS, arch, category="System")
    return Check(
        "CPU architecture", WARN, f"{arch} — untested (supported: {', '.join(sorted(ARCH_OK))})", category="System"
    )


def chk_storage():
    try:
        st = os.statvfs(_PFX)
        free = st.f_bavail * st.f_frsize // (1024 * 1024)
        tot = st.f_blocks * st.f_frsize // (1024 * 1024)
        det = f"{free} MB free / {tot} MB total"
        if free < 100:
            return Check("Storage space", WARN, det, fix_hint="Low storage — builds may fail.", category="System")
        return Check("Storage space", PASS, det, category="System")
    except Exception:
        return Check("Storage space", INFO, "could not check", category="System")


def chk_python():
    v = sys.version_info
    vs = f"{v.major}.{v.minor}.{v.micro}"
    if (v.major, v.minor) >= MIN_PYTHON:
        return Check("Python version", PASS, f"Python {vs}", category="Python")
    return Check(
        "Python version",
        FAIL,
        f"Python {vs} (need >= {MIN_PYTHON[0]}.{MIN_PYTHON[1]})",
        fix_cmd="pkg install python",
        fix_hint="pkg install python",
        category="Python",
    )


def chk_pip():
    for cmd in ["pip --version 2>/dev/null", "python3 -m pip --version 2>/dev/null"]:
        out, rc = _sh(cmd)
        if rc == 0 and out:
            ver = out.split()[1] if len(out.split()) > 1 else "?"
            return Check("pip", PASS, f"pip {ver}", category="Python")
    return Check(
        "pip",
        FAIL,
        "not found",
        fix_cmd="pkg install python",
        fix_hint="pkg install python  (pip is included)",
        category="Python",
    )


def chk_textual():
    try:
        import importlib.metadata

        ver_str = importlib.metadata.version("textual")
        parts = [int(x) for x in re.findall(r"\d+", ver_str)[:3]]
        while len(parts) < 3:
            parts.append(0)
        if tuple(parts) >= MIN_TEXTUAL:
            return Check("textual", PASS, f"textual {ver_str}", category="Python")
        return Check(
            "textual",
            WARN,
            f"textual {ver_str} (need >= {'.'.join(map(str, MIN_TEXTUAL))})",
            fix_cmd="pip install --upgrade textual --break-system-packages",
            fix_hint="pip install --upgrade textual --break-system-packages",
            category="Python",
        )
    except Exception:
        pass
    out, rc = _sh("python3 -c 'import textual; print(textual.__version__)' 2>/dev/null")
    if rc == 0 and out:
        return Check("textual", PASS, f"textual {out}", category="Python")
    return Check(
        "textual",
        FAIL,
        "not installed",
        fix_cmd="pip install textual --break-system-packages",
        fix_hint="pip install textual --break-system-packages",
        category="Python",
    )


def chk_python_importpath():
    out, rc = _sh(
        'python3 -c \'import sys; sp=[p for p in sys.path if "site-packages" in p];'
        ' print(sp[0] if sp else "")\' 2>/dev/null'
    )
    if rc != 0 or not out:
        return Check(
            "Python site-packages",
            WARN,
            "site-packages not in sys.path",
            fix_hint="pkg reinstall python",
            category="Python",
        )
    sp = Path(out)
    if not sp.exists():
        return Check(
            "Python site-packages",
            WARN,
            f"path does not exist: {out}",
            fix_hint="pkg reinstall python",
            category="Python",
        )
    return Check("Python site-packages", PASS, out, category="Python")


def chk_curl():
    if not _which("curl"):
        return Check(
            "curl", FAIL, "not found", fix_cmd="pkg install curl", fix_hint="pkg install curl", category="Tools"
        )
    out, _ = _sh("curl --version 2>/dev/null | head -1")
    return Check("curl", PASS, " ".join(out.split()[:2]) if out else "available", category="Tools")


def chk_git():
    if not _which("git"):
        return Check(
            "git",
            WARN,
            "not found (needed for contributing)",
            fix_cmd="pkg install git",
            fix_hint="pkg install git",
            category="Tools",
        )
    out, _ = _sh("git --version 2>/dev/null")
    return Check("git", PASS, out or "available", category="Tools")


def chk_dpkg():
    has_d = _which("dpkg")
    has_dd = _which("dpkg-deb")
    if has_d and has_dd:
        out, _ = _sh("dpkg --version 2>/dev/null | head -1")
        return Check("dpkg / dpkg-deb", PASS, out or "available", category="Tools")
    missing = [x for x, ok in [("dpkg", has_d), ("dpkg-deb", has_dd)] if not ok]
    return Check(
        "dpkg / dpkg-deb",
        WARN,
        f"missing: {', '.join(missing)} (needed for .deb builds)",
        fix_cmd="pkg install dpkg",
        fix_hint="pkg install dpkg",
        category="Tools",
    )


def chk_pkg():
    if _which("pkg"):
        return Check("pkg (Termux)", PASS, "available", category="Tools")
    return Check("pkg (Termux)", FAIL, "not found — must run inside Termux", category="Tools")


def chk_sha256sum():
    if _which("sha256sum"):
        return Check("sha256sum", PASS, "available", category="Tools")
    if _which("shasum"):
        return Check(
            "sha256sum",
            WARN,
            "not found but shasum available — build scripts may break",
            fix_hint="pkg install coreutils",
            category="Tools",
        )
    return Check(
        "sha256sum",
        WARN,
        "not found",
        fix_cmd="pkg install coreutils",
        fix_hint="pkg install coreutils",
        category="Tools",
    )


def chk_tas_binary():
    p = Path(BIN_TAS)
    if not p.exists():
        return Check(
            "termux-app-store binary",
            FAIL,
            "not installed",
            fix_cmd="pip install termux-app-store --break-system-packages",
            fix_hint="pip install termux-app-store  OR  bash install.sh",
            category="TAS",
        )
    if not (p.stat().st_mode & 0o111):
        return Check(
            "termux-app-store binary",
            WARN,
            f"{p} is not executable",
            fix_cmd=f"chmod +x {shlex.quote(str(BIN_TAS))}",
            fix_hint=f"chmod +x {BIN_TAS}",
            category="TAS",
        )
    return Check("termux-app-store binary", PASS, str(p), category="TAS")


def chk_tas_wrapper():
    p = Path(BIN_TAS)
    if not p.exists():
        return Check("TAS wrapper integrity", SKIP, "binary not present", category="TAS")
    try:
        content = p.read_text(errors="replace")
    except Exception as e:
        return Check("TAS wrapper integrity", WARN, f"cannot read: {e}", category="TAS")

    issues = []
    if "TERMUX_APP_STORE_HOME" not in content:
        issues.append("TERMUX_APP_STORE_HOME missing")

    m = re.search(r'TERMUX_APP_STORE_HOME="?([^"\n]+)"?', content)
    if m:
        home = Path(m.group(1).strip())
        if not home.exists():
            issues.append(f"TERMUX_APP_STORE_HOME={home} does not exist")
        elif not (home / "termux_app_store" / "main.py").exists():
            issues.append(f"main.py not found in {home}")

    if issues:
        return Check(
            "TAS wrapper integrity",
            WARN,
            "; ".join(issues),
            fix_cmd="bash install.sh 2>/dev/null || true",
            fix_hint="bash install.sh  to regenerate wrapper",
            category="TAS",
        )
    return Check("TAS wrapper integrity", PASS, "TERMUX_APP_STORE_HOME set and valid", category="TAS")


def chk_tas_version():
    s = Path(SENTINEL)
    if s.exists():
        try:
            for ln in s.read_text().splitlines():
                if ln.startswith("version="):
                    return Check("TAS version", PASS, f"v{ln.split('=', 1)[1]}", category="TAS")
        except Exception:
            pass
    try:
        import importlib.metadata

        ver = importlib.metadata.version("termux-app-store")
        return Check("TAS version", PASS, f"v{ver}", category="TAS")
    except Exception:
        pass
    out, rc = _sh(
        f"{shlex.quote(str(BIN_TAS))} --version 2>/dev/null || {shlex.quote(str(BIN_TAS))} version 2>/dev/null"
    )
    if rc == 0 and out:
        return Check("TAS version", PASS, out.strip(), category="TAS")
    return Check("TAS version", INFO, "could not determine", category="TAS")


def chk_tas_can_run():
    install_dir = Path(INSTALL_DIR)
    main_py = install_dir / "termux_app_store" / "main.py"

    if not main_py.exists():
        out, rc = _sh("python3 -c 'import termux_app_store; print(\"ok\")' 2>/dev/null")
        if rc == 0 and "ok" in out:
            return Check("TAS importable", PASS, "pip-installed OK", category="TAS")
        return Check(
            "TAS importable",
            FAIL,
            "termux_app_store module not found",
            fix_cmd="pip install termux-app-store --break-system-packages",
            fix_hint="pip install termux-app-store --break-system-packages",
            category="TAS",
        )

    out, rc = _sh(
        f'python3 -c \'import sys; sys.path.insert(0,"{install_dir}"); '
        f'from termux_app_store import termux_app_store; print("ok")\' 2>/dev/null'
    )
    if rc == 0 and "ok" in out:
        return Check("TAS importable", PASS, "source module OK", category="TAS")

    out2, _ = _sh(
        f'python3 -c \'import sys; sys.path.insert(0,"{install_dir}"); '
        f"from termux_app_store import termux_app_store' 2>&1"
    )
    detail = (out2.strip().split("\n")[-1])[:60] if out2 else "import failed"
    fix = None
    if "textual" in out2.lower():
        fix = "pip install textual --break-system-packages"
    elif "No module named" in out2:
        fix = "pip install termux-app-store --break-system-packages"

    return Check(
        "TAS importable",
        FAIL,
        detail,
        fix_cmd=fix,
        fix_hint=fix or "Check Python path and re-run install.sh",
        category="TAS",
    )


def chk_tasctl():
    for candidate in [BIN_TASCTL, str(Path(INSTALL_DIR) / "tasctl"), "./tasctl"]:
        if Path(candidate).exists():
            return Check("tasctl", PASS, str(Path(candidate).resolve()), category="TAS")
    out, rc = _sh("which tasctl 2>/dev/null")
    if rc == 0 and out:
        return Check("tasctl", PASS, out, category="TAS")
    return Check(
        "tasctl",
        WARN,
        "not found",
        fix_cmd="bash install.sh 2>/dev/null || true",
        fix_hint="bash install.sh  (from inside the repo directory)",
        category="TAS",
    )


def _pinned():
    override = os.environ.get("TAS_KEY_FPR", "").replace(" ", "").upper()
    return (override,) if override else PINNED_FINGERPRINTS


def _verify_key_data(data):
    if len(data) > 65536:
        raise ValueError("key file is too large")
    if data.startswith(b"-----BEGIN"):
        raise ValueError("key is ASCII-armored, a binary key is required")
    packets, pos, n = [], 0, len(data)
    try:
        while pos < n:
            hdr = data[pos]
            pos += 1
            if not hdr & 0x80:
                raise ValueError("not an OpenPGP packet stream")
            if hdr & 0x40:
                tag = hdr & 0x3F
                first = data[pos]
                if first < 192:
                    length, pos = first, pos + 1
                elif first < 224:
                    length, pos = ((first - 192) << 8) + data[pos + 1] + 192, pos + 2
                elif first == 255:
                    length, pos = int.from_bytes(data[pos + 1 : pos + 5], "big"), pos + 5
                else:
                    raise ValueError("unsupported packet length encoding")
            else:
                tag = (hdr >> 2) & 0x0F
                kind = hdr & 0x03
                if kind == 3:
                    raise ValueError("unsupported packet length encoding")
                size = (1, 2, 4)[kind]
                length = int.from_bytes(data[pos : pos + size], "big")
                pos += size
            if pos + length > n:
                raise ValueError("truncated key file")
            packets.append((tag, data[pos : pos + length]))
            pos += length
    except IndexError:
        raise ValueError("truncated key file")
    if not packets or packets[0][0] != 6:
        raise ValueError("file does not start with a public key")
    primary, primaries = None, 0
    for tag, body in packets:
        if tag not in (2, 6, 13, 14, 17):
            raise ValueError(f"unexpected OpenPGP packet type {tag}")
        if tag == 6:
            if not body or body[0] != 4 or len(body) > 0xFFFF:
                raise ValueError("only version 4 public keys are supported")
            primaries += 1
            primary = hashlib.sha1(b"\x99" + len(body).to_bytes(2, "big") + body).hexdigest().upper()
        elif tag == 14 and (not body or body[0] != 4):
            raise ValueError("only version 4 public keys are supported")
    if primaries != 1:
        raise ValueError("file must contain exactly one primary key")
    if primary not in _pinned():
        raise ValueError(f"key fingerprint {primary} does not match the pinned fingerprint")
    return primary


def _fix_repo_file():
    try:
        req = urllib.request.Request(KEY_URL, headers={"User-Agent": f"tas-doctor/{VERSION}"})
        with urllib.request.urlopen(req, timeout=20) as r:
            data = r.read(65537)
        primary = _verify_key_data(data)
    except Exception as e:
        print(f"  {BRED}XX{R}  Signing key rejected: {e}")
        return False
    Path(KEYRING_FILE).parent.mkdir(parents=True, exist_ok=True)
    tmp = Path(KEYRING_FILE + ".tmp")
    tmp.write_bytes(data)
    tmp.chmod(0o600)
    os.replace(tmp, KEYRING_FILE)
    print(f"  {BGRN}OK{R}  Key {primary} installed")

    Path(SOURCES_DIR).mkdir(parents=True, exist_ok=True)
    Path(SOURCES_FILE).write_text(REPO_ENTRY + "\n")
    print(f"  {BGRN}OK{R}  Written: {SOURCES_FILE}")
    return True


def chk_repo_file():
    p = Path(SOURCES_FILE)
    if p.exists():
        try:
            txt = p.read_text()
        except Exception as e:
            return Check("apt repo (tas.list)", WARN, f"read error: {e}", category="Repo")
        if REPO_URL in txt:
            active = [ln for ln in txt.splitlines() if ln.strip() and not ln.strip().startswith("#")]
            if any("trusted=yes" in ln for ln in active):
                return Check(
                    "apt repo (tas.list)",
                    WARN,
                    "insecure [trusted=yes] entry (no signature check)",
                    fix_fn=_fix_repo_file,
                    fix_hint="python3 install-repo.py  to migrate to signed-by",
                    category="Repo",
                )
            if not Path(KEYRING_FILE).exists():
                return Check(
                    "apt repo (tas.list)",
                    WARN,
                    f"signing key missing: {KEYRING_FILE}",
                    fix_fn=_fix_repo_file,
                    fix_hint="python3 install-repo.py",
                    category="Repo",
                )
            try:
                _verify_key_data(Path(KEYRING_FILE).read_bytes())
            except Exception as e:
                return Check(
                    "apt repo (tas.list)",
                    WARN,
                    f"keyring does not match pinned key: {e}",
                    fix_fn=_fix_repo_file,
                    fix_hint="python3 install-repo.py",
                    category="Repo",
                )
            if len(active) > 1:
                return Check(
                    "apt repo (tas.list)",
                    WARN,
                    f"{len(active)} entries (duplicate risk)",
                    fix_fn=_fix_repo_file,
                    fix_hint="python3 install-repo.py  to clean up",
                    category="Repo",
                )
            return Check("apt repo (tas.list)", PASS, str(p), category="Repo")
        return Check(
            "apt repo (tas.list)",
            WARN,
            f"{p} exists but TAS URL not found",
            fix_fn=_fix_repo_file,
            fix_hint="python3 install-repo.py",
            category="Repo",
        )
    if Path(MAIN_SOURCES).exists():
        try:
            if REPO_URL in Path(MAIN_SOURCES).read_text():
                return Check(
                    "apt repo (tas.list)",
                    WARN,
                    "URL found in main sources.list (wrong location)",
                    fix_fn=_fix_repo_file,
                    fix_hint="python3 install-repo.py",
                    category="Repo",
                )
        except Exception:
            pass
    return Check(
        "apt repo (tas.list)",
        FAIL,
        "not configured",
        fix_fn=_fix_repo_file,
        fix_hint="python3 install-repo.py",
        category="Repo",
    )


def chk_apt_lists():
    if not Path(SOURCES_FILE).exists():
        return Check("apt lists (freshness)", SKIP, "repo not configured yet", category="Repo")
    lists_dir = Path(APT_LISTS)
    if not lists_dir.exists():
        return Check(
            "apt lists (freshness)",
            WARN,
            "apt lists directory missing",
            fix_cmd="pkg update",
            fix_hint="pkg update",
            category="Repo",
        )
    tas_lists = list(lists_dir.glob("*djunekz*")) + list(lists_dir.glob("*termux-app-store*"))
    if not tas_lists:
        return Check(
            "apt lists (freshness)",
            WARN,
            "apt lists not updated since repo install",
            fix_cmd="pkg update",
            fix_hint="pkg update  (fetch package list from TAS repo)",
            category="Repo",
        )
    try:
        import time

        mtime = max(f.stat().st_mtime for f in tas_lists)
        age_days = (time.time() - mtime) / 86400
        if age_days > 7:
            return Check(
                "apt lists (freshness)",
                WARN,
                f"lists are {age_days:.0f} days old (> 7)",
                fix_cmd="pkg update",
                fix_hint="pkg update  (refresh TAS package list)",
                category="Repo",
            )
        return Check("apt lists (freshness)", PASS, f"up to date ({age_days:.0f} days old)", category="Repo")
    except Exception:
        return Check("apt lists (freshness)", PASS, "lists exist", category="Repo")


def _find_root():
    for p in [Path("."), Path(__file__).parent.parent, Path(INSTALL_DIR)]:
        if (p / "packages").is_dir() and (p / "build-package.sh").exists():
            return p
    return None


def chk_packages_dir():
    root = _find_root()
    for base in ([root / "packages"] if root else []) + [Path("packages"), Path(INSTALL_DIR) / "packages"]:
        if base and base.is_dir():
            count = sum(1 for x in base.iterdir() if x.is_dir() and (x / "build.sh").exists())
            return Check("packages/ directory", PASS, f"{base}  ({count} packages)", category="Project")
    return Check(
        "packages/ directory",
        WARN,
        "not found — run from inside the repo",
        fix_hint="cd ~/termux-app-store  then re-run doctor",
        category="Project",
    )


def chk_build_package_sh():
    root = _find_root()
    candidates = ([root / "build-package.sh"] if root else []) + [
        Path("build-package.sh"),
        Path(INSTALL_DIR) / "build-package.sh",
    ]
    for p in candidates:
        if p and p.exists():
            if p.stat().st_mode & 0o111:
                return Check("build-package.sh", PASS, str(p), category="Project")
            return Check(
                "build-package.sh",
                WARN,
                f"{p} not executable",
                fix_cmd=f"chmod +x {shlex.quote(str(p))}",
                fix_hint=f"chmod +x {p}",
                category="Project",
            )
    return Check(
        "build-package.sh",
        WARN,
        "not found — run from inside the repo",
        fix_hint="cd ~/termux-app-store",
        category="Project",
    )


def chk_termux_build():
    root = _find_root()
    candidates = ([root / "termux-build"] if root else []) + [Path("termux-build"), Path(INSTALL_DIR) / "termux-build"]
    for p in candidates:
        if p and p.exists():
            return Check("termux-build tool", PASS, str(p), category="Project")
    return Check(
        "termux-build tool",
        WARN,
        "not found — run from inside the repo",
        fix_hint="cd ~/termux-app-store",
        category="Project",
    )


def chk_build_sh_scan():
    root = _find_root()
    pkgs_dir = None
    for base in ([root / "packages"] if root else []) + [Path("packages"), Path(INSTALL_DIR) / "packages"]:
        if base and base.is_dir():
            pkgs_dir = base
            break
    if not pkgs_dir:
        return Check("build.sh scan", SKIP, "packages/ not found", category="Project")

    broken, total = [], 0
    for pkg_dir in sorted(pkgs_dir.iterdir()):
        if not pkg_dir.is_dir():
            continue
        bsh = pkg_dir / "build.sh"
        total += 1
        if not bsh.exists():
            broken.append(f"{pkg_dir.name}:missing")
            continue
        if not bsh.read_text(errors="replace").strip():
            broken.append(f"{pkg_dir.name}:empty")
            continue
        _, rc = _sh(f"bash -n {shlex.quote(str(bsh))} 2>/dev/null")
        if rc != 0:
            broken.append(f"{pkg_dir.name}:syntax")

    if broken:
        return Check(
            "build.sh scan",
            WARN,
            f"{len(broken)}/{total} broken: " + ", ".join(broken[:4]) + ("..." if len(broken) > 4 else ""),
            fix_hint="python3 build-tester.py --all  for full details",
            category="Project",
        )
    return Check("build.sh scan", PASS, f"all {total} packages OK", category="Project")


def chk_last_build():
    root = _find_root()
    if not root:
        return Check("recent build status", SKIP, "project root not found", category="Build")
    build_dir = root / "build"
    if not build_dir.exists():
        return Check("recent build status", INFO, "no builds yet", category="Build")

    incomplete = []
    output_dir = root / "output"
    for pkg_dir in build_dir.iterdir():
        if not pkg_dir.is_dir():
            continue
        debs = list(output_dir.glob(f"{pkg_dir.name}_*.deb")) if output_dir.exists() else []
        if not debs:
            incomplete.append(pkg_dir.name)

    if incomplete:

        def _clean():
            for pkg in incomplete:
                d = root / "build" / pkg
                if d.exists():
                    shutil.rmtree(d)
                    print(f"  {BGRN}OK{R}  Removed {d}")
            return True

        return Check(
            "recent build status",
            WARN,
            f"incomplete build dirs: {', '.join(incomplete[:3])}",
            fix_fn=_clean,
            fix_hint=f"rm -rf {root}/build/  to clean up",
            category="Build",
        )
    return Check("recent build status", PASS, "no incomplete builds", category="Build")


def chk_output_dir():
    root = _find_root()
    if not root:
        return Check("output/ (.deb files)", SKIP, "project root not found", category="Build")
    output = root / "output"
    if not output.exists():
        return Check("output/ (.deb files)", INFO, "no builds yet", category="Build")
    debs = list(output.glob("*.deb"))
    if not debs:
        return Check("output/ (.deb files)", INFO, "no .deb files", category="Build")
    corrupt = [d for d in debs if d.stat().st_size == 0]
    if corrupt:
        names = ", ".join(d.name for d in corrupt[:3])
        return Check(
            "output/ (.deb files)",
            WARN,
            f"corrupt (0-byte): {names}",
            fix_cmd=f"rm -f {shlex.quote(str(output))}/*.deb",
            fix_hint=f"rm {output}/*.deb  then rebuild",
            category="Build",
        )
    return Check("output/ (.deb files)", PASS, f"{len(debs)} .deb file(s)", category="Build")


def chk_installed_tas_pkgs():
    if not _which("dpkg"):
        return Check("TAS packages (installed)", SKIP, "dpkg not available", category="Build")
    out, rc = _sh("dpkg --get-selections 2>/dev/null | grep -i 'install$'")
    if rc != 0:
        return Check("TAS packages (installed)", INFO, "could not query dpkg", category="Build")
    root = _find_root()
    known = set()
    if root and (root / "packages").is_dir():
        known = {d.name for d in (root / "packages").iterdir() if d.is_dir() and (d / "build.sh").exists()}
    installed = [ln.split()[0] for ln in out.splitlines() if ln.split() and ln.split()[0] in known]
    if installed:
        return Check(
            "TAS packages (installed)", PASS, f"{len(installed)}: {', '.join(installed[:5])}", category="Build"
        )
    return Check("TAS packages (installed)", INFO, "none installed yet", category="Build")


def chk_network():
    try:
        req = urllib.request.Request(REPO_URL, headers={"User-Agent": f"tas-doctor/{VERSION}"}, method="HEAD")
        with urllib.request.urlopen(req, timeout=7) as r:
            code = r.getcode()
        if code == 200:
            return Check("Repo reachable", PASS, REPO_URL, category="Network")
        return Check("Repo reachable", WARN, f"HTTP {code}", category="Network")
    except urllib.error.URLError as e:
        return Check(
            "Repo reachable", WARN, f"unreachable: {e.reason}", fix_hint="Check internet connection", category="Network"
        )
    except Exception as e:
        return Check("Repo reachable", WARN, str(e)[:50], category="Network")


def chk_github():
    try:
        req = urllib.request.Request(
            "https://api.github.com/repos/djunekz/termux-app-store",
            headers={"User-Agent": f"tas-doctor/{VERSION}", "Accept": "application/vnd.github+json"},
        )
        with urllib.request.urlopen(req, timeout=7) as r:
            data = json.loads(r.read().decode())
        stars = data.get("stargazers_count", "?")
        return Check("GitHub API", PASS, f"reachable (stars: {stars})", category="Network")
    except Exception as e:
        return Check("GitHub API", WARN, str(e)[:50], fix_hint="Check internet connection", category="Network")


REQUIRED_FIELDS = [
    "TERMUX_PKG_HOMEPAGE",
    "TERMUX_PKG_DESCRIPTION",
    "TERMUX_PKG_LICENSE",
    "TERMUX_PKG_MAINTAINER",
    "TERMUX_PKG_VERSION",
    "TERMUX_PKG_SRCURL",
    "TERMUX_PKG_SHA256",
]


def _parse_build_sh(path: Path) -> dict:
    vals = {}
    for raw in path.read_text(errors="replace").splitlines():
        ln = raw.strip()
        if not ln or ln.startswith("#"):
            continue
        m = re.match(r"^(TERMUX_PKG_\w+)=(.*)$", ln)
        if not m:
            continue
        k, v = m.group(1), m.group(2).strip()
        if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
            v = v[1:-1]
        vals[k] = v
    ver = vals.get("TERMUX_PKG_VERSION", "")
    if ver:
        for k in vals:
            vals[k] = vals[k].replace("${TERMUX_PKG_VERSION}", ver)
    return vals


def _find_build_sh(pkg_name: str):
    root = _find_root()
    for base in ([root / "packages"] if root else []) + [Path("packages"), Path(INSTALL_DIR) / "packages"]:
        if base and (base / pkg_name / "build.sh").exists():
            return base / pkg_name / "build.sh"
    return None


def diagnose_build_sh(pkg_name: str) -> list:
    results = []

    build_sh = _find_build_sh(pkg_name)
    if not build_sh:
        results.append(
            Check(
                "packages/" + pkg_name + "/build.sh",
                FAIL,
                "file not found",
                fix_hint=f"python3 pkg-scaffold.py {pkg_name}  to create it",
                category="build.sh",
            )
        )
        return results
    results.append(Check("build.sh found", PASS, str(build_sh), category="build.sh"))

    content = build_sh.read_text(errors="replace")
    if not content.strip():
        results.append(
            Check(
                "build.sh not empty",
                FAIL,
                "file is empty",
                fix_hint=f"python3 pkg-scaffold.py {pkg_name}",
                category="build.sh",
            )
        )
        return results
    lines = content.splitlines()
    results.append(Check("build.sh not empty", PASS, f"{len(lines)} lines", category="build.sh"))

    out, rc = _sh(f"bash -n {shlex.quote(str(build_sh))} 2>&1")
    if rc != 0:
        m = re.search(r"line (\d+)", out)
        lineno = f" (line {m.group(1)})" if m else ""
        snippet = (out.strip().split("\n")[-1])[:55] if out else "syntax error"
        results.append(
            Check(
                "bash syntax",
                FAIL,
                f"error{lineno}: {snippet}",
                fix_hint=f"nano {build_sh}  — look for unmatched quotes/braces/EOF",
                category="build.sh",
            )
        )
        return results
    results.append(Check("bash syntax", PASS, "OK", category="build.sh"))

    try:
        vals = _parse_build_sh(build_sh)
    except Exception as e:
        results.append(Check("build.sh parse", FAIL, str(e), category="build.sh"))
        return results

    for field in REQUIRED_FIELDS:
        val = vals.get(field, "")
        if not val:
            hint = f"Add  {field}=...  to build.sh"
            if field == "TERMUX_PKG_SHA256":
                hint = "python3 build-tester.py " + pkg_name + " --deep  to compute SHA256 automatically"
            elif field == "TERMUX_PKG_SRCURL":
                hint = "URL to .tar.gz or .zip of the upstream source"
            results.append(Check(field, FAIL, "missing or empty", fix_hint=hint, category="build.sh"))
        else:
            results.append(Check(field, PASS, val[:52], category="build.sh"))

    ver = vals.get("TERMUX_PKG_VERSION", "")
    if ver and not re.match(r"^\d", ver):
        results.append(
            Check(
                "VERSION format",
                FAIL,
                f"'{ver}' does not start with digit",
                fix_hint=f"Change to: TERMUX_PKG_VERSION={ver.lstrip('v')}",
                category="build.sh",
            )
        )
    elif ver:
        results.append(Check("VERSION format", PASS, ver, category="build.sh"))

    sha = vals.get("TERMUX_PKG_SHA256", "")
    if sha and sha.upper() != "SKIP" and not re.match(r"^[0-9a-fA-F]{64}$", sha):
        results.append(
            Check(
                "SHA256 format",
                FAIL,
                f"invalid ({len(sha)} chars, need 64 hex)",
                fix_hint=("python3 build-tester.py " + pkg_name + " --deep  to compute the correct hash"),
                category="build.sh",
            )
        )
    elif sha and sha.upper() == "SKIP":
        results.append(
            Check(
                "SHA256 format",
                WARN,
                "SHA256=SKIP — verification disabled",
                fix_hint=("python3 build-tester.py " + pkg_name + " --deep  to generate real hash"),
                category="build.sh",
            )
        )

    forbidden = [
        (r"\bsudo\b", "sudo not allowed in Termux"),
        (r"\bapt-get\b", "use pkg instead of apt-get"),
        (r"\bapt install\b", "use pkg install instead of apt install"),
        (r"TERMUX_PKG_VERSION=v\d", "VERSION starts with 'v' (remove the v)"),
        (r"\bchown\b", "chown not available in Termux userspace"),
        (r"rm -rf /[^/\n]", "dangerous rm -rf detected"),
    ]
    in_heredoc, end_token = False, ""
    for i, ln in enumerate(lines, 1):
        stripped = ln.strip()
        if not in_heredoc:
            m = re.search(r"<<\s*['\"]?(\w+)['\"]?", ln)
            if m:
                in_heredoc = True
                end_token = m.group(1)
                continue
        else:
            if stripped == end_token:
                in_heredoc, end_token = False, ""
            continue
        if stripped.startswith("#"):
            continue
        for pattern, msg in forbidden:
            if re.search(pattern, ln):
                results.append(
                    Check(
                        f"Lint: {msg[:32]}",
                        FAIL,
                        f"line {i}: {ln.strip()[:42]}",
                        fix_hint=f"Edit line {i} of {build_sh.name}",
                        category="build.sh",
                    )
                )
                break

    hc_re = re.compile(r"/data/data/com\.termux/files/usr(?!/bin/env)")
    in_heredoc, end_token = False, ""
    for i, ln in enumerate(lines, 1):
        stripped = ln.strip()
        if not in_heredoc:
            m = re.search(r"<<\s*['\"]?(\w+)['\"]?", ln)
            if m:
                in_heredoc = True
                end_token = m.group(1)
                continue
        else:
            if stripped == end_token:
                in_heredoc, end_token = False, ""
            continue
        if stripped.startswith("#"):
            continue
        if hc_re.search(ln):
            results.append(
                Check(
                    "Lint: hardcoded prefix",
                    WARN,
                    f"line {i}: use $TERMUX_PREFIX instead",
                    fix_hint=f"Replace hardcoded path with $TERMUX_PREFIX (line {i})",
                    category="build.sh",
                )
            )
            break

    has_fn = "termux_step_make_install()" in content
    deps = vals.get("TERMUX_PKG_DEPENDS", "").lower()
    scripted = any(k in deps for k in ["python", "nodejs", "ruby", "perl", "php", "lua"])
    if not has_fn and scripted:
        results.append(
            Check(
                "termux_step_make_install()",
                WARN,
                "missing — needed for script-based packages",
                fix_hint="Add termux_step_make_install() { ... } to build.sh",
                category="build.sh",
            )
        )
    elif has_fn:
        results.append(Check("termux_step_make_install()", PASS, "found", category="build.sh"))
    else:
        results.append(
            Check("termux_step_make_install()", INFO, "not present (using default build flow)", category="build.sh")
        )

    if has_fn and "TERMUX_PKG_BUILD_IN_SRC" not in content:
        results.append(
            Check(
                "TERMUX_PKG_BUILD_IN_SRC",
                WARN,
                "not set — needed for most script packages",
                fix_hint="Add: TERMUX_PKG_BUILD_IN_SRC=true",
                category="build.sh",
            )
        )
    elif "TERMUX_PKG_BUILD_IN_SRC=true" in content:
        results.append(Check("TERMUX_PKG_BUILD_IN_SRC", PASS, "true", category="build.sh"))

    if _which("pkg"):
        dep_str = vals.get("TERMUX_PKG_DEPENDS", "")
        if dep_str:
            for dep in [d.strip().split()[0] for d in dep_str.split(",") if d.strip()]:
                out, rc = _sh(f"pkg info {shlex.quote(dep)} 2>/dev/null | head -1")
                if rc == 0 and out:
                    results.append(Check(f"dep: {dep}", PASS, out[:40], category="build.sh"))
                else:
                    results.append(
                        Check(
                            f"dep: {dep}",
                            WARN,
                            "not found via pkg",
                            fix_hint=f"Verify: pkg info {dep}",
                            category="build.sh",
                        )
                    )

    src = vals.get("TERMUX_PKG_SRCURL", "")
    if src and src.startswith("http") and "${" not in src:
        try:
            req = urllib.request.Request(src, headers={"User-Agent": "tas-doctor/2.0"}, method="HEAD")
            with urllib.request.urlopen(req, timeout=8) as r:
                code = r.getcode()
            if code == 200:
                size = r.headers.get("Content-Length", "?")
                sz = f"{int(size) // 1024} KB" if str(size).isdigit() else "?"
                results.append(Check("SRCURL reachable", PASS, f"HTTP 200 ({sz})", category="build.sh"))
            else:
                results.append(Check("SRCURL reachable", WARN, f"HTTP {code}", category="build.sh"))
        except urllib.error.HTTPError as e:
            lvl = WARN if e.code in (403, 405) else FAIL
            results.append(Check("SRCURL reachable", lvl, f"HTTP {e.code} (may still be valid)", category="build.sh"))
        except Exception as e:
            results.append(Check("SRCURL reachable", WARN, str(e)[:50], category="build.sh"))

    return results


def run_fix(check: Check, mode_fix: bool):
    if not mode_fix or check.status not in (FAIL, WARN):
        return False
    if not (check.fix_cmd or check.fix_fn or check.fix_hint):
        return False

    blank()
    print(f"  {BCYN}{B}FIX{R}  {B}{check.name}{R}")
    rule("─", DIM)

    if check.fix_fn:
        try:
            ok = check.fix_fn()
            print(f"  {BGRN if ok else BYLW}{B}{'OK  Fix applied' if ok else '!!  Fix ran — review result'}{R}")
        except Exception as e:
            print(f"  {BRED}{B}XX{R}  Fix function failed: {e}")
            return False
        return bool(ok)

    if check.fix_cmd:
        print(f"  {DIM}Running:{R}  {BCYN}{check.fix_cmd}{R}")
        blank()
        rc = subprocess.run(check.fix_cmd, shell=True).returncode

        blank()
        rule("─", DIM)
        if rc == 0:
            print(f"  {BGRN}{B}OK{R}  Fix applied")
            return True
        else:
            print(f"  {BRED}{B}XX{R}  Fix failed (exit {rc})")
            if check.fix_hint:
                print(f"  {DIM}Try manually:{R}  {BCYN}{check.fix_hint}{R}")
        return False

    print(f"  {BYLW}{B}!!{R}  No automatic fix — manual steps:")
    blank()
    for ln in textwrap.wrap(check.fix_hint, W() - 8):
        code(ln)
    rule("─", DIM)
    return False


PIP_ALIASES = {
    "yaml": "pyyaml",
    "bs4": "beautifulsoup4",
    "cv2": "opencv-python",
    "PIL": "pillow",
    "sklearn": "scikit-learn",
    "dateutil": "python-dateutil",
    "dotenv": "python-dotenv",
    "OpenSSL": "pyopenssl",
    "Crypto": "pycryptodome",
    "serial": "pyserial",
    "git": "gitpython",
    "jwt": "pyjwt",
    "socks": "pysocks",
    "attr": "attrs",
    "magic": "python-magic",
    "websocket": "websocket-client",
    "docx": "python-docx",
    "zmq": "pyzmq",
    "telegram": "python-telegram-bot",
    "slugify": "python-slugify",
    "discord": "discord.py",
}
TERMUX_PY_PKGS = {
    "numpy": "python-numpy",
    "scipy": "python-scipy",
    "pandas": "python-pandas",
    "cryptography": "python-cryptography",
    "lxml": "python-lxml",
    "PIL": "python-pillow",
}
_NAME_OK = re.compile(r"^[A-Za-z0-9_.+-]+$")
_PY_RE = r"(?:\S*/)?python[\d.]*"


def _stdlib_names():
    names = getattr(sys, "stdlib_module_names", None)
    return set(names) if names else set(sys.builtin_module_names)


def _import_guarded(node):
    for h in node.handlers:
        if h.type is None:
            return True
        elts = h.type.elts if isinstance(h.type, ast.Tuple) else [h.type]
        names = [getattr(e, "id", getattr(e, "attr", "")) for e in elts]
        if any(n in ("ImportError", "ModuleNotFoundError", "Exception", "BaseException") for n in names):
            return True
    return False


def required_imports(path):
    try:
        tree = ast.parse(Path(path).read_text(encoding="utf-8", errors="replace"))
    except (SyntaxError, ValueError, OSError):
        return []
    found = []

    def visit(body):
        for n in body:
            if isinstance(n, ast.Import):
                for a in n.names:
                    found.append((0, a.name, True))
            elif isinstance(n, ast.ImportFrom):
                mod = n.module or ""
                if n.level == 0 and mod:
                    found.append((0, mod, True))
                elif n.level == 0:
                    continue
                else:
                    found.append((n.level, mod, False))
                for a in n.names:
                    found.append((n.level, f"{mod}.{a.name}" if mod else a.name, False))
            elif isinstance(n, ast.If):
                test = ast.dump(n.test)
                if not any(k in test for k in ("version_info", "platform", "TYPE_CHECKING", "os")):
                    visit(n.body)
                    visit(n.orelse)
            elif isinstance(n, (ast.With, ast.For, ast.While)):
                visit(n.body)
            elif isinstance(n, ast.Try):
                if not _import_guarded(n):
                    visit(n.body)
                visit(n.orelse)
                visit(n.finalbody)

    visit(tree.body)
    return found


def _find_spec(name, extra):
    try:
        spec = importlib.util.find_spec(name)
        if spec is not None:
            return spec
    except (ImportError, ValueError, AttributeError):
        pass
    try:
        return importlib.machinery.PathFinder.find_spec(name, list(extra) + sys.path)
    except (ImportError, ValueError):
        return None


def _resolve_local(dotted, roots):
    parts = [p for p in dotted.split(".") if p]
    if not parts:
        return None
    for r in roots:
        p = Path(r).joinpath(*parts)
        if p.with_suffix(".py").is_file():
            return p.with_suffix(".py")
        if (p / "__init__.py").is_file():
            return p / "__init__.py"
    return None


def parse_launcher(path):
    info = {"kind": None, "script": None, "module": None, "pythonpath": [], "node_target": None}
    try:
        raw = Path(path).read_bytes()[:65536]
    except OSError:
        return info
    if b"\0" in raw:
        return info
    text = raw.decode("utf-8", "replace")
    for var in ("${PREFIX}", "$PREFIX", "${TERMUX_PREFIX}", "$TERMUX_PREFIX"):
        text = text.replace(var, _PFX)
    first = text.splitlines()[0] if text else ""

    m = re.search(rf"exec\s+{_PY_RE}\s+-m\s+([\w.]+)", text)
    if m:
        info.update(kind="python", module=m.group(1))
    else:
        m = re.search(rf"exec\s+{_PY_RE}\s+(?:-\S+\s+)*[\"']?(/[^\"'\s]+\.py)", text)
        if m:
            info.update(kind="python", script=m.group(1))
        elif first.startswith("#!") and "python" in first:
            info.update(kind="python", script=str(path))

    if info["kind"] is None:
        m = re.search(r"exec\s+(?:\S*/)?node\s+(?:-\S+\s+)*[\"']?(/[^\"'\s]+)", text) or re.search(
            r"require\(\s*[\"'](/[^\"']+)[\"']", text
        )
        if m:
            info.update(kind="node", node_target=m.group(1))
        elif first.startswith("#!") and re.search(r"\bnode\b", first):
            info.update(kind="node", node_target=str(path))

    for m in re.finditer(r"PYTHONPATH=[\"']?([^\"'\n]+)", text):
        for part in m.group(1).split(":"):
            part = re.sub(r"\$\{[^}]*\}", "", part).strip().rstrip("$")
            if part.startswith("/"):
                info["pythonpath"].append(part)
    return info


def scan_python_launcher(path, own_tops=()):
    info = parse_launcher(path)
    if info["kind"] != "python":
        return None
    extra = list(info["pythonpath"])
    stdlib = _stdlib_names()
    missing = {}
    queue = []

    if info["script"]:
        script = Path(info["script"])
        extra.append(str(script.parent))
        queue.append(script)
    elif info["module"]:
        top = info["module"].split(".")[0]
        spec = _find_spec(top, extra)
        if spec is None:
            return {top: str(path)}
        locs = list(spec.submodule_search_locations or [])
        if locs:
            main = Path(locs[0]) / "__main__.py"
            queue.append(main if main.is_file() else Path(locs[0]) / "__init__.py")
        elif spec.origin and spec.origin.endswith(".py"):
            queue.append(Path(spec.origin))

    own_tops = set(own_tops)
    seen = set()
    while queue and len(seen) < 150:
        f = queue.pop()
        if f in seen or not f.is_file():
            continue
        seen.add(f)
        for level, dotted, required in required_imports(f):
            if level:
                base = f.parent
                for _ in range(level - 1):
                    base = base.parent
                target = _resolve_local(dotted, [str(base)])
                if target:
                    queue.append(target)
                continue
            top = dotted.split(".")[0]
            if top in stdlib or top == "__future__":
                continue
            local = _resolve_local(dotted, extra)
            if local is None and top in own_tops:
                local = _resolve_local(dotted, sys.path)
            if local is not None:
                queue.append(local)
                continue
            if required and _find_spec(top, extra) is None:
                missing.setdefault(top, str(f))
    return missing


def scan_node_launcher(path):
    info = parse_launcher(path)
    target = info["node_target"]
    if target is None and os.path.islink(path):
        target = os.path.realpath(path)
        info["kind"] = "node"
    if info["kind"] != "node" or not target:
        return None
    if not os.path.exists(target):
        return {"dir": None, "missing": [], "problem": f"{target} does not exist"}
    d = Path(os.path.realpath(target)).parent
    pkg_dir = None
    for _ in range(6):
        if (d / "package.json").is_file():
            pkg_dir = d
            break
        if d.parent == d:
            break
        d = d.parent
    if pkg_dir is None:
        return None
    try:
        data = json.loads((pkg_dir / "package.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    deps = sorted((data.get("dependencies") or {}).keys())
    missing = []
    for dep in deps:
        ok = os.path.isdir(os.path.join(_PFX, "lib", "node_modules", dep))
        p = pkg_dir
        while not ok:
            if (p / "node_modules" / dep).exists():
                ok = True
            if p.parent == p:
                break
            p = p.parent
        if not ok:
            missing.append(dep)
    return {"dir": str(pkg_dir), "missing": missing, "problem": None}


def _run_list(cmd, timeout=15):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.stdout, r.returncode
    except Exception:
        return "", 1


def _dpkg_files(pkg):
    out, rc = _run_list(["dpkg", "-L", pkg])
    return [ln for ln in out.splitlines() if ln.startswith("/")] if rc == 0 else []


def _dpkg_installed(name):
    out, rc = _run_list(["dpkg-query", "-W", "-f=${Status}", name])
    return rc == 0 and "install ok installed" in out


def _tas_like_packages():
    out, rc = _run_list(["dpkg-query", "-W", "-f=${Package}\t${Maintainer}\t${Status}\n"])
    if rc != 0:
        return []
    names = []
    for ln in out.splitlines():
        parts = ln.split("\t")
        if len(parts) != 3 or "install ok installed" not in parts[2]:
            continue
        maint = parts[1].strip()
        if maint.startswith("@") and maint not in ("@termux", "@termux-user-repository"):
            names.append(parts[0])
    return sorted(names)


def _fix_cmd_for_modules(mods):
    pkgs, pips = [], []
    for m in mods:
        if m in TERMUX_PY_PKGS:
            pkgs.append(TERMUX_PY_PKGS[m])
        else:
            pips.append(PIP_ALIASES.get(m, m))
    pkgs = [p for p in dict.fromkeys(pkgs) if _NAME_OK.match(p)]
    pips = [p for p in dict.fromkeys(pips) if _NAME_OK.match(p)]
    cmds = []
    if pkgs:
        cmds.append("pkg install -y " + " ".join(shlex.quote(p) for p in pkgs))
    if pips:
        cmds.append("python3 -m pip install --break-system-packages " + " ".join(shlex.quote(p) for p in pips))
    return " && ".join(cmds) or None


def diagnose_package_runtime(pkg):
    checks = []
    files = _dpkg_files(pkg)
    if not files:
        return [Check(f"{pkg}", WARN, "package files not found (is it installed?)", category="Runtime")]

    own_tops = set()
    for f in files:
        m = re.search(r"/(?:site|dist)-packages/([^/]+)", f)
        if m:
            own_tops.add(re.sub(r"\.(?:py|so.*)$", "", m.group(1).split(".")[0]))

    for f in files:
        if os.path.islink(f) and not os.path.exists(f):
            checks.append(
                Check(
                    f"{pkg}: broken link",
                    FAIL,
                    f"{f} -> {os.readlink(f)}",
                    fix_cmd=f"pkg reinstall -y {shlex.quote(pkg)}" if _NAME_OK.match(pkg) else None,
                    fix_hint="The package was built with a link that points outside the .deb. "
                    "Reinstall after the maintainer rebuilds it.",
                    category="Runtime",
                )
            )

    bin_dir = os.path.join(_PFX, "bin")
    for f in files:
        if os.path.dirname(f) != bin_dir or not os.path.exists(f):
            continue
        name = os.path.basename(f)
        py_missing = scan_python_launcher(f, own_tops)
        if py_missing:
            mods = sorted(py_missing)
            checks.append(
                Check(
                    f"{pkg}: {name}",
                    FAIL,
                    "No module named: " + ", ".join(mods),
                    fix_cmd=_fix_cmd_for_modules(mods),
                    fix_hint="Install the missing modules. Ask the maintainer to rebuild the package so they are bundled.",
                    category="Runtime",
                )
            )
        node = scan_node_launcher(f)
        if node and node["problem"]:
            checks.append(Check(f"{pkg}: {name}", FAIL, node["problem"], category="Runtime"))
        elif node and node["missing"]:
            d = node["dir"]
            checks.append(
                Check(
                    f"{pkg}: {name}",
                    FAIL,
                    "Cannot find module: " + ", ".join(node["missing"][:6]),
                    fix_cmd=f"cd {shlex.quote(d)} && npm install --omit=dev --no-audit --no-fund",
                    fix_hint="Install the Node.js dependencies of the package.",
                    category="Runtime",
                )
            )

    out, rc = _run_list(["dpkg-query", "-W", "-f=${Depends}", pkg])
    if rc == 0 and out.strip():
        for dep in out.split(","):
            alts = [a.strip().split()[0] for a in dep.split("|") if a.strip()]
            if alts and not any(_dpkg_installed(a) for a in alts):
                first = alts[0]
                checks.append(
                    Check(
                        f"{pkg}: dependency",
                        FAIL,
                        f"{first} is not installed",
                        fix_cmd=f"pkg install -y {shlex.quote(first)}" if _NAME_OK.match(first) else None,
                        category="Runtime",
                    )
                )

    if not checks:
        checks.append(Check(f"{pkg}", PASS, "launchers, modules and dependencies look fine", category="Runtime"))
    return checks


def diagnose_runtime(names=None):
    if not _which("dpkg"):
        return [Check("Package runtime", SKIP, "dpkg not available", category="Runtime")]
    names = list(names) if names else _tas_like_packages()
    if not names:
        return [
            Check(
                "Package runtime",
                INFO,
                "no TAS packages found, pass names: tas doctor --modules <pkg>",
                category="Runtime",
            )
        ]
    checks = []
    for n in names:
        if not _NAME_OK.match(n):
            checks.append(Check(n, WARN, "invalid package name", category="Runtime"))
            continue
        checks.extend(diagnose_package_runtime(n))
    return checks


def chk_package_runtime():
    checks = diagnose_runtime()
    bad = [c for c in checks if c.status == FAIL]
    if bad:
        pkgs = sorted({c.name.split(":")[0] for c in bad})
        return Check(
            "Package runtime",
            FAIL,
            f"{len(bad)} problem(s) in: {', '.join(pkgs[:4])}",
            fix_hint="Run: tas doctor --modules --fix",
            category="Build",
        )
    real = [c for c in checks if c.status == PASS]
    if real:
        return Check("Package runtime", PASS, f"{len(real)} package(s) checked", category="Build")
    return Check("Package runtime", checks[0].status, checks[0].detail, category="Build")


SECTIONS = [
    ("System", [chk_termux, chk_arch, chk_storage]),
    ("Python", [chk_python, chk_pip, chk_textual, chk_python_importpath]),
    ("Tools", [chk_curl, chk_git, chk_dpkg, chk_pkg, chk_sha256sum]),
    ("TAS Installation", [chk_tas_binary, chk_tas_wrapper, chk_tas_version, chk_tas_can_run, chk_tasctl]),
    ("Repository", [chk_repo_file, chk_apt_lists]),
    ("Project", [chk_packages_dir, chk_build_package_sh, chk_termux_build, chk_build_sh_scan]),
    ("Build", [chk_last_build, chk_output_dir, chk_installed_tas_pkgs, chk_package_runtime]),
    ("Network", [chk_network, chk_github]),
]
ALL_FNS = [fn for _, fns in SECTIONS for fn in fns]


def print_summary(checks, mode_fix=False):
    blank()
    header_bar("DIAGNOSIS SUMMARY")
    blank()

    n_pass = sum(1 for c in checks if c.status == PASS)
    n_warn = sum(1 for c in checks if c.status == WARN)
    n_fail = sum(1 for c in checks if c.status == FAIL)
    n_info = sum(1 for c in checks if c.status in (INFO, SKIP))

    w = W() - 6
    rows = [
        ("Checks passed", str(n_pass), n_fail == 0 and n_warn == 0),
        ("Warnings", str(n_warn), n_warn == 0),
        ("Failures", str(n_fail), n_fail == 0),
        ("Info / Skip", str(n_info), True),
    ]
    lw = max(len(r[0]) for r in rows) + 2
    print(f" {DIM}┌{'─' * (w + 2)}┐{R}")
    for label, val, good in rows:
        col = BGRN if good else (BYLW if "Warn" in label else BRED)
        pad = max(0, w - 2 - lw - len(val))
        print(f" {DIM}│{R} {DIM}{label:<{lw}}{R} {col}{B}{val}{R}{' ' * pad}  {DIM}│{R}")
    print(f" {DIM}└{'─' * (w + 2)}┘{R}")
    blank()

    if n_fail:
        thick_rule(BRED)
        print(vcenter(f"{BRED}{B}FAIL  --  {n_fail} error(s) must be fixed{R}", W()))
        thick_rule(BRED)
    elif n_warn:
        thick_rule(BYLW)
        print(vcenter(f"{BYLW}{B}WARN  --  {n_warn} item(s) to review{R}", W()))
        thick_rule(BYLW)
    else:
        thick_rule(BGRN)
        print(vcenter(f"{BGRN}{B}ALL PASS  --  environment is healthy{R}", W()))
        thick_rule(BGRN)
    blank()

    actions = [c for c in checks if c.status in (FAIL, WARN) and (c.fix_cmd or c.fix_hint or c.fix_fn)]
    if actions and not mode_fix:
        section("Action items")
        for c in actions:
            col = BRED if c.status == FAIL else BYLW
            fix = c.fix_cmd or c.fix_hint or ""
            print(f"\n  {col}{B}{c.status}{R}  {B}{c.name}{R}")
            if c.category:
                print(f"  {DIM}category: {c.category}{R}")
            if fix:
                code(fix.split("\n")[0])
        blank()
        callout("TIP", "Run with --fix to automatically apply fixes where possible.", "tip")
        blank()


def print_help():
    blank()
    header_bar("SMART DOCTOR -- HELP")
    blank()
    rows = [
        ("(no args)", "Full environment diagnosis"),
        ("--fix", "Diagnose + auto-fix all fixable issues"),
        ("--pkg <name>", "Deep diagnosis of one package's build.sh"),
        ("--modules [name]", "Find missing modules in installed packages"),
        ("--brief", "One-line-per-check output"),
        ("--json", "JSON output for CI / scripting"),
        ("--help", "Show this help"),
    ]
    w = W() - 6
    lw = max(len(r[0]) for r in rows) + 2
    print(f" {DIM}┌{'─' * (w + 2)}┐{R}")
    for cmd, desc in rows:
        pad = max(0, w - 2 - lw - 2 - len(desc))
        print(f" {DIM}│{R} {BCYN}{cmd:<{lw}}{R}  {desc}{' ' * pad}   {DIM}│{R}")
    print(f" {DIM}└{'─' * (w + 2)}┘{R}")
    blank()
    section("Sections in full diagnosis")
    blank()
    cats = [
        ("System", "Termux env, CPU arch, free storage"),
        ("Python", "Python version, pip, textual, site-packages"),
        ("Tools", "curl, git, dpkg, pkg, sha256sum"),
        ("TAS Installation", "binary, wrapper, version, importable, tasctl"),
        ("Repository", "apt sources.list.d/tas.list, list freshness"),
        ("Project", "packages/, build-package.sh, termux-build, build.sh scan"),
        ("Build", "incomplete builds, output .deb, installed packages, missing modules"),
        ("Network", "repo URL, GitHub API"),
    ]
    lw2 = max(len(c[0]) for c in cats) + 2
    for cat, desc in cats:
        print(f"  {BCYN}{cat:<{lw2}}{R}  {DIM}{desc}{R}")
    blank()
    section("--pkg: what it checks")
    blank()
    items = [
        "File exists and is not empty",
        "Bash syntax (bash -n)",
        "All 7 required TERMUX_PKG_* fields",
        "VERSION format (must start with digit)",
        "SHA256 format (64 hex chars or SKIP)",
        "Forbidden patterns (sudo, apt-get, hardcoded paths, etc.)",
        "termux_step_make_install() presence",
        "TERMUX_PKG_BUILD_IN_SRC consistency",
        "Dependency availability via pkg info",
        "SRCURL HTTP reachability",
    ]
    for item in items:
        print(f"  {BCYN}+{R}  {item}")
    blank()
    section("Examples")
    blank()
    code("tas doctor")
    code("tas doctor --fix")
    code("tas doctor --pkg baxter")
    code("tas doctor --pkg mypackage --fix")
    code("tas doctor --modules")
    code("tas doctor --modules holehe --fix")
    code("tas doctor --brief")
    code("tas doctor --json | python3 -m json.tool")
    blank()


def main():
    args = sys.argv[1:]
    mode_fix = "--fix" in args
    mode_brief = "--brief" in args
    mode_json = "--json" in args
    mode_help = "--help" in args or "-h" in args
    mode_modules = "--modules" in args
    mode_pkg = None
    if "--pkg" in args:
        i = args.index("--pkg")
        if i + 1 < len(args):
            mode_pkg = args[i + 1]

    if not mode_json:
        banner()

    if mode_help:
        print_help()
        sys.exit(0)

    if mode_modules:
        i = args.index("--modules")
        names = [a for a in args[i + 1 :] if not a.startswith("-")]
        section("Package runtime check")
        blank()
        checks = diagnose_runtime(names)
        for c in checks:
            c.print_line()
            run_fix(c, mode_fix)
        blank()
        n_fail = sum(1 for c in checks if c.status == FAIL)
        if n_fail:
            callout(
                "FAIL",
                f"{n_fail} problem(s) found. Run 'tas doctor --modules --fix' to apply the suggested fixes.",
                "fail",
            )
        else:
            callout("PASS", "No missing modules or dependencies found.", "pass")
        blank()
        sys.exit(1 if n_fail else 0)

    if mode_pkg:
        section(f"build.sh diagnosis: {mode_pkg}")
        blank()
        checks = diagnose_build_sh(mode_pkg)
        for c in checks:
            c.print_line()
            run_fix(c, mode_fix)
        blank()
        n_fail = sum(1 for c in checks if c.status == FAIL)
        n_warn = sum(1 for c in checks if c.status == WARN)
        if n_fail:
            callout(
                "FAIL",
                f"Package '{mode_pkg}' has {n_fail} error(s) that must be fixed before building or submitting a PR.",
                "fail",
            )
        elif n_warn:
            callout("WARN", f"Package '{mode_pkg}' has {n_warn} warning(s). Review before submitting PR.", "note")
        else:
            callout("PASS", f"build.sh for '{mode_pkg}' looks good.", "pass")
        blank()
        sys.exit(1 if n_fail else 0)

    if mode_brief:
        all_checks = [fn() for fn in ALL_FNS]
        for c in all_checks:
            sym = {PASS: "+", WARN: "!", FAIL: "X", INFO: "-", SKIP: "-"}.get(c.status, "?")
            col = {PASS: BGRN, WARN: BYLW, FAIL: BRED}.get(c.status, DIM)
            print(f"  {col}[{sym}]{R} {c.name}: {DIM}{c.detail}{R}")
        blank()
        sys.exit(1 if any(c.status == FAIL for c in all_checks) else 0)

    if mode_json:
        all_checks = [fn() for fn in ALL_FNS]
        data = {
            "version": VERSION,
            "total": len(all_checks),
            "passed": sum(1 for c in all_checks if c.status == PASS),
            "warned": sum(1 for c in all_checks if c.status == WARN),
            "failed": sum(1 for c in all_checks if c.status == FAIL),
            "checks": [c.to_dict() for c in all_checks],
        }
        print(json.dumps(data, indent=2))
        sys.exit(0)

    if mode_fix:
        callout(
            "FIX MODE",
            "Doctor will attempt to auto-fix issues as it finds them. "
            "Items with no automatic fix will show manual instructions.",
            "tip",
        )
        blank()

    all_checks = []
    for sec_name, fns in SECTIONS:
        section(sec_name)
        blank()
        for fn in fns:
            c = fn()
            c.print_line()
            if run_fix(c, mode_fix):
                c = fn()
                print(f"  {DIM}↳ re-checked:{R}")
                c.print_line()
            all_checks.append(c)
        blank()

    print_summary(all_checks, mode_fix=mode_fix)
    sys.exit(1 if any(c.status == FAIL for c in all_checks) else 0)


def run():
    try:
        main()
    except KeyboardInterrupt:
        blank()
        rule("─", DIM)
        print(f"  {BYLW}Cancelled.{R}")
        rule("─", DIM)
        blank()
        sys.exit(130)


if __name__ == "__main__":
    run()
