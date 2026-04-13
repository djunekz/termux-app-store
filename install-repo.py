#!/usr/bin/env python3
import os
import sys
import subprocess
import platform


REPO_URL    = "https://djunekz.github.io/termux-app-store"
REPO_ENTRY  = f"deb [trusted=yes] {REPO_URL} termux main"
SOURCES_DIR = os.path.join(
    os.environ.get("PREFIX", "/data/data/com.termux/files/usr"),
    "etc/apt/sources.list.d"
)
SOURCES_FILE = os.path.join(SOURCES_DIR, "tas.list")


R       = "\033[0m"
BOLD    = "\033[1m"
DIM     = "\033[2m"
CYAN    = "\033[96m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
RED     = "\033[91m"
MAGENTA = "\033[35m"


def log(msg):  print(f" {CYAN}{BOLD}[*]{R} {msg}")
def ok(msg):   print(f" {GREEN}{BOLD}[✔]{R} {msg}")
def warn(msg): print(f" {YELLOW}{BOLD}[!]{R} {msg}", file=sys.stderr)
def err(msg):  print(f" {RED}{BOLD}[✗]{R} {msg}", file=sys.stderr)
def info(msg): print(f"     {DIM}{msg}{R}")
def step(msg): print(f"\n {MAGENTA}{BOLD}→{R} {msg}")
def sep():     print(f"  {DIM}{'─' * 44}{R}")


def banner():
    print(f"""
{CYAN}{BOLD}       ████████╗ █████╗ ███████╗
          ██╔══╝██╔══██╗██╔════╝
          ██║   ███████║███████╗
          ██║   ██╔══██║╚════██║
          ██║   ██║  ██║███████║
          ╚═╝   ╚═╝  ╚═╝╚══════╝{R}
       {DIM}{YELLOW}Termux App Store - Repository Installer{R}
                  {DIM}{YELLOW}by {GREEN}@djunekz{R}
""")


def is_termux() -> bool:
    prefix = os.environ.get("PREFIX", "")
    return "com.termux" in prefix or os.path.exists("/data/data/com.termux")


def repo_already_added() -> bool:
    if not os.path.exists(SOURCES_FILE):
        return False
    with open(SOURCES_FILE) as f:
        for line in f:
            stripped = line.strip()
            if stripped and not stripped.startswith("#") and REPO_URL in stripped:
                return True
    return False


def repo_in_main_sources() -> bool:
    main = os.path.join(
        os.environ.get("PREFIX", "/data/data/com.termux/files/usr"),
        "etc/apt/sources.list"
    )
    if not os.path.exists(main):
        return False
    with open(main) as f:
        return REPO_URL in f.read()


def add_repo() -> bool:
    step("Adding repository...")
    info(f"File  : {SOURCES_FILE}")
    info(f"Entry : {REPO_ENTRY}")

    os.makedirs(SOURCES_DIR, exist_ok=True)

    try:
        with open(SOURCES_FILE, "w") as f:
            f.write("# Termux App Store — https://github.com/djunekz/termux-app-store\n")
            f.write(f"{REPO_ENTRY}\n")
        ok(f"Repository added: {SOURCES_FILE}")
        return True
    except PermissionError:
        err(f"Permission denied writing to {SOURCES_FILE}")
        info("Try running directly: python3 install-repo.py")
        return False
    except Exception as e:
        err(f"Failed to write file: {e}")
        return False


def remove_repo() -> bool:
    step("Removing repository...")
    if os.path.exists(SOURCES_FILE):
        os.remove(SOURCES_FILE)
        ok(f"Removed: {SOURCES_FILE}")
        return True
    else:
        warn(f"Repository file not found: {SOURCES_FILE}")
        return False


def run_pkg_update() -> bool:
    step("Running pkg update...")
    try:
        result = subprocess.run(["pkg", "update", "-y"])
        if result.returncode == 0:
            ok("pkg update complete")
        else:
            warn("pkg update finished with warnings (usually safe to ignore)")
        return True
    except FileNotFoundError:
        warn("'pkg' not found — run manually: pkg update")
        return False
    except Exception as e:
        warn(f"pkg update failed: {e}")
        return False


def show_next_steps():
    print(f"""
{CYAN}{BOLD}Install a package:{R}

  {GREEN}pkg install baxter{R}
  {GREEN}pkg install aura{R}
  {GREEN}pkg install <package-name>{R}

{CYAN}{BOLD}Remove this repository:{R}

  {GREEN}rm {SOURCES_FILE}{R}
  {GREEN}pkg update{R}

  {DIM}or via tasctl:{R}
  {GREEN}tasctl uninstall-repo{R}

{CYAN}{BOLD}Repository URL:{R}
  {DIM}{REPO_URL}{R}
""")


def main():
    banner()

    step("Checking environment...")

    if not is_termux():
        warn("This script is designed for Termux (Android)")
        warn("Continuing, but paths may differ")
        info(f"PREFIX: {os.environ.get('PREFIX', '(not set)')}")

    arch = platform.machine()
    ok(f"Architecture : {arch}")
    info(f"Sources dir  : {SOURCES_DIR}")

    if repo_already_added():
        ok("Repository is already configured!")
        info(f"File: {SOURCES_FILE}")

        print()
        sep()
        answer = input(f"  {YELLOW}Re-install / refresh the entry?{R} [y/N] ").strip().lower()
        if answer not in ("y", "yes"):
            ok("No changes made.")
            show_next_steps()
            return

    if repo_in_main_sources():
        warn("Repository detected in main sources.list")
        info("Will also add it to sources.list.d/tas.list (cleaner approach)")

    if not add_repo():
        sys.exit(1)

    print()
    sep()
    answer = input(f"  {CYAN}Run pkg update now?{R} [Y/n] ").strip().lower()
    if answer not in ("n", "no"):
        if not run_pkg_update():
            warn("Run manually: pkg update")
    else:
        info("Run 'pkg update' manually to activate the repository")

    print(f"\n  {GREEN}{BOLD}✔ Termux App Store repository installed successfully!{R}")
    show_next_steps()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {YELLOW}Cancelled.{R}\n")
        sys.exit(130)
                     
