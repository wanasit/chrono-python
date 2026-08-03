import datetime
from chrono_python.locales import vi


def test_vi_strict_rejects_casual_dates():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    assert len(vi.strict.parse("hôm nay", ref_date)) == 0
    assert len(vi.strict.parse("hôm qua", ref_date)) == 0
    assert len(vi.strict.parse("ngày mai", ref_date)) == 0
    assert len(vi.strict.parse("ngày kia", ref_date)) == 0


def test_vi_strict_rejects_casual_times():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    assert len(vi.strict.parse("buổi sáng", ref_date)) == 0
    assert len(vi.strict.parse("buổi trưa", ref_date)) == 0
    assert len(vi.strict.parse("buổi chiều", ref_date)) == 0
    assert len(vi.strict.parse("buổi tối", ref_date)) == 0


def test_vi_strict_rejects_casual_relatives():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    assert len(vi.strict.parse("tuần này", ref_date)) == 0
    assert len(vi.strict.parse("tháng trước", ref_date)) == 0
    assert len(vi.strict.parse("năm sau", ref_date)) == 0


def test_vi_strict_rejects_weekday_only():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    assert len(vi.strict.parse("thứ hai", ref_date)) == 0
    assert len(vi.strict.parse("chủ nhật", ref_date)) == 0


def test_vi_strict_accepts_standard_dates_and_times():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.strict.parse("ngày 30 tháng 4 năm 1975", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.year == 1975
    assert dt.month == 4
    assert dt.day == 30

    results = vi.strict.parse("lúc 7 giờ 30 phút", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.hour == 7
    assert dt.minute == 30


def test_vi_strict_accepts_slash_dates():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.strict.parse("30/4/1975", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.day == 30
    assert dt.month == 4
    assert dt.year == 1975

    results = vi.strict.parse("15/3", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.day == 15
    assert dt.month == 3


def test_vi_strict_accepts_explicit_time_units():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.strict.parse("3 ngày trước", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.day == 7
    assert dt.month == 8

    results = vi.strict.parse("2 tuần sau", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.day == 24
    assert dt.month == 8
