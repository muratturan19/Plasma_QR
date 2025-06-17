"""Convenience script to launch the Streamlit interface."""

from __future__ import annotations

from dotenv import load_dotenv

from UI import run_streamlit

def main() -> None:
    """Execute the Streamlit UI."""
    load_dotenv()
    run_streamlit()


if __name__ == "__main__":
    main()
