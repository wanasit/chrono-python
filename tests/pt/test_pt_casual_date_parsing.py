import datetime
from chrono_python.locales import pt


def test_pt_casual_date():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # hoje
    results = pt.parse("La deadline é hoje", ref_date)
    assert len(results) == 1
    assert results[0].index == 14
    assert results[0].text == "hoje"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10

    # amanha
    results = pt.parse("La deadline é amanha", ref_date)
    assert len(results) == 1
    assert results[0].index == 14
    assert results[0].text == "amanha"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 11

    # amanhã
    results = pt.parse("La deadline é amanhã", ref_date)
    assert len(results) == 1
    assert results[0].index == 14
    assert results[0].text == "amanhã"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 11

    # ontem
    results = pt.parse("La deadline foi ontem", ref_date)
    assert len(results) == 1
    assert results[0].index == 16
    assert results[0].text == "ontem"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 9


def test_pt_casual_time():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # esta tarde
    results = pt.parse("esta tarde", ref_date)
    assert len(results) == 1
    assert results[0].text == "esta tarde"
    dt = results[0].moment.datetime()
    assert dt.hour == 15

    # esta noite
    results = pt.parse("esta noite", ref_date)
    assert len(results) == 1
    assert results[0].text == "esta noite"
    dt = results[0].moment.datetime()
    assert dt.hour == 22

    # esta manha
    results = pt.parse("esta manha", ref_date)
    assert len(results) == 1
    assert results[0].text == "esta manha"
    dt = results[0].moment.datetime()
    assert dt.hour == 6

    # esta manhã
    results = pt.parse("esta manhã", ref_date)
    assert len(results) == 1
    assert results[0].text == "esta manhã"
    dt = results[0].moment.datetime()
    assert dt.hour == 6

    # meio-dia
    results = pt.parse("meio-dia", ref_date)
    assert len(results) == 1
    assert results[0].text == "meio-dia"
    dt = results[0].moment.datetime()
    assert dt.hour == 12

    # a meia-noite
    ref_date_midnight = datetime.datetime(2020, 9, 1, 11, 0)
    results = pt.parse("a meia-noite", ref_date_midnight)
    assert len(results) == 1
    dt = results[0].moment.datetime()
    assert dt.year == 2020
    assert dt.month == 9
    assert dt.day == 2
    assert dt.hour == 0


def test_pt_casual_negative():
    assert len(pt.parse("naohoje")) == 0
    assert len(pt.parse("hyamanhã")) == 0
    assert len(pt.parse("xontem")) == 0
    assert len(pt.parse("porhora")) == 0
    assert len(pt.parse("agoraxsd")) == 0
