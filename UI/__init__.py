"""User interface utilities."""

from typing import List, Optional


def run_streamlit() -> None:
    """Start the Streamlit UI."""
    from . import streamlit_app
    from streamlit.web import bootstrap

    # ``bootstrap.run`` expects the path to the Streamlit application
    # rather than the function object itself. Passing the path prevents
    # ``TypeError`` issues when ``bootstrap`` tries to modify ``sys.path``.
    # ``bootstrap.run`` expects the path to the Streamlit application and a
    # boolean ``is_hello`` flag in recent Streamlit versions. Passing ``False``
    # avoids ``TypeError`` issues when the underlying implementation assumes a
    # boolean value.
    bootstrap.run(streamlit_app.__file__, False, [], [])


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
