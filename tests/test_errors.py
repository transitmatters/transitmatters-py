"""Tests for error types and retries."""

from __future__ import annotations

import asyncio
from collections.abc import Callable
from typing import Any

import httpx
import pytest

from transitmatters import (
    APIError,
    AsyncTransitMatters,
    BadRequestError,
    NetworkError,
    NotFoundError,
    RangeTooLongError,
    ServerError,
    TransitMatters,
)

Reply = httpx.Response | Exception


def scripted(
    *replies: Reply, **kwargs: Any
) -> tuple[TransitMatters, list[httpx.Request]]:
    """A client whose requests get `replies` in order; an exception is raised."""
    requests: list[httpx.Request] = []
    queue = list(replies)

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        reply = queue.pop(0)
        if isinstance(reply, Exception):
            raise reply
        return reply

    transport = httpx.MockTransport(handler)
    return TransitMatters(httpx_args={"transport": transport}, **kwargs), requests


def ok() -> httpx.Response:
    return httpx.Response(200, json=[])


@pytest.mark.parametrize(
    ("status", "body", "error"),
    [
        (400, {"Code": "BadRequestError", "Message": "bad"}, BadRequestError),
        (403, {"Code": "ForbiddenError", "Message": "too long"}, RangeTooLongError),
        (404, None, NotFoundError),
        (500, None, ServerError),
        (418, None, APIError),
    ],
)
def test_status_picks_error_class(status, body, error):
    tm, _ = scripted(httpx.Response(status, json=body))

    with pytest.raises(error) as exc_info:
        tm.trip_metrics("2024-01-01", "2024-01-31", line="line-red", agg="daily")
    assert exc_info.value.status_code == status


def test_undocumented_403_is_not_range_too_long():
    tm, _ = scripted(httpx.Response(403, content=b"Missing Authentication Token"))

    with pytest.raises(APIError) as exc_info:
        tm.routes()
    assert type(exc_info.value) is APIError


def test_route_not_found_is_not_found_error():
    tm, _ = scripted(httpx.Response(404, json={"error": "Route 'Purple' not found"}))

    with pytest.raises(NotFoundError, match="Purple"):
        tm.stops("Purple")


@pytest.mark.parametrize("status", [429, 502, 503, 504])
def test_retries_transient_statuses(status, sleeps):
    tm, requests = scripted(httpx.Response(status), httpx.Response(status), ok())

    assert tm.headways("2024-03-01") == []
    assert len(requests) == 3
    assert len(sleeps) == 2


def test_backoff_grows_and_is_capped(sleeps):
    tm, _ = scripted(*[httpx.Response(503)] * 7, ok(), max_retries=7)

    tm.headways("2024-03-01")

    # Each delay is between half and all of 0.5s * 2**attempt, capped at 8s.
    ceilings = [0.5, 1, 2, 4, 8, 8, 8]
    assert len(sleeps) == len(ceilings)
    for delay, ceiling in zip(sleeps, ceilings, strict=True):
        assert ceiling / 2 <= delay <= ceiling


def test_retry_after_seconds_is_honored(sleeps):
    tm, _ = scripted(httpx.Response(429, headers={"Retry-After": "7"}), ok())

    tm.headways("2024-03-01")

    assert sleeps == [7.0]


def test_long_retry_after_gives_up(sleeps):
    tm, requests = scripted(httpx.Response(429, headers={"Retry-After": "3600"}))

    with pytest.raises(APIError) as exc_info:
        tm.headways("2024-03-01")
    assert exc_info.value.status_code == 429
    assert (len(requests), sleeps) == (1, [])


def test_gives_up_after_max_retries(sleeps):
    tm, requests = scripted(*[httpx.Response(503)] * 3, max_retries=2)

    with pytest.raises(ServerError):
        tm.headways("2024-03-01")
    assert len(requests) == 3
    assert len(sleeps) == 2


def test_max_retries_zero_disables_retries(sleeps):
    tm, requests = scripted(httpx.Response(503), max_retries=0)

    with pytest.raises(ServerError):
        tm.headways("2024-03-01")
    assert (len(requests), sleeps) == (1, [])


@pytest.mark.parametrize(
    ("status", "body"),
    [(400, {"Code": "BadRequestError", "Message": "bad"}), (404, None), (500, None)],
)
def test_does_not_retry_other_errors(status, body, sleeps):
    tm, requests = scripted(httpx.Response(status, json=body))

    with pytest.raises(APIError):
        tm.headways("2024-03-01")
    assert (len(requests), sleeps) == (1, [])


def test_failing_healthcheck_is_not_retried(sleeps):
    tm, requests = scripted(httpx.Response(500, json={"status": "fail"}))

    assert tm.healthcheck().status == "fail"
    assert (len(requests), sleeps) == (1, [])


@pytest.mark.parametrize(
    "make_error",
    [httpx.ConnectError, httpx.ReadTimeout, httpx.RemoteProtocolError],
)
def test_retries_transport_errors(make_error: Callable[[str], Exception], sleeps):
    tm, requests = scripted(make_error("boom"), ok())

    assert tm.headways("2024-03-01") == []
    assert len(requests) == 2
    assert len(sleeps) == 1


def test_transport_error_becomes_network_error():
    tm, _ = scripted(*[httpx.ConnectError("refused")] * 4)

    with pytest.raises(
        NetworkError, match="GET .*/api/headways/2024-03-01: refused"
    ) as exc_info:
        tm.headways("2024-03-01")
    assert isinstance(exc_info.value.__cause__, httpx.ConnectError)


def test_unretryable_transport_error_is_raised_at_once(sleeps):
    tm, requests = scripted(httpx.UnsupportedProtocol("nope"))

    with pytest.raises(NetworkError):
        tm.headways("2024-03-01")
    assert (len(requests), sleeps) == (1, [])


def test_async_client_retries(sleeps):
    replies: list[Reply] = [httpx.ConnectError("refused"), httpx.Response(503), ok()]
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        reply = replies.pop(0)
        if isinstance(reply, Exception):
            raise reply
        return reply

    async def run() -> list[Any]:
        transport = httpx.MockTransport(handler)
        async with AsyncTransitMatters(httpx_args={"transport": transport}) as tm:
            return await tm.headways("2024-03-01")

    assert asyncio.run(run()) == []
    assert len(requests) == 3
    assert len(sleeps) == 2


def test_async_client_raises_network_error():
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("refused", request=request)

    async def run() -> None:
        transport = httpx.MockTransport(handler)
        async with AsyncTransitMatters(
            httpx_args={"transport": transport}, max_retries=0
        ) as tm:
            await tm.routes()

    with pytest.raises(NetworkError, match="refused"):
        asyncio.run(run())
