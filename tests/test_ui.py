import importlib
import sys
import types
import unittest
from unittest.mock import MagicMock, patch


class UILazyImportTest(unittest.TestCase):
    """Tests for lazy CLI import and UI.start."""

    def setUp(self) -> None:
        # Ensure a clean import state
        sys.modules.pop('UI', None)
        sys.modules.pop('UI.cli', None)
        self.UI = importlib.import_module('UI')

    def test_cli_not_imported_on_package_import(self) -> None:
        self.assertNotIn('UI.cli', sys.modules)

    def test_run_cli_imports_cli(self) -> None:
        dummy_cli = types.ModuleType('UI.cli')
        dummy_cli.main = MagicMock()
        with patch.dict(sys.modules, {'UI.cli': dummy_cli}):
            self.UI.run_cli()
            dummy_cli.main.assert_called_once()

    def test_start_invokes_run_cli(self) -> None:
        with patch.object(self.UI, 'run_cli') as mock_run:
            ui = self.UI.UI()
            ui.start()
            mock_run.assert_called_once()


class RunStreamlitTest(unittest.TestCase):
    """Tests for ``run_streamlit``."""

    def test_run_streamlit_invokes_bootstrap(self) -> None:
        module = importlib.import_module("UI")

        dummy_bootstrap = types.ModuleType("streamlit.web.bootstrap")
        dummy_bootstrap.run = MagicMock()
        dummy_web = types.ModuleType("streamlit.web")
        dummy_web.bootstrap = dummy_bootstrap
        dummy_streamlit = types.ModuleType("streamlit")
        dummy_streamlit.web = dummy_web

        with patch.dict(sys.modules, {
            "streamlit": dummy_streamlit,
            "streamlit.web": dummy_web,
            "streamlit.web.bootstrap": dummy_bootstrap,
        }), patch.object(module, "streamlit_app") as mock_app:
            mock_app.__file__ = "app_file"
            module.run_streamlit()
            dummy_bootstrap.run.assert_called_once_with(
                "app_file", False, [], []
            )


if __name__ == '__main__':
    unittest.main()
