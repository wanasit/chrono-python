import datetime
import chrono_python as chrono
from chrono_python.chrono import ParsingContext
from chrono_python.types import ParsedResult, DateTimeMoment, DateTimePrecision
from chrono_python.locales.en.refiners.en_unlikely_format_filter import ENUnlikelyFormatFilter


def test_en_unlikely_format_filter_may_direct():
    ref_dt = datetime.datetime(2020, 1, 1, 12, 0)
    ref_moment = DateTimeMoment.of(ref_dt)
    filter_inst = ENUnlikelyFormatFilter()

    # Standalone "may" when it's the whole text is valid
    context = ParsingContext("may", ref_moment)
    result = ParsedResult(index=0, text="may", moment=ref_moment)
    assert filter_inst.is_valid(context, result) is True

    # "may" in a sentence not preceded by "in" should be invalid
    context = ParsingContext("He may come today", ref_moment)
    result = ParsedResult(index=3, text="may", moment=ref_moment)
    assert filter_inst.is_valid(context, result) is False

    # "may" preceded by "in" should be valid
    context = ParsingContext("meet in may", ref_moment)
    result = ParsedResult(index=8, text="may", moment=ref_moment)
    assert filter_inst.is_valid(context, result) is True


def test_en_unlikely_format_filter_second_direct():
    ref_dt = datetime.datetime(2020, 1, 1, 12, 0)
    ref_moment = DateTimeMoment.of(ref_dt)
    filter_inst = ENUnlikelyFormatFilter()

    # Standalone "the second" when it's the whole text is valid
    context = ParsingContext("the second", ref_moment)
    result = ParsedResult(index=0, text="the second", moment=ref_moment)
    assert filter_inst.is_valid(context, result) is True

    # "the second" with trailing text should be invalid
    context = ParsingContext("the second option is better", ref_moment)
    result = ParsedResult(index=0, text="the second", moment=ref_moment)
    assert filter_inst.is_valid(context, result) is False


def test_en_unlikely_format_filter_integration():
    ref_date = datetime.datetime(2020, 1, 1, 12, 0)

    # Integration test with standard chrono parser
    # "in the second" has no trailing text, so it's kept.
    results = chrono.en.parse("in the second", ref_date)
    assert len(results) == 1
    assert results[0].text == "in the second"

    # "in the second option" has trailing text, so it is filtered out.
    results = chrono.en.parse("in the second option", ref_date)
    # The filter should reject it.
    assert len(results) == 0
