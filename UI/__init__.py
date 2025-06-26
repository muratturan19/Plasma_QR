"""User interface utilities."""

from typing import List, Optional
import subprocess
import sys
import tempfile
from pathlib import Path
from importlib import resources


def run_streamlit() -> None:
    """Launch the Streamlit application."""

    from . import streamlit_app

    script = Path(streamlit_app.__file__).resolve()
    frozen = getattr(sys, "frozen", False)

    if frozen or not script.exists():
        tmp_path = Path(tempfile.gettempdir()) / "streamlit_app.py"
        with resources.files("UI").joinpath("streamlit_app.py").open("rb") as src, \
                open(tmp_path, "wb") as dst:
            dst.write(src.read())
        script = tmp_path

    if frozen:
        sys.argv = ["streamlit", "run", str(script)]
        import streamlit.web.cli as stcli
        stcli.main()
    else:
        subprocess.run(["streamlit", "run", str(script)], check=True)


def run_cli(args: Optional[List[str]] = None) -> None:
    """Run the CLI application with optional ``args``.

    The CLI module is imported lazily to avoid the overhead at package import
    time.
    """
    from .cli import main

    main(args)


class UI:
    """Handles user interactions and supports quality-report methods."""

    def start(self) -> None:
        """Start the CLI."""
        run_cli()


__all__ = ["UI", "run_cli", "run_streamlit"]
