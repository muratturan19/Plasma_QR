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

    def test_query_llm_fallback(self) -> None:
        """``_query_llm`` should return a placeholder for non-auth errors."""
        mock_openai = types.ModuleType("openai")
        mock_openai.ChatCompletion = MagicMock()
        mock_openai.ChatCompletion.create.side_effect = Exception("network")
        with patch.dict("sys.modules", {"openai": mock_openai}):
            with patch.dict("os.environ", {"OPENAI_API_KEY": "key"}):
                result = self.analyzer._query_llm("prompt")
        self.assertTrue(result.startswith("LLM response placeholder"))

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


if __name__ == "__main__":
    unittest.main()
