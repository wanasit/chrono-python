import datetime
from chrono_python.locales import fi


def test_fi_month_name_single():
    ref_date = datetime.datetime(2012, 8, 10)

    # 15. elokuuta
    results = fi.parse("15. elokuuta", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 15

    # 15 elokuuta 2012
    results = fi.parse("15 elokuuta 2012", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 15

    # 15. elo 2012
    results = fi.parse("15. elo 2012", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 15

    # 3 tammikuuta
    results = fi.parse("3 tammikuuta", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.year == 2013
    assert dt.month == 1
    assert dt.day == 3

    # 1 joulukuuta 2023
    ref_date_2023 = datetime.datetime(2023, 11, 1)
    results = fi.parse("1 joulukuuta 2023", ref_date_2023)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.year == 2023
    assert dt.month == 12
    assert dt.day == 1


def test_fi_month_name_range():
    ref_date = datetime.datetime(2012, 8, 10)

    results = fi.parse("15-16 elokuuta", ref_date)
    assert len(results) == 1
    start_dt = results[0].start.datetime()
    assert start_dt.year == 2012
    assert start_dt.month == 8
    assert start_dt.day == 15

    end_dt = results[0].end.datetime()
    assert end_dt.year == 2012
    assert end_dt.month == 8
    assert end_dt.day == 16


def test_fi_month_name_impossible_dates():
    ref_date = datetime.datetime(2012, 8, 10)

    results = fi.parse("32 elokuuta", ref_date)
    assert len(results) == 0
