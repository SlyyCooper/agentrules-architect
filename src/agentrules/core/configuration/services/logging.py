"""Logging preference helpers."""

from __future__ import annotations

from ..models import CLIConfig
from ..utils import normalize_verbosity_label


def set_logging_verbosity(config: CLIConfig, verbosity: str | None) -> None:
    config.verbosity = normalize_verbosity_label(verbosity)


def get_logging_verbosity(config: CLIConfig) -> str | None:
    return config.verbosity

