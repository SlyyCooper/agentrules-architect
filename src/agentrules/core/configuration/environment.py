"""Environment adapters for applying configuration at runtime."""

from __future__ import annotations

import os
from collections.abc import MutableMapping

from .constants import DEFAULT_VERBOSITY, PROVIDER_ENV_MAP, TRUTHY_ENV_VALUES, VERBOSITY_ENV_VAR, VERBOSITY_PRESETS
from .models import CLIConfig
from .utils import normalize_verbosity_label


class EnvironmentManager:
    """Thin wrapper around environment access to aid testing and reuse."""

    def __init__(self, environ: MutableMapping[str, str] | None = None) -> None:
        self._environ = environ if environ is not None else os.environ

    def getenv(self, key: str) -> str | None:
        return self._environ.get(key)

    def apply_provider_credentials(self, config: CLIConfig) -> None:
        for provider, env_var in PROVIDER_ENV_MAP.items():
            if not env_var:
                continue
            cfg = config.providers.get(provider)
            api_key = cfg.api_key if cfg else None
            if not api_key:
                self._environ.pop(env_var, None)
                continue
            if provider == "gemini":
                self._environ.pop("GEMINI_API_KEY", None)
            self._environ[env_var] = api_key

    def resolve_log_level(self, config: CLIConfig, default: int | None = None) -> int:
        env_value = self.getenv(VERBOSITY_ENV_VAR)
        label = normalize_verbosity_label(env_value)
        if label is None:
            label = normalize_verbosity_label(config.verbosity)

        if label is None:
            fallback = VERBOSITY_PRESETS[DEFAULT_VERBOSITY]
            return fallback if default is None else default

        level = VERBOSITY_PRESETS.get(label)
        if level is not None:
            return level

        fallback = VERBOSITY_PRESETS[DEFAULT_VERBOSITY]
        return fallback if default is None else default

    def is_truthy(self, key: str) -> bool:
        value = self.getenv(key)
        return value is not None and value.strip().lower() in TRUTHY_ENV_VALUES
