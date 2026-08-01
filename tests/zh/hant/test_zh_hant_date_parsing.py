import datetime
import chrono_python as chrono
from chrono_python.common.types import CivilTimeComponent


def test_zh_hant_date_single_expression():
    ref_date = datetime.datetime(2012, 8, 10)

    # 我2016年9月3號要打遊戲
    res = chrono.zh.hant.parse("我2016年9月3號要打遊戲", ref_date)
    assert len(res) == 1
    assert res[0].index == 1
    assert res[0].text == "2016年9月3號"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2016
    assert res[0].start.get(CivilTimeComponent.MONTH) == 9
    assert res[0].start.get(CivilTimeComponent.DAY) == 3

    # 我二零一六年，九月三號要打遊戲
    res = chrono.zh.hant.parse("我二零一六年，九月三號要打遊戲", ref_date)
    assert len(res) == 1
    assert res[0].index == 1
    assert res[0].text == "二零一六年，九月三號"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2016
    assert res[0].start.get(CivilTimeComponent.MONTH) == 9
    assert res[0].start.get(CivilTimeComponent.DAY) == 3

    # 我九月三號要打遊戲
    ref_date_2014 = datetime.datetime(2014, 8, 10)
    res = chrono.zh.hant.parse("我九月三號要打遊戲", ref_date_2014)
    assert len(res) == 1
    assert res[0].index == 1
    assert res[0].text == "九月三號"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2014
    assert res[0].start.get(CivilTimeComponent.MONTH) == 9
    assert res[0].start.get(CivilTimeComponent.DAY) == 3

    # 2016年09月03號
    res = chrono.zh.hant.parse("2016年09月03號", ref_date)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "2016年09月03號"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2016
    assert res[0].start.get(CivilTimeComponent.MONTH) == 9
    assert res[0].start.get(CivilTimeComponent.DAY) == 3


def test_zh_hant_date_range_expression():
    ref_date = datetime.datetime(2012, 8, 10)

    # 2016年9月3號-2017年10月24號
    res = chrono.zh.hant.parse("2016年9月3號-2017年10月24號", ref_date)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "2016年9月3號-2017年10月24號"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2016
    assert res[0].start.get(CivilTimeComponent.MONTH) == 9
    assert res[0].start.get(CivilTimeComponent.DAY) == 3
    assert res[0].end.get(CivilTimeComponent.YEAR) == 2017
    assert res[0].end.get(CivilTimeComponent.MONTH) == 10
    assert res[0].end.get(CivilTimeComponent.DAY) == 24

    # 二零一六年九月三號ー2017年10月24號
    res = chrono.zh.hant.parse("二零一六年九月三號ー2017年10月24號", ref_date)
    assert len(res) == 1
    assert res[0].index == 0
    assert res[0].text == "二零一六年九月三號ー2017年10月24號"
    assert res[0].start.get(CivilTimeComponent.YEAR) == 2016
    assert res[0].start.get(CivilTimeComponent.MONTH) == 9
    assert res[0].start.get(CivilTimeComponent.DAY) == 3
    assert res[0].end.get(CivilTimeComponent.YEAR) == 2017
    assert res[0].end.get(CivilTimeComponent.MONTH) == 10
    assert res[0].end.get(CivilTimeComponent.DAY) == 24
