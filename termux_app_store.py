#!/usr/bin/env python3
"""TUI entrypoint for the Python (source) edition."""

# Keep a literal APP_VERSION here because install.sh extracts it with grep.
APP_VERSION = "0.2.0"

from termux_app_store.tui import main


if __name__ == "__main__":
    main()
