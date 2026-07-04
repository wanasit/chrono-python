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
├── types.py          # User-facing output wrappers (ParsedResult, ParsedRangeResult) and datetime wrappers (DateTimeMoment)
├── common/           # Shared, locale-agnostic logic
│   ├── types.py      # Enums (CivilTimeComponent) and internal parser/refiner types (ParsingCivilTimeMoment)
│   ├── parsers/      # Common parsers (ISOFormatParser, SlashDateFormatParser)
│   ├── refiners/     # Common refiners (RemoveOverlapRefiner)
│   ├── calendars.py  # Year offset and calculation helpers
│   └── weekdays.py   # Weekday calculation helpers
├── locales/          # Language/Locale specific components
│   ├── en/           # English configuration, constants, and locale parsers
│   └── ja/           # Japanese configuration and locale parsers
└── utils/            # Helper utilities
    ├── patterns.py   # Pattern utilities
    └── re.py         # Re.Match wrapper class (Match)
```

### Core Concepts
1. **Parsers (`chrono.Parser`)**:
   Identify date patterns in text. Must implement `pattern()` to return a compiled regex and `extract(context, match)` to output either `ParsedResult`, `Moment`, or `None`.
2. **Refiners (`chrono.Refiner`)**:
   Post-process and merge/filter the parsed results (e.g. merging date and time expressions, or resolving overlaps).
3. **ParsedResult and ParsedRangeResult (`types.ParsedResult`, `types.ParsedRangeResult`)**:
   Represent the final output structure of the parsing step, containing the matched index, matched text, and a `moment` (plus an optional `end` moment for ranges).
4. **DateTimeMoment and ReferenceMoment (`types.DateTimeMoment`, `types.ReferenceMoment`)**:
   - `DateTimeMoment`: Wraps an absolute datetime (with a specific precision).
   - `ReferenceMoment`: Represents a relative duration shift (e.g., "10 years ago") relative to a reference moment.
5. **ParsingCivilTimeMoment (`common.types.ParsingCivilTimeMoment`)**:
   Extends `DateTimeMoment` and tracks components of a date (e.g., Year, Month, Day) as either `known_values` (explicitly present in match) or `implied_values` (implied from reference date or other clues).
   - `ParsingCivilTimeMoment.datetime()` computes a resolved `datetime.datetime` by applying the assigned and implied components over the reference date.
   - Its precision represents the most precise component that is either assigned or implied.

---

## Key Context & Caveats

1. **Feature parity with TypeScript Chrono**:
   The Python version is currently a simplified, work-in-progress port of the JS/TS library. Options like `forwardDate` or a separate `GB` locale structure are not yet implemented.

---

## Git & Commit Message Format

Follow the existing commit message format conventions:
- Use prefix `New:` for new features or implementations (e.g. `New: Time expr parsing`, `New: Merge date range refiners`).
- Use prefix `New: (Locale)` for locale-specific features or implementations (e.g. `New: (JP) Setup Japanese merge date range refiner`).
- Use prefix `Refactor:` for code cleanups or refactoring changes (e.g. `Refactor: Introduce CivilTime concept`).
- Use prefix `Add:` or `Fix:` if adding tests or fixing issues (e.g. `Add test for parsers`).

---

## AI Agent Tool & Command Guidelines

To ensure secure, auditable, and standard operations:
- **Network Requests**: Do not run casual python commands to execute network calls (e.g. `python3 -c "import urllib..."`). Instead, use standard tools like `curl -L -k` or `wget`.
- **Code Execution**: Do not run temporary python code snippets locally to check outputs or verify states. Modify the workspace code directly and use the proper verification tools (e.g. `poetry run pytest`).



