import datetime
from chrono_python.locales import nl


def test_nl_relative_date_future():
    ref_date = datetime.datetime(2016, 10, 1, 12, 0)

    results = nl.parse("komend uur", ref_date)
    assert len(results) == 1
    assert results[0].text == "komend uur"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 10
    assert dt.day == 1
    assert dt.hour == 13

    results = nl.parse("volgende week", ref_date)
    assert len(results) == 1
    assert results[0].text == "volgende week"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 10
    assert dt.day == 8
    assert dt.hour == 12

    results = nl.parse("volgende dag", ref_date)
    assert len(results) == 1
    assert results[0].text == "volgende dag"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 10
    assert dt.day == 2
    assert dt.hour == 12

    results = nl.parse("volgende maand", ref_date)
    assert len(results) == 1
    assert results[0].text == "volgende maand"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 11
    assert dt.day == 1
    assert dt.hour == 12

    results = nl.parse("aankomende maand", ref_date)
    assert len(results) == 1
    assert results[0].text == "aankomende maand"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 11
    assert dt.day == 1
    assert dt.hour == 12

    ref_date = datetime.datetime(2020, 11, 22, 12, 11, 32, 6000)
    results = nl.parse("volgend jaar", ref_date)
    assert len(results) == 1
    assert results[0].text == "volgend jaar"
    dt = results[0].moment.datetime()
    assert dt.year == 2021
    assert dt.month == 11
    assert dt.day == 22
    assert dt.hour == 12
    assert dt.minute == 11
    assert dt.second == 32


def test_nl_relative_date_certainty():
    ref_date = datetime.datetime(2016, 10, 7, 12, 0)

    results = nl.parse("komend uur", ref_date)
    assert len(results) == 1
    assert results[0].text == "komend uur"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 10
    assert dt.day == 7
    assert dt.hour == 13

    results = nl.parse("volgende maand", ref_date)
    assert len(results) == 1
    assert results[0].text == "volgende maand"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 11
    assert dt.day == 7
    assert dt.hour == 12
