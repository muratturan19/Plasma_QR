"""Guide management module."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any


class GuideManager:
    """Manages guide steps and resources for quality-report methods."""

    def __init__(self) -> None:
        """Initialize the guide cache."""
        self._cache: Dict[str, Dict[str, Any]] = {}

    def load_guide(self, path: str) -> Dict[str, Any]:
        """Load guide information from the given path."""
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    def get_format(self, method: str) -> Dict[str, Any]:
        """Return the guide dictionary for the given method."""
        if method not in self._cache:
            base_dir = Path(__file__).resolve().parents[1] / "Guidelines"
            guide_path = base_dir / f"{method}_Guide.json"
            self._cache[method] = self.load_guide(str(guide_path))
        return self._cache[method]
