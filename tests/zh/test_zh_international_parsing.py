import datetime
import chrono_python as chrono
from chrono_python.common.types import CivilTimeComponent


def test_zh_international_compatible():
    ref_date = datetime.datetime(2012, 8, 8, 0, 0)
    results = chrono.zh.parse("1994-11-05T08:15:30-05:30", ref_date)
    assert len(results) == 1
    res = results[0]
    assert res.text == "1994-11-05T08:15:30-05:30"
    assert res.start.get(CivilTimeComponent.YEAR) == 1994
    assert res.start.get(CivilTimeComponent.MONTH) == 11
    assert res.start.get(CivilTimeComponent.DAY) == 5
    assert res.start.get(CivilTimeComponent.HOUR) == 8
    assert res.start.get(CivilTimeComponent.MINUTE) == 15
    assert res.start.get(CivilTimeComponent.SECOND) == 30
    assert res.start.get(CivilTimeComponent.TIMEZONE_OFFSET) == -330


def test_zh_default_combines_hans_and_hant():
    ref_date = datetime.datetime(2012, 8, 8, 12, 0)

    results1 = chrono.zh.parse("明天早上8点", ref_date)
    assert len(results1) == 1
    assert results1[0].text == "明天早上8点"
    assert results1[0].start.get(CivilTimeComponent.YEAR) == 2012
    assert results1[0].start.get(CivilTimeComponent.MONTH) == 8
    assert results1[0].start.get(CivilTimeComponent.DAY) == 9
    assert results1[0].start.get(CivilTimeComponent.HOUR) == 8

    results2 = chrono.zh.parse("明天早上8點", ref_date)
    assert len(results2) == 1
    assert results2[0].text == "明天早上8點"
    assert results2[0].start.get(CivilTimeComponent.YEAR) == 2012
    assert results2[0].start.get(CivilTimeComponent.MONTH) == 8
    assert results2[0].start.get(CivilTimeComponent.DAY) == 9
    assert results2[0].start.get(CivilTimeComponent.HOUR) == 8
