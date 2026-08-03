import re
import datetime
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent, Meridiem
from chrono_python.types import Moment

PATTERN = re.compile(
    r"(сейчас|прошлым\s*вечером|прошлой\s*ночью|следующей\s*ночью|сегодня\s*ночью|этой\s*ночью|ночью|этим\s+утром|утром|утра|в\s*полдень|вечером|вечера|в\s*полночь)",
    re.IGNORECASE,
)


class RUCasualTimeParser(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        target_date = context.reference.datetime()
        lower_text = match.group(0).lower()
        component = ParsingCivilTimeMoment.of(context.reference)

        if lower_text == "сейчас":
            component.assign_similar_date(target_date)
            component.assign_similar_time(target_date)
            if target_date.tzinfo is not None:
                offset = target_date.utcoffset()
                if offset is not None:
                    component.assign(
                        CivilTimeComponent.TIMEZONE_OFFSET,
                        int(offset.total_seconds() / 60),
                    )
        elif lower_text in ("вечером", "вечера"):
            component.imply_similar_date(target_date)
            component.imply(CivilTimeComponent.HOUR, 20)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)
        elif lower_text.endswith("утром") or lower_text.endswith("утра"):
            component.imply_similar_date(target_date)
            component.imply(CivilTimeComponent.HOUR, 6)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
        elif re.search(r"в\s*полдень", lower_text):
            component.imply_similar_date(target_date)
            component.imply(CivilTimeComponent.HOUR, 12)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.SECOND, 0)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
        elif re.search(r"прошлой\s*ночью", lower_text):
            if target_date.hour < 6:
                target_date = target_date - datetime.timedelta(days=1)
            component.assign_similar_date(target_date)
            component.imply(CivilTimeComponent.HOUR, 0)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
        elif re.search(r"прошлым\s*вечером", lower_text):
            target_date = target_date - datetime.timedelta(days=1)
            component.assign_similar_date(target_date)
            component.imply(CivilTimeComponent.HOUR, 20)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)
        elif re.search(r"следующей\s*ночью", lower_text):
            days_to_add = 1 if target_date.hour < 22 else 2
            next_day = target_date + datetime.timedelta(days=days_to_add)
            component.assign_similar_date(next_day)
            component.imply(CivilTimeComponent.HOUR, 0)
        elif re.search(r"в\s*полночь", lower_text) or lower_text.endswith("ночью"):
            component.imply_similar_date(target_date)
            component.imply(CivilTimeComponent.HOUR, 0)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
        else:
            return None

        return component
