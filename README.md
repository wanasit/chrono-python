# Chrono Python (v3)
A natural language date parser. 

A Python version of [chrono](https://github.com/wanasit/chrono) (originally written in Javascript), featuring a recent design and refined architecture. It identifies and extracts dates, times, and relative date expressions from free text without relying on external dependencies.

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
pip install chrono-python
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

### Locale Support

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

### Casual vs. Strict Modes

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

## Advanced Usage

### Parsed Results and Moments

When calling `chrono.parse(text)`, Chrono returns a list of `ParsedResult` objects (or `ParsedRangeResult` for date ranges).

#### ParsedResult & ParsedRangeResult

A `ParsedResult` represents a matched date expression within the input text and provides the following properties:

* **`index`**: The zero-based starting character position of the match in the input string.
* **`text`**: The exact substring matched from the input.
* **`start`** (or **`moment`**): The `Moment` object representing the parsed start date and time.
* **`datetime()`**: A convenience method returning the Python `datetime.datetime` object of the start moment.
* **`precision()`**: A convenience method returning the `DateTimePrecision` enum value of the start moment.

When a date range is parsed (e.g., *"August 10 to August 15, 2026"*), Chrono returns a `ParsedRangeResult` which includes an additional property:

* **`end`**: The `Moment` object representing the parsed end date and time.

```python
import chrono_python as chrono

results = chrono.parse("Meeting from 9:00am to 11:30am on Friday")
result = results[0]

print(result.index)        # 8
print(result.text)         # "9:00am to 11:30am on Friday"
print(result.datetime())   # 2026-08-21 09:00:00
print(result.precision())  # DateTimePrecision.MINUTE

if isinstance(result, chrono.ParsedRangeResult):
    print("Start:", result.start.datetime())  # 2026-08-21 09:00:00
    print("End:  ", result.end.datetime())    # 2026-08-21 11:30:00
```

#### The `Moment` Abstraction

`Moment` is the core abstraction representing an extracted point in time. It provides a consistent interface across different kinds of date expressions:

* **`moment.datetime() -> datetime.datetime`**: Converts the moment into a standard Python `datetime.datetime` object. For date-only expressions (where no time is specified), the time component defaults to 12:00 PM (noon).
* **`moment.precision() -> DateTimePrecision`**: Returns the level of precision of the extracted moment (see [Date & Time Precision](#date--time-precision)).

Under the hood, Chrono uses specialized `Moment` subclasses:
* **`DateTimeMoment`**: Represents an absolute point in time with a fixed precision.
* **`ReferenceMoment`**: Represents a relative duration offset from a reference date (e.g., *"5 days ago"* or *"in 2 weeks"*).
* **`CivilTimeMoment`**: Represents a calendar-component date/time tracking which components were explicitly stated (*certain*) vs. inferred (*implied*).

#### Civil Time and Components

Natural language date expressions rarely specify all date and clock fields. When parsing *"August 17 at 8:00"*, the month, day, hour, and minute are explicitly stated, but the year is inferred from the reference date.

Chrono represents this with `CivilTimeMoment`, separating fields into **known (certain) values** and **implied values**:

* **Certain / Known Values**: Components explicitly found in the parsed text (e.g., `"August"` -> month 8, `"17"` -> day 17).
* **Implied Values**: Components inferred from context, the reference date, or sensible defaults (e.g., the reference year or noon for date-only inputs).

You can import `CivilTimeComponent` from `chrono_python.common.types` to query individual fields and check certainty:

```python
import chrono_python as chrono
from chrono_python.common.types import CivilTimeComponent

results = chrono.parse("August 17 at 8:00")
moment = results[0].start

# Query component values (accepts enum or string)
print(moment.get(CivilTimeComponent.MONTH))  # 8
print(moment.get(CivilTimeComponent.DAY))    # 17
print(moment.get(CivilTimeComponent.HOUR))   # 8
print(moment.get(CivilTimeComponent.YEAR))   # 2026 (inferred from reference)

# Check certainty (whether it was explicitly mentioned in text)
print(moment.is_certain(CivilTimeComponent.DAY))   # True
print(moment.is_certain(CivilTimeComponent.YEAR))  # False

# List all explicitly stated components
print(moment.list(only_certain=True))
# [<CivilTimeComponent.MONTH: 'month'>, <CivilTimeComponent.DAY: 'day'>, <CivilTimeComponent.HOUR: 'hour'>, <CivilTimeComponent.MINUTE: 'minute'>]

# Helper query and validation methods
print(moment.is_only_date())               # False (contains time)
print(moment.is_date_with_unknown_year())  # True (month/day known, year implied)
print(moment.is_valid_date())              # True (validates calendar constraints & leap days)
```

### Date & Time Precision

Unlike standard Python `datetime` objects—which require year, month, day, hour, minute, and second, implicitly defaulting missing fields—Chrono preserves the exact granularity of the user's input through the `DateTimePrecision` enum.

Every `ParsedResult` and `Moment` provides `.precision()` indicating how fine-grained the matched input text was.

#### Precision Levels

`DateTimePrecision` defines the following levels in increasing order of granularity:

| Level | Value | Example Expression | Description |
| :--- | :---: | :--- | :--- |
| `YEAR` | 10 | *"in 2026"* | Only the year was specified |
| `MONTH` | 20 | *"August 2026"* | Specified down to the month |
| `WEEK` | 30 | *"next week"* | Specified as a week |
| `DAY` | 40 | *"August 17, 2026"*, *"today"* | Specified down to the day (date only) |
| `HOUR` | 50 | *"at 6pm"*, *"18:00"* | Specified down to the hour |
| `MINUTE` | 60 | *"at 18:40"*, *"8:15 AM"* | Specified down to the minute |
| `SECOND` | 70 | *"18:40:25"* | Specified down to the second |
| `MILLI_SECOND` | 80 | *"18:40:25.123"* | Specified down to milliseconds |

#### Using Precision in Your Application

You can use precision values to determine whether the user provided a specific time of day or only a general date:

```python
import chrono_python as chrono
from chrono_python.types import DateTimePrecision

results = chrono.parse("Let's meet on August 17 at 18:40")
result = results[0]

# Check if the user specified time-of-day information
if result.precision().value >= DateTimePrecision.HOUR.value:
    print(f"Specific meeting time: {result.datetime().strftime('%Y-%m-%d %H:%M')}")
else:
    print(f"All-day date: {result.datetime().strftime('%Y-%m-%d')}")
```

