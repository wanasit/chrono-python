import pytest
from datetime import datetime
from chrono_python.locales.ja import parse
from chrono_python.common.types import CivilTimeComponent

def test_ja_weekday_component_merging():
    reference_date = datetime(2014, 7, 10)
    
    # "2014年7月12日 (土)"
    results = parse("2014年7月12日 (土)", reference_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "2014年7月12日 (土)"
    assert result.moment.get(CivilTimeComponent.YEAR) == 2014
    assert result.moment.get(CivilTimeComponent.MONTH) == 7
    assert result.moment.get(CivilTimeComponent.DAY) == 12
    assert result.moment.get(CivilTimeComponent.WEEKDAY) == 6
    
    # "7月12日 土曜日"
    results = parse("7月12日 土曜日", reference_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "7月12日 土曜日"
    assert result.moment.get(CivilTimeComponent.YEAR) == 2014
    assert result.moment.get(CivilTimeComponent.MONTH) == 7
    assert result.moment.get(CivilTimeComponent.DAY) == 12
    assert result.moment.get(CivilTimeComponent.WEEKDAY) == 6
