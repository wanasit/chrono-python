import chrono_python as chrono
import datetime

from chrono_python.types import Moment, DateTimePrecision, DateTimeMoment
from chrono_python.common.types import CivilTimeComponent


def test_date_little_endian_full():
    results = chrono.parse('20 January 2012')
    assert len(results) == 1

    assert results[0].text == '20 January 2012'

    assert isinstance(results[0].moment, DateTimeMoment)
    assert results[0].moment.datetime() == datetime.datetime(2012, 1, 20, 12, 0)
    assert results[0].moment.precision() == DateTimePrecision.DAY
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2012
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 1
    assert results[0].moment.get(CivilTimeComponent.DAY) == 20



def test_date_little_endian_abbreviated_month():
    results = chrono.parse('20 Jan 2012')
    assert len(results) == 1

    assert results[0].text == '20 Jan 2012'

    assert isinstance(results[0].moment, DateTimeMoment)
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2012
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 1
    assert results[0].moment.get(CivilTimeComponent.DAY) == 20


def test_date_little_endian_with_ordinal_date():
    results = chrono.parse('20th January 2012')
    assert len(results) == 1

    assert results[0].text == '20th January 2012'

    assert isinstance(results[0].moment, DateTimeMoment)
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2012
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 1
    assert results[0].moment.get(CivilTimeComponent.DAY) == 20


def test_date_little_endian_with_hyphen_punctuation():
    results = chrono.parse('20-Jan-2012')
    assert len(results) == 1

    assert results[0].text == '20-Jan-2012'

    assert isinstance(results[0].moment, DateTimeMoment)
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2012
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 1
    assert results[0].moment.get(CivilTimeComponent.DAY) == 20


def test_date_little_endian_with_comma_punctuation():
    results = chrono.parse('20th Jan, 2012')
    assert len(results) == 1

    assert results[0].text == '20th Jan, 2012'
    assert isinstance(results[0].moment, DateTimeMoment)
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2012
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 1
    assert results[0].moment.get(CivilTimeComponent.DAY) == 20


def test_date_middle_endian_full():
    results = chrono.parse('January 20, 2012')
    assert len(results) == 1
    assert results[0].text == 'January 20, 2012'
    moment = results[0].moment
    assert isinstance(moment, DateTimeMoment)
    assert moment.get(CivilTimeComponent.YEAR) == 2012
    assert moment.get(CivilTimeComponent.MONTH) == 1
    assert moment.get(CivilTimeComponent.DAY) == 20


def test_date_middle_endian_abbreviated_month():
    results = chrono.parse('Jan 20, 2012')
    assert len(results) == 1
    assert results[0].text == 'Jan 20, 2012'
    moment = results[0].moment
    assert isinstance(moment, DateTimeMoment)
    assert moment.get(CivilTimeComponent.YEAR) == 2012
    assert moment.get(CivilTimeComponent.MONTH) == 1
    assert moment.get(CivilTimeComponent.DAY) == 20


def test_date_middle_endian_with_ordinal_date():
    results = chrono.parse('January 20th, 2012')
    assert len(results) == 1
    assert results[0].text == 'January 20th, 2012'
    moment = results[0].moment
    assert isinstance(moment, DateTimeMoment)
    assert moment.get(CivilTimeComponent.YEAR) == 2012
    assert moment.get(CivilTimeComponent.MONTH) == 1
    assert moment.get(CivilTimeComponent.DAY) == 20


def test_date_middle_endian_with_hyphen_punctuation_day_year():
    results = chrono.parse('Jan-20-2012')
    assert len(results) == 1
    assert results[0].text == 'Jan-20-2012'
    moment = results[0].moment
    assert isinstance(moment, DateTimeMoment)
    assert moment.get(CivilTimeComponent.YEAR) == 2012
    assert moment.get(CivilTimeComponent.MONTH) == 1
    assert moment.get(CivilTimeComponent.DAY) == 20


def test_date_middle_endian_with_slash_punctuation_day_year():
    results = chrono.parse('Jan/20/2012')
    assert len(results) == 1
    assert results[0].text == 'Jan/20/2012'
    moment = results[0].moment
    assert isinstance(moment, DateTimeMoment)
    assert moment.get(CivilTimeComponent.YEAR) == 2012
    assert moment.get(CivilTimeComponent.MONTH) == 1
    assert moment.get(CivilTimeComponent.DAY) == 20


