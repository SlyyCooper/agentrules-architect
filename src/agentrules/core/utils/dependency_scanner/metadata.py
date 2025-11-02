"""Metadata helpers for dependency manifest scanning."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from pathlib import Path

from .models import ManifestRecord


def infer_manifest_type(path: Path) -> str:
    """Best-effort manifest type inference based on file metadata."""
    if path.name == "package.json":
        return "package_json"
    if path.suffix == ".toml":
        return path.name
    if "requirements" in path.name.lower():
        return "requirements_txt"
    return path.name


def build_summary(records: Iterable[ManifestRecord]) -> dict[str, list[str]]:
    """Produce a manager -> manifest path summary."""
    summary: dict[str, list[str]] = defaultdict(list)
    for record in records:
        manager = record.manager or "unknown"
        summary[manager].append(record.path.as_posix())
    return dict(summary)
