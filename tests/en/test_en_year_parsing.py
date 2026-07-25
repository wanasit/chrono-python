import datetime
import chrono_python as chrono
from chrono_python.common.types import CivilTimeComponent

def test_era_parsing():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # 10 August 234 BCE -> year -234
    results = chrono.parse('10 August 234 BCE', ref_date)
    assert len(results) == 1
    assert results[0].text == '10 August 234 BCE'
    assert results[0].moment.get(CivilTimeComponent.YEAR) == -234
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 8
    assert results[0].moment.get(CivilTimeComponent.DAY) == 10

    # 10 August 234 BC -> year -234
    results = chrono.parse('10 August 234 BC', ref_date)
    assert len(results) == 1
    assert results[0].text == '10 August 234 BC'
    assert results[0].moment.get(CivilTimeComponent.YEAR) == -234

    # 10 August 2555 BE -> year 2012
    results = chrono.parse('10 August 2555 BE', ref_date)
    assert len(results) == 1
    assert results[0].text == '10 August 2555 BE'
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2012

    # August 10 2555 BE -> year 2012
    results = chrono.parse('August 10 2555 BE', ref_date)
    assert len(results) == 1
    assert results[0].text == 'August 10 2555 BE'
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2012

    # 10 August 1999 AD -> year 1999
    results = chrono.parse('10 August 1999 AD', ref_date)
    assert len(results) == 1
    assert results[0].text == '10 August 1999 AD'
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 1999

    # 10 August 123 CE -> year 123
    results = chrono.parse('10 August 123 CE', ref_date)
    assert len(results) == 1
    assert results[0].text == '10 August 123 CE'
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 123
