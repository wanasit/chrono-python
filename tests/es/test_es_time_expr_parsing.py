import datetime
from chrono_python.locales import es
from chrono_python.common.types import CivilTimeComponent, Meridiem


def test_es_time_expr_meridiem_imply():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = es.parse("de 1pm a 3", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "de 1pm a 3"
    assert results[0].start.get(CivilTimeComponent.HOUR) == 13
    assert results[0].start.get(CivilTimeComponent.MERIDIEM) == Meridiem.PM
    assert results[0].end is not None
    assert results[0].end.get(CivilTimeComponent.HOUR) == 15
    assert results[0].end.get(CivilTimeComponent.MERIDIEM) == Meridiem.PM


def test_es_time_expr_random():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    test_cases = [
        "lunes 4/29/2013 630-930am",
        "martes 5/1/2013 1115am",
        "miércoles 5/3/2013 1230pm",
        "domingo 5/6/2013  750am-910am",
        "lunes 5/13/2013 630-930am",
        "miércoles 5/15/2013 1030am",
        "jueves 6/21/2013 2:30",
        "martes 7/2/2013 1-230 pm",
        "Lunes, 6/24/2013, 7:00pm - 8:30pm",
        "Miércoles, 3 Julio de 2013 a las 2pm",
        "6pm",
        "6 pm",
        "7-10pm",
        "las 12",
    ]

    for text in test_cases:
        results = es.parse(text, ref_date)
        assert len(results) >= 1, f"Failed for text: '{text}'"
        assert results[0].text in text
