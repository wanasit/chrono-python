import re
import datetime
from chrono_python import chrono
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent, Meridiem
from chrono_python.types import Moment

PATTERN = re.compile(
    r'今日|きょう|本日|ほんじつ|昨日|きのう|明日|あした|今夜|こんや|今夕|こんゆう|今晩|こんばん|今朝|けさ',
    re.IGNORECASE
)


def normalize_text_to_kanji(text: str) -> str:
    mapping = {
        "きょう": "今日",
        "ほんじつ": "本日",
        "きのう": "昨日",
        "あした": "明日",
        "こんや": "今夜",
        "こんゆう": "今夕",
        "こんばん": "今晩",
        "けさ": "今朝",
    }
    return mapping.get(text, text)


class JACasualDateParser(chrono.Parser):
    def pattern(self) -> re.Pattern:
        return PATTERN

    def extract(self, context: chrono.ParsingContext, match: chrono.Match) -> chrono.ParsedResult | Moment | None:
        text = normalize_text_to_kanji(match.group(0))
        target_date = context.reference.datetime()

        if text in ("本日", "今日"):
            component = ParsingCivilTimeMoment.of(context.reference)
            component.assign_similar_date(target_date)
            component.imply_similar_time(target_date)
            component.delete(CivilTimeComponent.MERIDIEM)
            return component
        elif text == "昨日":
            component = ParsingCivilTimeMoment.of(context.reference)
            new_date = target_date - datetime.timedelta(days=1)
            component.assign_similar_date(new_date)
            component.imply_similar_time(new_date)
            component.delete(CivilTimeComponent.MERIDIEM)
            return component
        elif text == "明日":
            component = ParsingCivilTimeMoment.of(context.reference)
            new_date = target_date + datetime.timedelta(days=1)
            component.assign_similar_date(new_date)
            component.imply_similar_time(new_date)
            component.delete(CivilTimeComponent.MERIDIEM)
            return component

        components = ParsingCivilTimeMoment.of(context.reference)
        if text in ("今夜", "今夕", "今晩"):
            components.imply(CivilTimeComponent.HOUR, 22)
            components.imply(CivilTimeComponent.MERIDIEM, Meridiem.PM)
        elif text == "今朝":
            components.imply(CivilTimeComponent.HOUR, 6)
            components.imply(CivilTimeComponent.MERIDIEM, Meridiem.AM)
        else:
            return None

        components.assign(CivilTimeComponent.DAY, target_date.day)
        components.assign(CivilTimeComponent.MONTH, target_date.month)
        components.assign(CivilTimeComponent.YEAR, target_date.year)
        return components
