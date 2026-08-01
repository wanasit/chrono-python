import datetime
from chrono_python.locales import it


def test_it_casual_time_single():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # stamattina
    results = it.parse("La scadenza era stamattina ", ref_date)
    assert len(results) == 1
    assert results[0].index == 16
    assert results[0].text == "stamattina"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10
    assert dt.hour == 6

    # pomeriggio
    results = it.parse("La scadenza era questo pomeriggio ", ref_date)
    assert len(results) == 1
    assert results[0].index == 23
    assert results[0].text == "pomeriggio"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10
    assert dt.hour == 15

    # mezzanotte
    results = it.parse("La scadenza è mezzanotte ", ref_date)
    assert len(results) == 1
    assert results[0].text == "mezzanotte"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 11
    assert dt.hour == 0

    # mezzanotte at 1am
    ref_date_1am = datetime.datetime(2012, 8, 10, 1, 0)
    results = it.parse("La scadenza era mezzanotte ", ref_date_1am)
    assert len(results) == 1
    assert results[0].text == "mezzanotte"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10
    assert dt.hour == 0


def test_it_casual_time_combined():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    results = it.parse("La scadenza è oggi alle 17", ref_date)
    assert len(results) == 1
    assert results[0].index == 14
    assert results[0].text == "oggi alle 17"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10
    assert dt.hour == 17

    results = it.parse("Domani a mezzogiorno", datetime.datetime(2012, 8, 10, 14, 0))
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 11
    assert dt.hour == 12
