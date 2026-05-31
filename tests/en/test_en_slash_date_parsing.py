import datetime
import chrono_python as chrono

from chrono_python.chrono import Configuration, Chrono
from chrono_python.types import DateTimeComponent, Moment
from chrono_python.result import ParsingMoment
from chrono_python.common import parsers as common_parsers


def test_slash_shorten_dd_mm():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = chrono.parse('8/10', ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == '8/10'
    assert result.moment.get(DateTimeComponent.YEAR) == 2012
    assert result.moment.get(DateTimeComponent.MONTH) == 8
    assert result.moment.get(DateTimeComponent.DAY) == 10
    assert result.moment.is_certain(DateTimeComponent.YEAR) is False
    assert result.moment.is_certain(DateTimeComponent.MONTH) is True
    assert result.moment.is_certain(DateTimeComponent.DAY) is True


def test_slash_mm_dd_yyyy():
    results = chrono.parse('8/10/2012')
    assert len(results) == 1
    result = results[0]
    assert result.text == '8/10/2012'
    assert result.moment.get(DateTimeComponent.YEAR) == 2012
    assert result.moment.get(DateTimeComponent.MONTH) == 8
    assert result.moment.get(DateTimeComponent.DAY) == 10
    assert result.moment.is_certain(DateTimeComponent.YEAR) is True
    assert result.moment.is_certain(DateTimeComponent.MONTH) is True
    assert result.moment.is_certain(DateTimeComponent.DAY) is True


def test_slash_dd_mm_yyyy():
    parser = common_parsers.SlashDateFormatParser(little_endian=True)
    config = Configuration(parsers=[parser], refiners=[])
    custom_chrono = Chrono(config)
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = custom_chrono.parse('10/8/2012', ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == '10/8/2012'
    assert result.moment.get(DateTimeComponent.YEAR) == 2012
    assert result.moment.get(DateTimeComponent.MONTH) == 8
    assert result.moment.get(DateTimeComponent.DAY) == 10


def test_slash_swap_month_day():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    # 25/05/2015 parsed as month-first will have month=25 (>12).
    # Since 05 is <= 12 and 25 <= 31, it should swap them to day=25, month=5.
    results = chrono.parse('25/05/2015', ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == '25/05/2015'
    assert result.moment.get(DateTimeComponent.YEAR) == 2015
    assert result.moment.get(DateTimeComponent.MONTH) == 5
    assert result.moment.get(DateTimeComponent.DAY) == 25


def test_slash_two_digit_year():
    # 30-12-16 has month=30, day=12, year=16.
    # Month > 12 triggers swap: month=12, day=30.
    # Year <= 50 triggers find_most_likely_ad_year: 16 -> 2016.
    results = chrono.parse('Friday 30-12-16')
    assert len(results) == 1
    result = results[0]
    assert result.text == '30-12-16'
    assert result.moment.get(DateTimeComponent.YEAR) == 2016
    assert result.moment.get(DateTimeComponent.MONTH) == 12
    assert result.moment.get(DateTimeComponent.DAY) == 30


def test_slash_pattern_yyyy_mm_dd_hyphen():
    results = chrono.parse('2015-05-25')
    assert len(results) == 1
    assert results[0].moment.get(DateTimeComponent.YEAR) == 2015
    assert results[0].moment.get(DateTimeComponent.MONTH) == 5
    assert results[0].moment.get(DateTimeComponent.DAY) == 25


def test_slash_pattern_mm_dd_yyyy_slash():
    results = chrono.parse('05/25/2015')
    assert len(results) == 1
    assert results[0].moment.get(DateTimeComponent.YEAR) == 2015
    assert results[0].moment.get(DateTimeComponent.MONTH) == 5
    assert results[0].moment.get(DateTimeComponent.DAY) == 25


def test_slash_pattern_mm_dd_yyyy_dot():
    results = chrono.parse('05.25.2015')
    assert len(results) == 1
    assert results[0].moment.get(DateTimeComponent.YEAR) == 2015
    assert results[0].moment.get(DateTimeComponent.MONTH) == 5
    assert results[0].moment.get(DateTimeComponent.DAY) == 25


def test_slash_version_numbers_exclusion():
    # '1.12', '1.12.12' should be excluded
    assert len(chrono.parse('Version 1.12')) == 0
    assert len(chrono.parse('Version 1.12.12')) == 0


def test_slash_dot_no_year_exclusion():
    # '12.10' should be excluded because it uses '.' but has no year
    assert len(chrono.parse('12.10')) == 0


def test_slash_extra_chunk():
    # '14/4 90' should match '14/4' as month 4, day 14 (swapped), leaving ' 90' unmatched.
    results = chrono.parse('14/4 90')
    assert len(results) == 1
    result = results[0]
    assert result.text == '14/4'
    assert result.moment.get(DateTimeComponent.MONTH) == 4
    assert result.moment.get(DateTimeComponent.DAY) == 14


def test_slash_invalid_dates():
    assert len(chrono.parse('8/32/2014')) == 0
    assert len(chrono.parse('8/32')) == 0
    assert len(chrono.parse('15/28/2022')) == 0
