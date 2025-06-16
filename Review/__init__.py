"""Utilities for reviewing generated reports using a second LLM."""

from __future__ import annotations

import os
from typing import Iterable, List


class ReviewLLMError(RuntimeError):
    """Raised when the review LLM cannot be used."""


class Review:
    """Reviews generated reports or analysis results."""

    def __init__(self, model: str | None = None) -> None:
        """Initialize with an optional LLM model name."""
        if model is None:
            model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        self.model = model

    def _query_llm(self, prompt: str) -> str:
        """Return the LLM response for the given prompt."""
        try:
            import openai  # type: ignore
        except ImportError as exc:  # pragma: no cover - optional dependency
            raise ReviewLLMError("openai package is not installed") from exc

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ReviewLLMError("OPENAI_API_KEY not set")
        openai.api_key = api_key

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message["content"].strip()
        except Exception as exc:  # pragma: no cover - network issues
            if "invalid" in str(exc).lower():
                raise ReviewLLMError("Invalid OpenAI API key") from exc
            return f"LLM review placeholder for: {prompt[:50]}"

    def perform(self, data: Iterable[str]) -> List[str]:
        """Review the given data and return feedback for each item."""
        results: List[str] = []
        for text in data:
            prompt = f"REVIEW PROMPT PLACEHOLDER\n{text}"
            results.append(self._query_llm(prompt))
        return results
