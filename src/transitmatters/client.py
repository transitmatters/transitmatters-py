"""High-level clients for the TransitMatters Data Dashboard API.

Wraps the generated client in `transitmatters._generated` so callers get
parsed models back directly, errors as exceptions, and can pass dates as
strings and single IDs without wrapping them in a list. Requests that fail
transiently are retried.

```python
from transitmatters import TransitMatters

with TransitMatters() as tm:
    for event in tm.headways("2024-03-01", stop="70061"):
        print(event.current_dep_dt, event.headway_time_sec)
```
"""

from __future__ import annotations

import asyncio
import email.utils
import itertools
import random
import time
from collections.abc import Container, Mapping
from http import HTTPStatus
from typing import Any, Literal, Self

import httpx

from . import _endpoints as ep
from ._endpoints import Agg, Call, DateLike, OneOrMany
from ._generated.client import Client
from ._generated.models import ErrorResponse, RouteNotFoundResponse
from ._generated.types import Response
from .errors import (
    APIError,
    BadRequestError,
    NetworkError,
    NotFoundError,
    RangeTooLongError,
    ServerError,
)
from .models import (
    Alert,
    DailyHeadwayStats,
    DailyStats,
    Dwell,
    Facility,
    Headway,
    Healthcheck,
    LineDelays,
    LiveAlert,
    Ridership,
    Routes,
    RouteStops,
    ScheduledService,
    ServiceHours,
    ServiceRidershipDashboard,
    SpeedRestrictions,
    TimePredictionWeek,
    TravelTime,
    TravelTimeStats,
    TripMetrics,
)

DEFAULT_BASE_URL = "https://dashboard-api.labs.transitmatters.org"
DEFAULT_TIMEOUT = 30.0
DEFAULT_MAX_RETRIES = 3

_RETRY_STATUSES = frozenset(
    {
        HTTPStatus.TOO_MANY_REQUESTS,
        HTTPStatus.BAD_GATEWAY,
        HTTPStatus.SERVICE_UNAVAILABLE,
        HTTPStatus.GATEWAY_TIMEOUT,
    }
)
# Failures where the request may not have reached the API, or the response
# was cut off. Every endpoint is a GET, so trying again is safe.
_RETRY_ERRORS = (httpx.TimeoutException, httpx.NetworkError, httpx.RemoteProtocolError)
_BACKOFF_BASE = 0.5
_BACKOFF_CAP = 8.0
# Give up rather than wait longer than this for a server's Retry-After.
_MAX_RETRY_AFTER = 60.0

# Looked up at call time so tests can patch them.
_sleep = time.sleep
_asleep = asyncio.sleep


def _unwrap(response: Response[Any], ok: Container[int]) -> Any:
    """Return the parsed body of a successful response, or raise APIError."""
    if response.status_code in ok and response.parsed is not None:
        return response.parsed
    raise _api_error(response)


def _api_error(response: Response[Any]) -> APIError:
    status = int(response.status_code)
    parsed = response.parsed
    if isinstance(parsed, ErrorResponse):
        # Only trip metrics documents a 403, for ranges that are too long.
        cls = (
            RangeTooLongError
            if status == HTTPStatus.FORBIDDEN
            else _error_class(status)
        )
        return cls(status, parsed.message, code=parsed.code, content=response.content)
    if isinstance(parsed, RouteNotFoundResponse):
        return NotFoundError(status, parsed.error, content=response.content)
    # Undocumented status, so the body may not be JSON; report it as-is.
    message = response.content.decode(errors="replace").strip()
    return _error_class(status)(
        status, message or response.status_code.phrase, content=response.content
    )


def _error_class(status: int) -> type[APIError]:
    if status == HTTPStatus.BAD_REQUEST:
        return BadRequestError
    if status == HTTPStatus.NOT_FOUND:
        return NotFoundError
    if status >= HTTPStatus.INTERNAL_SERVER_ERROR:
        return ServerError
    return APIError


def _network_error(error: httpx.RequestError) -> NetworkError:
    detail = str(error) or type(error).__name__
    try:
        request = error.request
    except RuntimeError:  # httpx raises this when no request is attached
        return NetworkError(detail)
    return NetworkError(f"{request.method} {request.url}: {detail}")


def _result[T](call: Call[T], outcome: Response[Any] | httpx.RequestError) -> T:
    if isinstance(outcome, httpx.RequestError):
        raise _network_error(outcome) from outcome
    return call.convert(_unwrap(outcome, call.ok))


