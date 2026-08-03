import re
import datetime
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent, Meridiem
from chrono_python.types import Moment

PATTERN = re.compile(
    r"(jetzt|heute\s*(?:nacht|abend|morgen|nachmittag)?|diese\s*nacht|diesen\s*(?:abend|morgen)|morgen|übermorgen|uebermorgen|gestern\s*(?:abend|nacht)?|gestern|vorgestern)(?=\W|$)",
    re.IGNORECASE,
)


class DECasualDateParser(AbstractParserWithWordBoundary):
    def inner_pattern(self) -> re.Pattern:
        return PATTERN

    def inner_extract(
        self, context: chrono.ParsingContext, match: chrono.Match
    ) -> chrono.ParsedResult | Moment | None:
        target_date = context.reference.datetime()
        lower_text = match[0].lower()
        component = ParsingCivilTimeMoment.of(context.reference)

        if lower_text == "jetzt":
            component.assign_similar_date(target_date)
            component.assign_similar_time(target_date)
            if target_date.tzinfo is not None:
                offset = target_date.utcoffset()
                if offset is not None:
                    component.assign(
                        CivilTimeComponent.TIMEZONE_OFFSET,
                        int(offset.total_seconds() / 60),
                    )
        elif lower_text == "heute":
            component.assign_similar_date(target_date)
            component.imply_similar_time(target_date)
            component.delete(CivilTimeComponent.MERIDIEM)
        elif lower_text == "gestern":
            new_date = target_date - datetime.timedelta(days=1)
            component.assign_similar_date(new_date)
            component.imply_similar_time(new_date)
            component.delete(CivilTimeComponent.MERIDIEM)
        elif lower_text == "vorgestern":
            new_date = target_date - datetime.timedelta(days=2)
            component.assign_similar_date(new_date)
            component.imply_similar_time(new_date)
            component.delete(CivilTimeComponent.MERIDIEM)
        elif lower_text == "morgen":
            new_date = target_date + datetime.timedelta(days=1)
            component.assign_similar_date(new_date)
            component.imply_similar_time(new_date)
            component.delete(CivilTimeComponent.MERIDIEM)
        elif lower_text in ("übermorgen", "uebermorgen"):
            new_date = target_date + datetime.timedelta(days=2)
            component.assign_similar_date(new_date)
            component.imply_similar_time(new_date)
            component.delete(CivilTimeComponent.MERIDIEM)
        elif re.match(r"(?:heute|diese)\s*nacht", lower_text):
            component.assign_similar_date(target_date)
            component.imply(CivilTimeComponent.HOUR, 22)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)
        elif re.match(r"(?:heute|diesen)\s*abend", lower_text):
            component.assign_similar_date(target_date)
            component.imply(CivilTimeComponent.HOUR, 20)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)
        elif re.match(r"(?:heute|diesen)\s*morgen", lower_text):
            component.assign_similar_date(target_date)
            component.imply(CivilTimeComponent.HOUR, 6)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
        elif re.match(r"heute\s*nachmittag", lower_text):
            component.assign_similar_date(target_date)
            component.imply(CivilTimeComponent.HOUR, 15)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)
        elif re.match(r"gestern\s*abend", lower_text):
            new_date = target_date - datetime.timedelta(days=1)
            component.assign_similar_date(new_date)
            component.imply(CivilTimeComponent.HOUR, 20)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)
        elif re.match(r"gestern\s*nacht", lower_text):
            new_date = target_date - datetime.timedelta(days=1)
            component.assign_similar_date(new_date)
            component.imply(CivilTimeComponent.HOUR, 0)
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
        else:
            return None

        return component
