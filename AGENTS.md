# Agent Documentation - Project Setup & Architecture

This document provides a guide for AI agents working on `chrono-python` to quickly understand the project context, layout, testing commands, and implementation constraints.

## Project Overview
`chrono-python` is a Python port of the popular natural language date parser [chrono](https://github.com/wanasit/chrono). It identifies and extracts dates, times, and relative date expressions from free text without relying on external dependencies.

---

## Technical Stack & Setup
- **Language**: Python (requires version `^3.12` or newer)
- **Dependency Manager**: [uv](https://docs.astral.sh/uv/)
- **Testing Framework**: `pytest`

### Running Tests
To run the full test suite, execute:
```bash
uv run pytest
```
*Note: Test logging is configured to `DEBUG` level via `pytest.ini`.*

### Test File Naming Convention
Test files must describe the behavior they are testing (rather than the names of the parser/refiner classes), ending with a verb in `-ing` form (e.g. `_parsing.py`, `_filtering.py`, `_merging.py`). For example:
- `test_en_unlikely_format_filtering.py` (testing filtering behavior) instead of `test_en_unlikely_format_filter.py` (class).
- `test_en_date_range_merging.py` (testing merging behavior) instead of `test_en_merge_date_range_refiner.py` (class).

### Parser Class Naming Convention
Parser classes should use a descriptive name based on the relative position of the date/time components rather than endianness:
- `MonthNameAfterDate` (formerly `MonthNameLittleEndianParser`) for day-first formats (e.g., "20 January").
- `MonthNameBeforeDate` (formerly `MonthNameMiddleEndianParser`) for month-first formats (e.g., "January 20").
- `MonthNameBeforeYear` for month-before-year formats (e.g., "January 2012").
- `MonthNameAfterYear` for year-before-month formats (e.g., "2012 January").
- `JAYearMonthDateParser` (formerly `JPStandardParser`) for year-month-date formats (e.g., "2012年3月31日").
- `JAYearMonthParser` for year-month formats (e.g., "2026年4月").

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
   - **Filters (`common.refiners.AbstractFilter` or `Filter`)**:
     A specialized type of `Refiner` to discard invalid or unlikely matches. Subclasses implement `is_valid(context, result) -> bool` to determine if a candidate `ParsedResult` should be kept.
3. **ParsedResult and ParsedRangeResult (`types.ParsedResult`, `types.ParsedRangeResult`)**:
   Represent the final output structure of the parsing step, containing the matched index, matched text, and a `moment` (plus an optional `end` moment for ranges).
4. **DateTimeMoment and ReferenceMoment (`types.DateTimeMoment`, `types.ReferenceMoment`)**:
   - `DateTimeMoment`: Wraps an absolute datetime (with a specific precision).
   - `ReferenceMoment`: Represents a relative duration shift (e.g., "10 years ago") relative to a reference moment.
5. **CivilTimeMoment and ParsingCivilTimeMoment (`common.types.CivilTimeMoment`, `common.types.ParsingCivilTimeMoment`)**:
   - `CivilTimeMoment` (immutable) inherits from `DateTimeMoment` and tracks date/time components as either `known_values` (explicitly present in match) or `implied_values` (implied from reference date or other clues).
   - `ParsingCivilTimeMoment` (mutable subclass) is used during the parsing/merging phase.
   - Use `ParsingCivilTimeMoment.of(reference, precision=None)` (overriding `DateTimeMoment.of`) to initialize moments from a reference moment/datetime. `.of()` inspects the reference precision (or target `precision`) and implies component details accordingly.
   - Calling `.freeze()` on a mutable moment returns an immutable `CivilTimeMoment`, while `.to_mutable()` returns a mutable instance.
   - `precision()` only considers components in `known_values` (certain components) and falls back to `super().precision()` (the reference precision) if no components are known. If both are `None`, it raises `ValueError`.
   - `CivilTimeComponent.MERIDIEM` maps to `DateTimePrecision.DAY` (since meridiem alone does not specify an hour and should only lead to day-level precision).
   - Helper methods are provided for copying components while respecting target precision:
     - `assign_similar_date(target)` / `imply_similar_date(target)`
     - `assign_similar_time(target)` / `imply_similar_time(target)`

---

## Key Context & Caveats

1. **Feature parity with TypeScript Chrono**:
   The Python version is currently a simplified, work-in-progress port of the JS/TS library. Options like `forwardDate` or a separate `GB` locale structure are not yet implemented.

2. **Pattern Compilation & Options**:
   Avoid storing static, global compiled regexes (e.g. `PATTERN = re.compile(...)`) at the module level when they depend on configuration flags (like `allow_abbreviations` or `allow_casual_suffix`).
   Instead:
   - Define a file-local helper `compile_pattern(...)` that accepts option flags and returns a compiled `re.Pattern`.
   - Call `compile_pattern` inside the parser class's constructor `__init__` and store the result as `self._pattern`.
   - Do not name the attribute `self.pattern` because it shadows the inherited `pattern()` method.

3. **Full-Width Normalization (`to_hankaku`)**:
   Full-width character normalization is centrally located in `chrono_python.utils.patterns.to_hankaku`. Locale parsers and common parsers should import `to_hankaku` directly from `utils.patterns`.

4. **Unicode Word Boundaries in Regex**:
   In Python 3 regex, `\w` matches all Unicode word characters (including Japanese hiragana, katakana, and kanji such as `の`). Avoid using `\W` to demarcate word boundaries in non-English text; use non-digit lookahead `(?=[^\d０-９]|$)` or explicit character sets instead.

5. **Reusing Common Parsers & Refiners**:
   Common parsers and refiners (e.g., `SlashYearMonthDateParser(strict_month_date_order=True)`) should be instantiated directly in locale configurations with appropriate options/flags, rather than creating redundant locale-specific subclasses when no custom logic is needed.

---

## Git & Commit Message Format

Follow the existing commit message format conventions:
- Use prefix `New:` for new features or implementations (e.g. `New: Time expr parsing`, `New: Merge date range refiners`).
- Use prefix `New: (Locale)` for locale-specific features or implementations (e.g. `New: (JA) Setup Japanese merge date range refiner`).
- Use prefix `Refactor:` for code cleanups or refactoring changes (e.g. `Refactor: Introduce CivilTime concept`).
- Use prefix `Add:` or `Fix:` if adding tests or fixing issues (e.g. `Add test for parsers`).

---

## AI Agent Tool & Command Guidelines

To ensure secure, auditable, and standard operations:
- **Network Requests**: Do not run casual python commands to execute network calls (e.g. `python3 -c "import urllib..."`). Instead, use standard tools like `curl -L -k` or `wget`.
- **Code Execution**: Do not run temporary python code snippets locally to check outputs or verify states. Modify the workspace code directly and use the proper verification tools (e.g. `uv run pytest`).



