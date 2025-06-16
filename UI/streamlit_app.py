"""Streamlit interface for Quality Reporter."""

from __future__ import annotations

import streamlit as st

from GuideManager import GuideManager
from LLMAnalyzer import LLMAnalyzer
from ReportGenerator import ReportGenerator

METHODS = ["8D", "5N1K", "A3", "DMAIC", "Ishikawa"]


def main() -> None:
    """Run the Streamlit application."""
    st.title("Quality Reporter")

    complaint = st.text_area("Complaint")
    method = st.selectbox("Method", METHODS)
    customer = st.text_input("Customer")
    subject = st.text_input("Subject")
    part_code = st.text_input("Part code")

    if st.button("Analyze"):
        manager = GuideManager()
        guideline = manager.get_format(method)

        analyzer = LLMAnalyzer()
        details: dict[str, str] = {
            "complaint": complaint,
            "customer": customer,
            "subject": subject,
            "part_code": part_code,
        }
        with st.spinner("Analyzing..."):
            analysis = analyzer.analyze(details, guideline)

        complaint_info = {
            "customer": customer,
            "subject": subject,
            "part_code": part_code,
        }
        generator = ReportGenerator(manager)
        paths = generator.generate(analysis, complaint_info, "reports")

        st.subheader("Analysis")
        st.json(analysis)

        with open(paths["pdf"], "rb") as pdf_file:
            st.download_button("Download PDF", pdf_file, file_name="report.pdf")

        with open(paths["excel"], "rb") as excel_file:
            st.download_button("Download Excel", excel_file, file_name="report.xlsx")

        st.markdown(f"[PDF file]({paths['pdf']})")
        st.markdown(f"[Excel file]({paths['excel']})")


if __name__ == "__main__":
    main()
