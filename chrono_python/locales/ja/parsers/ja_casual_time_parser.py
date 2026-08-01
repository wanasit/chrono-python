import re
import datetime
from chrono_python import chrono
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent, Meridiem
from chrono_python.types import Moment, DateTimePrecision

PATTERN = re.compile(r'朝|午前中|昼|お昼|夕方|夜|深夜|真夜中|正午')


class JACasualTimeParser(chrono.Parser):
    def pattern(self) -> re.Pattern:
        return PATTERN

    def extract(self, context: chrono.ParsingContext, match: chrono.Match) -> chrono.ParsedResult | Moment | None:
        text = match.group(0)
        component = ParsingCivilTimeMoment.of(context.reference)

        if text in ("朝", "午前中"):
            component.assign(CivilTimeComponent.MERIDIEM, Meridiem.AM)
            component.imply(CivilTimeComponent.HOUR, 6)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.SECOND, 0)
            component.imply(CivilTimeComponent.MILLI_SECOND, 0)
        elif text in ("昼", "お昼", "正午"):
            component.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
            component.assign(CivilTimeComponent.HOUR, 12)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.SECOND, 0)
            component.imply(CivilTimeComponent.MILLI_SECOND, 0)
        elif text == "夕方":
            component.assign(CivilTimeComponent.MERIDIEM, Meridiem.PM)
            component.imply(CivilTimeComponent.HOUR, 18)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.SECOND, 0)
            component.imply(CivilTimeComponent.MILLI_SECOND, 0)
        elif text == "夜":
            component.assign(CivilTimeComponent.MERIDIEM, Meridiem.PM)
            component.imply(CivilTimeComponent.HOUR, 20)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.SECOND, 0)
            component.imply(CivilTimeComponent.MILLI_SECOND, 0)
        elif text in ("深夜", "真夜中"):
            target_date = context.reference.datetime()
            if target_date.hour > 2:
                target_date = target_date + datetime.timedelta(days=1)
            component = ParsingCivilTimeMoment.of(target_date, DateTimePrecision.DAY)
            component.assign(CivilTimeComponent.HOUR, 0)
            component.imply(CivilTimeComponent.MINUTE, 0)
            component.imply(CivilTimeComponent.SECOND, 0)
            component.imply(CivilTimeComponent.MILLI_SECOND, 0)
        else:
            return None

        return component
