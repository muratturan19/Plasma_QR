"""Utilities for configuring application logging."""

from __future__ import annotations

import logging
import os

__all__ = ["configure_logging"]


def configure_logging() -> None:
    """Initialize basic logging if no handlers are present."""
    if not logging.getLogger().handlers:
        level_name = os.getenv("LOG_LEVEL", "INFO").upper()
        level = getattr(logging, level_name, logging.INFO)
        logging.basicConfig(level=level)

