"""Tests for `Line` IDs and the station helpers on `RouteStops`."""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

import httpx
import pytest

from transitmatters import Line, TransitMatters
from transitmatters import models as m

FIXTURES = Path(__file__).parent / "fixtures"
STOPS = json.loads((FIXTURES / "get_stops_for_route.json").read_text())
START, END = "2025-01-01", "2025-01-31"


def recording_client(
    json_body: Any = None,
) -> tuple[TransitMatters, list[httpx.Request]]:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json=json_body)

    return TransitMatters(
        httpx_args={"transport": httpx.MockTransport(handler)}
    ), requests


# Method call -> (query parameter, attribute of `Line` it should carry).
SENDS: dict[str, tuple[Callable[[TransitMatters, Any], Any], str, str]] = {
    "historical_alerts": (
        lambda tm, line: tm.historical_alerts(START, route=line),
        "route",
        "route_id",
    ),
    "scheduled_service": (
        lambda tm, line: tm.scheduled_service(START, END, route=line, agg="daily"),
        "route_id",
        "route_id",
    ),
    "line_delays": (
        lambda tm, line: tm.line_delays(START, END, line=line),
        "line",
        "route_id",
    ),
    "time_predictions": (
        lambda tm, line: tm.time_predictions(line),
        "route_id",
        "route_id",
    ),
    "trip_metrics": (
        lambda tm, line: tm.trip_metrics(START, END, line=line, agg="daily"),
        "line",
        "key",
    ),
    "service_hours": (
        lambda tm, line: tm.service_hours(START, END, line=line, agg="daily"),
        "line_id",
        "key",
    ),
    "ridership": (
        lambda tm, line: tm.ridership(START, END, line=line),
        "line_id",
        "gtfs_line_id",
    ),
    "speed_restrictions": (
        lambda tm, line: tm.speed_restrictions(START, line=line),
        "line_id",
        "gtfs_line_id",
    ),
}
BRANCH_ONLY = {"line_delays", "time_predictions"}
# Responses for the methods that don't return a list.
BODIES = {
    "scheduled_service": json.loads(
        (FIXTURES / "get_scheduled_service.json").read_text()
    ),
    "speed_restrictions": {"available": False},
}


def test_line_ids():
    assert [(line.route_id, line.key, line.gtfs_line_id) for line in Line] == [
        ("Red", "line-red", "line-Red"),
        ("Orange", "line-orange", "line-Orange"),
        ("Blue", "line-blue", "line-Blue"),
        ("Green", "line-green", "line-Green"),
        ("Mattapan", "line-mattapan", "line-Mattapan"),
    ]
    assert Line.GREEN.branches == ("Green-B", "Green-C", "Green-D", "Green-E")
    assert Line.RED.branches == ()


@pytest.mark.parametrize(
    ("method", "line"),
    [
        (method, line)
        for method in sorted(SENDS)
        for line in Line
        # See test_green_line_needs_a_branch.
        if not (method in BRANCH_ONLY and line is Line.GREEN)
    ],
)
def test_line_is_sent_in_each_endpoints_format(method, line):
    call, param, attribute = SENDS[method]
    tm, requests = recording_client(BODIES.get(method, []))

    call(tm, line)

    assert requests[0].url.params[param] == getattr(line, attribute)


def test_stops_takes_a_line():
    tm, requests = recording_client(STOPS)

    tm.stops(Line.ORANGE)

    assert requests[0].url.path == "/api/stops/Orange"


@pytest.mark.parametrize("method", sorted(SENDS))
def test_strings_are_sent_unchanged(method):
    call, param, _ = SENDS[method]
    tm, requests = recording_client(BODIES.get(method, []))

    call(tm, "Some-ID")

    assert requests[0].url.params[param] == "Some-ID"


def test_alert_routes_mix_lines_and_strings():
    tm, requests = recording_client([])

    tm.historical_alerts(START, route=[Line.RED, "66"])

    assert requests[0].url.params.get_list("route") == ["Red", "66"]


@pytest.mark.parametrize("method", sorted(BRANCH_ONLY))
def test_green_line_needs_a_branch(method):
    call, _, _ = SENDS[method]
    tm, requests = recording_client([])

    with pytest.raises(ValueError, match="'Green-B', 'Green-C', 'Green-D', 'Green-E'"):
        call(tm, Line.GREEN)
    assert requests == []


def red() -> m.RouteStops:
    tm, _ = recording_client(STOPS)
    return tm.stops(Line.RED)


@pytest.mark.parametrize("name", ["Davis", "davis", "place-davis", "PLACE-DAVIS"])
def test_station_by_name_or_id(name):
    assert red().station(name).station == "place-davis"


def test_unknown_station_suggests_close_names():
    with pytest.raises(KeyError, match="did you mean 'Davis'"):
        red().station("Daviss")


def test_trip_infers_direction():
    stops = red()

    southbound = stops.trip("Davis", "Porter")
    northbound = stops.trip("Porter", "Davis")

    assert southbound == m.StopPair(
        from_stop=("70063",), to_stop=("70065",), direction=1
    )
    assert northbound == m.StopPair(
        from_stop=("70066",), to_stop=("70064",), direction=0
    )


def test_trip_from_trunk_onto_a_branch():
    pair = red().trip("Alewife", "Braintree")

    assert pair == m.StopPair(from_stop=("70061",), to_stop=("70105",), direction=1)


def test_trip_with_explicit_direction():
    assert red().trip("Davis", "Porter", direction=0).from_stop == ("70064",)


def test_trip_between_branches_raises():
    with pytest.raises(ValueError, match="different branches"):
        red().trip("Ashmont", "Braintree")


def test_trip_to_same_station_raises():
    with pytest.raises(ValueError, match="both the origin and destination"):
        red().trip("Davis", "place-davis")


def test_trip_pair_feeds_travel_times():
    pair = red().trip("Davis", "Porter")
    tm, requests = recording_client([])

    tm.travel_times(START, from_stop=pair.from_stop, to_stop=pair.to_stop)

    assert requests[0].url.params.get_list("from_stop") == ["70063"]
    assert requests[0].url.params.get_list("to_stop") == ["70065"]
