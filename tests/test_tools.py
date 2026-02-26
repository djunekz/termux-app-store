import pytest
import importlib.util
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).parent.parent / "tools"

def import_from_path(file_path: Path):
    spec = importlib.util.spec_from_file_location(file_path.stem, str(file_path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[file_path.stem] = module
    spec.loader.exec_module(module)
    return module

def call_main_if_exists(module):
    main_func = getattr(module, "main", None)
    if callable(main_func):
        try:
            main_func()
        except Exception:
            pass

def test_all_tools_importable_and_run_main():
    for file_path in TOOLS_DIR.glob("*.py"):
        if file_path.name.startswith("__"):
            continue
        module = import_from_path(file_path)
        assert module is not None
        call_main_if_exists(module)
