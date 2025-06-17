import unittest

from Comparison import Comparison


class ComparisonTest(unittest.TestCase):
    """Tests for the Comparison utilities."""

    def setUp(self) -> None:
        self.comp = Comparison()

    def test_compare_strings(self) -> None:
        result = self.comp.compare("a\nb", "a\nc")
        self.assertEqual(result["added"], ["c"])
        self.assertEqual(result["removed"], ["b"])

    def test_compare_dicts(self) -> None:
        old = {"a": 1, "b": 2}
        new = {"a": 1, "b": 3, "c": 4}
        result = self.comp.compare(old, new)
        self.assertIn('  "b": 3,', result["added"])  # note trailing comma from JSON
        self.assertIn('  "c": 4', result["added"])
        self.assertIn('  "b": 2', result["removed"])


if __name__ == "__main__":
    unittest.main()
