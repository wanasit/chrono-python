import datetime
from chrono_python.locales import vi


def test_vi_month_year():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("tháng 4 năm 1975", ref_date)
    assert len(results) == 1
    assert results[0].text == "tháng 4 năm 1975"
    moment = results[0].moment
    assert moment.get("month") == 4
    assert moment.get("year") == 1975
    assert moment.is_certain("month") is True
    assert moment.is_certain("year") is True
    assert moment.is_certain("day") is False

    results = vi.parse("tháng 1 năm 1863", ref_date)
    assert len(results) == 1
    assert results[0].moment.get("month") == 1
    assert results[0].moment.get("year") == 1863


def test_vi_month_slash_year():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("tháng 3/1975", ref_date)
    assert len(results) == 1
    assert results[0].moment.get("month") == 3
    assert results[0].moment.get("year") == 1975


def test_vi_month_only():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("tháng 3", ref_date)
    assert len(results) == 1
    moment = results[0].moment
    assert moment.get("month") == 3
    assert moment.is_certain("year") is False
    assert moment.get("year") == 2012


def test_vi_month_invalid():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    assert len(vi.parse("tháng 13", ref_date)) == 0
    assert len(vi.parse("tháng 0", ref_date)) == 0
