"""Implementation of the `analyze` subcommand."""

from __future__ import annotations

from pathlib import Path

import typer

from ..bootstrap import bootstrap_runtime
from ..services.pipeline_runner import run_pipeline

DEFAULT_ANALYZE_PATH = Path.cwd()
PATH_ARGUMENT = typer.Argument(
    DEFAULT_ANALYZE_PATH,
    exists=True,
    dir_okay=True,
    file_okay=False,
    resolve_path=True,
)


def register(app: typer.Typer) -> None:
    """Register the `analyze` subcommand with the provided Typer app."""

    @app.command()
    def analyze(  # type: ignore[func-returns-value]
        path: Path = PATH_ARGUMENT,
        offline: bool = typer.Option(False, "--offline", help="Run using offline dummy architects (no API calls)."),
    ) -> None:
        context = bootstrap_runtime()
        run_pipeline(path, offline, context)
