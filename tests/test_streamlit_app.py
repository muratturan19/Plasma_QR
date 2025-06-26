import importlib
import json
import sys
import types
import unittest
from contextlib import contextmanager
from unittest.mock import MagicMock, patch, mock_open
from pathlib import Path


class StreamlitAppTest(unittest.TestCase):
    """Tests for the Streamlit UI."""

    def setUp(self) -> None:
        dummy_st = types.ModuleType("streamlit")
        dummy_st.title = MagicMock()
        dummy_st.set_page_config = MagicMock()
        dummy_st.text_area = MagicMock(return_value="c")
        dummy_st.selectbox = MagicMock(side_effect=["A3", "Tümü"])
        dummy_st.text_input = MagicMock(side_effect=["cust", "subject", "code"])
        dummy_st.button = MagicMock(return_value=True)
        dummy_st.checkbox = MagicMock(return_value=False)
        dummy_st.subheader = MagicMock()
        dummy_st.write = MagicMock()
        dummy_st.json = MagicMock()
        dummy_st.download_button = MagicMock()
        dummy_st.markdown = MagicMock()
        sidebar = types.SimpleNamespace(
            markdown=MagicMock(),
            text_input=MagicMock(return_value="q"),
            button=MagicMock(return_value=False),
            json=MagicMock(),
            image=MagicMock(),
        )
        dummy_st.sidebar = sidebar

        def columns(num: int):
            return [dummy_st for _ in range(num)]

        dummy_st.columns = MagicMock(side_effect=columns)

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
        m_open = mock_open(read_data=b"data")
        with patch.object(module, "GuideManager") as mock_manager, \
             patch.object(module, "LLMAnalyzer") as mock_analyzer, \
             patch.object(module, "ReportGenerator") as mock_report, \
             patch.object(module, "Review") as mock_review, \
             patch.object(module, "ComplaintStore") as mock_store, \
             patch.object(module, "ExcelClaimsSearcher") as mock_claims, \
             patch("builtins.open", m_open), \
             patch.object(Path, "exists", return_value=True):
            mock_manager.return_value.get_format.return_value = {"fields": []}
            mock_analyzer.return_value.analyze.return_value = {
                "full_text": "ok"
            }
            mock_review.return_value.perform.return_value = "checked"
            mock_report.return_value.generate.return_value = {
                "pdf": "file.pdf",
                "excel": "file.xlsx",
            }
            mock_claims.return_value.search.return_value = []

            module.main()

            self.dummy_st.set_page_config.assert_called_once()
            self.dummy_st.columns.assert_called()

            m_open.assert_any_call(Path("reports") / "LLM1.txt", "w", encoding="utf-8")
            m_open.assert_any_call(Path("reports") / "LLM2.txt", "w", encoding="utf-8")

            mock_manager.return_value.get_format.assert_called_with("A3")
            mock_analyzer.return_value.analyze.assert_called_once()
            mock_review.return_value.perform.assert_called_with(
                "ok",
                method="A3",
                customer="cust",
                subject="subject",
                part_code="code",
                guideline_json=json.dumps({"fields": []}, ensure_ascii=False),
            )
            mock_report.return_value.generate.assert_called_with(
                {
                    "full_text": "ok",
                    "full_report": {"response": "checked"},
                },
                {"customer": "cust", "subject": "subject", "part_code": "code"},
                "reports",
            )
            mock_store.return_value.add_complaint.assert_called_once()
            mock_claims.return_value.search.assert_called_once()
            self.assertTrue(self.dummy_st.download_button.called)


class StreamlitSearchTest(unittest.TestCase):
    """Tests for sidebar search behavior."""

    def _setup_env(self, sidebar_button: bool, query_button: bool = False) -> types.ModuleType:
        dummy_st = types.ModuleType("streamlit")
        dummy_st.title = MagicMock()
        dummy_st.set_page_config = MagicMock()
        dummy_st.text_area = MagicMock(return_value="")
        dummy_st.selectbox = MagicMock(side_effect=["A3", "Tümü"])
        dummy_st.text_input = MagicMock(side_effect=["c", "s", "p"])
        dummy_st.button = MagicMock(side_effect=[query_button, False])
        dummy_st.checkbox = MagicMock(return_value=False)
        dummy_st.subheader = MagicMock()
        dummy_st.write = MagicMock()
        dummy_st.json = MagicMock()
        dummy_st.download_button = MagicMock()
        dummy_st.markdown = MagicMock()
        sidebar = types.SimpleNamespace(
            markdown=MagicMock(),
            text_input=MagicMock(return_value="k"),
            button=MagicMock(return_value=sidebar_button),
            json=MagicMock(),
            image=MagicMock(),
            write=MagicMock(),
        )
        dummy_st.sidebar = sidebar
        dummy_st.columns = MagicMock(return_value=[dummy_st, dummy_st])

        spinner_mock = MagicMock()

        @contextmanager
        def spinner(*args, **kwargs):
            spinner_mock(*args, **kwargs)
            yield

        dummy_st.spinner = spinner
        sys.modules["streamlit"] = dummy_st
        self.spinner = spinner_mock
        self.dummy_st = dummy_st
        return dummy_st

    def tearDown(self) -> None:
        sys.modules.pop("streamlit", None)

    def test_empty_search_shows_message(self) -> None:
        dummy_st = self._setup_env(True)
        module = importlib.import_module("UI.streamlit_app")
        importlib.reload(module)
        with patch.object(module, "ComplaintStore") as mock_store:
            mock_store.return_value.search.return_value = []
            module.main()
            self.assertTrue(self.spinner.called)
            calls = dummy_st.sidebar.markdown.call_args_list
            self.assertTrue(any("Sonuç bulunamadı" in str(c.args[0]) for c in calls))

    def test_search_renders_card(self) -> None:
        record = {"complaint": "x", "subject": "y", "customer": "z", "date": "d"}
        dummy_st = self._setup_env(True)
        module = importlib.import_module("UI.streamlit_app")
        importlib.reload(module)
        with patch.object(module, "ComplaintStore") as mock_store:
            mock_store.return_value.search.return_value = [record]
            module.main()
            self.assertTrue(self.spinner.called)
            html_calls = [str(c.args[0]) for c in dummy_st.sidebar.markdown.call_args_list]
            self.assertTrue(any("<strong>" in h for h in html_calls))

    def test_query_empty_search_shows_message(self) -> None:
        dummy_st = self._setup_env(False, query_button=True)
        module = importlib.import_module("UI.streamlit_app")
        importlib.reload(module)
        with patch.object(module, "ExcelClaimsSearcher") as mock_searcher:
            mock_searcher.return_value.search.return_value = []
            module.main()
            self.assertTrue(self.spinner.called)
            calls = dummy_st.markdown.call_args_list
            self.assertTrue(any("Sonuç bulunamadı" in str(c.args[0]) for c in calls))

    def test_query_search_renders_card(self) -> None:
        record = {"complaint": "a", "subject": "b", "customer": "c", "date": "d"}
        dummy_st = self._setup_env(False, query_button=True)
        module = importlib.import_module("UI.streamlit_app")
        importlib.reload(module)
        with patch.object(module, "ExcelClaimsSearcher") as mock_searcher:
            mock_searcher.return_value.search.return_value = [record]
            module.main()
            self.assertTrue(self.spinner.called)
            html_calls = [str(c.args[0]) for c in dummy_st.markdown.call_args_list]
            self.assertTrue(any("<strong>" in h for h in html_calls))


if __name__ == "__main__":
    unittest.main()
