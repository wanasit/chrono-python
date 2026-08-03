import datetime
from chrono_python.locales import de


def test_de_casual_date_single():
    ref_date = datetime.datetime(2012, 8, 10, 8, 9, 10, 11)

    # jetzt
    results = de.parse("Frist ist jetzt", ref_date)
    assert len(results) == 1
    assert results[0].text == "jetzt"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10
    assert dt.hour == 8
    assert dt.minute == 9

    # heute
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = de.parse("Frist ist heute", ref_date)
    assert len(results) == 1
    assert results[0].text == "heute"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10

    # morgen
    results = de.parse("Frist ist morgen", ref_date)
    assert len(results) == 1
    assert results[0].text == "morgen"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 11

    # übermorgen
    results = de.parse("Frist ist übermorgen", ref_date)
    assert len(results) == 1
    assert results[0].text == "übermorgen"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 12

    # gestern
    results = de.parse("Frist war gestern", ref_date)
    assert len(results) == 1
    assert results[0].text == "gestern"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 9

    # vorgestern
    results = de.parse("Frist war vorgestern", ref_date)
    assert len(results) == 1
    assert results[0].text == "vorgestern"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 8


def test_de_casual_date_with_time_of_day():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # heute Nacht
    results = de.parse("heute Nacht", ref_date)
    assert len(results) == 1
    assert results[0].text == "heute Nacht"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10
    assert dt.hour == 22

    # heute Abend
    results = de.parse("heute Abend", ref_date)
    assert len(results) == 1
    assert results[0].text == "heute Abend"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10
    assert dt.hour == 20

    # gestern Abend
    results = de.parse("gestern Abend", ref_date)
    assert len(results) == 1
    assert results[0].text == "gestern Abend"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 9
    assert dt.hour == 20
