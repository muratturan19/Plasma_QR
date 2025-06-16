"""User interface utilities."""

from typing import Optional

from .cli import main as run_cli


class UI:
    """Handles user interactions and supports quality-report methods."""

    def start(self) -> Optional[bool]:
        """Start the CLI."""
        run_cli()
        return None


__all__ = ["UI", "run_cli"]
