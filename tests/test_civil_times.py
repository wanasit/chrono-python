import datetime
import pytest
from dataclasses import FrozenInstanceError

from chrono_python.types import DateTimeMoment, DateTimePrecision
from chrono_python.common.types import CivilTimeMoment, ParsingCivilTimeMoment, CivilTimeComponent, Meridiem


def test_parsing_civil_time_moment_datetime_calculation():
    ref_dt = datetime.datetime(2026, 5, 31, 8, 30, 45)
    ref = DateTimeMoment.of(ref_dt, DateTimePrecision.SECOND)

    # Test case 1: empty values (should default date to reference date, and time to reference time)
    moment = ParsingCivilTimeMoment.of(ref)
    expected_dt = datetime.datetime(2026, 5, 31, 12, 0, 0)
    assert moment.datetime() == expected_dt

    # Test case 2: custom assigned date components
    moment = ParsingCivilTimeMoment.of(ref)
    moment.assign(CivilTimeComponent.YEAR, 2025)
    moment.assign(CivilTimeComponent.MONTH, 12)
    moment.assign(CivilTimeComponent.DAY, 25)
    expected_dt = datetime.datetime(2025, 12, 25, 12, 0, 0)
    assert moment.datetime() == expected_dt

    # Test case 3: custom assigned time components
    moment = ParsingCivilTimeMoment.of(ref)
    moment.assign(CivilTimeComponent.HOUR, 16)
    moment.assign(CivilTimeComponent.MINUTE, 45)
    moment.assign(CivilTimeComponent.SECOND, 10)
    expected_dt = datetime.datetime(2026, 5, 31, 16, 45, 10)
    assert moment.datetime() == expected_dt


def test_parsing_civil_time_moment_precision_calculation():
    ref_dt = datetime.datetime(2026, 5, 31, 8, 30, 45)
    ref = DateTimeMoment.of(ref_dt, DateTimePrecision.SECOND)

    # Test case 1: empty components with fallback precision (should return fallback precision)
    moment = ParsingCivilTimeMoment.of(ref)
    assert moment.precision() == DateTimePrecision.SECOND

    # Test case 2: empty components without precision (should raise ValueError)
    moment = ParsingCivilTimeMoment()
    with pytest.raises(ValueError, match="Cannot determine precision"):
        moment.precision()

    # Test case 3: assign year, month, day (most precise is DAY)
    moment = ParsingCivilTimeMoment.of(ref)
    moment.assign(CivilTimeComponent.YEAR, 2025)
    moment.assign(CivilTimeComponent.MONTH, 12)
    moment.assign(CivilTimeComponent.DAY, 25)
    assert moment.precision() == DateTimePrecision.DAY

    # Test case 4: assign time (most precise is MINUTE)
    moment = ParsingCivilTimeMoment.of(ref)
    moment.assign(CivilTimeComponent.HOUR, 16)
    moment.assign(CivilTimeComponent.MINUTE, 45)
    assert moment.precision() == DateTimePrecision.MINUTE


def test_parsing_civil_time_moment_assign_overrides_imply():
    ref_dt = datetime.datetime(2026, 5, 31, 8, 30, 45)
    ref = DateTimeMoment.of(ref_dt, DateTimePrecision.SECOND)

    moment = ParsingCivilTimeMoment.of(ref)

    # Imply a value
    moment.imply(CivilTimeComponent.YEAR, 2025)
    assert moment.get(CivilTimeComponent.YEAR) == 2025
    assert moment.is_certain(CivilTimeComponent.YEAR) is False

    # Assign the same component (should promote to certain/known)
    moment.assign(CivilTimeComponent.YEAR, 2026)
    assert moment.get(CivilTimeComponent.YEAR) == 2026
    assert moment.is_certain(CivilTimeComponent.YEAR) is True
    # Implied values dict shouldn't have the key anymore
    assert CivilTimeComponent.YEAR not in moment._implied_values


