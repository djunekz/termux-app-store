import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGE_DIR = ROOT / "termux_app_store"


def _load(name: str, path: Path):
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def load_store_common():
    return _load("tas_store_common_under_test", PACKAGE_DIR / "store_common.py")


def load_cli():
    return _load("tas_cli_under_test", PACKAGE_DIR / "termux_app_store_cli.py")
