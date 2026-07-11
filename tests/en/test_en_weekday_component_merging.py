import pytest
from datetime import datetime
from chrono_python.locales.en import parse
from chrono_python.common.types import CivilTimeComponent

def test_en_weekday_component_merging():
    reference_date = datetime(2014, 7, 10)  # July 10, 2014 (Thursday)
    
    # "Sunday, 12/7/2014"
    results = parse("Sunday, 12/7/2014", reference_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "Sunday, 12/7/2014"
    assert result.moment.get(CivilTimeComponent.YEAR) == 2014
    assert result.moment.get(CivilTimeComponent.MONTH) == 12
    assert result.moment.get(CivilTimeComponent.DAY) == 7
    assert result.moment.get(CivilTimeComponent.WEEKDAY) == 0
    
    # "Tuesday, January 13, 2012"
    results = parse("Tuesday, January 13, 2012", reference_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "Tuesday, January 13, 2012"
    assert result.moment.get(CivilTimeComponent.YEAR) == 2012
    assert result.moment.get(CivilTimeComponent.MONTH) == 1
    assert result.moment.get(CivilTimeComponent.DAY) == 13
    assert result.moment.get(CivilTimeComponent.WEEKDAY) == 2
