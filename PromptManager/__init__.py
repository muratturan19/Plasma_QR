"""Utilities for loading prompt templates."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


class PromptManager:
    """Manages LLM prompt templates."""

    def __init__(self) -> None:
        """Initialize the template caches."""
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._text_cache: Dict[str, str] = {}

    def load_prompt(self, path: str) -> Dict[str, Any]:
        """Load a prompt template from ``path``."""
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    def load_text_prompt(self, path: str) -> str:
        """Return the text content of a prompt file."""
        with open(path, "r", encoding="utf-8") as file:
            return file.read()

    def get_template(self, method: str) -> Dict[str, Any]:
        """Return the prompt template for ``method`` with caching."""
        if method not in self._cache:
            base_dir = Path(__file__).resolve().parents[1] / "Prompts"
            prompt_path = base_dir / f"{method}_Prompt.json"
            self._cache[method] = self.load_prompt(str(prompt_path))
        return self._cache[method]

    def get_text_prompt(self, method: str) -> str:
        """Return the text prompt for ``method`` with caching."""
        if method not in self._text_cache:
            base_dir = Path(__file__).resolve().parents[1] / "Prompts"
            prompt_path = base_dir / f"{method}_Prompt.txt"
            if prompt_path.exists():
                self._text_cache[method] = self.load_text_prompt(str(prompt_path))
            else:
                self._text_cache[method] = ""
        return self._text_cache[method]


__all__ = ["PromptManager"]
