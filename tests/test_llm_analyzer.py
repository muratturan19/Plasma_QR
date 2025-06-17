import unittest
from unittest.mock import patch, MagicMock
import types

from GuideManager import GuideManager

from LLMAnalyzer import LLMAnalyzer, OpenAIError


class LLMAnalyzerTest(unittest.TestCase):
    """Tests for LLMAnalyzer.analyze."""

    def setUp(self) -> None:
        self.analyzer = LLMAnalyzer()
        self.guideline = {"fields": [{"id": "Step1"}, {"id": "Step2"}]}

    @patch.object(LLMAnalyzer, "_query_llm", return_value="answer")
    def test_analyze_returns_keys(self, mock_query) -> None:  # type: ignore
        details = {
            "complaint": "text",
            "customer": "cust",
            "subject": "subj",
            "part_code": "code",
        }
        result = self.analyzer.analyze(details, self.guideline)
        self.assertEqual(set(result.keys()), {"Step1", "Step2"})
        for value in result.values():
            self.assertIn("response", value)

    @patch.object(LLMAnalyzer, "_query_llm", return_value="answer")
    def test_analyze_handles_steps(self, mock_query) -> None:  # type: ignore
        """Guidelines using 'steps' should be processed correctly."""
        guideline = {"steps": [{"step": "D1"}, {"step": "D2"}]}
        details = {"complaint": "c"}
        result = self.analyzer.analyze(details, guideline)
        self.assertEqual(set(result.keys()), {"D1", "D2"})

    @patch.object(LLMAnalyzer, "_query_llm", return_value="answer")
    def test_prompt_focuses_on_single_step(self, mock_query) -> None:  # type: ignore
        """Prompt should instruct the model to analyze only the current step."""
        guideline = {
            "method": "8D",
            "fields": [{"id": "D1", "definition": "desc"}],
        }
        details = {"complaint": "issue"}
        self.analyzer.analyze(details, guideline)
        system_prompt, user_prompt = mock_query.call_args[0]
        self.assertIn("D1", system_prompt)
        self.assertIn("SADECE", system_prompt)

    @patch.object(LLMAnalyzer, "_query_llm", return_value="ok")
    def test_analyze_uses_prompt_template(self, mock_query) -> None:  # type: ignore
        """Templates from PromptManager should be applied."""
        manager = GuideManager()
        guideline = manager.get_format("8D")
        details = {
            "complaint": "c",
            "customer": "cust",
            "subject": "subj",
            "part_code": "code",
        }
        self.analyzer.analyze(details, guideline)
        system_prompt, user_prompt = mock_query.call_args_list[0][0]
        self.assertIn("D1", system_prompt)
        self.assertIn("Ekip Oluşturma", system_prompt)
        self.assertIn("Müşteri Şikayeti: c", user_prompt)
        self.assertIn("Parça Kodu: code", user_prompt)

    @patch.object(LLMAnalyzer, "_query_llm")
    def test_previous_results_included(self, mock_query) -> None:  # type: ignore
        """Earlier step answers should appear in later step prompts."""
        mock_query.side_effect = ["first", "second"]
        guideline = {
            "method": "8D",
            "fields": [{"id": "D1"}, {"id": "D2"}],
        }
        details = {"complaint": "c"}

        self.analyzer.analyze(details, guideline)

        first_call = mock_query.call_args_list[0][0]
        second_call = mock_query.call_args_list[1][0]

        self.assertNotIn("first", first_call[1])
        self.assertIn("first", second_call[1])

    def test_query_llm_fallback(self) -> None:
        """``_query_llm`` should return a placeholder for non-auth errors."""
        mock_openai = types.ModuleType("openai")
        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = Exception("network")
        mock_openai.OpenAI = MagicMock(return_value=mock_client)
        with patch.dict("sys.modules", {"openai": mock_openai}):
            with patch.dict("os.environ", {"OPENAI_API_KEY": "key"}):
                result = self.analyzer._query_llm("sys", "prompt")
        self.assertTrue(result.startswith("LLM response placeholder"))

    def test_query_llm_logs_error(self) -> None:
        """Network errors should be logged for easier debugging."""
        mock_openai = types.ModuleType("openai")
        mock_client = MagicMock()
        exc = Exception("timeout")
        mock_client.chat.completions.create.side_effect = exc
        mock_openai.OpenAI = MagicMock(return_value=mock_client)
        with patch.dict("sys.modules", {"openai": mock_openai}):
            with patch.dict("os.environ", {"OPENAI_API_KEY": "key"}):
                with self.assertLogs("LLMAnalyzer", level="ERROR") as log:
                    self.analyzer._query_llm("sys", "prompt")
        self.assertIn(f"LLMAnalyzer error: {exc}", "\n".join(log.output))

    def test_missing_api_key_raises(self) -> None:
        """Missing ``OPENAI_API_KEY`` should raise ``OpenAIError``."""
        mock_openai = types.ModuleType("openai")
        mock_openai.OpenAI = MagicMock(return_value=MagicMock())
        with patch.dict("sys.modules", {"openai": mock_openai}):
            with patch.dict("os.environ", {}, clear=True):
                with self.assertRaises(OpenAIError):
                    self.analyzer._query_llm("sys", "prompt")

    def test_invalid_api_key_raises(self) -> None:
        """Invalid API key should raise ``OpenAIError``."""
        mock_openai = types.ModuleType("openai")
        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = Exception("invalid api key")
        mock_openai.OpenAI = MagicMock(return_value=mock_client)
        with patch.dict("sys.modules", {"openai": mock_openai}):
            with patch.dict("os.environ", {"OPENAI_API_KEY": "bad"}):
                with self.assertRaises(OpenAIError):
                    self.analyzer._query_llm("sys", "prompt")

    def test_init_uses_openai_model_env(self) -> None:
        """Default model should come from ``OPENAI_MODEL`` env variable."""
        with patch.dict("os.environ", {"OPENAI_MODEL": "gpt-test"}):
            analyzer = LLMAnalyzer()
        self.assertEqual(analyzer.model, "gpt-test")

    def test_query_llm_logs_tokens(self) -> None:
        """Successful calls should log start, token usage and end messages."""
        mock_openai = types.ModuleType("openai")
        usage = types.SimpleNamespace(total_tokens=5)
        response = types.SimpleNamespace(
            choices=[types.SimpleNamespace(message=types.SimpleNamespace(content="ok"))],
            usage=usage,
        )
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = response
        mock_openai.OpenAI = MagicMock(return_value=mock_client)
        with patch.dict("sys.modules", {"openai": mock_openai}):
            with patch.dict("os.environ", {"OPENAI_API_KEY": "key"}):
                with self.assertLogs("LLMAnalyzer", level="DEBUG") as log:
                    result = self.analyzer._query_llm("sys", "prompt")
        self.assertEqual(result, "ok")
        messages = "\n".join(log.output)
        self.assertIn("LLMAnalyzer._query_llm start", messages)
        self.assertIn("LLMAnalyzer tokens used: 5", messages)
        self.assertIn("LLMAnalyzer._query_llm end", messages)


if __name__ == "__main__":
    unittest.main()
