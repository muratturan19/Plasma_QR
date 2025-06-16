import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch
import tempfile
from pathlib import Path

from UI import cli
import json


class CLITest(unittest.TestCase):
    """Tests for the command-line interface."""

    @patch("UI.cli.ReportGenerator")
    @patch("UI.cli.Review")
    @patch("UI.cli.LLMAnalyzer")
    @patch("UI.cli.GuideManager")
    def test_main_pipeline(self, mock_manager, mock_analyzer, mock_review, mock_report):
        mock_manager.return_value.get_format.return_value = {"fields": []}
        mock_analyzer.return_value.analyze.return_value = {
            "Step1": {"response": "ok"}
        }
        mock_review.return_value.perform.return_value = ["checked"]
        mock_report.return_value.generate.return_value = {
            "pdf": "file.pdf",
            "excel": "file.xlsx",
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            with io.StringIO() as buf, redirect_stdout(buf):
                cli.main([
                    "--complaint",
                    "c",
                    "--method",
                    "8D",
                    "--output",
                    tmpdir,
                    "--customer",
                    "cust",
                    "--subject",
                    "subject",
                    "--part-code",
                    "code",
                ])
                output = buf.getvalue()
            llm1 = Path(tmpdir) / "LLM1.txt"
            llm2 = Path(tmpdir) / "LLM2.txt"
            self.assertTrue(llm1.exists())
            self.assertTrue(llm2.exists())

        self.assertIn("Step1", output)
        self.assertIn("file.pdf", output)
        mock_manager.return_value.get_format.assert_called_with("8D")
        mock_analyzer.return_value.analyze.assert_called_once()
        mock_review.return_value.perform.assert_called_with(
            ["ok"],
            method="8D",
            customer="cust",
            subject="subject",
            part_code="code",
            guideline_json=json.dumps({"fields": []}, ensure_ascii=False),
        )
        mock_report.return_value.generate.assert_called_with(
            {
                "Step1": {"response": "checked"},
            },
            {
                "customer": "cust",
                "subject": "subject",
                "part_code": "code",
            },
            tmpdir,
        )


if __name__ == "__main__":
    unittest.main()
