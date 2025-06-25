import tempfile
import unittest

from ComplaintSearch import ComplaintStore


class ComplaintStoreTest(unittest.TestCase):
    """Tests for the ComplaintStore utility."""

    def test_add_and_search(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = f"{tmpdir}/complaints.json"
            store = ComplaintStore(path)
            record = {
                "complaint": "noise issue",
                "customer": "ACME",
                "subject": "engine",
                "part_code": "X1",
            }
            store.add_complaint(record)
            results = store.search("noise")
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0]["customer"], "ACME")
            results_empty = store.search("missing")
            self.assertEqual(results_empty, [])

    def test_normalization_and_fuzzy(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = f"{tmpdir}/complaints.json"
            store = ComplaintStore(path)
            store.add_complaint({
                "complaint": "M\u015fteri \u015fikayet",  # includes accents
                "customer": "ACME",
                "subject": "engine",
                "part_code": "X1",
            })
            store.add_complaint({
                "complaint": "noise issue",
                "customer": "BETA",
                "subject": "door",
                "part_code": "X2",
            })

            accent = store.search("sikayet")
            self.assertEqual(len(accent), 1)
            self.assertEqual(accent[0]["customer"], "ACME")

            typo = store.search("noize issue")
            self.assertEqual(len(typo), 1)
            self.assertEqual(typo[0]["customer"], "BETA")


if __name__ == "__main__":
    unittest.main()
