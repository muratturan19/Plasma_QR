"""Entry point to launch the FastAPI API server."""

from __future__ import annotations

from dotenv import load_dotenv
import uvicorn

from api.logging_config import configure_logging

from api import app


def main() -> None:
    """Start the API server."""
    configure_logging()
    load_dotenv()
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
