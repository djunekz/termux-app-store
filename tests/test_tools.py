import importlib.util
import sys
from pathlib import Path

import pytest

TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools"
TOOL_FILES = sorted(path for path in TOOLS_DIR.glob("*.py") if not path.name.startswith("__"))
TOOLS_WITH_MAIN = [path for path in TOOL_FILES if "def main(" in path.read_text(encoding="utf-8")]


def load_tool(path: Path):
    module_name = f"tas_tool_{path.stem}"
    spec = importlib.util.spec_from_file_location(module_name, str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def test_tools_directory_contains_expected_modules():
    names = {path.name for path in TOOL_FILES}
    assert {"build.py", "package_manager.py"} <= names


@pytest.mark.parametrize("path", TOOL_FILES, ids=lambda path: path.name)
def test_tool_imports_cleanly(path):
    module = load_tool(path)
    assert Path(module.__file__).resolve() == path.resolve()


@pytest.mark.parametrize("path", TOOLS_WITH_MAIN, ids=lambda path: path.name)
def test_tool_main_runs_in_an_isolated_directory(path, tmp_path, monkeypatch):
    module = load_tool(path)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", [path.name])
    assert module.main() in (None, 0, 1)
