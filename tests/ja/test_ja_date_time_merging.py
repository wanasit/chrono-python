import datetime
import chrono_python as chrono
from chrono_python.common.types import CivilTimeComponent, Meridiem


def test_ja_merge_date_time():
    ref_date = datetime.datetime(2012, 3, 20, 12, 0)

    # 2012年3月31日の午後3時
    results = chrono.ja.parse("2012年3月31日の午後3時", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "2012年3月31日の午後3時"
    assert result.moment.get(CivilTimeComponent.YEAR) == 2012
    assert result.moment.get(CivilTimeComponent.MONTH) == 3
    assert result.moment.get(CivilTimeComponent.DAY) == 31
    assert result.moment.get(CivilTimeComponent.HOUR) == 15
    assert result.moment.datetime().minute == 0
    assert result.moment.get(CivilTimeComponent.MERIDIEM) == Meridiem.PM

    # 7月27日 10時
    results = chrono.ja.parse("7月27日 10時", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "7月27日 10時"
    assert result.moment.get(CivilTimeComponent.YEAR) == 2012
    assert result.moment.get(CivilTimeComponent.MONTH) == 7
    assert result.moment.get(CivilTimeComponent.DAY) == 27
    assert result.moment.get(CivilTimeComponent.HOUR) == 10
    assert result.moment.get(CivilTimeComponent.MERIDIEM) == Meridiem.AM


def test_ja_merge_casual_date_time():
    from chrono_python.types import DateTimePrecision

    ref_date = datetime.datetime(2012, 8, 9, 12, 0) # Thursday Aug 9, 2012

    # 今日の午後3時
    results = chrono.ja.parse("今日の午後3時", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "今日の午後3時"
    assert result.moment.get(CivilTimeComponent.YEAR) == 2012
    assert result.moment.get(CivilTimeComponent.MONTH) == 8
    assert result.moment.get(CivilTimeComponent.DAY) == 9
    assert result.moment.get(CivilTimeComponent.HOUR) == 15
    assert result.moment.get(CivilTimeComponent.MERIDIEM) == Meridiem.PM
    # since PM 3 o'clock is specified, hour and meridiem are known, and minute is assigned to 0, so precision is MINUTE
    assert result.moment.precision() == DateTimePrecision.MINUTE

    # 明日の10:30
    results = chrono.ja.parse("明日の10:30", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "明日の10:30"
    assert result.moment.get(CivilTimeComponent.YEAR) == 2012
    assert result.moment.get(CivilTimeComponent.MONTH) == 8
    assert result.moment.get(CivilTimeComponent.DAY) == 10
    assert result.moment.get(CivilTimeComponent.HOUR) == 10
    assert result.moment.get(CivilTimeComponent.MINUTE) == 30
    # since 10:30 is specified, precision is MINUTE
    assert result.moment.precision() == DateTimePrecision.MINUTE


def test_ja_merge_casual_date_and_casual_time():
    ref_date = datetime.datetime(2016, 10, 1, 8, 0)

    # 今日の夕方
    results = chrono.ja.parse("今日の夕方", ref_date)
    assert len(results) == 1
    assert results[0].text == "今日の夕方"
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2016
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 10
    assert results[0].moment.get(CivilTimeComponent.DAY) == 1
    assert results[0].moment.get(CivilTimeComponent.HOUR) == 18
    assert results[0].datetime() == datetime.datetime(2016, 10, 1, 18, 0)

    # 昨日の夜
    results = chrono.ja.parse("昨日の夜", ref_date)
    assert len(results) == 1
    assert results[0].text == "昨日の夜"
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2016
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 9
    assert results[0].moment.get(CivilTimeComponent.DAY) == 30
    assert results[0].moment.get(CivilTimeComponent.HOUR) == 20
    assert results[0].datetime() == datetime.datetime(2016, 9, 30, 20, 0)

    # 明日の朝
    results = chrono.ja.parse("明日の朝", ref_date)
    assert len(results) == 1
    assert results[0].text == "明日の朝"
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2016
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 10
    assert results[0].moment.get(CivilTimeComponent.DAY) == 2
    assert results[0].moment.get(CivilTimeComponent.HOUR) == 6
    assert results[0].datetime() == datetime.datetime(2016, 10, 2, 6, 0)
