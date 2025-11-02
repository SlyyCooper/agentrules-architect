"""Parsers for Python dependency manifests."""

from __future__ import annotations

import ast
import configparser
import re
import tomllib
from pathlib import Path
from typing import Any

from ..registry import ManifestParserRegistry, ParserRegistration
from .helpers import trim_excerpt

RE_REQUIREMENT = re.compile(r"^\s*([^#=\s]+)(?:\s*==\s*([^\s#]+))?")
INSTALL_RE_LIST = re.compile(r"install_requires\s*=\s*(\[.*?\])", re.DOTALL)
EXTRAS_RE = re.compile(r"extras_require\s*=\s*(\{.*?\})", re.DOTALL)


def register_python_parsers(registry: ManifestParserRegistry) -> None:
    registry.register(
        ParserRegistration(
            parser=parse_pyproject_toml,
            names=("pyproject.toml",),
            priority=90,
        )
    )
    registry.register(
        ParserRegistration(
            parser=parse_pipfile,
            names=("Pipfile",),
            priority=90,
        )
    )
    registry.register(
        ParserRegistration(
            parser=parse_requirements_txt,
            suffixes=(".txt", ".in"),
            predicate=_requirements_predicate,
            priority=80,
        )
    )
    registry.register(
        ParserRegistration(
            parser=parse_setup_cfg,
            names=("setup.cfg",),
            priority=80,
        )
    )
    registry.register(
        ParserRegistration(
            parser=parse_setup_py,
            names=("setup.py",),
            priority=80,
        )
    )
    registry.register(
        ParserRegistration(
            parser=parse_environment_yaml,
            names=("environment.yml", "environment.yaml"),
            priority=70,
        )
    )


def parse_pyproject_toml(path: Path) -> dict[str, Any]:
    content = path.read_text(encoding="utf-8", errors="replace")
    data = tomllib.loads(content)

    dependencies: dict[str, Any] = {}
    project = data.get("project", {})
    if isinstance(project, dict):
        deps = project.get("dependencies")
        if isinstance(deps, list):
            dependencies["project"] = deps
        optional = project.get("optional-dependencies")
        if isinstance(optional, dict):
            dependencies["optional"] = optional
    poetry = data.get("tool", {}).get("poetry", {})
    if isinstance(poetry, dict):
        for key in ("dependencies", "dev-dependencies", "group"):
            section = poetry.get(key)
            if section:
                dependencies[f"poetry_{key}"] = section

    return {
        "type": "pyproject.toml",
        "manager": "python",
        "data": dependencies or None,
        "raw_excerpt": trim_excerpt(content),
    }


def parse_pipfile(path: Path) -> dict[str, Any]:
    content = path.read_text(encoding="utf-8", errors="replace")
    data = tomllib.loads(content)

    dependencies: dict[str, Any] = {}
    for key in ("packages", "dev-packages"):
        section = data.get(key)
        if isinstance(section, dict):
            dependencies[key] = section

    return {
        "type": "Pipfile",
        "manager": "pipenv",
        "data": dependencies or None,
        "raw_excerpt": trim_excerpt(content),
    }


def parse_requirements_txt(path: Path) -> dict[str, Any]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines(True)

    deps: list[dict[str, str]] = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        match = RE_REQUIREMENT.match(stripped)
        if match:
            name, version = match.groups()
            entry = {"name": name}
            if version:
                entry["version"] = version
            deps.append(entry)

    return {
        "type": "requirements_txt",
        "manager": "pip",
        "data": deps or None,
        "raw_excerpt": trim_excerpt("".join(lines)),
    }


def parse_environment_yaml(path: Path) -> dict[str, Any]:
    content = path.read_text(encoding="utf-8", errors="replace")
    return {
        "type": "environment_yaml",
        "manager": "conda",
        "data": None,
        "raw_excerpt": trim_excerpt(content),
    }


def parse_setup_cfg(path: Path) -> dict[str, Any]:
    content = path.read_text(encoding="utf-8", errors="replace")

    parser = configparser.ConfigParser()
    parser.read_string(content)

    data: dict[str, Any] = {}
    if parser.has_section("metadata"):
        metadata = dict(parser.items("metadata"))
        if metadata:
            data["metadata"] = metadata
    if parser.has_section("options"):
        options = dict(parser.items("options"))
        if options:
            install_raw = options.get("install_requires")
            if install_raw:
                items = [item.strip() for item in install_raw.splitlines() if item.strip()]
                data["install_requires"] = items
            extras_raw = options.get("extras_require")
            if extras_raw:
                data["extras_require"] = extras_raw
    for section in parser.sections():
        if section.startswith("options.extras_require"):
            extras = dict(parser.items(section))
            if extras:
                data.setdefault("extras_require_sections", {})[section] = extras

    return {
        "type": "setup_cfg",
        "manager": "python",
        "data": data or None,
        "raw_excerpt": trim_excerpt(content),
    }


def parse_setup_py(path: Path) -> dict[str, Any]:
    content = path.read_text(encoding="utf-8", errors="replace")
    data: dict[str, Any] = {}

    def _extract(pattern: re.Pattern[str]) -> Any | None:
        match = pattern.search(content)
        if not match:
            return None
        value = match.group(1)
        try:
            return ast.literal_eval(value)
        except (ValueError, SyntaxError):
            return value

    install_requires = _extract(INSTALL_RE_LIST)
    if install_requires:
        data["install_requires"] = install_requires

    extras_require = _extract(EXTRAS_RE)
    if extras_require:
        data["extras_require"] = extras_require

    return {
        "type": "setup_py",
        "manager": "python",
        "data": data or None,
        "raw_excerpt": trim_excerpt(content),
    }


def _requirements_predicate(path: Path) -> bool:
    return "requirements" in path.name.lower()
