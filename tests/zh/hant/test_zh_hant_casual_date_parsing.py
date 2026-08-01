import datetime
import chrono_python as chrono
from chrono_python.common.types import CivilTimeComponent, Meridiem


def test_zh_hant_casual_single_expression():
    ref_date_micro = datetime.datetime(2012, 8, 10, 8, 9, 10, 11000)

    # 雞而家全部都係雞
    res = chrono.zh.hant.parse("雞而家全部都係雞", ref_date_micro)
    assert len(res) == 1
    assert res[0].index == 1
    assert res[0].text == "而家"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2012
    assert res[0].start.get(CivilTimeComponent.MONTH) == 8
    assert res[0].start.get(CivilTimeComponent.DAY) == 10
    assert res[0].start.get(CivilTimeComponent.HOUR) == 8
    assert res[0].start.get(CivilTimeComponent.MINUTE) == 9
    assert res[0].start.get(CivilTimeComponent.SECOND) == 10
    assert res[0].start.get(CivilTimeComponent.MILLI_SECOND) == 11

    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # 雞今日全部都係雞
    res = chrono.zh.hant.parse("雞今日全部都係雞", ref_date)
    assert len(res) == 1
    assert res[0].index == 1
    assert res[0].text == "今日"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2012
    assert res[0].start.get(CivilTimeComponent.MONTH) == 8
    assert res[0].start.get(CivilTimeComponent.DAY) == 10

    # 雞聽日全部都係雞
    res = chrono.zh.hant.parse("雞聽日全部都係雞", ref_date)
    assert len(res) == 1
    assert res[0].index == 1
    assert res[0].text == "聽日"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2012
    assert res[0].start.get(CivilTimeComponent.MONTH) == 8
    assert res[0].start.get(CivilTimeComponent.DAY) == 11

    # 雞明天全部都係雞 (1 AM ref date)
    ref_date_1am = datetime.datetime(2012, 8, 10, 1, 0)
    res = chrono.zh.hant.parse("雞明天全部都係雞", ref_date_1am)
    assert len(res) == 1
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 10, 12, 0)

    # 雞後天凌晨全部都係雞
    ref_date_midnight = datetime.datetime(2012, 8, 10, 0, 0)
    res = chrono.zh.hant.parse("雞後天凌晨全部都係雞", ref_date_midnight)
    assert len(res) == 1
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 12, 0, 0)

    # 雞大前天凌晨全部都係雞
    res = chrono.zh.hant.parse("雞大前天凌晨全部都係雞", ref_date_midnight)
    assert len(res) == 1
    assert res[0].start.datetime() == datetime.datetime(2012, 8, 7, 0, 0)

    # 雞前日全部都係雞
    res = chrono.zh.hant.parse("雞前日全部都係雞", ref_date)
    assert len(res) == 1
    assert res[0].index == 1
    assert res[0].text == "前日"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2012
    assert res[0].start.get(CivilTimeComponent.MONTH) == 8
    assert res[0].start.get(CivilTimeComponent.DAY) == 8

    # 雞琴日全部都係雞
    res = chrono.zh.hant.parse("雞琴日全部都係雞", ref_date)
    assert len(res) == 1
    assert res[0].index == 1
    assert res[0].text == "琴日"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2012
    assert res[0].start.get(CivilTimeComponent.MONTH) == 8
    assert res[0].start.get(CivilTimeComponent.DAY) == 9

    # 雞昨天晚上全部都係雞
    res = chrono.zh.hant.parse("雞昨天晚上全部都係雞", ref_date)
    assert len(res) == 1
    assert res[0].index == 1
    assert res[0].text == "昨天晚上"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2012
    assert res[0].start.get(CivilTimeComponent.MONTH) == 8
    assert res[0].start.get(CivilTimeComponent.DAY) == 9
    assert res[0].start.get(CivilTimeComponent.HOUR) == 22

    # 雞今日朝早全部都係雞
    res = chrono.zh.hant.parse("雞今日朝早全部都係雞", ref_date)
    assert len(res) == 1
    assert res[0].index == 1
    assert res[0].text == "今日朝早"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2012
    assert res[0].start.get(CivilTimeComponent.MONTH) == 8
    assert res[0].start.get(CivilTimeComponent.DAY) == 10
    assert res[0].start.get(CivilTimeComponent.HOUR) == 6

    # 雞晏晝全部都係雞
    res = chrono.zh.hant.parse("雞晏晝全部都係雞", ref_date)
    assert len(res) == 1
    assert res[0].index == 1
    assert res[0].text == "晏晝"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2012
    assert res[0].start.get(CivilTimeComponent.MONTH) == 8
    assert res[0].start.get(CivilTimeComponent.DAY) == 10
    assert res[0].start.get(CivilTimeComponent.HOUR) == 15

    # 雞今晚全部都係雞
    res = chrono.zh.hant.parse("雞今晚全部都係雞", ref_date)
    assert len(res) == 1
    assert res[0].index == 1
    assert res[0].text == "今晚"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2012
    assert res[0].start.get(CivilTimeComponent.MONTH) == 8
    assert res[0].start.get(CivilTimeComponent.DAY) == 10
    assert res[0].start.get(CivilTimeComponent.HOUR) == 22