def _backoff(attempt: int) -> float:
    delay = min(_BACKOFF_CAP, _BACKOFF_BASE * 2**attempt)
    return delay / 2 + random.uniform(0, delay / 2)


def _retry_after(headers: Mapping[str, str]) -> float | None:
    """Seconds to wait from a Retry-After header, if it has a usable one."""
    value = headers.get("retry-after")
    if value is None:
        return None
    try:
        return max(0.0, float(value))
    except ValueError:
        pass
    try:
        when = email.utils.parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return None
    return max(0.0, when.timestamp() - time.time())


class _BaseClient:
    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        *,
        timeout: float | httpx.Timeout | None = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        headers: Mapping[str, str] | None = None,
        httpx_args: Mapping[str, Any] | None = None,
    ) -> None:
        """
        Args:
            base_url: API root. Defaults to the production API.
            timeout: Seconds to wait for each request, an `httpx.Timeout`,
                or `None` to wait indefinitely.
            max_retries: How many times to retry a request that timed out,
                couldn't connect, or got a 429, 502, 503, or 504, with
                exponential backoff. `0` disables retries.
            headers: Extra headers to send with every request.
            httpx_args: Extra keyword arguments for the underlying `httpx`
                client, such as `transport` or `proxy`.
        """
        if isinstance(timeout, int | float):
            timeout = httpx.Timeout(timeout)
        self._max_retries = max_retries
        self._client = Client(
            base_url=base_url,
            timeout=timeout,
            headers=dict(headers or {}),
            httpx_args=dict(httpx_args or {}),
        )

    @property
    def raw_client(self) -> Client:
        """The underlying generated client.

        Pass it to functions in `transitmatters._generated.api` to reach the
        API directly. Those functions return generated types, which may
        change whenever the spec is regenerated.
        """
        return self._client

    def _retry_delay(
        self,
        attempt: int,
        outcome: Response[Any] | httpx.RequestError,
        ok: Container[int],
    ) -> float | None:
        """Seconds to wait before retrying, or `None` to stop."""
        if attempt >= self._max_retries:
            return None
        if isinstance(outcome, httpx.RequestError):
            return _backoff(attempt) if isinstance(outcome, _RETRY_ERRORS) else None
        status = outcome.status_code
        if status in ok or status not in _RETRY_STATUSES:
            return None
        delay = _retry_after(outcome.headers)
        if delay is None:
            return _backoff(attempt)
        return delay if delay <= _MAX_RETRY_AFTER else None


