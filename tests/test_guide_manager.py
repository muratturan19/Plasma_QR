import json
from pathlib import Path
import unittest

from GuideManager import GuideManager


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


if __name__ == "__main__":
    unittest.main()
