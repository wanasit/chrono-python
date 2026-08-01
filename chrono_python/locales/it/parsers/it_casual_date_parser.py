import re
import datetime
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent, Meridiem
from chrono_python.types import Moment

PATTERN = re.compile(
    r"(adesso|ora|oggi|stasera|stanotte|domani|dopodomani|ieri\s*sera|ieri\s*notte|ieri)(?=\W|$)",
    re.IGNORECASE,
)


class ITCasualDateParser(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        target_date = context.reference.datetime()
        lower_text = match[0].lower()
        component = ParsingCivilTimeMoment.of(context.reference)

        if lower_text in ("adesso", "ora"):
            component.assign_similar_date(target_date)
            component.assign_similar_time(target_date)
            if target_date.tzinfo is not None:
                offset = target_date.utcoffset()
                if offset is not None:
                    component.assign(
                        CivilTimeComponent.TIMEZONE_OFFSET,
                        int(offset.total_seconds() / 60),
                    )
        elif lower_text == "oggi":
            component.assign_similar_date(target_date)
            component.imply_similar_time(target_date)
            component.delete(CivilTimeComponent.MERIDIEM)
        elif lower_text == "ieri":
            new_date = target_date - datetime.timedelta(days=1)
            component.assign_similar_date(new_date)
            component.imply_similar_time(new_date)
            component.delete(CivilTimeComponent.MERIDIEM)
        elif lower_text == "domani":
            new_date = target_date + datetime.timedelta(days=1)
            component.assign_similar_date(new_date)
            component.imply_similar_time(new_date)
            component.delete(CivilTimeComponent.MERIDIEM)
        elif lower_text == "dopodomani":
            new_date = target_date + datetime.timedelta(days=2)
            component.assign_similar_date(new_date)
            component.imply_similar_time(new_date)
            component.delete(CivilTimeComponent.MERIDIEM)
        elif lower_text in ("stasera", "stanotte"):
            component.assign_similar_date(target_date)
            component.imply(CivilTimeComponent.HOUR, 22)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)
        elif re.match(r"ieri\s*sera", lower_text):
            if target_date.hour > 6:
                target_date = target_date - datetime.timedelta(days=1)
            component.assign_similar_date(target_date)
            component.imply(CivilTimeComponent.HOUR, 20)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)
        elif re.match(r"ieri\s*notte", lower_text):
            if target_date.hour > 6:
                target_date = target_date - datetime.timedelta(days=1)
            component.assign_similar_date(target_date)
            component.imply(CivilTimeComponent.HOUR, 0)
        else:
            return None

        return component
