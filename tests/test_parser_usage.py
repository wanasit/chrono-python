import datetime
import re
from chrono_python.chrono import Chrono, Configuration, Parser, ParsingContext
from chrono_python.types import Timeunit, ReferenceMoment, ParsedResult, DateTimeMoment, DateTimePrecision
from chrono_python.common.types import ParsingDateTimeMoment, DateTimeComponent
from chrono_python.utils.re import Match


def test_no_parsers():
    # A Chrono instance with no parsers
    config = Configuration(parsers=[], refiners=[])
    chrono = Chrono(config)

    ref_date = datetime.datetime(2025, 6, 1, 12, 0)
    results = chrono.parse("Chrismas is Tomorrow", reference=ref_date)
    assert len(results) == 0


def test_custom_parser_return_date():
    class ChrismasParser(Parser):
        def pattern(self) -> re.Pattern:
            return re.compile(r'Chrismas', re.IGNORECASE)

        def extract(self, context: ParsingContext, match: Match) -> ParsingDateTimeMoment | None:
            moment = ParsingDateTimeMoment(context.reference, {})
            moment.assign(DateTimeComponent.MONTH, 12)
            moment.assign(DateTimeComponent.DAY, 25)
            moment.imply(DateTimeComponent.YEAR, context.reference.datetime().year)
            return moment

    # A custom parser that detects only "Chrismas" and returns 12/25 and year implied from reference date
    parser = ChrismasParser()
    config = Configuration(parsers=[parser], refiners=[])
    chrono = Chrono(config)

    ref_date = datetime.datetime(2025, 6, 1, 12, 0)
    results = chrono.parse("We celebrate Chrismas!", reference=ref_date)
    assert len(results) == 1

    result = results[0]
    assert result.text == "Chrismas"
    assert result.index == 13
    assert isinstance(result.moment, DateTimeMoment)
    assert result.moment.datetime() == datetime.datetime(2025, 12, 25, 12, 0)
    assert result.moment.precision() == DateTimePrecision.DAY

    # Check component values
    assert result.moment.get(DateTimeComponent.MONTH) == 12
    assert result.moment.get(DateTimeComponent.DAY) == 25
    assert result.moment.get(DateTimeComponent.YEAR) == 2025

    # Check certainty
    assert result.moment.is_certain(DateTimeComponent.MONTH) is True
    assert result.moment.is_certain(DateTimeComponent.DAY) is True
    assert result.moment.is_certain(DateTimeComponent.YEAR) is False


def test_custom_parser_return_ref():
    class TomorrowParser(Parser):
        def pattern(self) -> re.Pattern:
            return re.compile(r'Tomorrow', re.IGNORECASE)

        def extract(self, context: ParsingContext, match: Match) -> ReferenceMoment | None:
            return ReferenceMoment(context.reference, {Timeunit.DAY: 1})

    # A custom parser that detects only "Tomorrow" and returns ref+1d
    parser = TomorrowParser()
    config = Configuration(parsers=[parser], refiners=[])
    chrono = Chrono(config)

    ref_date = datetime.datetime(2025, 6, 1, 12, 0)
    results = chrono.parse("Let's meet Tomorrow afternoon", reference=ref_date)
    assert len(results) == 1

    result = results[0]
    assert result.text == "Tomorrow"
    assert result.index == 11
    assert isinstance(result.moment, ReferenceMoment)

    # Check that datetime() on result returns ref_date + 1 day
    expected_date = ref_date + datetime.timedelta(days=1)
    assert result.moment.datetime() == expected_date
    assert result.datetime() == expected_date


def test_custom_parser_return_result():
    class TodayParser(Parser):
        def pattern(self) -> re.Pattern:
            return re.compile(r'Today', re.IGNORECASE)

        def extract(self, context: ParsingContext, match: Match) -> ParsedResult | None:
            moment = ReferenceMoment(context.reference, {Timeunit.DAY: 0})
            return context.create_parsed_result(match.start(), match.end(), moment)

    parser = TodayParser()
    config = Configuration(parsers=[parser], refiners=[])
    chrono = Chrono(config)

    ref_date = datetime.datetime(2025, 6, 1, 12, 0)
    results = chrono.parse("Today is a sunny day", reference=ref_date)
    assert len(results) == 1

    result = results[0]
    assert result.text == "Today"
    assert result.index == 0
    assert isinstance(result, ParsedResult)
    assert result.moment.datetime().year == 2025
    assert result.moment.datetime().month == 6
    assert result.moment.datetime().day == 1
