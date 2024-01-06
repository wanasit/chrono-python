import re

from chrono_python import chrono
from chrono_python.types import DateTimeComponent


class ISOFormatParser(chrono.Parser):
    def pattern(self):
        return re.compile(r'(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{2})')

    def extract(self, context, match):
        moment = chrono.ParsingMoment(context.reference, {})
        moment.assign(DateTimeComponent.YEAR, int(match.group('year')))
        moment.assign(DateTimeComponent.MONTH, int(match.group('month')))
        moment.assign(DateTimeComponent.DAY, int(match.group('day')))

        return moment
