"""Streamlit interface for Quality Reporter."""

from __future__ import annotations

import streamlit as st

from pathlib import Path
import json
from GuideManager import GuideManager
from LLMAnalyzer import LLMAnalyzer
from ReportGenerator import ReportGenerator
from Review import Review

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
        with st.spinner("Rapor değerlendiriliyor..."):
            reviewer = Review()
            reviewed = reviewer.perform(
                [v["response"] for v in analysis.values()],
                method=method,
                customer=customer,
                subject=subject,
                part_code=part_code,
                guideline_json=json.dumps(guideline, ensure_ascii=False),
            )
            for (key, value), new_resp in zip(analysis.items(), reviewed):
                value["response"] = new_resp

        complaint_info = {
            "customer": customer,
            "subject": subject,
            "part_code": part_code,
        }
        generator = ReportGenerator(manager)
        paths = generator.generate(analysis, complaint_info, "reports")

        st.subheader("Analysis")
        st.json(analysis)

        pdf_name = Path(paths["pdf"]).name
        with open(paths["pdf"], "rb") as pdf_file:
            st.download_button("Download PDF", pdf_file, file_name=pdf_name)

        excel_name = Path(paths["excel"]).name
        with open(paths["excel"], "rb") as excel_file:
            st.download_button("Download Excel", excel_file, file_name=excel_name)

        st.markdown(f"[PDF file]({paths['pdf']})")
        st.markdown(f"[Excel file]({paths['excel']})")


if __name__ == "__main__":
    main()
