import datetime
import pytest

import chrono_python as chrono
from chrono_python.types import DateTimeMoment, DateTimePrecision
from chrono_python.common.types import DateTimeComponent


def test_single_expression():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)
    
    # 2012年3月31日
    results = chrono.ja.parse("主な株主（2012年3月31日現在）", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.index == 5
    assert result.text == "2012年3月31日"
    assert result.moment.get(DateTimeComponent.YEAR) == 2012
    assert result.moment.get(DateTimeComponent.MONTH) == 3
    assert result.moment.get(DateTimeComponent.DAY) == 31
    assert result.moment.is_certain(DateTimeComponent.YEAR) is True
    assert result.moment.is_certain(DateTimeComponent.MONTH) is True
    assert result.moment.is_certain(DateTimeComponent.DAY) is True
    assert result.moment.datetime() == datetime.datetime(2012, 3, 31, 12, 0)

    # 2012年９月3日
    results = chrono.ja.parse("主な株主（2012年９月3日現在）", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.index == 5
    assert result.text == "2012年９月3日"
    assert result.moment.get(DateTimeComponent.YEAR) == 2012
    assert result.moment.get(DateTimeComponent.MONTH) == 9
    assert result.moment.get(DateTimeComponent.DAY) == 3
    assert result.moment.is_certain(DateTimeComponent.YEAR) is True
    assert result.moment.is_certain(DateTimeComponent.MONTH) is True
    assert result.moment.is_certain(DateTimeComponent.DAY) is True
    assert result.moment.datetime() == datetime.datetime(2012, 9, 3, 12, 0)

    # 2020年2月29日 with ref in 2019
    ref_date_2019 = datetime.datetime(2019, 8, 10, 12, 0)
    results = chrono.ja.parse("主な株主（2020年2月29日現在）", ref_date_2019)
    assert len(results) == 1
    result = results[0]
    assert result.index == 5
    assert result.text == "2020年2月29日"
    assert result.moment.get(DateTimeComponent.YEAR) == 2020
    assert result.moment.get(DateTimeComponent.MONTH) == 2
    assert result.moment.get(DateTimeComponent.DAY) == 29
    assert result.moment.datetime() == datetime.datetime(2020, 2, 29, 12, 0)

    # ９月3日 (No year)
    results = chrono.ja.parse("主な株主（９月3日現在）", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.index == 5
    assert result.text == "９月3日"
    assert result.moment.get(DateTimeComponent.YEAR) == 2012
    assert result.moment.get(DateTimeComponent.MONTH) == 9
    assert result.moment.get(DateTimeComponent.DAY) == 3
    assert result.moment.is_certain(DateTimeComponent.YEAR) is False
    assert result.moment.is_certain(DateTimeComponent.MONTH) is True
    assert result.moment.is_certain(DateTimeComponent.DAY) is True
    assert result.moment.datetime() == datetime.datetime(2012, 9, 3, 12, 0)


def test_era_expressions():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # 平成26年12月29日 (Heisei 26 = 1988 + 26 = 2014)
    results = chrono.ja.parse("主な株主（平成26年12月29日）", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.index == 5
    assert result.text == "平成26年12月29日"
    assert result.moment.get(DateTimeComponent.YEAR) == 2014
    assert result.moment.get(DateTimeComponent.MONTH) == 12
    assert result.moment.get(DateTimeComponent.DAY) == 29
    assert result.moment.is_certain(DateTimeComponent.YEAR) is True
    assert result.moment.datetime() == datetime.datetime(2014, 12, 29, 12, 0)

    # 昭和６４年１月７日 (Showa 64 = 1925 + 64 = 1989)
    results = chrono.ja.parse("主な株主（昭和６４年１月７日）", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.index == 5
    assert result.text == "昭和６４年１月７日"
    assert result.moment.get(DateTimeComponent.YEAR) == 1989
    assert result.moment.get(DateTimeComponent.MONTH) == 1
    assert result.moment.get(DateTimeComponent.DAY) == 7
    assert result.moment.datetime() == datetime.datetime(1989, 1, 7, 12, 0)

    # 令和元年5月1日 (Reiwa 1/Gannen = 2018 + 1 = 2019)
    results = chrono.ja.parse("主な株主（令和元年5月1日）", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.index == 5
    assert result.text == "令和元年5月1日"
    assert result.moment.get(DateTimeComponent.YEAR) == 2019
    assert result.moment.get(DateTimeComponent.MONTH) == 5
    assert result.moment.get(DateTimeComponent.DAY) == 1
    assert result.moment.datetime() == datetime.datetime(2019, 5, 1, 12, 0)

    # 令和2年5月1日 (Reiwa 2 = 2018 + 2 = 2020)
    results = chrono.ja.parse("主な株主（令和2年5月1日）", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.index == 5
    assert result.text == "令和2年5月1日"
    assert result.moment.get(DateTimeComponent.YEAR) == 2020
    assert result.moment.get(DateTimeComponent.MONTH) == 5
    assert result.moment.get(DateTimeComponent.DAY) == 1
    assert result.moment.is_certain(DateTimeComponent.YEAR) is True
    assert result.moment.datetime() == datetime.datetime(2020, 5, 1, 12, 0)


def test_relative_year_expressions():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # 同年7月27日
    results = chrono.ja.parse("主な株主（同年7月27日）", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.index == 5
    assert result.text == "同年7月27日"
    assert result.moment.get(DateTimeComponent.YEAR) == 2012
    assert result.moment.get(DateTimeComponent.MONTH) == 7
    assert result.moment.get(DateTimeComponent.DAY) == 27
    assert result.moment.datetime() == datetime.datetime(2012, 7, 27, 12, 0)

    # 本年7月27日
    results = chrono.ja.parse("主な株主（本年7月27日）", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.index == 5
    assert result.text == "本年7月27日"
    assert result.moment.get(DateTimeComponent.YEAR) == 2012
    assert result.moment.get(DateTimeComponent.MONTH) == 7
    assert result.moment.get(DateTimeComponent.DAY) == 27
    assert result.moment.datetime() == datetime.datetime(2012, 7, 27, 12, 0)

    # 今年7月27日
    results = chrono.ja.parse("主な株主（今年7月27日）", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.index == 5
    assert result.text == "今年7月27日"
    assert result.moment.get(DateTimeComponent.YEAR) == 2012
    assert result.moment.get(DateTimeComponent.MONTH) == 7
    assert result.moment.get(DateTimeComponent.DAY) == 27
    assert result.moment.datetime() == datetime.datetime(2012, 7, 27, 12, 0)

    # 今年11月27日 with ref in Jan
    ref_jan = datetime.datetime(2012, 1, 10, 12, 0)
    results = chrono.ja.parse("今年11月27日", ref_jan)
    assert len(results) == 1
    result = results[0]
    assert result.index == 0
    assert result.text == "今年11月27日"
    assert result.moment.get(DateTimeComponent.YEAR) == 2012
    assert result.moment.get(DateTimeComponent.MONTH) == 11
    assert result.moment.get(DateTimeComponent.DAY) == 27
    assert result.moment.datetime() == datetime.datetime(2012, 11, 27, 12, 0)


def test_expression_without_year():
    ref_date = datetime.datetime(2012, 8, 10, 12, 0)

    # 7月27日 (reference year 2012 is closest)
    results = chrono.ja.parse("7月27日", ref_date)
    assert len(results) == 1
    result = results[0]
    assert result.index == 0
    assert result.text == "7月27日"
    assert result.moment.get(DateTimeComponent.YEAR) == 2012
    assert result.moment.get(DateTimeComponent.MONTH) == 7
    assert result.moment.get(DateTimeComponent.DAY) == 27
    assert result.moment.datetime() == datetime.datetime(2012, 7, 27, 12, 0)

    # 11月27日 with ref in Jan 2012 (Nov 27, 2011 is closer than Nov 27, 2012)
    ref_jan = datetime.datetime(2012, 1, 10, 12, 0)
    results = chrono.ja.parse("11月27日", ref_jan)
    assert len(results) == 1
    result = results[0]
    assert result.index == 0
    assert result.text == "11月27日"
    assert result.moment.get(DateTimeComponent.YEAR) == 2011
    assert result.moment.get(DateTimeComponent.MONTH) == 11
    assert result.moment.get(DateTimeComponent.DAY) == 27
    assert result.moment.datetime() == datetime.datetime(2011, 11, 27, 12, 0)
