"""Parser registration and lookup for dependency manifests."""

from __future__ import annotations

import fnmatch
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ParserFn = Callable[[Path], dict[str, Any]]
PredicateFn = Callable[[Path], bool]


@dataclass(slots=True, frozen=True)
class ParserRegistration:
    """Associates manifest metadata with a parser implementation."""

    parser: ParserFn
    names: tuple[str, ...] = ()
    suffixes: tuple[str, ...] = ()
    patterns: tuple[str, ...] = ()
    predicate: PredicateFn | None = None
    priority: int = 0

    def matches(self, path: Path) -> bool:
        if self.names and path.name in self.names:
            return True
        if self.suffixes and path.suffix.lower() in self.suffixes:
            return True
        if self.patterns and any(fnmatch.fnmatch(path.name, pattern) for pattern in self.patterns):
            return True
        if self.predicate and self.predicate(path):
            return True
        return False


@dataclass(slots=True)
class ManifestParserRegistry:
    """Lookup table for resolving the appropriate parser for a manifest."""

    registrations: list[ParserRegistration] = field(default_factory=list)
    fallback: ParserFn | None = None

    def register(self, registration: ParserRegistration) -> None:
        self.registrations.append(registration)
        self.registrations.sort(key=lambda item: item.priority, reverse=True)

    def resolve(self, path: Path) -> ParserFn:
        for registration in self.registrations:
            if registration.matches(path):
                return registration.parser
        if self.fallback is None:
            msg = f"No parser registered for manifest: {path}"
            raise LookupError(msg)
        return self.fallback
