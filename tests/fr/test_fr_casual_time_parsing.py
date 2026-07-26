import datetime
from chrono_python.locales import fr


def test_fr_casual_time_single():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # ce matin
    results = fr.parse("La deadline est ce matin", ref_date)
    assert len(results) == 1
    assert results[0].index == 16
    assert results[0].text == "ce matin"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10
    assert dt.hour == 8

    # cet après-midi
    results = fr.parse("La deadline est cet après-midi", ref_date)
    assert len(results) == 1
    assert results[0].index == 16
    assert results[0].text == "cet après-midi"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10
    assert dt.hour == 14

    # cet aprem
    results = fr.parse("La deadline est cet aprem", ref_date)
    assert len(results) == 1
    assert results[0].index == 16
    assert results[0].text == "cet aprem"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10
    assert dt.hour == 14

    # ce soir
    results = fr.parse("La deadline est ce soir", ref_date)
    assert len(results) == 1
    assert results[0].index == 16
    assert results[0].text == "ce soir"
    dt = results[0].moment.datetime()
    assert dt.year == 2012
    assert dt.month == 8
    assert dt.day == 10
    assert dt.hour == 18

    # a midi
    results = fr.parse("a midi", ref_date)
    assert len(results) == 1
    assert results[0].text == "a midi"
    assert results[0].moment.datetime().hour == 12

    # à minuit
    results = fr.parse("à minuit", ref_date)
    assert len(results) == 1
    assert results[0].text == "à minuit"
    assert results[0].moment.datetime().hour == 0
