import json
from pathlib import Path
import unittest
import unittest.mock

from PromptManager import PromptManager


class PromptManagerTest(unittest.TestCase):
    """Tests for PromptManager template loading."""

    def setUp(self) -> None:
        self.manager = PromptManager()
        self.base_dir = Path(__file__).resolve().parents[1] / "Prompts"

    def test_get_template(self) -> None:
        for method in ["5N1K", "A3", "DMAIC", "Ishikawa"]:
            with self.subTest(method=method):
                expected_path = self.base_dir / f"{method}_Prompt.json"
                with open(expected_path, "r", encoding="utf-8") as f:
                    expected = json.load(f)
                result = self.manager.get_template(method)
                self.assertEqual(result, expected)

    def test_load_prompt(self) -> None:
        test_file = self.base_dir / "5N1K_Prompt.json"
        with open(test_file, "r", encoding="utf-8") as f:
            expected = json.load(f)
        result = self.manager.load_prompt(str(test_file))
        self.assertEqual(result, expected)

    def test_get_template_caches_result(self) -> None:
        """Repeated calls should not reopen the template file."""
        test_file = self.base_dir / "5N1K_Prompt.json"
        with open(test_file, "r", encoding="utf-8") as f:
            data = f.read()

        with unittest.mock.patch(
            "builtins.open", unittest.mock.mock_open(read_data=data)
        ) as mocked_open:
            first = self.manager.get_template("5N1K")
            second = self.manager.get_template("5N1K")

            self.assertEqual(mocked_open.call_count, 1)
            self.assertIs(first, second)

if __name__ == "__main__":
    unittest.main()
