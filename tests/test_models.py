"""Tests for the public models, converted from recorded API responses."""

from __future__ import annotations

import dataclasses
import datetime
import inspect
import json
import pkgutil
import typing
from collections.abc import Callable
from pathlib import Path
from typing import Any

import attrs
import httpx
import pytest

from transitmatters import TransitMatters, _convert
from transitmatters import models as m
from transitmatters._convert import EASTERN
from transitmatters._generated import models as generated_models
from transitmatters._generated.api import api as generated_api
from transitmatters._generated.types import Unset

FIXTURES = Path(__file__).parent / "fixtures"
ERROR_BODIES = {"ErrorResponse", "RouteNotFoundResponse"}

# Generated endpoint module -> the call that returns its recorded fixture.
CALLS: dict[str, Callable[[TransitMatters], Any]] = {
    "get_healthcheck": lambda tm: tm.healthcheck(),
    "get_headways": lambda tm: tm.headways("2025-03-04", stop="70061"),
    "get_dwells": lambda tm: tm.dwells("2025-03-04", stop="70063"),
    "get_travel_times": lambda tm: tm.travel_times(
        "2025-03-04", from_stop="70061", to_stop="70105"
    ),
    "get_historical_alerts": lambda tm: tm.historical_alerts("2025-03-04", route="Red"),
    "get_aggregate_travel_times": lambda tm: tm.aggregate_travel_times(
        "2025-03-03", "2025-03-07", from_stop="70061", to_stop="70105"
    ),
    "get_aggregate_travel_times_v2": lambda tm: tm.aggregate_travel_times_v2(
        "2025-03-03", "2025-03-07", from_stop="70061", to_stop="70105"
    ),
    "get_aggregate_headways": lambda tm: tm.aggregate_headways(
        "2025-03-03", "2025-03-07", stop="70061"
    ),
    "get_aggregate_dwells": lambda tm: tm.aggregate_dwells(
        "2025-03-03", "2025-03-07", stop="70063"
    ),
    "get_current_alerts": lambda tm: tm.current_alerts(),
    "get_line_delays": lambda tm: tm.line_delays(
        "2025-01-01", "2025-03-31", line="Red"
    ),
    "get_trip_metrics": lambda tm: tm.trip_metrics(
        "2025-03-01", "2025-03-31", line="line-red", agg="daily"
    ),
    "get_scheduled_service": lambda tm: tm.scheduled_service(
        "2025-03-01", "2025-03-31", route_id="Red", agg="daily"
    ),
    "get_ridership": lambda tm: tm.ridership(
        "2025-01-01", "2025-03-31", line_id="line-Red"
    ),
    "get_facilities": lambda tm: tm.facilities(),
    "get_speed_restrictions": lambda tm: tm.speed_restrictions(
        "2025-03-04", line_id="line-Red"
    ),
    "get_service_hours": lambda tm: tm.service_hours(
        "2025-03-01", "2025-03-31", line_id="line-red", agg="daily"
    ),
    "get_time_predictions": lambda tm: tm.time_predictions("Red"),
    "get_service_ridership_dashboard": lambda tm: tm.service_ridership_dashboard(),
    "get_routes": lambda tm: tm.routes(),
    "get_stops_for_route": lambda tm: tm.stops("Red"),
}


def fixture(endpoint: str) -> Any:
    return json.loads((FIXTURES / f"{endpoint}.json").read_text())


def replay(endpoint: str) -> Any:
    """Call `endpoint` against a transport that answers with its fixture."""
    body = fixture(endpoint)
    transport = httpx.MockTransport(lambda _: httpx.Response(200, json=body))
    return CALLS[endpoint](TransitMatters(httpx_args={"transport": transport}))


def walk(value: Any) -> typing.Iterator[Any]:
    """Every value reachable from `value`, through models and containers."""
    yield value
    if dataclasses.is_dataclass(value):
        for field in dataclasses.fields(value):
            yield from walk(getattr(value, field.name))
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from walk(key)
            yield from walk(item)
    elif isinstance(value, list | tuple):
        for item in value:
            yield from walk(item)


def test_every_endpoint_has_a_fixture():
    endpoints = {m.name for m in pkgutil.iter_modules(generated_api.__path__)}

    assert set(CALLS) == endpoints
    assert {p.stem for p in FIXTURES.glob("*.json")} == endpoints


