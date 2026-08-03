import datetime
from chrono_python.locales import fi


def test_fi_time_unit_within_sisalla():
    ref_date = datetime.datetime(2012, 8, 10)  # month 8, day 10

    results = fi.parse("pitää tehdä jotain 5 päivää sisällä", ref_date)
    assert len(results) == 1
    assert results[0].text == "5 päivää sisällä"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 15

    ref_date_time = datetime.datetime(2012, 8, 10, 12, 14)
    results = fi.parse("5 minuuttia sisällä", ref_date_time)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "5 minuuttia sisällä"
    dt = results[0].moment.datetime()
    assert dt.hour == 12
    assert dt.minute == 19

    results = fi.parse("1 tuntia sisällä", ref_date_time)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "1 tuntia sisällä"
    dt = results[0].moment.datetime()
    assert dt.hour == 13
    assert dt.minute == 14

    results = fi.parse("2 viikkoa sisällä", ref_date_time)
    assert len(results) == 1
    assert results[0].text == "2 viikkoa sisällä"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 24


def test_fi_time_unit_within_kuluessa():
    ref_date = datetime.datetime(2012, 8, 10)

    results = fi.parse("5 päivää kuluessa", ref_date)
    assert len(results) == 1
    assert results[0].text == "5 päivää kuluessa"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 15

    ref_date_time = datetime.datetime(2012, 8, 10, 12, 14)
    results = fi.parse("yksi vuotta kuluessa", ref_date_time)
    assert len(results) == 1
    assert results[0].text == "yksi vuotta kuluessa"
    dt = results[0].moment.datetime()
    assert dt.year == 2013
    assert dt.month == 8
    assert dt.day == 10
    assert dt.hour == 12
    assert dt.minute == 14


def test_fi_time_unit_within_paasta():
    ref_date_time = datetime.datetime(2012, 8, 10, 12, 14)

    results = fi.parse("5 minuuttia päästä", ref_date_time)
    assert len(results) == 1
    assert results[0].text == "5 minuuttia päästä"
    dt = results[0].moment.datetime()
    assert dt.hour == 12
    assert dt.minute == 19

    results = fi.parse("3 päivää päästä", ref_date_time)
    assert len(results) == 1
    assert results[0].text == "3 päivää päästä"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 13

    ref_date_2016 = datetime.datetime(2016, 10, 1)
    results = fi.parse("2 viikkoa päästä", ref_date_2016)
    assert len(results) == 1
    assert results[0].text == "2 viikkoa päästä"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 10
    assert dt.day == 15
