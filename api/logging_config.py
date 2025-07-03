"""Utilities for configuring application logging."""

from __future__ import annotations

import logging
import os

__all__ = ["configure_logging"]


def configure_logging() -> None:
    """Initialize basic logging if no user handlers are present."""
    root = logging.getLogger()
    ignore = {"LogCaptureHandler", "_LiveLoggingNullHandler", "_FileHandler"}
    has_real = any(h.__class__.__name__ not in ignore for h in root.handlers)
    if not has_real:
        level_name = os.getenv("LOG_LEVEL", "INFO").upper()
        level = getattr(logging, level_name, logging.INFO)
        logging.basicConfig(level=level)

