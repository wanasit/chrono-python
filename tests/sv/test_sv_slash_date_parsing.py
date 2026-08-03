import datetime
from chrono_python.locales import sv
from chrono_python.common.types import CivilTimeComponent


def test_sv_slash_date_parsing():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # 15/8/2012 (little endian: DD/MM/YYYY)
    results = sv.parse("15/8/2012", ref_date)
    assert len(results) == 1
    assert results[0].text == "15/8/2012"
    assert results[0].moment.get(CivilTimeComponent.YEAR) == 2012
    assert results[0].moment.get(CivilTimeComponent.MONTH) == 8
    assert results[0].moment.get(CivilTimeComponent.DAY) == 15
