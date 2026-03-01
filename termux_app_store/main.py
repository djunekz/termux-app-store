#!/usr/bin/env python3
import sys
from termux_app_store import run_tui
from termux_app_store_cli import run_cli

def main():
    if len(sys.argv) > 1:
        run_cli()
    else:
        run_tui()

if __name__ == "__main__": # pragma: no cover
    main() # pragma: no cover
