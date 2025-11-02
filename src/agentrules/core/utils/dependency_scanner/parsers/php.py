"""Parsers for PHP dependency manifests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..registry import ManifestParserRegistry, ParserRegistration
from .helpers import trim_excerpt


def register_php_parsers(registry: ManifestParserRegistry) -> None:
    registry.register(
        ParserRegistration(
            parser=parse_composer_json,
            names=("composer.json",),
            priority=90,
        )
    )


def parse_composer_json(path: Path) -> dict[str, Any]:
    content = path.read_text(encoding="utf-8", errors="replace")
    payload = json.loads(content)

    dependencies: dict[str, Any] = {}
    for field in ("require", "require-dev"):
        section = payload.get(field)
        if isinstance(section, dict) and section:
            dependencies[field] = dict(section)

    return {
        "type": "composer_json",
        "manager": "composer",
        "data": dependencies or None,
        "raw_excerpt": trim_excerpt(content),
    }
