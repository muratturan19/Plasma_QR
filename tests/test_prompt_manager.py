import json
from pathlib import Path
import unittest

from PromptManager import PromptManager


class PromptManagerTest(unittest.TestCase):
    """Tests for PromptManager template loading."""

    def setUp(self) -> None:
        self.manager = PromptManager()
        self.base_dir = Path(__file__).resolve().parents[1] / "Prompts"

    def test_get_template(self) -> None:
        for method in ["5N1K", "8D", "A3", "DMAIC", "Ishikawa"]:
            with self.subTest(method=method):
                expected_path = self.base_dir / f"{method}_Prompt.json"
                with open(expected_path, "r", encoding="utf-8") as f:
                    expected = json.load(f)
                result = self.manager.get_template(method)
                self.assertEqual(result, expected)

    def test_load_prompt(self) -> None:
        test_file = self.base_dir / "8D_Prompt.json"
        with open(test_file, "r", encoding="utf-8") as f:
            expected = json.load(f)
        result = self.manager.load_prompt(str(test_file))
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
