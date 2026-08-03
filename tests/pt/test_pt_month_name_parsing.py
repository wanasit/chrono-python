import datetime
from chrono_python.locales import pt
from chrono_python.common.types import CivilTimeComponent


def test_pt_month_name_single():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    results = pt.parse("10 Agosto 2012", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "10 Agosto 2012"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10

    results = pt.parse("10 Agosto 234 AC", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "10 Agosto 234 AC"
    assert results[0].moment.get(CivilTimeComponent.YEAR) == -234
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 8
    assert results[0].moment.get(CivilTimeComponent.DAY) == 10

    results = pt.parse("10 Agosto 88 d. C.", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "10 Agosto 88 d. C."
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 88
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 8
    assert results[0].moment.get(CivilTimeComponent.DAY) == 10

    ref_date_2013 = datetime.datetime(2013, 8, 10, 12, 0)
    results = pt.parse("Dom 15Set", ref_date_2013)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "Dom 15Set"
    dt = results[0].moment.datetime()
    assert dt.year == 2013
    assert dt.month == 9
    assert dt.day == 15

    results = pt.parse("DOM 15SET", ref_date_2013)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "DOM 15SET"
    dt = results[0].moment.datetime()
    assert dt.year == 2013
    assert dt.month == 9
    assert dt.day == 15

    results = pt.parse("O prazo é 10 Agosto", ref_date)
    assert len(results) == 1
    assert results[0].index == 10
    assert results[0].text == "10 Agosto"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10

    results = pt.parse("O prazo é terça-feira, 10 de janeiro", ref_date)
    assert len(results) == 1
    assert results[0].index == 10
    assert results[0].text == "terça-feira, 10 de janeiro"
    dt = results[0].moment.datetime()
    assert dt.year == 2013
    assert dt.month == 1
    assert dt.day == 10
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 2

    results = pt.parse("O prazo é Qua, 10 Janeiro", ref_date)
    assert len(results) == 1
    assert results[0].index == 10
    assert results[0].text == "Qua, 10 Janeiro"
    dt = results[0].moment.datetime()
    assert dt.year == 2013
    assert dt.month == 1
    assert dt.day == 10
    assert results[0].moment.get(CivilTimeComponent.WEEKDAY) == 3

    ref_date_2010 = datetime.datetime(2010, 2, 1, 12, 0)
    results = pt.parse("10 de Agosto de 2012", ref_date_2010)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "10 de Agosto de 2012"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10


def test_pt_month_name_range():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    results = pt.parse("10 - 22 Agosto 2012", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "10 - 22 Agosto 2012"
    dt_start = results[0].moment.datetime()
    assert dt_start.year == 2012
    assert dt_start.month == 8
    assert dt_start.day == 10
    assert results[0].end is not None
    dt_end = results[0].end.datetime()
    assert dt_end.year == 2012
    assert dt_end.month == 8
    assert dt_end.day == 22

    results = pt.parse("10 a 22 Agosto 2012", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "10 a 22 Agosto 2012"
    dt_start = results[0].moment.datetime()
    assert dt_start.year == 2012
    assert dt_start.month == 8
    assert dt_start.day == 10
    assert results[0].end is not None
    dt_end = results[0].end.datetime()
    assert dt_end.year == 2012
    assert dt_end.month == 8
    assert dt_end.day == 22

    results = pt.parse("10 Agosto - 12 Setembro", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "10 Agosto - 12 Setembro"
    dt_start = results[0].moment.datetime()
    assert dt_start.year == 2012
    assert dt_start.month == 8
    assert dt_start.day == 10
    assert results[0].end is not None
    dt_end = results[0].end.datetime()
    assert dt_end.year == 2012
    assert dt_end.month == 9
    assert dt_end.day == 12

    results = pt.parse("10 Agosto - 12 Setembro 2013", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "10 Agosto - 12 Setembro 2013"
    dt_start = results[0].moment.datetime()
    assert dt_start.year == 2013
    assert dt_start.month == 8
    assert dt_start.day == 10
    assert results[0].end is not None
    dt_end = results[0].end.datetime()
    assert dt_end.year == 2013
    assert dt_end.month == 9
    assert dt_end.day == 12


def test_pt_month_name_combined():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    results = pt.parse("12 de Julho às 19:00", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "12 de Julho às 19:00"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 7
    assert dt.day == 12
    assert dt.hour == 19
    assert dt.minute == 0


def test_pt_month_name_impossible_strict():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    assert len(pt.strict.parse("32 Agosto 2014", ref_date)) == 0
    assert len(pt.strict.parse("29 Fevereiro 2014", ref_date)) == 0
    assert len(pt.strict.parse("32 Agosto", ref_date)) == 0
