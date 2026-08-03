import datetime
from chrono_python.locales import nl


def test_nl_time_unit_within_single():
    ref_date = datetime.datetime(2012, 8, 10)

    results = nl.parse("we have to make something binnen de 10 dagen", ref_date)
    assert len(results) == 1
    assert results[0].index == 26
    assert results[0].text == "binnen de 10 dagen"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 20

    ref_date = datetime.datetime(2012, 8, 10, 12, 14)
    results = nl.parse("binnen 5 minuten", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "binnen 5 minuten"
    dt = results[0].moment.datetime()
    assert dt.hour == 12
    assert dt.minute == 19

    results = nl.parse("wait voor 5 minuten", ref_date)
    assert len(results) == 1
    assert results[0].index == 5
    assert results[0].text == "voor 5 minuten"
    dt = results[0].moment.datetime()
    assert dt.hour == 12
    assert dt.minute == 19

    results = nl.parse("binnen 1 uur", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "binnen 1 uur"
    dt = results[0].moment.datetime()
    assert dt.hour == 13
    assert dt.minute == 14

    results = nl.parse("Binnen 5 minuten ben ik thuis", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "Binnen 5 minuten"
    dt = results[0].moment.datetime()
    assert dt.hour == 12
    assert dt.minute == 19

    results = nl.parse("Binnen de 5 minuten moet een auto zich verzetten", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "Binnen de 5 minuten"
    dt = results[0].moment.datetime()
    assert dt.hour == 12
    assert dt.minute == 19

    results = nl.parse("Binnen 5 seconden moet een auto zich verzetten", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "Binnen 5 seconden"
    dt = results[0].moment.datetime()
    assert dt.hour == 12
    assert dt.minute == 14
    assert dt.second == 5

    results = nl.parse("Binnen de 2 weken", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "Binnen de 2 weken"
    dt = results[0].moment.datetime()
    assert dt.month == 8
    assert dt.day == 24

    results = nl.parse("Binnen een maand", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "Binnen een maand"
    dt = results[0].moment.datetime()
    assert dt.month == 9
    assert dt.day == 10

    results = nl.parse("Binnen een jaar", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "Binnen een jaar"
    dt = results[0].moment.datetime()
    assert dt.year == 2013
    assert dt.month == 8
    assert dt.day == 10

    ref_date = datetime.datetime(2016, 10, 1)
    results = nl.parse("binnen een week", ref_date)
    assert len(results) == 1
    assert results[0].text == "binnen een week"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 10
    assert dt.day == 8


def test_nl_time_unit_within_implied_values():
    ref_date = datetime.datetime(2020, 7, 10, 12, 14)

    results = nl.parse("Binnen 24 uur", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.year == 2020
    assert dt.month == 7
    assert dt.day == 11
    assert dt.hour == 12
    assert dt.minute == 14

    results = nl.parse("binnen een dag", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.year == 2020
    assert dt.month == 7
    assert dt.day == 11
    assert dt.hour == 12
    assert dt.minute == 14


def test_nl_time_unit_within_certainty():
    ref_date = datetime.datetime(2016, 10, 1, 14, 52)

    results = nl.parse("binnen 2 minuten", ref_date)
    assert len(results) == 1
    assert results[0].text == "binnen 2 minuten"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 10
    assert dt.day == 1
    assert dt.hour == 14
    assert dt.minute == 54

    results = nl.parse("binnen 2 uur", ref_date)
    assert len(results) == 1
    assert results[0].text == "binnen 2 uur"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 10
    assert dt.day == 1
    assert dt.hour == 16
    assert dt.minute == 52

    results = nl.parse("binnen de 12 maand", ref_date)
    assert len(results) == 1
    assert results[0].text == "binnen de 12 maand"
    dt = results[0].moment.datetime()
    assert dt.year == 2017
    assert dt.month == 10
    assert dt.day == 1

    results = nl.parse("binnen de 3 dagen", ref_date)
    assert len(results) == 1
    assert results[0].text == "binnen de 3 dagen"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 10
    assert dt.day == 4
