from chrono_python.locales.en import constants
from chrono_python.types import DateTimeUnit


def test_parse_time_units():
    assert constants.parse_time_units('3y') == {DateTimeUnit.YEAR: 3}
    assert constants.parse_time_units('1day') == {DateTimeUnit.DAY: 1}
    assert constants.parse_time_units('45 minutes') == {DateTimeUnit.MINUTE: 45}

    assert constants.parse_time_units('4 hours 23 minutes') == {DateTimeUnit.HOUR: 4, DateTimeUnit.MINUTE: 23}
    assert constants.parse_time_units('23 minutes 4 hours') == {DateTimeUnit.HOUR: 4, DateTimeUnit.MINUTE: 23}
