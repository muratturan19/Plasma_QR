"""Module providing analysis via Large Language Models."""

from __future__ import annotations

import os
from typing import Any, Dict


class OpenAIError(RuntimeError):
    """Raised when the OpenAI client cannot be used."""


class LLMAnalyzer:
    """Analyzes text using a Large Language Model."""

    def __init__(self, model: str | None = None) -> None:
        """Initialize the analyzer with an optional LLM model name.

        If ``model`` is ``None``, ``OPENAI_MODEL`` environment variable is used.
        When the variable is not set, ``"gpt-3.5-turbo"`` becomes the default.
        """
        if model is None:
            model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        self.model = model

    def _query_llm(self, prompt: str) -> str:
        """Return the LLM response for the given prompt."""
        print("LLMAnalyzer._query_llm start")
        try:
            from openai import OpenAI  # type: ignore
        except ImportError as exc:  # pragma: no cover - import errors not expected
            raise OpenAIError("openai package is not installed") from exc

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise OpenAIError("OPENAI_API_KEY not set")
        client = OpenAI(api_key=api_key)

        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
            )
            tokens = getattr(getattr(response, "usage", None), "total_tokens", None)
            if tokens is not None:
                print(f"LLMAnalyzer tokens used: {tokens}")
            result = response.choices[0].message.content.strip()
            print("LLMAnalyzer._query_llm end")
            return result
        except Exception as exc:  # pragma: no cover - network issues
            if "invalid" in str(exc).lower() or "incorrect" in str(exc).lower():
                raise OpenAIError("Invalid OpenAI API key") from exc
            print(f"LLMAnalyzer error: {exc}")
            print("LLMAnalyzer._query_llm end")
            return f"LLM response placeholder for: {prompt[:50]}"

    def analyze(self, details: Dict[str, Any], guideline: Dict[str, Any]) -> Dict[str, Any]:
        """Return analysis results per guideline step using complaint details."""
        complaint_text = details.get("complaint", "")
        customer = details.get("customer", "")
        subject = details.get("subject", "")
        part_code = details.get("part_code", "")

        results: Dict[str, Any] = {}
        fields = guideline.get("fields") or guideline.get("steps", [])
        for step in fields:
            step_id = step.get("id") or step.get("step", "unknown")
            definition = step.get("definition") or step.get("detail", "")
            prompt = (
                f"You are preparing content for step '{step_id}' only.\n"
                f"Ignore other steps and analyze solely this one.\n"
                f"Step definition: {definition}\n"
                f"Customer: {customer}\n"
                f"Subject: {subject}\n"
                f"Part code: {part_code}\n"
                f"Complaint: {complaint_text}"
            )
            answer = self._query_llm(prompt)
            results[step_id] = {"response": answer}
        return results
