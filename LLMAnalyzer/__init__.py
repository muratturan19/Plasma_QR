"""Module providing analysis via Large Language Models."""

from __future__ import annotations

import os
import logging
from typing import Any, Dict

from PromptManager import PromptManager


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
        self.logger = logging.getLogger(__name__)

    def _query_llm(self, system_prompt: str, user_prompt: str) -> str:
        """Return the LLM response for the given prompt pair."""
        self.logger.debug("LLMAnalyzer._query_llm start")
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
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
            tokens = getattr(getattr(response, "usage", None), "total_tokens", None)
            if tokens is not None:
                self.logger.debug("LLMAnalyzer tokens used: %s", tokens)
            result = response.choices[0].message.content.strip()
            self.logger.debug("LLMAnalyzer._query_llm end")
            return result
        except Exception as exc:  # pragma: no cover - network issues
            if "invalid" in str(exc).lower() or "incorrect" in str(exc).lower():
                raise OpenAIError("Invalid OpenAI API key") from exc
            self.logger.error("LLMAnalyzer error: %s", exc)
            self.logger.debug("LLMAnalyzer._query_llm end")
            return f"LLM response placeholder for: {user_prompt[:50]}"

    def analyze(self, details: Dict[str, Any], guideline: Dict[str, Any]) -> Dict[str, Any]:
        """Return analysis results per guideline step using complaint details."""
        complaint_text = details.get("complaint", "")
        customer = details.get("customer", "")
        subject = details.get("subject", "")
        part_code = details.get("part_code", "")

        method_field = guideline.get("method", "")
        method = method_field.split()[0] if method_field else ""
        prompt_manager = PromptManager()
        template = {"system": "", "steps": {}}
        if method:
            template = prompt_manager.get_template(method)
        system_tmpl = template.get("system", "")
        step_templates = template.get("steps", {})
        template_has_steps = bool(step_templates)

        results: Dict[str, Any] = {}
        accumulated: Dict[str, str] = {}
        fields = guideline.get("fields") or guideline.get("steps", [])
        for step in fields:
            step_id = step.get("id") or step.get("step", "unknown")
            definition = step.get("definition") or step.get("detail", "")

            values = {
                "step_id": step_id,
                "customer": customer,
                "subject": subject,
                "part_code": part_code,
                "complaint_text": complaint_text,
                "definition": definition,
                "complaint": complaint_text,
                "description": details.get("description", complaint_text),
            }

            if template_has_steps:
                system_prompt = system_tmpl.format(**values)
                step_tmpl = step_templates.get(step_id, {}).get("prompt", "")
                user_prompt = f"Step definition: {definition}"
                if step_tmpl:
                    user_prompt += f"\n{step_tmpl.format(**values)}"
            else:
                if method == "8D":
                    system_prompt, user_prompt = prompt_manager.get_8d_step_prompt(
                        step_id, values, accumulated
                    )
                else:
                    step_entry = template.get(step_id, {})
                    system_prompt = step_entry.get("system", "").format(**values)
                    user_prompt = step_entry.get("user_template", "").format(**values)

            answer = self._query_llm(system_prompt, user_prompt)
            results[step_id] = {"response": answer}
            accumulated[step_id] = answer

        return results
