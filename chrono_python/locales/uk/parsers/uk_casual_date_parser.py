import re
import datetime
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent
from chrono_python.types import Moment

PATTERN = re.compile(
    r"(?:з|із|від)?\s*(сьогодні|вчора|завтра|післязавтра|післяпіслязавтра|позапозавчора|позавчора)(?=\W|$)",
    re.IGNORECASE,
)


class UKCasualDateParser(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        target_date = context.reference.datetime()
        lower_text = match.group(1).lower()
        component = ParsingCivilTimeMoment.of(context.reference)

        if lower_text == "сьогодні":
            component.assign_similar_date(target_date)
            component.imply_similar_time(target_date)
            component.delete(CivilTimeComponent.MERIDIEM)
        elif lower_text == "вчора":
            new_date = target_date - datetime.timedelta(days=1)
            component.assign_similar_date(new_date)
            component.imply_similar_time(new_date)
            component.delete(CivilTimeComponent.MERIDIEM)
        elif lower_text == "завтра":
            new_date = target_date + datetime.timedelta(days=1)
            component.assign_similar_date(new_date)
            component.imply_similar_time(new_date)
            component.delete(CivilTimeComponent.MERIDIEM)
        elif lower_text == "післязавтра":
            new_date = target_date + datetime.timedelta(days=2)
            component.assign_similar_date(new_date)
            component.imply_similar_time(new_date)
            component.delete(CivilTimeComponent.MERIDIEM)
        elif lower_text == "післяпіслязавтра":
            new_date = target_date + datetime.timedelta(days=3)
            component.assign_similar_date(new_date)
            component.imply_similar_time(new_date)
            component.delete(CivilTimeComponent.MERIDIEM)
        elif lower_text == "позавчора":
            new_date = target_date - datetime.timedelta(days=2)
            component.assign_similar_date(new_date)
            component.imply_similar_time(new_date)
            component.delete(CivilTimeComponent.MERIDIEM)
        elif lower_text == "позапозавчора":
            new_date = target_date - datetime.timedelta(days=3)
            component.assign_similar_date(new_date)
            component.imply_similar_time(new_date)
            component.delete(CivilTimeComponent.MERIDIEM)
        else:
            return None

        return component
