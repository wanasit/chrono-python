import datetime
from chrono_python.locales import sv
from chrono_python.common.types import CivilTimeComponent


def test_sv_time_expr_single():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # kl 15:00
    results = sv.parse("kl 15:00", ref_date)
    assert len(results) == 1
    assert results[0].text == "kl 15:00"
    assert results[0].moment.get(CivilTimeComponent.HOUR) == 15
    assert results[0].moment.get(CivilTimeComponent.MINUTE) == 0

    # kl. 8:30
    results = sv.parse("kl. 8:30", ref_date)
    assert len(results) == 1
    assert results[0].text == "kl. 8:30"
    assert results[0].moment.get(CivilTimeComponent.HOUR) == 8
    assert results[0].moment.get(CivilTimeComponent.MINUTE) == 30

    # klockan 20.00
    results = sv.parse("klockan 20.00", ref_date)
    assert len(results) == 1
    assert results[0].text == "klockan 20.00"
    assert results[0].moment.get(CivilTimeComponent.HOUR) == 20
    assert results[0].moment.get(CivilTimeComponent.MINUTE) == 0


def test_sv_time_expr_range():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # kl 13:00 - 15:00
    results = sv.parse("kl 13:00 - 15:00", ref_date)
    assert len(results) == 1
    assert results[0].text == "kl 13:00 - 15:00"
    assert results[0].start.get(CivilTimeComponent.HOUR) == 13
    assert results[0].end.get(CivilTimeComponent.HOUR) == 15
