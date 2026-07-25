import re

from chrono_python import chrono
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent

# ISO 8601
# - YYYY-MM-DD
# - YYYY-MM-DDThh:mmTZD
# - YYYY-MM-DDThh:mm:ssTZD
# - YYYY-MM-DDThh:mm:ss.sTZD
# - TZD = (Z or +hh:mm or -hh:mm)
PATTERN = re.compile(
    r'([0-9]{4})\-([0-9]{1,2})\-([0-9]{1,2})'
    r'(?:T'
        r'([0-9]{1,2}):([0-9]{1,2})'
        r'(?:'
            r':([0-9]{1,2})(?:\.(\d{1,4}))?'
        r')?'
        r'('
            r'Z|([+-]\d{2}):?(\d{2})?'
        r')?'
    r')?'
    r'(?=\W|$)',
    re.IGNORECASE
)


class ISOFormatParser(chrono.Parser):
    def pattern(self) -> re.Pattern:
        return PATTERN

    def extract(self, context: chrono.ParsingContext, match: chrono.Match) -> ParsingCivilTimeMoment | None:
        components = ParsingCivilTimeMoment(context.reference, {})
        components.assign(CivilTimeComponent.YEAR, int(match.group(1)))
        components.assign(CivilTimeComponent.MONTH, int(match.group(2)))
        components.assign(CivilTimeComponent.DAY, int(match.group(3)))

        if match.group(4) is not None:
            components.assign(CivilTimeComponent.HOUR, int(match.group(4)))
            components.assign(CivilTimeComponent.MINUTE, int(match.group(5)))

            if match.group(6) is not None:
                components.assign(CivilTimeComponent.SECOND, int(match.group(6)))

            if match.group(7) is not None:
                # Milliseconds can be 1-4 digits in the pattern. Pad/truncate to 3 digits.
                ms_str = match.group(7)[:3].ljust(3, '0')
                components.assign(CivilTimeComponent.MILLI_SECOND, int(ms_str))

            if match.group(8) is not None:
                tzd = match.group(8)
                if tzd.upper() == 'Z':
                    offset = 0
                else:
                    hour_offset = int(match.group(9))
                    minute_offset = int(match.group(10)) if match.group(10) is not None else 0
                    
                    offset = hour_offset * 60
                    if offset < 0:
                        offset -= minute_offset
                    else:
                        offset += minute_offset
                components.assign(CivilTimeComponent.TIMEZONE_OFFSET, offset)

        return components
