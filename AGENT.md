# Agent Documentation - Project Setup & Architecture

This document provides a guide for AI agents working on `chrono-python` to quickly understand the project context, layout, testing commands, and implementation constraints.

## Project Overview
`chrono-python` is a Python port of the popular natural language date parser [chrono](https://github.com/wanasit/chrono). It identifies and extracts dates, times, and relative date expressions from free text without relying on external dependencies.

---

## Technical Stack & Setup
- **Language**: Python (requires version `^3.12` or newer)
- **Dependency Manager**: [Poetry](https://python-poetry.org/)
- **Testing Framework**: `pytest`

### Running Tests
To run the full test suite, execute:
```bash
poetry run pytest
```
*Note: Test logging is configured to `DEBUG` level via `pytest.ini`.*

---

## Directory Structure & Architecture

```
chrono_python/
├── chrono.py         # Main orchestrator (Chrono, Parser, Refiner, Configuration)
├── result.py         # Output wrappers (ParsedResult, ParsedRangeResult, ParsingMoment)
├── types.py          # Enums (DateTimeComponent, Timeunit) and datetime wrappers (DateTimeMoment)
├── re.py             # Re.Match wrapper class (Match)
├── common/           # Shared, locale-agnostic logic
│   ├── parsers/      # Common parsers (ISOFormatParser, SlashDateFormatParser)
│   └── refiners/     # Common refiners (RemoveOverlapRefiner)
├── locales/          # Language/Locale specific components
│   ├── en/           # English configuration, constants, and locale parsers
│   └── ja/           # Japanese configuration and locale parsers
└── utils/            # Helper utilities
    ├── calendars.py  # Year offset and calculation helpers
    └── patterns.py   # Pattern utilities
```

### Core Concepts
1. **Parsers (`chrono.Parser`)**:
   Identify date patterns in text. Must implement `pattern()` to return a compiled regex and `extract(context, match)` to output either `ParsedResult`, `Moment`, or `None`.
2. **Refiners (`chrono.Refiner`)**:
   Post-process and merge/filter the parsed results (e.g. merging date and time expressions, or resolving overlaps).
3. **ParsingMoment (`result.ParsingMoment`)**:
   Tracks components of a date (e.g. Year, Month, Day) as either `known_values` (explicitly present in match) or `implied_values` (implied from reference date).

---

## Key Context & Caveats

1. **Commented out unittest code**:
   The `TestBesicOperations` class in `tests/test_basic_operations.py` has been commented out because it was broken due to a missing `unittest` dependency import and needs to be rewritten later using the standard `pytest` structure. Do not uncomment it unless you are actively refactoring it.
2. **Feature parity with TypeScript Chrono**:
   The Python version is currently a simplified, work-in-progress port of the JS/TS library. Options like `forwardDate` or a separate `GB` locale structure are not yet implemented.
3. **ParsingMoment Evaluation**:
   `ParsingMoment.datetime()` currently returns the reference datetime directly (`self._reference.datetime()`), which means `chrono.parse_date()` does not yet construct a fully resolved datetime from the extracted components. The current testing convention checks the parsed values directly using `.moment.get(DateTimeComponent.X)`.
