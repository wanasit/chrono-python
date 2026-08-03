import datetime
from chrono_python.locales import vi


def test_vi_year_nam():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("Việt Nam thống nhất vào năm 1976.", ref_date)
    assert len(results) == 1
    assert results[0].text == "năm 1976"
    assert results[0].moment.get("year") == 1976

    results = vi.parse("Cách mạng năm 1789.", ref_date)
    assert len(results) == 1
    assert results[0].moment.get("year") == 1789


def test_vi_year_bc():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("Năm 179 TCN, triều Diệt bị diệt.", ref_date)
    assert len(results) == 1
    assert results[0].moment.get("year") == -179

    results = vi.parse("Văn minh có từ năm 3000 TCN.", ref_date)
    assert len(results) == 1
    assert results[0].moment.get("year") == -3000


def test_vi_year_3_digits():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("năm 938 là năm độc lập.", ref_date)
    assert len(results) == 1
    assert results[0].moment.get("year") == 938


def test_vi_year_with_month_day():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("ngày 2 tháng 9 năm 1945", ref_date)
    assert len(results) == 1
    assert results[0].moment.get("year") == 1945
    assert results[0].moment.is_certain("year") is True


def test_vi_year_negative_bare_number():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    assert len(vi.parse("Có 1975 người tham gia.", ref_date)) == 0
