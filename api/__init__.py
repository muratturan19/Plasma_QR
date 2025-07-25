"""Expose the FastAPI application and route handlers for the API.

The module creates the :class:`FastAPI` instance and defines HTTP endpoints
used by the Quality Reporter service.
"""

from __future__ import annotations

from typing import Any, Dict, Optional
from pathlib import Path
import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from GuideManager import GuideManager
from LLMAnalyzer import LLMAnalyzer
from Review import Review
from ReportGenerator import ReportGenerator
from ComplaintSearch import ComplaintStore, ExcelClaimsSearcher, normalize_text
from EightDScanner import EightDScanner

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

logger = logging.getLogger(__name__)

# Map common query aliases to Excel header names
ALIAS_TO_HEADER = {
    normalize_text("customer"): "Müşteri Adı",
    normalize_text("musteri"): "Müşteri Adı",
    normalize_text("müşteri adı"): "Müşteri Adı",
    normalize_text("musteri adi"): "Müşteri Adı",
    normalize_text("subject"): "Hata Tanımı - Kök Neden",
    normalize_text("konu"): "Konu",
    normalize_text("hata tanımı - kök neden"): "Hata Tanımı - Kök Neden",
    normalize_text("part_code"): "Parça Numarası",
    normalize_text("parca kodu"): "Parça Numarası",
    normalize_text("parça kodu"): "Parça Numarası",
    normalize_text("parça numarası"): "Parça Numarası",
}

# Shared component instances
_guide_manager = GuideManager()
analyzer = LLMAnalyzer()
reviewer = Review()
reporter = ReportGenerator(_guide_manager)
_store = ComplaintStore()
_excel_searcher = ExcelClaimsSearcher()
_scanner = EightDScanner(Path(__file__).resolve().parents[1] / "eight_d_reports")


class AnalyzeBody(BaseModel):
    details: Dict[str, Any]
    guideline: Dict[str, Any]
    directives: str = ""
    language: str = "Türkçe"


@app.post("/analyze")
def analyze(body: AnalyzeBody) -> Dict[str, Any]:
    """Return analysis results from ``LLMAnalyzer``."""
    logger.info("Analyze request body: %s", body.dict())
    try:
        result = analyzer.analyze(
            body.details,
            body.guideline,
            body.directives,
            body.language,
        )
    except Exception as exc:  # pragma: no cover - unexpected failure
        logger.exception("Analyze failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    logger.info("Analyze result: %s", result)
    return result


class ReviewBody(BaseModel):
    text: str
    context: Dict[str, str] = {}


@app.post("/review")
def review(body: ReviewBody) -> Dict[str, str]:
    """Return reviewed text using ``Review``."""
    logger.info("Review request body: %s", body.dict())
    try:
        result = reviewer.perform(body.text, **body.context)
    except Exception as exc:  # pragma: no cover - network issues
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    logger.info("Review result: %s", result)
    return {"result": result}


class ReportBody(BaseModel):
    analysis: Dict[str, Any]
    complaint_info: Dict[str, str]
    output_dir: str = "."


@app.post("/report")
def report(body: ReportBody) -> Dict[str, str]:
    """Generate PDF and Excel reports via ``ReportGenerator``."""
    logger.info("Report request body: %s", body.dict())
    try:
        paths = reporter.generate(body.analysis, body.complaint_info, REPORT_DIR)
    except Exception as exc:  # pragma: no cover - unexpected failure
        logger.exception("Report generation failed")
        raise HTTPException(status_code=500, detail="Report generation failed") from exc
    result = {
        "pdf": f"/reports/{Path(paths['pdf']).name}",
        "excel": f"/reports/{Path(paths['excel']).name}",
    }
    logger.info("Report result: %s", result)
    return result


@app.get("/complaints")
def complaints(
    request: Request,
    year: Optional[int] = None,
    start_year: Optional[int] = None,
    end_year: Optional[int] = None,
) -> Dict[str, Any]:
    """Return complaint queries from JSON store and Excel file."""
    logger.info("Complaints query params: %s", request.query_params)
    keyword = request.query_params.get("keyword")
    store_results = _store.search(keyword) if keyword else []
    known = {"keyword", "year", "start_year", "end_year"}
    filters: Dict[str, str] = {
        k: v for k, v in request.query_params.items() if k not in known
    }
    normalized: Dict[str, str] = {}
    for key, val in filters.items():
        norm = normalize_text(key)
        mapped = ALIAS_TO_HEADER.get(norm, key)
        if isinstance(val, str):
            val = val.strip()
        normalized[mapped] = val
    excel_results = []
    if normalized or year is not None or start_year is not None or end_year is not None:
        excel_results = _excel_searcher.search(
            normalized,
            year,
            start_year=start_year,
            end_year=end_year,
        )
    result = {"store": store_results, "excel": excel_results}
    logger.info("Complaints result: %s", result)
    return result


class ComplaintBody(BaseModel):
    complaint: str
    customer: str
    subject: str
    part_code: str


@app.post("/complaints")
def add_complaint(body: ComplaintBody) -> Dict[str, str]:
    """Persist a complaint in the JSON store."""
    logger.info("Add complaint body: %s", body.dict())
    _store.add_complaint(body.dict())
    result = {"status": "ok"}
    logger.info("Add complaint result: %s", result)
    return result


@app.get("/options/{field}")
def options(field: str, request: Request) -> Dict[str, Any]:
    """Return unique option values for ``field`` from the Excel claims file."""
    logger.info("Options query params: %s", request.query_params)
    mapped_field = ALIAS_TO_HEADER.get(normalize_text(field), field)
    result = {"values": _excel_searcher.unique_values(mapped_field)}
    logger.info("Options result: %s", result)
    return result


@app.get("/guide/{method}")
def guide(method: str, request: Request) -> Dict[str, Any]:
    """Return guideline data for ``method``."""
    logger.info("Guide method: %s", method)
    result = _guide_manager.get_format(method)
    logger.debug("Guide result: %s", result)
    return result


@app.post("/scan_8d")
def scan_8d() -> Dict[str, Any]:
    """Scan 8D Excel reports and store rows in SQLite."""
    logger.info("Scanning 8D reports")
    try:
        count = _scanner.scan()
    except Exception as exc:  # pragma: no cover - unexpected failure
        logger.exception("Scan failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    result = {"status": "ok", "count": count}
    logger.info("Scan result: %s", result)
    return result


__all__ = ["app", "scan_8d"]
