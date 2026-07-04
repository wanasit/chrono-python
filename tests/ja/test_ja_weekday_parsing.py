import datetime
import chrono_python as chrono

from chrono_python.types import DateTimePrecision, DateTimeMoment
from chrono_python.common.types import CivilTimeComponent


def test_single_expression():
    ref_date = datetime.datetime(2016, 9, 2, 12, 0)  # Friday Sept 2, 2016

    # 木曜日 (Thursday)
    results = chrono.ja.parse("木曜日", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "木曜日"
    assert isinstance(results[0].moment, DateTimeMoment)
    assert results[0].moment.datetime() == datetime.datetime(2016, 9, 1, 12, 0)
    assert results[0].moment.precision() == DateTimePrecision.DAY
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2016
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 9
    assert results[0].moment.get(CivilTimeComponent.DAY) == 1
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 4
    assert not results[0].moment.is_certain(CivilTimeComponent.DAY)
    assert not results[0].moment.is_certain(CivilTimeComponent.MONTH)
    assert not results[0].moment.is_certain(CivilTimeComponent.YEAR)
    assert results[0].moment.is_certain(CivilTimeComponent.WEEKDAY)

    # 前の水曜日 (previous Wednesday)
    results = chrono.ja.parse("前の水曜日", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "前の水曜日"
    assert results[0].moment.datetime() == datetime.datetime(2016, 8, 31, 12, 0)
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2016
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 8
    assert results[0].moment.get(CivilTimeComponent.DAY) == 31
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 3


def test_merge_date_and_weekday():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # 8月27日水曜日 (Wednesday Aug 27)
    results = chrono.ja.parse("8月27日水曜日", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "8月27日水曜日"
    assert results[0].moment.datetime() == datetime.datetime(2012, 8, 27, 12, 0)
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2012
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 8
    assert results[0].moment.get(CivilTimeComponent.DAY) == 27
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 3
