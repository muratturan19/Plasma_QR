import types
import unittest
from unittest.mock import patch, mock_open, MagicMock

from Review import Review


class ReviewTest(unittest.TestCase):
    """Tests for the Review class."""

    def test_perform_uses_query_llm(self) -> None:
        review = Review()
        with patch.object(Review, "_query_llm", side_effect=["a", "b"]) as mock_query:
            result = review.perform(["x", "y"])
            self.assertEqual(result, ["a", "b"])
            self.assertEqual(mock_query.call_count, 2)

    def test_prompt_template_is_used(self) -> None:
        template = "prefix {initial_report_text} suffix"
        with patch("builtins.open", mock_open(read_data=template)):
            review = Review()
        with patch.object(Review, "_query_llm") as mock_query:
            mock_query.return_value = "ok"
            review.perform(["data"])
            mock_query.assert_called_with("prefix data suffix")

    def test_query_llm_logs_error(self) -> None:
        """Ensure network errors are printed for debugging."""
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
                with patch("builtins.print") as mock_print:
                    review._query_llm("prompt")
        mock_print.assert_any_call(f"Review error: {exc}")

    def test_query_llm_logs_tokens(self) -> None:
        """Ensure start and end messages as well as token usage are printed."""
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
                with patch("builtins.print") as mock_print:
                    result = review._query_llm("prompt")
        self.assertEqual(result, "rev")
        expected = [
            unittest.mock.call("Review._query_llm start"),
            unittest.mock.call("Review tokens used: 3"),
            unittest.mock.call("Review._query_llm end"),
        ]
        mock_print.assert_has_calls(expected)
        self.assertEqual(mock_print.call_count, 3)


if __name__ == "__main__":
    unittest.main()
