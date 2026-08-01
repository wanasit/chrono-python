import datetime
import chrono_python as chrono
from chrono_python.common.types import CivilTimeComponent


def test_zh_hant_deadline_expression():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # 五日內我要通關遊戲
    res = chrono.zh.hant.parse("五日內我要通關遊戲", ref_date)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "五日內"
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 15, 12, 0)

    # 5日之內我要通關遊戲
    res = chrono.zh.hant.parse("5日之內我要通關遊戲", ref_date)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "5日之內"
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 15, 12, 0)

    # 十日內我要通關遊戲
    res = chrono.zh.hant.parse("十日內我要通關遊戲", ref_date)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "十日內"
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 20, 12, 0)

    ref_date_time = datetime.datetime(2012, 8, 10, 12, 14)

    # 五分鐘後
    res = chrono.zh.hant.parse("五分鐘後", ref_date_time)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "五分鐘後"
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 10, 12, 19)

    # 一個鐘之內
    res = chrono.zh.hant.parse("一個鐘之內", ref_date_time)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "一個鐘之內"
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 10, 13, 14)

    # 5分鐘之後出門
    res = chrono.zh.hant.parse("5分鐘之後出門", ref_date_time)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "5分鐘之後"
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 10, 12, 19)

    # 我要5秒之後出門
    res = chrono.zh.hant.parse("我要5秒之後出門", ref_date_time)
    assert len(res) == 1
    assert res[0].index == 2
    assert res[0].text == "5秒之後"
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 10, 12, 14, 5)

    # 半小時之內
    res = chrono.zh.hant.parse("半小時之內", ref_date_time)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "半小時之內"
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 10, 12, 44)

    # 兩個禮拜內答覆我
    res = chrono.zh.hant.parse("兩個禮拜內答覆我", ref_date_time)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "兩個禮拜內"
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 24, 12, 0)

    # 1個月之內答覆我
    res = chrono.zh.hant.parse("1個月之內答覆我", ref_date_time)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "1個月之內"
    assert res[0].start.datetime() == datetime.datetime(2012, 9, 10, 12, 0)

    # 幾個月之內答覆我
    res = chrono.zh.hant.parse("幾個月之內答覆我", ref_date_time)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "幾個月之內"
    assert res[0].start.datetime() == datetime.datetime(2012, 11, 10, 12, 0)

    # 一年內答覆我
    res = chrono.zh.hant.parse("一年內答覆我", ref_date_time)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "一年內"
    assert res[0].start.datetime() == datetime.datetime(2013, 8, 10, 12, 0)

    # 1年之內答覆我
    res = chrono.zh.hant.parse("1年之內答覆我", ref_date_time)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "1年之內"
    assert res[0].start.datetime() == datetime.datetime(2013, 8, 10, 12, 0)
