from chrono_python.locales.en import constants
from chrono_python.types import Timeunit


def test_parse_time_units():
    assert constants.parse_time_units('3y') == {Timeunit.YEAR: 3}
    assert constants.parse_time_units('1day') == {Timeunit.DAY: 1}
    assert constants.parse_time_units('45 minutes') == {Timeunit.MINUTE: 45}

    assert constants.parse_time_units('4 hours 23 minutes') == {Timeunit.HOUR: 4, Timeunit.MINUTE: 23}
    assert constants.parse_time_units('23 minutes 4 hours') == {Timeunit.HOUR: 4, Timeunit.MINUTE: 23}
