import datetime
from chrono_python.locales import fi


def test_fi_time_unit_relative_future():
    ref_date = datetime.datetime(2012, 7, 10, 12, 14)

    results = fi.parse("seuraava 2 viikkoa", ref_date)
    assert len(results) == 1
    assert results[0].text == "seuraava 2 viikkoa"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 7
    assert dt.day == 24

    results = fi.parse("seuraavan 2 viikon", ref_date)
    assert len(results) == 1
    assert results[0].text == "seuraavan 2 viikon"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 7
    assert dt.day == 24

    results = fi.parse("seuraavat 3 päivää", ref_date)
    assert len(results) == 1
    assert results[0].text == "seuraavat 3 päivää"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 7
    assert dt.day == 13

    results = fi.parse("seuraavien 3 päivän", ref_date)
    assert len(results) == 1
    assert results[0].text == "seuraavien 3 päivän"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 7
    assert dt.day == 13


def test_fi_time_unit_relative_past():
    ref_date = datetime.datetime(2012, 7, 10, 12, 14)

    results = fi.parse("edellinen 2 viikkoa", ref_date)
    assert len(results) == 1
    assert results[0].text == "edellinen 2 viikkoa"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 6
    assert dt.day == 26

    results = fi.parse("edellisten 2 viikon", ref_date)
    assert len(results) == 1
    assert results[0].text == "edellisten 2 viikon"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 6
    assert dt.day == 26

    results = fi.parse("viimeiset 3 päivää", ref_date)
    assert len(results) == 1
    assert results[0].text == "viimeiset 3 päivää"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 7
    assert dt.day == 7

    results = fi.parse("viimeisten 3 päivän", ref_date)
    assert len(results) == 1
    assert results[0].text == "viimeisten 3 päivän"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 7
    assert dt.day == 7

    results = fi.parse("kuluneet 3 päivää", ref_date)
    assert len(results) == 1
    assert results[0].text == "kuluneet 3 päivää"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 7
    assert dt.day == 7


def test_fi_time_unit_relative_plus_minus():
    ref_date = datetime.datetime(2012, 7, 10, 12, 14)

    results = fi.parse("+15 minuuttia", ref_date)
    assert len(results) == 1
    assert results[0].text == "+15 minuuttia"
    dt = results[0].moment.datetime()
    assert dt.hour == 12
    assert dt.minute == 29

    results = fi.parse("+15min", ref_date)
    assert len(results) == 1
    assert results[0].text == "+15min"
    dt = results[0].moment.datetime()
    assert dt.hour == 12
    assert dt.minute == 29

    results = fi.parse("+1 päivä 2 tuntia", ref_date)
    assert len(results) == 1
    assert results[0].text == "+1 päivä 2 tuntia"
    dt = results[0].moment.datetime()
    assert dt.day == 11
    assert dt.hour == 14
    assert dt.minute == 14

    ref_date_2015 = datetime.datetime(2015, 7, 10, 12, 14)
    results = fi.parse("-3vuotta", ref_date_2015)
    assert len(results) == 1
    assert results[0].text == "-3vuotta"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 7
    assert dt.day == 10
