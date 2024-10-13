import chrono_python as chrono

from chrono_python.types import Moment, DateTimeComponent, DateTimePrecision
from chrono_python.result import ParsingMoment


def test_date_little_endian_full():
    results = chrono.parse('20 January 2012')
    assert len(results) == 1

    assert results[0].text == '20 January 2012'

    assert isinstance(results[0].moment, ParsingMoment)
    assert results[0].moment.get(DateTimeComponent.YEAR) == 2012
    assert results[0].moment.get(DateTimeComponent.MONTH) == 1
    assert results[0].moment.get(DateTimeComponent.DAY) == 20


def test_date_little_endian_abbreviated_month():
    results = chrono.parse('20 Jan 2012')
    assert len(results) == 1

    assert results[0].text == '20 Jan 2012'

    assert isinstance(results[0].moment, ParsingMoment)
    assert results[0].moment.get(DateTimeComponent.YEAR) == 2012
    assert results[0].moment.get(DateTimeComponent.MONTH) == 1
    assert results[0].moment.get(DateTimeComponent.DAY) == 20


def test_date_little_endian_with_ordinal_date():
    results = chrono.parse('20th January 2012')
    assert len(results) == 1

    assert results[0].text == '20th January 2012'

    assert isinstance(results[0].moment, ParsingMoment)
    assert results[0].moment.get(DateTimeComponent.YEAR) == 2012
    assert results[0].moment.get(DateTimeComponent.MONTH) == 1
    assert results[0].moment.get(DateTimeComponent.DAY) == 20


def test_date_little_endian_with_hyphen_punctuation():
    results = chrono.parse('20-Jan-2012')
    assert len(results) == 1

    assert results[0].text == '20-Jan-2012'

    assert isinstance(results[0].moment, ParsingMoment)
    assert results[0].moment.get(DateTimeComponent.YEAR) == 2012
    assert results[0].moment.get(DateTimeComponent.MONTH) == 1
    assert results[0].moment.get(DateTimeComponent.DAY) == 20


def test_date_little_endian_with_comma_punctuation():
    results = chrono.parse('20th Jan, 2012')
    assert len(results) == 1

    assert results[0].text == '20th Jan, 2012'
    assert isinstance(results[0].moment, ParsingMoment)
    assert results[0].moment.get(DateTimeComponent.YEAR) == 2012
    assert results[0].moment.get(DateTimeComponent.MONTH) == 1
    assert results[0].moment.get(DateTimeComponent.DAY) == 20
