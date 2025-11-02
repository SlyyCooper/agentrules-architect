"""Shared helpers for manifest parsers."""

from __future__ import annotations


def trim_excerpt(content: str, max_lines: int = 40) -> str:
    lines = content.splitlines()
    if len(lines) <= max_lines:
        return content
    snippet = "\n".join(lines[: max_lines - 1])
    return f"{snippet}\n…"
