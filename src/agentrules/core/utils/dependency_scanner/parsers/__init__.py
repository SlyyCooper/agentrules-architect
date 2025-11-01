"""Built-in manifest parsers."""

from __future__ import annotations

from ..registry import ManifestParserRegistry
from .clojure import register_clojure_parsers
from .dart import register_dart_parsers
from .dotnet import register_dotnet_parsers
from .elixir import register_elixir_parsers
from .generic import parse_generic_text
from .go import register_go_parsers
from .java import register_java_parsers
from .javascript import register_javascript_parsers
from .php import register_php_parsers
from .python import register_python_parsers
from .ruby import register_ruby_parsers
from .swift import register_swift_parsers
from .toml_based import register_toml_parsers


def build_parser_registry() -> ManifestParserRegistry:
    registry = ManifestParserRegistry(fallback=parse_generic_text)
    register_javascript_parsers(registry)
    register_python_parsers(registry)
    register_php_parsers(registry)
    register_go_parsers(registry)
    register_java_parsers(registry)
    register_dotnet_parsers(registry)
    register_ruby_parsers(registry)
    register_swift_parsers(registry)
    register_elixir_parsers(registry)
    register_clojure_parsers(registry)
    register_dart_parsers(registry)
    register_toml_parsers(registry)
    return registry
