"""Interactive main menu for the agentrules CLI."""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import questionary

from ..context import CliContext
from ..services.pipeline_runner import run_pipeline
from .settings import configure_settings
from .styles import CLI_STYLE, navigation_choice


def run_main_menu(context: CliContext) -> None:
    console = context.console
    banner = dedent(
        """
        [bold cyan]
         █████╗  ██████╗ ███████╗███╗   ██╗████████╗██████╗ ██╗   ██╗██╗     ███████╗███████╗
        ██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝██╔══██╗██║   ██║██║     ██╔════╝██╔════╝
        ███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║   ██████╔╝██║   ██║██║     █████╗  ███████╗
        ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║   ██╔══██╗██║   ██║██║     ██╔══╝  ╚════██║
        ██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║   ██║  ██║╚██████╔╝███████╗███████╗███████║
        ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝╚══════╝
        [/bold cyan]
        """
    )
    console.print(banner)
    console.print("[dim]Analyze projects, manage providers, and tune model presets.[/dim]\n")

    menu_options = [
        ("Analyze current directory", "analyze_current"),
        ("Analyze another path", "analyze_other"),
        ("Settings", "settings"),
    ]

    while True:
        choices = [
            questionary.Choice(title=label, value=value)
            for label, value in menu_options
        ]
        choices.append(navigation_choice("Exit", value="exit"))

        choice = questionary.select(
            "What would you like to do?",
            choices=choices,
            qmark="🤖",
            style=CLI_STYLE,
        ).ask()

        if choice in (None, "exit"):
            console.print("Goodbye!")
            return

        action = choice
        if action == "analyze_current":
            run_pipeline(Path.cwd(), offline=False, context=context)
        elif action == "analyze_other":
            path_answer = questionary.path(
                "Target project directory:",
                only_directories=True,
                style=CLI_STYLE,
            ).ask()
            if not path_answer:
                continue
            target = Path(path_answer.strip()).expanduser().resolve()
            if not target.exists() or not target.is_dir():
                console.print(f"[red]Invalid directory: {target}[/]")
                continue
            run_pipeline(target, offline=False, context=context)
        elif action == "settings":
            configure_settings(context)
