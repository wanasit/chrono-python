import pytest
from datetime import datetime
from chrono_python.locales.ja import parse
from chrono_python.common.types import CivilTimeComponent

def test_ja_weekday_with_parentheses_parsing():
    reference_date = datetime(2012, 8, 9)

    results = parse("(水)", reference_date)
    assert len(results) == 1
    result = results[0]
    assert result.index == 0
    assert result.text == "(水)"
    assert result.moment.get(CivilTimeComponent.WEEKDAY) == 3
    assert not result.moment.is_certain(CivilTimeComponent.DAY)

    results = parse("（土）", reference_date)
    assert len(results) == 1
    result = results[0]
    assert result.index == 0
    assert result.text == "（土）"
    assert result.moment.get(CivilTimeComponent.WEEKDAY) == 6
    assert not result.moment.is_certain(CivilTimeComponent.DAY)
