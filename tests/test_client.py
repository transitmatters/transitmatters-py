"""Tests for the high-level clients, run against a mocked transport."""

from __future__ import annotations

import asyncio
import datetime
import inspect
import pkgutil
from typing import Any

import httpx
import pytest

from transitmatters import (
    DEFAULT_BASE_URL,
    APIError,
    AsyncTransitMatters,
    TransitMatters,
)
from transitmatters import _endpoints as endpoints
from transitmatters._convert import EASTERN
from transitmatters._generated.api import api as generated_api
from transitmatters.models import Headway, Healthcheck

HEADWAY = {
    "route_id": "Red",
    "direction": "0",
    "current_dep_dt": "2024-03-01T08:00:00",
    "headway_time_sec": 300.0,
    "vehicle_label": "1850",
}
PARSED_HEADWAY = Headway(
    route_id="Red",
    direction=0,
    current_dep_dt=datetime.datetime(2024, 3, 1, 8, tzinfo=EASTERN),
    headway_time_sec=300.0,
    benchmark_headway_time_sec=None,
    vehicle_label="1850",
    vehicle_consist=(),
)


def mock_transport(
    status_code: int = 200, json: Any = None, content: bytes | None = None
) -> tuple[httpx.MockTransport, list[httpx.Request]]:
    """A transport that answers every request the same way, and the requests it saw."""
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if content is not None:
            return httpx.Response(status_code, content=content)
        return httpx.Response(status_code, json=json)

    return httpx.MockTransport(handler), requests


def mock_client(
    status_code: int = 200, json: Any = None, content: bytes | None = None
) -> tuple[TransitMatters, list[httpx.Request]]:
    transport, requests = mock_transport(status_code, json, content)
    return TransitMatters(httpx_args={"transport": transport}), requests


def test_returns_parsed_models_from_production():
    tm, requests = mock_client(json=[HEADWAY])

    assert tm.headways("2024-03-01", stop="70061") == [PARSED_HEADWAY]
    assert (
        str(requests[0].url) == f"{DEFAULT_BASE_URL}/api/headways/2024-03-01?stop=70061"
    )


@pytest.mark.parametrize(
    "date",
    [
        "2024-03-01",
        datetime.date(2024, 3, 1),
        datetime.datetime(2024, 3, 1, 17, 30),
    ],
)
def test_dates_accept_strings_dates_and_datetimes(date):
    tm, requests = mock_client(json=[])

    tm.headways(date)
    tm.aggregate_headways(date, date)

    assert requests[0].url.path == "/api/headways/2024-03-01"
    assert requests[1].url.params["start_date"] == "2024-03-01"
    assert requests[1].url.params["end_date"] == "2024-03-01"


def test_multiple_ids_repeat_the_query_param():
    tm, requests = mock_client(json=[])

    tm.travel_times("2024-03-01", from_stop=["70061", "70063"], to_stop="70105")

    params = requests[0].url.params
    assert params.get_list("from_stop") == ["70061", "70063"]
    assert params.get_list("to_stop") == ["70105"]


def test_omitted_filters_are_not_sent():
    tm, requests = mock_client(json=[])

    tm.headways("2024-03-01")

    assert requests[0].url.query == b""


def test_agg_is_sent_and_line_delays_defaults_to_weekly():
    tm, requests = mock_client(json=[])

    tm.trip_metrics("2024-01-01", "2024-03-31", line="line-red", agg="monthly")
    tm.line_delays("2024-01-01", "2024-03-31", line="Red")

    assert requests[0].url.params["agg"] == "monthly"
    assert requests[1].url.params["agg"] == "weekly"


def test_invalid_agg_raises_before_sending():
    tm, requests = mock_client(json=[])

    with pytest.raises(ValueError, match="yearly"):
        tm.trip_metrics("2024-01-01", "2024-03-31", line="line-red", agg="yearly")  # type: ignore[arg-type]
    assert requests == []


def test_error_response_raises_api_error():
    tm, _ = mock_client(400, {"Code": "BadRequestError", "Message": "Invalid date"})

    with pytest.raises(APIError) as exc_info:
        tm.headways("2024-03-01", stop="70061")

    err = exc_info.value
    assert (err.status_code, err.code, err.message) == (
        400,
        "BadRequestError",
        "Invalid date",
    )
    assert str(err) == "400 BadRequestError: Invalid date"


def test_route_not_found_raises_api_error():
    tm, _ = mock_client(404, {"error": "Route 'Purple' not found"})

    with pytest.raises(APIError, match="Route 'Purple' not found") as exc_info:
        tm.stops("Purple")
    assert exc_info.value.status_code == 404


def test_undocumented_status_raises_with_raw_body():
    tm, _ = mock_client(502, content=b"Bad Gateway")

    with pytest.raises(APIError, match="^502: Bad Gateway$"):
        tm.routes()


def test_failing_healthcheck_is_returned_not_raised():
    tm, _ = mock_client(500, {"status": "fail", "failed_checks_sum": 1})

    result = tm.healthcheck()

    assert isinstance(result, Healthcheck)
    assert not result.ok


def test_context_manager_closes_connection_pool():
    tm, _ = mock_client(json=[])

    with tm:
        tm.current_alerts()

    assert tm.raw_client.get_httpx_client().is_closed


def test_async_client():
    transport, requests = mock_transport(json=[HEADWAY])

    async def run() -> tuple[list[Headway], AsyncTransitMatters]:
        async with AsyncTransitMatters(httpx_args={"transport": transport}) as tm:
            return await tm.headways("2024-03-01", stop=["70061", "70063"]), tm

    events, tm = asyncio.run(run())

    assert events == [PARSED_HEADWAY]
    assert requests[0].url.path == "/api/headways/2024-03-01"
    assert requests[0].url.params.get_list("stop") == ["70061", "70063"]
    assert tm.raw_client.get_async_httpx_client().is_closed


def test_async_client_raises_api_error():
    transport, _ = mock_transport(400, {"Code": "BadRequestError", "Message": "nope"})

    async def run() -> None:
        async with AsyncTransitMatters(httpx_args={"transport": transport}) as tm:
            await tm.ridership("2024-01-01", "2024-01-31", line_id="line-Red")

    with pytest.raises(APIError, match="nope"):
        asyncio.run(run())


def test_async_client_mirrors_sync_client():
    def methods(cls: type) -> dict[str, inspect.Signature]:
        return {
            name: inspect.signature(member)
            for name, member in inspect.getmembers(cls, inspect.isfunction)
            if not name.startswith("_") and name not in {"close", "aclose"}
        }

    assert methods(TransitMatters) == methods(AsyncTransitMatters)


@pytest.mark.parametrize(
    "endpoint", sorted(m.name for m in pkgutil.iter_modules(generated_api.__path__))
)
def test_every_generated_endpoint_is_wrapped(endpoint):
    # Fails when a spec sync adds an endpoint, as a reminder to wrap it.
    source = inspect.getsource(endpoints)
    assert f"{endpoint}.sync_detailed," in source
    assert f"{endpoint}.asyncio_detailed," in source
