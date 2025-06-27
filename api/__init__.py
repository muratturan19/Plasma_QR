"""FastAPI server exposing core Quality Reporter functionality."""

from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from GuideManager import GuideManager
from LLMAnalyzer import LLMAnalyzer
from Review import Review
from ReportGenerator import ReportGenerator
from ComplaintSearch import ComplaintStore, ExcelClaimsSearcher

app = FastAPI(title="Plasma QR API")

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
    return reporter.generate(body.analysis, body.complaint_info, body.output_dir)


@app.get("/complaints")
def complaints(
    keyword: Optional[str] = None,
    complaint: Optional[str] = None,
    customer: Optional[str] = None,
    subject: Optional[str] = None,
    part_code: Optional[str] = None,
    year: Optional[int] = None,
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
    excel_results = _excel_searcher.search(filters, year) if filters or year else []
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
