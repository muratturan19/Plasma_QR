import unittest
from unittest.mock import patch, MagicMock
import types

from GuideManager import GuideManager

from LLMAnalyzer import DEFAULT_8D_PROMPT, LLMAnalyzer, OpenAIError


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

    @patch.object(LLMAnalyzer, "_query_llm", return_value="ok")
    def test_8d_returns_full_text(self, mock_query) -> None:  # type: ignore
        """Method ``8D`` should return a ``full_text`` key with the response."""
        guideline = {"method": "8D", "fields": []}
        details = {"complaint": "c", "subject": "s", "part_code": "p"}
        result = self.analyzer.analyze(details, guideline)
        self.assertEqual(result, {"full_text": "ok"})
        mock_query.assert_called_once()
        call_args = mock_query.call_args[0]
        self.assertEqual(call_args[0], DEFAULT_8D_PROMPT)

    @patch.object(LLMAnalyzer, "_query_llm", return_value="text")
    def test_text_prompt_returns_full_text(self, mock_query) -> None:  # type: ignore
        """Methods with text prompts should return ``full_text``."""
        guideline = {"method": "A3", "fields": []}
        details = {"complaint": "comp", "subject": "sub", "part_code": "p"}
        result = self.analyzer.analyze(details, guideline)
        self.assertEqual(result, {"full_text": "text"})
        mock_query.assert_called_once()
        call_args = mock_query.call_args[0]
        self.assertEqual(call_args[0], "")
        self.assertIn("comp", call_args[1])

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
        self.assertIn("INFO:LLMAnalyzer:LLMAnalyzer tokens used: 5", messages)
        self.assertIn("LLMAnalyzer._query_llm end", messages)


if __name__ == "__main__":
    unittest.main()
