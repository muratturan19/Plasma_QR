"""Streamlit interface for Quality Reporter."""

from __future__ import annotations

import streamlit as st

from pathlib import Path
import json
from datetime import datetime
from GuideManager import GuideManager
from LLMAnalyzer import LLMAnalyzer
from ReportGenerator import ReportGenerator
from Review import Review
from ComplaintSearch import ComplaintStore, ExcelClaimsSearcher

st.set_page_config(
    page_title="Akıllı Kalite Raporlama Asistanı",
    page_icon=":memo:",
    layout="centered",
)

st.markdown(
    """
    <style>
        body {
            background-color: #f9f9f9;
        }
        h1 {
            color: #4E79A7;
        }
        .card {
            background-color: #ffffff;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-bottom: 1rem;
        }
        .stButton>button {
            background-color: #d72638;
            color: white;
        }
        .stButton>button:hover {
            background-color: #b71c2f;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

METHODS = ["8D", "5N1K", "A3", "DMAIC", "Ishikawa"]


def main() -> None:
    """Run the Streamlit application."""

    logo_path = Path(__file__).resolve().parents[1] / "Logo" / "logo.png"
    if logo_path.exists():
        cols = st.columns(3)
        # Display the logo at four times the previous width
        cols[1].image(str(logo_path), width=240)
    st.markdown(
        "<h1 style='text-align: center; font-size: 64px;'>PLASMA PLASTİK</h1>",
        unsafe_allow_html=True,
    )
    st.sidebar.markdown("### Search Complaints")
    search_term = st.sidebar.text_input("Keyword")
    if st.sidebar.button("Search"):
        results = ComplaintStore().search(search_term)
        st.sidebar.write(f"Results: {len(results)}")
        for item in results:
            st.sidebar.json(item)
    st.title("Akıllı Kalite Raporlama Asistanı")
    st.markdown(
        "Müşteri şikâyetini girin, metod seçin ve saniyeler "
        "içinde profesyonel bir rapor oluşturun."
    )
    st.markdown("---")

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    col1.markdown("### Details")
    complaint = col1.text_area("Complaint")
    method = col1.selectbox("Method", METHODS)

    col2.markdown("### Meta")
    customer = col2.text_input("Customer")
    subject = col2.text_input("Subject")
    part_code = col2.text_input("Part code")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### Benzer şikayetleri sorgula")
    col_chk1, col_chk2 = st.columns(2)
    opt_complaint = col_chk1.checkbox("Benzer Şikayet")
    opt_customer = col_chk1.checkbox("Müşteri")
    opt_part_code = col_chk2.checkbox("Parça Kodu")
    opt_subject = col_chk2.checkbox("Şikayet Konusu")

    current_year = datetime.now().year
    years = [str(y) for y in range(current_year, current_year - 20, -1)]
    year_label = "Tümü"
    year_option = st.selectbox("Yıl (opsiyonel)", [year_label] + years)

    if st.button("SORGULA", key="query"):
        filters = {}
        if opt_complaint:
            filters["complaint"] = complaint
        if opt_customer:
            filters["customer"] = customer
        if opt_part_code:
            filters["part_code"] = part_code
        if opt_subject:
            filters["subject"] = subject
        year = None if year_option == year_label else int(year_option)
        results = ExcelClaimsSearcher().search(filters, year=year)
        st.write(f"Sonuçlar: {len(results)}")
        for item in results:
            st.json(item)

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
        ComplaintStore().add_complaint(details)
        with st.spinner("Analyzing..."):
            analysis = analyzer.analyze(details, guideline)
        out_dir = Path("reports")
        out_dir.mkdir(parents=True, exist_ok=True)
        with open(out_dir / "LLM1.txt", "w", encoding="utf-8") as f:
            json.dump(analysis, f, ensure_ascii=False, indent=2)
        with st.spinner("Rapor değerlendiriliyor..."):
            reviewer = Review()
            if "full_text" in analysis:
                combined = analysis["full_text"]
            else:
                combined = "\n".join(v["response"] for v in analysis.values())
            full_report = reviewer.perform(
                combined,
                method=method,
                customer=customer,
                subject=subject,
                part_code=part_code,
                guideline_json=json.dumps(guideline, ensure_ascii=False),
            )
            analysis["full_report"] = {"response": full_report}
        with open(out_dir / "LLM2.txt", "w", encoding="utf-8") as f:
            json.dump(analysis, f, ensure_ascii=False, indent=2)

        complaint_info = {
            "customer": customer,
            "subject": subject,
            "part_code": part_code,
        }
        generator = ReportGenerator(manager)
        paths = generator.generate(analysis, complaint_info, "reports")

        st.subheader("Final Report")
        final_text = analysis.get("full_report", {}).get("response")
        if final_text:
            st.text_area("Report", final_text, height=300)
        else:
            st.write("No final report available.")

        pdf_name = Path(paths["pdf"]).name
        excel_name = Path(paths["excel"]).name

        col_dl1, col_dl2 = st.columns(2)
        with open(paths["pdf"], "rb") as pdf_file:
            col_dl1.download_button("Download PDF", pdf_file, file_name=pdf_name)
        with open(paths["excel"], "rb") as excel_file:
            col_dl2.download_button(
                "Download Excel",
                excel_file,
                file_name=excel_name,
            )



if __name__ == "__main__":
    main()
