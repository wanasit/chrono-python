import datetime
import pytest
from chrono_python.common.timezone import (
    to_timezone_offset,
    TIMEZONE_ABBR_MAP,
)

def test_to_timezone_offset_numeric():
    assert to_timezone_offset(540) == 540
    assert to_timezone_offset(-300) == -300
    assert to_timezone_offset(None) is None


def test_to_timezone_offset_unambiguous():
    # JST is GMT+9 => 540 minutes
    assert to_timezone_offset("JST") == 540
    # ACDT is GMT+10.5 => 630 minutes
    assert to_timezone_offset("ACDT") == 630


def test_to_timezone_offset_ambiguous_dst():
    # CET: DST offset +120, non-DST +60
    # dstStart is last Sunday of March at 2 AM.
    # In 2026, last Sunday of March is March 29.
    # So before Mar 29 2AM (e.g. Mar 29 1AM), it is non-DST (60).
    # After Mar 29 2AM (e.g. Mar 29 3AM), it is DST (120).
    dt_before_cet = datetime.datetime(2026, 3, 29, 1, 0)
    dt_after_cet = datetime.datetime(2026, 3, 29, 3, 0)
    assert to_timezone_offset("CET", dt_before_cet) == 60
    assert to_timezone_offset("CET", dt_after_cet) == 120

    # dstEnd is last Sunday of October at 3 AM.
    # In 2026, last Sunday of October is October 25.
    # So before Oct 25 3AM (e.g. Oct 25 2AM), it is DST (120).
    # After Oct 25 3AM (e.g. Oct 25 4AM), it is non-DST (60).
    dt_before_cet_end = datetime.datetime(2026, 10, 25, 2, 0)
    dt_after_cet_end = datetime.datetime(2026, 10, 25, 4, 0)
    assert to_timezone_offset("CET", dt_before_cet_end) == 120
    assert to_timezone_offset("CET", dt_after_cet_end) == 60

    # Without a date context, CET resolution should return None
    assert to_timezone_offset("CET") is None


def test_to_timezone_offset_ambiguous_nth():
    # ET: DST offset -240 (EDT), non-DST -300 (EST)
    # dstStart is 2nd Sunday of March at 2 AM.
    # In 2026, March 1 is Sunday, so 2nd Sunday is March 8.
    dt_before_et = datetime.datetime(2026, 3, 8, 1, 0)
    dt_after_et = datetime.datetime(2026, 3, 8, 3, 0)
    assert to_timezone_offset("ET", dt_before_et) == -300
    assert to_timezone_offset("ET", dt_after_et) == -240


def test_to_timezone_offset_overrides():
    overrides = {
        "CUSTOM_TZ": 42,
        "JST": 999,
    }
    assert to_timezone_offset("CUSTOM_TZ", timezone_overrides=overrides) == 42
    # Overrides should take precedence
    assert to_timezone_offset("JST", timezone_overrides=overrides) == 999


def test_timezone_abbr_map_frozen():
    # Attempting to modify the map should raise a TypeError
    with pytest.raises(TypeError):
        TIMEZONE_ABBR_MAP["JST"] = 123

    # Attempting to modify nested maps should also raise a TypeError
    with pytest.raises(TypeError):
        TIMEZONE_ABBR_MAP["CET"]["timezoneOffsetDuringDst"] = 123
