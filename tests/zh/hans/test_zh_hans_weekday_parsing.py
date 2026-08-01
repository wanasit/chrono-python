import datetime
import chrono_python as chrono
from chrono_python.common.types import CivilTimeComponent


def test_zh_hans_weekday_single_expression():
    ref_date = datetime.datetime(2016, 9, 2)  # Friday Sep 2, 2016

    # 星期四
    res = chrono.zh.hans.parse("星期四", ref_date)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "星期四"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2016
    assert res[0].start.get(CivilTimeComponent.MONTH) == 9
    assert res[0].start.get(CivilTimeComponent.DAY) == 1
    assert res[0].start.get(CivilTimeComponent.WEEKDAY) == 4
    assert res[0].start.is_certain(CivilTimeComponent.WEEKDAY) is True
    assert res[0].start.is_certain(CivilTimeComponent.DAY) is False

    # 我周一要打游戏
    ref_date_2 = datetime.datetime(2012, 8, 10)  # Friday Aug 10, 2012
    res = chrono.zh.hans.parse("我周一要打游戏", ref_date_2)
    assert len(res) == 1
    assert res[0].index == 1
    assert res[0].text == "周一"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2012
    assert res[0].start.get(CivilTimeComponent.MONTH) == 8
    assert res[0].start.get(CivilTimeComponent.DAY) == 13
    assert res[0].start.get(CivilTimeComponent.WEEKDAY) == 1

    # 礼拜日
    res = chrono.zh.hans.parse("礼拜日", ref_date)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "礼拜日"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2016
    assert res[0].start.get(CivilTimeComponent.MONTH) == 9
    assert res[0].start.get(CivilTimeComponent.DAY) == 4
    assert res[0].start.get(CivilTimeComponent.WEEKDAY) == 0

    # 我上个礼拜三在打游戏
    res = chrono.zh.hans.parse("我上个礼拜三在打游戏", ref_date)
    assert len(res) == 1
    assert res[0].index == 1
    assert res[0].text == "上个礼拜三"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2016
    assert res[0].start.get(CivilTimeComponent.MONTH) == 8
    assert res[0].start.get(CivilTimeComponent.DAY) == 24
    assert res[0].start.get(CivilTimeComponent.WEEKDAY) == 3

    # 我下星期天打游戏
    res = chrono.zh.hans.parse("我下星期天打游戏", ref_date)
    assert len(res) == 1
    assert res[0].index == 1
    assert res[0].text == "下星期天"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2016
    assert res[0].start.get(CivilTimeComponent.MONTH) == 9
    assert res[0].start.get(CivilTimeComponent.DAY) == 4
    assert res[0].start.get(CivilTimeComponent.WEEKDAY) == 0


def test_zh_hans_weekday_this_week():
    ref_date = datetime.datetime(2012, 8, 10)

    # 我这个星期一要打游戏
    res = chrono.zh.hans.parse("我这个星期一要打游戏", ref_date)
    assert len(res) == 1
    assert res[0].index == 1
    assert res[0].text == "这个星期一"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2012
    assert res[0].start.get(CivilTimeComponent.MONTH) == 8
    assert res[0].start.get(CivilTimeComponent.DAY) == 6
    assert res[0].start.get(CivilTimeComponent.WEEKDAY) == 1

    # 星期一
    res = chrono.zh.hans.parse("星期一", ref_date)
    assert len(res) == 1
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2012
    assert res[0].start.get(CivilTimeComponent.MONTH) == 8
    assert res[0].start.get(CivilTimeComponent.DAY) == 13
    assert res[0].start.get(CivilTimeComponent.WEEKDAY) == 1
