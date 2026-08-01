import datetime
import chrono_python as chrono
from chrono_python.common.types import CivilTimeComponent, Meridiem


def test_zh_hans_casual_single_expression():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # 我今天要打游戏
    res = chrono.zh.hans.parse("我今天要打游戏", ref_date)
    assert len(res) == 1
    assert res[0].index == 1
    assert res[0].text == "今天"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2012
    assert res[0].start.get(CivilTimeComponent.MONTH) == 8
    assert res[0].start.get(CivilTimeComponent.DAY) == 10
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 10, 12, 0)

    # 我明日要打游戏
    res = chrono.zh.hans.parse("我明日要打游戏", ref_date)
    assert len(res) == 1
    assert res[0].index == 1
    assert res[0].text == "明日"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2012
    assert res[0].start.get(CivilTimeComponent.MONTH) == 8
    assert res[0].start.get(CivilTimeComponent.DAY) == 11
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 11, 12, 0)

    # 我明天要打游戏 (1 AM ref date)
    ref_date_1am = datetime.datetime(2012, 8, 10, 1, 0)
    res = chrono.zh.hans.parse("我明天要打游戏", ref_date_1am)
    assert len(res) == 1
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 10, 12, 0)

    # 我后天凌晨要打游戏
    ref_date_midnight = datetime.datetime(2012, 8, 10, 0, 0)
    res = chrono.zh.hans.parse("我后天凌晨要打游戏", ref_date_midnight)
    assert len(res) == 1
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 12, 0, 0)

    # 我大前天凌晨要打游戏
    res = chrono.zh.hans.parse("我大前天凌晨要打游戏", ref_date_midnight)
    assert len(res) == 1
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 7, 0, 0)

    # 我前天要打游戏
    res = chrono.zh.hans.parse("我前天要打游戏", ref_date)
    assert len(res) == 1
    assert res[0].index == 1
    assert res[0].text == "前天"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2012
    assert res[0].start.get(CivilTimeComponent.MONTH) == 8
    assert res[0].start.get(CivilTimeComponent.DAY) == 8

    # 我昨日要打游戏
    res = chrono.zh.hans.parse("我昨日要打游戏", ref_date)
    assert len(res) == 1
    assert res[0].index == 1
    assert res[0].text == "昨日"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2012
    assert res[0].start.get(CivilTimeComponent.MONTH) == 8
    assert res[0].start.get(CivilTimeComponent.DAY) == 9

    # 我昨天晚上要打游戏
    res = chrono.zh.hans.parse("我昨天晚上要打游戏", ref_date)
    assert len(res) == 1
    assert res[0].index == 1
    assert res[0].text == "昨天晚上"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2012
    assert res[0].start.get(CivilTimeComponent.MONTH) == 8
    assert res[0].start.get(CivilTimeComponent.DAY) == 9
    assert res[0].start.get(CivilTimeComponent.HOUR) == 22

    # 我今天早上要打游戏
    res = chrono.zh.hans.parse("我今天早上要打游戏", ref_date)
    assert len(res) == 1
    assert res[0].index == 1
    assert res[0].text == "今天早上"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2012
    assert res[0].start.get(CivilTimeComponent.MONTH) == 8
    assert res[0].start.get(CivilTimeComponent.DAY) == 10
    assert res[0].start.get(CivilTimeComponent.HOUR) == 6

    # 我下午要打游戏
    res = chrono.zh.hans.parse("我下午要打游戏", ref_date)
    assert len(res) == 1
    assert res[0].index == 1
    assert res[0].text == "下午"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2012
    assert res[0].start.get(CivilTimeComponent.MONTH) == 8
    assert res[0].start.get(CivilTimeComponent.DAY) == 10
    assert res[0].start.get(CivilTimeComponent.HOUR) == 15

    # 我今晚要打游戏
    res = chrono.zh.hans.parse("我今晚要打游戏", ref_date)
    assert len(res) == 1
    assert res[0].index == 1
    assert res[0].text == "今晚"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2012
    assert res[0].start.get(CivilTimeComponent.MONTH) == 8
    assert res[0].start.get(CivilTimeComponent.DAY) == 10
    assert res[0].start.get(CivilTimeComponent.HOUR) == 22


def test_zh_hans_casual_combined_expression():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    res = chrono.zh.hans.parse("我今天下午5点要打游戏", ref_date)
    assert len(res) == 1
    assert res[0].index == 1
    assert res[0].text == "今天下午5点"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2012
    assert res[0].start.get(CivilTimeComponent.MONTH) == 8
    assert res[0].start.get(CivilTimeComponent.DAY) == 10
    assert res[0].start.get(CivilTimeComponent.HOUR) == 17


def test_zh_hans_casual_date_range():
    ref_date_1 = datetime.datetime(2012, 8, 4, 12, 0)
    res1 = chrono.zh.hans.parse("我今天 - 下周五要打游戏", ref_date_1)
    assert len(res1) == 1
    assert res1[0].index == 1
    assert res1[0].text == "今天 - 下周五"
    assert res1[0].start.get(CivilTimeComponent.YEAR) == 2012
    assert res1[0].start.get(CivilTimeComponent.MONTH) == 8
    assert res1[0].start.get(CivilTimeComponent.DAY) == 4
    assert res1[0].end.get(CivilTimeComponent.YEAR) == 2012
    assert res1[0].end.get(CivilTimeComponent.MONTH) == 8
    assert res1[0].end.get(CivilTimeComponent.DAY) == 10

    ref_date_2 = datetime.datetime(2012, 8, 10, 12, 0)
    res2 = chrono.zh.hans.parse("我今日 - 下周五要打游戏", ref_date_2)
    assert len(res2) == 1
    assert res2[0].index == 1
    assert res2[0].text == "今日 - 下周五"
    assert res2[0].start.get(CivilTimeComponent.YEAR) == 2012
    assert res2[0].start.get(CivilTimeComponent.MONTH) == 8
    assert res2[0].start.get(CivilTimeComponent.DAY) == 10
    assert res2[0].end.get(CivilTimeComponent.YEAR) == 2012
    assert res2[0].end.get(CivilTimeComponent.MONTH) == 8
    assert res2[0].end.get(CivilTimeComponent.DAY) == 17


def test_zh_hans_casual_random_text():
    ref_date = datetime.datetime(2012, 1, 1, 12, 0)

    res = chrono.zh.hans.parse("今日夜晚", ref_date)
    assert len(res) == 1
    assert res[0].text == "今日夜晚"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2012
    assert res[0].start.get(CivilTimeComponent.MONTH) == 1
    assert res[0].start.get(CivilTimeComponent.DAY) == 1
    assert res[0].start.get(CivilTimeComponent.HOUR) == 22
    assert res[0].start.get(CivilTimeComponent.MERIDIEM) == Meridiem.PM.value

    res = chrono.zh.hans.parse("今晚8点正", ref_date)
    assert len(res) == 1
    assert res[0].text == "今晚8点正"
    assert res[0].start.get(CivilTimeComponent.HOUR) == 20
    assert res[0].start.get(CivilTimeComponent.MERIDIEM) == Meridiem.PM.value

    res = chrono.zh.hans.parse("晚上8点", ref_date)
    assert len(res) == 1
    assert res[0].text == "晚上8点"
    assert res[0].start.get(CivilTimeComponent.HOUR) == 20

    res = chrono.zh.hans.parse("星期四", ref_date)
    assert len(res) == 1
    assert res[0].text == "星期四"
    assert res[0].start.get(CivilTimeComponent.WEEKDAY) == 4
