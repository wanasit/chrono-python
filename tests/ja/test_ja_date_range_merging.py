import datetime
import chrono_python as chrono
from chrono_python.types import ParsedResult, ParsedRangeResult, DateTimeMoment, DateTimePrecision
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent
from chrono_python.chrono import ParsingContext
from chrono_python.locales.ja.refiners import JPMergeDateRangeRefiner


def test_standard_jp_date_range():
    ref = datetime.datetime(2012, 8, 10, 12, 0)

    # 1. 2012年3月31日〜2012年4月1日 (with Wave Dash 〜)
    result = chrono.ja.parse("主な株主（2012年3月31日〜2012年4月1日現在）", ref)
    assert len(result) == 1
    assert result[0].text == "2012年3月31日〜2012年4月1日"
    assert isinstance(result[0], ParsedRangeResult)
    assert result[0].start.datetime() == datetime.datetime(2012, 3, 31, 12, 0)
    assert result[0].end.datetime() == datetime.datetime(2012, 4, 1, 12, 0)

    # 2. 2012年3月31日から2012年4月1日 (with から)
    result = chrono.ja.parse("主な株主（2012年3月31日から2012年4月1日現在）", ref)
    assert len(result) == 1
    assert result[0].text == "2012年3月31日から2012年4月1日"
    assert isinstance(result[0], ParsedRangeResult)
    assert result[0].start.datetime() == datetime.datetime(2012, 3, 31, 12, 0)
    assert result[0].end.datetime() == datetime.datetime(2012, 4, 1, 12, 0)


def test_jp_weekday_range_refiner_directly():
    ref = datetime.datetime(2020, 7, 1, 12, 0)  # July 1, 2020 is a Wednesday
    context = ParsingContext("水曜日から金曜日", DateTimeMoment.of(ref))
    refiner = JPMergeDateRangeRefiner()

    # 水曜日 (July 1) - 金曜日 (July 3) (no adjustment)
    wed_moment = ParsingCivilTimeMoment(
        reference=DateTimeMoment.of(ref),
        known_values={CivilTimeComponent.WEEKDAY: 3},
        implied_values={
            CivilTimeComponent.DAY: 1,
            CivilTimeComponent.MONTH: 7,
            CivilTimeComponent.YEAR: 2020,
        }
    )
    fri_moment = ParsingCivilTimeMoment(
        reference=DateTimeMoment.of(ref),
        known_values={CivilTimeComponent.WEEKDAY: 5},
        implied_values={
            CivilTimeComponent.DAY: 3,
            CivilTimeComponent.MONTH: 7,
            CivilTimeComponent.YEAR: 2020,
        }
    )
    results = [
        ParsedResult(index=0, text="水曜日", moment=wed_moment),
        ParsedResult(index=5, text="金曜日", moment=fri_moment)
    ]
    merged = refiner.refine(context, results)

    assert len(merged) == 1
    assert merged[0].text == "水曜日から金曜日"
    assert isinstance(merged[0], ParsedRangeResult)
    assert merged[0].start.datetime() == datetime.datetime(2020, 7, 1, 12, 0)
    assert merged[0].end.datetime() == datetime.datetime(2020, 7, 3, 12, 0)


def test_jp_weekday_range_forward_adjustment():
    ref = datetime.datetime(2020, 7, 1, 12, 0)  # Wednesday
    context = ParsingContext("金曜日から月曜日", DateTimeMoment.of(ref))
    refiner = JPMergeDateRangeRefiner()

    # 金曜日 (July 3) - 月曜日 (June 29)
    # Since July 3 > June 29, it should adjust Monday to July 6.
    fri_moment = ParsingCivilTimeMoment(
        reference=DateTimeMoment.of(ref),
        known_values={CivilTimeComponent.WEEKDAY: 5},
        implied_values={
            CivilTimeComponent.DAY: 3,
            CivilTimeComponent.MONTH: 7,
            CivilTimeComponent.YEAR: 2020,
        }
    )
    mon_moment = ParsingCivilTimeMoment(
        reference=DateTimeMoment.of(ref),
        known_values={CivilTimeComponent.WEEKDAY: 1},
        implied_values={
            CivilTimeComponent.DAY: 29,
            CivilTimeComponent.MONTH: 6,
            CivilTimeComponent.YEAR: 2020,
        }
    )
    results = [
        ParsedResult(index=0, text="金曜日", moment=fri_moment),
        ParsedResult(index=5, text="月曜日", moment=mon_moment)
    ]
    merged = refiner.refine(context, results)

    assert len(merged) == 1
    assert merged[0].text == "金曜日から月曜日"
    assert isinstance(merged[0], ParsedRangeResult)
    assert merged[0].start.datetime() == datetime.datetime(2020, 7, 3, 12, 0)
    assert merged[0].end.datetime() == datetime.datetime(2020, 7, 6, 12, 0)


def test_jp_unknown_year_adjustment():
    ref = datetime.datetime(2020, 7, 1, 12, 0)
    # 12月30日 parses to Dec 30, 2020.
    # 1月5日 parses to Jan 5, 2020.
    # Since Dec 30 > Jan 5, and Jan 5 has unknown year, it adjusts to Jan 5, 2021.
    result = chrono.ja.parse("12月30日〜1月5日", reference=ref)

    assert len(result) == 1
    assert result[0].text == "12月30日〜1月5日"
    assert isinstance(result[0], ParsedRangeResult)
    assert result[0].start.datetime() == datetime.datetime(2020, 12, 30, 12, 0)
    assert result[0].end.datetime() == datetime.datetime(2021, 1, 5, 12, 0)


def test_ja_casual_time_range_merging():
    ref_date = datetime.datetime(2012, 8, 4, 12, 0)

    # 今日の朝から明日
    results = chrono.ja.parse("今日の朝から明日", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "今日の朝から明日"
    assert isinstance(result, ParsedRangeResult)
    assert result.start.get(CivilTimeComponent.MONTH) == 8
    assert result.start.get(CivilTimeComponent.DAY) == 4
    assert result.start.get(CivilTimeComponent.HOUR) == 6
    assert not result.start.is_certain(CivilTimeComponent.HOUR)
    assert result.start.precision() == DateTimePrecision.DAY

    assert result.end.get(CivilTimeComponent.MONTH) == 8
    assert result.end.get(CivilTimeComponent.DAY) == 5
    assert result.end.get(CivilTimeComponent.HOUR) == 12
    assert not result.end.is_certain(CivilTimeComponent.HOUR)
    assert result.end.precision() == DateTimePrecision.DAY

    # 今日から明日の夕方
    results = chrono.ja.parse("今日から明日の夕方", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "今日から明日の夕方"
    assert isinstance(result, ParsedRangeResult)
    assert result.start.get(CivilTimeComponent.MONTH) == 8
    assert result.start.get(CivilTimeComponent.DAY) == 4
    assert result.start.get(CivilTimeComponent.HOUR) == 12
    assert not result.start.is_certain(CivilTimeComponent.HOUR)
    assert result.start.precision() == DateTimePrecision.DAY

    assert result.end.get(CivilTimeComponent.MONTH) == 8
    assert result.end.get(CivilTimeComponent.DAY) == 5
    assert result.end.get(CivilTimeComponent.HOUR) == 18
    assert not result.end.is_certain(CivilTimeComponent.HOUR)
    assert result.end.precision() == DateTimePrecision.DAY
