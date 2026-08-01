import datetime
import chrono_python as chrono
from chrono_python.common.types import CivilTimeComponent


def test_zh_hans_deadline_expression():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # 五日内我要通关游戏
    res = chrono.zh.hans.parse("五日内我要通关游戏", ref_date)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "五日内"
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 15, 12, 0)

    # 5日之内我要通关游戏
    res = chrono.zh.hans.parse("5日之内我要通关游戏", ref_date)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "5日之内"
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 15, 12, 0)

    # 十日内我要通关游戏
    res = chrono.zh.hans.parse("十日内我要通关游戏", ref_date)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "十日内"
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 20, 12, 0)

    ref_date_time = datetime.datetime(2012, 8, 10, 12, 14)

    # 五分钟后
    res = chrono.zh.hans.parse("五分钟后", ref_date_time)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "五分钟后"
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 10, 12, 19)

    # 一个钟之内
    res = chrono.zh.hans.parse("一个钟之内", ref_date_time)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "一个钟之内"
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 10, 13, 14)

    # 5分钟之后出门
    res = chrono.zh.hans.parse("5分钟之后出门", ref_date_time)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "5分钟之后"
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 10, 12, 19)

    # 我要5秒之后出门
    res = chrono.zh.hans.parse("我要5秒之后出门", ref_date_time)
    assert len(res) == 1
    assert res[0].index == 2
    assert res[0].text == "5秒之后"
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 10, 12, 14, 5)

    # 半小时之内
    res = chrono.zh.hans.parse("半小时之内", ref_date_time)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "半小时之内"
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 10, 12, 44)

    # 两个礼拜内答复我
    res = chrono.zh.hans.parse("两个礼拜内答复我", ref_date_time)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "两个礼拜内"
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 24, 12, 0)

    # 1个月之内答复我
    res = chrono.zh.hans.parse("1个月之内答复我", ref_date_time)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "1个月之内"
    assert res[0].start.datetime() == datetime.datetime(2012, 9, 10, 12, 0)

    # 几个月之内答复我
    res = chrono.zh.hans.parse("几个月之内答复我", ref_date_time)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "几个月之内"
    assert res[0].start.datetime() == datetime.datetime(2012, 11, 10, 12, 0)

    # 一年内答复我
    res = chrono.zh.hans.parse("一年内答复我", ref_date_time)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "一年内"
    assert res[0].start.datetime() == datetime.datetime(2013, 8, 10, 12, 0)

    # 1年之内答复我
    res = chrono.zh.hans.parse("1年之内答复我", ref_date_time)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "1年之内"
    assert res[0].start.datetime() == datetime.datetime(2013, 8, 10, 12, 0)


def test_zh_hans_deadline_untested_units():
    ref_date = datetime.datetime(2012, 8, 10, 12, 14)

    res = chrono.zh.hans.parse("5秒钟后", ref_date)
    assert res[0].text == "5秒钟后"
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 10, 12, 14, 5)

    res = chrono.zh.hans.parse("2小时后", ref_date)
    assert res[0].text == "2小时后"
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 10, 14, 14)

    res = chrono.zh.hans.parse("3天后", ref_date)
    assert res[0].text == "3天后"
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 13, 12, 0)

    res = chrono.zh.hans.parse("2星期后", ref_date)
    assert res[0].text == "2星期后"
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 24, 12, 0)

    res = chrono.zh.hans.parse("5分钟过后", ref_date)
    assert res[0].text == "5分钟过后"
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 10, 12, 19)
