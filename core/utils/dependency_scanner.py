"""Utilities for collecting dependency manifest data from a project tree."""

from __future__ import annotations

import ast
import configparser
import fnmatch
import json
import re
import tomllib
import xml.etree.ElementTree as ET
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from pathspec import PathSpec

from config.exclusions import EXCLUDED_DIRS, EXCLUDED_EXTENSIONS, EXCLUDED_FILES
from core.utils.file_system.file_retriever import list_files

# Files we explicitly want to inspect even though some are excluded globally.
MANIFEST_FILENAMES = {
    # JavaScript / TypeScript
    "package.json",
    # Python
    "requirements.txt",
    "requirements-dev.txt",
    "requirements_prod.txt",
    "requirements_dev.txt",
    "requirements.in",
    "Pipfile",
    "pyproject.toml",
    "setup.cfg",
    "setup.py",
    "environment.yml",
    "environment.yaml",
    # Rust
    "Cargo.toml",
    # Go
    "go.mod",
    # PHP
    "composer.json",
    # Java / Kotlin
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    # Ruby
    "Gemfile",
    # Swift
    "Package.swift",
    # Elixir
    "mix.exs",
    # Clojure
    "deps.edn",
    "project.clj",
    # Julia
    "Project.toml",
    # Dart / Flutter
    "pubspec.yaml",
}

# Allow simple glob-style matching for custom requirement variants and other manifests.
MANIFEST_PATTERNS = {
    "requirements*.txt",
    "requirements/*.txt",
    "*.csproj",
    "*.fsproj",
    "*.vbproj",
    "*.gemspec",
}


def collect_dependency_info(
    directory: Path,
    *,
    gitignore_spec: PathSpec | None = None,
    max_depth: int = 4,
) -> dict[str, Any]:
    """Collect dependency manifest data from the target directory."""
    manifests: list[dict[str, Any]] = []

    for manifest_path in _iter_manifest_files(directory, gitignore_spec, max_depth=max_depth):
        parsed = _parse_manifest(manifest_path)
        manifests.append(parsed)

    summary = _build_summary(manifests)
    return {
        "manifests": manifests,
        "summary": summary,
    }


def _iter_manifest_files(
    directory: Path,
    gitignore_spec: PathSpec | None,
    *,
    max_depth: int,
) -> Iterable[Path]:
    """Yield manifest files from the project directory."""
    include_files = MANIFEST_FILENAMES
    include_patterns = MANIFEST_PATTERNS

    # Build exclusion patterns but allow manifest files.
    exclude_patterns = set(EXCLUDED_FILES) - include_files
    for ext in EXCLUDED_EXTENSIONS:
        exclude_patterns.add(f"*{ext}")

    for path in list_files(
        directory,
        EXCLUDED_DIRS,
        exclude_patterns,
        max_depth=max_depth,
        gitignore_spec=gitignore_spec,
        root=directory,
    ):
        name = path.name
        if name in include_files or any(fnmatch.fnmatch(name, pattern) for pattern in include_patterns):
            yield path


def _parse_manifest(path: Path) -> dict[str, Any]:
    """Parse a known manifest file into a structured representation."""
    parser = _get_parser(path)
    try:
        data = parser(path)
    except Exception as exc:  # noqa: BLE001
        data = {
            "error": f"{type(exc).__name__}: {exc}",
        }

    return {
        "path": path.as_posix(),
        "type": data.get("type", _infer_manifest_type(path)),
        "manager": data.get("manager"),
        "data": data.get("data"),
        "raw_excerpt": data.get("raw_excerpt"),
        "error": data.get("error"),
    }


def _get_parser(path: Path):
    name = path.name
    suffix = path.suffix.lower()

    if name == "package.json":
        return _parse_package_json
    if name == "composer.json":
        return _parse_composer_json
    if suffix == ".toml" or name in {"Pipfile", "Cargo.toml", "Project.toml"}:
        return _parse_toml_like
    if suffix in {".txt", ".in"} or "requirements" in name.lower():
        return _parse_requirements_txt
    if name == "setup.cfg":
        return _parse_setup_cfg
    if name == "setup.py":
        return _parse_setup_py
    if name == "pubspec.yaml":
        return _parse_pubspec_yaml
    if suffix in {".yml", ".yaml"}:
        return _parse_environment_yaml
    if name == "go.mod":
        return _parse_go_mod
    if name == "pom.xml":
        return _parse_pom_xml
    if name in {"build.gradle", "build.gradle.kts"}:
        return _parse_gradle
    if suffix == ".csproj":
        return _parse_csproj
    if suffix == ".fsproj" or suffix == ".vbproj":
        return _parse_csproj
    if name == "Gemfile":
        return _parse_gemfile
    if suffix == ".gemspec":
        return _parse_gemspec
    if name == "Package.swift":
        return _parse_package_swift
    if name == "mix.exs":
        return _parse_mix_exs
    if name == "deps.edn":
        return _parse_deps_edn
    if name == "project.clj":
        return _parse_project_clj
    if name == "pubspec.yaml":
        return _parse_pubspec_yaml
    return _parse_generic_text


