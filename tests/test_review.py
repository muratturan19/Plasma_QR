import unittest
from unittest.mock import patch

from Review import Review


class ReviewTest(unittest.TestCase):
    """Tests for the Review class."""

    def test_perform_uses_query_llm(self) -> None:
        review = Review()
        with patch.object(Review, "_query_llm", side_effect=["a", "b"]) as mock_query:
            result = review.perform(["x", "y"])
            self.assertEqual(result, ["a", "b"])
            self.assertEqual(mock_query.call_count, 2)


if __name__ == "__main__":
    unittest.main()
