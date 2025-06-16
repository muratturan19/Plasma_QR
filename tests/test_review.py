import unittest
from unittest.mock import patch, mock_open

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


if __name__ == "__main__":
    unittest.main()
