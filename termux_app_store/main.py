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


def main():
    if len(sys.argv) > 1:
        run_cli()
    else:
        run_tui()


def tas():
    if len(sys.argv) > 1:
        run_cli()
    else:
        run_tui()


if __name__ == "__main__":
    main()
