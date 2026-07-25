import datetime
import chrono_python as chrono
from chrono_python.common.types import CivilTimeComponent, Meridiem
from chrono_python.types import DateTimePrecision


def test_ja_time_expr_parsing():
    ref_date = datetime.datetime(2020, 1, 1, 12, 0)

    # 10時
    results = chrono.ja.parse("10時", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "10時"
    assert result.moment.get(CivilTimeComponent.HOUR) == 10
    assert result.moment.get(CivilTimeComponent.MINUTE) == 0
    assert result.moment.is_certain(CivilTimeComponent.MINUTE) is False
    assert result.moment.get(CivilTimeComponent.MERIDIEM) == Meridiem.AM
    assert result.moment.precision() == DateTimePrecision.HOUR

    # 午前十時半
    results = chrono.ja.parse("午前十時半", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "午前十時半"
    assert result.moment.get(CivilTimeComponent.HOUR) == 10
    assert result.moment.get(CivilTimeComponent.MINUTE) == 30
    assert result.moment.get(CivilTimeComponent.MERIDIEM) == Meridiem.AM

    # 午後３時分秒表記無し
    results = chrono.ja.parse("午後３時", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "午後３時"
    assert result.moment.get(CivilTimeComponent.HOUR) == 15
    assert result.moment.get(CivilTimeComponent.MERIDIEM) == Meridiem.PM

    # 十五時三十分二十秒
    results = chrono.ja.parse("十五時三十分二十秒", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "十五時三十分二十秒"
    assert result.moment.get(CivilTimeComponent.HOUR) == 15
    assert result.moment.get(CivilTimeComponent.MINUTE) == 30
    assert result.moment.get(CivilTimeComponent.SECOND) == 20
    assert result.moment.get(CivilTimeComponent.MERIDIEM) == Meridiem.PM

    # 午後１3時 (invalid time expression with AM/PM prefix)
    results = chrono.ja.parse("午後１3時", ref_date)
    assert len(results) == 0


def test_ja_time_range_parsing():
    ref_date = datetime.datetime(2020, 1, 1, 12, 0)

    # 午前10時〜午後1時
    results = chrono.ja.parse("午前10時〜午後1時", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "午前10時〜午後1時"
    assert result.start.get(CivilTimeComponent.HOUR) == 10
    assert result.start.get(CivilTimeComponent.MERIDIEM) == Meridiem.AM
    assert result.end.get(CivilTimeComponent.HOUR) == 13
    assert result.end.get(CivilTimeComponent.MERIDIEM) == Meridiem.PM

    # 10時 - 11時 (imply AM/PM)
    results = chrono.ja.parse("10時 - 11時", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "10時 - 11時"
    assert result.start.get(CivilTimeComponent.HOUR) == 10
    assert result.end.get(CivilTimeComponent.HOUR) == 11

    # 午後10時 - 1時 (cross midnight range check)
    results = chrono.ja.parse("午後10時 - 1時", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "午後10時 - 1時"
    assert result.start.get(CivilTimeComponent.HOUR) == 22
    assert result.start.datetime().day == 1
    assert result.end.get(CivilTimeComponent.HOUR) == 1
    assert result.end.datetime().day == 2



