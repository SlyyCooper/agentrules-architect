"""Parsers for Go dependency manifests."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..registry import ManifestParserRegistry, ParserRegistration
from .helpers import trim_excerpt


def register_go_parsers(registry: ManifestParserRegistry) -> None:
    registry.register(
        ParserRegistration(
            parser=parse_go_mod,
            names=("go.mod",),
            priority=80,
        )
    )


def parse_go_mod(path: Path) -> dict[str, Any]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines(True)

    module_name: str | None = None
    go_version: str | None = None
    deps: list[dict[str, str]] = []

    in_require_block = False
    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith("//"):
            continue
        if line.startswith("module "):
            module_name = line.split(maxsplit=1)[1]
            continue
        if line.startswith("go "):
            go_version = line.split(maxsplit=1)[1]
            continue
        if line.startswith("require ("):
            in_require_block = True
            continue
        if in_require_block and line == ")":
            in_require_block = False
            continue
        if in_require_block:
            parts = line.split()
            if len(parts) >= 2:
                deps.append({"module": parts[0], "version": parts[1]})
            continue
        if line.startswith("require "):
            parts = line.split()
            if len(parts) >= 3:
                deps.append({"module": parts[1], "version": parts[2]})

    data: dict[str, Any] = {}
    if module_name:
        data["module"] = module_name
    if go_version:
        data["go"] = go_version
    if deps:
        data["dependencies"] = deps

    return {
        "type": "go_mod",
        "manager": "go",
        "data": data or None,
        "raw_excerpt": trim_excerpt("".join(lines)),
    }
