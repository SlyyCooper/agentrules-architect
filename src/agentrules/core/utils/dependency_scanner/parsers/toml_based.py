"""Parsers for TOML-based dependency manifests."""

from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any

from ..registry import ManifestParserRegistry, ParserRegistration
from .helpers import trim_excerpt


def register_toml_parsers(registry: ManifestParserRegistry) -> None:
    registry.register(
        ParserRegistration(
            parser=parse_cargo_toml,
            names=("Cargo.toml",),
            priority=80,
        )
    )
    registry.register(
        ParserRegistration(
            parser=parse_project_toml,
            names=("Project.toml",),
            priority=70,
        )
    )
    registry.register(
        ParserRegistration(
            parser=parse_generic_toml,
            suffixes=(".toml",),
            priority=10,
        )
    )


def parse_cargo_toml(path: Path) -> dict[str, Any]:
    content = path.read_text(encoding="utf-8", errors="replace")
    data = tomllib.loads(content)

    dependencies: dict[str, Any] = {}
    for key in ("dependencies", "dev-dependencies", "build-dependencies"):
        section = data.get(key)
        if isinstance(section, dict) and section:
            dependencies[key] = section
    target = data.get("target")
    if isinstance(target, dict) and target:
        dependencies["target"] = target

    return {
        "type": "Cargo.toml",
        "manager": "cargo",
        "data": dependencies or None,
        "raw_excerpt": trim_excerpt(content),
    }


def parse_project_toml(path: Path) -> dict[str, Any]:
    content = path.read_text(encoding="utf-8", errors="replace")
    data = tomllib.loads(content)

    dependencies: dict[str, Any] = {}
    project = data.get("project")
    if isinstance(project, dict):
        dependencies["project"] = project

    return {
        "type": "Project.toml",
        "manager": "julia",
        "data": dependencies or None,
        "raw_excerpt": trim_excerpt(content),
    }


def parse_generic_toml(path: Path) -> dict[str, Any]:
    content = path.read_text(encoding="utf-8", errors="replace")
    data = tomllib.loads(content)

    return {
        "type": path.name,
        "manager": None,
        "data": data or None,
        "raw_excerpt": trim_excerpt(content),
    }
