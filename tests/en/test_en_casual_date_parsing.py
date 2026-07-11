import datetime
import chrono_python as chrono
from chrono_python.types import DateTimePrecision
from chrono_python.common.types import CivilTimeComponent

def test_casual_date_expressions():
    ref_date = datetime.datetime(2012, 8, 9, 12, 0)

    # today
    results = chrono.parse('today', ref_date)
    assert len(results) == 1
    assert results[0].text == 'today'
    assert results[0].moment.datetime() == datetime.datetime(2012, 8, 9, 12, 0)
    assert results[0].moment.precision() == DateTimePrecision.DAY
    assert results[0].moment.is_certain(CivilTimeComponent.DAY)
    assert results[0].moment.is_certain(CivilTimeComponent.MONTH)
    assert results[0].moment.is_certain(CivilTimeComponent.YEAR)
    assert not results[0].moment.is_certain(CivilTimeComponent.HOUR)

    # tomorrow
    results = chrono.parse('tomorrow', ref_date)
    assert len(results) == 1
    assert results[0].text == 'tomorrow'
    assert results[0].moment.datetime() == datetime.datetime(2012, 8, 10, 12, 0)
    assert results[0].moment.precision() == DateTimePrecision.DAY

    # tmr / tmrw
    results = chrono.parse('tmr', ref_date)
    assert len(results) == 1
    assert results[0].text == 'tmr'
    assert results[0].moment.datetime() == datetime.datetime(2012, 8, 10, 12, 0)
    assert results[0].moment.precision() == DateTimePrecision.DAY

    results = chrono.parse('tmrw', ref_date)
    assert len(results) == 1
    assert results[0].text == 'tmrw'
    assert results[0].moment.datetime() == datetime.datetime(2012, 8, 10, 12, 0)
    assert results[0].moment.precision() == DateTimePrecision.DAY

    # yesterday
    results = chrono.parse('yesterday', ref_date)
    assert len(results) == 1
    assert results[0].text == 'yesterday'
    assert results[0].moment.datetime() == datetime.datetime(2012, 8, 8, 12, 0)
    assert results[0].moment.precision() == DateTimePrecision.DAY

    # tonight
    results = chrono.parse('tonight', ref_date)
    assert len(results) == 1
    assert results[0].text == 'tonight'
    assert results[0].moment.datetime() == datetime.datetime(2012, 8, 9, 22, 0)
    assert results[0].moment.precision() == DateTimePrecision.DAY
    assert not results[0].moment.is_certain(CivilTimeComponent.HOUR)

    # now
    results = chrono.parse('now', ref_date)
    assert len(results) == 1
    assert results[0].text == 'now'
    assert results[0].moment.datetime() == datetime.datetime(2012, 8, 9, 12, 0)
    assert results[0].moment.precision() == DateTimePrecision.MILLI_SECOND
    assert results[0].moment.is_certain(CivilTimeComponent.HOUR)
    assert results[0].moment.is_certain(CivilTimeComponent.MINUTE)

    # overmorrow
    results = chrono.parse('overmorrow', ref_date)
    assert len(results) == 1
    assert results[0].text == 'overmorrow'
    assert results[0].moment.datetime() == datetime.datetime(2012, 8, 11, 12, 0)
    assert results[0].moment.precision() == DateTimePrecision.DAY


def test_casual_date_last_night():
    # If ref_date is past 6 AM (e.g. 12:00 PM)
    ref_date_noon = datetime.datetime(2012, 8, 9, 12, 0)
    results = chrono.parse('last night', ref_date_noon)
    assert len(results) == 1
    assert results[0].text == 'last night'
    # Should point to last night (Aug 8, 00:00:00 / midnight)
    assert results[0].moment.datetime() == datetime.datetime(2012, 8, 8, 0, 0)
    assert results[0].moment.precision() == DateTimePrecision.DAY

    # If ref_date is early morning (e.g. 3:00 AM)
    ref_date_early = datetime.datetime(2012, 8, 9, 3, 0)
    results = chrono.parse('last night', ref_date_early)
    assert len(results) == 1
    assert results[0].text == 'last night'
    # Should point to last night (Aug 8, 00:00:00)
    assert results[0].moment.datetime() == datetime.datetime(2012, 8, 9, 0, 0)
    assert results[0].moment.precision() == DateTimePrecision.DAY


def test_strict_vs_casual():
    ref_date = datetime.datetime(2012, 8, 9, 12, 0)

    # Casual configuration should parse "today"
    assert len(chrono.en.casual.parse('today', ref_date)) == 1

    # Strict configuration should NOT parse "today"
    assert len(chrono.en.strict.parse('today', ref_date)) == 0
