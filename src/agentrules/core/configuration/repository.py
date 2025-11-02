"""Persistence adapters for CLI configuration."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

from .constants import CONFIG_DIR, CONFIG_FILE
from .models import CLIConfig
from .serde import config_from_dict, config_to_dict

try:  # Python 3.11+
    import tomllib as tomli  # type: ignore[import-not-found]
except ModuleNotFoundError:  # pragma: no cover - fallback for older interpreters
    import tomli  # type: ignore[no-redef]
import tomli_w


class ConfigRepository(Protocol):
    """Abstraction for loading and persisting CLI configuration."""

    def load(self) -> CLIConfig:
        ...

    def save(self, config: CLIConfig) -> None:
        ...


class TomlConfigRepository(ConfigRepository):
    """Stores configuration in a TOML file."""

    def __init__(self, path: Path = CONFIG_FILE) -> None:
        self._path = path

    def load(self) -> CLIConfig:
        if not self._path.exists():
            return CLIConfig()
        with self._path.open("rb") as fh:
            payload = tomli.load(fh)
        return config_from_dict(payload)

    def save(self, config: CLIConfig) -> None:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with self._path.open("wb") as fh:
            tomli_w.dump(config_to_dict(config), fh)

