"""Command-line interface for generating quality reports."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List, Optional
import logging

from GuideManager import GuideManager
from LLMAnalyzer import LLMAnalyzer
from ReportGenerator import ReportGenerator
from Review import Review


METHODS = ["8D", "5N1K", "A3", "DMAIC", "Ishikawa"]


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Return CLI arguments."""
    parser = argparse.ArgumentParser(description="Quality Reporter CLI")
    parser.add_argument("--complaint", "-c", help="Complaint text")
    parser.add_argument("--method", "-m", choices=METHODS, help="Reporting method")
    parser.add_argument("--output", "-o", default="reports", help="Output directory")
    parser.add_argument("--customer", help="Customer name")
    parser.add_argument("--subject", help="Complaint subject")
    parser.add_argument("--part-code", help="Related part code")
    return parser.parse_args(args)


def main(args: Optional[List[str]] = None) -> None:
    """Run the CLI application."""
    logging.basicConfig(level=logging.INFO)
    options = parse_args(args)

    complaint = options.complaint or input("Complaint text: ")
    method = options.method or input(f"Method ({', '.join(METHODS)}): ")
    customer = options.customer or input("Customer: ")
    subject = options.subject or input("Subject: ")
    part_code = options.part_code or input("Part code: ")

    manager = GuideManager()
    guideline = manager.get_format(method)

    analyzer = LLMAnalyzer()
    details = {
        "complaint": complaint,
        "customer": customer,
        "subject": subject,
        "part_code": part_code,
    }
    analysis = analyzer.analyze(details, guideline)

    out_dir = Path(options.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "LLM1.txt", "w", encoding="utf-8") as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)

    reviewer = Review()
    if method == "8D" and "full_text" in analysis:
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
    paths = generator.generate(analysis, complaint_info, options.output)

    print(json.dumps(analysis, indent=2, ensure_ascii=False))
    print(f"PDF report: {paths['pdf']}")
    print(f"Excel report: {paths['excel']}")


if __name__ == "__main__":
    main()
