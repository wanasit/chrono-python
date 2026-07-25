import datetime
import pytest

from chrono_python.types import (
    DateTimeMoment,
    DateTimePrecision,
    ParsedRangeResult,
    ParsedResult,
    ReferenceMoment,
    Timeunit,
    Weekday,
)


def test_date_time_moment():
    dt = datetime.datetime(2026, 5, 31, 14, 30, 0)
    moment = DateTimeMoment.of(dt, DateTimePrecision.MINUTE)

    assert moment.datetime() == dt
    assert moment.precision() == DateTimePrecision.MINUTE
    assert moment.is_valid_date() is True


def test_date_time_moment_none_precision():
    dt = datetime.datetime(2026, 5, 31, 14, 30, 0)
    with pytest.raises(ValueError, match="DateTimeMoment precision cannot be None"):
        DateTimeMoment.of(dt, None)


def test_date_time_moment_now():
    now_moment = DateTimeMoment.now()
    assert isinstance(now_moment.datetime(), datetime.datetime)
    assert now_moment.precision() == DateTimePrecision.MILLI_SECOND


def test_reference_moment_with_datetime():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    next_day = ReferenceMoment.of(ref_date, {Timeunit.DAY: 1})
    assert next_day.datetime() == datetime.datetime(2012, 8, 11, 12, 0)
    assert next_day.precision() == DateTimePrecision.DAY


def test_reference_moment_with_datetime_moment():
    ref_dt = datetime.datetime(2012, 8, 10, 12, 0)
    ref_moment = DateTimeMoment.of(ref_dt, DateTimePrecision.MINUTE)
    next_day = ReferenceMoment.of(ref_moment, {Timeunit.DAY: 1})
    assert next_day.datetime() == datetime.datetime(2012, 8, 11, 12, 0)
    assert next_day.precision() == DateTimePrecision.DAY


def test_reference_moment_default_delta():
    ref_dt = datetime.datetime(2026, 5, 31, 14, 30, 0)
    moment = ReferenceMoment.of(ref_dt)
    assert moment.datetime() == ref_dt
    assert moment.precision() == DateTimePrecision.DAY


def test_reference_moment_multiple_units():
    ref_dt = datetime.datetime(2020, 1, 15, 10, 30)
    ref_moment = DateTimeMoment.of(ref_dt, DateTimePrecision.MINUTE)
    shifted = ReferenceMoment.of(
        ref_moment,
        {
            Timeunit.YEAR: 1,
            Timeunit.MONTH: 2,
            Timeunit.DAY: 5,
            Timeunit.HOUR: 3,
        },
    )
    assert shifted.datetime() == datetime.datetime(2021, 3, 20, 13, 30)
    assert shifted.precision() == DateTimePrecision.HOUR


def test_parsed_result():
    dt = datetime.datetime(2026, 7, 26, 9, 0)
    moment = DateTimeMoment.of(dt, DateTimePrecision.HOUR)
    result = ParsedResult(index=5, text="today", moment=moment)

    assert result.index == 5
    assert result.text == "today"
    assert result.moment == moment
    assert result.datetime() == dt


def test_parsed_range_result():
    start_dt = datetime.datetime(2026, 7, 26, 9, 0)
    end_dt = datetime.datetime(2026, 7, 26, 17, 0)
    start_moment = DateTimeMoment.of(start_dt, DateTimePrecision.HOUR)
    end_moment = DateTimeMoment.of(end_dt, DateTimePrecision.HOUR)

    range_result = ParsedRangeResult(
        index=0, text="9am to 5pm", moment=start_moment, end=end_moment
    )

    assert range_result.start == start_moment
    assert range_result.end == end_moment
    assert range_result.datetime() == start_dt