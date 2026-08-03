import datetime
from chrono_python.locales import fi


def test_fi_time_unit_ago_single():
    ref_date = datetime.datetime(2012, 8, 10)

    results = fi.parse("5 päivää sitten tehtiin jotain", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "5 päivää sitten"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 5

    ref_date = datetime.datetime(2012, 7, 10, 13, 30)
    results = fi.parse("10 päivää sitten tehtiin jotain", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "10 päivää sitten"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 6
    assert dt.day == 30
    assert dt.hour == 13
    assert dt.minute == 30

    ref_date = datetime.datetime(2012, 7, 10, 12, 14)
    results = fi.parse("15 minuuttia sitten", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "15 minuuttia sitten"
    dt = results[0].moment.datetime()
    assert dt.hour == 11
    assert dt.minute == 59

    results = fi.parse("   12 tuntia sitten", ref_date)
    assert len(results) == 1
    assert results[0].index == 3
    assert results[0].text == "12 tuntia sitten"
    dt = results[0].moment.datetime()
    assert dt.hour == 0
    assert dt.minute == 14

    results = fi.parse("12 tuntia sitten tapahtui jotain", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "12 tuntia sitten"
    dt = results[0].moment.datetime()
    assert dt.hour == 0
    assert dt.minute == 14


def test_fi_time_unit_ago_casual():
    ref_date = datetime.datetime(2012, 10, 10)
    results = fi.parse("5 kuukautta sitten tehtiin jotain", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "5 kuukautta sitten"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 5
    assert dt.day == 10

    ref_date = datetime.datetime(2012, 8, 10, 22, 22)
    results = fi.parse("5 vuotta sitten tehtiin jotain", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "5 vuotta sitten"
    dt = results[0].moment.datetime()
    assert dt.year == 2007
    assert dt.month == 8
    assert dt.day == 10

    ref_date = datetime.datetime(2012, 8, 3, 8, 34)
    results = fi.parse("yksi viikkoa sitten tehtiin jotain", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "yksi viikkoa sitten"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 7
    assert dt.day == 27
