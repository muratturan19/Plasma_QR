"""Module providing analysis via Large Language Models."""

from __future__ import annotations

import os
import logging
from typing import Any, Dict

from PromptManager import PromptManager

# Default prompt used for 8D analyses when no template is loaded.
DEFAULT_8D_PROMPT = """
Sen deneyimli bir kalite mühendisisin. Aşağıdaki müşteri şikayetine göre 8D Problem
Çözme metodolojisine uygun detaylı bir rapor hazırla.

Müşteri Şikayeti: {musteri_sikayeti}
Parça Kodu: {parca_kodu}
Problem Açıklaması: {problem_aciklamasi}

Rapor formatı şu şekilde olmalıdır:

D1: Ekip Oluşturma
[...]

D2: Problemin Tanımı
[...]

D3: Geçici Önlemler
[...]

D4: Kök Neden Analizi
[...]

D5: Kalıcı Çözüm Geliştirme
[...]

D6: Kalıcı Çözümün Uygulanması
[...]

D7: Önleyici Faaliyetler
[...]

D8: Takdir ve Kapanış
[...]

❗️Yalnızca yukarıdaki başlıklara uygun teknik içerik üret. Giriş paragrafı, genel yorum
ya da metodoloji açıklaması yapma. Her başlığı kendi içeriğiyle doldur, ekstra bilgi verme.
"""


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
        truncated_sys = system_prompt.replace("\n", " ")[:200]
        truncated_user = user_prompt.replace("\n", " ")[:200]
        self.logger.debug("system_prompt: %s", truncated_sys)
        self.logger.debug("user_prompt: %s", truncated_user)
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
                self.logger.info("LLMAnalyzer tokens used: %s", tokens)
            result = response.choices[0].message.content.strip()
            self.logger.debug("LLMAnalyzer returned: %s", result.replace("\n", " ")[:200])
            self.logger.debug("LLMAnalyzer._query_llm end")
            return result
        except Exception as exc:  # pragma: no cover - network issues
            if "invalid" in str(exc).lower() or "incorrect" in str(exc).lower():
                raise OpenAIError("Invalid OpenAI API key") from exc
            self.logger.error("LLMAnalyzer error: %s", exc)
            self.logger.debug("LLMAnalyzer._query_llm end")
            return f"LLM response placeholder for: {user_prompt[:50]}"

    def analyze(
        self,
        details: Dict[str, Any],
        guideline: Dict[str, Any],
        directives: str = "",
    ) -> Dict[str, Any]:
        """Return analysis using complaint details and optional directives."""
        complaint_text = details.get("complaint", "")
        customer = details.get("customer", "")
        subject = details.get("subject", "")
        part_code = details.get("part_code", "")

        method_field = guideline.get("method", "")
        method = method_field.split()[0] if method_field else ""

        # ``8D`` method now uses a single LLM call with a dedicated prompt.
        if method == "8D":
            user_prompt = (
                f"Müşteri Şikayeti: {complaint_text}\n"
                f"Parça Kodu: {part_code}\n"
                f"Problem Açıklaması: {subject or complaint_text}"
            )
            if directives:
                user_prompt += (
                    "\n---\nKullanıcıdan gelen özel talimatlar:\n"
                    f"{directives}\n\n"
                    "Lütfen yukarıdaki taleplere ve kısıtlamalara mutlaka uy."
                )
            answer = self._query_llm(DEFAULT_8D_PROMPT, user_prompt)
            return {"full_text": answer}

        prompt_manager = PromptManager()
        text_template = prompt_manager.get_text_prompt(method)
        if text_template:
            user_prompt = (
                text_template.replace("{{musteri_sikayeti}}", complaint_text)
                .replace("{{parca_kodu}}", part_code)
                .replace("{{problem_aciklamasi}}", subject or complaint_text)
            )
            if directives:
                user_prompt += (
                    "\n---\nKullanıcıdan gelen özel talimatlar:\n"
                    f"{directives}\n\n"
                    "Lütfen yukarıdaki taleplere ve kısıtlamalara mutlaka uy."
                )
            answer = self._query_llm("", user_prompt)
            return {"full_text": answer}

        template = {"system": "", "steps": {}}
        if method:
            template = prompt_manager.get_template(method)
        system_tmpl = template.get("system", "")
        step_templates = template.get("steps", {})
        template_has_steps = bool(step_templates)

        results: Dict[str, Any] = {}
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
                step_entry = template.get(step_id, {})
                system_prompt = step_entry.get("system", "").format(**values)
                user_prompt = step_entry.get("user_template", "").format(**values)
            if directives:
                user_prompt += (
                    "\n---\nKullanıcıdan gelen özel talimatlar:\n"
                    f"{directives}\n\n"
                    "Lütfen yukarıdaki taleplere ve kısıtlamalara mutlaka uy."
                )

            answer = self._query_llm(system_prompt, user_prompt)
            results[step_id] = {"response": answer}

        return results


__all__ = ["LLMAnalyzer", "OpenAIError", "DEFAULT_8D_PROMPT"]
