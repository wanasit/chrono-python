import datetime
from chrono_python.locales import vi
from chrono_python.common.types import Meridiem


def test_vi_time_expr_hours():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("Cuộc hẹn lúc 7 giờ.", ref_date)
    assert len(results) == 1
    assert results[0].index == 9
    assert results[0].text == "lúc 7 giờ"
    dt = results[0].moment.datetime()
    assert dt.hour == 7
    assert dt.minute == 0

    results = vi.parse("7 giờ sáng", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.hour == 7
    assert results[0].moment.get("meridiem") in (Meridiem.AM, Meridiem.AM.value)

    results = vi.parse("7 giờ tối", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.hour == 19


def test_vi_time_expr_hours_minutes():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("lúc 7 giờ 30 phút", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.hour == 7
    assert dt.minute == 30

    results = vi.parse("vào 15 giờ 45 phút", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.hour == 15
    assert dt.minute == 45


def test_vi_time_expr_colon():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("Hẹn lúc 15:30.", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.hour == 15
    assert dt.minute == 30


def test_vi_time_expr_date_and_time():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("ngày 30 tháng 4 năm 1975 lúc 11 giờ", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.day == 30
    assert dt.month == 4
    assert dt.year == 1975
    assert dt.hour == 11


def test_vi_time_expr_meridiem_keywords():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("9 giờ sáng", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.hour == 9
    assert results[0].moment.get("meridiem") in (Meridiem.AM, Meridiem.AM.value)

    results = vi.parse("3 giờ chiều", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.hour == 15

    results = vi.parse("10 giờ đêm", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.hour == 22


def test_vi_time_expr_trua_meridiem():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("1 giờ trưa", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.hour == 13
    assert results[0].moment.get("meridiem") in (Meridiem.PM, Meridiem.PM.value)

    results = vi.parse("11 giờ trưa", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.hour == 11
    assert results[0].moment.get("meridiem") in (Meridiem.AM, Meridiem.AM.value)

    results = vi.parse("12 giờ trưa", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.hour == 12
    assert results[0].moment.get("meridiem") in (Meridiem.PM, Meridiem.PM.value)


def test_vi_time_expr_midnight():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("12 giờ sáng", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.hour == 0
    assert results[0].moment.get("meridiem") in (Meridiem.AM, Meridiem.AM.value)


def test_vi_time_expr_certainty():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("lúc 7 giờ", ref_date)
    assert len(results) == 1
    assert results[0].moment.is_certain("hour") is True
    assert results[0].moment.is_certain("meridiem") is False

    results = vi.parse("7 giờ sáng", ref_date)
    assert len(results) == 1
    assert results[0].moment.is_certain("hour") is True
    assert results[0].moment.is_certain("meridiem") is True
