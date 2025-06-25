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


if __name__ == "__main__":
    unittest.main()
