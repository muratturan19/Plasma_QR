import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from UI import cli


class CLITest(unittest.TestCase):
    """Tests for the command-line interface."""

    @patch("UI.cli.ReportGenerator")
    @patch("UI.cli.LLMAnalyzer")
    @patch("UI.cli.GuideManager")
    def test_main_pipeline(self, mock_manager, mock_analyzer, mock_report):
        mock_manager.return_value.get_format.return_value = {"fields": []}
        mock_analyzer.return_value.analyze.return_value = {
            "Step1": {"response": "ok"}
        }
        mock_report.return_value.generate.return_value = {
            "pdf": "file.pdf",
            "excel": "file.xlsx",
        }

        with io.StringIO() as buf, redirect_stdout(buf):
            cli.main(["--complaint", "c", "--method", "8D", "--output", "out"])
            output = buf.getvalue()

        self.assertIn("Step1", output)
        self.assertIn("file.pdf", output)
        mock_manager.return_value.get_format.assert_called_with("8D")
        mock_analyzer.return_value.analyze.assert_called_once()
        mock_report.return_value.generate.assert_called_once()


if __name__ == "__main__":
    unittest.main()
