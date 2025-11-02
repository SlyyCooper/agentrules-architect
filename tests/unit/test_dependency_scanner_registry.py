from __future__ import annotations

from pathlib import Path
from textwrap import dedent

from agentrules.core.utils.dependency_scanner import build_parser_registry
from agentrules.core.utils.dependency_scanner.parsers.javascript import parse_package_json
from agentrules.core.utils.dependency_scanner.parsers.python import parse_pyproject_toml
from agentrules.core.utils.dependency_scanner.registry import (
    ManifestParserRegistry,
    ParserRegistration,
)


def _write(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def test_registry_prefers_highest_priority_match(tmp_path: Path) -> None:
    calls: list[str] = []

    def low_parser(_: Path) -> dict[str, object]:
        calls.append("low")
        return {"type": "low"}

    def high_parser(_: Path) -> dict[str, object]:
        calls.append("high")
        return {"type": "high"}

    registry = ManifestParserRegistry(fallback=None)
    registry.register(
        ParserRegistration(parser=low_parser, suffixes=(".json",), priority=10)
    )
    registry.register(
        ParserRegistration(parser=high_parser, names=("package.json",), priority=20)
    )

    manifest = tmp_path / "package.json"
    manifest.write_text("{}", encoding="utf-8")

    parser = registry.resolve(manifest)
    result = parser(manifest)

    assert result["type"] == "high"
    assert calls == ["high"]


def test_registry_falls_back_when_no_match(tmp_path: Path) -> None:
    fallback_called: list[Path] = []

    def fallback_parser(path: Path) -> dict[str, object]:
        fallback_called.append(path)
        return {"type": path.name}

    registry = ManifestParserRegistry(fallback=fallback_parser)

    manifest = tmp_path / "Custom.MF"
    manifest.write_text("name=demo", encoding="utf-8")

    parser = registry.resolve(manifest)
    result = parser(manifest)

    assert result == {"type": "Custom.MF"}
    assert fallback_called == [manifest]


def test_build_parser_registry_handles_requirements_variants(tmp_path: Path) -> None:
    registry = build_parser_registry()

    requirements = tmp_path / "requirements-prod.txt"
    _write(requirements, "flask==3.0.0")

    parser = registry.resolve(requirements)
    parsed = parser(requirements)

    assert parsed["manager"] == "pip"
    assert {"name": "flask", "version": "3.0.0"} in (parsed["data"] or [])
    assert parsed["type"] == "requirements_txt"


def test_parse_package_json_extracts_sections(tmp_path: Path) -> None:
    manifest = tmp_path / "package.json"
    _write(
        manifest,
        dedent(
            """
            {
              "dependencies": {"react": "^18.2.0"},
              "devDependencies": {"typescript": "5.4.0"}
            }
            """
        ).strip(),
    )

    result = parse_package_json(manifest)

    assert result["manager"] == "npm"
    assert result["data"]["dependencies"]["react"] == "^18.2.0"
    assert result["data"]["devDependencies"]["typescript"] == "5.4.0"


def test_parse_pyproject_toml_reads_poetry_sections(tmp_path: Path) -> None:
    manifest = tmp_path / "pyproject.toml"
    _write(
        manifest,
        dedent(
            """
            [project]
            dependencies = ["fastapi==0.115.0"]

            [tool.poetry]
            name = "demo"
            version = "0.1.0"

            [tool.poetry.dependencies]
            python = "^3.11"
            pendulum = "3.0.0"
            """
        ).strip(),
    )

    result = parse_pyproject_toml(manifest)

    assert result["manager"] == "python"
    assert "fastapi==0.115.0" in result["data"]["project"]
    assert result["data"]["poetry_dependencies"]["pendulum"] == "3.0.0"