def _parse_package_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        content = fh.read()
    payload = json.loads(content)
    dependencies: dict[str, Any] = {}
    for field in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
        section = payload.get(field)
        if isinstance(section, dict) and section:
            dependencies[field] = dict(section)
    return {
        "type": "package_json",
        "manager": "npm",
        "data": dependencies or None,
        "raw_excerpt": _trim_excerpt(content),
    }


def _parse_composer_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        content = fh.read()
    payload = json.loads(content)
    dependencies: dict[str, Any] = {}
    for field in ("require", "require-dev"):
        section = payload.get(field)
        if isinstance(section, dict) and section:
            dependencies[field] = dict(section)
    return {
        "type": "composer_json",
        "manager": "composer",
        "data": dependencies or None,
        "raw_excerpt": _trim_excerpt(content),
    }


def _parse_toml_like(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        content = fh.read()
    data = tomllib.loads(content)
    name = path.name

    dependencies: dict[str, Any] = {}
    if name == "pyproject.toml":
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
    elif name == "Pipfile":
        for key in ("packages", "dev-packages"):
            section = data.get(key)
            if isinstance(section, dict):
                dependencies[key] = section
    elif name == "Cargo.toml":
        for key in ("dependencies", "dev-dependencies", "build-dependencies"):
            section = data.get(key)
            if isinstance(section, dict) and section:
                dependencies[key] = section
        target = data.get("target")
        if isinstance(target, dict) and target:
            dependencies["target"] = target
    elif name == "Project.toml":
        project = data.get("project")
        if isinstance(project, dict):
            dependencies["project"] = project
    else:
        dependencies = data
    return {
        "type": name,
        "manager": _infer_manager_from_toml(path),
        "data": dependencies or None,
        "raw_excerpt": _trim_excerpt(content),
    }


RE_REQUIREMENT = re.compile(r"^\s*([^#=\s]+)(?:\s*==\s*([^\s#]+))?")


def _parse_requirements_txt(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        lines = fh.readlines()
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
        "raw_excerpt": _trim_excerpt("".join(lines)),
    }


def _parse_environment_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        content = fh.read()
    return {
        "type": "environment_yaml",
        "manager": "conda",
        "data": None,
        "raw_excerpt": _trim_excerpt(content),
    }


def _parse_generic_text(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        content = fh.read()
    return {
        "type": path.name,
        "manager": None,
        "data": None,
        "raw_excerpt": _trim_excerpt(content),
    }


def _trim_excerpt(content: str, max_lines: int = 40) -> str:
    lines = content.splitlines()
    if len(lines) <= max_lines:
        return content
    snippet = "\n".join(lines[: max_lines - 1])
    return f"{snippet}\n…"


def _infer_manager_from_toml(path: Path) -> str | None:
    name = path.name
    if name == "pyproject.toml":
        return "python"
    if name == "Pipfile":
        return "pipenv"
    if name == "Cargo.toml":
        return "cargo"
    if name == "Project.toml":
        return "julia"
    return None


def _infer_manifest_type(path: Path) -> str:
    if path.name == "package.json":
        return "package_json"
    if path.suffix == ".toml":
        return path.name
    if "requirements" in path.name.lower():
        return "requirements_txt"
    return path.name


def _build_summary(manifests: list[dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, list[str]] = {}
    for entry in manifests:
        manager = entry.get("manager") or "unknown"
        summary.setdefault(manager, []).append(entry["path"])
    return summary


def _parse_setup_cfg(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        content = fh.read()

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
        "raw_excerpt": _trim_excerpt(content),
    }


INSTALL_RE_LIST = re.compile(r"install_requires\s*=\s*(\[.*?\])", re.DOTALL)
EXTRAS_RE = re.compile(r"extras_require\s*=\s*(\{.*?\})", re.DOTALL)


def _parse_setup_py(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        content = fh.read()

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
        "raw_excerpt": _trim_excerpt(content),
    }


def _parse_go_mod(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        lines = fh.readlines()

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
        "raw_excerpt": _trim_excerpt("".join(lines)),
    }


def _parse_pom_xml(path: Path) -> dict[str, Any]:
    tree = ET.parse(path)
    root = tree.getroot()
    dependencies: list[dict[str, Any]] = []

    for dep in root.findall(".//{*}dependency"):
        group = dep.findtext("{*}groupId")
        artifact = dep.findtext("{*}artifactId")
        version = dep.findtext("{*}version")
        scope = dep.findtext("{*}scope")
        entry = {
            "groupId": group,
            "artifactId": artifact,
        }
        if version:
            entry["version"] = version
        if scope:
            entry["scope"] = scope
        dependencies.append(entry)

    with path.open("r", encoding="utf-8", errors="replace") as fh:
        content = fh.read()

    return {
        "type": "pom_xml",
        "manager": "maven",
        "data": {"dependencies": dependencies} if dependencies else None,
        "raw_excerpt": _trim_excerpt(content),
    }


GRADLE_DEP_RE = re.compile(
    r"^\s*(api|implementation|compileOnly|runtimeOnly|testImplementation|testCompileOnly)"
    r"\s+['\"]([^'\"]+)['\"]"
)


def _parse_gradle(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        lines = fh.readlines()

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
        "raw_excerpt": _trim_excerpt("".join(lines)),
    }


def _parse_csproj(path: Path) -> dict[str, Any]:
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

    with path.open("r", encoding="utf-8", errors="replace") as fh:
        content = fh.read()

    return {
        "type": path.suffix.lstrip(".") + "_project",
        "manager": ".net",
        "data": {"dependencies": dependencies} if dependencies else None,
        "raw_excerpt": _trim_excerpt(content),
    }


GEMFILE_RE = re.compile(r"^\s*gem\s+['\"]([^'\"]+)['\"](?:,\s*['\"]([^'\"]+)['\"])?")


def _parse_gemfile(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        lines = fh.readlines()

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
        "raw_excerpt": _trim_excerpt("".join(lines)),
    }


GEMSPEC_RE = re.compile(
    r"add_(?:runtime_)?dependency\s*\(\s*['\"]([^'\"]+)['\"](?:,\s*['\"]([^'\"]+)['\"])?"
)


def _parse_gemspec(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        lines = fh.readlines()

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
        "raw_excerpt": _trim_excerpt("".join(lines)),
    }


SWIFT_PKG_RE = re.compile(
    r"\.package\s*\(\s*name:\s*\"([^\"']+)\".*?(?:from|exact):\s*\"([^\"']+)\"",
    re.DOTALL,
)


def _parse_package_swift(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        content = fh.read()

    deps = []
    for match in SWIFT_PKG_RE.finditer(content):
        name, version = match.groups()
        deps.append({"name": name, "version": version})

    return {
        "type": "Package.swift",
        "manager": "swiftpm",
        "data": {"dependencies": deps} if deps else None,
        "raw_excerpt": _trim_excerpt(content),
    }


MIX_DEP_RE = re.compile(r"{\s*:([^,\s]+)\s*,\s*\"([^\"]+)\"")


def _parse_mix_exs(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        content = fh.read()

    deps = []
    for match in MIX_DEP_RE.finditer(content):
        name, version = match.groups()
        deps.append({"name": name, "version": version})

    return {
        "type": "mix_exs",
        "manager": "mix",
        "data": {"dependencies": deps} if deps else None,
        "raw_excerpt": _trim_excerpt(content),
    }


DEPS_EDN_RE = re.compile(
    r"([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)\s+\{\s*:mvn/version\s+\"([^\"]+)\""
)


def _parse_deps_edn(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        content = fh.read()

    deps = []
    for match in DEPS_EDN_RE.finditer(content):
        name, version = match.groups()
        deps.append({"name": name, "version": version})

    return {
        "type": "deps_edn",
        "manager": "clojure",
        "data": {"dependencies": deps} if deps else None,
        "raw_excerpt": _trim_excerpt(content),
    }


PROJECT_CLJ_RE = re.compile(r"\[([\w\.-]+/[\w\.-]+)\s+\"([^\"]+)\"")


def _parse_project_clj(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        content = fh.read()

    deps = []
    for match in PROJECT_CLJ_RE.finditer(content):
        name, version = match.groups()
        deps.append({"name": name, "version": version})

    return {
        "type": "project_clj",
        "manager": "leiningen",
        "data": {"dependencies": deps} if deps else None,
        "raw_excerpt": _trim_excerpt(content),
    }


def _parse_pubspec_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        lines = fh.readlines()

    sections = ("dependencies", "dev_dependencies")
    data: dict[str, dict[str, str]] = {}
    current_section: str | None = None

    for raw_line in lines:
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.endswith(":"):
            section = stripped[:-1]
            if section in sections:
                current_section = section
                data.setdefault(section, {})
            continue
        if current_section:
            if ":" in stripped:
                name, version = stripped.split(":", maxsplit=1)
                data[current_section][name.strip()] = version.strip()

    return {
        "type": "pubspec_yaml",
        "manager": "dart",
        "data": data or None,
        "raw_excerpt": _trim_excerpt("".join(lines)),
    }
