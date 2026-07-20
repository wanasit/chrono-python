import datetime
from datetime import timedelta
from chrono_python.types import Moment, DateTimeMoment, Weekday
from chrono_python.common.types import CivilTimeMoment, ParsingCivilTimeMoment, CivilTimeComponent

def create_parsing_components_at_weekday(
    reference: Moment,
    weekday: int,  # 0 is Sunday, 1 is Monday, ..., 6 is Saturday
    modifier: str | None = None
) -> ParsingCivilTimeMoment:
    """
    Returns the parsing components at the weekday (considering the modifier).
    The time and timezone is assumed to be similar to the reference.
    """
    ref_dt = reference.datetime()
    days_to_weekday = get_days_to_weekday(ref_dt, weekday, modifier)

    # Calculate the target datetime by shifting by the calculated days
    target_dt = ref_dt + timedelta(days=days_to_weekday)

    moment = ParsingCivilTimeMoment(reference, {})
    moment.imply(CivilTimeComponent.YEAR, target_dt.year)
    moment.imply(CivilTimeComponent.MONTH, target_dt.month)
    moment.imply(CivilTimeComponent.DAY, target_dt.day)
    moment.assign(CivilTimeComponent.WEEKDAY, weekday)

    return moment


def get_days_to_weekday(ref_dt, weekday: int, modifier: str | None = None) -> int:
    """
    Returns number of days from ref_dt to the weekday.
    """
    ref_weekday = (ref_dt.weekday() + 1) % 7  # Convert Python weekday (Mon=0..Sun=6) to JS (Sun=0..Sat=6)
    
    if modifier == "this":
        return get_days_forward_to_weekday(ref_dt, weekday)
    elif modifier == "last":
        return get_backward_days_to_weekday(ref_dt, weekday)
    elif modifier == "next":
        # From Sunday, the next Sunday is 7 days later.
        # Otherwise, next Mon is 1 days later, next Tues is 2 days later, and so on...
        if ref_weekday == 0:  # Sunday
            return 7 if weekday == 0 else weekday
            
        # From Saturday, the next Saturday is 7 days later, the next Sunday is 8-days later.
        # Otherwise, next Mon is (1 + 1) days later, next Tues is (1 + 2) days later, and so on...
        if ref_weekday == 6:  # Saturday
            if weekday == 6:
                return 7
            if weekday == 0:
                return 8
            return 1 + weekday
            
        # From weekdays, next Mon is the following week's Mon, next Tues the following week's Tues, and so on...
        # If the week's weekday already passed (weekday < ref_weekday), we simply count forward to next week.
        # Otherwise, count forward to this week, then add another 7 days.
        if weekday < ref_weekday and weekday != 0:
            return get_days_forward_to_weekday(ref_dt, weekday)
        else:
            return get_days_forward_to_weekday(ref_dt, weekday) + 7

    return get_days_to_weekday_closest(ref_dt, weekday)


def get_days_to_weekday_closest(ref_dt, weekday: int) -> int:
    backward = get_backward_days_to_weekday(ref_dt, weekday)
    forward = get_days_forward_to_weekday(ref_dt, weekday)
    return forward if forward < -backward else backward


def get_days_forward_to_weekday(ref_dt, weekday: int) -> int:
    ref_weekday = (ref_dt.weekday() + 1) % 7
    forward_count = weekday - ref_weekday
    if forward_count < 0:
        forward_count += 7
    return forward_count


def get_backward_days_to_weekday(ref_dt, weekday: int) -> int:
    ref_weekday = (ref_dt.weekday() + 1) % 7
    backward_count = weekday - ref_weekday
    if backward_count >= 0:
        backward_count -= 7
    return backward_count


def nth_weekday_of_month(year: int, month: int, weekday: Weekday, n: int, hour: int = 0) -> CivilTimeMoment:
    """
    Return day-level precision moment at the date.
    """
    weekday_val = weekday.value
    day_of_month = 0
    i = 0
    while i < n:
        day_of_month += 1
        dt = datetime.datetime(year, month, day_of_month)
        dt_weekday = (dt.weekday() + 1) % 7
        if dt_weekday == weekday_val:
            i += 1

    target_dt = datetime.datetime(year, month, day_of_month, hour)
    ref = DateTimeMoment.of(target_dt)
    known = {
        CivilTimeComponent.YEAR: year,
        CivilTimeComponent.MONTH: month,
        CivilTimeComponent.DAY: day_of_month,
    }
    implied = {
        CivilTimeComponent.HOUR: hour
    }
    return CivilTimeMoment(ref, known, implied)


def last_weekday_of_month(year: int, month: int, weekday: Weekday, hour: int = 0) -> CivilTimeMoment:
    """
    Return day-level precision moment at the date.
    """
    weekday_val = weekday.value
    one_indexed_weekday = 7 if weekday_val == 0 else weekday_val
    if month == 12:
        next_month_year = year + 1
        next_month = 1
    else:
        next_month_year = year
        next_month = month + 1

    next_month_first = datetime.datetime(next_month_year, next_month, 1, 12)
    first_weekday_next_month = next_month_first.weekday() + 1
    
    if first_weekday_next_month == one_indexed_weekday:
        day_diff = 7
    elif first_weekday_next_month < one_indexed_weekday:
        day_diff = 7 + first_weekday_next_month - one_indexed_weekday
    else:
        day_diff = first_weekday_next_month - one_indexed_weekday

    target_date = next_month_first - datetime.timedelta(days=day_diff)
    day_of_month = target_date.day

    target_dt = datetime.datetime(year, month, day_of_month, hour)
    ref = DateTimeMoment.of(target_dt)
    known = {
        CivilTimeComponent.YEAR: year,
        CivilTimeComponent.MONTH: month,
        CivilTimeComponent.DAY: day_of_month,
    }
    implied = {
        CivilTimeComponent.HOUR: hour
    }
    return CivilTimeMoment(ref, known, implied)
