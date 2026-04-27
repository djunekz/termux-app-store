#!/usr/bin/env python3
# Termux App Store -- Repository Installer
# github.com/djunekz/termux-app-store

import os
import sys
import subprocess
import platform
import shutil
import time

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
REPO_ENTRY   = f"deb [trusted=yes] {REPO_URL} termux main"
_PREFIX      = os.environ.get("PREFIX", "/data/data/com.termux/files/usr")
SOURCES_DIR  = os.path.join(_PREFIX, "etc/apt/sources.list.d")
SOURCES_FILE = os.path.join(SOURCES_DIR, "tas.list")
MAIN_SOURCES = os.path.join(_PREFIX, "etc/apt/sources.list")

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

def repo_already_added() -> bool:
    if not os.path.exists(SOURCES_FILE):
        return False
    with open(SOURCES_FILE) as f:
        for line in f:
            s = line.strip()
            if s and not s.startswith("#") and REPO_URL in s:
                return True
    return False

def repo_in_main_sources() -> bool:
    if not os.path.exists(MAIN_SOURCES):
        return False
    with open(MAIN_SOURCES) as f:
        return REPO_URL in f.read()

def add_repo() -> bool:
    step("Adding repository to sources")
    path_box("file", SOURCES_FILE)
    blank()
    entry_box("entry", REPO_ENTRY)
    blank()
    os.makedirs(SOURCES_DIR, exist_ok=True)
    try:
        with open(SOURCES_FILE, "w") as f:
            f.write("# Termux App Store\n")
            f.write("# https://github.com/djunekz/termux-app-store\n")
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
    if os.path.exists(SOURCES_FILE):
        os.remove(SOURCES_FILE)
        ok(f"Removed: {SOURCES_FILE}")
        return True
    else:
        warn(f"File not found: {SOURCES_FILE}")
        return False


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
    code_line(f"rm {SOURCES_FILE}")
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

    if repo_already_added():
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
        info("It will also be added to sources.list.d/tas.list (cleaner)")

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
