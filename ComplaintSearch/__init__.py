"""Utilities for storing and searching customer complaints."""

from __future__ import annotations

from pathlib import Path
import json
from typing import Dict, List


class ComplaintStore:
    """Persist and query complaint records."""

    def __init__(self, path: str | Path = "complaints.json") -> None:
        self.path = Path(path)
        if not self.path.exists():
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump([], f)

    def add_complaint(self, info: Dict[str, str]) -> None:
        """Append a complaint record to the store."""
        if not self.path.exists():
            data: List[Dict[str, str]] = []
        else:
            with open(self.path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
        data.append(info)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def search(self, keyword: str) -> List[Dict[str, str]]:
        """Return complaint records containing ``keyword``."""
        if not self.path.exists():
            return []
        with open(self.path, "r", encoding="utf-8") as f:
            try:
                items: List[Dict[str, str]] = json.load(f)
            except json.JSONDecodeError:
                return []
        keyword = keyword.lower()
        results = []
        for item in items:
            if any(
                keyword in str(item.get(field, "")).lower()
                for field in ["complaint", "customer", "subject", "part_code"]
            ):
                results.append(item)
        return results


__all__ = ["ComplaintStore"]
