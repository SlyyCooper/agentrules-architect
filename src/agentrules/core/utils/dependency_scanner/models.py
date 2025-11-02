"""Domain models for dependency manifest scanning."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class ManifestRecord:
    """Structured representation of a dependency manifest."""

    path: Path
    type: str
    manager: str | None
    data: Any
    raw_excerpt: str | None
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path.as_posix(),
            "type": self.type,
            "manager": self.manager,
            "data": self.data,
            "raw_excerpt": self.raw_excerpt,
            "error": self.error,
        }