def test_date_middle_endian_no_year():
    # Assuming current year is implied. Test with a fixed reference date.
    ref_date = datetime.datetime(2023, 1, 1, 12, 0, 0)
    results = chrono.parse('February 10th', ref_date)
    assert len(results) == 1
    assert results[0].text == 'February 10th'
    moment = results[0].moment
    assert isinstance(moment, DateTimeMoment)
    assert moment.is_certain(CivilTimeComponent.YEAR) is False  # Year is implied
    assert moment.get(CivilTimeComponent.YEAR) == 2023  # Closest year to ref_date
    assert moment.get(CivilTimeComponent.MONTH) == 2
    assert moment.get(CivilTimeComponent.DAY) == 10


def test_date_middle_endian_no_year_past_date_implies_next_year():
    # Test that "Dec 25" when today is "Dec 30" implies next year's Dec 25
    ref_date = datetime.datetime(2023, 12, 30, 12, 0, 0)
    results = chrono.parse('December 25', ref_date)

    assert len(results) == 1
    assert results[0].text == 'December 25'

    moment = results[0].moment
    assert isinstance(moment, DateTimeMoment)
    assert moment.is_certain(CivilTimeComponent.YEAR) is False
    assert moment.get(CivilTimeComponent.YEAR) == 2023
    assert moment.get(CivilTimeComponent.MONTH) == 12
    assert moment.get(CivilTimeComponent.DAY) == 25


def test_date_middle_endian_no_year_future_date_implies_current_year():
    # Test that "Jan 5" when today is "Jan 1" implies current year's Jan 5
    ref_date = datetime.datetime(2023, 1, 1, 12, 0, 0)
    results = chrono.parse('January 5', ref_date)
    assert len(results) == 1
    assert results[0].text == 'January 5'
    moment = results[0].moment
    assert isinstance(moment, DateTimeMoment)
    assert moment.is_certain(CivilTimeComponent.YEAR) is False
    assert moment.get(CivilTimeComponent.YEAR) == 2023  # Should be current year
    assert moment.get(CivilTimeComponent.MONTH) == 1
    assert moment.get(CivilTimeComponent.DAY) == 5


def test_date_middle_endian_no_punctuation_between_month_day():
    results = chrono.parse('Sep15 2022')
    assert len(results) == 1
    assert results[0].text == 'Sep15 2022'
    moment = results[0].moment
    assert isinstance(moment, DateTimeMoment)
    assert moment.get(CivilTimeComponent.YEAR) == 2022
    assert moment.get(CivilTimeComponent.MONTH) == 9
    assert moment.get(CivilTimeComponent.DAY) == 15


def test_date_middle_endian_range():
    results = chrono.parse('March 10th - 12th, 2023')
    assert len(results) == 1
    assert results[0].text == 'March 10th - 12th, 2023'

    start_moment = results[0].moment
    end_moment = results[0].end
    assert isinstance(start_moment, DateTimeMoment)
    assert isinstance(end_moment, DateTimeMoment)

    assert start_moment.get(CivilTimeComponent.YEAR) == 2023
    assert start_moment.get(CivilTimeComponent.MONTH) == 3
    assert start_moment.get(CivilTimeComponent.DAY) == 10

    assert end_moment.get(CivilTimeComponent.YEAR) == 2023
    assert end_moment.get(CivilTimeComponent.MONTH) == 3
    assert end_moment.get(CivilTimeComponent.DAY) == 12


def test_month_name_before_year():
    # January, 2012
    results = chrono.parse('January, 2012')
    assert len(results) == 1
    assert results[0].text == 'January, 2012'
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2012
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 1
    assert results[0].moment.get(CivilTimeComponent.DAY) == 1
    assert results[0].moment.is_certain(CivilTimeComponent.DAY) is False
    assert results[0].moment.precision() == DateTimePrecision.MONTH

    # January 2012
    results = chrono.parse('January 2012')
    assert len(results) == 1
    assert results[0].text == 'January 2012'
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2012
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 1
    assert results[0].moment.get(CivilTimeComponent.DAY) == 1
    assert results[0].moment.precision() == DateTimePrecision.MONTH

    # in Jan
    ref_date = datetime.datetime(2023, 5, 1, 12, 0, 0)
    results = chrono.parse('in Jan', ref_date)
    assert len(results) == 1
    assert results[0].text == 'Jan'
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 1
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2023
    assert results[0].moment.precision() == DateTimePrecision.MONTH


def test_month_name_after_year():
    # 2012 January
    results = chrono.parse('2012 January')
    assert len(results) == 1
    assert results[0].text == '2012 January'
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2012
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 1
    assert results[0].moment.get(CivilTimeComponent.DAY) == 1
    assert results[0].moment.is_certain(CivilTimeComponent.DAY) is False
    assert results[0].moment.precision() == DateTimePrecision.MONTH

    # 2012 of January
    results = chrono.parse('2012 of January')
    assert len(results) == 1
    assert results[0].text == '2012 of January'
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2012
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 1
    assert results[0].moment.precision() == DateTimePrecision.MONTH
