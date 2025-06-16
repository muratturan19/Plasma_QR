import importlib
import unittest
from unittest.mock import patch


class RunAppTest(unittest.TestCase):
    """Tests for the ``run_app`` entry point."""

    def test_main_invokes_run_streamlit(self) -> None:
        with patch("dotenv.load_dotenv") as mock_load:
            module = importlib.import_module("run_app")
        mock_load.assert_called_once()
        with patch.object(module, "run_streamlit") as mock_run:
            module.main()
            mock_run.assert_called_once()


if __name__ == "__main__":
    unittest.main()
