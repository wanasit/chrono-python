import datetime
from chrono_python.locales import fr


def test_fr_date_range_merging():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # Du 24 août 2023 au 26 août 2023
    results = fr.parse("Du 24 août 2023 au 26 août 2023", ref_date)
    assert len(results) == 1
    assert results[0].text == "24 août 2023 au 26 août 2023"
    assert results[0].start.datetime().day == 24
    assert results[0].end.datetime().day == 26

    # 10 août - 12 septembre
    results = fr.parse("10 août - 12 septembre", ref_date)
    assert len(results) == 1
    assert results[0].text == "10 août - 12 septembre"
    assert results[0].start.datetime().month == 8
    assert results[0].start.datetime().day == 10
    assert results[0].end.datetime().month == 9
    assert results[0].end.datetime().day == 12

    # 10 août - 12 septembre 2013
    results = fr.parse("10 août - 12 septembre 2013", ref_date)
    assert len(results) == 1
    assert results[0].text == "10 août - 12 septembre 2013"
    assert results[0].start.datetime().year == 2013
    assert results[0].end.datetime().year == 2013
