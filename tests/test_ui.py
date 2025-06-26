import importlib
import sys
import types
import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path


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
    """Tests for ``run_streamlit`` under different environments."""

    def test_run_streamlit_invokes_subprocess_when_not_frozen(self) -> None:
        module = importlib.import_module("UI")

        with patch.object(module.sys, "frozen", False, create=True), \
                patch("subprocess.run") as mock_run, \
                patch("UI.streamlit_app", create=True) as mock_app, \
                patch.object(Path, "exists", return_value=True):
            mock_app.__file__ = "app_file"
            module.run_streamlit()
            expected = ["streamlit", "run", str(Path("app_file").resolve())]
            mock_run.assert_called_once_with(expected, check=True)

    def test_run_streamlit_invokes_cli_when_frozen(self) -> None:
        module = importlib.import_module("UI")

        dummy_cli = types.ModuleType("streamlit.web.cli")
        dummy_cli.main = MagicMock()
        dummy_web = types.ModuleType("streamlit.web")
        dummy_web.cli = dummy_cli
        dummy_streamlit = types.ModuleType("streamlit")
        dummy_streamlit.web = dummy_web

        with patch.object(module.sys, "frozen", True, create=True), \
                patch.dict(sys.modules, {
                    "streamlit": dummy_streamlit,
                    "streamlit.web": dummy_web,
                    "streamlit.web.cli": dummy_cli,
                }), \
                patch("UI.streamlit_app", create=True) as mock_app, \
                patch("subprocess.run") as mock_run, \
                patch.object(Path, "exists", return_value=True):
            mock_app.__file__ = "app_file"
            module.run_streamlit()
            dummy_cli.main.assert_called_once()
            mock_run.assert_not_called()

    def test_run_streamlit_writes_temp_when_missing(self) -> None:
        module = importlib.import_module("UI")

        resource_path = Path(__file__).resolve().parents[1] / "UI" / "streamlit_app.py"

        dummy_files = MagicMock()
        dummy_files.joinpath.return_value = resource_path

        with patch.object(module.sys, "frozen", False, create=True), \
                patch("subprocess.run") as mock_run, \
                patch("UI.streamlit_app", create=True) as mock_app, \
                patch.object(Path, "exists", return_value=False), \
                patch("importlib.resources.files", return_value=dummy_files), \
                patch("tempfile.gettempdir", return_value="/tmp"):
            mock_app.__file__ = "missing.py"
            module.run_streamlit()
            expected = ["streamlit", "run", "/tmp/streamlit_app.py"]
            mock_run.assert_called_once_with(expected, check=True)


if __name__ == '__main__':
    unittest.main()
