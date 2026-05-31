import datetime
import pytest

import chrono_python as chrono
from chrono_python.common.types import DateTimeComponent


def test_ja_inherited_iso_format():
    # ISO Format should be parsed successfully using the Japanese config
    results = chrono.ja.parse("2021-12-03T15:30:00")
    assert len(results) == 1
    result = results[0]
    assert result.text == "2021-12-03"
    assert result.moment.get(DateTimeComponent.YEAR) == 2021
    assert result.moment.get(DateTimeComponent.MONTH) == 12
    assert result.moment.get(DateTimeComponent.DAY) == 3


def test_ja_inherited_slash_date():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    
    # Slash dates (e.g. 8/10) should be parsed successfully using the Japanese config
    results = chrono.ja.parse("8/10", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "8/10"
    assert result.moment.get(DateTimeComponent.YEAR) == 2012
    assert result.moment.get(DateTimeComponent.MONTH) == 8
    assert result.moment.get(DateTimeComponent.DAY) == 10
