import datetime
from chrono_python.locales import vi


def test_vi_time_unit_within_days():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("trong 3 ngày", ref_date)
    assert len(results) == 1
    assert results[0].text == "trong 3 ngày"
    dt = results[0].moment.datetime()
    assert dt.month == 8
    assert dt.day == 13


def test_vi_time_unit_within_weeks():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("Hoàn thành trong 2 tuần.", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.month == 8
    assert dt.day == 24


def test_vi_time_unit_within_months():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("trong vòng 3 tháng", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.month == 11
    assert dt.year == 2012
