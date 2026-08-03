import datetime
from chrono_python.locales import nl


def test_nl_time_unit_ago_single():
    ref_date = datetime.datetime(2012, 8, 10, 12, 14)

    results = nl.parse("15 minuten eerder", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "15 minuten eerder"
    dt = results[0].moment.datetime()
    assert dt.hour == 11
    assert dt.minute == 59

    results = nl.parse("15 minuten voor", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "15 minuten voor"
    dt = results[0].moment.datetime()
    assert dt.hour == 11
    assert dt.minute == 59

    results = nl.parse("   12 uur geleden", ref_date)
    assert len(results) == 1
    assert results[0].index == 3
    assert results[0].text == "12 uur geleden"
    dt = results[0].moment.datetime()
    assert dt.hour == 0
    assert dt.minute == 14

    results = nl.parse("1u geleden", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "1u geleden"
    dt = results[0].moment.datetime()
    assert dt.hour == 11
    assert dt.minute == 14

    results = nl.parse("   half uur geleden", ref_date)
    assert len(results) == 1
    assert results[0].index == 3
    assert results[0].text == "half uur geleden"
    dt = results[0].moment.datetime()
    assert dt.hour == 11
    assert dt.minute == 44

    results = nl.parse("12 uur geleden deed ik iets", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "12 uur geleden"
    dt = results[0].moment.datetime()
    assert dt.hour == 0
    assert dt.minute == 14

    results = nl.parse("12 seconden geleden deed ik iets", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "12 seconden geleden"
    dt = results[0].moment.datetime()
    assert dt.hour == 12
    assert dt.minute == 13
    assert dt.second == 48

    results = nl.parse("drie seconden geleden deed ik iets", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "drie seconden geleden"
    dt = results[0].moment.datetime()
    assert dt.hour == 12
    assert dt.minute == 13
    assert dt.second == 57

    ref_date = datetime.datetime(2012, 8, 10)
    results = nl.parse("5 dagen geleden, hebben we iets gedaan", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "5 dagen geleden"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 5

    results = nl.parse("Een dag geleden, hebben we wat gedaan", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "Een dag geleden"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 9

    ref_date = datetime.datetime(2012, 8, 10, 12, 14)
    results = nl.parse("een minuut geleden", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "een minuut geleden"
    dt = results[0].moment.datetime()
    assert dt.hour == 12
    assert dt.minute == 13


def test_nl_time_unit_ago_casual():
    ref_date = datetime.datetime(2012, 10, 10)
    results = nl.parse("5 maanden geleden, hebben we iets gedaan", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "5 maanden geleden"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 5
    assert dt.day == 10

    ref_date = datetime.datetime(2012, 8, 10)
    results = nl.parse("5 jaar geleden,  hebben we iets gedaan", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "5 jaar geleden"
    dt = results[0].moment.datetime()
    assert dt.year == 2007
    assert dt.month == 8
    assert dt.day == 10

    ref_date = datetime.datetime(2012, 8, 3)
    results = nl.parse("een week geleden, hebben we iets gedaan", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "een week geleden"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 7
    assert dt.day == 27

    ref_date = datetime.datetime(2012, 8, 2)
    results = nl.parse("paar dagen geleden, hebben we iets gedaan", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "paar dagen geleden"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 7
    assert dt.day == 31


def test_nl_time_unit_ago_nested():
    ref_date = datetime.datetime(2012, 8, 10, 22, 30)

    results = nl.parse("15 uur 29 minuten geleden", ref_date)
    assert len(results) == 1
    assert results[0].text == "15 uur 29 minuten geleden"
    dt = results[0].moment.datetime()
    assert dt.day == 10
    assert dt.hour == 7
    assert dt.minute == 1

    results = nl.parse("1 dag 21 uur geleden ", ref_date)
    assert len(results) == 1
    assert results[0].text == "1 dag 21 uur geleden"
    dt = results[0].moment.datetime()
    assert dt.day == 9
    assert dt.hour == 1
    assert dt.minute == 30

    results = nl.parse("3 min 49 sec geleden ", ref_date)
    assert len(results) == 1
    assert results[0].text == "3 min 49 sec geleden"
    dt = results[0].moment.datetime()
    assert dt.day == 10
    assert dt.hour == 22
    assert dt.minute == 26
    assert dt.second == 11


def test_nl_time_unit_ago_negative():
    assert len(nl.strict.parse("15 uur 29 min")) == 0
    assert len(nl.strict.parse("een paar uur")) == 0
    assert len(nl.strict.parse("5 dagen")) == 0
