from __future__ import annotations

from pathlib import Path
from textwrap import dedent

from agentrules.core.utils.dependency_scanner import collect_dependency_info


def _write(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def test_collect_dependency_info_parses_common_manifests(tmp_path: Path) -> None:
    package_json = tmp_path / "package.json"
    _write(
        package_json,
        dedent(
            """
            {
              "name": "demo-app",
              "dependencies": {
                "react": "^18.2.0"
              },
              "devDependencies": {
                "typescript": "5.4.0"
              }
            }
            """
        ).strip(),
    )

    requirements_txt = tmp_path / "requirements.txt"
    _write(
        requirements_txt,
        dedent(
            """
            requests==2.32.0
            # comment line
            flask
            """
        ).strip(),
    )

    pyproject = tmp_path / "pyproject.toml"
    _write(
        pyproject,
        dedent(
            """
            [project]
            name = "demo-app"
            version = "0.1.0"
            dependencies = [
              "fastapi==0.115.0",
            ]

            [tool.poetry]
            name = "demo-app"
            version = "0.1.0"

            [tool.poetry.dependencies]
            python = "^3.11"
            pendulum = "3.0.0"
            """
        ).strip(),
    )

    result = collect_dependency_info(tmp_path)

    manifest_map = {entry["path"]: entry for entry in result["manifests"]}
    assert len(manifest_map) == 3

    pkg_entry = manifest_map[package_json.as_posix()]
    assert pkg_entry["manager"] == "npm"
    assert pkg_entry["data"]["dependencies"]["react"] == "^18.2.0"
    assert pkg_entry["data"]["devDependencies"]["typescript"] == "5.4.0"

    req_entry = manifest_map[requirements_txt.as_posix()]
    assert req_entry["manager"] == "pip"
    assert {"name": "requests", "version": "2.32.0"} in req_entry["data"]
    assert {"name": "flask"} in req_entry["data"]

    pyproject_entry = manifest_map[pyproject.as_posix()]
    assert pyproject_entry["manager"] == "python"
    assert "fastapi==0.115.0" in pyproject_entry["data"]["project"]
    assert pyproject_entry["data"]["poetry_dependencies"]["python"] == "^3.11"

    summary = result["summary"]
    assert set(summary["npm"]) == {package_json.as_posix()}
    assert set(summary["pip"]) == {requirements_txt.as_posix()}
    assert set(summary["python"]) == {pyproject.as_posix()}


def test_collect_dependency_info_handles_broader_manifests(tmp_path: Path) -> None:
    cargo = tmp_path / "Cargo.toml"
    _write(
        cargo,
        dedent(
            """
            [package]
            name = "demo"
            version = "0.1.0"

            [dependencies]
            serde = "1.0"

            [dev-dependencies]
            anyhow = "1.0"
            """
        ).strip(),
    )

    go_mod = tmp_path / "go.mod"
    _write(
        go_mod,
        dedent(
            """
            module example.com/demo

            go 1.22

            require (
                github.com/pkg/errors v0.9.1
                golang.org/x/net v0.25.0
            )
            """
        ).strip(),
    )

    composer = tmp_path / "composer.json"
    _write(
        composer,
        dedent(
            """
            {
              "require": {
                "laravel/framework": "^11.0"
              },
              "require-dev": {
                "phpunit/phpunit": "^11.0"
              }
            }
            """
        ).strip(),
    )

    setup_cfg = tmp_path / "setup.cfg"
    _write(
        setup_cfg,
        dedent(
            """
            [metadata]
            name = demo

            [options]
            install_requires =
                uvicorn
                starlette==0.37.0
            """
        ).strip(),
    )

    csproj = tmp_path / "Demo.csproj"
    _write(
        csproj,
        dedent(
            """
            <Project Sdk="Microsoft.NET.Sdk">
              <ItemGroup>
                <PackageReference Include="Newtonsoft.Json" Version="13.0.3" />
              </ItemGroup>
            </Project>
            """
        ).strip(),
    )

    gemfile = tmp_path / "Gemfile"
    _write(
        gemfile,
        dedent(
            """
            source 'https://rubygems.org'
            gem 'rails', '~> 7.1'
            gem 'pg'
            """
        ).strip(),
    )

    package_swift = tmp_path / "Package.swift"
    _write(
        package_swift,
        dedent(
            """
            // swift-tools-version:5.9
            import PackageDescription

            let package = Package(
                name: "Demo",
                dependencies: [
                    .package(name: "Alamofire", url: "https://github.com/Alamofire/Alamofire.git", from: "5.8.0")
                ]
            )
            """
        ).strip(),
    )

    mix_exs = tmp_path / "mix.exs"
    _write(
        mix_exs,
        dedent(
            """
            defp deps do
              [
                {:phoenix, "~> 1.7.0"},
                {:ecto_sql, "~> 3.11"}
              ]
            end
            """
        ).strip(),
    )

    deps_edn = tmp_path / "deps.edn"
    _write(
        deps_edn,
        dedent(
            """
            {:paths ["src"]
             :deps {org.clojure/clojure {:mvn/version "1.11.2"}}}
            """
        ).strip(),
    )

    project_clj = tmp_path / "project.clj"
    _write(
        project_clj,
        dedent(
            """
            (defproject demo "0.1.0-SNAPSHOT"
              :dependencies [[org.clojure/clojure "1.11.2"]])
            """
        ).strip(),
    )

    pubspec = tmp_path / "pubspec.yaml"
    _write(
        pubspec,
        dedent(
            """
            name: demo
            dependencies:
              flutter:
                sdk: flutter
              http: ^1.2.0
            dev_dependencies:
              flutter_test:
                sdk: flutter
            """
        ).strip(),
    )

    result = collect_dependency_info(tmp_path)
    manifest_map = {entry["path"]: entry for entry in result["manifests"]}

    assert manifest_map[cargo.as_posix()]["manager"] == "cargo"
    cargo_data = manifest_map[cargo.as_posix()]["data"]
    assert "dependencies" in cargo_data and "serde" in cargo_data["dependencies"]

    go_data = manifest_map[go_mod.as_posix()]["data"]
    assert go_data["module"] == "example.com/demo"
    assert {"module": "github.com/pkg/errors", "version": "v0.9.1"} in go_data["dependencies"]

    composer_data = manifest_map[composer.as_posix()]["data"]
    assert composer_data["require"]["laravel/framework"] == "^11.0"

    setup_cfg_data = manifest_map[setup_cfg.as_posix()]["data"]
    assert "uvicorn" in setup_cfg_data["install_requires"]

    csproj_data = manifest_map[csproj.as_posix()]["data"]
    assert {"package": "Newtonsoft.Json", "version": "13.0.3"} in csproj_data["dependencies"]

    gemfile_data = manifest_map[gemfile.as_posix()]["data"]
    assert {"name": "rails", "version": "~> 7.1"} in gemfile_data["dependencies"]

    swift_data = manifest_map[package_swift.as_posix()]["data"]
    assert {"name": "Alamofire", "version": "5.8.0"} in swift_data["dependencies"]

    mix_data = manifest_map[mix_exs.as_posix()]["data"]
    assert {"name": "phoenix", "version": "~> 1.7.0"} in mix_data["dependencies"]

    deps_data = manifest_map[deps_edn.as_posix()]["data"]
    assert {"name": "org.clojure/clojure", "version": "1.11.2"} in deps_data["dependencies"]

    project_data = manifest_map[project_clj.as_posix()]["data"]
    assert {"name": "org.clojure/clojure", "version": "1.11.2"} in project_data["dependencies"]

    pubspec_data = manifest_map[pubspec.as_posix()]["data"]
    assert pubspec_data["dependencies"]["http"] == "^1.2.0"

    summary = result["summary"]
    assert cargo.as_posix() in summary["cargo"]
    assert go_mod.as_posix() in summary["go"]
    assert composer.as_posix() in summary["composer"]
    assert setup_cfg.as_posix() in summary["python"]
    assert csproj.as_posix() in summary[".net"]
