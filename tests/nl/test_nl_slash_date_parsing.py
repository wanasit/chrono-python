import datetime
from chrono_python.locales import nl


def test_nl_slash_date_offset():
    ref_date = datetime.datetime(2012, 8, 10)
    results = nl.parse("    04/2016   ", ref_date)
    assert len(results) == 1
    assert results[0].index == 4
    assert results[0].text == "04/2016"


def test_nl_slash_date_single():
    ref_date = datetime.datetime(2012, 8, 10)

    results = nl.parse("Het evenement gaat door (04/2016)", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.index == 25
    assert result.text == "04/2016"
    dt = result.moment.datetime()
    assert dt.year == 2016
    assert dt.month == 4
    assert dt.day == 1

    results = nl.parse("Gepubliceerd: 06/2004", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.index == 14
    assert result.text == "06/2004"
    dt = result.moment.datetime()
    assert dt.year == 2004
    assert dt.month == 6
    assert dt.day == 1

    ref_date = datetime.datetime(2012, 10, 8)
    results = nl.parse("8/10/2012", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.index == 0
    assert result.text == "8/10/2012"
    dt = result.moment.datetime()
    assert dt.year == 2012
    assert dt.month == 10
    assert dt.day == 8

    ref_date = datetime.datetime(2012, 1, 8)
    results = nl.parse(": 8/1/2012", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.index == 2
    assert result.text == "8/1/2012"
    dt = result.moment.datetime()
    assert dt.year == 2012
    assert dt.month == 1
    assert dt.day == 8

    ref_date = datetime.datetime(2012, 10, 8)
    results = nl.parse("8/10", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.index == 0
    assert result.text == "8/10"
    dt = result.moment.datetime()
    assert dt.year == 2012
    assert dt.month == 10
    assert dt.day == 8

    results = nl.parse("De deadline is 8/10/2012", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.index == 15
    assert result.text == "8/10/2012"
    dt = result.moment.datetime()
    assert dt.year == 2012
    assert dt.month == 10
    assert dt.day == 8

    ref_date = datetime.datetime(2015, 11, 3)
    results = nl.parse("De deadline is dinsdag 11/3/2015", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.index == 15
    assert result.text == "dinsdag 11/3/2015"
    dt = result.moment.datetime()
    assert dt.year == 2015
    assert dt.month == 3
    assert dt.day == 11

    results = nl.parse("28/2/2014")
    assert len(results) == 1
    assert results[0].text == "28/2/2014"

    results = nl.parse("30-12-16")
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 12
    assert dt.day == 30

    results = nl.parse("vrijdag 30-12-16")
    assert len(results) == 1
    assert results[0].text == "vrijdag 30-12-16"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 12
    assert dt.day == 30


def test_nl_slash_date_range():
    ref_date = datetime.datetime(2012, 8, 10)
    results = nl.parse("10/8/2012 - 15/8/2012", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.index == 0
    assert result.text == "10/8/2012 - 15/8/2012"
    start_dt = result.moment.datetime()
    assert start_dt.year == 2012
    assert start_dt.month == 8
    assert start_dt.day == 10

    assert result.end is not None
    end_dt = result.end.datetime()
    assert end_dt.year == 2012
    assert end_dt.month == 8
    assert end_dt.day == 15


def test_nl_slash_date_splitters():
    expected_date = datetime.datetime(2015, 5, 25, 12, 0)
    for text in [
        "2015-05-25",
        "2015/05/25",
        "2015.05.25",
        "25-05-2015",
        "25/05/2015",
        "25.05.2015",
    ]:
        results = nl.parse(text)
        assert len(results) == 1
        dt = results[0].moment.datetime()
        assert dt.year == expected_date.year
        assert dt.month == expected_date.month
        assert dt.day == expected_date.day


def test_nl_slash_date_impossible():
    ref_date = datetime.datetime(2012, 8, 10)
    assert len(nl.parse("8/32/2014", ref_date)) == 0
    assert len(nl.parse("8/32", ref_date)) == 0
    assert len(nl.parse("2/29/2014", ref_date)) == 0
    assert len(nl.parse("2014/22/29", ref_date)) == 0
    assert len(nl.parse("2014/13/22", ref_date)) == 0
    assert len(nl.parse("80-32-89-89", ref_date)) == 0