def test_civil_time_objects_creation():
    ref_dt = datetime.datetime(2026, 5, 31, 8, 30, 45, 500000)

    # YEAR precision implies only YEAR
    year_moment = CivilTimeMoment.of(ref_dt, DateTimePrecision.YEAR)
    assert year_moment.get(CivilTimeComponent.YEAR) == 2026
    assert year_moment.get(CivilTimeComponent.MONTH) is None
    assert year_moment.get(CivilTimeComponent.DAY) is None

    # MONTH precision implies YEAR and MONTH
    month_moment = CivilTimeMoment.of(ref_dt, DateTimePrecision.MONTH)
    assert month_moment.get(CivilTimeComponent.YEAR) == 2026
    assert month_moment.get(CivilTimeComponent.MONTH) == 5
    assert month_moment.get(CivilTimeComponent.DAY) is None

    # DAY precision implies YEAR, MONTH, DAY
    day_moment = CivilTimeMoment.of(ref_dt, DateTimePrecision.DAY)
    assert day_moment.get(CivilTimeComponent.YEAR) == 2026
    assert day_moment.get(CivilTimeComponent.MONTH) == 5
    assert day_moment.get(CivilTimeComponent.DAY) == 31
    assert day_moment.get(CivilTimeComponent.HOUR) is None

    # HOUR precision implies date + HOUR + MERIDIEM
    hour_moment = CivilTimeMoment.of(ref_dt, DateTimePrecision.HOUR)
    assert hour_moment.get(CivilTimeComponent.HOUR) == 8
    assert hour_moment.get(CivilTimeComponent.MERIDIEM) == Meridiem.AM
    assert hour_moment.get(CivilTimeComponent.MINUTE) is None

    # MINUTE precision implies date + HOUR + MERIDIEM + MINUTE
    min_moment = CivilTimeMoment.of(ref_dt, DateTimePrecision.MINUTE)
    assert min_moment.get(CivilTimeComponent.HOUR) == 8
    assert min_moment.get(CivilTimeComponent.MINUTE) == 30
    assert min_moment.get(CivilTimeComponent.SECOND) is None

    # SECOND precision implies date + time up to SECOND
    sec_moment = CivilTimeMoment.of(ref_dt, DateTimePrecision.SECOND)
    assert sec_moment.get(CivilTimeComponent.SECOND) == 45
    assert sec_moment.get(CivilTimeComponent.MILLI_SECOND) is None

    # MILLI_SECOND precision implies date + time up to MILLI_SECOND
    ms_moment = CivilTimeMoment.of(ref_dt, DateTimePrecision.MILLI_SECOND)
    assert ms_moment.get(CivilTimeComponent.MILLI_SECOND) == 500

    moment = CivilTimeMoment(known_values={CivilTimeComponent.YEAR: 2026})
    assert moment.get(CivilTimeComponent.YEAR) == 2026

    # Try to set directly
    with pytest.raises((FrozenInstanceError, AttributeError)):
        moment._known_values = {}

    # Check that it returns itself on freeze
    assert moment.freeze() is moment

    # Clone on CivilTimeMoment returns CivilTimeMoment
    cloned = moment.clone()
    assert isinstance(cloned, CivilTimeMoment)
    assert not isinstance(cloned, ParsingCivilTimeMoment)

    # Convert to mutable
    mutable_moment = moment.to_mutable()
    assert isinstance(mutable_moment, ParsingCivilTimeMoment)
    assert mutable_moment.get(CivilTimeComponent.YEAR) == 2026

    # Mutate the mutable one
    mutable_moment.assign(CivilTimeComponent.YEAR, 2027)
    assert mutable_moment.get(CivilTimeComponent.YEAR) == 2027

    # Clone on ParsingCivilTimeMoment returns ParsingCivilTimeMoment
    cloned_mutable = mutable_moment.clone()
    assert isinstance(cloned_mutable, ParsingCivilTimeMoment)

    # Freeze it back
    frozen_moment = mutable_moment.freeze()
    assert isinstance(frozen_moment, CivilTimeMoment)
    assert not isinstance(frozen_moment, ParsingCivilTimeMoment)
    assert frozen_moment.get(CivilTimeComponent.YEAR) == 2027


