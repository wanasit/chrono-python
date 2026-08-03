import datetime
from chrono_python.locales import pt
from chrono_python.common.types import CivilTimeComponent


def test_pt_weekday_single():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)  # Friday (5)

    results = pt.parse("segunda", ref_date)
    assert len(results) == 1
    assert results[0].text == "segunda"
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 1

    results = pt.parse("terça-feira", ref_date)
    assert len(results) == 1
    assert results[0].text == "terça-feira"
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 2

    results = pt.parse("este domingo", ref_date)
    assert len(results) == 1
    assert results[0].text == "este domingo"
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 0

    results = pt.parse("próxima sexta", ref_date)
    assert len(results) == 1
    assert results[0].text == "próxima sexta"
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 5
