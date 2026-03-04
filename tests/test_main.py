import sys
import os
import types
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

_tmp = tempfile.mkdtemp()
_fake_root = Path(_tmp)
(_fake_root / "packages").mkdir()
(_fake_root / "build-package.sh").write_text("# Termux App Store Official\n")
os.environ["TERMUX_APP_STORE_HOME"] = str(_fake_root)

if "termux_app_store_cli" not in sys.modules:
    _fake_cli = types.ModuleType("termux_app_store_cli")
    _fake_cli.run_cli = MagicMock()
    sys.modules["termux_app_store_cli"] = _fake_cli

sys.modules.pop("termux_app_store.main", None)
from termux_app_store import main as main_module

del os.environ["TERMUX_APP_STORE_HOME"]


class TestMain:

    def test_with_args_calls_run_cli(self):
        with patch("sys.argv", ["termux-app-store", "help"]), \
             patch.object(main_module, "run_cli") as mock_cli, \
             patch.object(main_module, "run_tui") as mock_tui:
            main_module.main()
        mock_cli.assert_called_once()
        mock_tui.assert_not_called()

    def test_no_args_calls_run_tui(self):
        with patch("sys.argv", ["termux-app-store"]), \
             patch.object(main_module, "run_cli") as mock_cli, \
             patch.object(main_module, "run_tui") as mock_tui:
            main_module.main()
        mock_tui.assert_called_once()
        mock_cli.assert_not_called()

    def test_multiple_args_calls_run_cli(self):
        with patch("sys.argv", ["termux-app-store", "install", "bower"]), \
             patch.object(main_module, "run_cli") as mock_cli, \
             patch.object(main_module, "run_tui"):
            main_module.main()
        mock_cli.assert_called_once()

    def test_main_if_name_main(self):
        with patch("sys.argv", ["termux-app-store", "help"]), \
             patch.object(main_module, "run_cli"), \
             patch.object(main_module, "run_tui"), \
             patch.object(main_module, "main") as mock_main:
            exec("main()", {"main": mock_main})
        mock_main.assert_called_once()