def test_civil_time_assign_similar_target():
    ref_dt = datetime.datetime(2026, 5, 31, 8, 30, 45)
    ref = DateTimeMoment.of(ref_dt, DateTimePrecision.SECOND)

    moment = ParsingCivilTimeMoment.of(ref)
    target_dt = datetime.datetime(2025, 12, 25, 14, 20, 10, 500000)

    moment.assign_similar_date(target_dt)
    assert moment.get(CivilTimeComponent.YEAR) == 2025
    assert moment.get(CivilTimeComponent.MONTH) == 12
    assert moment.get(CivilTimeComponent.DAY) == 25
    assert moment.is_certain(CivilTimeComponent.YEAR) is True

    moment.assign_similar_time(target_dt)
    assert moment.get(CivilTimeComponent.HOUR) == 14
    assert moment.get(CivilTimeComponent.MINUTE) == 20
    assert moment.get(CivilTimeComponent.SECOND) == 10
    assert moment.get(CivilTimeComponent.MILLI_SECOND) == 500
    assert moment.get(CivilTimeComponent.MERIDIEM) == Meridiem.PM
    assert moment.is_certain(CivilTimeComponent.HOUR) is True


def test_civil_time_imply_similar_target():
    ref_dt = datetime.datetime(2026, 5, 31, 8, 30, 45)
    ref = DateTimeMoment.of(ref_dt, DateTimePrecision.SECOND)

    moment = ParsingCivilTimeMoment.of(ref)
    target_dt = datetime.datetime(2025, 12, 25, 14, 20, 10, 500000)

    moment.imply_similar_date(target_dt)
    assert moment.get(CivilTimeComponent.YEAR) == 2025
    assert moment.get(CivilTimeComponent.MONTH) == 12
    assert moment.get(CivilTimeComponent.DAY) == 25
    assert moment.is_certain(CivilTimeComponent.YEAR) is False

    moment.imply_similar_time(target_dt)
    assert moment.get(CivilTimeComponent.HOUR) == 14
    assert moment.get(CivilTimeComponent.MINUTE) == 20
    assert moment.get(CivilTimeComponent.SECOND) == 10
    assert moment.get(CivilTimeComponent.MILLI_SECOND) == 500
    assert moment.get(CivilTimeComponent.MERIDIEM) == Meridiem.PM
    assert moment.is_certain(CivilTimeComponent.HOUR) is False


def test_civil_time_similar_precision_target():
    ref_dt = datetime.datetime(2026, 5, 31, 8, 30, 45)
    ref = DateTimeMoment.of(ref_dt, DateTimePrecision.SECOND)

    moment = ParsingCivilTimeMoment.of(ref)

    # Create target with MINUTE precision (only HOUR and MINUTE are known)
    target_moment = ParsingCivilTimeMoment.of(ref)
    target_moment.assign(CivilTimeComponent.HOUR, 10)
    target_moment.assign(CivilTimeComponent.MINUTE, 30)
    assert target_moment.precision() == DateTimePrecision.MINUTE

    moment.assign_similar_time(target_moment)
    assert moment.get(CivilTimeComponent.HOUR) == 10
    assert moment.get(CivilTimeComponent.MINUTE) == 30
    assert moment.get(CivilTimeComponent.SECOND) is None


def test_civil_time_delete_components():
    ref_dt = datetime.datetime(2026, 5, 31, 8, 30, 45)
    ref = DateTimeMoment.of(ref_dt, DateTimePrecision.SECOND)

    moment = ParsingCivilTimeMoment.of(ref)
    moment.assign(CivilTimeComponent.YEAR, 2025)
    assert moment.get(CivilTimeComponent.YEAR) == 2025

    moment.delete(CivilTimeComponent.YEAR)
    assert moment.get(CivilTimeComponent.YEAR) is None
