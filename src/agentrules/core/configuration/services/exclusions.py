"""Exclusion override helpers."""

from __future__ import annotations

from agentrules.config.exclusions import EXCLUDED_DIRS, EXCLUDED_EXTENSIONS, EXCLUDED_FILES

from ..models import CLIConfig, ExclusionOverrides
from ..utils import apply_overrides, exclusion_attr_names, normalize_exclusion_value


def get_exclusion_overrides(config: CLIConfig) -> ExclusionOverrides:
    return config.exclusions


def get_effective_exclusions(config: CLIConfig) -> tuple[set[str], set[str], set[str]]:
    overrides = config.exclusions
    directories = apply_overrides(EXCLUDED_DIRS, overrides.add_directories, overrides.remove_directories)
    files = apply_overrides(EXCLUDED_FILES, overrides.add_files, overrides.remove_files)
    extensions = apply_overrides(EXCLUDED_EXTENSIONS, overrides.add_extensions, overrides.remove_extensions)
    return directories, files, extensions


def add_exclusion_entry(config: CLIConfig, kind: str, value: str) -> str | None:
    normalized = normalize_exclusion_value(kind, value)
    if normalized is None:
        return None

    add_attr, remove_attr = exclusion_attr_names(kind)
    add_list = getattr(config.exclusions, add_attr)
    remove_list = getattr(config.exclusions, remove_attr)

    if normalized not in add_list:
        add_list.append(normalized)
    if normalized in remove_list:
        remove_list.remove(normalized)

    return normalized


def remove_exclusion_entry(config: CLIConfig, kind: str, value: str) -> str | None:
    normalized = normalize_exclusion_value(kind, value)
    if normalized is None:
        return None

    add_attr, remove_attr = exclusion_attr_names(kind)
    add_list = getattr(config.exclusions, add_attr)
    remove_list = getattr(config.exclusions, remove_attr)

    if normalized in add_list:
        add_list.remove(normalized)
    elif normalized not in remove_list:
        remove_list.append(normalized)

    return normalized


def reset_exclusions(config: CLIConfig) -> None:
    config.exclusions = ExclusionOverrides()


def set_respect_gitignore(config: CLIConfig, enabled: bool) -> None:
    config.exclusions.respect_gitignore = bool(enabled)


def should_respect_gitignore(config: CLIConfig, default: bool = True) -> bool:
    if config.exclusions is None:
        return default
    return bool(config.exclusions.respect_gitignore)


def get_tree_max_depth(config: CLIConfig, default: int = 5) -> int:
    depth = config.exclusions.tree_max_depth
    if depth is None:
        return max(default, 1)
    return max(depth, 1)


def set_tree_max_depth(config: CLIConfig, value: int | None) -> None:
    if value is not None and value < 1:
        raise ValueError("tree depth must be at least 1")
    config.exclusions.tree_max_depth = value


def reset_tree_max_depth(config: CLIConfig) -> None:
    config.exclusions.tree_max_depth = None

