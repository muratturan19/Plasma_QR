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
        info = {"customer": "cust", "subject": "sub", "part_code": "code"}
        with tempfile.TemporaryDirectory() as tmpdir:
            paths = self.generator.generate(analysis, info, tmpdir)
            pdf_path = Path(paths["pdf"])
            excel_path = Path(paths["excel"])
            self.assertTrue(pdf_path.exists())
            self.assertTrue(excel_path.exists())

    def test_generate_unique_paths(self) -> None:
        """Consecutive calls should produce different file names."""
        analysis = {"Step1": {"response": "foo"}}
        info = {"customer": "c"}
        with tempfile.TemporaryDirectory() as tmpdir:
            first = self.generator.generate(analysis, info, tmpdir)
            second = self.generator.generate(analysis, info, tmpdir)
            self.assertNotEqual(first["pdf"], second["pdf"])
            self.assertNotEqual(first["excel"], second["excel"])

    def test_generate_handles_unicode(self) -> None:
        """PDF creation should not fail with non-Latin characters."""
        analysis = {"Adım1": {"response": "İşlem tamam"}}
        info = {"customer": "Müşteri", "subject": "Konu", "part_code": "K001"}
        with tempfile.TemporaryDirectory() as tmpdir:
            paths = self.generator.generate(analysis, info, tmpdir)
            self.assertTrue(Path(paths["pdf"]).exists())
            self.assertTrue(Path(paths["excel"]).exists())

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
