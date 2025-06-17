import json
from pathlib import Path
import unittest
import unittest.mock

from GuideManager import DEFAULT_8D_GUIDE, GuideManager


class GuideManagerTest(unittest.TestCase):
    """Tests for GuideManager guide loading."""

    def setUp(self) -> None:
        self.manager = GuideManager()
        self.base_dir = Path(__file__).resolve().parents[1] / "Guidelines"

    def test_get_format(self) -> None:
        for method in ["5N1K", "8D", "A3", "DMAIC", "Ishikawa"]:
            with self.subTest(method=method):
                expected_path = self.base_dir / f"{method}_Guide.json"
                with open(expected_path, "r", encoding="utf-8") as f:
                    expected = json.load(f)
                result = self.manager.get_format(method)
                self.assertEqual(result, expected)

    def test_load_guide(self) -> None:
        test_file = self.base_dir / "5N1K_Guide.json"
        with open(test_file, "r", encoding="utf-8") as f:
            expected = json.load(f)
        result = self.manager.load_guide(str(test_file))
        self.assertEqual(result, expected)

    def test_get_format_caches_result(self) -> None:
        """Repeated calls should not reopen the guideline file."""
        test_file = self.base_dir / "8D_Guide.json"
        with open(test_file, "r", encoding="utf-8") as f:
            data = f.read()

        with unittest.mock.patch(
            "builtins.open", unittest.mock.mock_open(read_data=data)
        ) as mocked_open:
            first = self.manager.get_format("8D")
            second = self.manager.get_format("8D")

            self.assertEqual(mocked_open.call_count, 1)
            self.assertIs(first, second)

    def test_get_format_fallback_default_8d(self) -> None:
        """Return the default guide when the file is missing."""
        target = self.base_dir / "8D_Guide.json"
        backup = target.with_suffix(".json.bak")
        target.rename(backup)
        try:
            result = self.manager.get_format("8D")
            self.assertEqual(result, DEFAULT_8D_GUIDE)
        finally:
            backup.rename(target)


if __name__ == "__main__":
    unittest.main()
