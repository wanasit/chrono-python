import datetime
import chrono_python as chrono

from chrono_python.types import DateTimePrecision, DateTimeMoment
from chrono_python.common.types import CivilTimeComponent, Meridiem


def test_simple_time_parsing():
    ref_date = datetime.datetime(2020, 1, 1, 12, 0)
    
    # 1:30
    results = chrono.parse('1:30', ref_date)
    assert len(results) == 1
    assert results[0].text == '1:30'
    assert results[0].moment.get(CivilTimeComponent.HOUR) == 1
    assert results[0].moment.get(CivilTimeComponent.MINUTE) == 30
    assert results[0].moment.get(CivilTimeComponent.MERIDIEM) == Meridiem.AM
    
    # 1:30pm
    results = chrono.parse('1:30pm', ref_date)
    assert len(results) == 1
    assert results[0].text == '1:30pm'
    assert results[0].moment.get(CivilTimeComponent.HOUR) == 13
    assert results[0].moment.get(CivilTimeComponent.MINUTE) == 30
    assert results[0].moment.get(CivilTimeComponent.MERIDIEM) == Meridiem.PM

    # 1:30am
    results = chrono.parse('1:30am', ref_date)
    assert len(results) == 1
    assert results[0].text == '1:30am'
    assert results[0].moment.get(CivilTimeComponent.HOUR) == 1
    assert results[0].moment.get(CivilTimeComponent.MINUTE) == 30
    assert results[0].moment.get(CivilTimeComponent.MERIDIEM) == Meridiem.AM


def test_time_with_seconds_and_milliseconds():
    ref_date = datetime.datetime(2020, 1, 1, 12, 0)
    
    # 1:30:45
    results = chrono.parse('1:30:45', ref_date)
    assert len(results) == 1
    assert results[0].text == '1:30:45'
    assert results[0].moment.get(CivilTimeComponent.HOUR) == 1
    assert results[0].moment.get(CivilTimeComponent.MINUTE) == 30
    assert results[0].moment.get(CivilTimeComponent.SECOND) == 45
    assert results[0].moment.get(CivilTimeComponent.MILLI_SECOND) is None

    # 1:30:45.123
    results = chrono.parse('1:30:45.123', ref_date)
    assert len(results) == 1
    assert results[0].text == '1:30:45.123'
    assert results[0].moment.get(CivilTimeComponent.HOUR) == 1
    assert results[0].moment.get(CivilTimeComponent.MINUTE) == 30
    assert results[0].moment.get(CivilTimeComponent.SECOND) == 45
    assert results[0].moment.get(CivilTimeComponent.MILLI_SECOND) == 123


def test_time_suffixes():
    ref_date = datetime.datetime(2020, 1, 1, 12, 0)

    # 8:00 o'clock
    results = chrono.parse("8:00 o'clock", ref_date)
    assert len(results) == 1
    assert results[0].text == "8:00 o'clock"
    assert results[0].moment.get(CivilTimeComponent.HOUR) == 8

    # 1:30 in the morning
    results = chrono.parse('1:30 in the morning', ref_date)
    assert len(results) == 1
    assert results[0].text == '1:30 in the morning'
    assert results[0].moment.get(CivilTimeComponent.HOUR) == 1
    assert results[0].moment.get(CivilTimeComponent.MERIDIEM) == Meridiem.AM

    # 3:15 in the afternoon
    results = chrono.parse('3:15 in the afternoon', ref_date)
    assert len(results) == 1
    assert results[0].text == '3:15 in the afternoon'
    assert results[0].moment.get(CivilTimeComponent.HOUR) == 15
    assert results[0].moment.get(CivilTimeComponent.MERIDIEM) == Meridiem.PM

    # 8:00 at night
    results = chrono.parse('8:00 at night', ref_date)
    assert len(results) == 1
    assert results[0].text == '8:00 at night'
    assert results[0].moment.get(CivilTimeComponent.HOUR) == 20
    assert results[0].moment.get(CivilTimeComponent.MERIDIEM) == Meridiem.PM


def test_time_ranges():
    ref_date = datetime.datetime(2020, 1, 1, 12, 0)

    # 1:30-12:10
    results = chrono.parse('1:30-12:10', ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == '1:30-12:10'
    assert result.start.get(CivilTimeComponent.HOUR) == 1
    assert result.start.get(CivilTimeComponent.MINUTE) == 30
    assert result.end.get(CivilTimeComponent.HOUR) == 12
    assert result.end.get(CivilTimeComponent.MINUTE) == 10

    # 1:30-2:10pm
    results = chrono.parse('1:30-2:10pm', ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == '1:30-2:10pm'
    assert result.start.get(CivilTimeComponent.HOUR) == 13
    assert result.start.get(CivilTimeComponent.MINUTE) == 30
    assert result.end.get(CivilTimeComponent.HOUR) == 14
    assert result.end.get(CivilTimeComponent.MINUTE) == 10


def test_cross_midnight_ranges():
    # 10:00pm - 1:00am
    ref_date = datetime.datetime(2020, 1, 1, 12, 0)
    results = chrono.parse('10:00pm - 1:00am', ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == '10:00pm - 1:00am'
    assert result.start.get(CivilTimeComponent.HOUR) == 22
    assert result.start.get(CivilTimeComponent.DAY) == 1
    assert result.end.get(CivilTimeComponent.HOUR) == 1
    assert result.end.get(CivilTimeComponent.DAY) == 2


def test_exclusions_and_strict_mode():
    ref_date = datetime.datetime(2020, 1, 1, 12, 0)

    # Single digit should be excluded
    assert len(chrono.parse('1', ref_date)) == 0

    # Year-like number should be excluded without prefix/suffix
    assert len(chrono.parse('2014', ref_date)) == 0

    # Ending with a or p like '123p' should be excluded
    assert len(chrono.parse('123p', ref_date)) == 0

    # Ending with invalid range numbers above 24 (e.g. at 25)
    assert len(chrono.parse('at 25', ref_date)) == 0
