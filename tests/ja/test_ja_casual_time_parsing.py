import datetime
import chrono_python as chrono
from chrono_python.types import DateTimePrecision
from chrono_python.common.types import CivilTimeComponent, Meridiem

def test_ja_casual_time_parsing():
    ref_date = datetime.datetime(2016, 10, 1, 8, 0) # Saturday Oct 1, 2016

    # 朝
    results = chrono.ja.parse("朝", ref_date)
    assert len(results) == 1
    assert results[0].text == "朝"
    assert results[0].moment.datetime().hour == 6
    assert results[0].moment.datetime().minute == 0
    assert results[0].moment.get(CivilTimeComponent.MERIDIEM) == Meridiem.AM
    assert not results[0].moment.is_certain(CivilTimeComponent.HOUR)
    assert results[0].moment.precision() == DateTimePrecision.DAY

    # 午前中
    results = chrono.ja.parse("午前中", ref_date)
    assert len(results) == 1
    assert results[0].text == "午前中"
    assert results[0].moment.datetime().hour == 6
    assert results[0].moment.datetime().minute == 0
    assert results[0].moment.get(CivilTimeComponent.MERIDIEM) == Meridiem.AM
    assert not results[0].moment.is_certain(CivilTimeComponent.HOUR)
    assert results[0].moment.precision() == DateTimePrecision.DAY

    # 昼
    results = chrono.ja.parse("昼", ref_date)
    assert len(results) == 1
    assert results[0].text == "昼"
    assert results[0].moment.datetime().hour == 12
    assert results[0].moment.get(CivilTimeComponent.MERIDIEM) == Meridiem.AM
    assert results[0].moment.is_certain(CivilTimeComponent.HOUR)
    assert results[0].moment.precision() == DateTimePrecision.HOUR

    # お昼
    results = chrono.ja.parse("お昼", ref_date)
    assert len(results) == 1
    assert results[0].text == "お昼"
    assert results[0].moment.datetime().hour == 12
    assert results[0].moment.get(CivilTimeComponent.MERIDIEM) == Meridiem.AM
    assert results[0].moment.is_certain(CivilTimeComponent.HOUR)
    assert results[0].moment.precision() == DateTimePrecision.HOUR

    # 正午
    results = chrono.ja.parse("正午", ref_date)
    assert len(results) == 1
    assert results[0].text == "正午"
    assert results[0].moment.datetime().hour == 12
    assert results[0].moment.get(CivilTimeComponent.MERIDIEM) == Meridiem.AM
    assert results[0].moment.is_certain(CivilTimeComponent.HOUR)
    assert results[0].moment.precision() == DateTimePrecision.HOUR

    # 夕方
    results = chrono.ja.parse("夕方", ref_date)
    assert len(results) == 1
    assert results[0].text == "夕方"
    assert results[0].moment.datetime().hour == 18
    assert results[0].moment.get(CivilTimeComponent.MERIDIEM) == Meridiem.PM
    assert not results[0].moment.is_certain(CivilTimeComponent.HOUR)
    assert results[0].moment.precision() == DateTimePrecision.DAY

    # 夜
    results = chrono.ja.parse("夜", ref_date)
    assert len(results) == 1
    assert results[0].text == "夜"
    assert results[0].moment.datetime().hour == 20
    assert results[0].moment.get(CivilTimeComponent.MERIDIEM) == Meridiem.PM
    assert not results[0].moment.is_certain(CivilTimeComponent.HOUR)
    assert results[0].moment.precision() == DateTimePrecision.DAY


def test_ja_casual_time_midnight():
    # If reference hour is > 2 (e.g. 8:00 AM)
    ref_date_day = datetime.datetime(2016, 10, 1, 8, 0)

    # 深夜
    results = chrono.ja.parse("深夜", ref_date_day)
    assert len(results) == 1
    assert results[0].text == "深夜"
    # Should point to tomorrow's midnight (Oct 2, 00:00:00)
    assert results[0].moment.datetime() == datetime.datetime(2016, 10, 2, 0, 0)
    assert results[0].moment.is_certain(CivilTimeComponent.HOUR)
    assert results[0].moment.get(CivilTimeComponent.HOUR) == 0
    assert results[0].moment.precision() == DateTimePrecision.HOUR

    # 真夜中
    results = chrono.ja.parse("真夜中", ref_date_day)
    assert len(results) == 1
    assert results[0].text == "真夜中"
    assert results[0].moment.datetime() == datetime.datetime(2016, 10, 2, 0, 0)
    assert results[0].moment.is_certain(CivilTimeComponent.HOUR)
    assert results[0].moment.get(CivilTimeComponent.HOUR) == 0
    assert results[0].moment.precision() == DateTimePrecision.HOUR

    # If reference hour is <= 2 (e.g. 1:00 AM)
    ref_date_early = datetime.datetime(2016, 10, 1, 1, 0)

    # 深夜
    results = chrono.ja.parse("深夜", ref_date_early)
    assert len(results) == 1
    assert results[0].text == "深夜"
    # Should point to today's midnight (Oct 1, 00:00:00)
    assert results[0].moment.datetime() == datetime.datetime(2016, 10, 1, 0, 0)
    assert results[0].moment.precision() == DateTimePrecision.HOUR

    # 真夜中
    results = chrono.ja.parse("真夜中", ref_date_early)
    assert len(results) == 1
    assert results[0].text == "真夜中"
    assert results[0].moment.datetime() == datetime.datetime(2016, 10, 1, 0, 0)
    assert results[0].moment.precision() == DateTimePrecision.HOUR


def test_ja_strict_vs_casual_time():
    ref_date = datetime.datetime(2016, 10, 1, 8, 0)

    # Casual configuration should parse "朝"
    assert len(chrono.ja.casual.parse('朝', ref_date)) == 1

    # Strict configuration should NOT parse "朝"
    assert len(chrono.ja.strict.parse('朝', ref_date)) == 0
