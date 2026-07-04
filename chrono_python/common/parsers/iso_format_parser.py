import re

from chrono_python import chrono
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent


class ISOFormatParser(chrono.Parser):
    def pattern(self):
        return re.compile(r'(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{2})')

    def extract(self, context, match):
        moment = ParsingCivilTimeMoment(context.reference, {})
        moment.assign(CivilTimeComponent.YEAR, int(match.group('year')))
        moment.assign(CivilTimeComponent.MONTH, int(match.group('month')))
        moment.assign(CivilTimeComponent.DAY, int(match.group('day')))

        return moment
