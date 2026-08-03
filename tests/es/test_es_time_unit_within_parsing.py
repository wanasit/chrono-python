import datetime
from chrono_python.locales import es


def test_es_time_unit_within_single():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = es.parse("Tenemos que hacer algo en 5 días.", ref_date)
    assert len(results) == 1
    assert results[0].index == 23
    assert results[0].text == "en 5 días"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 15

    ref_date = datetime.datetime(2012, 8, 10, 11, 12)
    results = es.parse("Tenemos que hacer algo en cinco días.", ref_date)
    assert len(results) == 1
    assert results[0].index == 23
    assert results[0].text == "en cinco días"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 15
    assert dt.hour == 11
    assert dt.minute == 12

    ref_date = datetime.datetime(2012, 8, 10, 12, 14)
    results = es.parse("en 5 minutos", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "en 5 minutos"
    dt = results[0].moment.datetime()
    assert dt.minute == 19

    results = es.parse("por 5 minutos", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "por 5 minutos"
    dt = results[0].moment.datetime()
    assert dt.minute == 19

    results = es.parse("en 1 hora", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "en 1 hora"
    dt = results[0].moment.datetime()
    assert dt.hour == 13

    results = es.parse("establecer un temporizador de 5 minutos", ref_date)
    assert len(results) == 1
    assert results[0].index == 27
    assert results[0].text == "de 5 minutos"
    dt = results[0].moment.datetime()
    assert dt.minute == 19

    results = es.parse("En 5 minutos me voy a casa", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "En 5 minutos"

    results = es.parse("En 5 segundos un auto se moverá", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "En 5 segundos"
    dt = results[0].moment.datetime()
    assert dt.second == 5

    results = es.parse("en dos semanas", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "en dos semanas"
    dt = results[0].moment.datetime()
    assert dt.day == 24

    ref_date_7_14 = datetime.datetime(2012, 8, 10, 7, 14)
    results = es.parse("dentro de un mes", ref_date_7_14)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "dentro de un mes"
    dt = results[0].moment.datetime()
    assert dt.month == 9

    ref_date_july = datetime.datetime(2012, 7, 10, 22, 14)
    results = es.parse("en algunos meses", ref_date_july)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "en algunos meses"
    dt = results[0].moment.datetime()
    assert dt.month == 10

    results = es.parse("en un año", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "en un año"
    dt = results[0].moment.datetime()
    assert dt.year == 2013

    results = es.parse("dentro de un año", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "dentro de un año"
    dt = results[0].moment.datetime()
    assert dt.year == 2013
