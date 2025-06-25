import os
import tempfile
import unittest
from datetime import datetime

from ComplaintSearch.claims_excel import ExcelClaimsSearcher
from openpyxl import Workbook


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
