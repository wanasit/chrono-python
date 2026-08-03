import datetime
from chrono_python.locales import es
from chrono_python.common.types import CivilTimeComponent


def test_es_slash_date_single():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = es.parse("lunes 8/2/2016", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "lunes 8/2/2016"
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2016
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 2
    assert results[0].moment.get(CivilTimeComponent.DAY) == 8

    results = es.parse("Martes 9/2/2016", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "Martes 9/2/2016"
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2016
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 2
    assert results[0].moment.get(CivilTimeComponent.DAY) == 9
