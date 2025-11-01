"""Parsers for Swift Package Manager manifests."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from ..registry import ManifestParserRegistry, ParserRegistration
from .helpers import trim_excerpt

SWIFT_PKG_RE = re.compile(
    r"\.package\s*\(\s*name:\s*\"([^\"']+)\".*?(?:from|exact):\s*\"([^\"']+)\"",
    re.DOTALL,
)


def register_swift_parsers(registry: ManifestParserRegistry) -> None:
    registry.register(
        ParserRegistration(
            parser=parse_package_swift,
            names=("Package.swift",),
            priority=60,
        )
    )


def parse_package_swift(path: Path) -> dict[str, Any]:
    content = path.read_text(encoding="utf-8", errors="replace")

    deps: list[dict[str, str]] = []
    for match in SWIFT_PKG_RE.finditer(content):
        name, version = match.groups()
        deps.append({"name": name, "version": version})

    return {
        "type": "Package.swift",
        "manager": "swiftpm",
        "data": {"dependencies": deps} if deps else None,
        "raw_excerpt": trim_excerpt(content),
    }
