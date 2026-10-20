#!/usr/bin/env python3
# Termux App Store -- Repository Installer
# github.com/djunekz/termux-app-store

import os
import sys
import subprocess
import platform
import shutil
import time
import tempfile
import urllib.request
import urllib.error

R    = "\033[0m"
B    = "\033[1m"
DIM  = "\033[2m"
IT   = "\033[3m"

RED  = "\033[31m"
GRN  = "\033[32m"
CYN  = "\033[36m"

BRED = "\033[91m"
BGRN = "\033[92m"
BYLW = "\033[93m"
BCYN = "\033[96m"
BWHT = "\033[97m"

BG_BBLK = "\033[100m"
BG_BBLU = "\033[104m"
BG_BRED = "\033[101m"
BG_BGRN = "\033[102m"

REPO_URL     = "https://djunekz.github.io/termux-app-store"
KEY_URL      = f"{REPO_URL}/termux-app-store.gpg"
_PREFIX      = os.environ.get("PREFIX", "/data/data/com.termux/files/usr")
SOURCES_DIR  = os.path.join(_PREFIX, "etc/apt/sources.list.d")
SOURCES_FILE = os.path.join(SOURCES_DIR, "tas.list")
MAIN_SOURCES = os.path.join(_PREFIX, "etc/apt/sources.list")
KEYRING_DIR  = os.path.join(_PREFIX, "etc/apt/keyrings")
KEYRING_FILE = os.path.join(KEYRING_DIR, "termux-app-store.gpg")
REPO_ENTRY   = f"deb [signed-by={KEYRING_FILE}] {REPO_URL} termux main"

KEY_FINGERPRINT = os.environ.get("TAS_KEY_FPR", "").replace(" ", "").upper()
MAX_KEY_SIZE    = 64 * 1024

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

def log(msg):
    print(f"  {BCYN}{B}::{R} {msg}")

def ok(msg):
    print(f"  {BGRN}{B}OK{R}  {msg}")

def warn(msg):
    print(f"  {BYLW}{B}!!{R}  {msg}", file=sys.stderr)

def err(msg):
    print(f"  {BRED}{B}XX{R}  {msg}", file=sys.stderr)

def info(msg):
    print(f"      {DIM}{msg}{R}")

def step(title):
    blank()
    w     = W()
    inner = f" {title}  "
    pad   = max(0, w - len(inner) - 2)
    print(f" {BCYN}{B}>{R} {B}{BWHT}{title}{R}")
    print(f" {DIM}{'─' * (w - 2)}{R}")

def kv(label, value, lw=18):
    print(f"  {DIM}{label:<{lw}}{R}  {BCYN}{value}{R}")

def sep():
    rule("─", DIM)

def code_line(cmd, indent=4):
    pad_l = " " * indent
    print(f"{pad_l}{BYLW}${R} {BCYN}{cmd}{R}")

def path_box(label, path):
    w        = W() - 2
    dash_w   = w + 2
    lbl_str  = f" {label} "
    fill     = max(0, dash_w - len(lbl_str))
    top      = f"{DIM}┌{lbl_str}{'─' * fill}┐{R}"
    pad      = max(0, w - len(path))
    mid      = f"{DIM}│{R} {BCYN}{path}{R}{' ' * pad} {DIM}│{R}"
    bot      = f"{DIM}└{'─' * dash_w}┘{R}"
    print(top); print(mid); print(bot)

def entry_box(label, entry):
    import textwrap
    w       = W() - 2
    dash_w  = w + 2
    lbl_str = f" {label} "
    fill    = max(0, dash_w - len(lbl_str))
    print(f"{DIM}┌{lbl_str}{'─' * fill}┐{R}")
    for chunk in textwrap.wrap(entry, w - 2) or [entry]:
        pad = max(0, w - len(chunk))
        print(f"{DIM}│{R} {IT}{DIM}{chunk}{R}{' ' * pad} {DIM}│{R}")
    print(f"{DIM}└{'─' * dash_w}┘{R}")

_LOGO = [
    r" _______ _______ _______",
    r"|__   __|   _   |   ____|",
    r"   | |  |  |_|  |__\  \ ",
    r"   | |  |   _   | __\  \  ",
    r"   |_|  |_| |_| |_______| ",
]

