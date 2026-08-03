import datetime
from chrono_python.locales import vi
from chrono_python.common.types import Meridiem


def test_vi_casual_time_morning():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("7 giờ sáng", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.hour == 7
    assert results[0].moment.get("meridiem") in (Meridiem.AM, Meridiem.AM.value)

    results = vi.parse("hôm nay buổi sáng", datetime.datetime(2012, 8, 10, 6, 0))
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.hour == 9
    assert results[0].moment.get("meridiem") in (Meridiem.AM, Meridiem.AM.value)


def test_vi_casual_time_noon():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("buổi trưa", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.hour == 12
    assert results[0].moment.get("meridiem") in (Meridiem.PM, Meridiem.PM.value)


def test_vi_casual_time_afternoon():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("buổi chiều", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.hour == 15
    assert results[0].moment.get("meridiem") in (Meridiem.PM, Meridiem.PM.value)


def test_vi_casual_time_evening():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("buổi tối", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.hour == 19
    assert results[0].moment.get("meridiem") in (Meridiem.PM, Meridiem.PM.value)


def test_vi_casual_time_night():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("buổi đêm", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.hour == 22
    assert results[0].moment.get("meridiem") in (Meridiem.PM, Meridiem.PM.value)

    results = vi.parse("đêm", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.hour == 22
    assert results[0].moment.get("meridiem") in (Meridiem.PM, Meridiem.PM.value)


def test_vi_casual_time_midnight():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("nửa đêm", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.hour == 0
    assert results[0].moment.get("meridiem") in (Meridiem.AM, Meridiem.AM.value)


def test_vi_casual_time_dawn():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("bình minh", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.hour == 6
    assert results[0].moment.get("meridiem") in (Meridiem.AM, Meridiem.AM.value)

    results = vi.parse("sáng sớm", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.hour == 6
    assert results[0].moment.get("meridiem") in (Meridiem.AM, Meridiem.AM.value)


def test_vi_casual_time_merge_with_date():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("hôm nay buổi chiều", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.day == 10
    assert dt.hour == 15
