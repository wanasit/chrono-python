import datetime
from chrono_python.locales import vi


def test_vi_time_unit_ago_days():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("Sự kiện 3 ngày trước.", ref_date)
    assert len(results) == 1
    assert results[0].index == 8
    assert results[0].text == "3 ngày trước"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 7


def test_vi_time_unit_ago_weeks():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("2 tuần trước", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.month == 7
    assert dt.day == 27


def test_vi_time_unit_ago_months():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("3 tháng trước", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.month == 5
    assert dt.year == 2012


def test_vi_time_unit_ago_years():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("5 năm trước", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.year == 2007


def test_vi_time_unit_ago_qua_variant():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("1 tháng qua", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.month == 7
    assert dt.year == 2012


def test_vi_time_unit_ago_word_numbers():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("hai tuần trước", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.month == 7
    assert dt.day == 27

    results = vi.parse("ba ngày trước", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.month == 8
    assert dt.day == 7

    results = vi.parse("một tháng qua", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.month == 7
    assert dt.year == 2012
