"""Shared styling helpers for Questionary prompts."""

from __future__ import annotations

from typing import Any

import questionary
from questionary import Style

# Central style for all CLI Questionary prompts. Keeps the pointer and highlights
# branded while dimming navigation actions like "Back" and "Done".
CLI_STYLE = Style(
    [
        ("qmark", "fg:#00d1b2 bold"),
        ("question", "bold"),
        ("answer", "fg:#00d1b2 bold"),
        ("pointer", "fg:#00d1b2 bold"),
        ("highlighted", "fg:#00d1b2 bold"),
        ("selected", "fg:#00d1b2"),
        ("instruction", ""),
        ("text", ""),
        ("navigation", "fg:#888888 italic"),
        ("status.enabled", "fg:#00d1b2 bold"),
        ("status.disabled", "fg:#ff5f5f bold"),
        ("status.separator", "fg:#444444"),
        ("status.bracket", "fg:#666666"),
        ("status.value", "fg:#00d1b2"),
        ("status.model", "fg:#00d1b2 bold"),
        ("status.provider", "fg:#888888"),
        ("status.variant", "fg:#00d1b2"),
    ]
)


def navigation_choice(label: str, *, value: Any) -> questionary.Choice:
    """Return a dimmed navigation choice (e.g. Back, Done)."""

    tokens: list[tuple[str, str]] = [("class:navigation", label)]
    return questionary.Choice(tokens, value=value)


def toggle_choice(label: str, enabled: bool, *, value: Any) -> questionary.Choice:
    """Return a choice with a color-coded ON/OFF status badge."""

    status_class = "status.enabled" if enabled else "status.disabled"
    status_text = "ON" if enabled else "OFF"
    tokens: list[tuple[str, str]] = [
        ("class:text", label),
        ("class:status.separator", "  "),
        ("class:status.bracket", "["),
        (f"class:{status_class}", status_text),
        ("class:status.bracket", "]"),
    ]
    return questionary.Choice(tokens, value=value)


def value_choice(label: str, value_text: str, *, value: Any) -> questionary.Choice:
    """Return a choice showing the current value in accent color."""

    tokens: list[tuple[str, str]] = [
        ("class:text", label),
        ("class:status.separator", "  "),
        ("class:status.bracket", "["),
        ("class:status.value", value_text),
        ("class:status.bracket", "]"),
    ]
    return questionary.Choice(tokens, value=value)


def model_display_choice(
    prefix: str,
    model_label: str,
    provider_label: str,
    *,
    value: Any,
) -> questionary.Choice:
    """Render a phase row with colored model/provider segments."""

    tokens: list[tuple[str, str]] = []
    if prefix:
        tokens.append(("class:text", prefix))
        tokens.append(("class:text", " "))
    tokens.extend(
        [
            ("class:status.model", model_label),
            ("class:text", "  "),
            ("class:status.provider", f"[{provider_label}]")
        ]
    )
    return questionary.Choice(tokens, value=value)


def model_variant_choice(label: str, variant: str | None, provider: str, *, value: Any) -> questionary.Choice:
    """Colored choice for variant entries when expanding a model group."""

    tokens: list[tuple[str, str]] = [
        ("class:text", label),
        ("class:status.separator", "  "),
        ("class:status.variant", variant or "Default"),
        ("class:text", "  "),
        ("class:status.provider", f"[{provider}]")
    ]
    return questionary.Choice(tokens, value=value)
