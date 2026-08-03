import datetime
from chrono_python.locales import es
from chrono_python.common.types import CivilTimeComponent


def test_es_casual_date_single():
    ref_date = datetime.datetime(2012, 8, 10, 8, 9, 10, 11)
    results = es.parse("La fecha límite es ahora", ref_date)
    assert len(results) == 1
    assert results[0].index == 19
    assert results[0].text == "ahora"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10
    assert dt.hour == 8
    assert dt.minute == 9
    assert dt.second == 10

    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = es.parse("La fecha límite es hoy", ref_date)
    assert len(results) == 1
    assert results[0].index == 19
    assert results[0].text == "hoy"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10

    results = es.parse("La fecha límite es Mañana", ref_date)
    assert len(results) == 1
    assert results[0].index == 19
    assert results[0].text == "Mañana"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 11

    results = es.parse("La fecha límite fue ayer", ref_date)
    assert len(results) == 1
    assert results[0].index == 20
    assert results[0].text == "ayer"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 9

    results = es.parse("La fecha límite fue ayer de noche ", ref_date)
    assert len(results) == 1
    assert results[0].index == 20
    assert results[0].text == "ayer de noche"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 9
    assert dt.hour == 22

    results = es.parse("La fecha límite fue esta mañana ", ref_date)
    assert len(results) == 1
    assert results[0].index == 20
    assert results[0].text == "esta mañana"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10
    assert dt.hour == 6

    results = es.parse("La fecha límite fue esta tarde ", ref_date)
    assert len(results) == 1
    assert results[0].index == 20
    assert results[0].text == "esta tarde"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10
    assert dt.hour == 15


def test_es_casual_date_combined():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = es.parse("La fecha límite es hoy a las 5PM", ref_date)
    assert len(results) == 1
    assert results[0].index == 19
    assert results[0].text == "hoy a las 5PM"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10
    assert dt.hour == 17


def test_es_casual_date_random():
    ref_date = datetime.datetime(2012, 1, 1, 12, 0)
    results = es.parse("esta noche", ref_date)
    assert len(results) == 1
    assert results[0].text == "esta noche"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 1
    assert dt.day == 1
    assert dt.hour == 22

    results = es.parse("esta noche 8pm", ref_date)
    assert len(results) == 1
    assert results[0].text == "esta noche 8pm"
    dt = results[0].moment.datetime()
    assert dt.hour == 20

    results = es.parse("esta noche a las 8", ref_date)
    assert len(results) == 1
    assert results[0].text == "esta noche a las 8"
    dt = results[0].moment.datetime()
    assert dt.hour == 20

    results = es.parse("jueves", ref_date)
    assert len(results) == 1
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 4

    results = es.parse("viernes", ref_date)
    assert len(results) == 1
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 5

    ref_date2 = datetime.datetime(2020, 8, 1, 11, 0)
    results = es.parse("el mediodía", ref_date2)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.hour == 12
    assert dt.day == 1

    results = es.parse("la medianoche", ref_date2)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.hour == 0
    assert dt.day == 2


def test_es_casual_date_negative():
    assert len(es.parse("nohoy")) == 0
    assert len(es.parse("hymañana")) == 0
    assert len(es.parse("xayer")) == 0
    assert len(es.parse("porhora")) == 0
    assert len(es.parse("ahoraxsd")) == 0
