import datetime
from chrono_python.locales import vi


def test_vi_casual_relative_date_time():
    ref_date = datetime.datetime(2012, 8, 10, 6, 0)
    results = vi.parse("hôm qua lúc 7 giờ", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 9
    assert dt.hour == 7

    ref_noon = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("ngày mai lúc 15 giờ", ref_noon)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.day == 11
    assert dt.hour == 15

    results = vi.parse("hôm nay buổi sáng", ref_noon)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.day == 10
    assert dt.hour == 9


def test_vi_bare_time_unit_relative():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("tháng trước", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 7

    results = vi.parse("năm sau", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.year == 2013

    results = vi.parse("tuần trước", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 3

    results = vi.parse("2 tuần trước", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.month == 7
    assert dt.day == 27
