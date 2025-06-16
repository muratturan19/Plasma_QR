import unittest
from unittest.mock import patch, MagicMock
import types

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

    def test_query_llm_fallback(self) -> None:
        """``_query_llm`` should return a placeholder for non-auth errors."""
        mock_openai = types.ModuleType("openai")
        mock_openai.ChatCompletion = MagicMock()
        mock_openai.ChatCompletion.create.side_effect = Exception("network")
        with patch.dict("sys.modules", {"openai": mock_openai}):
            with patch.dict("os.environ", {"OPENAI_API_KEY": "key"}):
                result = self.analyzer._query_llm("prompt")
        self.assertTrue(result.startswith("LLM response placeholder"))

    def test_query_llm_logs_error(self) -> None:
        """Network errors should be printed for easier debugging."""
        mock_openai = types.ModuleType("openai")
        mock_openai.ChatCompletion = MagicMock()
        exc = Exception("timeout")
        mock_openai.ChatCompletion.create.side_effect = exc
        with patch.dict("sys.modules", {"openai": mock_openai}):
            with patch.dict("os.environ", {"OPENAI_API_KEY": "key"}):
                with patch("builtins.print") as mock_print:
                    self.analyzer._query_llm("prompt")
        mock_print.assert_any_call(f"LLMAnalyzer error: {exc}")

    def test_missing_api_key_raises(self) -> None:
        """Missing ``OPENAI_API_KEY`` should raise ``OpenAIError``."""
        mock_openai = types.ModuleType("openai")
        mock_openai.ChatCompletion = MagicMock()
        with patch.dict("sys.modules", {"openai": mock_openai}):
            with patch.dict("os.environ", {}, clear=True):
                with self.assertRaises(OpenAIError):
                    self.analyzer._query_llm("prompt")

    def test_invalid_api_key_raises(self) -> None:
        """Invalid API key should raise ``OpenAIError``."""
        mock_openai = types.ModuleType("openai")
        mock_openai.ChatCompletion = MagicMock()
        mock_openai.ChatCompletion.create.side_effect = Exception("invalid api key")
        with patch.dict("sys.modules", {"openai": mock_openai}):
            with patch.dict("os.environ", {"OPENAI_API_KEY": "bad"}):
                with self.assertRaises(OpenAIError):
                    self.analyzer._query_llm("prompt")

    def test_init_uses_openai_model_env(self) -> None:
        """Default model should come from ``OPENAI_MODEL`` env variable."""
        with patch.dict("os.environ", {"OPENAI_MODEL": "gpt-test"}):
            analyzer = LLMAnalyzer()
        self.assertEqual(analyzer.model, "gpt-test")

    def test_query_llm_logs_tokens(self) -> None:
        """Successful calls should print start, token usage and end messages."""
        mock_openai = types.ModuleType("openai")
        usage = types.SimpleNamespace(total_tokens=5)
        response = types.SimpleNamespace(
            choices=[types.SimpleNamespace(message={"content": "ok"})],
            usage=usage,
        )
        mock_chat = MagicMock()
        mock_chat.create.return_value = response
        mock_openai.ChatCompletion = mock_chat
        with patch.dict("sys.modules", {"openai": mock_openai}):
            with patch.dict("os.environ", {"OPENAI_API_KEY": "key"}):
                with patch("builtins.print") as mock_print:
                    result = self.analyzer._query_llm("prompt")
        self.assertEqual(result, "ok")
        expected = [
            unittest.mock.call("LLMAnalyzer._query_llm start"),
            unittest.mock.call("LLMAnalyzer tokens used: 5"),
            unittest.mock.call("LLMAnalyzer._query_llm end"),
        ]
        mock_print.assert_has_calls(expected)
        self.assertEqual(mock_print.call_count, 3)


if __name__ == "__main__":
    unittest.main()
