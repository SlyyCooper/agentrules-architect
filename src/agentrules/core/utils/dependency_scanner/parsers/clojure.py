"""Parsers for Clojure dependency manifests."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from ..registry import ManifestParserRegistry, ParserRegistration
from .helpers import trim_excerpt

DEPS_EDN_RE = re.compile(r"([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)\s+\{\s*:mvn/version\s+\"([^\"]+)\"")
PROJECT_CLJ_RE = re.compile(r"\[([\w\.-]+/[\w\.-]+)\s+\"([^\"]+)\"")


def register_clojure_parsers(registry: ManifestParserRegistry) -> None:
    registry.register(
        ParserRegistration(
            parser=parse_deps_edn,
            names=("deps.edn",),
            priority=60,
        )
    )
    registry.register(
        ParserRegistration(
            parser=parse_project_clj,
            names=("project.clj",),
            priority=60,
        )
    )


def parse_deps_edn(path: Path) -> dict[str, Any]:
    content = path.read_text(encoding="utf-8", errors="replace")

    deps = []
    for match in DEPS_EDN_RE.finditer(content):
        name, version = match.groups()
        deps.append({"name": name, "version": version})

    return {
        "type": "deps_edn",
        "manager": "clojure",
        "data": {"dependencies": deps} if deps else None,
        "raw_excerpt": trim_excerpt(content),
    }


def parse_project_clj(path: Path) -> dict[str, Any]:
    content = path.read_text(encoding="utf-8", errors="replace")

    deps = []
    for match in PROJECT_CLJ_RE.finditer(content):
        name, version = match.groups()
        deps.append({"name": name, "version": version})

    return {
        "type": "project_clj",
        "manager": "leiningen",
        "data": {"dependencies": deps} if deps else None,
        "raw_excerpt": trim_excerpt(content),
    }
