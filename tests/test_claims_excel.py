import os
import tempfile
import unittest
from datetime import datetime

from ComplaintSearch.claims_excel import ExcelClaimsSearcher
from openpyxl import Workbook, load_workbook


class ExcelClaimsSearchTest(unittest.TestCase):
    """Tests for ExcelClaimsSearcher.search."""

    def _create_file(self, path: str, headers=None) -> None:
        wb = Workbook()
        ws = wb.active
        if headers is None:
            headers = ["complaint", "customer", "subject", "part_code", "date"]
        ws.append(headers)
        ws.append(["noise", "ACME", "engine", "X1", datetime(2023, 1, 1)])
        ws.append(["crack", "BETA", "body", "X2", datetime(2022, 5, 1)])
        wb.save(path)

    def test_search_filters(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "claims.xlsx")
            self._create_file(file_path)
            searcher = ExcelClaimsSearcher(file_path)
            result = searcher.search({"customer": "ACME"}, year=2023)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["customer"], "ACME")
            empty = searcher.search({"customer": "ACME"}, year=2022)
            self.assertEqual(empty, [])

    def test_normalization_and_fuzzy(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "claims.xlsx")
            self._create_file(file_path)

            wb = load_workbook(file_path)
            ws = wb.active
            ws.append(["\u015fikayet var", "GAMMA", "door", "X3", datetime(2023, 2, 1)])
            wb.save(file_path)

            searcher = ExcelClaimsSearcher(file_path)

            accent = searcher.search({"complaint": "sikayet"})
            self.assertEqual(len(accent), 1)
            self.assertEqual(accent[0]["customer"], "GAMMA")

            typo = searcher.search({"complaint": "noize"})
            self.assertEqual(len(typo), 1)
            self.assertEqual(typo[0]["customer"], "ACME")

    def test_turkish_headers(self) -> None:
        """Ensure search works when headers are Turkish."""
        headers = [
            "müşteri şikayeti",
            "müşteri",
            "konu",
            "parça kodu",
            "tarih",
        ]
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "claims.xlsx")
            self._create_file(file_path, headers=headers)
            searcher = ExcelClaimsSearcher(file_path)
            result = searcher.search({"customer": "ACME"}, year=2023)
            self.assertEqual(len(result), 1)
            self.assertIn("customer", result[0])
            self.assertEqual(result[0]["customer"], "ACME")


if __name__ == "__main__":
    unittest.main()
