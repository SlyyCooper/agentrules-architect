"""Generic fallback parsers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .helpers import trim_excerpt


def parse_generic_text(path: Path) -> dict[str, Any]:
    content = path.read_text(encoding="utf-8", errors="replace")
    return {
        "type": path.name,
        "manager": None,
        "data": None,
        "raw_excerpt": trim_excerpt(content),
    }