@pytest.mark.parametrize("endpoint", sorted(CALLS))
def test_fixture_converts_to_public_models(endpoint):
    result = replay(endpoint)

    values = list(walk(result))
    assert any(isinstance(v, m.Model) for v in values)
    for value in values:
        assert not isinstance(value, Unset)
        assert not type(value).__module__.startswith("transitmatters._generated")
        if isinstance(value, datetime.datetime):
            assert value.tzinfo is EASTERN


@pytest.mark.parametrize(
    "method",
    [
        n
        for n, f in inspect.getmembers(TransitMatters, inspect.isfunction)
        if not n.startswith("_")
    ],
)
def test_return_types_are_public(method):
    hints = typing.get_type_hints(getattr(TransitMatters, method))

    def classes(tp: Any) -> typing.Iterator[type]:
        if isinstance(tp, type):
            yield tp
        for arg in typing.get_args(tp):
            yield from classes(arg)

    for cls in classes(hints["return"]):
        assert not cls.__module__.startswith("transitmatters._generated"), cls


def test_generated_fields_are_all_converted():
    # Fails when a spec sync adds a field, as a reminder to add it to a model
    # (or to IGNORED_FIELDS with a reason).
    # Only the converters' code, not IGNORED_FIELDS, which names fields too.
    source = "".join(
        inspect.getsource(fn)
        for _, fn in inspect.getmembers(_convert, inspect.isfunction)
        if fn.__module__ == _convert.__name__
    )
    missing = []
    for name in generated_models.__all__:
        cls = getattr(generated_models, name)
        # Request parameters and error bodies aren't converted into models.
        if not attrs.has(cls) or name.endswith("Params") or name in ERROR_BODIES:
            continue
        for field in attrs.fields(cls):
            key = f"{name}.{field.name}"
            if field.name == "additional_properties" or key in _convert.IGNORED_FIELDS:
                continue
            if f".{field.name}" not in source:
                missing.append(key)
    assert missing == []


def test_headways():
    first = replay("get_headways")[0]
    raw = fixture("get_headways")[0]

    assert first.direction == int(raw["direction"]) == 0
    assert first.current_dep_dt == datetime.datetime(2025, 3, 4, 5, 56, tzinfo=EASTERN)
    assert first.benchmark_headway_time_sec == raw["benchmark_headway_time_sec"]
    assert first.vehicle_consist == ()


def test_vehicle_consist_splits_car_numbers():
    body = [{**fixture("get_dwells")[0], "vehicle_consist": "1850|1851"}]
    transport = httpx.MockTransport(lambda _: httpx.Response(200, json=body))
    tm = TransitMatters(httpx_args={"transport": transport})

    assert tm.dwells("2025-03-04")[0].vehicle_consist == ("1850", "1851")


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        # Eastern wall-clock time, as alerts before 2024-04-12 and all events use.
        ("2024-01-05T08:00:00", datetime.datetime(2024, 1, 5, 8, tzinfo=EASTERN)),
        # With an offset, as newer alerts use.
        (
            "2025-03-04T20:00:00-05:00",
            datetime.datetime(2025, 3, 4, 20, tzinfo=EASTERN),
        ),
        # Another zone's offset is converted to Eastern.
        ("2025-07-01T12:00:00+00:00", datetime.datetime(2025, 7, 1, 8, tzinfo=EASTERN)),
    ],
)
def test_timestamps_become_eastern(raw, expected):
    parsed = _convert._dt(raw)

    assert parsed == expected
    assert parsed.utcoffset() == expected.utcoffset()


def test_historical_alerts():
    first = replay("get_historical_alerts")[0]

    assert first.valid_from == datetime.datetime(2025, 3, 4, 20, tzinfo=EASTERN)
    assert first.text.startswith("Red Line")


def test_live_alert_stop_ids_are_strings():
    alerts = replay("get_current_alerts")
    raw = fixture("get_current_alerts")

    assert any(isinstance(stop, int) for a in raw for stop in a["stops"])
    assert all(isinstance(stop, str) for a in alerts for stop in a.stops)
    assert alerts[0].stops == ("1587",)
    assert alerts[0].active_period[0].upcoming


def test_aggregate_stats_have_readable_names():
    first = replay("get_aggregate_travel_times")[0]
    raw = fixture("get_aggregate_travel_times")[0]

    assert (first.min, first.max, first.sum) == (raw["min"], raw["max"], raw["sum"])
    assert (first.p25, first.p50, first.p75) == (raw["25%"], raw["50%"], raw["75%"])
    assert first.service_date == datetime.date.fromisoformat(raw["service_date"])


