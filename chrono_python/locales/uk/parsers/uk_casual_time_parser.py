import re
import datetime
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent, Meridiem
from chrono_python.types import Moment

PATTERN = re.compile(
    r"(зараз|минулого\s*вечора|минулої\s*ночі|наступної\s*ночі|сьогодні\s*вночі|цієї\s*ночі|цього\s*ранку|вранці|ранку|зранку|опівдні|ввечері|вечора|опівночі|вночі)(?=\W|$)",
    re.IGNORECASE,
)


class UKCasualTimeParser(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        target_date = context.reference.datetime()
        lower_text = match.group(0).lower()
        component = ParsingCivilTimeMoment.of(context.reference)

        if lower_text == "зараз":
            component.assign_similar_date(target_date)
            component.assign_similar_time(target_date)
            if target_date.tzinfo is not None:
                offset = target_date.utcoffset()
                if offset is not None:
                    component.assign(
                        CivilTimeComponent.TIMEZONE_OFFSET,
                        int(offset.total_seconds() / 60),
                    )
            return component
        elif lower_text in ("ввечері", "вечора"):
            component.imply(CivilTimeComponent.HOUR, 20)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)
        elif lower_text.endswith("вранці") or lower_text.endswith("ранку") or lower_text.endswith("зранку"):
            component.imply(CivilTimeComponent.HOUR, 6)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
        elif lower_text.endswith("опівдні"):
            component.imply(CivilTimeComponent.HOUR, 12)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
        elif re.search(r"минулої\s*ночі", lower_text):
            if target_date.hour > 6:
                target_date = target_date - datetime.timedelta(days=1)
            component.assign_similar_date(target_date)
            component.imply(CivilTimeComponent.HOUR, 0)
        elif re.search(r"минулого\s*вечора", lower_text):
            target_date = target_date - datetime.timedelta(days=1)
            component.assign_similar_date(target_date)
            component.imply(CivilTimeComponent.HOUR, 20)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)
        elif re.search(r"наступної\s*ночі", lower_text):
            days_to_add = 1 if target_date.hour < 22 else 2
            next_day = target_date + datetime.timedelta(days=days_to_add)
            component.assign_similar_date(next_day)
            component.imply(CivilTimeComponent.HOUR, 1)
        elif re.search(r"цієї\s*ночі", lower_text) or lower_text.endswith("опівночі") or lower_text.endswith("вночі"):
            component.imply(CivilTimeComponent.HOUR, 0)
        else:
            return None

        return component
