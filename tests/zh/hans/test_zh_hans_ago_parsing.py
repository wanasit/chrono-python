import datetime
import chrono_python as chrono


def test_zh_hans_ago_expression():
    ref_date = datetime.datetime(2012, 8, 10, 12, 14)

    # 1小时前
    res = chrono.zh.hans.parse("1小时前", ref_date)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "1小时前"
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 10, 11, 14)

    # 1小时之前出门了
    res = chrono.zh.hans.parse("1小时之前出门了", ref_date)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "1小时之前"
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 10, 11, 14)

    # 五分钟前
    res = chrono.zh.hans.parse("五分钟前", ref_date)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "五分钟前"
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 10, 12, 9)

    # 3天前
    res = chrono.zh.hans.parse("3天前", ref_date)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "3天前"
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 7, 12, 0)

    # 2星期前
    res = chrono.zh.hans.parse("2星期前", ref_date)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "2星期前"
    assert res[0].start.datetime() == datetime.datetime(2012, 7, 27, 12, 0)

    # 半小时前
    res = chrono.zh.hans.parse("半小时前", ref_date)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "半小时前"
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 10, 11, 44)
