import sys
import types
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent))

_mock_run_tui = MagicMock()
_mock_run_cli = MagicMock()

_fake_tui_mod = types.ModuleType("termux_app_store")
_fake_tui_mod.run_tui = _mock_run_tui
sys.modules["termux_app_store"] = _fake_tui_mod

_fake_cli_mod = types.ModuleType("termux_app_store_cli")
_fake_cli_mod.run_cli = _mock_run_cli
sys.modules["termux_app_store_cli"] = _fake_cli_mod

sys.modules.pop("termux_app_store.main", None)
import termux_app_store.main as main_module

main_module.run_tui = _mock_run_tui
main_module.run_cli = _mock_run_cli


class TestMain:

    def setup_method(self):
        _mock_run_tui.reset_mock()
        _mock_run_cli.reset_mock()

    def test_with_args_calls_run_cli(self):
        with patch("sys.argv", ["termux-app-store", "help"]):
            main_module.main()
        _mock_run_cli.assert_called_once()
        _mock_run_tui.assert_not_called()

    def test_no_args_calls_run_tui(self):
        with patch("sys.argv", ["termux-app-store"]):
            main_module.main()
        _mock_run_tui.assert_called_once()
        _mock_run_cli.assert_not_called()

    def test_multiple_args_calls_run_cli(self):
        with patch("sys.argv", ["termux-app-store", "install", "bower"]):
            main_module.main()
        _mock_run_cli.assert_called_once()

    def test_main_if_name_main(self):
        with patch("sys.argv", ["termux-app-store", "help"]):
            with patch.object(main_module, "main") as mock_main:
                exec("main()", {"main": mock_main})
            mock_main.assert_called_once()
