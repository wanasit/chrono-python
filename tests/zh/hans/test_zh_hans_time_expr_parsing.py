import datetime
import chrono_python as chrono
from chrono_python.common.types import CivilTimeComponent, Meridiem


def test_zh_hans_time_expr_single_expression():
    ref_date = datetime.datetime(2012, 8, 10, 0, 0)

    # 我上午6点13分打游戏
    res = chrono.zh.hans.parse("我上午6点13分打游戏", ref_date)
    assert len(res) == 1
    assert res[0].index == 1
    assert res[0].text == "上午6点13分"
    assert res[0].start.get(CivilTimeComponent.HOUR) == 6
    assert res[0].start.get(CivilTimeComponent.MINUTE) == 13

    # 我后天凌晨打游戏
    res = chrono.zh.hans.parse("我后天凌晨打游戏", ref_date)
    assert len(res) == 1
    assert res[0].index == 1
    assert res[0].text == "后天凌晨"
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 12, 0, 0)

    # 我大前天凌晨打游戏
    res = chrono.zh.hans.parse("我大前天凌晨打游戏", ref_date)
    assert len(res) == 1
    assert res[0].index == 1
    assert res[0].text == "大前天凌晨"
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 7, 0, 0)

    # 我明天上午8点要打游戏
    ref_date_12 = datetime.datetime(2012, 8, 10, 12, 0)
    res = chrono.zh.hans.parse("我明天上午8点要打游戏", ref_date_12)
    assert len(res) == 1
    assert res[0].index == 1
    assert res[0].text == "明天上午8点"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2012
    assert res[0].start.get(CivilTimeComponent.MONTH) == 8
    assert res[0].start.get(CivilTimeComponent.DAY) == 11
    assert res[0].start.get(CivilTimeComponent.HOUR) == 8

    # 早上8点
    res = chrono.zh.hans.parse("早上8点", ref_date_12)
    assert len(res) == 1
    assert res[0].text == "早上8点"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2012
    assert res[0].start.get(CivilTimeComponent.MONTH) == 8
    assert res[0].start.get(CivilTimeComponent.DAY) == 10
    assert res[0].start.get(CivilTimeComponent.HOUR) == 8


def test_zh_hans_time_expr_range_expression():
    ref_date = datetime.datetime(2012, 8, 10, 0, 0)

    # 我从今早八点十分至下午11点32分打游戏
    res = chrono.zh.hans.parse("我从今早八点十分至下午11点32分打游戏", ref_date)
    assert len(res) == 1
    assert res[0].index == 1
    assert res[0].text == "从今早八点十分至下午11点32分"
    assert res[0].start.get(CivilTimeComponent.HOUR) == 8
    assert res[0].start.get(CivilTimeComponent.MINUTE) == 10
    assert res[0].end.get(CivilTimeComponent.HOUR) == 23
    assert res[0].end.get(CivilTimeComponent.MINUTE) == 32

    # 6点30pm-11点pm
    res = chrono.zh.hans.parse("6点30pm-11点pm", ref_date)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "6点30pm-11点pm"
    assert res[0].start.get(CivilTimeComponent.HOUR) == 18
    assert res[0].start.get(CivilTimeComponent.MINUTE) == 30
    assert res[0].start.get(CivilTimeComponent.MERIDIEM) == Meridiem.PM.value
    assert res[0].end.get(CivilTimeComponent.HOUR) == 23
    assert res[0].end.get(CivilTimeComponent.MINUTE) == 0
    assert res[0].end.get(CivilTimeComponent.MERIDIEM) == Meridiem.PM.value


def test_zh_hans_time_expr_date_plus_time():
    ref_date = datetime.datetime(2012, 8, 10, 0, 0)
    res = chrono.zh.hans.parse("我二零一八年十一月二十六日下午三点半五十九秒打游戏", ref_date)
    assert len(res) == 1
    assert res[0].index == 1
    assert res[0].text == "二零一八年十一月二十六日下午三点半五十九秒"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2018
    assert res[0].start.get(CivilTimeComponent.MONTH) == 11
    assert res[0].start.get(CivilTimeComponent.DAY) == 26
    assert res[0].start.get(CivilTimeComponent.HOUR) == 15
    assert res[0].start.get(CivilTimeComponent.MINUTE) == 30
    assert res[0].start.get(CivilTimeComponent.SECOND) == 59


def test_zh_hans_time_expr_meridiem_imply():
    ref_date = datetime.datetime(2012, 8, 10, 0, 0)
    res = chrono.zh.hans.parse("1点pm到3点", ref_date)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "1点pm到3点"
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


def test_zh_hans_time_expr_iso_format():
    ref_date = datetime.datetime(2012, 8, 10, 0, 0)
    res = chrono.zh.hans.parse("2023-10-26 10:30:00", ref_date)
    assert len(res) == 1
    assert res[0].text == "2023-10-26 10:30:00"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2023
    assert res[0].start.get(CivilTimeComponent.MONTH) == 10
    assert res[0].start.get(CivilTimeComponent.DAY) == 26
    assert res[0].start.get(CivilTimeComponent.HOUR) == 10
    assert res[0].start.get(CivilTimeComponent.MINUTE) == 30
    assert res[0].start.get(CivilTimeComponent.SECOND) == 0


def test_zh_hans_time_expr_range_with_days():
    ref_date = datetime.datetime(2012, 8, 10, 0, 0)

    # 今晚10点 - 明天早上6点
    res = chrono.zh.hans.parse("今晚10点 - 明天早上6点", ref_date)
    assert len(res) == 1
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2012
    assert res[0].start.get(CivilTimeComponent.MONTH) == 8
    assert res[0].start.get(CivilTimeComponent.DAY) == 10
    assert res[0].start.get(CivilTimeComponent.HOUR) == 22
    assert res[0].end.get(CivilTimeComponent.YEAR) == 2012
    assert res[0].end.get(CivilTimeComponent.MONTH) == 8
    assert res[0].end.get(CivilTimeComponent.DAY) == 11
    assert res[0].end.get(CivilTimeComponent.HOUR) == 6

    # 晚上11点 ~ 凌晨2点
    res = chrono.zh.hans.parse("晚上11点 ~ 凌晨2点", ref_date)
    assert len(res) == 1
    assert res[0].start.get(CivilTimeComponent.HOUR) == 23
    assert res[0].end.get(CivilTimeComponent.HOUR) == 2
    assert res[0].end.get(CivilTimeComponent.DAY) == 11
