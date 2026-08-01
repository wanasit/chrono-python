import datetime
from chrono_python.locales import it


def test_it_relative_date_parsing():
    # la settimana prossima
    ref_date = datetime.datetime(2016, 10, 1, 12, 0)
    results = it.parse("la settimana prossima", ref_date)
    assert len(results) == 1
    assert results[0].text == "la settimana prossima"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 10
    assert dt.day == 8

    # la settimana scorsa
    results = it.parse("la settimana scorsa", ref_date)
    assert len(results) == 1
    assert results[0].text == "la settimana scorsa"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 9
    assert dt.day == 24

    # il mese prossimo
    results = it.parse("il mese prossimo", ref_date)
    assert len(results) == 1
    assert results[0].text == "il mese prossimo"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 11
    assert dt.day == 1

    # il mese scorso
    results = it.parse("il mese scorso", ref_date)
    assert len(results) == 1
    assert results[0].text == "il mese scorso"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 9
    assert dt.day == 1

    # l'anno prossimo
    ref_date_2020 = datetime.datetime(2020, 11, 22, 12, 11, 32, 6)
    results = it.parse("l'anno prossimo", ref_date_2020)
    assert len(results) == 1
    assert results[0].text == "l'anno prossimo"
    dt = results[0].moment.datetime()
    assert dt.year == 2021
    assert dt.month == 11
    assert dt.day == 22

    # l'anno scorso
    results = it.parse("l'anno scorso", ref_date_2020)
    assert len(results) == 1
    assert results[0].text == "l'anno scorso"
    dt = results[0].moment.datetime()
    assert dt.year == 2019
    assert dt.month == 11
    assert dt.day == 22