def test_aggregate_headways_have_bunching():
    first = replay("get_aggregate_headways")[0]
    raw = fixture("get_aggregate_headways")[0]

    assert isinstance(first, m.DailyHeadwayStats)
    assert (first.bunched, first.on_time) == (raw["bunched"], raw["on_time"])


def test_time_of_day_slots_sort_past_midnight():
    def slot(dep_time_from_epoch: str) -> m.TimeOfDayStats:
        return _convert._time_of_day_stats(
            generated_models.AggregateByTime.from_dict(
                {
                    **fixture("get_aggregate_travel_times_v2")["by_time"][0],
                    "dep_time_from_epoch": dep_time_from_epoch,
                }
            )
        )

    assert slot("1970-01-01T05:30:00").dep_time == datetime.timedelta(
        hours=5, minutes=30
    )
    assert slot("1970-01-02T00:30:00").dep_time == datetime.timedelta(
        hours=24, minutes=30
    )


def test_trip_metrics_fleet_mix():
    first = replay("get_trip_metrics")[0]

    assert first.fleet_mix == {"red1": 25.5, "red2": 19.6, "red3": 29.4, "red4": 25.5}
    assert first.avg_car_age == 33.2


def test_scheduled_service():
    result = replay("get_scheduled_service")

    assert result.start_date == datetime.date(2025, 3, 1)
    assert result.start_date_service_levels.weekday.date == datetime.date(2025, 3, 3)
    assert result.counts[0] == m.ScheduledServiceCount(
        date=datetime.date(2025, 3, 1), count=370
    )


def test_speed_restrictions():
    result = replay("get_speed_restrictions")

    assert result.date == datetime.date(2025, 3, 4)
    assert result.zones[0].from_stop_id == "place-cntsq"
    assert result.zones[0].reported == datetime.date(2025, 2, 26)


def test_speed_restrictions_unavailable():
    transport = httpx.MockTransport(
        lambda _: httpx.Response(200, json={"available": False})
    )
    tm = TransitMatters(httpx_args={"transport": transport})

    result = tm.speed_restrictions("2015-01-01", line_id="line-Red")

    assert result == m.SpeedRestrictions(available=False, date=None, zones=())


def test_route_stops():
    red = replay("get_stops_for_route")
    davis = red.stations[1]

    assert red.directions == {0: "northbound", 1: "southbound"}
    assert davis.stop_name == "Davis"
    assert davis.stops == {0: ("70064",), 1: ("70063",)}
    assert davis.branches == ("A", "B")
    assert (davis.accessible, davis.terminus) == (True, False)


def test_facilities():
    andrew = replay("get_facilities")[0]

    assert andrew.type == "ELEVATOR"
    assert andrew.stop_id == "place-andrw"
    assert andrew.latitude is None
    assert m.FacilityProperty(name="excludes-stop", value="13") in andrew.properties


def test_facility_coordinates_are_floats():
    facility = fixture("get_facilities")["data"][0]
    facility["attributes"].update(latitude="42.352271", longitude="-71.055242")
    body = {"data": [facility]}
    transport = httpx.MockTransport(lambda _: httpx.Response(200, json=body))

    result = TransitMatters(httpx_args={"transport": transport}).facilities()[0]

    assert (result.latitude, result.longitude) == (42.352271, -71.055242)


def test_healthcheck_failures():
    body = {"status": "fail", "failed_checks_sum": 1, "failed_checks": {"S3": "down"}}
    transport = httpx.MockTransport(lambda _: httpx.Response(500, json=body))

    result = TransitMatters(httpx_args={"transport": transport}).healthcheck()

    assert not result.ok
    assert result.failed_checks == {"S3": "down"}


def test_service_ridership_dashboard():
    result = replay("get_service_ridership_dashboard")
    red = result.line_data["line-Red"]

    assert set(result.mode_data) == {"rapid-transit", "regional-rail", "boat", "bus"}
    assert red.long_name == "Red Line"
    assert red.ridership_history[datetime.date(2018, 1, 1)] == 122736
    assert red.service_regimes.current.weekday.total_trips == 241


def test_time_predictions():
    first = replay("get_time_predictions")[0]

    assert first.week == datetime.date(2020, 8, 3)
    assert first.prediction[0].bin == "0-3 min"


def test_to_dict_nests_models():
    red = replay("get_stops_for_route")

    as_dict = red.to_dict()

    assert as_dict["stations"][1]["stop_name"] == "Davis"
    assert as_dict["stations"][1]["stops"] == {0: ("70064",), 1: ("70063",)}
