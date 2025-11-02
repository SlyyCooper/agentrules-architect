"""Parsers for Dart and Flutter dependency manifests."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..registry import ManifestParserRegistry, ParserRegistration
from .helpers import trim_excerpt


def register_dart_parsers(registry: ManifestParserRegistry) -> None:
    registry.register(
        ParserRegistration(
            parser=parse_pubspec_yaml,
            names=("pubspec.yaml",),
            priority=60,
        )
    )


def parse_pubspec_yaml(path: Path) -> dict[str, Any]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines(True)

    sections = ("dependencies", "dev_dependencies")
    data: dict[str, dict[str, str]] = {}
    current_section: str | None = None

    for raw_line in lines:
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.endswith(":"):
            section = stripped[:-1]
            if section in sections:
                current_section = section
                data.setdefault(section, {})
            continue
        if current_section and ":" in stripped:
            name, version = stripped.split(":", maxsplit=1)
            data[current_section][name.strip()] = version.strip()

    return {
        "type": "pubspec_yaml",
        "manager": "dart",
        "data": data or None,
        "raw_excerpt": trim_excerpt("".join(lines)),
    }
