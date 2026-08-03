import re
import datetime
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent
from chrono_python.types import Moment
from chrono_python.locales.fi.parsers.fi_casual_time_parser import FICasualTimeParser

PATTERN = re.compile(
    r"(nyt|tänään|huomenna|ylihuomenna|eilen|toissapäivänä|viime\s*yönä)"
    r"(?:\s*(aamulla|aamuna|aamupäivällä|päivällä|iltapäivällä|illalla|yöllä|keskiyöllä))?"
    r"(?=\W|$)",
    re.IGNORECASE,
)


class FICasualDateParser(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        target_date = context.reference.datetime()
        date_keyword = (match.group(1) or "").lower()
        time_keyword = (match.group(2) or "").lower()

        component = ParsingCivilTimeMoment.of(context.reference)

        if date_keyword == "nyt":
            component.assign_similar_date(target_date)
            component.assign_similar_time(target_date)
            if target_date.tzinfo is not None:
                offset = target_date.utcoffset()
                if offset is not None:
                    component.assign(
                        CivilTimeComponent.TIMEZONE_OFFSET,
                        int(offset.total_seconds() / 60),
                    )
        elif date_keyword == "tänään":
            component.assign_similar_date(target_date)
            component.imply_similar_time(target_date)
            component.delete(CivilTimeComponent.MERIDIEM)
        elif date_keyword == "huomenna":
            new_date = target_date + datetime.timedelta(days=1)
            component.assign_similar_date(new_date)
            component.imply_similar_time(new_date)
            component.delete(CivilTimeComponent.MERIDIEM)
        elif date_keyword == "ylihuomenna":
            new_date = target_date + datetime.timedelta(days=2)
            component.assign_similar_date(new_date)
            component.imply_similar_time(new_date)
            component.delete(CivilTimeComponent.MERIDIEM)
        elif date_keyword == "eilen":
            new_date = target_date - datetime.timedelta(days=1)
            component.assign_similar_date(new_date)
            component.imply_similar_time(new_date)
            component.delete(CivilTimeComponent.MERIDIEM)
        elif date_keyword == "toissapäivänä":
            new_date = target_date - datetime.timedelta(days=2)
            component.assign_similar_date(new_date)
            component.imply_similar_time(new_date)
            component.delete(CivilTimeComponent.MERIDIEM)
        elif re.match(r"viime\s*yönä", date_keyword):
            if target_date.hour > 6:
                target_date = target_date - datetime.timedelta(days=1)
            component.assign_similar_date(target_date)
            component.imply(CivilTimeComponent.HOUR, 0)
        else:
            return None

        if time_keyword:
            component = FICasualTimeParser.extract_time_components(component, time_keyword)

        return component
