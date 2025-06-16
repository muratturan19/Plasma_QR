"""Command-line interface for generating quality reports."""

from __future__ import annotations

import argparse
import json
from typing import List, Optional

from GuideManager import GuideManager
from LLMAnalyzer import LLMAnalyzer
from ReportGenerator import ReportGenerator


METHODS = ["8D", "5N1K", "A3", "DMAIC", "Ishikawa"]


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Return CLI arguments."""
    parser = argparse.ArgumentParser(description="Quality Reporter CLI")
    parser.add_argument("--complaint", "-c", help="Complaint text")
    parser.add_argument("--method", "-m", choices=METHODS, help="Reporting method")
    parser.add_argument("--output", "-o", default="reports", help="Output directory")
    return parser.parse_args(args)


def main(args: Optional[List[str]] = None) -> None:
    """Run the CLI application."""
    options = parse_args(args)

    complaint = options.complaint or input("Complaint text: ")
    method = options.method or input(f"Method ({', '.join(METHODS)}): ")

    manager = GuideManager()
    guideline = manager.get_format(method)

    analyzer = LLMAnalyzer()
    analysis = analyzer.analyze(complaint, guideline)

    generator = ReportGenerator(manager)
    paths = generator.generate(analysis, options.output)

    print(json.dumps(analysis, indent=2, ensure_ascii=False))
    print(f"PDF report: {paths['pdf']}")
    print(f"Excel report: {paths['excel']}")


if __name__ == "__main__":
    main()
