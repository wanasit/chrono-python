import datetime
import chrono_python as chrono
from chrono_python.types import DateTimePrecision
from chrono_python.common.types import CivilTimeComponent, Meridiem

def test_casual_date_expressions():
    ref_date = datetime.datetime(2012, 8, 9, 12, 0) # Thursday Aug 9, 2012

    # 今日 (today)
    for word in ("今日", "きょう", "本日", "ほんじつ"):
        results = chrono.ja.parse(word, ref_date)
        assert len(results) == 1
        assert results[0].text == word
        assert results[0].moment.datetime() == datetime.datetime(2012, 8, 9, 12, 0)
        assert results[0].moment.precision() == DateTimePrecision.DAY
        assert results[0].moment.is_certain(CivilTimeComponent.DAY)
        assert results[0].moment.is_certain(CivilTimeComponent.MONTH)
        assert results[0].moment.is_certain(CivilTimeComponent.YEAR)
        assert not results[0].moment.is_certain(CivilTimeComponent.HOUR)

    # 昨日 (yesterday)
    for word in ("昨日", "きのう"):
        results = chrono.ja.parse(word, ref_date)
        assert len(results) == 1
        assert results[0].text == word
        assert results[0].moment.datetime() == datetime.datetime(2012, 8, 8, 12, 0)
        assert results[0].moment.precision() == DateTimePrecision.DAY

    # 明日 (tomorrow)
    for word in ("明日", "あした"):
        results = chrono.ja.parse(word, ref_date)
        assert len(results) == 1
        assert results[0].text == word
        assert results[0].moment.datetime() == datetime.datetime(2012, 8, 10, 12, 0)
        assert results[0].moment.precision() == DateTimePrecision.DAY

    # 今夜 (tonight)
    for word in ("今夜", "こんや", "今夕", "こんゆう", "今晩", "こんばん"):
        results = chrono.ja.parse(word, ref_date)
        assert len(results) == 1
        assert results[0].text == word
        assert results[0].moment.datetime() == datetime.datetime(2012, 8, 9, 22, 0)
        assert results[0].moment.precision() == DateTimePrecision.DAY
        assert results[0].moment.get(CivilTimeComponent.MERIDIEM) == Meridiem.PM
        assert not results[0].moment.is_certain(CivilTimeComponent.HOUR)

    # 今朝 (morning)
    for word in ("今朝", "けさ"):
        results = chrono.ja.parse(word, ref_date)
        assert len(results) == 1
        assert results[0].text == word
        assert results[0].moment.datetime() == datetime.datetime(2012, 8, 9, 6, 0)
        assert results[0].moment.precision() == DateTimePrecision.DAY
        assert results[0].moment.get(CivilTimeComponent.MERIDIEM) == Meridiem.AM
        assert not results[0].moment.is_certain(CivilTimeComponent.HOUR)


def test_strict_vs_casual():
    ref_date = datetime.datetime(2012, 8, 9, 12, 0)

    # Casual configuration should parse "今日"
    assert len(chrono.ja.casual.parse('今日', ref_date)) == 1

    # Strict configuration should NOT parse "今日"
    assert len(chrono.ja.strict.parse('今日', ref_date)) == 0
