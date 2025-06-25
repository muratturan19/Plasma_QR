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
            background: linear-gradient(#ffffff, #f0f0f0);
            color: #333333;
        }
        h1, h2, h3 {
            font-weight: 700;
            color: #2E86C1;
        }
        h1 {
            font-size: 3rem;
        }
        .card {
            background-color: #ffffff;
            padding: 1rem;
            border-radius: 12px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-bottom: 1rem;
        }
        input, textarea, select {
            padding: 0.75rem;
            border-radius: 8px;
            font-size: 1rem;
            width: 100%;
        }
        .stButton>button {
            background-color: #2E86C1;
            color: #ffffff;
            padding: 0.75rem 1.25rem;
            border-radius: 8px;
            font-size: 1rem;
            width: 100%;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #1A5276;
            color: #ffffff;
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
        st.sidebar.image(str(logo_path), use_column_width=True)
    st.markdown(
        "<h1 style='text-align: center; font-size: 64px;'>PLASMA PLASTİK</h1>",
        unsafe_allow_html=True,
    )
    st.sidebar.markdown("### Search Complaints")
    search_term = st.sidebar.text_input("Keyword")
    if st.sidebar.button("Search"):
        with st.spinner("Searching complaints..."):
            results = ComplaintStore().search(search_term)
        if not results:
            st.sidebar.markdown("Sonuç bulunamadı")
        else:
            st.sidebar.write(f"Results: {len(results)}")
            for item in results:
                card = (
                    f"<div class='card'>"
                    f"<strong>{item.get('complaint', '')}</strong><br>"
                    f"<em>{item.get('subject', '')}</em><br>"
                    f"<span style='font-size: 0.85em'>"
                    f"{item.get('customer', '')} - {item.get('date', '')}"
                    f"</span></div>"
                )
                st.sidebar.markdown(card, unsafe_allow_html=True)
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
        with st.spinner("Searching records..."):
            results = ExcelClaimsSearcher().search(filters, year=year)
        if not results:
            st.markdown("Sonuç bulunamadı")
        else:
            st.write(f"Sonuçlar: {len(results)}")
            for item in results:
                card = (
                    f"<div class='card'>"
                    f"<strong>{item.get('complaint', '')}</strong><br>"
                    f"<em>{item.get('subject', '')}</em><br>"
                    f"<span style='font-size: 0.85em'>"
                    f"{item.get('customer', '')} - {item.get('date', '')}"
                    f"</span></div>"
                )
                st.markdown(card, unsafe_allow_html=True)

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
