import datetime
from chrono_python.locales import nl


def test_nl_weekday_single():
    ref_date = datetime.datetime(2012, 8, 9)  # Thursday

    results = nl.parse("maandag", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "maandag"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 6

    results = nl.parse("donderdag", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "donderdag"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 9

    results = nl.parse("zondag", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "zondag"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 12

    results = nl.parse("De deadline is vorige vrijdag...", ref_date)
    assert len(results) == 1
    assert results[0].index == 15
    assert results[0].text == "vorige vrijdag"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 3

    ref_date = datetime.datetime(2012, 8, 12)
    results = nl.parse("De deadline is vorige vrijdag...", ref_date)
    assert len(results) == 1
    assert results[0].index == 15
    assert results[0].text == "vorige vrijdag"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10

    ref_date = datetime.datetime(2015, 4, 16)
    results = nl.parse("Laten we een meeting hebben op volgende week vrijdag", ref_date)
    assert len(results) == 1
    assert results[0].index == 28
    assert results[0].text == "op volgende week vrijdag"
    dt = results[0].moment.datetime()
    assert dt.year == 2015
    assert dt.month == 4
    assert dt.day == 24

    ref_date = datetime.datetime(2015, 4, 18)
    results = nl.parse("Ik plan een vrije dag op volgende week dinsdag", ref_date)
    assert len(results) == 1
    assert results[0].index == 22
    assert results[0].text == "op volgende week dinsdag"
    dt = results[0].moment.datetime()
    assert dt.year == 2015
    assert dt.month == 4
    assert dt.day == 21


def test_nl_weekday_with_casual_time():
    ref_date = datetime.datetime(2015, 4, 18)
    results = nl.parse("Laten we op dinsdag ochtend afspreken", ref_date)
    assert len(results) == 1
    assert results[0].index == 9
    assert results[0].text == "op dinsdag ochtend"
    dt = results[0].moment.datetime()
    assert dt.year == 2015
    assert dt.month == 4
    assert dt.day == 21
    assert dt.hour == 6


def test_nl_weekday_overlap():
    ref_date = datetime.datetime(2012, 8, 9)

    results = nl.parse("zondag, 7 december 2014", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "zondag, 7 december 2014"
    dt = results[0].moment.datetime()
    assert dt.year == 2014
    assert dt.month == 12
    assert dt.day == 7

    results = nl.parse("zondag 7/12/2014", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "zondag 7/12/2014"
    dt = results[0].moment.datetime()
    assert dt.year == 2014
    assert dt.month == 12
    assert dt.day == 7
