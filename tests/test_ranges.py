"""Tests for date ranges: per-day fan-out and trip metrics chunking."""

from __future__ import annotations

import asyncio
import datetime
import threading
import time
from typing import Any

import httpx
import pytest

from transitmatters import APIError, AsyncTransitMatters, TransitMatters


def headway(day: str) -> dict[str, Any]:
    return {
        "route_id": "Red",
        "direction": "0",
        "current_dep_dt": f"{day}T08:00:00",
        "headway_time_sec": 300.0,
        "vehicle_label": "1850",
    }


def per_day_handler(requests: list[httpx.Request], delay: float = 0.0) -> Any:
    """Answers /api/headways/<day> with one headway on that day.

    Earlier days answer more slowly, so results finish out of order.
    """

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        day = request.url.path.rsplit("/", 1)[1]
        time.sleep(delay * (31 - int(day[-2:])))
        return httpx.Response(200, json=[headway(day)])

    return handler


def client(handler: Any, **kwargs: Any) -> TransitMatters:
    return TransitMatters(
        httpx_args={"transport": httpx.MockTransport(handler)}, **kwargs
    )


def test_single_day_makes_one_request():
    requests: list[httpx.Request] = []

    result = client(per_day_handler(requests)).headways("2025-03-04", stop="70061")

    assert len(result) == 1
    assert [r.url.path for r in requests] == ["/api/headways/2025-03-04"]


def test_range_fetches_each_day_and_keeps_date_order():
    requests: list[httpx.Request] = []
    tm = client(per_day_handler(requests, delay=0.002))

    result = tm.headways("2025-03-01", "2025-03-05", stop="70061")

    assert sorted(r.url.path for r in requests) == [
        f"/api/headways/2025-03-0{d}" for d in range(1, 6)
    ]
    assert all(r.url.params["stop"] == "70061" for r in requests)
    assert [h.current_dep_dt.day for h in result] == [1, 2, 3, 4, 5]


@pytest.mark.parametrize("method", ["dwells", "travel_times", "historical_alerts"])
def test_other_per_day_methods_take_ranges(method):
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json=[])

    getattr(client(handler), method)("2025-03-01", "2025-03-03")

    assert len(requests) == 3


def test_end_before_start_raises_before_sending():
    requests: list[httpx.Request] = []

    with pytest.raises(ValueError, match="before start date"):
        client(per_day_handler(requests)).headways("2025-03-05", "2025-03-01")
    assert requests == []


def test_range_respects_max_concurrency():
    in_flight = peak = 0
    lock = threading.Lock()

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal in_flight, peak
        with lock:
            in_flight += 1
            peak = max(peak, in_flight)
        time.sleep(0.02)
        with lock:
            in_flight -= 1
        return httpx.Response(200, json=[])

    client(handler, max_concurrency=2).headways("2025-03-01", "2025-03-06")

    assert peak == 2


def test_failure_on_one_day_raises():
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("03-02"):
            return httpx.Response(
                400, json={"Code": "BadRequestError", "Message": "no"}
            )
        return httpx.Response(200, json=[])

    with pytest.raises(APIError, match="no"):
        client(handler).headways("2025-03-01", "2025-03-03")


def test_max_concurrency_must_be_positive():
    with pytest.raises(ValueError, match="max_concurrency"):
        TransitMatters(max_concurrency=0)


def test_alerts_spanning_days_are_returned_once():
    multi_day = {
        "valid_from": "2025-03-01T20:00:00-05:00",
        "valid_to": None,
        "text": "A",
    }

    def handler(request: httpx.Request) -> httpx.Response:
        day = request.url.path.rsplit("/", 1)[1]
        one_day = {"valid_from": f"{day}T09:00:00-05:00", "valid_to": None, "text": "B"}
        return httpx.Response(200, json=[multi_day, one_day])

    alerts = client(handler).historical_alerts("2025-03-01", "2025-03-03", route="Red")

    assert [a.text for a in alerts] == ["A", "B", "B", "B"]


@pytest.mark.parametrize(
    ("agg", "max_days"), [("daily", 150), ("weekly", 1050), ("monthly", 4500)]
)
def test_trip_metrics_splits_long_ranges(agg, max_days):
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json=[])

    tm = client(handler)
    start = datetime.date(2020, 1, 1)

    def spans(days: int) -> list[tuple[str, str]]:
        requests.clear()
        end = start + datetime.timedelta(days=days - 1)
        tm.trip_metrics(start, end, line="line-red", agg=agg)
        return sorted(
            (r.url.params["start_date"], r.url.params["end_date"]) for r in requests
        )

    last = start + datetime.timedelta(days=max_days - 1)
    assert spans(max_days) == [(str(start), str(last))]
    assert spans(max_days + 1) == [
        (str(start), str(last)),
        (str(last + datetime.timedelta(days=1)),) * 2,
    ]


def test_trip_metrics_dedupes_by_date():
    entry = {
        "date": "2020-05-30",
        "line": "line-red",
        "count": 1.0,
        "total_time": 1.0,
        "miles_covered": 1.0,
    }
    tm = client(lambda request: httpx.Response(200, json=[entry]))

    result = tm.trip_metrics("2020-01-01", "2020-12-31", line="line-red", agg="daily")

    assert [e.date for e in result] == [datetime.date(2020, 5, 30)]


def test_async_range_respects_max_concurrency_and_order():
    in_flight = peak = 0

    async def handler(request: httpx.Request) -> httpx.Response:
        nonlocal in_flight, peak
        in_flight += 1
        peak = max(peak, in_flight)
        day = request.url.path.rsplit("/", 1)[1]
        await asyncio.sleep(0.001 * (31 - int(day[-2:])))
        in_flight -= 1
        return httpx.Response(200, json=[headway(day)])

    async def run() -> list[Any]:
        transport = httpx.MockTransport(handler)
        async with AsyncTransitMatters(
            httpx_args={"transport": transport}, max_concurrency=3
        ) as tm:
            return await tm.headways("2025-03-01", "2025-03-08")

    result = asyncio.run(run())

    assert peak == 3
    assert [h.current_dep_dt.day for h in result] == list(range(1, 9))


def test_async_failure_on_one_day_raises():
    async def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("03-02"):
            return httpx.Response(404, json=None)
        await asyncio.sleep(0.01)
        return httpx.Response(200, json=[])

    async def run() -> None:
        transport = httpx.MockTransport(handler)
        async with AsyncTransitMatters(httpx_args={"transport": transport}) as tm:
            await tm.dwells("2025-03-01", "2025-03-05")

    with pytest.raises(APIError):
        asyncio.run(run())
