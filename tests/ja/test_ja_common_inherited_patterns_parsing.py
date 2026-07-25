import datetime

import chrono_python as chrono
from chrono_python.common.types import CivilTimeComponent


def test_ja_inherited_iso_format():
    # ISO Format should be parsed successfully using the Japanese config
    results = chrono.ja.parse("2021-12-03")
    assert len(results) == 1
    result = results[0]
    assert result.text == "2021-12-03"
    assert result.moment.get(CivilTimeComponent.YEAR) == 2021
    assert result.moment.get(CivilTimeComponent.MONTH) == 12
    assert result.moment.get(CivilTimeComponent.DAY) == 3


def test_ja_inherited_slash_date():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    
    # 8/10 -> MM/DD
    results = chrono.ja.parse("8/10", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "8/10"
    assert result.moment.get(CivilTimeComponent.YEAR) == 2012
    assert result.moment.get(CivilTimeComponent.MONTH) == 8
    assert result.moment.get(CivilTimeComponent.DAY) == 10

    # 8/10/2012 -> MM/DD/YYYY
    results = chrono.ja.parse("8/10/2012", ref_date)
    assert len(results) == 1
    assert results[0].text == "8/10/2012"
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2012
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 8
    assert results[0].moment.get(CivilTimeComponent.DAY) == 10

    # 2012/8/10 -> YYYY/MM/DD
    results = chrono.ja.parse("2012/8/10", ref_date)
    assert len(results) == 1
    assert results[0].text == "2012/8/10"
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2012
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 8
    assert results[0].moment.get(CivilTimeComponent.DAY) == 10

    # 04/2016 -> MM/YYYY
    results = chrono.ja.parse("04/2016", ref_date)
    assert len(results) == 1
    assert results[0].text == "04/2016"
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2016
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 4
    assert results[0].moment.get(CivilTimeComponent.DAY) == 1

    # 2012/08 -> YYYY/MM
    results = chrono.ja.parse("2012/08", ref_date)
    assert len(results) == 1
    assert results[0].text == "2012/08"
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2012
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 8
    assert results[0].moment.get(CivilTimeComponent.DAY) == 1



def test_ja_inherited_time_expression():
    ref_date = datetime.datetime(2020, 1, 1, 12, 0)
    
    # 15:30
    results = chrono.ja.parse("15:30", ref_date)
    assert len(results) == 1
    assert results[0].text == "15:30"
    assert results[0].moment.get(CivilTimeComponent.HOUR) == 15
    assert results[0].moment.get(CivilTimeComponent.MINUTE) == 30

    # 1:30-2:30 range
    results = chrono.ja.parse("1:30-2:30", ref_date)
    assert len(results) == 1
    assert results[0].text == "1:30-2:30"
    assert results[0].start.get(CivilTimeComponent.HOUR) == 1
    assert results[0].start.get(CivilTimeComponent.MINUTE) == 30
    assert results[0].end.get(CivilTimeComponent.HOUR) == 2
    assert results[0].end.get(CivilTimeComponent.MINUTE) == 30

