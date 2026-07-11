import re
import datetime
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent, Meridiem
from chrono_python.types import Moment

PATTERN = re.compile(
    r'(now|today|tonight|tomorrow|overmorrow|tmr|tmrw|yesterday|last\s*night)(?=\W|$)',
    re.IGNORECASE
)


class ENCasualDateParser(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(self, context: chrono.ParsingContext, match: chrono.Match) -> chrono.ParsedResult | Moment | None:
        target_date = context.reference.datetime()
        lower_text = match[0].lower()
        component = ParsingCivilTimeMoment(context.reference, {})

        if lower_text == "now":
            component.assign_similar_date(target_date)
            component.assign_similar_time(target_date)
            if target_date.tzinfo is not None:
                offset = target_date.utcoffset()
                if offset is not None:
                    component.assign(CivilTimeComponent.TIMEZONE_OFFSET, int(offset.total_seconds() / 60))
        elif lower_text == "today":
            component.assign_similar_date(target_date)
            component.imply_similar_time(target_date)
            component.delete(CivilTimeComponent.MERIDIEM)
        elif lower_text == "yesterday":
            new_date = target_date - datetime.timedelta(days=1)
            component.assign_similar_date(new_date)
            component.imply_similar_time(new_date)
            component.delete(CivilTimeComponent.MERIDIEM)
        elif lower_text in ("tomorrow", "tmr", "tmrw"):
            new_date = target_date + datetime.timedelta(days=1)
            component.assign_similar_date(new_date)
            component.imply_similar_time(new_date)
            component.delete(CivilTimeComponent.MERIDIEM)
        elif lower_text == "overmorrow":
            new_date = target_date + datetime.timedelta(days=2)
            component.assign_similar_date(new_date)
            component.imply_similar_time(new_date)
            component.delete(CivilTimeComponent.MERIDIEM)
        elif lower_text == "tonight":
            component.assign_similar_date(target_date)
            component.imply(CivilTimeComponent.HOUR, 22)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)
        elif re.match(r'last\s*night', lower_text):
            if target_date.hour > 6:
                target_date = target_date - datetime.timedelta(days=1)
            component.assign_similar_date(target_date)
            component.imply(CivilTimeComponent.HOUR, 0)
        else:
            return None

        return component
