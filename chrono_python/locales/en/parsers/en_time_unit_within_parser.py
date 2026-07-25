import re
import datetime
from chrono_python import chrono
from chrono_python.common.parsers.abstract_parser_with_word_boundary import AbstractParserWithWordBoundary
from chrono_python.locales.en import constants
from chrono_python.types import Moment, ReferenceMoment, Timeunit
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent

def compile_pattern(timeunit_pattern: str, timeunit_word_pattern: str) -> re.Pattern:
    return re.compile(
        r'(?:'
            r'(?:within|in|for)\s*(?:(?:about|around|roughly|approximately|just)\s*(?:~\s*)?)?'
            rf'({timeunit_pattern})'
        r'|'
            r'(this|last|past|next|after\s+this)\s+'
            r'(?:'
                r'(?:(?:about|around)\s{0,3})?'
                rf'({timeunit_pattern})'
                r'|'
                rf'({timeunit_word_pattern})'
            r')'
        r')'
        r'(?=\W|$)',
        re.IGNORECASE
    )


class ENTimeUnitWithinParser(AbstractParserWithWordBoundary):
    def __init__(self, allow_abbreviations: bool = True):
        super().__init__()
        timeunit_pattern = constants.TIME_UNITS_PATTERN if allow_abbreviations else constants.TIME_UNITS_NO_ABBR_PATTERN
        
        # Sort time unit dictionary keys by length in descending order and escape them
        sorted_keys = sorted(constants.TIME_UNIT_DICTIONARY.keys(), key=len, reverse=True)
        escaped_keys = [k.replace('.', '\\.') for k in sorted_keys]
        timeunit_word_pattern = f'(?:{"|".join(escaped_keys)})'
        
        self._pattern = compile_pattern(timeunit_pattern, timeunit_word_pattern)

    def inner_pattern(self) -> re.Pattern:
        return self._pattern

    def inner_extract(self, context: chrono.ParsingContext, match: chrono.Match) -> chrono.ParsedResult | Moment | None:
        if re.match(r'^for\s*the\s*\w+', match.group(0), re.IGNORECASE):
            return None

        # Case 1: within/in/for
        if match.group(1) is not None:
            time_units = constants.parse_duration(match.group(1))
            if not time_units:
                return None
            return ReferenceMoment.of(context.reference, time_units)

        # Case 2: this/next/last/past/after this
        prefix = match.group(2).lower()
        duration_text = match.group(3)
        unit_word = match.group(4)

        if duration_text:
            time_units = constants.parse_duration(duration_text)
        elif unit_word:
            unit = constants.TIME_UNIT_DICTIONARY[unit_word.lower()]
            time_units = {unit: 1}
        else:
            return None

        if not time_units:
            return None

        # Apply multiplier/negation based on prefix
        if prefix in ('last', 'past'):
            # reverse duration
            time_units = {k: -v for k, v in time_units.items()}
            return ReferenceMoment.of(context.reference, time_units)
        elif prefix == 'this':
            if unit_word:
                unit = list(time_units.keys())[0]
                moment = ParsingCivilTimeMoment.of(context.reference)
                ref_dt = context.reference.datetime()
                if unit == Timeunit.WEEK:
                    # Sunday-start of the week
                    js_weekday = (ref_dt.weekday() + 1) % 7
                    start_of_week = ref_dt - datetime.timedelta(days=js_weekday)
                    moment.imply(CivilTimeComponent.DAY, start_of_week.day)
                    moment.imply(CivilTimeComponent.MONTH, start_of_week.month)
                    moment.imply(CivilTimeComponent.YEAR, start_of_week.year)
                elif unit == Timeunit.MONTH:
                    moment.imply(CivilTimeComponent.DAY, 1)
                    moment.assign(CivilTimeComponent.MONTH, ref_dt.month)
                    moment.assign(CivilTimeComponent.YEAR, ref_dt.year)
                elif unit == Timeunit.YEAR:
                    moment.imply(CivilTimeComponent.DAY, 1)
                    moment.imply(CivilTimeComponent.MONTH, 1)
                    moment.assign(CivilTimeComponent.YEAR, ref_dt.year)
                else:
                    # fallback to offset 0
                    time_units = {unit: 0}
                    return ReferenceMoment.of(context.reference, time_units)
                return moment
            else:
                return ReferenceMoment.of(context.reference, time_units)
        else:
            # next / after this
            return ReferenceMoment.of(context.reference, time_units)
