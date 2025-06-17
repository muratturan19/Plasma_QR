"""Utilities for loading prompt templates."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


class PromptManager:
    """Manages LLM prompt templates."""

    def load_prompt(self, path: str) -> Dict[str, Any]:
        """Load a prompt template from ``path``."""
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    def get_template(self, method: str) -> Dict[str, Any]:
        """Return the prompt template for ``method``."""
        base_dir = Path(__file__).resolve().parents[1] / "Prompts"
        prompt_path = base_dir / f"{method}_Prompt.json"
        return self.load_prompt(str(prompt_path))
