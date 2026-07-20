import datetime
import chrono_python as chrono
from chrono_python.types import DateTimeMoment, ReferenceMoment
from chrono_python.common.types import CivilTimeComponent

def test_timezone_offset_parsing():
    ref = datetime.datetime(2026, 7, 19, 12, 0)

    # Positive offset without colon
    result = chrono.en.parse("2026-07-19 GMT+0900", reference=ref)
    assert len(result) == 1
    assert result[0].text == "2026-07-19 GMT+0900"
    assert isinstance(result[0].moment, DateTimeMoment)
    assert result[0].moment.get(CivilTimeComponent.TIMEZONE_OFFSET) == 540

    # Negative offset with colon and parentheses
    result = chrono.en.parse("2026-07-19 (GMT-05:30)", reference=ref)
    assert len(result) == 1
    assert result[0].text == "2026-07-19 (GMT-05:30)"
    assert result[0].moment.get(CivilTimeComponent.TIMEZONE_OFFSET) == -330

    # UTC offset
    result = chrono.en.parse("2026-07-19 UTC+00:00", reference=ref)
    assert len(result) == 1
    assert result[0].text == "2026-07-19 UTC+00:00"
    assert result[0].moment.get(CivilTimeComponent.TIMEZONE_OFFSET) == 0


def test_timezone_abbr_parsing():
    ref = datetime.datetime(2026, 7, 19, 12, 0)

    # JST abbreviation
    result = chrono.en.parse("11:00 AM JST", reference=ref)
    assert len(result) == 1
    assert result[0].text == "11:00 AM JST"
    assert result[0].moment.get(CivilTimeComponent.TIMEZONE_OFFSET) == 540

    # EST abbreviation (winter)
    ref_winter = datetime.datetime(2026, 12, 19, 12, 0)
    result = chrono.en.parse("11:00 AM EST", reference=ref_winter)
    assert len(result) == 1
    assert result[0].text == "11:00 AM EST"
    # EST is non-DST for ET => -300
    assert result[0].moment.get(CivilTimeComponent.TIMEZONE_OFFSET) == -300

    # EDT abbreviation (summer)
    ref_summer = datetime.datetime(2026, 7, 19, 12, 0)
    result = chrono.en.parse("11:00 AM EDT", reference=ref_summer)
    assert len(result) == 1
    assert result[0].text == "11:00 AM EDT"
    # EDT is DST for ET => -240
    assert result[0].moment.get(CivilTimeComponent.TIMEZONE_OFFSET) == -240


def test_timezone_offset_and_abbr_combination():
    ref = datetime.datetime(2026, 7, 19, 12, 0)

    result = chrono.en.parse("11 am GMT+0900 (JST)", reference=ref)
    assert len(result) == 1
    assert result[0].text == "11 am GMT+0900 (JST)"
    assert result[0].moment.get(CivilTimeComponent.TIMEZONE_OFFSET) == 540


def test_timezone_not_applied_to_reference_moment():
    ref = datetime.datetime(2026, 7, 19, 12, 0)

    # "2 hours ago" is parsed as a ReferenceMoment.
    # The refiners should ignore JST and GMT+0900 because they are not CivilTimeMoments.
    result = chrono.en.parse("2 hours ago JST", reference=ref)
    assert len(result) == 1
    # JST is NOT appended to the text, meaning it was ignored
    assert result[0].text == "2 hours ago"
    assert isinstance(result[0].moment, ReferenceMoment)

    result = chrono.en.parse("2 hours ago GMT+0900", reference=ref)
    assert len(result) == 1
    assert result[0].text == "2 hours ago"
    assert isinstance(result[0].moment, ReferenceMoment)
