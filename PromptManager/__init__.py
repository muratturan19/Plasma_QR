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

    def get_8d_step_prompt(
        self,
        step_id: str,
        details: Dict[str, Any],
        previous_results: Dict[str, str] | None = None,
    ) -> tuple[str, str]:
        """Return ``system`` and ``user`` prompts for an 8D step.

        Parameters
        ----------
        step_id:
            The identifier of the current 8D step (e.g. ``"D1"``).
        details:
            Complaint details used to fill the prompt template.
        previous_results:
            Mapping of earlier step ids to their LLM responses. These are
            appended to the user prompt to provide context. Each response is
            truncated to the first 300 characters and an ellipsis is appended
            if truncation occurs.
        """

        template = self.get_template("8D")
        step_template = template.get(step_id, {})

        system_prompt = step_template.get("system", "").format(**details)
        user_prompt = step_template.get("user_template", "").format(**details)

        if previous_results:
            def _shorten(text: str, limit: int = 300) -> str:
                return text[:limit] + ("..." if len(text) > limit else "")

            joined = "\n".join(
                f"{sid}: {_shorten(resp)}" for sid, resp in previous_results.items()
            )
            user_prompt = f"{user_prompt}\n\nPrevious step results:\n{joined}"

        return system_prompt, user_prompt
