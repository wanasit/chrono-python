import datetime
from chrono_python.locales import vi


def test_vi_standard_full():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("Ngày 30 tháng 4 năm 1975 là ngày giải phóng.", ref_date)
    assert len(results) == 1
    moment = results[0].moment
    assert moment.get("year") == 1975
    assert moment.get("month") == 4
    assert moment.get("day") == 30
    assert moment.is_certain("year") is True
    assert moment.is_certain("month") is True
    assert moment.is_certain("day") is True

    results = vi.parse("Hiệp định được ký ngày 27 tháng 1 năm 1973.", ref_date)
    assert len(results) == 1
    assert results[0].text == "ngày 27 tháng 1 năm 1973"
    assert results[0].moment.get("year") == 1973
    assert results[0].moment.get("month") == 1
    assert results[0].moment.get("day") == 27

    results = vi.parse("ngày 2 tháng 9 năm 1945", ref_date)
    assert len(results) == 1
    assert results[0].moment.get("year") == 1945
    assert results[0].moment.get("month") == 9
    assert results[0].moment.get("day") == 2


def test_vi_standard_no_ngay_prefix():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("7 tháng 5 năm 1954 là ngày chấm dứt trận Điện Biên Phủ.", ref_date)
    assert len(results) == 1
    assert results[0].moment.get("day") == 7
    assert results[0].moment.get("month") == 5
    assert results[0].moment.get("year") == 1954

    results = vi.parse("1 tháng 1 năm 1863", ref_date)
    assert len(results) == 1
    assert results[0].moment.get("day") == 1
    assert results[0].moment.get("month") == 1
    assert results[0].moment.get("year") == 1863


def test_vi_standard_no_year():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("ngày 15 tháng 3", ref_date)
    assert len(results) == 1
    moment = results[0].moment
    assert moment.get("day") == 15
    assert moment.get("month") == 3
    assert moment.is_certain("year") is False
    assert moment.is_certain("day") is True
    assert moment.is_certain("month") is True


def test_vi_standard_index():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("Sự kiện ngày 30 tháng 4 năm 1975 quan trọng.", ref_date)
    assert len(results) == 1
    assert results[0].index == 8
    assert results[0].text == "ngày 30 tháng 4 năm 1975"
    assert results[0].moment.get("year") == 1975


def test_vi_standard_invalid_month():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    assert len(vi.parse("ngày 1 tháng 13", ref_date)) == 0
