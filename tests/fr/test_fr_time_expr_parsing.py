import datetime
from chrono_python.locales import fr
from chrono_python.common.types import CivilTimeComponent


def test_fr_time_expr_single():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # 8h10
    results = fr.parse("8h10", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "8h10"
    dt = results[0].moment.datetime()
    assert dt.hour == 8
    assert dt.minute == 10
    assert results[0].moment.is_certain(CivilTimeComponent.HOUR)
    assert results[0].moment.is_certain(CivilTimeComponent.MINUTE)
    assert not results[0].moment.is_certain(CivilTimeComponent.SECOND)

    # 8h10m
    results = fr.parse("8h10m", ref_date)
    assert len(results) == 1
    assert results[0].text == "8h10m"
    assert results[0].moment.datetime().hour == 8
    assert results[0].moment.datetime().minute == 10

    # 8h10m00
    results = fr.parse("8h10m00", ref_date)
    assert len(results) == 1
    assert results[0].text == "8h10m00"
    assert results[0].moment.datetime().hour == 8
    assert results[0].moment.datetime().minute == 10
    assert results[0].moment.is_certain(CivilTimeComponent.SECOND)

    # 8h10m00s
    results = fr.parse("8h10m00s", ref_date)
    assert len(results) == 1
    assert results[0].text == "8h10m00s"
    assert results[0].moment.datetime().hour == 8
    assert results[0].moment.datetime().minute == 10
    assert results[0].moment.is_certain(CivilTimeComponent.SECOND)

    # 8:10 PM
    results = fr.parse("8:10 PM", ref_date)
    assert len(results) == 1
    assert results[0].text == "8:10 PM"
    assert results[0].moment.datetime().hour == 20

    # 8h10 PM
    results = fr.parse("8h10 PM", ref_date)
    assert len(results) == 1
    assert results[0].text == "8h10 PM"
    assert results[0].moment.datetime().hour == 20

    # 1230pm
    results = fr.parse("1230pm", ref_date)
    assert len(results) == 1
    assert results[0].text == "1230pm"
    assert results[0].moment.datetime().hour == 12
    assert results[0].moment.datetime().minute == 30

    # 5:16p
    results = fr.parse("5:16p", ref_date)
    assert len(results) == 1
    assert results[0].text == "5:16p"
    assert results[0].moment.datetime().hour == 17

    # 5h16p
    results = fr.parse("5h16p", ref_date)
    assert len(results) == 1
    assert results[0].text == "5h16p"
    assert results[0].moment.datetime().hour == 17

    # 5h16mp
    results = fr.parse("5h16mp", ref_date)
    assert len(results) == 1
    assert results[0].text == "5h16mp"
    assert results[0].moment.datetime().hour == 17

    # RDV à 6.13 AM
    results = fr.parse("RDV à 6.13 AM", ref_date)
    assert len(results) == 1
    assert results[0].index == 4
    assert results[0].text == "à 6.13 AM"
    assert results[0].moment.datetime().hour == 6
    assert results[0].moment.datetime().minute == 13


def test_fr_time_expr_range():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # 13h-15h
    results = fr.parse("13h-15h", ref_date)
    assert len(results) == 1
    assert results[0].text == "13h-15h"
    assert results[0].start.datetime().hour == 13
    assert results[0].end.datetime().hour == 15

    # 13-15h
    results = fr.parse("13-15h", ref_date)
    assert len(results) == 1
    assert results[0].text == "13-15h"
    assert results[0].start.datetime().hour == 13
    assert results[0].end.datetime().hour == 15

    # 1-3pm
    results = fr.parse("1-3pm", ref_date)
    assert len(results) == 1
    assert results[0].text == "1-3pm"
    assert results[0].start.datetime().hour == 13
    assert results[0].end.datetime().hour == 15

    # 11pm-2
    results = fr.parse("11pm-2", ref_date)
    assert len(results) == 1
    assert results[0].text == "11pm-2"
    assert results[0].start.datetime().hour == 23
    assert results[0].end.datetime().hour == 2

    # 8:10 - 12.32
    results = fr.parse("8:10 - 12.32", ref_date)
    assert len(results) == 1
    assert results[0].text == "8:10 - 12.32"
    assert results[0].start.datetime().hour == 8
    assert results[0].start.datetime().minute == 10
    assert results[0].end.datetime().hour == 12
    assert results[0].end.datetime().minute == 32

    # de 6:30pm à 11:00pm
    results = fr.parse(" de 6:30pm à 11:00pm ", ref_date)
    assert len(results) == 1
    assert results[0].start.datetime().hour == 18
    assert results[0].start.datetime().minute == 30
    assert results[0].end.datetime().hour == 23
    assert results[0].end.datetime().minute == 0


def test_fr_time_expr_timezone():
    ref_date = datetime.datetime(2016, 4, 28, 12, 0)

    results = fr.parse("vendredi 2 pm EST", ref_date)
    assert len(results) == 1
    assert results[0].text == "vendredi 2 pm EST"
    assert results[0].start.is_certain(CivilTimeComponent.TIMEZONE_OFFSET)
    assert results[0].start.get(CivilTimeComponent.TIMEZONE_OFFSET) == -300

    results = fr.parse("vendredi 15h CET", datetime.datetime(2016, 2, 28))
    assert len(results) == 1
    assert results[0].text == "vendredi 15h CET"
    assert results[0].start.is_certain(CivilTimeComponent.TIMEZONE_OFFSET)
    assert results[0].start.get(CivilTimeComponent.TIMEZONE_OFFSET) == 60

    results = fr.parse("vendredi 15h cest", datetime.datetime(2016, 2, 28))
    assert len(results) == 1
    assert results[0].text == "vendredi 15h cest"
    assert results[0].start.is_certain(CivilTimeComponent.TIMEZONE_OFFSET)
    assert results[0].start.get(CivilTimeComponent.TIMEZONE_OFFSET) == 120


def test_fr_time_expr_impossible():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    assert len(fr.parse("8:62", ref_date)) == 0
    assert len(fr.parse("25:12", ref_date)) == 0
    assert len(fr.parse("12h12:99s", ref_date)) == 0
    assert len(fr.parse("13.12 PM", ref_date)) == 0
