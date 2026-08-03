import datetime
from chrono_python.locales import nl


def test_nl_month_name_parsing_range():
    ref_date = datetime.datetime(2012, 8, 10)

    results = nl.parse("10 tot 22 augustus 2012", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.index == 0
    assert result.text == "10 tot 22 augustus 2012"
    start_dt = result.moment.datetime()
    assert start_dt.year == 2012
    assert start_dt.month == 8
    assert start_dt.day == 10

    assert result.end is not None
    end_dt = result.end.datetime()
    assert end_dt.year == 2012
    assert end_dt.month == 8
    assert end_dt.day == 22

    results = nl.parse("10 augustus - 12 september", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.index == 0
    assert result.text == "10 augustus - 12 september"
    start_dt = result.moment.datetime()
    assert start_dt.year == 2012
    assert start_dt.month == 8
    assert start_dt.day == 10

    assert result.end is not None
    end_dt = result.end.datetime()
    assert end_dt.year == 2012
    assert end_dt.month == 9
    assert end_dt.day == 12

    results = nl.parse("10 augustus - 12 september 2013", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.index == 0
    assert result.text == "10 augustus - 12 september 2013"
    start_dt = result.moment.datetime()
    assert start_dt.year == 2013
    assert start_dt.month == 8
    assert start_dt.day == 10

    assert result.end is not None
    end_dt = result.end.datetime()
    assert end_dt.year == 2013
    assert end_dt.month == 9
    assert end_dt.day == 12


def test_nl_month_name_parsing_combined():
    ref_date = datetime.datetime(2012, 8, 10)

    results = nl.parse("12de juli om 19:00", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "12de juli om 19:00"
    start_dt = result.moment.datetime()
    assert start_dt.year == 2012
    assert start_dt.month == 7
    assert start_dt.day == 12
    assert start_dt.hour == 19

    results = nl.parse("5 mei 12:00", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "5 mei 12:00"
    start_dt = result.moment.datetime()
    assert start_dt.year == 2012
    assert start_dt.month == 5
    assert start_dt.day == 5
    assert start_dt.hour == 12

    results = nl.parse("7 mei 11:00", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "7 mei 11:00"
    start_dt = result.moment.datetime()
    assert start_dt.year == 2012
    assert start_dt.month == 5
    assert start_dt.day == 7
    assert start_dt.hour == 11


def test_nl_month_name_parsing_ordinals():
    ref_date = datetime.datetime(2012, 8, 10)

    results = nl.parse("vierentwintigste mei", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "vierentwintigste mei"
    start_dt = result.moment.datetime()
    assert start_dt.year == 2012
    assert start_dt.month == 5
    assert start_dt.day == 24

    results = nl.parse("achtste tot elfde mei 2010", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "achtste tot elfde mei 2010"
    start_dt = result.moment.datetime()
    assert start_dt.year == 2010
    assert start_dt.month == 5
    assert start_dt.day == 8

    assert result.end is not None
    end_dt = result.end.datetime()
    assert end_dt.year == 2010
    assert end_dt.month == 5
    assert end_dt.day == 11


def test_nl_month_name_parsing_with_time():
    ref_date = datetime.datetime(2017, 7, 7, 15, 0)

    results = nl.parse("24ste oktober, 9:00", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "24ste oktober, 9:00"
    start_dt = result.moment.datetime()
    assert start_dt.day == 24
    assert start_dt.month == 10
    assert start_dt.hour == 9

    results = nl.parse("24ste oktober, 21:00", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "24ste oktober, 21:00"
    start_dt = result.moment.datetime()
    assert start_dt.day == 24
    assert start_dt.month == 10
    assert start_dt.hour == 21

    results = nl.parse("24 oktober, 21:00", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "24 oktober, 21:00"
    start_dt = result.moment.datetime()
    assert start_dt.day == 24
    assert start_dt.month == 10
    assert start_dt.hour == 21


def test_nl_month_name_parsing_90s_year():
    ref_date = datetime.datetime(2012, 8, 10)

    results = nl.parse("03 aug 96", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "03 aug 96"
    start_dt = result.moment.datetime()
    assert start_dt.year == 1996
    assert start_dt.month == 8
    assert start_dt.day == 3

    results = nl.parse("3 aug 96", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "3 aug 96"
    start_dt = result.moment.datetime()
    assert start_dt.year == 1996
    assert start_dt.month == 8
    assert start_dt.day == 3

    results = nl.parse("9 aug 96", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "9 aug 96"
    start_dt = result.moment.datetime()
    assert start_dt.year == 1996
    assert start_dt.month == 8
    assert start_dt.day == 9
