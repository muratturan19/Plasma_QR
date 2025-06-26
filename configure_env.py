"""Interactive helper to create or update the `.env` file."""

from __future__ import annotations

from pathlib import Path
from dotenv import set_key


ENV_PATH = Path(".env")


def main() -> None:
    """Prompt for configuration values and store them in ``.env``."""
    api_key = input("OpenAI API key: ").strip()
    claims_path = input("Path to claims.xlsx: ").strip()

    ENV_PATH.touch(exist_ok=True)
    set_key(str(ENV_PATH), "OPENAI_API_KEY", api_key)
    set_key(str(ENV_PATH), "CLAIMS_FILE_PATH", claims_path)
    print(f"Configuration written to {ENV_PATH}")


if __name__ == "__main__":
    main()
