"""FastAPI server exposing core Quality Reporter functionality."""

from __future__ import annotations

from typing import Any, Dict, Optional
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from GuideManager import GuideManager
from LLMAnalyzer import LLMAnalyzer
from Review import Review
from ReportGenerator import ReportGenerator
from ComplaintSearch import ComplaintStore, ExcelClaimsSearcher

REPORT_DIR = Path(__file__).resolve().parents[1] / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="Plasma QR API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/reports", StaticFiles(directory=str(REPORT_DIR)), name="reports")

# Shared component instances
_guide_manager = GuideManager()
analyzer = LLMAnalyzer()
reviewer = Review()
reporter = ReportGenerator(_guide_manager)
_store = ComplaintStore()
_excel_searcher = ExcelClaimsSearcher()


class AnalyzeBody(BaseModel):
    details: Dict[str, Any]
    guideline: Dict[str, Any]
    directives: str = ""


@app.post("/analyze")
def analyze(body: AnalyzeBody) -> Dict[str, Any]:
    """Return analysis results from ``LLMAnalyzer``."""
    return analyzer.analyze(body.details, body.guideline, body.directives)


class ReviewBody(BaseModel):
    text: str
    context: Dict[str, str] = {}


@app.post("/review")
def review(body: ReviewBody) -> Dict[str, str]:
    """Return reviewed text using ``Review``."""
    try:
        result = reviewer.perform(body.text, **body.context)
    except Exception as exc:  # pragma: no cover - network issues
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return {"result": result}


class ReportBody(BaseModel):
    analysis: Dict[str, Any]
    complaint_info: Dict[str, str]
    output_dir: str = "."


@app.post("/report")
def report(body: ReportBody) -> Dict[str, str]:
    """Generate PDF and Excel reports via ``ReportGenerator``."""
    paths = reporter.generate(body.analysis, body.complaint_info, REPORT_DIR)
    return {
        "pdf": f"/reports/{Path(paths['pdf']).name}",
        "excel": f"/reports/{Path(paths['excel']).name}",
    }


@app.get("/complaints")
def complaints(
    keyword: Optional[str] = None,
    complaint: Optional[str] = None,
    customer: Optional[str] = None,
    subject: Optional[str] = None,
    part_code: Optional[str] = None,
    year: Optional[int] = None,
    start_year: Optional[int] = None,
    end_year: Optional[int] = None,
) -> Dict[str, Any]:
    """Return complaint queries from JSON store and Excel file."""
    store_results = _store.search(keyword) if keyword else []
    filters: Dict[str, str] = {}
    if complaint:
        filters["complaint"] = complaint
    if customer:
        filters["customer"] = customer
    if subject:
        filters["subject"] = subject
    if part_code:
        filters["part_code"] = part_code
    excel_results = []
    if filters or year is not None or start_year is not None or end_year is not None:
        excel_results = _excel_searcher.search(
            filters,
            year,
            start_year=start_year,
            end_year=end_year,
        )
    return {"store": store_results, "excel": excel_results}


class ComplaintBody(BaseModel):
    complaint: str
    customer: str
    subject: str
    part_code: str


@app.post("/complaints")
def add_complaint(body: ComplaintBody) -> Dict[str, str]:
    """Persist a complaint in the JSON store."""
    _store.add_complaint(body.dict())
    return {"status": "ok"}


@app.get("/options/{field}")
def options(field: str) -> Dict[str, Any]:
    """Return unique option values for ``field`` from the Excel claims file."""
    return {"values": _excel_searcher.unique_values(field)}


@app.get("/guide/{method}")
def guide(method: str) -> Dict[str, Any]:
    """Return guideline data for ``method``."""
    return _guide_manager.get_format(method)


__all__ = ["app"]
