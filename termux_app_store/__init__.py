from .core.binary_core import BinaryCache
from .core.mirrors import MirrorManager
from .core.package import Package
from .core.validator import PackageValidator, validate_package


def run_tui(*args, **kwargs):
    from termux_app_store.termux_app_store import run_tui as _run_tui
    return _run_tui(*args, **kwargs)


def run_cli(*args, **kwargs):
    from termux_app_store.termux_app_store_cli import run_cli as _run_cli
    return _run_cli(*args, **kwargs)


"""
termux-app-store
~~~~~~~~~~~~~~~~
The first offline-first, source-based TUI package manager built natively for Termux.

:copyright: (c) 2026 djunekz
:license: MIT, see LICENSE for more details.
"""

__version__ = "0.8.5"
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
