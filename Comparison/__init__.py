"""Comparison utilities."""

from __future__ import annotations

from typing import Any, Dict, List
import difflib
import json


class Comparison:
    """Compares different versions of reports or data sets."""

    def _to_lines(self, data: Any) -> List[str]:
        """Return ``data`` as a list of strings for diffing."""
        if isinstance(data, str):
            return data.splitlines()
        if isinstance(data, dict):
            text = json.dumps(data, sort_keys=True, indent=2)
            return text.splitlines()
        return str(data).splitlines()

    def compare(self, old: Any, new: Any) -> Dict[str, List[str]]:
        """Return added and removed lines between ``old`` and ``new``."""
        old_lines = self._to_lines(old)
        new_lines = self._to_lines(new)
        diff = difflib.unified_diff(old_lines, new_lines, lineterm="")

        added: List[str] = []
        removed: List[str] = []
        for line in diff:
            if line.startswith("+") and not line.startswith("+++"):
                added.append(line[1:])
            elif line.startswith("-") and not line.startswith("---"):
                removed.append(line[1:])

        return {"added": added, "removed": removed}


__all__ = ["Comparison"]
