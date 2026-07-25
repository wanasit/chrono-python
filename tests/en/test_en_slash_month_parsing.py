import datetime
import chrono_python as chrono
from chrono_python.types import DateTimePrecision
from chrono_python.common.types import CivilTimeComponent

def test_slash_month_year():
    # 04/2016
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = chrono.parse('04/2016', ref_date)
    assert len(results) == 1
    assert results[0].text == '04/2016'
    assert results[0].index == 0
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2016
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 4
    assert results[0].moment.get(CivilTimeComponent.DAY) == 1
    assert results[0].moment.is_certain(CivilTimeComponent.YEAR) is True
    assert results[0].moment.is_certain(CivilTimeComponent.MONTH) is True
    assert results[0].moment.is_certain(CivilTimeComponent.DAY) is False

    # Published: 06/2004
    results = chrono.parse('Published: 06/2004', ref_date)
    assert len(results) == 1
    assert results[0].text == '06/2004'
    assert results[0].index == 11
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2004
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 6
    assert results[0].moment.get(CivilTimeComponent.DAY) == 1
