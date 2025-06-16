import importlib
import sys
import types
import unittest
from contextlib import contextmanager
from unittest.mock import MagicMock, patch, mock_open


class StreamlitAppTest(unittest.TestCase):
    """Tests for the Streamlit UI."""

    def setUp(self) -> None:
        dummy_st = types.ModuleType("streamlit")
        dummy_st.title = MagicMock()
        dummy_st.text_area = MagicMock(return_value="c")
        dummy_st.selectbox = MagicMock(return_value="8D")
        dummy_st.text_input = MagicMock(side_effect=["cust", "subject", "code"])
        dummy_st.button = MagicMock(return_value=True)
        dummy_st.subheader = MagicMock()
        dummy_st.json = MagicMock()
        dummy_st.download_button = MagicMock()
        dummy_st.markdown = MagicMock()

        @contextmanager
        def spinner(*args, **kwargs):
            yield

        dummy_st.spinner = spinner
        sys.modules["streamlit"] = dummy_st
        self.dummy_st = dummy_st

    def tearDown(self) -> None:
        sys.modules.pop("streamlit", None)

    def test_main_pipeline(self) -> None:
        module = importlib.import_module("UI.streamlit_app")
        with patch.object(module, "GuideManager") as mock_manager, \
             patch.object(module, "LLMAnalyzer") as mock_analyzer, \
             patch.object(module, "ReportGenerator") as mock_report, \
             patch.object(module, "Review") as mock_review, \
             patch("builtins.open", mock_open(read_data=b"data")):
            mock_manager.return_value.get_format.return_value = {"fields": []}
            mock_analyzer.return_value.analyze.return_value = {
                "Step1": {"response": "ok"}
            }
            mock_review.return_value.perform.return_value = ["checked"]
            mock_report.return_value.generate.return_value = {
                "pdf": "file.pdf",
                "excel": "file.xlsx",
            }

            module.main()

            mock_manager.return_value.get_format.assert_called_with("8D")
            mock_analyzer.return_value.analyze.assert_called_once()
            mock_review.return_value.perform.assert_called_with(["ok"])
            mock_report.return_value.generate.assert_called_with(
                {"Step1": {"response": "checked"}},
                {"customer": "cust", "subject": "subject", "part_code": "code"},
                "reports",
            )
            self.assertTrue(self.dummy_st.download_button.called)


if __name__ == "__main__":
    unittest.main()
