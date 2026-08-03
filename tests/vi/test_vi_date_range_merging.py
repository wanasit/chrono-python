import datetime
from chrono_python.locales import vi


def test_vi_date_range_den():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("từ ngày 5 tháng 8 đến ngày 10 tháng 8 năm 2012", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.start.get("day") == 5
    assert result.start.get("month") == 8
    assert result.start.get("year") == 2012

    assert result.end is not None
    assert result.end.get("day") == 10
    assert result.end.get("month") == 8
    assert result.end.get("year") == 2012


def test_vi_date_range_em_dash():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("ngày 1 tháng 4 – ngày 30 tháng 4 năm 2000", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.start.get("day") == 1
    assert result.start.get("month") == 4

    assert result.end is not None
    assert result.end.get("day") == 30
    assert result.end.get("month") == 4
    assert result.end.get("year") == 2000


def test_vi_date_range_hyphen():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("ngày 3 tháng 9 - ngày 5 tháng 9 năm 1945", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.start.get("day") == 3
    assert result.start.get("month") == 9
    assert result.start.get("year") == 1945

    assert result.end is not None
    assert result.end.get("day") == 5
    assert result.end.get("month") == 9
    assert result.end.get("year") == 1945


def test_vi_date_range_toi():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("tháng 3 tới tháng 5 năm 1975", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.start.get("month") == 3

    assert result.end is not None
    assert result.end.get("month") == 5
    assert result.end.get("year") == 1975


def test_vi_date_range_order():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("ngày 1 tháng 1 đến ngày 31 tháng 12 năm 2020", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.end is not None
    assert result.start.datetime() < result.end.datetime()
