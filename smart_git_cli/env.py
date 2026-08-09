"""Minimal .env loader with no external dependencies."""

from __future__ import annotations

import os
from pathlib import Path


def load_dotenv(path: str | os.PathLike[str] | None = None) -> None:
    """Load KEY=VALUE lines from a .env file into os.environ.

    Existing environment variables always take precedence. Blank lines and
    lines starting with ``#`` are ignored. The value is used verbatim, so it
    must not contain unquoted spaces.
    """
    env_file = Path(path) if path else Path(".env")
    if not env_file.is_file():
        return

    for raw in env_file.read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip("\"'")
        if key and key not in os.environ:
            os.environ[key] = value