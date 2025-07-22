import sqlite3
from pathlib import Path
import unittest

from EightDScanner import EightDScanner
from openpyxl import Workbook


class TestEightDScanner(unittest.TestCase):
    def setUp(self) -> None:
        self.dir = Path("tests/temp_reports")
        self.dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.dir / "data.db"

    def tearDown(self) -> None:
        for item in self.dir.glob("*"):
            item.unlink()
        self.dir.rmdir()

    def _create_excel(self, path: Path) -> None:
        wb = Workbook()
        ws = wb.active
        ws.append([
            "Malzeme Kodu",
            "Tanım",
            "Müşteri",
            "Kök Neden",
            "Kalıcı Aksiyon",
        ])
        ws.append(["123", "desc", "cust", "root", "action"])
        wb.save(path)

    def test_scan_inserts_rows(self) -> None:
        file_path = self.dir / "test.xlsx"
        self._create_excel(file_path)
        scanner = EightDScanner(self.dir, self.db_path)
        count = scanner.scan()
        self.assertEqual(count, 1)
        with sqlite3.connect(self.db_path) as conn:
            rows = list(conn.execute("SELECT material_code, description, customer, root_cause, permanent_action FROM reports"))
        self.assertEqual(rows, [("123", "desc", "cust", "root", "action")])


if __name__ == "__main__":
    unittest.main()
