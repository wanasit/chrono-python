from chrono_python.locales.en import constants
from chrono_python.types import DateTimeComponent


def test_parse_time_units():
    assert constants.parse_time_units('3y') == {DateTimeComponent.YEAR: 3}
    assert constants.parse_time_units('1day') == {DateTimeComponent.DAY: 1}
    assert constants.parse_time_units('45 minutes') == {DateTimeComponent.MINUTE: 45}

    assert constants.parse_time_units('4 hours 23 minutes') == {DateTimeComponent.HOUR: 4, DateTimeComponent.MINUTE: 23}
    assert constants.parse_time_units('23 minutes 4 hours') == {DateTimeComponent.HOUR: 4, DateTimeComponent.MINUTE: 23}