def test_zh_hant_casual_combined_expression():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    res = chrono.zh.hant.parse("雞今日晏晝5點全部都係雞", ref_date)
    assert len(res) == 1
    assert res[0].index == 1
    assert res[0].text == "今日晏晝5點"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2012
    assert res[0].start.get(CivilTimeComponent.MONTH) == 8
    assert res[0].start.get(CivilTimeComponent.DAY) == 10
    assert res[0].start.get(CivilTimeComponent.HOUR) == 17


def test_zh_hant_casual_date_range():
    ref_date_1 = datetime.datetime(2012, 8, 4, 12, 0)
    res1 = chrono.zh.hant.parse("雞今日 - 下禮拜五全部都係雞", ref_date_1)
    assert len(res1) == 1
    assert res1[0].index == 1
    assert res1[0].text == "今日 - 下禮拜五"
    assert res1[0].start.get(CivilTimeComponent.YEAR) == 2012
    assert res1[0].start.get(CivilTimeComponent.MONTH) == 8
    assert res1[0].start.get(CivilTimeComponent.DAY) == 4
    assert res1[0].end.get(CivilTimeComponent.YEAR) == 2012
    assert res1[0].end.get(CivilTimeComponent.MONTH) == 8
    assert res1[0].end.get(CivilTimeComponent.DAY) == 10

    ref_date_2 = datetime.datetime(2012, 8, 10, 12, 0)
    res2 = chrono.zh.hant.parse("雞今日 - 下禮拜五全部都係雞", ref_date_2)
    assert len(res2) == 1
    assert res2[0].index == 1
    assert res2[0].text == "今日 - 下禮拜五"
    assert res2[0].start.get(CivilTimeComponent.YEAR) == 2012
    assert res2[0].start.get(CivilTimeComponent.MONTH) == 8
    assert res2[0].start.get(CivilTimeComponent.DAY) == 10
    assert res2[0].end.get(CivilTimeComponent.YEAR) == 2012
    assert res2[0].end.get(CivilTimeComponent.MONTH) == 8
    assert res2[0].end.get(CivilTimeComponent.DAY) == 17


def test_zh_hant_casual_random_text():
    ref_date = datetime.datetime(2012, 1, 1, 12, 0)

    res = chrono.zh.hant.parse("今日夜晚", ref_date)
    assert len(res) == 1
    assert res[0].text == "今日夜晚"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2012
    assert res[0].start.get(CivilTimeComponent.MONTH) == 1
    assert res[0].start.get(CivilTimeComponent.DAY) == 1
    assert res[0].start.get(CivilTimeComponent.HOUR) == 22
    assert res[0].start.get(CivilTimeComponent.MERIDIEM) == Meridiem.PM.value

    res = chrono.zh.hant.parse("今晚8點正", ref_date)
    assert len(res) == 1
    assert res[0].text == "今晚8點正"
    assert res[0].start.get(CivilTimeComponent.HOUR) == 20
    assert res[0].start.get(CivilTimeComponent.MERIDIEM) == Meridiem.PM.value

    res = chrono.zh.hant.parse("晚上8點", ref_date)
    assert len(res) == 1
    assert res[0].text == "晚上8點"
    assert res[0].start.get(CivilTimeComponent.HOUR) == 20

    res = chrono.zh.hant.parse("星期四", ref_date)
    assert len(res) == 1
    assert res[0].text == "星期四"
    assert res[0].start.get(CivilTimeComponent.WEEKDAY) == 4
