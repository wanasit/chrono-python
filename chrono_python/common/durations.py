import math
from typing import Mapping

from chrono_python.types import Timeunit


def normalize_duration(fragments: Mapping[Timeunit | str, float]) -> dict[Timeunit, int]:
    """Normalize a mapping of time unit quantities into integer time units.

    Handles conversion of quarters into months (1 quarter = 3 months) and cascades
    fractional remainders down to smaller time units (e.g., 1.5 years -> 1 year, 6 months).

    Args:
        fragments: A mapping of Timeunit keys (or 'quarter') to float quantities.

    Returns:
        A dictionary mapping Timeunit enums to their integer amounts, omitting zero values.
    """
    quarter_val = fragments.get(Timeunit.QUARTER, 0.0) + fragments.get("quarter", 0.0)

    years = fragments.get(Timeunit.YEAR, 0.0)
    months = fragments.get(Timeunit.MONTH, 0.0) + quarter_val * 3.0
    weeks = fragments.get(Timeunit.WEEK, 0.0)
    days = fragments.get(Timeunit.DAY, 0.0)
    hours = fragments.get(Timeunit.HOUR, 0.0)
    minutes = fragments.get(Timeunit.MINUTE, 0.0)
    seconds = fragments.get(Timeunit.SECOND, 0.0)
    milliseconds = fragments.get(Timeunit.MILLI_SECOND, 0.0)

    floor_years = math.floor(years)
    rem_years = years - floor_years
    if rem_years > 0:
        months += rem_years * 12.0

    floor_months = math.floor(months)
    rem_months = months - floor_months
    if rem_months > 0:
        weeks += rem_months * 4.0

    floor_weeks = math.floor(weeks)
    rem_weeks = weeks - floor_weeks
    if rem_weeks > 0:
        days += rem_weeks * 7.0

    floor_days = math.floor(days)
    rem_days = days - floor_days
    if rem_days > 0:
        hours += rem_days * 24.0

    floor_hours = math.floor(hours)
    rem_hours = hours - floor_hours
    if rem_hours > 0:
        minutes += rem_hours * 60.0

    floor_minutes = math.floor(minutes)
    rem_minutes = minutes - floor_minutes
    if rem_minutes > 0:
        seconds += rem_minutes * 60.0

    floor_seconds = math.floor(seconds)
    rem_seconds = seconds - floor_seconds
    if rem_seconds > 0:
        milliseconds += rem_seconds * 1000.0

    floor_milliseconds = math.floor(milliseconds)

    result: dict[Timeunit, int] = {}
    if floor_years != 0:
        result[Timeunit.YEAR] = int(floor_years)
    if floor_months != 0:
        result[Timeunit.MONTH] = int(floor_months)
    if floor_weeks != 0:
        result[Timeunit.WEEK] = int(floor_weeks)
    if floor_days != 0:
        result[Timeunit.DAY] = int(floor_days)
    if floor_hours != 0:
        result[Timeunit.HOUR] = int(floor_hours)
    if floor_minutes != 0:
        result[Timeunit.MINUTE] = int(floor_minutes)
    if floor_seconds != 0:
        result[Timeunit.SECOND] = int(floor_seconds)
    if floor_milliseconds != 0:
        result[Timeunit.MILLI_SECOND] = int(floor_milliseconds)

    return result
