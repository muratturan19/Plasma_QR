import logging
import os
import unittest
from unittest.mock import patch

from api.logging_config import configure_logging


class LoggingConfigTest(unittest.TestCase):
    """Tests for the logging configuration helper."""

    def setUp(self) -> None:
        self.root = logging.getLogger()
        self.orig_handlers = self.root.handlers[:]
        for handler in self.root.handlers:
            self.root.removeHandler(handler)

    def tearDown(self) -> None:
        for handler in self.root.handlers:
            self.root.removeHandler(handler)
        for handler in self.orig_handlers:
            self.root.addHandler(handler)

    def test_basic_config_called_no_handlers(self) -> None:
        with patch("logging.basicConfig") as mock_basic:
            configure_logging()
            mock_basic.assert_called_once_with(level=logging.INFO)

    def test_level_from_env(self) -> None:
        with patch("logging.basicConfig") as mock_basic, \
             patch.dict(os.environ, {"LOG_LEVEL": "DEBUG"}):
            configure_logging()
            mock_basic.assert_called_once_with(level=logging.DEBUG)

    def test_no_config_when_handlers_exist(self) -> None:
        handler = logging.NullHandler()
        self.root.addHandler(handler)
        try:
            with patch("logging.basicConfig") as mock_basic:
                configure_logging()
                mock_basic.assert_not_called()
        finally:
            self.root.removeHandler(handler)


if __name__ == "__main__":
    unittest.main()
