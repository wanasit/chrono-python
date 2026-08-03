import datetime
from chrono_python.locales import vi


def test_vi_weekday_full_names():
    ref_date = datetime.datetime(2012, 8, 9, 12, 0)  # Thursday
    results = vi.parse("Hẹn vào thứ hai", ref_date)
    assert len(results) == 1
    assert results[0].index == 8
    assert results[0].moment.get("weekday") == 1

    assert vi.parse("thứ ba", ref_date)[0].moment.get("weekday") == 2
    assert vi.parse("thứ tư", ref_date)[0].moment.get("weekday") == 3
    assert vi.parse("thứ năm", ref_date)[0].moment.get("weekday") == 4
    assert vi.parse("thứ sáu", ref_date)[0].moment.get("weekday") == 5
    assert vi.parse("thứ bảy", ref_date)[0].moment.get("weekday") == 6
    assert vi.parse("chủ nhật", ref_date)[0].moment.get("weekday") == 0


def test_vi_weekday_abbreviations():
    ref_date = datetime.datetime(2012, 8, 9, 12, 0)
    results = vi.parse("Hẹn t2", ref_date)
    assert len(results) == 1
    assert results[0].index == 4
    assert results[0].moment.get("weekday") == 1

    assert vi.parse("t7", ref_date)[0].moment.get("weekday") == 6
    assert vi.parse("cn", ref_date)[0].moment.get("weekday") == 0


def test_vi_weekday_implies_date():
    ref_date = datetime.datetime(2012, 8, 9, 12, 0)
    results = vi.parse("thứ hai tới", ref_date)
    assert len(results) == 1
    assert results[0].moment.get("weekday") == 1
    assert results[0].moment.is_certain("day") is False


def test_vi_weekday_next():
    ref_date = datetime.datetime(2012, 8, 9, 12, 0)  # Thu Aug 9
    results = vi.parse("thứ hai tới", ref_date)
    assert len(results) == 1
    assert results[0].moment.get("weekday") == 1
    assert results[0].moment.get("day") == 13

    results = vi.parse("thứ hai sau", ref_date)
    assert len(results) == 1
    assert results[0].moment.get("weekday") == 1
    assert results[0].moment.get("day") == 13


def test_vi_weekday_last():
    ref_date = datetime.datetime(2012, 8, 9, 12, 0)  # Thu Aug 9
    results = vi.parse("thứ hai qua", ref_date)
    assert len(results) == 1
    assert results[0].moment.get("weekday") == 1
    assert results[0].moment.get("day") == 6


def test_vi_weekday_sau_khi_conjunction():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("thứ hai sau khi chiến tranh kết thúc", ref_date)
    assert len(results) == 1
    assert results[0].text == "thứ hai"
