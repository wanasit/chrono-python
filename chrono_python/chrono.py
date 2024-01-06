import re
import datetime
from abc import abstractmethod, ABC

from chrono_python.result import ParsedResult, ParsedRangeResult, ParsingMoment
from chrono_python.types import Moment, DateTimeMoment


class ParsingContext:
    def __init__(self, text: str, reference: Moment):
        self._text = text
        self._reference = reference

    @property
    def text(self) -> str:
        return self._text

    @property
    def reference(self) -> Moment:
        return self._reference

    def create_parsed_result(self, index: int, text_or_end_index: str | int, start: Moment,
                             end: Moment | None = None) -> ParsedResult:
        text = text_or_end_index if isinstance(text_or_end_index, str) else self.text[index:text_or_end_index]
        if end is not None:
            return ParsedRangeResult(index, text, start, end)
        return ParsedResult(index, text, start)


class Parser(ABC):
    @abstractmethod
    def pattern(self) -> re.Pattern:
        raise NotImplementedError()

    @abstractmethod
    def extract(self, context: ParsingContext, match: re.Match):
        raise NotImplementedError()


class Refiner(ABC):

    @abstractmethod
    def refine(self, context: ParsingContext, results: list[ParsedResult]) -> list[ParsedResult]:
        raise NotImplementedError()


class Configuration:
    def __init__(self, parsers: list[Parser], refiners: list[Refiner]):
        self.parsers = parsers
        self.refiners = refiners


class Chrono:
    def __init__(self, configuration: Configuration):
        self.parsers = configuration.parsers[:]
        self.refiners = configuration.refiners[:]

    def parse_date(self, text, reference: Moment | None) -> datetime.datetime | None:
        results = self.parse(text, reference)
        if len(results) > 0:
            return results[0].datetime()
        return None

    def parse(self, text, reference: Moment | None) -> list[ParsedResult]:
        reference = reference if reference is not None else DateTimeMoment.now()
        context = ParsingContext(text, reference)
        results: list[ParsedResult] = []
        for parser in self.parsers:
            sub_results = Chrono._execute_parser(context, parser)
            results += sub_results

        results = sorted(results, key=lambda x: x.index)
        for refiners in self.refiners:
            results = refiners.refine(context, results)

        return results

    @staticmethod
    def _execute_parser(context: ParsingContext, parser: Parser) -> list[ParsedResult]:
        results: list[ParsedResult] = []
        pattern = parser.pattern()

        offset = 0
        while offset < len(context.text):
            match = pattern.search(context.text, offset)
            if match is None:
                return results

            result = parser.extract(context, match)
            if result is None:
                offset += 1
                continue

            if isinstance(result, Moment):
                result = context.create_parsed_result(match.start(), match.end(), result)

            offset += result.index + len(result.text)
            results.append(result)
        return results
