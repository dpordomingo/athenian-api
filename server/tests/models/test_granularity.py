from datetime import date, timedelta

import pytest

from athenian.api.models.web import Granularity


@pytest.mark.parametrize("value,result", [
    ("day", [date(2020, 1, 1) + i * timedelta(days=1) for i in range(62)]),
    ("1 day", [date(2020, 1, 1) + i * timedelta(days=1) for i in range(62)]),
    ("2 day", [date(2020, 1, 1) + 2 * i * timedelta(days=1) for i in range(31)]),
    ("week", [date(2020, 1, 1) + i * timedelta(days=7) for i in range(9)]),
    ("3 week", [date(2020, 1, 1) + 3 * i * timedelta(days=7) for i in range(3)]),
    ("month", [date(2020, 1, 1), date(2020, 2, 1), date(2020, 3, 1)]),
    ("4 month", [date(2020, 1, 1)]),
    ("year", [date(2020, 1, 1)]),
])
def test_split(value, result):
    splitted = Granularity.split(value, date(2020, 1, 1), date(2020, 3, 2))
    assert result == splitted


@pytest.mark.parametrize("value", ["bullshit", "days", " day", "0 day", "01 day", "2day"])
def test_split_errors(value):
    with pytest.raises(ValueError):
        Granularity.split(value, date(2020, 1, 1), date(2020, 3, 2))
