from chrono_python.locales.en import constants
from chrono_python.types import Timeunit


def test_parse_time_units():
    assert constants.parse_time_units('3y') == {Timeunit.YEAR: 3}
    assert constants.parse_time_units('1day') == {Timeunit.DAY: 1}
    assert constants.parse_time_units('45 minutes') == {Timeunit.MINUTE: 45}

    assert constants.parse_time_units('4 hours 23 minutes') == {Timeunit.HOUR: 4, Timeunit.MINUTE: 23}
    assert constants.parse_time_units('23 minutes 4 hours') == {Timeunit.HOUR: 4, Timeunit.MINUTE: 23}


def test_parse_number_pattern():
    assert constants.parse_number_pattern('one') == 1.0
    assert constants.parse_number_pattern('twelve') == 12.0
    assert constants.parse_number_pattern('half') == 0.5
    assert constants.parse_number_pattern('a') == 1.0
    assert constants.parse_number_pattern('few') == 3.0
    assert constants.parse_number_pattern('several') == 7.0
    assert constants.parse_number_pattern('couple') == 2.0
    assert constants.parse_number_pattern('3.5') == 3.5


def test_parse_duration_and_normalization():
    # Decimals and normalization
    assert constants.parse_duration('1.5 years') == {Timeunit.YEAR: 1, Timeunit.MONTH: 6}
    assert constants.parse_duration('1.25 years') == {Timeunit.YEAR: 1, Timeunit.MONTH: 3}
    assert constants.parse_duration('2.5 months') == {Timeunit.MONTH: 2, Timeunit.WEEK: 2}
    assert constants.parse_duration('half an hour') == {Timeunit.MINUTE: 30}
    assert constants.parse_duration('a few days') == {Timeunit.DAY: 3}
    assert constants.parse_duration('several weeks') == {Timeunit.WEEK: 7}
    
    # Quarters
    assert constants.parse_duration('1 quarter') == {Timeunit.MONTH: 3}
    assert constants.parse_duration('2 quarters') == {Timeunit.MONTH: 6}
    
    # Multi-unit
    assert constants.parse_duration('1 year and 3 months') == {Timeunit.YEAR: 1, Timeunit.MONTH: 3}

