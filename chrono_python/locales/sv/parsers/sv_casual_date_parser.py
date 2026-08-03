import re
import datetime
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent
from chrono_python.types import Moment

PATTERN = re.compile(
    r"(nu|idag|imorgon|imorn|övermorgon|igår|förrgår|i\s*förrgår)"
    r"(?:\s*(?:på\s*|vid\s*)?(morgonen?|förmiddagen?|middagen?|eftermiddagen?|kvällen?|natten?|midnatt))?"
    r"(?=\W|$)",
    re.IGNORECASE,
)


class SVCasualDateParser(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        target_date = context.reference.datetime()
        date_keyword = (match.group(1) or "").lower()
        time_keyword = (match.group(2) or "").lower()

        component = ParsingCivilTimeMoment.of(context.reference)

        if date_keyword == "nu":
            component.assign_similar_date(target_date)
            component.assign_similar_time(target_date)
            if target_date.tzinfo is not None:
                offset = target_date.utcoffset()
                if offset is not None:
                    component.assign(
                        CivilTimeComponent.TIMEZONE_OFFSET,
                        int(offset.total_seconds() / 60),
                    )
        elif date_keyword == "idag":
            component.assign_similar_date(target_date)
            component.imply_similar_time(target_date)
            component.delete(CivilTimeComponent.MERIDIEM)
        elif date_keyword in ("imorgon", "imorn"):
            next_day = target_date + datetime.timedelta(days=1)
            component.assign_similar_date(next_day)
            component.imply_similar_time(next_day)
            component.delete(CivilTimeComponent.MERIDIEM)
        elif date_keyword == "övermorgon":
            next_day = target_date + datetime.timedelta(days=2)
            component.assign_similar_date(next_day)
            component.imply_similar_time(next_day)
            component.delete(CivilTimeComponent.MERIDIEM)
        elif date_keyword == "igår":
            prev_day = target_date - datetime.timedelta(days=1)
            component.assign_similar_date(prev_day)
            component.imply_similar_time(prev_day)
            component.delete(CivilTimeComponent.MERIDIEM)
        elif date_keyword in ("förrgår", "i förrgår") or re.match(r"i\s*förrgår", date_keyword):
            two_days_ago = target_date - datetime.timedelta(days=2)
            component.assign_similar_date(two_days_ago)
            component.imply_similar_time(two_days_ago)
            component.delete(CivilTimeComponent.MERIDIEM)

        if time_keyword in ("morgon", "morgonen"):
            component.imply(CivilTimeComponent.HOUR, 6)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.SECOND, 0)
            component.imply(CivilTimeComponent.MILLI_SECOND, 0)
        elif time_keyword in ("förmiddag", "förmiddagen"):
            component.imply(CivilTimeComponent.HOUR, 9)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.SECOND, 0)
            component.imply(CivilTimeComponent.MILLI_SECOND, 0)
        elif time_keyword in ("middag", "middagen"):
            component.imply(CivilTimeComponent.HOUR, 12)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.SECOND, 0)
            component.imply(CivilTimeComponent.MILLI_SECOND, 0)
        elif time_keyword in ("eftermiddag", "eftermiddagen"):
            component.imply(CivilTimeComponent.HOUR, 15)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.SECOND, 0)
            component.imply(CivilTimeComponent.MILLI_SECOND, 0)
        elif time_keyword in ("kväll", "kvällen"):
            component.imply(CivilTimeComponent.HOUR, 20)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.SECOND, 0)
            component.imply(CivilTimeComponent.MILLI_SECOND, 0)
        elif time_keyword in ("natt", "natten", "midnatt"):
            if time_keyword == "midnatt":
                component.imply(CivilTimeComponent.HOUR, 0)
            else:
                component.imply(CivilTimeComponent.HOUR, 2)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.SECOND, 0)
            component.imply(CivilTimeComponent.MILLI_SECOND, 0)

        return component
