import unittest
from unittest.mock import patch

from LLMAnalyzer import LLMAnalyzer


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
        """``_query_llm`` should return a placeholder when OpenAI fails."""
        result = self.analyzer._query_llm("prompt")
        self.assertTrue(result.startswith("LLM response placeholder"))


if __name__ == "__main__":
    unittest.main()
