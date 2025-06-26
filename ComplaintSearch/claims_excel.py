"""Excel-based query utilities for customer claims."""

from __future__ import annotations

from typing import Any, Dict, List
from pathlib import Path
from datetime import datetime

from difflib import SequenceMatcher
from openpyxl import load_workbook

from . import normalize_text


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
                cell_raw = str(record.get(key, ""))
                cell = normalize_text(cell_raw)
                val_norm = normalize_text(str(val))
                if key == "complaint":
                    if val_norm in cell:
                        continue
                    ratio = SequenceMatcher(None, val_norm, cell).ratio()
                    if ratio < 0.8:
                        match = False
                        break
                else:
                    ratio = SequenceMatcher(None, val_norm, cell).ratio()
                    if cell != val_norm and ratio < 0.8:
                        match = False
                        break
            if match:
                results.append(record)

        wb.close()
        return results

    def unique_values(self, field: str) -> List[str]:
        """Return sorted unique values for ``field``.

        Parameters
        ----------
        field:
            Column name to extract unique values from. Turkish headers are
            automatically mapped to their English counterparts.

        Returns
        -------
        List[str]
            Unique cell values as strings. Empty cells are ignored.
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

        if field not in headers:
            wb.close()
            return []

        index = headers.index(field)
        values = set()
        for row in rows:
            if index >= len(row):
                continue
            val = row[index]
            if val is None:
                continue
            text = str(val).strip()
            if text:
                values.add(text)

        wb.close()
        return sorted(values)


__all__ = ["ExcelClaimsSearcher"]
