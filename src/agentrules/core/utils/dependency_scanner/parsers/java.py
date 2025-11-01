"""Parsers for Java and Kotlin dependency manifests."""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from ..registry import ManifestParserRegistry, ParserRegistration
from .helpers import trim_excerpt

GRADLE_DEP_RE = re.compile(
    r"^\s*(api|implementation|compileOnly|runtimeOnly|testImplementation|testCompileOnly)\s+['\"]([^'\"]+)['\"]"
)


def register_java_parsers(registry: ManifestParserRegistry) -> None:
    registry.register(
        ParserRegistration(
            parser=parse_pom_xml,
            names=("pom.xml",),
            priority=80,
        )
    )
    registry.register(
        ParserRegistration(
            parser=parse_gradle,
            names=("build.gradle", "build.gradle.kts"),
            priority=80,
        )
    )


def parse_pom_xml(path: Path) -> dict[str, Any]:
    tree = ET.parse(path)
    root = tree.getroot()
    dependencies: list[dict[str, Any]] = []

    for dep in root.findall(".//{*}dependency"):
        group = dep.findtext("{*}groupId")
        artifact = dep.findtext("{*}artifactId")
        version = dep.findtext("{*}version")
        scope = dep.findtext("{*}scope")
        entry = {"groupId": group, "artifactId": artifact}
        if version:
            entry["version"] = version
        if scope:
            entry["scope"] = scope
        dependencies.append(entry)

    content = path.read_text(encoding="utf-8", errors="replace")

    return {
        "type": "pom_xml",
        "manager": "maven",
        "data": {"dependencies": dependencies} if dependencies else None,
        "raw_excerpt": trim_excerpt(content),
    }


def parse_gradle(path: Path) -> dict[str, Any]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines(True)

    deps: list[dict[str, str]] = []
    for line in lines:
        match = GRADLE_DEP_RE.match(line)
        if not match:
            continue
        configuration, notation = match.groups()
        deps.append({"configuration": configuration, "notation": notation})

    return {
        "type": path.name,
        "manager": "gradle",
        "data": {"dependencies": deps} if deps else None,
        "raw_excerpt": trim_excerpt("".join(lines)),
    }
