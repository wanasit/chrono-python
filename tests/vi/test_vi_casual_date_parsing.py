import datetime
from chrono_python.locales import vi


def test_vi_casual_date_today():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("Cuộc hẹn hôm nay.", ref_date)
    assert len(results) == 1
    assert results[0].index == 9
    assert results[0].text == "hôm nay"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10


def test_vi_casual_date_yesterday():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("Hội nghị hôm qua.", ref_date)
    assert len(results) == 1
    assert results[0].index == 9
    assert results[0].text == "hôm qua"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 9

    ref_date_boundary = datetime.datetime(2012, 8, 1, 12, 0)
    results = vi.parse("hôm qua", ref_date_boundary)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.month == 7
    assert dt.day == 31


def test_vi_casual_date_tomorrow():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("Lịch ngày mai.", ref_date)
    assert len(results) == 1
    assert results[0].index == 5
    assert results[0].text == "ngày mai"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 11

    ref_date_boundary = datetime.datetime(2012, 8, 31, 12, 0)
    results = vi.parse("ngày mai", ref_date_boundary)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.month == 9
    assert dt.day == 1


def test_vi_casual_date_day_after_tomorrow():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("ngày kia", ref_date)
    assert len(results) == 1
    assert results[0].text == "ngày kia"
    dt = results[0].moment.datetime()
    assert dt.day == 12


def test_vi_casual_date_now():
    ref_date = datetime.datetime(2012, 8, 10, 8, 9, 10, 11)
    results = vi.parse("bây giờ", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10
    assert dt.hour == 8
    assert dt.minute == 9
    assert dt.second == 10

    results = vi.parse("lúc này", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.hour == 8


def test_vi_casual_date_day_before_yesterday():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("hôm kia", ref_date)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 8


def test_vi_casual_date_certainty():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("hôm nay", ref_date)
    assert len(results) == 1
    moment = results[0].moment
    assert moment.is_certain("day") is True
    assert moment.is_certain("month") is True
    assert moment.is_certain("year") is True
    assert moment.is_certain("hour") is False
