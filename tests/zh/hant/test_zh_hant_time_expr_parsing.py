import datetime
import chrono_python as chrono
from chrono_python.common.types import CivilTimeComponent, Meridiem


def test_zh_hant_time_expr_single_expression():
    ref_date = datetime.datetime(2012, 8, 10, 0, 0)

    # 我上午6點13分打遊戲
    res = chrono.zh.hant.parse("我上午6點13分打遊戲", ref_date)
    assert len(res) == 1
    assert res[0].index == 1
    assert res[0].text == "上午6點13分"
    assert res[0].start.get(CivilTimeComponent.HOUR) == 6
    assert res[0].start.get(CivilTimeComponent.MINUTE) == 13

    # 我後天凌晨打遊戲
    res = chrono.zh.hant.parse("我後天凌晨打遊戲", ref_date)
    assert len(res) == 1
    assert res[0].index == 1
    assert res[0].text == "後天凌晨"
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 12, 0, 0)

    # 我大前天凌晨打遊戲
    res = chrono.zh.hant.parse("我大前天凌晨打遊戲", ref_date)
    assert len(res) == 1
    assert res[0].index == 1
    assert res[0].text == "大前天凌晨"
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 7, 0, 0)

    # 我明天上午8點要打遊戲
    ref_date_12 = datetime.datetime(2012, 8, 10, 12, 0)
    res = chrono.zh.hant.parse("我明天上午8點要打遊戲", ref_date_12)
    assert len(res) == 1
    assert res[0].index == 1
    assert res[0].text == "明天上午8點"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2012
    assert res[0].start.get(CivilTimeComponent.MONTH) == 8
    assert res[0].start.get(CivilTimeComponent.DAY) == 11
    assert res[0].start.get(CivilTimeComponent.HOUR) == 8

    # 早上8點
    res = chrono.zh.hant.parse("早上8點", ref_date_12)
    assert len(res) == 1
    assert res[0].text == "早上8點"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2012
    assert res[0].start.get(CivilTimeComponent.MONTH) == 8
    assert res[0].start.get(CivilTimeComponent.DAY) == 10
    assert res[0].start.get(CivilTimeComponent.HOUR) == 8


def test_zh_hant_time_expr_range_expression():
    ref_date = datetime.datetime(2012, 8, 10, 0, 0)

    # 我從今早八點十分至下午11點32分打遊戲
    res = chrono.zh.hant.parse("我從今早八點十分至下午11點32分打遊戲", ref_date)
    assert len(res) == 1
    assert res[0].index == 1
    assert res[0].text == "從今早八點十分至下午11點32分"
    assert res[0].start.get(CivilTimeComponent.HOUR) == 8
    assert res[0].start.get(CivilTimeComponent.MINUTE) == 10
    assert res[0].end.get(CivilTimeComponent.HOUR) == 23
    assert res[0].end.get(CivilTimeComponent.MINUTE) == 32

    # 6點30pm-11點pm
    res = chrono.zh.hant.parse("6點30pm-11點pm", ref_date)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "6點30pm-11點pm"
    assert res[0].start.get(CivilTimeComponent.HOUR) == 18
    assert res[0].start.get(CivilTimeComponent.MINUTE) == 30
    assert res[0].start.get(CivilTimeComponent.MERIDIEM) == Meridiem.PM.value
    assert res[0].end.get(CivilTimeComponent.HOUR) == 23
    assert res[0].end.get(CivilTimeComponent.MINUTE) == 0
    assert res[0].end.get(CivilTimeComponent.MERIDIEM) == Meridiem.PM.value


def test_zh_hant_time_expr_date_plus_time():
    ref_date = datetime.datetime(2012, 8, 10, 0, 0)
    res = chrono.zh.hant.parse("我二零一八年十一月二十六日下午三點半五十九秒打遊戲", ref_date)
    assert len(res) == 1
    assert res[0].index == 1
    assert res[0].text == "二零一八年十一月二十六日下午三點半五十九秒"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2018
    assert res[0].start.get(CivilTimeComponent.MONTH) == 11
    assert res[0].start.get(CivilTimeComponent.DAY) == 26
    assert res[0].start.get(CivilTimeComponent.HOUR) == 15
    assert res[0].start.get(CivilTimeComponent.MINUTE) == 30
    assert res[0].start.get(CivilTimeComponent.SECOND) == 59


def test_zh_hant_time_expr_meridiem_imply():
    ref_date = datetime.datetime(2012, 8, 10, 0, 0)
    res = chrono.zh.hant.parse("1點pm到3點", ref_date)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "1點pm到3點"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2012
    assert res[0].start.get(CivilTimeComponent.MONTH) == 8
    assert res[0].start.get(CivilTimeComponent.DAY) == 10
    assert res[0].start.get(CivilTimeComponent.HOUR) == 13
    assert res[0].start.get(CivilTimeComponent.MINUTE) == 0
    assert res[0].start.get(CivilTimeComponent.SECOND) == 0
    assert res[0].start.get(CivilTimeComponent.MERIDIEM) == Meridiem.PM.value
    assert res[0].start.is_certain(CivilTimeComponent.MERIDIEM) is True

    assert res[0].end.get(CivilTimeComponent.YEAR) == 2012
    assert res[0].end.get(CivilTimeComponent.MONTH) == 8
    assert res[0].end.get(CivilTimeComponent.DAY) == 11
    assert res[0].end.get(CivilTimeComponent.HOUR) == 3
    assert res[0].end.get(CivilTimeComponent.MINUTE) == 0
    assert res[0].end.get(CivilTimeComponent.SECOND) == 0
    assert res[0].end.is_certain(CivilTimeComponent.MERIDIEM) is False


def test_zh_hant_time_expr_range_with_days():
    ref_date = datetime.datetime(2012, 8, 10, 0, 0)

    # 今晚10點 - 明天早上6點
    res = chrono.zh.hant.parse("今晚10點 - 明天早上6點", ref_date)
    assert len(res) == 1
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2012
    assert res[0].start.get(CivilTimeComponent.MONTH) == 8
    assert res[0].start.get(CivilTimeComponent.DAY) == 10
    assert res[0].start.get(CivilTimeComponent.HOUR) == 22
    assert res[0].end.get(CivilTimeComponent.YEAR) == 2012
    assert res[0].end.get(CivilTimeComponent.MONTH) == 8
    assert res[0].end.get(CivilTimeComponent.DAY) == 11
    assert res[0].end.get(CivilTimeComponent.HOUR) == 6

    # 晚上11點 ~ 凌晨2點
    res = chrono.zh.hant.parse("晚上11點 ~ 凌晨2點", ref_date)
    assert len(res) == 1
    assert res[0].start.get(CivilTimeComponent.HOUR) == 23
    assert res[0].end.get(CivilTimeComponent.HOUR) == 2
    assert res[0].end.get(CivilTimeComponent.DAY) == 11
