import datetime
from chrono_python.locales import es
from chrono_python.common.types import CivilTimeComponent


def test_es_month_name_single():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = es.parse("10 Agosto 2012", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "10 Agosto 2012"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10

    results = es.parse("10 Agosto 234 AC", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "10 Agosto 234 AC"
    assert results[0].moment.get(CivilTimeComponent.YEAR) == -234
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 8
    assert results[0].moment.get(CivilTimeComponent.DAY) == 10

    results = es.parse("10 Agosto 88 d. C.", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "10 Agosto 88 d. C."
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 88
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 8
    assert results[0].moment.get(CivilTimeComponent.DAY) == 10

    ref_date = datetime.datetime(2013, 8, 10, 12, 0)
    results = es.parse("Dom 15Sep", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "Dom 15Sep"
    dt = results[0].moment.datetime()
    assert dt.year == 2013
    assert dt.month == 9
    assert dt.day == 15

    results = es.parse("DOM 15SEP", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "DOM 15SEP"
    dt = results[0].moment.datetime()
    assert dt.year == 2013
    assert dt.month == 9
    assert dt.day == 15

    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = es.parse("La fecha límite es 10 Agosto", ref_date)
    assert len(results) == 1
    assert results[0].index == 19
    assert results[0].text == "10 Agosto"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10

    results = es.parse("La fecha límite es el martes, 10 de enero", ref_date)
    assert len(results) == 1
    assert results[0].index == 22
    assert results[0].text == "martes, 10 de enero"
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2013
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 1
    assert results[0].moment.get(CivilTimeComponent.DAY) == 10
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 2

    results = es.parse("La fecha límite es el miércoles, 10 de enero ", ref_date)
    assert len(results) == 1
    assert results[0].index == 22
    assert results[0].text == "miércoles, 10 de enero"
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2013
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 1
    assert results[0].moment.get(CivilTimeComponent.DAY) == 10
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 3

    ref_date = datetime.datetime(2010, 2, 1, 12, 0)
    results = es.parse("10 de Agosto de 2012", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "10 de Agosto de 2012"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10


def test_es_month_name_range():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = es.parse("10 - 22 Agosto 2012", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "10 - 22 Agosto 2012"
    assert results[0].start.get(CivilTimeComponent.DAY) == 10
    assert results[0].end.get(CivilTimeComponent.DAY) == 22
    assert results[0].start.get(CivilTimeComponent.MONTH) == 8
    assert results[0].end.get(CivilTimeComponent.MONTH) == 8

    results = es.parse("10 a 22 Agosto 2012", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "10 a 22 Agosto 2012"
    assert results[0].start.get(CivilTimeComponent.DAY) == 10
    assert results[0].end.get(CivilTimeComponent.DAY) == 22

    results = es.parse("10 Agosto - 12 Septiembre", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "10 Agosto - 12 Septiembre"
    assert results[0].start.get(CivilTimeComponent.MONTH) == 8
    assert results[0].start.get(CivilTimeComponent.DAY) == 10
    assert results[0].end.get(CivilTimeComponent.MONTH) == 9
    assert results[0].end.get(CivilTimeComponent.DAY) == 12

    results = es.parse("10 Agosto - 12 Septiembre 2013", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "10 Agosto - 12 Septiembre 2013"
    assert results[0].start.get(CivilTimeComponent.YEAR) == 2013
    assert results[0].start.get(CivilTimeComponent.MONTH) == 8
    assert results[0].end.get(CivilTimeComponent.YEAR) == 2013
    assert results[0].end.get(CivilTimeComponent.MONTH) == 9


def test_es_month_name_combined():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = es.parse("12 de julio a las 19:00", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "12 de julio a las 19:00"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 7
    assert dt.day == 12
    assert dt.hour == 19
    assert dt.minute == 0


def test_es_month_name_impossible_strict():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    assert len(es.strict.parse("32 Agosto 2014", ref_date)) == 0
    assert len(es.strict.parse("29 Febrero 2014", ref_date)) == 0
    assert len(es.strict.parse("32 Agosto", ref_date)) == 0
