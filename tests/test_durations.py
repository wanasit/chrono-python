from chrono_python.common.durations import normalize_duration
from chrono_python.types import Timeunit


def test_normalize_duration_empty():
    assert normalize_duration({}) == {}


def test_normalize_duration_whole_units():
    fragments = {
        Timeunit.YEAR: 1.0,
        Timeunit.MONTH: 2.0,
        Timeunit.WEEK: 3.0,
        Timeunit.DAY: 4.0,
        Timeunit.HOUR: 5.0,
        Timeunit.MINUTE: 6.0,
        Timeunit.SECOND: 7.0,
        Timeunit.MILLI_SECOND: 800.0,
    }
    result = normalize_duration(fragments)
    assert result == {
        Timeunit.YEAR: 1,
        Timeunit.MONTH: 2,
        Timeunit.WEEK: 3,
        Timeunit.DAY: 4,
        Timeunit.HOUR: 5,
        Timeunit.MINUTE: 6,
        Timeunit.SECOND: 7,
        Timeunit.MILLI_SECOND: 800,
    }


def test_normalize_duration_quarter():
    assert normalize_duration({Timeunit.QUARTER: 1.0}) == {Timeunit.MONTH: 3}
    assert normalize_duration({"quarter": 2.0}) == {Timeunit.MONTH: 6}


def test_normalize_duration_fractional_carryover():
    # 1.5 years = 1 year, 6 months
    assert normalize_duration({Timeunit.YEAR: 1.5}) == {
        Timeunit.YEAR: 1,
        Timeunit.MONTH: 6,
    }

    # 1.5 hours = 1 hour, 30 minutes
    assert normalize_duration({Timeunit.HOUR: 1.5}) == {
        Timeunit.HOUR: 1,
        Timeunit.MINUTE: 30,
    }

    # 0.5 seconds = 500 milliseconds
    assert normalize_duration({Timeunit.SECOND: 0.5}) == {
        Timeunit.MILLI_SECOND: 500,
    }
