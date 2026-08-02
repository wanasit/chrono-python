# Chrono Python

A natural language date parser for Python.

`chrono-python` is a Python port of [chrono](https://github.com/wanasit/chrono), featuring a recent design and refined architecture tailored for Python. It identifies and extracts dates, times, and relative date expressions from free text without relying on external dependencies.

### Features & Supported Formats
* *Today*, *Tomorrow*, *Yesterday*, *Last Friday*, etc.
* *17 August 2013 - 19 August 2013*
* *This Friday from 13:00 - 16:00*
* *5 days ago*, *2 weeks from now*
* *2014-11-30T08:15:30-05:30*
* Multi-language support: **English (`en`)**, **Japanese (`ja`)**, **French (`fr`)**, **Italian (`it`)**, and **Chinese (`zh`)**.

### Difference from Chrono v2 (Javascript)
While `chrono-python` retains Chrono's core parsing logic and multi-locale design, it introduces a refined architecture tailored for Python:
* **Separation of Date-Time & Reference Abstractions**: Decouples absolute moments, calendar component representations, and relative shifts using `DateTimeMoment`, `CivilTimeMoment`, and `ReferenceMoment`, rather than relying on JavaScript `Date` / `ParsingComponents`.
* **Explicit Precision System**: Tracks the exact level of granularity of every parsed expression (`YEAR`, `MONTH`, `DAY`, `HOUR`, `MINUTE`, `SECOND`, etc.) via `DateTimePrecision`.
* **Descriptive Parser Naming**: Uses positional naming conventions (e.g., `MonthNameBeforeDate`, `MonthNameAfterDate`) rather than endianness terms.

## Installation

Install using pip:

```bash
pip install git+https://github.com/wanasit/chrono-python.git
```

## Usage

Simply pass a string to `chrono.parse` or `chrono.parse_date`:

```python
import chrono_python as chrono

# parse() returns a list of ParsedResult objects
results = chrono.parse("An appointment on Sep 12-13")
# [<ParsedRangeResult "Sep 12-13" : 2026-09-12 12:00:00 -> 2026-09-13 12:00:00>]

# parse_date() returns a standard Python datetime.datetime object (or None)
date = chrono.parse_date("12 June 2026")
# datetime.datetime(2026, 6, 12, 12, 0)
```

### Reference Dates

Relative date expressions like *"Friday"*, *"tomorrow"*, or *"2 days ago"* depend on when they are mentioned. Pass a `reference` datetime to resolve relative expressions against a specific point in time:

```python
import datetime
import chrono_python as chrono

ref_date = datetime.datetime(2012, 8, 23, 12, 0)

# "Friday" following Aug 23, 2012
chrono.parse_date("Friday", reference=ref_date)
# datetime.datetime(2012, 8, 24, 12, 0)

# "2 days ago" relative to Aug 23, 2012
chrono.parse_date("2 days ago", reference=ref_date)
# datetime.datetime(2012, 8, 21, 12, 0)
```

### Date & Time Precision

Every parsed result (or `Moment` object) tracks its precision level via `result.precision()` (or `moment.precision()`), which returns a `DateTimePrecision` enum (`YEAR`, `MONTH`, `DAY`, `HOUR`, `MINUTE`, `SECOND`, etc.). This indicates how fine-grained the matched input text was:

```python
import chrono_python as chrono

results = chrono.parse("August 17, 2013 at 18:40")
result = results[0]

result.precision()
# <DateTimePrecision.MINUTE: 60>

date_only_result = chrono.parse("August 17, 2013")[0]
date_only_result.precision()
# <DateTimePrecision.DAY: 40>
```

## Locale Support

`chrono.parse` defaults to international English. To parse text in other supported languages, access the locale's `casual` or `strict` configuration:

```python
import chrono_python as chrono

# Japanese
chrono.ja.casual.parse("明日5時に")

# French
chrono.fr.casual.parse("demain à 15h")

# Italian
chrono.it.casual.parse("domani alle 15:00")

# Chinese
chrono.zh.casual.parse("明天下午5点")
```

You can also import locale submodules directly:

```python
from chrono_python.locales import ja, fr

results = ja.casual.parse("2026年8月2日")
```

## Casual vs. Strict Modes

Most locales provide two parsing configurations:
- **`casual`**: Parses informal/casual terms (e.g., "today", "tomorrow", "next week", "10m ago") in addition to standard date formats.
- **`strict`**: Parses only formal/strict date expressions (e.g., ISO formats, explicit slash dates, exact month-day patterns).

```python
import chrono_python as chrono

# Casual mode parses relative words
chrono.en.casual.parse("today")   # Returns parsed result for today

# Strict mode ignores informal words
chrono.en.strict.parse("today")   # Returns []
```
