import datetime
import chrono_python as chrono


def test_zh_hant_ago_expression():
    ref_date = datetime.datetime(2012, 8, 10, 12, 14)

    # 1小時前
    res = chrono.zh.hant.parse("1小時前", ref_date)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "1小時前"
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 10, 11, 14)

    # 1小時之前出門了
    res = chrono.zh.hant.parse("1小時之前出門了", ref_date)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "1小時之前"
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 10, 11, 14)

    # 五分鐘前
    res = chrono.zh.hant.parse("五分鐘前", ref_date)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "五分鐘前"
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 10, 12, 9)

    # 3天前
    res = chrono.zh.hant.parse("3天前", ref_date)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "3天前"
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 7, 12, 0)

    # 2禮拜前
    res = chrono.zh.hant.parse("2禮拜前", ref_date)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "2禮拜前"
    assert res[0].start.datetime() == datetime.datetime(2012, 7, 27, 12, 0)

    # 半小時前
    res = chrono.zh.hant.parse("半小時前", ref_date)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "半小時前"
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 10, 11, 44)
