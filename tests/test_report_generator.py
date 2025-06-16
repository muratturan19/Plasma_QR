import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch

from GuideManager import GuideManager
from ReportGenerator import ReportGenerator


class ReportGeneratorTest(unittest.TestCase):
    """Tests for ReportGenerator.generate."""

    def setUp(self) -> None:
        self.manager = GuideManager()
        self.generator = ReportGenerator(self.manager)

    def test_generate_creates_files(self) -> None:
        analysis = {"Step1": {"response": "foo"}, "Step2": {"response": "bar"}}
        details = {"complaint": "c", "customer": "cust", "subject": "sub", "part_code": "code"}
        with tempfile.TemporaryDirectory() as tmpdir:
            paths = self.generator.generate(analysis, details, tmpdir)
            pdf_path = Path(paths["pdf"])
            excel_path = Path(paths["excel"])
            self.assertTrue(pdf_path.exists())
            self.assertTrue(excel_path.exists())

    def test_generate_template_uses_manager(self) -> None:
        """``generate_template`` should fetch the correct format via ``GuideManager``."""
        expected = {"fields": []}
        method = "8D"
        with patch.object(GuideManager, "get_format", return_value=expected) as mock_get:
            generator = ReportGenerator(self.manager)
            result = generator.generate_template(method)
            mock_get.assert_called_with(method)
            self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
