"""Dependency scanning utilities."""

from __future__ import annotations

from .parsers import build_parser_registry
from .registry import ManifestParserRegistry, ParserRegistration
from .scan import collect_dependency_info

__all__ = [
    "collect_dependency_info",
    "ManifestParserRegistry",
    "ParserRegistration",
    "build_parser_registry",
]
