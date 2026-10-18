"""Tests for to_dataframe."""

from __future__ import annotations

import builtins
import datetime
from typing import Any

import pytest
from test_models import CALLS, replay

from transitmatters import models as m
from transitmatters import to_dataframe
from transitmatters._convert import EASTERN

pandas = pytest.importorskip("pandas")


def headway(hour: int, **overrides: Any) -> m.Headway:
    return m.Headway(
        **{
            "route_id": "Red",
            "direction": 0,
            "current_dep_dt": datetime.datetime(2025, 3, 4, hour, tzinfo=EASTERN),
            "headway_time_sec": 300.0,
            "benchmark_headway_time_sec": None,
            "vehicle_label": "1850",
            "vehicle_consist": (),
            **overrides,
        }
    )


def test_one_row_per_model_one_column_per_field():
    df = to_dataframe([headway(8), headway(9, benchmark_headway_time_sec=310.0)])

    assert list(df.columns) == [
        "route_id",
        "direction",
        "current_dep_dt",
        "headway_time_sec",
        "benchmark_headway_time_sec",
        "vehicle_label",
        "vehicle_consist",
    ]
    assert len(df) == 2
    assert df["benchmark_headway_time_sec"].isna().tolist() == [True, False]


def test_times_stay_eastern():
    df = to_dataframe([headway(8)])

    assert str(df["current_dep_dt"].dt.tz) == "America/New_York"
    assert df["current_dep_dt"][0] == pandas.Timestamp("2025-03-04 08:00", tz=EASTERN)


def test_dates_become_datetimes():
    df = to_dataframe([m.Ridership(date=datetime.date(2025, 1, 6), count=1)])

    assert pandas.api.types.is_datetime64_dtype(df["date"])
    assert df["date"][0] == pandas.Timestamp("2025-01-06")


def test_timedeltas_stay_timedeltas():
    stats = m.TimeOfDayStats(
        count=1, mean=1, min=1, max=1, std=0, sum=1, p25=1, p50=1, p75=1,
        dep_time=datetime.timedelta(hours=24, minutes=30),
        is_peak_day=True,
    )  # fmt: skip

    df = to_dataframe([stats])

    assert pandas.api.types.is_timedelta64_dtype(df["dep_time"])


def test_empty_list_gives_empty_frame():
    assert to_dataframe([]).empty


def test_mixed_models_raise():
    with pytest.raises(TypeError, match="Headway, Ridership"):
        to_dataframe([headway(8), m.Ridership(date=datetime.date(2025, 1, 6), count=1)])


def test_missing_pandas_says_how_to_install(monkeypatch):
    real_import = builtins.__import__

    def no_pandas(name: str, *args: Any, **kwargs: Any) -> Any:
        if name == "pandas":
            raise ImportError("No module named 'pandas'")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", no_pandas)

    with pytest.raises(ImportError, match=r"transitmatters\[pandas\]"):
        to_dataframe([headway(8)])


@pytest.mark.parametrize(
    "endpoint", [e for e in sorted(CALLS) if isinstance(replay(e), list)]
)
def test_every_list_result_converts(endpoint):
    result = replay(endpoint)

    df = to_dataframe(result)

    assert len(df) == len(result)
