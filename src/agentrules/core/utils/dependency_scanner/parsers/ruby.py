"""Parsers for Ruby dependency manifests."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from ..registry import ManifestParserRegistry, ParserRegistration
from .helpers import trim_excerpt

GEMFILE_RE = re.compile(r"^\s*gem\s+['\"]([^'\"]+)['\"](?:,\s*['\"]([^'\"]+)['\"])?")
GEMSPEC_RE = re.compile(
    r"add_(?:runtime_)?dependency\s*\(\s*['\"]([^'\"]+)['\"](?:,\s*['\"]([^'\"]+)['\"])?"
)


def register_ruby_parsers(registry: ManifestParserRegistry) -> None:
    registry.register(
        ParserRegistration(
            parser=parse_gemfile,
            names=("Gemfile",),
            priority=70,
        )
    )
    registry.register(
        ParserRegistration(
            parser=parse_gemspec,
            patterns=("*.gemspec",),
            priority=70,
        )
    )


def parse_gemfile(path: Path) -> dict[str, Any]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines(True)

    deps: list[dict[str, str]] = []
    for line in lines:
        match = GEMFILE_RE.match(line)
        if match:
            name, version = match.groups()
            entry = {"name": name}
            if version:
                entry["version"] = version
            deps.append(entry)

    return {
        "type": "Gemfile",
        "manager": "bundler",
        "data": {"dependencies": deps} if deps else None,
        "raw_excerpt": trim_excerpt("".join(lines)),
    }


def parse_gemspec(path: Path) -> dict[str, Any]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines(True)

    deps: list[dict[str, str]] = []
    for line in lines:
        match = GEMSPEC_RE.search(line)
        if match:
            name, version = match.groups()
            entry = {"name": name}
            if version:
                entry["version"] = version
            deps.append(entry)

    return {
        "type": "gemspec",
        "manager": "bundler",
        "data": {"dependencies": deps} if deps else None,
        "raw_excerpt": trim_excerpt("".join(lines)),
    }