class TransitMatters(_BaseClient):
    """Client for the TransitMatters Data Dashboard API.

    Use it as a context manager, or call `close` when finished, to release
    the connection pool. Methods raise `transitmatters.APIError` when the API
    returns an error, and `transitmatters.NetworkError` when no response
    arrives.

    Stop, route, and line IDs differ by endpoint; each method's docstring
    shows the expected form. `routes` and `stops` list valid IDs.
    """

    def close(self) -> None:
        """Close the underlying connection pool."""
        self._client.get_httpx_client().close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    def _run[T](self, call: Call[T]) -> T:
        for attempt in itertools.count():
            try:
                outcome = call.sync()
            except httpx.RequestError as e:
                outcome = e
            delay = self._retry_delay(attempt, outcome, call.ok)
            if delay is None:
                return _result(call, outcome)
            _sleep(delay)
        raise AssertionError("unreachable")

    def healthcheck(self) -> Healthcheck:
        """Run the API's health checks.

        Failing checks come back with `ok` false rather than raising.
        """
        return self._run(ep.healthcheck(self._client))

    def headways(
        self, date: DateLike, *, stop: OneOrMany | None = None
    ) -> list[Headway]:
        """Time between consecutive departures from `stop` on `date`.

        Returns one event per departure. `stop` is one or more MBTA stop IDs,
        e.g. `"70061"`.
        """
        return self._run(ep.headways(self._client, date, stop=stop))

    def dwells(self, date: DateLike, *, stop: OneOrMany | None = None) -> list[Dwell]:
        """Time vehicles spent stopped at `stop` on `date`.

        Returns one event per stop a vehicle made. `stop` is one or more MBTA
        stop IDs, e.g. `"70061"`.
        """
        return self._run(ep.dwells(self._client, date, stop=stop))

    def travel_times(
        self,
        date: DateLike,
        *,
        from_stop: OneOrMany | None = None,
        to_stop: OneOrMany | None = None,
    ) -> list[TravelTime]:
        """Travel time of each trip from `from_stop` to `to_stop` on `date`.

        Returns one event per trip. Both are one or more MBTA stop IDs, e.g.
        `"70061"`, and must be platforms for the same direction of travel.
        """
        return self._run(
            ep.travel_times(self._client, date, from_stop=from_stop, to_stop=to_stop)
        )

    def historical_alerts(
        self, date: DateLike, *, route: OneOrMany | None = None
    ) -> list[Alert]:
        """Alerts that were active on `date` for `route`.

        `route` is one or more MBTA route IDs, e.g. `"Red"` or `"66"`.
        """
        return self._run(ep.historical_alerts(self._client, date, route=route))

    def aggregate_travel_times(
        self,
        start_date: DateLike,
        end_date: DateLike,
        *,
        from_stop: OneOrMany | None = None,
        to_stop: OneOrMany | None = None,
    ) -> list[DailyStats]:
        """Daily travel-time statistics between stops over an inclusive date range.

        Returns one entry per service date and peak period. Stop IDs work as
        in `travel_times`.
        """
        return self._run(
            ep.aggregate_travel_times(
                self._client, start_date, end_date, from_stop=from_stop, to_stop=to_stop
            )
        )

    def aggregate_travel_times_v2(
        self,
        start_date: DateLike,
        end_date: DateLike,
        *,
        from_stop: OneOrMany | None = None,
        to_stop: OneOrMany | None = None,
    ) -> TravelTimeStats:
        """Travel-time statistics between stops, by date and by time of day.

        `by_date` matches `aggregate_travel_times`; `by_time` groups trips into
        30-minute departure-time buckets across the whole range.
        """
        return self._run(
            ep.aggregate_travel_times_v2(
                self._client, start_date, end_date, from_stop=from_stop, to_stop=to_stop
            )
        )

    def aggregate_headways(
        self,
        start_date: DateLike,
        end_date: DateLike,
        *,
        stop: OneOrMany | None = None,
    ) -> list[DailyHeadwayStats]:
        """Daily headway statistics for `stop` over an inclusive date range.

        Returns one entry per service date, with bunching and on-time counts.
        """
        return self._run(
            ep.aggregate_headways(self._client, start_date, end_date, stop=stop)
        )

    def aggregate_dwells(
        self,
        start_date: DateLike,
        end_date: DateLike,
        *,
        stop: OneOrMany | None = None,
    ) -> list[DailyStats]:
        """Daily dwell-time statistics for `stop` over an inclusive date range.

        Returns one entry per service date and peak period.
        """
        return self._run(
            ep.aggregate_dwells(self._client, start_date, end_date, stop=stop)
        )

    def current_alerts(self) -> list[LiveAlert]:
        """Alerts in effect right now, live from the MBTA."""
        return self._run(ep.current_alerts(self._client))

    def line_delays(
        self,
        start_date: DateLike,
        end_date: DateLike,
        *,
        line: str,
        agg: Literal["daily", "weekly"] = "weekly",
    ) -> list[LineDelays]:
        """Alert-attributed delays on `line` over an inclusive date range.

        Returns one entry per day or week, with minutes of delay by cause.
        `line` is e.g. `"Red"` or `"CR-Fairmount"`.
        """
        return self._run(
            ep.line_delays(self._client, start_date, end_date, line=line, agg=agg)
        )

    def trip_metrics(
        self,
        start_date: DateLike,
        end_date: DateLike,
        *,
        line: str,
        agg: Agg,
    ) -> list[TripMetrics]:
        """Speed and travel-time metrics for `line` over an inclusive date range.

        Returns one entry per day, week, or month. `line` is a rapid transit
        line, e.g. `"line-red"`.
        """
        return self._run(
            ep.trip_metrics(self._client, start_date, end_date, line=line, agg=agg)
        )

    def scheduled_service(
        self,
        start_date: DateLike,
        end_date: DateLike,
        *,
        route_id: str,
        agg: Agg,
    ) -> ScheduledService:
        """Scheduled trip counts for a route over an inclusive date range.

        `counts` has one entry per day, week, or month. `route_id` is an MBTA
        route ID, e.g. `"Red"` or `"66"`.
        """
        return self._run(
            ep.scheduled_service(
                self._client, start_date, end_date, route_id=route_id, agg=agg
            )
        )

    def ridership(
        self,
        start_date: DateLike,
        end_date: DateLike,
        *,
        line_id: str,
    ) -> list[Ridership]:
        """Ridership on a line over an inclusive date range.

        Returns one entry per week. `line_id` is e.g. `"line-Red"`,
        `"line-66"`, or `"line-Fairmount"`.
        """
        return self._run(
            ep.ridership(self._client, start_date, end_date, line_id=line_id)
        )

    def facilities(self) -> list[Facility]:
        """Elevators and escalators, live from the MBTA."""
        return self._run(ep.facilities(self._client))

    def speed_restrictions(self, date: DateLike, *, line_id: str) -> SpeedRestrictions:
        """Speed restrictions in effect on a rapid transit line on `date`.

        `line_id` is case-sensitive, e.g. `"line-Red"`.
        """
        return self._run(ep.speed_restrictions(self._client, date, line_id=line_id))

    def service_hours(
        self,
        start_date: DateLike,
        end_date: DateLike,
        *,
        line_id: str,
        agg: Agg,
    ) -> list[ServiceHours]:
        """Scheduled and delivered service hours on a line over a date range.

        Returns one entry per day, week, or month. `line_id` is a rapid
        transit line, e.g. `"line-red"`.
        """
        return self._run(
            ep.service_hours(
                self._client, start_date, end_date, line_id=line_id, agg=agg
            )
        )

    def time_predictions(self, route_id: str) -> list[TimePredictionWeek]:
        """Weekly arrival-prediction accuracy for a route, e.g. `"Red"`."""
        return self._run(ep.time_predictions(self._client, route_id))

    def service_ridership_dashboard(self) -> ServiceRidershipDashboard:
        """Combined service and ridership data behind the overview dashboard."""
        return self._run(ep.service_ridership_dashboard(self._client))

    def routes(self) -> Routes:
        """All route IDs the dashboard supports, grouped by mode."""
        return self._run(ep.routes(self._client))

    def stops(self, route_id: str) -> RouteStops:
        """Stations and stop IDs along a route, e.g. `"Red"`."""
        return self._run(ep.stops(self._client, route_id))


