import datetime
import chrono_python as chrono
from chrono_python.common.types import CivilTimeComponent

def test_iso_format_date_only():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = chrono.parse('1994-11-05', ref_date)
    assert len(results) == 1
    assert results[0].text == '1994-11-05'
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 1994
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 11
    assert results[0].moment.get(CivilTimeComponent.DAY) == 5
    assert results[0].moment.get(CivilTimeComponent.HOUR) is None

def test_iso_format_date_time_timezone():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # 1994-11-05T08:15:30-05:30
    results = chrono.parse('1994-11-05T08:15:30-05:30', ref_date)
    assert len(results) == 1
    assert results[0].text == '1994-11-05T08:15:30-05:30'
    moment = results[0].moment
    assert moment.get(CivilTimeComponent.YEAR) == 1994
    assert moment.get(CivilTimeComponent.MONTH) == 11
    assert moment.get(CivilTimeComponent.DAY) == 5
    assert moment.get(CivilTimeComponent.HOUR) == 8
    assert moment.get(CivilTimeComponent.MINUTE) == 15
    assert moment.get(CivilTimeComponent.SECOND) == 30
    assert moment.get(CivilTimeComponent.TIMEZONE_OFFSET) == -330 # -5 hours 30 mins = -330 mins

    # 1994-11-05T08:15:30Z
    results = chrono.parse('1994-11-05T08:15:30Z', ref_date)
    assert len(results) == 1
    assert results[0].text == '1994-11-05T08:15:30Z'
    assert results[0].moment.get(CivilTimeComponent.TIMEZONE_OFFSET) == 0

    # 1994-11-05T08:15:30.123Z
    results = chrono.parse('1994-11-05T08:15:30.123Z', ref_date)
    assert len(results) == 1
    assert results[0].text == '1994-11-05T08:15:30.123Z'
    assert results[0].moment.get(CivilTimeComponent.MILLI_SECOND) == 123
    assert results[0].moment.get(CivilTimeComponent.TIMEZONE_OFFSET) == 0
