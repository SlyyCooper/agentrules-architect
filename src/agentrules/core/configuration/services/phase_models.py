"""Model override helpers."""

from __future__ import annotations

from ..models import CLIConfig


def set_phase_model(config: CLIConfig, phase: str, preset_key: str | None) -> None:
    if preset_key and preset_key.strip():
        config.models[phase] = preset_key.strip()
    else:
        config.models.pop(phase, None)


def get_model_overrides(config: CLIConfig) -> dict[str, str]:
    return dict(config.models)

