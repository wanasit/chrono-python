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
    
    # Slash dates (e.g. 8/10) should be parsed successfully using the Japanese config
    results = chrono.ja.parse("8/10", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "8/10"
    assert result.moment.get(CivilTimeComponent.YEAR) == 2012
    assert result.moment.get(CivilTimeComponent.MONTH) == 8
    assert result.moment.get(CivilTimeComponent.DAY) == 10


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

