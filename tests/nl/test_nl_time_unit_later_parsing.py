import datetime
from chrono_python.locales import nl


def test_nl_time_unit_later_from_now():
    ref_date = datetime.datetime(2012, 8, 10)

    results = nl.parse("5 dagen vanaf nu we hebben iets gedaan", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "5 dagen vanaf nu"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 15

    results = nl.parse("10 dagen vanaf nu we hebben iets gedaan", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "10 dagen vanaf nu"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 20

    ref_date = datetime.datetime(2012, 8, 10, 12, 14)
    results = nl.parse("15 minuten vanaf nu", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "15 minuten vanaf nu"
    dt = results[0].moment.datetime()
    assert dt.hour == 12
    assert dt.minute == 29

    results = nl.parse("15 minuten eerder", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "15 minuten eerder"
    dt = results[0].moment.datetime()
    assert dt.hour == 11
    assert dt.minute == 59

    results = nl.parse("15 minuten uit", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "15 minuten uit"
    dt = results[0].moment.datetime()
    assert dt.hour == 12
    assert dt.minute == 29

    results = nl.parse("   12 uur vanaf nu", ref_date)
    assert len(results) == 1
    assert results[0].index == 3
    assert results[0].text == "12 uur vanaf nu"
    dt = results[0].moment.datetime()
    assert dt.day == 11
    assert dt.hour == 0
    assert dt.minute == 14

    results = nl.parse("   half uur vanaf nu", ref_date)
    assert len(results) == 1
    assert results[0].index == 3
    assert results[0].text == "half uur vanaf nu"
    dt = results[0].moment.datetime()
    assert dt.hour == 12
    assert dt.minute == 44

    results = nl.parse("Over 12 uur heb ik iets gedaan", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "Over 12 uur"
    dt = results[0].moment.datetime()
    assert dt.day == 11
    assert dt.hour == 0
    assert dt.minute == 14

    results = nl.parse("Over 12 seconden heb ik iets gedaan", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "Over 12 seconden"
    dt = results[0].moment.datetime()
    assert dt.hour == 12
    assert dt.minute == 14
    assert dt.second == 12

    results = nl.parse("over drie seconden heb ik iets gedaan", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "over drie seconden"
    dt = results[0].moment.datetime()
    assert dt.hour == 12
    assert dt.minute == 14
    assert dt.second == 3

    ref_date = datetime.datetime(2012, 8, 10)
    results = nl.parse("Over 5 dagen hebben we iets gedaan", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "Over 5 dagen"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 15

    results = nl.parse("Over een dag hebben we iets gedaan", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "Over een dag"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 11

    ref_date = datetime.datetime(2012, 8, 10, 12, 14)
    results = nl.parse("een minuutje uit", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "een minuutje uit"
    dt = results[0].moment.datetime()
    assert dt.hour == 12
    assert dt.minute == 15

    results = nl.parse("in 1 uur", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "in 1 uur"
    dt = results[0].moment.datetime()
    assert dt.hour == 13
    assert dt.minute == 14

    ref_date = datetime.datetime(2012, 8, 10, 12, 40)
    results = nl.parse("over 1,5 uur", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "over 1,5 uur"
    dt = results[0].moment.datetime()
    assert dt.hour == 14
    assert dt.minute == 10


def test_nl_time_unit_later_strict():
    ref_date = datetime.datetime(2012, 8, 10, 12, 14)
    results = nl.strict.parse("15 minuten vanaf nu", ref_date)
    assert len(results) == 1
    assert results[0].text == "15 minuten vanaf nu"
    dt = results[0].moment.datetime()
    assert dt.hour == 12
    assert dt.minute == 29

    ref_date = datetime.datetime(2012, 8, 10, 12, 40)
    results = nl.strict.parse("25 minuten later", ref_date)
    assert len(results) == 1
    assert results[0].index == 0
    assert results[0].text == "25 minuten later"
    dt = results[0].moment.datetime()
    assert dt.hour == 13
    assert dt.minute == 5
