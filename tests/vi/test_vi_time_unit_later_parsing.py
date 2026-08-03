import datetime
from chrono_python.locales import vi


def test_vi_time_unit_later_days():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("Sự kiện 3 ngày sau.", ref_date)
    assert len(results) == 1
    assert results[0].index == 8
    assert results[0].text == "3 ngày sau"
    dt = results[0].moment.datetime()
    assert dt.month == 8
    assert dt.day == 13


def test_vi_time_unit_later_weeks():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("2 tuần nữa", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.month == 8
    assert dt.day == 24


def test_vi_time_unit_later_months():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("3 tháng tới", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.month == 11
    assert dt.year == 2012


def test_vi_time_unit_later_years():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("10 năm sau", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.year == 2022


def test_vi_time_unit_later_word_numbers():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("ba ngày sau", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.month == 8
    assert dt.day == 13

    results = vi.parse("hai tuần nữa", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.month == 8
    assert dt.day == 24
