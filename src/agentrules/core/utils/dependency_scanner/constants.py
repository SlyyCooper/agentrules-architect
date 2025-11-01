"""Static configuration for dependency manifest scanning."""

from __future__ import annotations

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
