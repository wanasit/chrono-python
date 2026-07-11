import datetime
import chrono_python as chrono
from chrono_python.common.types import CivilTimeComponent


def test_ja_unlikely_format_filter_ichiji():
    ref_date = datetime.datetime(2020, 1, 1, 12, 0)

    # Standalone "一時" is likely 1 o'clock
    results = chrono.ja.parse("一時", ref_date)
    assert len(results) == 1
    assert results[0].text == "一時"
    assert results[0].moment.get(CivilTimeComponent.HOUR) == 1

    # "一時頃" should be valid
    results = chrono.ja.parse("一時頃", ref_date)
    assert len(results) == 1
    assert results[0].text == "一時" or "一時頃" in results[0].text
    assert results[0].moment.get(CivilTimeComponent.HOUR) == 1

    # "一時的" (temporary) should not be parsed
    results = chrono.ja.parse("一時的", ref_date)
    assert len(results) == 0

    # "一時停止" (temporary stop) should not be parsed
    results = chrono.ja.parse("一時停止", ref_date)
    assert len(results) == 0

    # "一時保存" (temporary save) should not be parsed
    results = chrono.ja.parse("一時保存", ref_date)
    assert len(results) == 0

    # "一時しのぎ" should not be parsed
    results = chrono.ja.parse("一時しのぎ", ref_date)
    assert len(results) == 0

    # "一時預かり" should not be parsed
    results = chrono.ja.parse("一時預かり", ref_date)
    assert len(results) == 0

    # "一時払い" should not be parsed
    results = chrono.ja.parse("一時払い", ref_date)
    assert len(results) == 0