_LOGO_BLOCK = """\
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
    for line in _LOGO_BLOCK.splitlines():
        print(vcenter(f"{BCYN}{B}{line}{R}", w))
    blank()
    print(vcenter(f"{BWHT}{B}Termux App Store{R}", w))
    print(vcenter(f"{DIM}Repository Installer  --  github.com/djunekz/termux-app-store{R}", w))
    print(vcenter(f"{DIM}by {BGRN}@djunekz{R}", w))
    blank()
    thick_rule(BCYN, w)
    blank()

def is_termux() -> bool:
    return "com.termux" in _PREFIX or os.path.exists("/data/data/com.termux")

def _active_lines(path):
    try:
        with open(path) as f:
            return [ln.strip() for ln in f
                    if ln.strip() and not ln.strip().startswith("#")]
    except OSError:
        return []

def repo_is_legacy() -> bool:
    return any(REPO_URL in ln and "trusted=yes" in ln
               for ln in _active_lines(SOURCES_FILE))

def repo_already_added() -> bool:
    if not os.path.exists(KEYRING_FILE):
        return False
    return any(REPO_URL in ln and "signed-by=" in ln and "trusted=yes" not in ln
               for ln in _active_lines(SOURCES_FILE))

def repo_in_main_sources() -> bool:
    if not os.path.exists(MAIN_SOURCES):
        return False
    with open(MAIN_SOURCES) as f:
        return REPO_URL in f.read()

def _is_openpgp_binary(data: bytes) -> bool:
    if not data or data.startswith(b"-----BEGIN"):
        return False
    return data[0] in (0x98, 0x99, 0x9A, 0x9B, 0xC6)

def _key_fingerprints(path):
    gpg = shutil.which("gpg")
    if not gpg:
        return None
    try:
        out = subprocess.run(
            [gpg, "--batch", "--no-tty", "--show-keys", "--with-colons", path],
            capture_output=True, text=True, timeout=30,
        ).stdout
    except Exception:
        return None
    return [ln.split(":")[9] for ln in out.splitlines()
            if ln.startswith("fpr:") and len(ln.split(":")) > 9]

def install_key() -> bool:
    step("Installing repository signing key")
    path_box("keyring", KEYRING_FILE)
    blank()
    info(f"Downloading: {KEY_URL}")

    try:
        req = urllib.request.Request(KEY_URL, headers={"User-Agent": "tas-install-repo"})
        with urllib.request.urlopen(req, timeout=20) as r:
            data = r.read(MAX_KEY_SIZE + 1)
    except (urllib.error.URLError, OSError) as e:
        err(f"Could not download the signing key: {e}")
        info("The repository will NOT be added without a verifiable key.")
        return False

    if len(data) > MAX_KEY_SIZE or not _is_openpgp_binary(data):
        err("Downloaded file is not a valid binary OpenPGP public key")
        return False

    os.makedirs(KEYRING_DIR, exist_ok=True)
    tmp_fd, tmp_path = tempfile.mkstemp(dir=KEYRING_DIR, prefix=".tas-key-")
    try:
        with os.fdopen(tmp_fd, "wb") as f:
            f.write(data)

        fprs = _key_fingerprints(tmp_path)
        if KEY_FINGERPRINT:
            if fprs is None:
                err("TAS_KEY_FPR is set but 'gpg' is not installed (pkg install gnupg)")
                return False
            if KEY_FINGERPRINT not in [x.upper() for x in fprs]:
                err("Key fingerprint does NOT match the pinned fingerprint")
                for x in fprs:
                    info(f"got      : {x}")
                info(f"expected : {KEY_FINGERPRINT}")
                return False
            ok("Fingerprint matches pinned value")
        elif fprs:
            for x in fprs:
                kv("Fingerprint", x)
        else:
            info("Install 'gnupg' to display/verify the key fingerprint")

        os.chmod(tmp_path, 0o644)
        os.replace(tmp_path, KEYRING_FILE)
        tmp_path = None
        ok(f"Written: {KEYRING_FILE}")
        return True
    except Exception as e:
        err(f"Failed to install key: {e}")
        return False
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)

def add_repo() -> bool:
    if repo_is_legacy():
        warn("Old insecure entry ([trusted=yes]) found -- migrating to signed-by")

    if not install_key():
        return False

    step("Adding repository to sources")
    path_box("file", SOURCES_FILE)
    blank()
    entry_box("entry", REPO_ENTRY)
    blank()
    try:
        os.makedirs(SOURCES_DIR, exist_ok=True)
        with open(SOURCES_FILE, "w") as f:
            f.write(f"{REPO_ENTRY}\n")
        ok(f"Written: {SOURCES_FILE}")
        return True
    except PermissionError:
        err(f"Permission denied writing to {SOURCES_FILE}")
        info("Try: python3 install-repo.py  (without sudo)")
        return False
    except Exception as e:
        err(f"Failed to write file: {e}")
        return False

def remove_repo() -> bool:
    step("Removing repository")
    removed = False
    for path in (SOURCES_FILE, KEYRING_FILE):
        if os.path.exists(path):
            os.remove(path)
            ok(f"Removed: {path}")
            removed = True
        else:
            warn(f"File not found: {path}")
    return removed

def run_pkg_update() -> bool:
    step("Running pkg update")
    try:
        result = subprocess.run(["pkg", "update", "-y"])
        if result.returncode == 0:
            ok("pkg update complete")
        else:
            warn("pkg update finished with warnings (usually safe to ignore)")
        return True
    except FileNotFoundError:
        warn("'pkg' not found -- run manually:")
        code_line("pkg update")
        return False
    except Exception as e:
        warn(f"pkg update error: {e}")
        return False

def prompt(question, default_yes=True) -> bool:
    if not sys.stdin.isatty():
        return default_yes
    hint = f"{BWHT}Y{R}{DIM}/n{R}" if default_yes else f"{DIM}y/{R}{BWHT}N{R}"
    blank()
    sep()
    try:
        answer = input(f"  {BCYN}{B}?{R}  {question} [{hint}] ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        blank()
        return False
    sep()
    if default_yes:
        return answer not in ("n", "no")
    else:
        return answer in ("y", "yes")

def show_next_steps():
    blank()
    header_bar("NEXT STEPS")
    blank()

    print(f"  {B}{BWHT}Install a package{R}")
    blank()
    code_line("pkg install <package-name>")
    code_line("pkg install baxter")
    code_line("pkg install aura")
    blank()
    sep()

    print(f"  {B}{BWHT}Remove this repository{R}")
    blank()
    code_line(f"rm {SOURCES_FILE} {KEYRING_FILE}")
    code_line("pkg update")
    blank()
    print(f"  {DIM}or via tasctl:{R}")
    code_line("tasctl uninstall-repo")
    blank()
    sep()

    print(f"  {B}{BWHT}Repository URL{R}")
    blank()
    path_box("url", REPO_URL)
    blank()

def main():
    banner()

    step("Checking environment")
    blank()

    if not is_termux():
        warn("This script is designed for Termux (Android)")
        warn("Continuing -- but paths may differ from expected")
        info(f"PREFIX: {os.environ.get('PREFIX', '(not set)')}")
    else:
        ok("Running inside Termux")

    arch = platform.machine()
    ok(f"Architecture : {arch}")
    blank()
    kv("Sources dir",   SOURCES_DIR)
    kv("Sources file",  SOURCES_FILE)
    kv("Repository",    REPO_URL)
    blank()

    if repo_already_added() and not repo_is_legacy():
        blank()
        header_bar("REPOSITORY ALREADY CONFIGURED")
        blank()
        ok(f"Found in: {SOURCES_FILE}")
        blank()
        if not prompt("Re-install / refresh the entry?", default_yes=False):
            blank()
            ok("No changes made.")
            show_next_steps()
            return

    if repo_in_main_sources():
        blank()
        warn("Repository URL detected in main sources.list")
        info("Remove that line (especially if it has [trusted=yes]); the signed")
        info("entry in sources.list.d/tas.list is used instead")

    if not add_repo():
        blank()
        err("Repository installation failed.")
        blank()
        sys.exit(1)

    if prompt("Run pkg update now?", default_yes=True):
        if not run_pkg_update():
            blank()
            warn("Run manually:")
            code_line("pkg update")
    else:
        blank()
        info("Run 'pkg update' manually to activate the repository.")

    blank()
    thick_rule(BGRN)
    print(vcenter(f"{BGRN}{B}Repository installed successfully{R}", W()))
    thick_rule(BGRN)
    blank()

    show_next_steps()

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
