"""Parsers for Elixir dependency manifests."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from ..registry import ManifestParserRegistry, ParserRegistration
from .helpers import trim_excerpt

MIX_DEP_RE = re.compile(r"{\s*:([^,\s]+)\s*,\s*\"([^\"]+)\"")


def register_elixir_parsers(registry: ManifestParserRegistry) -> None:
    registry.register(
        ParserRegistration(
            parser=parse_mix_exs,
            names=("mix.exs",),
            priority=60,
        )
    )


def parse_mix_exs(path: Path) -> dict[str, Any]:
    content = path.read_text(encoding="utf-8", errors="replace")

    deps: list[dict[str, str]] = []
    for match in MIX_DEP_RE.finditer(content):
        name, version = match.groups()
        deps.append({"name": name, "version": version})

    return {
        "type": "mix_exs",
        "manager": "mix",
        "data": {"dependencies": deps} if deps else None,
        "raw_excerpt": trim_excerpt(content),
    }
