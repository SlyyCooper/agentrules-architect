"""Provider configuration flows."""

from __future__ import annotations

import questionary
from rich.table import Table

from agentrules.cli.context import CliContext, format_secret_status, mask_secret
from agentrules.cli.services import configuration
from agentrules.cli.ui.styles import CLI_STYLE, navigation_choice


def _render_provider_table(context: CliContext, states: list[configuration.ProviderState]) -> None:
    table = Table(title="[bold]Provider API Keys[/bold]", show_lines=False, pad_edge=False)
    table.add_column("Provider", style="bold", no_wrap=True)
    table.add_column("Status", style="", no_wrap=True)
    table.add_column("Key", style="dim")

    for state in states:
        status_display = format_secret_status(state.api_key)
        key_display = mask_secret(state.api_key) if state.api_key else "-"
        if state.api_key:
            key_display = f"[dim]{key_display}[/]"
        else:
            key_display = "[dim]-[/]"
        table.add_row(state.name.title(), status_display, key_display)

    context.console.print("")
    context.console.print(table)
    context.console.print("")


def show_provider_summary(context: CliContext) -> None:
    """Print a rich summary table of provider API keys."""

    states = configuration.list_provider_states()
    _render_provider_table(context, states)


def configure_provider_keys(context: CliContext) -> None:
    """Interactive flow for updating provider API keys."""

    console = context.console
    console.print("\n[bold]Configure Provider API Keys[/bold]")
    console.print("Select a provider to update. Leave the key blank to keep the current value.")

    updated = False

    while True:
        states = configuration.list_provider_states()
        _render_provider_table(context, states)
        choices: list[questionary.Choice] = [
            questionary.Choice(title=state.name.title(), value=state.name) for state in states
        ]
        choices.append(navigation_choice("Done", value="__DONE__"))

        selection = questionary.select(
            "Select provider to configure:",
            choices=choices,
            qmark="🔐",
            style=CLI_STYLE,
        ).ask()

        if selection is None:
            console.print("[yellow]Configuration cancelled.[/]")
            return
        if selection == "__DONE__":
            break

        state = next((item for item in states if item.name == selection), None)
        if not state:
            console.print("[red]Unknown provider selected.[/]")
            continue

        current_display = mask_secret(state.api_key)
        answer = questionary.password(
            f"Enter {state.name.title()} API key [{current_display}]",
            qmark="🔐",
            default="",
            style=CLI_STYLE,
        ).ask()

        if answer is None:
            console.print("[yellow]Configuration cancelled.[/]")
            return

        trimmed = answer.strip()
        if trimmed:
            configuration.save_provider_key(selection, trimmed)
            updated = True
            console.print(f"[green]{selection.title()} key updated.[/]")
        else:
            console.print("[dim]No changes made.[/]")

    if updated:
        console.print("[green]Provider keys updated.[/]")
    else:
        console.print("[dim]No provider keys changed.[/]")
