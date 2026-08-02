import datetime
import importlib
from typing import TYPE_CHECKING

from chrono_python import types
from chrono_python.chrono import Chrono, Parser, Refiner, Configuration
from chrono_python.types import ParsedResult, ParsedRangeResult, DateTimeMoment, ReferenceMoment

# Enable static type checking (mypy, pyright, IDE autocomplete) for lazily imported
# locale submodules without eagerly importing them at runtime.
if TYPE_CHECKING:
    from chrono_python.locales import en, ja, fr, it, zh


def parse(text: str, reference: types.Moment | datetime.datetime | None = None) -> list[ParsedResult]:
    """A shorthand for `chrono.en.casual.parse()`.
    
    Parse input text using the default English casual configuration and return a list of parsed results.

    Args:
        text: The natural language date/time text to parse.
        reference: Optional reference moment or datetime to resolve relative date expressions.

    Returns:
        A list of ParsedResult objects representing extracted date/time components.
    """
    en_module = globals().get("en") or __getattr__("en")
    return en_module.casual.parse(text, reference)


def parse_date(text: str, reference: types.Moment | datetime.datetime | None = None) -> datetime.datetime | None:
    """A shorthand for `chrono.en.casual.parse_date()`.
    
    Parse input text using the default English casual configuration and return the first matched datetime.

    Args:
        text: The natural language date/time text to parse.
        reference: Optional reference moment or datetime to resolve relative date expressions.

    Returns:
        The Python datetime object of the first result, or None if no date was matched.
    """
    en_module = globals().get("en") or __getattr__("en")
    return en_module.casual.parse_date(text, reference)

# -------------------------------
# Lazy Submodule Loading (PEP 562)
#
# Locale submodules ('en', 'ja', 'fr', etc.) are loaded dynamically on demand when accessed
# (e.g., `chrono_python.ja`) to avoid eager regex compilation and heavy module loading at startup.

_LOCALES = {"en", "ja", "fr", "it", "zh"}

def __getattr__(name: str):
    if name in _LOCALES:
        module = importlib.import_module(f"chrono_python.locales.{name}")
        globals()[name] = module
        return module
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


def __dir__():
    return sorted(list(globals().keys()) + list(_LOCALES))


__all__ = [
    "Chrono",
    "Parser",
    "Refiner",
    "Configuration",
    "ParsedResult",
    "ParsedRangeResult",
    "DateTimeMoment",
    "ReferenceMoment",
    "parse",
    "parse_date",
] + list(_LOCALES)
