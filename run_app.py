"""Convenience script to launch the Streamlit interface."""

from __future__ import annotations

from dotenv import load_dotenv

from UI import run_streamlit

load_dotenv()


def main() -> None:
    """Execute the Streamlit UI."""
    run_streamlit()


if __name__ == "__main__":
    main()
