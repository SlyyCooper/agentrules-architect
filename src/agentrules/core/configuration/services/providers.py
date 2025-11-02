"""Provider credential helpers."""

from __future__ import annotations

from collections.abc import Callable

from ..constants import PROVIDER_ENV_MAP
from ..models import CLIConfig, ProviderConfig


def set_provider_key(config: CLIConfig, provider: str, api_key: str | None) -> None:
    config.providers[provider] = ProviderConfig(api_key=api_key)


def current_provider_keys(config: CLIConfig) -> dict[str, str | None]:
    return {
        provider: config.providers.get(provider, ProviderConfig()).api_key
        for provider in PROVIDER_ENV_MAP
    }


def has_tavily_credentials(config: CLIConfig, getenv: Callable[[str], str | None]) -> bool:
    stored = config.providers.get("tavily")
    if stored and stored.api_key:
        return True
    env_var = PROVIDER_ENV_MAP.get("tavily")
    return bool(env_var and getenv(env_var))

