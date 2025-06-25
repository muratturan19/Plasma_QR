"""Utilities for storing and searching customer complaints."""

from __future__ import annotations

from pathlib import Path
import json
import re
import unicodedata
from difflib import SequenceMatcher
from typing import Dict, List


def normalize_text(text: str) -> str:
    """Return lowercase ASCII text without punctuation or extra spaces."""
    text_norm = unicodedata.normalize("NFKD", text)
    ascii_text = text_norm.encode("ascii", "ignore").decode("ascii")
    lowered = ascii_text.lower()
    no_punct = re.sub(r"[^\w\s]", "", lowered)
    collapsed = re.sub(r"\s+", " ", no_punct)
    return collapsed.strip()


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
        """Return complaint records fuzzy-matching ``keyword``."""
        if not self.path.exists():
            return []

        with open(self.path, "r", encoding="utf-8") as f:
            try:
                items: List[Dict[str, str]] = json.load(f)
            except json.JSONDecodeError:
                return []

        keyword_norm = normalize_text(keyword)
        results = []

        for item in items:
            for field in ["complaint", "customer", "subject", "part_code"]:
                value = str(item.get(field, ""))
                value_norm = normalize_text(value)
                if keyword_norm in value_norm:
                    results.append(item)
                    break
                ratio = SequenceMatcher(None, keyword_norm, value_norm).ratio()
                if ratio >= 0.8:
                    results.append(item)
                    break
        return results


from .claims_excel import ExcelClaimsSearcher

__all__ = ["ComplaintStore", "ExcelClaimsSearcher"]
