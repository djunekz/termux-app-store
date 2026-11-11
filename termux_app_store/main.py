#!/usr/bin/env python3
import sys
from pathlib import Path

_this_dir = Path(__file__).resolve().parent
_is_script_mode = not __package__ or __package__ == "" or __name__ == "__main__" and __package__ is None

if _is_script_mode and str(_this_dir) not in sys.path:
    sys.path.insert(0, str(_this_dir.parent))
    sys.path.insert(0, str(_this_dir))

try:
    from termux_app_store.termux_app_store import run_tui
    from termux_app_store.termux_app_store_cli import run_cli
except ModuleNotFoundError:
    from termux_app_store_cli import run_cli  # type: ignore

    from termux_app_store import run_tui  # type: ignore


_REPO_CMDS = {"install-repo", "uninstall-repo", "repo", "doctor", "guide", "guidebook"}


def _auto_repo():
    if len(sys.argv) > 1 and sys.argv[1] in _REPO_CMDS | {"help", "-h", "--help", "version", "-v"}:
        return
    try:
        try:
            from termux_app_store.repo_setup import ensure_repo
        except ModuleNotFoundError:
            from repo_setup import ensure_repo  # type: ignore
        ensure_repo()
    except Exception:
        pass


def main():
    _auto_repo()
    if len(sys.argv) > 1:
        run_cli()
    else:
        run_tui()


def tas():
    _auto_repo()
    if len(sys.argv) > 1:
        run_cli()
    else:
        run_tui()


if __name__ == "__main__":
    main()
