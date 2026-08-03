import datetime
from chrono_python.locales import sv


def test_sv_month_name_single():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # den 15 augusti
    results = sv.parse("den 15 augusti", ref_date)
    assert len(results) == 1
    assert results[0].text == "den 15 augusti"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 15

    # 15 augusti 2012
    results = sv.parse("15 augusti 2012", ref_date)
    assert len(results) == 1
    assert results[0].text == "15 augusti 2012"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 15

    # 15 aug 2012
    results = sv.parse("15 aug 2012", ref_date)
    assert len(results) == 1
    assert results[0].text == "15 aug 2012"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 15


def test_sv_month_name_range():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # 15-16 augusti
    results = sv.parse("15-16 augusti", ref_date)
    assert len(results) == 1
    assert results[0].text == "15-16 augusti"
    start_dt = results[0].start.datetime()
    assert start_dt.year == 2012
    assert start_dt.month == 8
    assert start_dt.day == 15
    end_dt = results[0].end.datetime()
    assert end_dt.year == 2012
    assert end_dt.month == 8
    assert end_dt.day == 16

    # 15 till 16 augusti
    results = sv.parse("15 till 16 augusti", ref_date)
    assert len(results) == 1
    assert results[0].text == "15 till 16 augusti"
    start_dt = results[0].start.datetime()
    assert start_dt.year == 2012
    assert start_dt.month == 8
    assert start_dt.day == 15
    end_dt = results[0].end.datetime()
    assert end_dt.year == 2012
    assert end_dt.month == 8
    assert end_dt.day == 16


def test_sv_month_name_impossible():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    assert len(sv.parse("32 augusti", ref_date)) == 0
