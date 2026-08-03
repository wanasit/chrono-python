import datetime
from chrono_python.locales import pt
from chrono_python.common.types import CivilTimeComponent, Meridiem


def test_pt_time_expr_single():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    results = pt.parse("Ficaremos às 6.13 AM", ref_date)
    assert len(results) == 1
    assert results[0].index == 10
    assert results[0].text == "às 6.13 AM"
    assert results[0].moment.get(CivilTimeComponent.HOUR) == 6
    assert results[0].moment.get(CivilTimeComponent.MINUTE) == 13
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10
    assert dt.hour == 6
    assert dt.minute == 13


def test_pt_time_expr_range():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    results = pt.parse("8:10 - 12.32", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "8:10 - 12.32"
    assert results[0].moment.get(CivilTimeComponent.HOUR) == 8
    assert results[0].moment.get(CivilTimeComponent.MINUTE) == 10
    assert not results[0].moment.is_certain(CivilTimeComponent.DAY)
    assert not results[0].moment.is_certain(CivilTimeComponent.MONTH)
    assert not results[0].moment.is_certain(CivilTimeComponent.YEAR)
    assert results[0].moment.is_certain(CivilTimeComponent.HOUR)
    assert results[0].moment.is_certain(CivilTimeComponent.MINUTE)
    assert results[0].end is not None
    assert results[0].end.get(CivilTimeComponent.HOUR) == 12
    assert results[0].end.get(CivilTimeComponent.MINUTE) == 32

    results = pt.parse(" de 6:30pm a 11:00pm ", ref_date)
    assert len(results) == 1
    assert results[0].index == 1
    assert results[0].text == "de 6:30pm a 11:00pm"
    assert results[0].moment.get(CivilTimeComponent.HOUR) == 18
    assert results[0].moment.get(CivilTimeComponent.MINUTE) == 30
    assert results[0].moment.get(CivilTimeComponent.MERIDIEM) == Meridiem.PM
    assert results[0].end is not None
    assert results[0].end.get(CivilTimeComponent.HOUR) == 23
    assert results[0].end.get(CivilTimeComponent.MINUTE) == 0
    assert results[0].end.get(CivilTimeComponent.MERIDIEM) == Meridiem.PM


def test_pt_date_time_expr():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    results = pt.parse("Algo passou em 10 de Agosto de 2012 10:12:59 pm", ref_date)
    assert len(results) == 1
    assert results[0].index == 15
    assert results[0].text == "10 de Agosto de 2012 10:12:59 pm"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10
    assert dt.hour == 22
    assert dt.minute == 12
    assert dt.second == 59


def test_pt_time_expr_meridiem_imply():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    results = pt.parse("de 1pm a 3", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "de 1pm a 3"
    assert results[0].moment.get(CivilTimeComponent.HOUR) == 13
    assert results[0].moment.get(CivilTimeComponent.MINUTE) == 0
    assert results[0].moment.get(CivilTimeComponent.MERIDIEM) == Meridiem.PM
    assert results[0].moment.is_certain(CivilTimeComponent.MERIDIEM)
    assert results[0].end is not None
    assert results[0].end.get(CivilTimeComponent.HOUR) == 15
    assert results[0].end.get(CivilTimeComponent.MINUTE) == 0
    assert results[0].end.is_certain(CivilTimeComponent.MERIDIEM)


def test_pt_random_time_expressions():
    test_cases = [
        "segunda 4/29/2013 630-930am",
        "terça 5/1/2013 1115am",
        "quarta 5/3/2013 1230pm",
        "domingo 5/6/2013  750am-910am",
        "segunda-feira 5/13/2013 630-930am",
        "quarta-feira 5/15/2013 1030am",
        "quinta 6/21/2013 2:30",
        "terça-feira 7/2/2013 1-230 pm",
        "Segunda-feira, 6/24/2013, 7:00pm - 8:30pm",
        "Quarta, 3 Julho de 2013 às 2pm",
        "6pm",
        "6 pm",
        "7-10pm",
        "11.1pm",
        "às 12",
    ]
    for text in test_cases:
        results = pt.parse(text)
        assert len(results) > 0, f"Failed to parse '{text}'"
        assert results[0].text == text, f"Expected '{text}', got '{results[0].text}'"
