import chrono_python as chrono

from chrono_python.types import Moment, DateTimeComponent, DateTimePrecision
from chrono_python.result import ParsingMoment


def test_simple_date_little_endian():
    result = chrono.parse('20 January 2012')
    assert len(result) == 1

    assert result[0].text == '20 January 2012'

    assert isinstance(result[0].moment, ParsingMoment)
    assert result[0].moment.get(DateTimeComponent.YEAR) == 2012
    assert result[0].moment.get(DateTimeComponent.MONTH) == 1
    assert result[0].moment.get(DateTimeComponent.DAY) == 20
