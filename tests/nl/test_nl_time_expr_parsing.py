import datetime
from chrono_python.locales import nl


def test_nl_time_expr_offset():
    ref_date = datetime.datetime(2016, 10, 1, 8, 0)

    results = nl.parse("  11:00 ", ref_date)
    assert len(results) == 1
    assert results[0].index == 2
    assert results[0].text == "11:00"

    results = nl.parse("2020 om  11:00 ", ref_date)
    assert len(results) == 1
    assert results[0].index == 5
    assert results[0].text == "om  11:00"


def test_nl_time_expr_single():
    ref_date = datetime.datetime(2016, 10, 1, 8, 0)
    results = nl.parse("20:32:13", ref_date)
    assert len(results) == 1
    assert results[0].text == "20:32:13"
    dt = results[0].moment.datetime()
    assert dt.hour == 20
    assert dt.minute == 32
    assert dt.second == 13


def test_nl_time_expr_range():
    ref_date = datetime.datetime(2016, 10, 1, 8, 0)
    results = nl.parse("10:00:00 - 21:45:00", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "10:00:00 - 21:45:00"
    start_dt = result.moment.datetime()
    assert start_dt.hour == 10
    assert start_dt.minute == 0
    assert start_dt.second == 0

    assert result.end is not None
    end_dt = result.end.datetime()
    assert end_dt.hour == 21
    assert end_dt.minute == 45
    assert end_dt.second == 0


def test_nl_time_expr_casual():
    ref_date = datetime.datetime(2016, 10, 1, 8, 0)

    results = nl.parse("23:00 's avonds", ref_date)
    assert len(results) == 1
    assert results[0].text == "23:00 's avonds"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 10
    assert dt.day == 1
    assert dt.hour == 23

    results = nl.parse("23:00 vanavond", ref_date)
    assert len(results) == 1
    assert results[0].text == "23:00 vanavond"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 10
    assert dt.day == 1
    assert dt.hour == 23

    results = nl.parse("6:00 's ochtends", ref_date)
    assert len(results) == 1
    assert results[0].text == "6:00 's ochtends"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 10
    assert dt.day == 1
    assert dt.hour == 6
    assert dt.minute == 0

    results = nl.parse("6:00 in de namiddag", ref_date)
    assert len(results) == 1
    assert results[0].text == "6:00 in de namiddag"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 10
    assert dt.day == 1
    assert dt.hour == 18
    assert dt.minute == 0
