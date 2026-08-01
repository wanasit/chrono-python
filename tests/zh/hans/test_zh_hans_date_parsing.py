import datetime
import chrono_python as chrono
from chrono_python.common.types import CivilTimeComponent


def test_zh_hans_date_single_expression():
    ref_date = datetime.datetime(2012, 8, 10)

    # 我2016年9月3号要打游戏
    res = chrono.zh.hans.parse("我2016年9月3号要打游戏", ref_date)
    assert len(res) == 1
    assert res[0].index == 1
    assert res[0].text == "2016年9月3号"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2016
    assert res[0].start.get(CivilTimeComponent.MONTH) == 9
    assert res[0].start.get(CivilTimeComponent.DAY) == 3

    # 我二零一刷新，九月三号要打游戏
    res = chrono.zh.hans.parse("我二零一六年，九月三号要打游戏", ref_date)
    assert len(res) == 1
    assert res[0].index == 1
    assert res[0].text == "二零一六年，九月三号"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2016
    assert res[0].start.get(CivilTimeComponent.MONTH) == 9
    assert res[0].start.get(CivilTimeComponent.DAY) == 3

    # 我九月三号要打游戏
    ref_date_2014 = datetime.datetime(2014, 8, 10)
    res = chrono.zh.hans.parse("我九月三号要打游戏", ref_date_2014)
    assert len(res) == 1
    assert res[0].index == 1
    assert res[0].text == "九月三号"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2014
    assert res[0].start.get(CivilTimeComponent.MONTH) == 9
    assert res[0].start.get(CivilTimeComponent.DAY) == 3

    # 2016年09月03号
    res = chrono.zh.hans.parse("2016年09月03号", ref_date)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "2016年09月03号"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2016
    assert res[0].start.get(CivilTimeComponent.MONTH) == 9
    assert res[0].start.get(CivilTimeComponent.DAY) == 3


def test_zh_hans_date_range_expression():
    ref_date = datetime.datetime(2012, 8, 10)

    # 2016年9月3号-2017年10月24号
    res = chrono.zh.hans.parse("2016年9月3号-2017年10月24号", ref_date)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "2016年9月3号-2017年10月24号"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2016
    assert res[0].start.get(CivilTimeComponent.MONTH) == 9
    assert res[0].start.get(CivilTimeComponent.DAY) == 3
    assert res[0].end.get(CivilTimeComponent.YEAR) == 2017
    assert res[0].end.get(CivilTimeComponent.MONTH) == 10
    assert res[0].end.get(CivilTimeComponent.DAY) == 24

    # 二零一六年九月三号ー2017年10月24号
    res = chrono.zh.hans.parse("二零一六年九月三号ー2017年10月24号", ref_date)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "二零一六年九月三号ー2017年10月24号"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2016
    assert res[0].start.get(CivilTimeComponent.MONTH) == 9
    assert res[0].start.get(CivilTimeComponent.DAY) == 3
    assert res[0].end.get(CivilTimeComponent.YEAR) == 2017
    assert res[0].end.get(CivilTimeComponent.MONTH) == 10
    assert res[0].end.get(CivilTimeComponent.DAY) == 24
