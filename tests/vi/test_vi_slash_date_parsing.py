import datetime
from chrono_python.locales import vi


def test_vi_slash_date_little_endian():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("Ngày 30/04/1975.", ref_date)
    assert len(results) == 1
    assert results[0].index == 5
    assert results[0].moment.get("day") == 30
    assert results[0].moment.get("month") == 4
    assert results[0].moment.get("year") == 1975

    results = vi.parse("Hội nghị 01/01/1954", ref_date)
    assert len(results) == 1
    assert results[0].index == 9
    assert results[0].moment.get("day") == 1
    assert results[0].moment.get("month") == 1
    assert results[0].moment.get("year") == 1954


def test_vi_slash_date_unpadded():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("3/5/1968", ref_date)
    assert len(results) == 1
    assert results[0].moment.get("day") == 3
    assert results[0].moment.get("month") == 5
    assert results[0].moment.get("year") == 1968


def test_vi_slash_date_iso():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = vi.parse("Ngày 2024-03-15 là quan trọng.", ref_date)
    assert len(results) == 1
    assert results[0].moment.get("year") == 2024
    assert results[0].moment.get("month") == 3
    assert results[0].moment.get("day") == 15
