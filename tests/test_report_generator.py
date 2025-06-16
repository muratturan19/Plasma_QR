import tempfile
from pathlib import Path
import unittest

from GuideManager import GuideManager
from ReportGenerator import ReportGenerator


class ReportGeneratorTest(unittest.TestCase):
    """Tests for ReportGenerator.generate."""

    def setUp(self) -> None:
        self.manager = GuideManager()
        self.generator = ReportGenerator(self.manager)

    def test_generate_creates_files(self) -> None:
        analysis = {"Step1": {"response": "foo"}, "Step2": {"response": "bar"}}
        with tempfile.TemporaryDirectory() as tmpdir:
            paths = self.generator.generate(analysis, tmpdir)
            pdf_path = Path(paths["pdf"])
            excel_path = Path(paths["excel"])
            self.assertTrue(pdf_path.exists())
            self.assertTrue(excel_path.exists())


if __name__ == "__main__":
    unittest.main()
