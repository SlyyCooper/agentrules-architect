"""Parsers for .NET dependency manifests."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from ..registry import ManifestParserRegistry, ParserRegistration
from .helpers import trim_excerpt


def register_dotnet_parsers(registry: ManifestParserRegistry) -> None:
    registry.register(
        ParserRegistration(
            parser=parse_project_file,
            patterns=("*.csproj", "*.fsproj", "*.vbproj"),
            priority=70,
        )
    )


def parse_project_file(path: Path) -> dict[str, Any]:
    tree = ET.parse(path)
    root = tree.getroot()
    dependencies: list[dict[str, str]] = []
    for pkg in root.findall(".//{*}PackageReference"):
        include = pkg.attrib.get("Include")
        version = pkg.attrib.get("Version") or pkg.findtext("{*}Version")
        if include:
            entry = {"package": include}
            if version:
                entry["version"] = version
            dependencies.append(entry)

    content = path.read_text(encoding="utf-8", errors="replace")

    return {
        "type": path.suffix.lstrip(".") + "_project",
        "manager": ".net",
        "data": {"dependencies": dependencies} if dependencies else None,
        "raw_excerpt": trim_excerpt(content),
    }
