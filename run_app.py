"""Convenience script to launch the Streamlit interface."""

from __future__ import annotations

from dotenv import load_dotenv
import logging

from UI import run_streamlit

load_dotenv()

def main() -> None:
    """Execute the Streamlit UI."""
    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    run_streamlit()


if __name__ == "__main__":
    main()
