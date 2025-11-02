"""Logging configuration flow."""

from __future__ import annotations

import os

import questionary

from agentrules.cli.context import CliContext
from agentrules.cli.services import configuration
from agentrules.cli.ui.styles import CLI_STYLE, navigation_choice


def configure_logging(context: CliContext) -> None:
    """Interactive prompt for adjusting logging verbosity."""

    console = context.console
    console.print("\n[bold]Configure logging verbosity[/bold]")
    console.print(
        "Choose how much detail agentrules prints during analysis. Environment variable"
        " [cyan]AGENTRULES_LOG_LEVEL[/cyan] takes precedence if set.\n"
    )

    env_override = os.getenv("AGENTRULES_LOG_LEVEL")
    if env_override:
        console.print(
            f"[yellow]Active override detected:[/] AGENTRULES_LOG_LEVEL={env_override!r}."
            " Update or unset the variable to change levels here.\n"
        )

    choices = [
        questionary.Choice(title="Quiet – only warnings and errors", value="quiet"),
        questionary.Choice(title="Standard – progress updates (default)", value="standard"),
        questionary.Choice(title="Verbose – include debug diagnostics", value="verbose"),
        navigation_choice("Reset to default", value="__RESET__"),
        navigation_choice("Cancel", value="__CANCEL__"),
    ]

    current = configuration.get_logging_preference() or "standard"
    default_choice = current if current in {"quiet", "standard", "verbose"} else "standard"

    selection = questionary.select(
        "Select logging verbosity:",
        choices=choices,
        default=default_choice,
        qmark="🪵",
        style=CLI_STYLE,
    ).ask()

    if selection in (None, "__CANCEL__"):
        console.print("[yellow]No changes made to logging verbosity.[/]")
        return
    if selection == "__RESET__":
        configuration.save_logging_preference(None)
        console.print("[green]Logging verbosity reset to default (standard).[/]")
        return

    configuration.save_logging_preference(selection)
    if selection == "quiet":
        console.print("[green]Logging set to quiet. Only warnings and errors will display.[/]")
    elif selection == "verbose":
        console.print("[green]Logging set to verbose. Debug output will be shown.[/]")
    else:
        console.print("[green]Logging set to standard verbosity.[/]")
