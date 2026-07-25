import datetime
import chrono_python as chrono
from chrono_python.types import ParsedResult, ParsedRangeResult, DateTimeMoment, DateTimePrecision
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent
from chrono_python.chrono import ParsingContext
from chrono_python.locales.en.refiners import ENMergeDateRangeRefiner


def test_standard_date_range():
    ref = datetime.datetime(2020, 7, 1, 12, 0)
    result = chrono.en.parse("2020-02-13 to 2020-02-15", reference=ref)

    assert len(result) == 1
    assert result[0].text == "2020-02-13 to 2020-02-15"
    assert isinstance(result[0], ParsedRangeResult)
    assert result[0].start.datetime() == datetime.datetime(2020, 2, 13, 12, 0)
    assert result[0].end.datetime() == datetime.datetime(2020, 2, 15, 12, 0)


def test_weekday_range_refiner_directly():
    ref = datetime.datetime(2020, 7, 1, 12, 0)  # July 1, 2020 is a Wednesday
    context = ParsingContext("Wednesday - Friday", DateTimeMoment.of(ref))
    refiner = ENMergeDateRangeRefiner()

    # Wednesday (July 1) - Friday (July 3) (no adjustment)
    wed_moment = ParsingCivilTimeMoment(
        known_values={CivilTimeComponent.WEEKDAY: 3},
        implied_values={
            CivilTimeComponent.DAY: 1,
            CivilTimeComponent.MONTH: 7,
            CivilTimeComponent.YEAR: 2020,
        }
    )
    fri_moment = ParsingCivilTimeMoment(
        known_values={CivilTimeComponent.WEEKDAY: 5},
        implied_values={
            CivilTimeComponent.DAY: 3,
            CivilTimeComponent.MONTH: 7,
            CivilTimeComponent.YEAR: 2020,
        }
    )
    results = [
        ParsedResult(index=0, text="Wednesday", moment=wed_moment),
        ParsedResult(index=12, text="Friday", moment=fri_moment)
    ]
    merged = refiner.refine(context, results)

    assert len(merged) == 1
    assert merged[0].text == "Wednesday - Friday"
    assert isinstance(merged[0], ParsedRangeResult)
    assert merged[0].start.datetime() == datetime.datetime(2020, 7, 1, 12, 0)
    assert merged[0].end.datetime() == datetime.datetime(2020, 7, 3, 12, 0)


def test_weekday_range_forward_adjustment():
    ref = datetime.datetime(2020, 7, 1, 12, 0)  # Wednesday
    context = ParsingContext("Friday - Monday", DateTimeMoment.of(ref))
    refiner = ENMergeDateRangeRefiner()

    # Friday (July 3) - Monday (June 29)
    # Since July 3 > June 29, it should adjust Monday to July 6.
    fri_moment = ParsingCivilTimeMoment(
        known_values={CivilTimeComponent.WEEKDAY: 5},
        implied_values={
            CivilTimeComponent.DAY: 3,
            CivilTimeComponent.MONTH: 7,
            CivilTimeComponent.YEAR: 2020,
        }
    )
    mon_moment = ParsingCivilTimeMoment(
        known_values={CivilTimeComponent.WEEKDAY: 1},
        implied_values={
            CivilTimeComponent.DAY: 29,
            CivilTimeComponent.MONTH: 6,
            CivilTimeComponent.YEAR: 2020,
        }
    )
    results = [
        ParsedResult(index=0, text="Friday", moment=fri_moment),
        ParsedResult(index=9, text="Monday", moment=mon_moment)
    ]
    merged = refiner.refine(context, results)

    assert len(merged) == 1
    assert merged[0].text == "Friday - Monday"
    assert isinstance(merged[0], ParsedRangeResult)
    assert merged[0].start.datetime() == datetime.datetime(2020, 7, 3, 12, 0)
    assert merged[0].end.datetime() == datetime.datetime(2020, 7, 6, 12, 0)


def test_unknown_year_adjustment():
    ref = datetime.datetime(2020, 7, 1, 12, 0)
    # December 30 parses to Dec 30, 2020.
    # January 5 parses to Jan 5, 2020.
    # Since Dec 30 > Jan 5, and Jan 5 has unknown year, it adjusts to Jan 5, 2021.
    result = chrono.en.parse("December 30 - January 5", reference=ref)

    assert len(result) == 1
    assert result[0].text == "December 30 - January 5"
    assert isinstance(result[0], ParsedRangeResult)
    assert result[0].start.datetime() == datetime.datetime(2020, 12, 30, 12, 0)
    assert result[0].end.datetime() == datetime.datetime(2021, 1, 5, 12, 0)


def test_swap_fallback():
    ref = datetime.datetime(2020, 7, 1, 12, 0)
    # Both dates have explicit years, so no adjustment logic matches.
    # It should fallback to swapping them.
    result = chrono.en.parse("2020-02-15 - 2020-02-13", reference=ref)

    assert len(result) == 1
    assert result[0].text == "2020-02-15 - 2020-02-13"
    assert isinstance(result[0], ParsedRangeResult)
    assert result[0].start.datetime() == datetime.datetime(2020, 2, 13, 12, 0)
    assert result[0].end.datetime() == datetime.datetime(2020, 2, 15, 12, 0)


def test_en_casual_time_range_merging():
    ref_date = datetime.datetime(2012, 8, 4, 12, 0)

    # today morning to tomorrow
    results = chrono.parse("annual leave from today morning to tomorrow", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "today morning to tomorrow"
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

    # today to tomorrow afternoon
    results = chrono.parse("annual leave from today to tomorrow afternoon", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "today to tomorrow afternoon"
    assert isinstance(result, ParsedRangeResult)
    assert result.start.get(CivilTimeComponent.MONTH) == 8
    assert result.start.get(CivilTimeComponent.DAY) == 4
    assert result.start.get(CivilTimeComponent.HOUR) == 12
    assert not result.start.is_certain(CivilTimeComponent.HOUR)
    assert result.start.precision() == DateTimePrecision.DAY

    assert result.end.get(CivilTimeComponent.MONTH) == 8
    assert result.end.get(CivilTimeComponent.DAY) == 5
    assert result.end.get(CivilTimeComponent.HOUR) == 15
    assert not result.end.is_certain(CivilTimeComponent.HOUR)
    assert result.end.precision() == DateTimePrecision.DAY
