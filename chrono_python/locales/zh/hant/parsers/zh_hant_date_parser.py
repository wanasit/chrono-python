import re
from chrono_python import chrono
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent
from chrono_python.locales.zh.hant.constants import NUMBER, zh_string_to_number, zh_string_to_year


class ZHHantDateParser(chrono.Parser):
    def __init__(self):
        num_chars = "".join(NUMBER.keys())
        self._pattern = re.compile(
            rf"(?:"
            rf"(\d{{2,4}}|[{num_chars}]{{4}}|[{num_chars}]{{2}})"
            rf"(?:\s*)(?:年)?[\s|,|，]*"
            rf")?"
            rf"(\d{{1,2}}|[{num_chars}]{{1,3}})"
            rf"(?:\s*)(?:月)(?:\s*)"
            rf"(\d{{1,2}}|[{num_chars}]{{1,3}})?"
            rf"(?:\s*)(?:日|號)?" ,
            re.IGNORECASE,
        )

    def pattern(self) -> re.Pattern:
        return self._pattern

    def extract(self, context: chrono.ParsingContext, match: chrono.Match) -> chrono.ParsedResult | None:
        year_str = match.group(1)
        month_str = match.group(2)
        day_str = match.group(3)

        result = ParsingCivilTimeMoment.of(context.reference)
        ref_dt = context.reference.datetime()

        # Month
        if month_str.isdigit():
            month = int(month_str)
        else:
            month = zh_string_to_number(month_str)
        result.assign(CivilTimeComponent.MONTH, month)

        # Day
        if day_str:
            if day_str.isdigit():
                day = int(day_str)
            else:
                day = zh_string_to_number(day_str)
            result.assign(CivilTimeComponent.DAY, day)
        else:
            result.imply(CivilTimeComponent.DAY, ref_dt.day)

        # Year
        if year_str:
            if year_str.isdigit():
                year = int(year_str)
            else:
                year = zh_string_to_year(year_str)
            result.assign(CivilTimeComponent.YEAR, year)
        else:
            result.imply(CivilTimeComponent.YEAR, ref_dt.year)

        return result
