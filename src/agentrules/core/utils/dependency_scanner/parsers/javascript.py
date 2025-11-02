"""Parsers for JavaScript and TypeScript ecosystems."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..registry import ManifestParserRegistry, ParserRegistration
from .helpers import trim_excerpt


def register_javascript_parsers(registry: ManifestParserRegistry) -> None:
    registry.register(
        ParserRegistration(
            parser=parse_package_json,
            names=("package.json",),
            priority=100,
        )
    )


def parse_package_json(path: Path) -> dict[str, Any]:
    content = path.read_text(encoding="utf-8", errors="replace")
    payload = json.loads(content)

    dependencies: dict[str, Any] = {}
    for field in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
        section = payload.get(field)
        if isinstance(section, dict) and section:
            dependencies[field] = dict(section)

    return {
        "type": "package_json",
        "manager": "npm",
        "data": dependencies or None,
        "raw_excerpt": trim_excerpt(content),
    }
