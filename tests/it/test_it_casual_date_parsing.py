import datetime
from chrono_python.locales import it


def test_it_casual_date_single():
    ref_date = datetime.datetime(2012, 8, 10, 8, 9, 10, 11)

    # adesso
    results = it.parse("La scadenza è adesso", ref_date)
    assert len(results) == 1
    assert results[0].index == 14
    assert results[0].text == "adesso"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10
    assert dt.hour == 8
    assert dt.minute == 9
    assert dt.second == 10

    # oggi
    ref_date = datetime.datetime(2012, 8, 10, 14, 12)
    results = it.parse("La scadenza è oggi", ref_date)
    assert len(results) == 1
    assert results[0].index == 14
    assert results[0].text == "oggi"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10

    # domani
    ref_date = datetime.datetime(2012, 8, 10, 17, 10)
    results = it.parse("La scadenza è domani", ref_date)
    assert len(results) == 1
    assert results[0].index == 14
    assert results[0].text == "domani"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 11

    # ieri
    ref_date = datetime.datetime(2012, 8, 10, 12)
    results = it.parse("La scadenza era ieri", ref_date)
    assert len(results) == 1
    assert results[0].index == 16
    assert results[0].text == "ieri"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 9

    # ieri sera
    results = it.parse("La scadenza era ieri sera ", ref_date)
    assert len(results) == 1
    assert results[0].index == 16
    assert results[0].text == "ieri sera"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 9
    assert dt.hour == 20

    # stasera
    results = it.parse("La scadenza era stasera ", ref_date)
    assert len(results) == 1
    assert results[0].index == 16
    assert results[0].text == "stasera"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10
    assert dt.hour == 22

    # dopodomani
    results = it.parse("La scadenza è dopodomani", ref_date)
    assert len(results) == 1
    assert results[0].text == "dopodomani"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 12
