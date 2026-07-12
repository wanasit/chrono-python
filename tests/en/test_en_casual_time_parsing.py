import datetime
import chrono_python as chrono
from chrono_python.types import DateTimePrecision
from chrono_python.common.types import CivilTimeComponent, Meridiem

def test_en_casual_time_parsing():
    ref_date = datetime.datetime(2016, 10, 1, 8, 0)

    # morning
    results = chrono.parse('morning', ref_date)
    assert len(results) == 1
    assert results[0].text == 'morning'
    assert results[0].moment.datetime().hour == 6
    assert results[0].moment.datetime().minute == 0
    assert results[0].moment.get(CivilTimeComponent.MERIDIEM) == Meridiem.AM
    assert not results[0].moment.is_certain(CivilTimeComponent.HOUR)
    assert results[0].moment.precision() == DateTimePrecision.DAY

    # this morning
    results = chrono.parse('this morning', ref_date)
    assert len(results) == 1
    assert results[0].text == 'this morning'
    assert results[0].moment.datetime().hour == 6
    assert results[0].moment.precision() == DateTimePrecision.DAY

    # afternoon
    results = chrono.parse('afternoon', ref_date)
    assert len(results) == 1
    assert results[0].text == 'afternoon'
    assert results[0].moment.datetime().hour == 15
    assert results[0].moment.get(CivilTimeComponent.MERIDIEM) == Meridiem.PM
    assert not results[0].moment.is_certain(CivilTimeComponent.HOUR)
    assert results[0].moment.precision() == DateTimePrecision.DAY

    # evening
    results = chrono.parse('evening', ref_date)
    assert len(results) == 1
    assert results[0].text == 'evening'
    assert results[0].moment.datetime().hour == 20
    assert results[0].moment.get(CivilTimeComponent.MERIDIEM) == Meridiem.PM
    assert results[0].moment.precision() == DateTimePrecision.DAY

    # night
    results = chrono.parse('night', ref_date)
    assert len(results) == 1
    assert results[0].text == 'night'
    assert results[0].moment.datetime().hour == 20
    assert results[0].moment.precision() == DateTimePrecision.DAY

    # noon
    results = chrono.parse('noon', ref_date)
    assert len(results) == 1
    assert results[0].text == 'noon'
    assert results[0].moment.datetime().hour == 12
    assert results[0].moment.get(CivilTimeComponent.MERIDIEM) == Meridiem.AM
    assert results[0].moment.is_certain(CivilTimeComponent.HOUR)
    assert results[0].moment.precision() == DateTimePrecision.HOUR

    # midday
    results = chrono.parse('midday', ref_date)
    assert len(results) == 1
    assert results[0].text == 'midday'
    assert results[0].moment.datetime().hour == 12
    assert results[0].moment.get(CivilTimeComponent.MERIDIEM) == Meridiem.AM
    assert results[0].moment.is_certain(CivilTimeComponent.HOUR)
    assert results[0].moment.precision() == DateTimePrecision.HOUR


def test_en_casual_time_midnight():
    # If reference hour is > 2 (e.g. 8:00 AM)
    ref_date_day = datetime.datetime(2016, 10, 1, 8, 0)
    results = chrono.parse('midnight', ref_date_day)
    assert len(results) == 1
    assert results[0].text == 'midnight'
    # Should point to tomorrow's midnight (Oct 2, 00:00:00)
    assert results[0].moment.datetime() == datetime.datetime(2016, 10, 2, 0, 0)
    assert results[0].moment.is_certain(CivilTimeComponent.HOUR)
    assert results[0].moment.get(CivilTimeComponent.HOUR) == 0
    assert results[0].moment.precision() == DateTimePrecision.HOUR

    # If reference hour is <= 2 (e.g. 1:00 AM)
    ref_date_early = datetime.datetime(2016, 10, 1, 1, 0)
    results = chrono.parse('midnight', ref_date_early)
    assert len(results) == 1
    assert results[0].text == 'midnight'
    # Should point to today's midnight (Oct 1, 00:00:00)
    assert results[0].moment.datetime() == datetime.datetime(2016, 10, 1, 0, 0)
    assert results[0].moment.precision() == DateTimePrecision.HOUR


def test_en_strict_vs_casual_time():
    ref_date = datetime.datetime(2016, 10, 1, 8, 0)

    # Casual configuration should parse "morning"
    assert len(chrono.en.casual.parse('morning', ref_date)) == 1

    # Strict configuration should NOT parse "morning"
    assert len(chrono.en.strict.parse('morning', ref_date)) == 0
