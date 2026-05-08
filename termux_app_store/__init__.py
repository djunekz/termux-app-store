"""
termux-app-store
~~~~~~~~~~~~~~~~
The first offline-first, source-based TUI package manager built natively for Termux.

:copyright: (c) 2026 djunekz
:license: MIT, see LICENSE for more details.
"""

__version__ = "0.3.0"
__author__ = "djunekz"
__license__ = "MIT"

from termux_app_store.termux_app_store import run_tui
from termux_app_store.termux_app_store_cli import run_cli

__all__ = ["run_tui", "run_cli", "__version__"]
