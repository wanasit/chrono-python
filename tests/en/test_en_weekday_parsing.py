import chrono_python as chrono
import datetime

from chrono_python.types import DateTimePrecision, DateTimeMoment
from chrono_python.common.types import CivilTimeComponent


def test_single_expression():
    ref_date = datetime.datetime(2012, 8, 9, 12, 0)
    
    # Monday
    results = chrono.parse('Monday', ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == 'Monday'
    assert isinstance(results[0].moment, DateTimeMoment)
    assert results[0].moment.datetime() == datetime.datetime(2012, 8, 6, 12, 0)
    assert results[0].moment.precision() == DateTimePrecision.DAY
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2012
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 8
    assert results[0].moment.get(CivilTimeComponent.DAY) == 6
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 1
    assert not results[0].moment.is_certain(CivilTimeComponent.DAY)
    assert not results[0].moment.is_certain(CivilTimeComponent.MONTH)
    assert not results[0].moment.is_certain(CivilTimeComponent.YEAR)
    assert results[0].moment.is_certain(CivilTimeComponent.WEEKDAY)

    # Thursday
    results = chrono.parse('Thursday', ref_date)
    assert len(results) == 1
    assert results[0].text == 'Thursday'
    assert results[0].moment.datetime() == datetime.datetime(2012, 8, 9, 12, 0)
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 4

    # Sunday
    results = chrono.parse('Sunday', ref_date)
    assert len(results) == 1
    assert results[0].text == 'Sunday'
    assert results[0].moment.datetime() == datetime.datetime(2012, 8, 12, 12, 0)
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 0

    # last Friday
    results = chrono.parse('The Deadline is last Friday...', ref_date)
    assert len(results) == 1
    assert results[0].index == 16
    assert results[0].text == 'last Friday'
    assert results[0].moment.datetime() == datetime.datetime(2012, 8, 3, 12, 0)
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 5

    # past Friday
    results = chrono.parse('The Deadline is past Friday...', ref_date)
    assert len(results) == 1
    assert results[0].index == 16
    assert results[0].text == 'past Friday'
    assert results[0].moment.datetime() == datetime.datetime(2012, 8, 3, 12, 0)
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 5

    # on Friday next week
    ref_date_2 = datetime.datetime(2015, 4, 18, 12, 0)
    results = chrono.parse("Let's have a meeting on Friday next week", ref_date_2)
    assert len(results) == 1
    assert results[0].index == 21
    assert results[0].text == 'on Friday next week'
    assert results[0].moment.datetime() == datetime.datetime(2015, 4, 24, 12, 0)
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 5

    # on Tuesday, next week
    results = chrono.parse('I plan on taking the day off on Tuesday, next week', ref_date_2)
    assert len(results) == 1
    assert results[0].index == 29
    assert results[0].text == 'on Tuesday, next week'
    assert results[0].moment.datetime() == datetime.datetime(2015, 4, 21, 12, 0)
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 2


def test_weekday_casual_this_guessing():
    ref_date = datetime.datetime(2022, 8, 2, 12, 0)  # Tue Aug 2 2022
    
    assert chrono.parse('This Saturday', ref_date)[0].moment.datetime() == datetime.datetime(2022, 8, 6, 12, 0)
    assert chrono.parse('This Sunday', ref_date)[0].moment.datetime() == datetime.datetime(2022, 8, 7, 12, 0)
    assert chrono.parse('This Wednesday', ref_date)[0].moment.datetime() == datetime.datetime(2022, 8, 3, 12, 0)

    ref_date_sun = datetime.datetime(2022, 8, 7, 12, 0)  # Sun Aug 7 2022
    assert chrono.parse('This Saturday', ref_date_sun)[0].moment.datetime() == datetime.datetime(2022, 8, 13, 12, 0)
    assert chrono.parse('This Sunday', ref_date_sun)[0].moment.datetime() == datetime.datetime(2022, 8, 7, 12, 0)
    assert chrono.parse('This Wednesday', ref_date_sun)[0].moment.datetime() == datetime.datetime(2022, 8, 10, 12, 0)


def test_weekday_casual_last_guessing():
    ref_date = datetime.datetime(2022, 8, 2, 12, 0)  # Tue Aug 2 2022
    assert chrono.parse('Last Saturday', ref_date)[0].moment.datetime() == datetime.datetime(2022, 7, 30, 12, 0)
    assert chrono.parse('Last Sunday', ref_date)[0].moment.datetime() == datetime.datetime(2022, 7, 31, 12, 0)
    assert chrono.parse('Last Wednesday', ref_date)[0].moment.datetime() == datetime.datetime(2022, 7, 27, 12, 0)


def test_weekday_casual_next_guessing():
    # Ref Tue Aug 2 2022
    ref_date_tue = datetime.datetime(2022, 8, 2, 12, 0)
    assert chrono.parse('Next Saturday', ref_date_tue)[0].moment.datetime() == datetime.datetime(2022, 8, 13, 12, 0)
    assert chrono.parse('Next Sunday', ref_date_tue)[0].moment.datetime() == datetime.datetime(2022, 8, 14, 12, 0)
    assert chrono.parse('Next Wednesday', ref_date_tue)[0].moment.datetime() == datetime.datetime(2022, 8, 10, 12, 0)

    # Ref Sat Aug 6 2022
    ref_date_sat = datetime.datetime(2022, 8, 6, 12, 0)
    assert chrono.parse('Next Saturday', ref_date_sat)[0].moment.datetime() == datetime.datetime(2022, 8, 13, 12, 0)
    assert chrono.parse('Next Sunday', ref_date_sat)[0].moment.datetime() == datetime.datetime(2022, 8, 14, 12, 0)
    assert chrono.parse('Next Wednesday', ref_date_sat)[0].moment.datetime() == datetime.datetime(2022, 8, 10, 12, 0)

    # Ref Sun Aug 7 2022
    ref_date_sun = datetime.datetime(2022, 8, 7, 12, 0)
    assert chrono.parse('Next Saturday', ref_date_sun)[0].moment.datetime() == datetime.datetime(2022, 8, 13, 12, 0)
    assert chrono.parse('Next Sunday', ref_date_sun)[0].moment.datetime() == datetime.datetime(2022, 8, 14, 12, 0)
    assert chrono.parse('Next Wednesday', ref_date_sun)[0].moment.datetime() == datetime.datetime(2022, 8, 10, 12, 0)


def test_casual_weekend_and_weekday():
    ref_date_fri = datetime.datetime(2024, 10, 18, 12, 0)  # Friday
    assert chrono.parse('last weekend', ref_date_fri)[0].moment.datetime() == datetime.datetime(2024, 10, 13, 12, 0)  # Sunday
    assert chrono.parse('this weekend', ref_date_fri)[0].moment.datetime() == datetime.datetime(2024, 10, 19, 12, 0)  # Saturday
    assert chrono.parse('next weekend', ref_date_fri)[0].moment.datetime() == datetime.datetime(2024, 10, 26, 12, 0)  # Saturday

    # Casual weekday
    assert chrono.parse('last weekday', ref_date_fri)[0].moment.datetime() == datetime.datetime(2024, 10, 17, 12, 0)  # Thursday
    assert chrono.parse('next weekday', ref_date_fri)[0].moment.datetime() == datetime.datetime(2024, 10, 21, 12, 0)  # Monday

    ref_date_sat = datetime.datetime(2024, 10, 19, 12, 0)  # Saturday
    assert chrono.parse('last weekday', ref_date_sat)[0].moment.datetime() == datetime.datetime(2024, 10, 18, 12, 0)  # Friday
    assert chrono.parse('next weekday', ref_date_sat)[0].moment.datetime() == datetime.datetime(2024, 10, 21, 12, 0)  # Monday


def test_weekday_with_casual_time():
    ref_date = datetime.datetime(2015, 4, 18, 12, 0)
    results = chrono.parse('Lets meet on Tuesday morning', ref_date)
    assert len(results) == 1
    assert results[0].index == 10
    assert results[0].text == 'on Tuesday morning'
    assert results[0].moment.datetime() == datetime.datetime(2015, 4, 21, 6, 0)
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 2
    assert results[0].moment.get(CivilTimeComponent.HOUR) == 6
    assert results[0].moment.precision() == DateTimePrecision.DAY
    assert not results[0].moment.is_certain(CivilTimeComponent.HOUR)
    assert results[0].moment.is_certain(CivilTimeComponent.MERIDIEM)


def test_weekday_overlap():
    ref_date = datetime.datetime(2012, 8, 9, 12, 0)
    results = chrono.parse('Sunday, December 7, 2014', ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == 'Sunday, December 7, 2014'
    assert results[0].moment.datetime() == datetime.datetime(2014, 12, 7, 12, 0)
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 0
    assert results[0].moment.is_certain(CivilTimeComponent.DAY)
    assert results[0].moment.is_certain(CivilTimeComponent.MONTH)
    assert results[0].moment.is_certain(CivilTimeComponent.YEAR)
    assert results[0].moment.is_certain(CivilTimeComponent.WEEKDAY)

    results = chrono.parse('Sunday 12/7/2014', ref_date)
    assert len(results) == 1
    assert results[0].text == 'Sunday 12/7/2014'
    assert results[0].moment.datetime() == datetime.datetime(2014, 12, 7, 12, 0)

    results = chrono.parse('Friday 30-12-16', ref_date)
    assert len(results) == 1
    assert results[0].text == 'Friday 30-12-16'
    assert results[0].moment.datetime() == datetime.datetime(2016, 12, 30, 12, 0)
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 5


def test_weekday_range():
    ref_date = datetime.datetime(2023, 4, 9, 12, 0)  # Sunday
    
    results = chrono.parse('Friday to Monday', ref_date)
    assert len(results) == 1
    assert results[0].moment.datetime() == datetime.datetime(2023, 4, 7, 12, 0)
    assert results[0].end.datetime() == datetime.datetime(2023, 4, 10, 12, 0)

    results = chrono.parse('Monday to Friday', ref_date)
    assert len(results) == 1
    assert results[0].moment.datetime() == datetime.datetime(2023, 4, 10, 12, 0)
    assert results[0].end.datetime() == datetime.datetime(2023, 4, 14, 12, 0)


def test_weekday_of_week_connector():
    ref_date = datetime.datetime(2022, 8, 2, 12, 0)  # Tuesday Aug 2

    # Tuesday of next week
    results = chrono.parse('Tuesday of next week', ref_date)
    assert len(results) == 1
    assert results[0].text == 'Tuesday of next week'
    assert results[0].moment.datetime() == datetime.datetime(2022, 8, 9, 12, 0)

    # Friday of next week
    results = chrono.parse('Friday of next week', ref_date)
    assert len(results) == 1
    assert results[0].moment.datetime() == datetime.datetime(2022, 8, 12, 12, 0)

    # Monday of next week
    results = chrono.parse('Monday of next week', ref_date)
    assert len(results) == 1
    assert results[0].moment.datetime() == datetime.datetime(2022, 8, 8, 12, 0)

    # Tuesday of last week
    results = chrono.parse('Tuesday of last week', ref_date)
    assert len(results) == 1
    assert results[0].moment.datetime() == datetime.datetime(2022, 7, 26, 12, 0)

    # Friday of last week
    results = chrono.parse('Friday of last week', ref_date)
    assert len(results) == 1
    assert results[0].moment.datetime() == datetime.datetime(2022, 7, 29, 12, 0)

    # Wednesday of this week
    results = chrono.parse('Wednesday of this week', ref_date)
    assert len(results) == 1
    assert results[0].moment.datetime() == datetime.datetime(2022, 8, 3, 12, 0)

    # Tuesday of this week
    results = chrono.parse('Tuesday of this week', ref_date)
    assert len(results) == 1
    assert results[0].moment.datetime() == datetime.datetime(2022, 8, 2, 12, 0)

    # Tuesday of next week after 2pm
    results = chrono.parse('Tuesday of next week after 2pm', ref_date)
    assert len(results) == 1
    assert results[0].moment.datetime() == datetime.datetime(2022, 8, 9, 14, 0)

    # Friday of next week at 9am
    results = chrono.parse('Friday of next week at 9am', ref_date)
    assert len(results) == 1
    assert results[0].moment.datetime() == datetime.datetime(2022, 8, 12, 9, 0)

    # Let's sync on Tuesday of next week
    results = chrono.parse("Let's sync on Tuesday of next week", ref_date)
    assert len(results) == 1
    assert results[0].text == 'on Tuesday of next week'
    assert results[0].moment.datetime() == datetime.datetime(2022, 8, 9, 12, 0)
