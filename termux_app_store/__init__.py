from .core.binary_core import BinaryCache
from .core.mirrors import MirrorManager
from .core.package import Package
from .core.validator import PackageValidator, validate_package
from termux_app_store.termux_app_store import run_tui
from termux_app_store.termux_app_store_cli import run_cli

"""
termux-app-store
~~~~~~~~~~~~~~~~
The first offline-first, source-based TUI package manager built natively for Termux.

:copyright: (c) 2026 djunekz
:license: MIT, see LICENSE for more details.
"""

__version__ = "0.4.5"
__author__ = "djunekz"
__license__ = "MIT"
__all__ = [
    "BinaryCache",
    "run_tui",
    "run_cli",
    "__version__",
    "MirrorManager",
    "Package",
    "PackageValidator",
    "validate_package",
]
