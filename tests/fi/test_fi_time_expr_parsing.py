import datetime
from chrono_python.locales import fi


def test_fi_time_expr():
    ref_date = datetime.datetime(2012, 8, 10)

    results = fi.parse("klo 15:00", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.hour == 15
    assert dt.minute == 0

    results = fi.parse("kello 8:30", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.hour == 8
    assert dt.minute == 30

    results = fi.parse("klo 13.00", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.hour == 13
    assert dt.minute == 0


def test_fi_time_range_expr():
    ref_date = datetime.datetime(2012, 8, 10)

    results = fi.parse("klo 10:00-12:00", ref_date)
    assert len(results) == 1
    start_dt = results[0].start.datetime()
    assert start_dt.hour == 10
    assert start_dt.minute == 0

    end_dt = results[0].end.datetime()
    assert end_dt.hour == 12
    assert end_dt.minute == 0


def test_fi_date_and_time_expr():
    ref_date = datetime.datetime(2012, 8, 10)

    results = fi.parse("15 elokuuta 2012 klo 14:00", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 15
    assert dt.hour == 14
    assert dt.minute == 0
