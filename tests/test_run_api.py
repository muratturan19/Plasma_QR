import importlib
import unittest
from unittest.mock import patch


class RunAPITest(unittest.TestCase):
    """Tests for the ``run_api`` entry point."""

    def test_main_invokes_uvicorn(self) -> None:
        module = importlib.import_module("run_api")
        with patch.object(module, "load_dotenv") as mock_load, \
             patch.object(module, "uvicorn") as mock_uvicorn:
            module.main()
            mock_load.assert_called_once()
            mock_uvicorn.run.assert_called_once_with(module.app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    unittest.main()
