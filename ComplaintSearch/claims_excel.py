"""Excel-based query utilities for customer claims."""

from __future__ import annotations

from typing import Any, Dict, List
from pathlib import Path
from datetime import datetime

from openpyxl import load_workbook


class ExcelClaimsSearcher:
    """Search complaint records stored in an Excel file."""

    def __init__(self, path: str | Path = "CC/claims.xlsx") -> None:
        self.path = Path(path)

    def search(self, filters: Dict[str, str], year: int | None = None) -> List[Dict[str, Any]]:
        """Return rows matching ``filters`` and optional ``year`` filter.

        Parameters
        ----------
        filters:
            Mapping of field names to filter values. Keys are compared
            case-insensitively. The ``complaint`` filter performs a substring
            search while other fields must match exactly.
        year:
            Optional year constraint applied to a ``date`` column when present.

        Returns
        -------
        List[Dict[str, Any]]
            Matching rows as dictionaries with lowercase keys.
        """
        if not self.path.exists():
            return []

        wb = load_workbook(self.path, read_only=True)
        ws = wb.active
        rows = ws.iter_rows(values_only=True)
        try:
            headers = [str(c).strip().lower() if c is not None else "" for c in next(rows)]
            mapping = {
                "müşteri şikayeti": "complaint",
                "müşteri": "customer",
                "konu": "subject",
                "parça kodu": "part_code",
                "tarih": "date",
            }
            headers = [mapping.get(h, h) for h in headers]
        except StopIteration:
            wb.close()
            return []
        indices = {h: i for i, h in enumerate(headers)}
        results: List[Dict[str, Any]] = []

        for row in rows:
            record = {h: row[i] if i < len(row) else None for h, i in indices.items()}
            if year is not None and "date" in indices:
                value = record.get("date")
                if isinstance(value, str):
                    try:
                        value = datetime.fromisoformat(value)
                    except ValueError:
                        continue
                if getattr(value, "year", None) != year:
                    continue
            match = True
            for key, val in filters.items():
                if not val:
                    continue
                key = key.lower()
                cell = str(record.get(key, "")).lower()
                val_str = str(val).lower()
                if key == "complaint":
                    if val_str not in cell:
                        match = False
                        break
                else:
                    if cell != val_str:
                        match = False
                        break
            if match:
                results.append(record)

        wb.close()
        return results


__all__ = ["ExcelClaimsSearcher"]
