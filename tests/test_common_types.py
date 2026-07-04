import datetime
from chrono_python.types import DateTimeMoment, DateTimePrecision
from chrono_python.common.types import ParsingCivilTimeMoment, CivilTimeComponent

def test_parsing_civil_time_moment_datetime_calculation():
    ref_dt = datetime.datetime(2026, 5, 31, 8, 30, 45)
    ref = DateTimeMoment.of(ref_dt, DateTimePrecision.SECOND)
    
    # Test case 1: empty values (should default date to reference date, and time to 12:00:00)
    moment = ParsingCivilTimeMoment(ref, {})
    expected_dt = datetime.datetime(2026, 5, 31, 12, 0, 0)
    assert moment.datetime() == expected_dt
    
    # Test case 2: custom assigned date components
    moment = ParsingCivilTimeMoment(ref, {})
    moment.assign(CivilTimeComponent.YEAR, 2025)
    moment.assign(CivilTimeComponent.MONTH, 12)
    moment.assign(CivilTimeComponent.DAY, 25)
    expected_dt = datetime.datetime(2025, 12, 25, 12, 0, 0)
    assert moment.datetime() == expected_dt
    
    # Test case 3: custom assigned time components
    moment = ParsingCivilTimeMoment(ref, {})
    moment.assign(CivilTimeComponent.HOUR, 16)
    moment.assign(CivilTimeComponent.MINUTE, 45)
    moment.assign(CivilTimeComponent.SECOND, 10)
    expected_dt = datetime.datetime(2026, 5, 31, 16, 45, 10)
    assert moment.datetime() == expected_dt


def test_parsing_civil_time_moment_precision_calculation():
    ref_dt = datetime.datetime(2026, 5, 31, 8, 30, 45)
    ref = DateTimeMoment.of(ref_dt, DateTimePrecision.SECOND)
    
    # Test case 1: empty components (should fallback to reference precision)
    moment = ParsingCivilTimeMoment(ref, {})
    assert moment.precision() == DateTimePrecision.SECOND
    
    # Test case 2: imply month
    moment = ParsingCivilTimeMoment(ref, {})
    moment.imply(CivilTimeComponent.MONTH, 6)
    assert moment.precision() == DateTimePrecision.MONTH
    
    # Test case 3: assign year, month, day (most precise is DAY)
    moment = ParsingCivilTimeMoment(ref, {})
    moment.assign(CivilTimeComponent.YEAR, 2025)
    moment.assign(CivilTimeComponent.MONTH, 12)
    moment.assign(CivilTimeComponent.DAY, 25)
    assert moment.precision() == DateTimePrecision.DAY
    
    # Test case 4: assign time (most precise is MINUTE)
    moment = ParsingCivilTimeMoment(ref, {})
    moment.assign(CivilTimeComponent.HOUR, 16)
    moment.assign(CivilTimeComponent.MINUTE, 45)
    assert moment.precision() == DateTimePrecision.MINUTE


def test_parsing_civil_time_moment_assign_overrides_imply():
    ref_dt = datetime.datetime(2026, 5, 31, 8, 30, 45)
    ref = DateTimeMoment.of(ref_dt, DateTimePrecision.SECOND)
    
    moment = ParsingCivilTimeMoment(ref, {})
    
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