class AsyncTransitMatters(_BaseClient):
    """Async client for the TransitMatters Data Dashboard API.

    Mirrors `TransitMatters`; see it for details on each method. Use it as an
    async context manager, or await `aclose` when finished.
    """

    async def aclose(self) -> None:
        """Close the underlying connection pool."""
        await self._client.get_async_httpx_client().aclose()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        await self.aclose()

    async def _run[T](self, call: Call[T]) -> T:
        for attempt in itertools.count():
            try:
                outcome = await call.asyncio()
            except httpx.RequestError as e:
                outcome = e
            delay = self._retry_delay(attempt, outcome, call.ok)
            if delay is None:
                return _result(call, outcome)
            await _asleep(delay)
        raise AssertionError("unreachable")

    async def healthcheck(self) -> Healthcheck:
        """Run the API's health checks.

        Failing checks come back with `ok` false rather than raising.
        """
        return await self._run(ep.healthcheck(self._client))

    async def headways(
        self, date: DateLike, *, stop: OneOrMany | None = None
    ) -> list[Headway]:
        """Time between consecutive departures from `stop` on `date`."""
        return await self._run(ep.headways(self._client, date, stop=stop))

    async def dwells(
        self, date: DateLike, *, stop: OneOrMany | None = None
    ) -> list[Dwell]:
        """Time vehicles spent stopped at `stop` on `date`."""
        return await self._run(ep.dwells(self._client, date, stop=stop))

    async def travel_times(
        self,
        date: DateLike,
        *,
        from_stop: OneOrMany | None = None,
        to_stop: OneOrMany | None = None,
    ) -> list[TravelTime]:
        """Travel time of each trip from `from_stop` to `to_stop` on `date`."""
        return await self._run(
            ep.travel_times(self._client, date, from_stop=from_stop, to_stop=to_stop)
        )

    async def historical_alerts(
        self, date: DateLike, *, route: OneOrMany | None = None
    ) -> list[Alert]:
        """Alerts that were active on `date` for `route`."""
        return await self._run(ep.historical_alerts(self._client, date, route=route))

    async def aggregate_travel_times(
        self,
        start_date: DateLike,
        end_date: DateLike,
        *,
        from_stop: OneOrMany | None = None,
        to_stop: OneOrMany | None = None,
    ) -> list[DailyStats]:
        """Daily travel-time statistics between stops over an inclusive date range."""
        return await self._run(
            ep.aggregate_travel_times(
                self._client, start_date, end_date, from_stop=from_stop, to_stop=to_stop
            )
        )

    async def aggregate_travel_times_v2(
        self,
        start_date: DateLike,
        end_date: DateLike,
        *,
        from_stop: OneOrMany | None = None,
        to_stop: OneOrMany | None = None,
    ) -> TravelTimeStats:
        """Travel-time statistics between stops, by date and by time of day."""
        return await self._run(
            ep.aggregate_travel_times_v2(
                self._client, start_date, end_date, from_stop=from_stop, to_stop=to_stop
            )
        )

    async def aggregate_headways(
        self,
        start_date: DateLike,
        end_date: DateLike,
        *,
        stop: OneOrMany | None = None,
    ) -> list[DailyHeadwayStats]:
        """Daily headway statistics for `stop` over an inclusive date range."""
        return await self._run(
            ep.aggregate_headways(self._client, start_date, end_date, stop=stop)
        )

    async def aggregate_dwells(
        self,
        start_date: DateLike,
        end_date: DateLike,
        *,
        stop: OneOrMany | None = None,
    ) -> list[DailyStats]:
        """Daily dwell-time statistics for `stop` over an inclusive date range."""
        return await self._run(
            ep.aggregate_dwells(self._client, start_date, end_date, stop=stop)
        )

    async def current_alerts(self) -> list[LiveAlert]:
        """Alerts in effect right now, live from the MBTA."""
        return await self._run(ep.current_alerts(self._client))

    async def line_delays(
        self,
        start_date: DateLike,
        end_date: DateLike,
        *,
        line: str,
        agg: Literal["daily", "weekly"] = "weekly",
    ) -> list[LineDelays]:
        """Alert-attributed delays on `line` over an inclusive date range."""
        return await self._run(
            ep.line_delays(self._client, start_date, end_date, line=line, agg=agg)
        )

    async def trip_metrics(
        self,
        start_date: DateLike,
        end_date: DateLike,
        *,
        line: str,
        agg: Agg,
    ) -> list[TripMetrics]:
        """Speed and travel-time metrics for `line` over an inclusive date range."""
        return await self._run(
            ep.trip_metrics(self._client, start_date, end_date, line=line, agg=agg)
        )

    async def scheduled_service(
        self,
        start_date: DateLike,
        end_date: DateLike,
        *,
        route_id: str,
        agg: Agg,
    ) -> ScheduledService:
        """Scheduled trip counts for a route over an inclusive date range."""
        return await self._run(
            ep.scheduled_service(
                self._client, start_date, end_date, route_id=route_id, agg=agg
            )
        )

    async def ridership(
        self,
        start_date: DateLike,
        end_date: DateLike,
        *,
        line_id: str,
    ) -> list[Ridership]:
        """Ridership on a line over an inclusive date range."""
        return await self._run(
            ep.ridership(self._client, start_date, end_date, line_id=line_id)
        )

    async def facilities(self) -> list[Facility]:
        """Elevators and escalators, live from the MBTA."""
        return await self._run(ep.facilities(self._client))

    async def speed_restrictions(
        self, date: DateLike, *, line_id: str
    ) -> SpeedRestrictions:
        """Speed restrictions in effect on a rapid transit line on `date`."""
        return await self._run(
            ep.speed_restrictions(self._client, date, line_id=line_id)
        )

    async def service_hours(
        self,
        start_date: DateLike,
        end_date: DateLike,
        *,
        line_id: str,
        agg: Agg,
    ) -> list[ServiceHours]:
        """Scheduled and delivered service hours on a line over a date range."""
        return await self._run(
            ep.service_hours(
                self._client, start_date, end_date, line_id=line_id, agg=agg
            )
        )

    async def time_predictions(self, route_id: str) -> list[TimePredictionWeek]:
        """Weekly arrival-prediction accuracy for a route."""
        return await self._run(ep.time_predictions(self._client, route_id))

    async def service_ridership_dashboard(self) -> ServiceRidershipDashboard:
        """Combined service and ridership data behind the overview dashboard."""
        return await self._run(ep.service_ridership_dashboard(self._client))

    async def routes(self) -> Routes:
        """All route IDs the dashboard supports, grouped by mode."""
        return await self._run(ep.routes(self._client))

    async def stops(self, route_id: str) -> RouteStops:
        """Stations and stop IDs along a route."""
        return await self._run(ep.stops(self._client, route_id))
