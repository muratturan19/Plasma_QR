"""Module providing analysis via Large Language Models."""

from __future__ import annotations

import os
from typing import Any, Dict


class LLMAnalyzer:
    """Analyzes text using a Large Language Model."""

    def __init__(self, model: str = "gpt-3.5-turbo") -> None:
        """Initialize the analyzer with an optional LLM model name."""
        self.model = model

    def _query_llm(self, prompt: str) -> str:
        """Return the LLM response for the given prompt."""
        try:
            import openai  # type: ignore

            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise RuntimeError("OPENAI_API_KEY not set")
            openai.api_key = api_key

            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message["content"].strip()
        except Exception:
            # Fallback for offline or missing API key
            return f"LLM response placeholder for: {prompt[:50]}"

    def analyze(self, details: Dict[str, Any], guideline: Dict[str, Any]) -> Dict[str, Any]:
        """Return analysis results per guideline step using complaint details."""
        complaint_text = details.get("complaint", "")
        customer = details.get("customer", "")
        subject = details.get("subject", "")
        part_code = details.get("part_code", "")

        results: Dict[str, Any] = {}
        fields = guideline.get("fields", [])
        for step in fields:
            step_id = step.get("id", "unknown")
            definition = step.get("definition", "")
            prompt = (
                f"Analyze according to step '{step_id}'.\n"
                f"Step definition: {definition}\n"
                f"Customer: {customer}\n"
                f"Subject: {subject}\n"
                f"Part code: {part_code}\n"
                f"Complaint: {complaint_text}"
            )
            answer = self._query_llm(prompt)
            results[step_id] = {"response": answer}
        return results
