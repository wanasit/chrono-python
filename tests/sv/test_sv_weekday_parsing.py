import datetime
from chrono_python.locales import sv
from chrono_python.common.types import CivilTimeComponent


def test_sv_weekday_single():
    ref_date = datetime.datetime(2012, 8, 9, 12, 0)  # Thursday

    # måndag
    results = sv.parse("måndag", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "måndag"
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2012
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 8
    assert results[0].moment.get(CivilTimeComponent.DAY) == 6
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 1

    # på måndag
    results = sv.parse("på måndag", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "på måndag"
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2012
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 8
    assert results[0].moment.get(CivilTimeComponent.DAY) == 6
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 1


def test_sv_weekday_relative():
    ref_date = datetime.datetime(2012, 8, 9, 12, 0)  # Thursday

    # nästa måndag
    results = sv.parse("nästa måndag", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "nästa måndag"
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2012
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 8
    assert results[0].moment.get(CivilTimeComponent.DAY) == 13
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 1

    # förra måndag
    results = sv.parse("förra måndag", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "förra måndag"
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2012
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 8
    assert results[0].moment.get(CivilTimeComponent.DAY) == 6
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 1


def test_sv_weekday_variations():
    ref_date = datetime.datetime(2012, 8, 9, 12, 0)

    results = sv.parse("söndag", ref_date)
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 0

    results = sv.parse("tisdag", ref_date)
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 2

    results = sv.parse("fredag", ref_date)
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 5

    results = sv.parse("lördag", ref_date)
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 6
