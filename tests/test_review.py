import types
import unittest
from unittest.mock import patch, mock_open, MagicMock

from Review import Review


class ReviewTest(unittest.TestCase):
    """Tests for the Review class."""

    def test_perform_uses_query_llm(self) -> None:
        review = Review()
        with patch.object(Review, "_query_llm", return_value="a") as mock_query:
            result = review.perform("x")
            self.assertEqual(result, "a")
            mock_query.assert_called_once()

    def test_prompt_template_is_used(self) -> None:
        template = "prefix {initial_report_text} suffix"
        with patch("builtins.open", mock_open(read_data=template)):
            review = Review()
        with patch.object(Review, "_query_llm") as mock_query:
            mock_query.return_value = "ok"
            review.perform("data", language="Türkçe")
            mock_query.assert_called_with("prefix data suffix")

    def test_query_llm_logs_error(self) -> None:
        """Ensure network errors are logged for debugging."""
        template = "{initial_report_text}"
        with patch("builtins.open", mock_open(read_data=template)):
            review = Review()
        mock_openai = types.ModuleType("openai")
        mock_client = MagicMock()
        exc = Exception("timeout")
        mock_client.chat.completions.create.side_effect = exc
        mock_openai.OpenAI = MagicMock(return_value=mock_client)
        with patch.dict("sys.modules", {"openai": mock_openai}):
            with patch.dict("os.environ", {"OPENAI_API_KEY": "key"}):
                with self.assertLogs("Review", level="ERROR") as log:
                    review._query_llm("prompt")
        self.assertIn(f"Review error: {exc}", "\n".join(log.output))

    def test_query_llm_logs_tokens(self) -> None:
        """Ensure start, end and token usage messages are logged."""
        template = "{initial_report_text}"
        with patch("builtins.open", mock_open(read_data=template)):
            review = Review()
        mock_openai = types.ModuleType("openai")
        usage = types.SimpleNamespace(total_tokens=3)
        response = types.SimpleNamespace(
            choices=[types.SimpleNamespace(message=types.SimpleNamespace(content="rev"))],
            usage=usage,
        )
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = response
        mock_openai.OpenAI = MagicMock(return_value=mock_client)
        with patch.dict("sys.modules", {"openai": mock_openai}):
            with patch.dict("os.environ", {"OPENAI_API_KEY": "key"}):
                with self.assertLogs("Review", level="DEBUG") as log:
                    result = review._query_llm("prompt")
        self.assertEqual(result, "rev")
        messages = "\n".join(log.output)
        self.assertIn("Review._query_llm start", messages)
        self.assertIn("INFO:Review:Review tokens used: 3", messages)
        self.assertIn("Review._query_llm end", messages)


if __name__ == "__main__":
    unittest.main()
