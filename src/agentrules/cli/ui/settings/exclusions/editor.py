"""Prompt helpers for exclusion settings."""

from __future__ import annotations

import questionary

from agentrules.cli.ui.styles import CLI_STYLE


def prompt_exclusion_value(kind: str, default: str | None = None) -> str | None:
    """Prompt the user for an exclusion value with validation."""

    label_map = {
        "directories": "Directory name",
        "files": "Filename",
        "extensions": "Extension (with or without dot)",
    }
    qmark_map = {
        "directories": "📁",
        "files": "📄",
        "extensions": "🔣",
    }

    question = label_map.get(kind, "Value")
    qmark = qmark_map.get(kind, "?")

    def _validate(text: str) -> bool:
        stripped = text.strip()
        if not stripped:
            return False
        if kind == "directories" and ("/" in stripped or "\\" in stripped):
            return False
        if kind == "extensions" and ("/" in stripped or "\\" in stripped or " " in stripped):
            return False
        return True

    answer = questionary.text(
        question + ":",
        default=default or "",
        qmark=qmark,
        style=CLI_STYLE,
        validate=lambda text: _validate(text) or f"Enter a valid {question.lower()}",
    ).ask()

    return answer.strip() if answer else None
