import datetime
from chrono_python.locales import nl


def test_nl_casual_date_single():
    ref_date = datetime.datetime(2012, 8, 10, 8, 9, 10, 11)

    # nu
    results = nl.parse("nu", ref_date)
    assert len(results) == 1
    assert results[0].text == "nu"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10
    assert dt.hour == 8
    assert dt.minute == 9

    # vandaag
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = nl.parse("vandaag", ref_date)
    assert len(results) == 1
    assert results[0].text == "vandaag"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10

    # morgen
    results = nl.parse("morgen", ref_date)
    assert len(results) == 1
    assert results[0].text == "morgen"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 11

    # morgend
    results = nl.parse("morgend", ref_date)
    assert len(results) == 1
    assert results[0].text == "morgend"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 11

    # gisteren
    results = nl.parse("gisteren", ref_date)
    assert len(results) == 1
    assert results[0].text == "gisteren"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 9

    # morgen 12:00
    results = nl.parse("morgen 12:00", ref_date)
    assert len(results) == 1
    assert results[0].text == "morgen 12:00"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 11
    assert dt.hour == 12

    # morgenavond
    ref_date = datetime.datetime(2012, 8, 10, 14, 0)
    results = nl.parse("morgenavond", ref_date)
    assert len(results) == 1
    assert results[0].text == "morgenavond"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 11
    assert dt.hour == 20


def test_nl_casual_date_range():
    ref_date = datetime.datetime(2012, 8, 4, 12, 0)
    results = nl.parse("Het evenement is vandaag - volgende vrijdag", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.index == 17
    assert result.text == "vandaag - volgende vrijdag"
    assert result.moment is not None
    start_dt = result.moment.datetime()
    assert start_dt.year == 2012
    assert start_dt.month == 8
    assert start_dt.day == 4
    assert start_dt.hour == 12

    assert result.end is not None
    end_dt = result.end.datetime()
    assert end_dt.year == 2012
    assert end_dt.month == 8
    assert end_dt.day == 10
    assert end_dt.hour == 12

    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    results = nl.parse("Het evenement is vandaag - volgende vrijdag", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.index == 17
    assert result.text == "vandaag - volgende vrijdag"
    start_dt = result.moment.datetime()
    assert start_dt.year == 2012
    assert start_dt.month == 8
    assert start_dt.day == 10

    assert result.end is not None
    end_dt = result.end.datetime()
    assert end_dt.year == 2012
    assert end_dt.month == 8
    assert end_dt.day == 17


def test_nl_casual_time_implication():
    ref_date = datetime.datetime(2012, 8, 4, 12, 0)
    results = nl.parse("jaarlijks verlof vanaf vandaag tot morgennamiddag", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "vandaag tot morgennamiddag"
    start_dt = result.moment.datetime()
    assert start_dt.month == 8
    assert start_dt.day == 4
    assert start_dt.hour == 12

    assert result.end is not None
    end_dt = result.end.datetime()
    assert end_dt.month == 8
    assert end_dt.day == 5
    assert end_dt.hour == 15

    results = nl.parse("jaarlijks verlof vanaf deze ochtend tot morgen", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.text == "deze ochtend tot morgen"
    start_dt = result.moment.datetime()
    assert start_dt.month == 8
    assert start_dt.day == 4
    assert start_dt.hour == 6

    assert result.end is not None
    end_dt = result.end.datetime()
    assert end_dt.month == 8
    assert end_dt.day == 5
    assert end_dt.hour == 12


def test_nl_casual_random_text():
    ref_date = datetime.datetime(2012, 1, 1, 12, 0)

    results = nl.parse("vanavond", ref_date)
    assert len(results) == 1
    assert results[0].text == "vanavond"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 1
    assert dt.day == 1
    assert dt.hour == 20

    results = nl.parse("middag", ref_date)
    assert len(results) == 1
    assert results[0].text == "middag"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 1
    assert dt.day == 1
    assert dt.hour == 12

    results = nl.parse("vanavond 22:00", ref_date)
    assert len(results) == 1
    assert results[0].text == "vanavond 22:00"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 1
    assert dt.day == 1
    assert dt.hour == 22

    results = nl.parse("vanavond om 21:00", ref_date)
    assert len(results) == 1
    assert results[0].text == "vanavond om 21:00"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 1
    assert dt.day == 1
    assert dt.hour == 21

    results = nl.parse("morgen voor 16:00", ref_date)
    assert len(results) == 1
    assert results[0].text == "morgen voor 16:00"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 1
    assert dt.day == 2
    assert dt.hour == 16

    results = nl.parse("morgen na 16:00", ref_date)
    assert len(results) == 1
    assert results[0].text == "morgen na 16:00"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 1
    assert dt.day == 2
    assert dt.hour == 16

    results = nl.parse("donderdag", ref_date)
    assert len(results) == 1

    ref_date = datetime.datetime(2016, 10, 1, 12, 0)
    results = nl.parse("deze avond", ref_date)
    assert len(results) == 1
    assert results[0].text == "deze avond"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 10
    assert dt.day == 1
    assert dt.hour == 20

    results = nl.parse("gisterennamiddag", ref_date)
    assert len(results) == 1
    assert results[0].text == "gisterennamiddag"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 9
    assert dt.day == 30
    assert dt.hour == 15

    ref_date = datetime.datetime(2016, 10, 1, 8, 0)
    results = nl.parse("morgenochtend", ref_date)
    assert len(results) == 1
    assert results[0].text == "morgenochtend"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 10
    assert dt.day == 2
    assert dt.hour == 6

    results = nl.parse("deze namiddag om 15:00", ref_date)
    assert len(results) == 1
    assert results[0].text == "deze namiddag om 15:00"
    dt = results[0].moment.datetime()
    assert dt.year == 2016
    assert dt.month == 10
    assert dt.day == 1
    assert dt.hour == 15


def test_nl_casual_negative_text():
    assert len(nl.parse("notoday")) == 0
    assert len(nl.parse("tdtmr")) == 0
    assert len(nl.parse("xyesterday")) == 0
    assert len(nl.parse("nowhere")) == 0
    assert len(nl.parse("noway")) == 0
    assert len(nl.parse("knowledge")) == 0
