"""High-level clients for the TransitMatters Data Dashboard API.

Wraps the generated client in `transitmatters._generated` so callers get
parsed models back directly, errors as exceptions, and can pass dates as
strings and single IDs without wrapping them in a list.

```python
from transitmatters import TransitMatters

with TransitMatters() as tm:
    for event in tm.headways("2024-03-01", stop="70061"):
        print(event.current_dep_dt, event.headway_time_sec)
```
"""

from __future__ import annotations

import datetime
from collections.abc import Container, Mapping, Sequence
from http import HTTPStatus
from typing import Any, Literal, Self

import httpx

from ._generated.api.api import (
    get_aggregate_dwells,
    get_aggregate_headways,
    get_aggregate_travel_times,
    get_aggregate_travel_times_v2,
    get_current_alerts,
    get_dwells,
    get_facilities,
    get_headways,
    get_healthcheck,
    get_historical_alerts,
    get_line_delays,
    get_ridership,
    get_routes,
    get_scheduled_service,
    get_service_hours,
    get_service_ridership_dashboard,
    get_speed_restrictions,
    get_stops_for_route,
    get_time_predictions,
    get_travel_times,
    get_trip_metrics,
)
from ._generated.client import Client
from ._generated.models import (
    AggregateByDate,
    Alert,
    DwellEvent,
    ErrorResponse,
    FacilitiesResponse,
    GetLineDelaysAgg,
    GetScheduledServiceAgg,
    GetScheduledServiceResponse,
    GetServiceHoursAgg,
    GetTripMetricsAgg,
    HeadwayAggregateByDate,
    HeadwayEvent,
    HealthcheckResponse,
    LineDelayEntry,
    LiveAlert,
    RidershipEntry,
    RouteNotFoundResponse,
    RoutesResponse,
    ServiceHoursEntry,
    ServiceRidershipDashboardResponse,
    SpeedRestrictionsResponse,
    StopsResponse,
    TimePredictionWeek,
    TravelTimeAggregate2Response,
    TravelTimeEvent,
    TripMetricsEntry,
)
from ._generated.types import UNSET, Response, Unset
from .errors import APIError

DEFAULT_BASE_URL = "https://dashboard-api.labs.transitmatters.org"
DEFAULT_TIMEOUT = 30.0

DateLike = datetime.date | str
"""A date, or an ISO 8601 `YYYY-MM-DD` string."""

OneOrMany = str | Sequence[str]
"""A single ID, or several."""

Agg = Literal["daily", "weekly", "monthly"]

# The healthcheck reports failing checks with a 500 and a normal body.
_HEALTHCHECK_OK = (HTTPStatus.OK, HTTPStatus.INTERNAL_SERVER_ERROR)


def _to_date(value: DateLike) -> datetime.date:
    # datetime subclasses date, but its str() includes the time, which the API rejects.
    if isinstance(value, datetime.datetime):
        return value.date()
    if isinstance(value, datetime.date):
        return value
    return datetime.date.fromisoformat(value)


def _to_list(values: OneOrMany | None) -> list[str] | Unset:
    if values is None:
        return UNSET
    if isinstance(values, str):
        return [values]
    return list(values)


def _unwrap(response: Response[Any], ok: Container[int] = (HTTPStatus.OK,)) -> Any:
    """Return the parsed body of a successful response, or raise APIError."""
    if response.status_code in ok and response.parsed is not None:
        return response.parsed
    raise _api_error(response)


def _api_error(response: Response[Any]) -> APIError:
    status = int(response.status_code)
    parsed = response.parsed
    if isinstance(parsed, ErrorResponse):
        return APIError(
            status, parsed.message, code=parsed.code, content=response.content
        )
    if isinstance(parsed, RouteNotFoundResponse):
        return APIError(status, parsed.error, content=response.content)
    # Undocumented status, so the body may not be JSON; report it as-is.
    message = response.content.decode(errors="replace").strip()
    return APIError(
        status, message or response.status_code.phrase, content=response.content
    )


class _BaseClient:
    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        *,
        timeout: float | httpx.Timeout | None = DEFAULT_TIMEOUT,
        headers: Mapping[str, str] | None = None,
        httpx_args: Mapping[str, Any] | None = None,
    ) -> None:
        """
        Args:
            base_url: API root. Defaults to the production API.
            timeout: Seconds to wait for each request, an `httpx.Timeout`,
                or `None` to wait indefinitely.
            headers: Extra headers to send with every request.
            httpx_args: Extra keyword arguments for the underlying `httpx`
                client, such as `transport` or `proxy`.
        """
        if isinstance(timeout, int | float):
            timeout = httpx.Timeout(timeout)
        self._client = Client(
            base_url=base_url,
            timeout=timeout,
            headers=dict(headers or {}),
            httpx_args=dict(httpx_args or {}),
        )

    @property
    def raw_client(self) -> Client:
        """The underlying generated client.

        Pass it to functions in `transitmatters._generated.api` to reach
        endpoints this class doesn't wrap yet.
        """
        return self._client


class TransitMatters(_BaseClient):
    """Client for the TransitMatters Data Dashboard API.

    Use it as a context manager, or call `close` when finished, to release
    the connection pool. Methods raise `transitmatters.APIError` when the API
    returns an error.

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

    def healthcheck(self) -> HealthcheckResponse:
        """Run the API's health checks.

        Failing checks come back as `status == "fail"` rather than raising.
        """
        response = get_healthcheck.sync_detailed(client=self._client)
        return _unwrap(response, ok=_HEALTHCHECK_OK)

    def headways(
        self, date: DateLike, *, stop: OneOrMany | None = None
    ) -> list[HeadwayEvent]:
        """Time between consecutive departures from `stop` on `date`.

        Returns one event per departure. `stop` is one or more MBTA stop IDs,
        e.g. `"70061"`.
        """
        response = get_headways.sync_detailed(
            _to_date(date), client=self._client, stop=_to_list(stop)
        )
        return _unwrap(response)

    def dwells(
        self, date: DateLike, *, stop: OneOrMany | None = None
    ) -> list[DwellEvent]:
        """Time vehicles spent stopped at `stop` on `date`.

        Returns one event per stop a vehicle made. `stop` is one or more MBTA
        stop IDs, e.g. `"70061"`.
        """
        response = get_dwells.sync_detailed(
            _to_date(date), client=self._client, stop=_to_list(stop)
        )
        return _unwrap(response)

    def travel_times(
        self,
        date: DateLike,
        *,
        from_stop: OneOrMany | None = None,
        to_stop: OneOrMany | None = None,
    ) -> list[TravelTimeEvent]:
        """Travel time of each trip from `from_stop` to `to_stop` on `date`.

        Returns one event per trip. Both are one or more MBTA stop IDs, e.g.
        `"70061"`, and must be platforms for the same direction of travel.
        """
        response = get_travel_times.sync_detailed(
            _to_date(date),
            client=self._client,
            from_stop=_to_list(from_stop),
            to_stop=_to_list(to_stop),
        )
        return _unwrap(response)

    def historical_alerts(
        self, date: DateLike, *, route: OneOrMany | None = None
    ) -> list[Alert]:
        """Alerts that were active on `date` for `route`.

        `route` is one or more MBTA route IDs, e.g. `"Red"` or `"66"`.
        """
        response = get_historical_alerts.sync_detailed(
            _to_date(date), client=self._client, route=_to_list(route)
        )
        return _unwrap(response)

    def aggregate_travel_times(
        self,
        start_date: DateLike,
        end_date: DateLike,
        *,
        from_stop: OneOrMany | None = None,
        to_stop: OneOrMany | None = None,
    ) -> list[AggregateByDate]:
        """Daily travel-time statistics between stops over an inclusive date range.

        Returns one entry per service date and peak period. Stop IDs work as
        in `travel_times`.
        """
        response = get_aggregate_travel_times.sync_detailed(
            client=self._client,
            start_date=_to_date(start_date),
            end_date=_to_date(end_date),
            from_stop=_to_list(from_stop),
            to_stop=_to_list(to_stop),
        )
        return _unwrap(response)

    def aggregate_travel_times_v2(
        self,
        start_date: DateLike,
        end_date: DateLike,
        *,
        from_stop: OneOrMany | None = None,
        to_stop: OneOrMany | None = None,
    ) -> TravelTimeAggregate2Response:
        """Travel-time statistics between stops, by date and by time of day.

        `by_date` matches `aggregate_travel_times`; `by_time` groups trips into
        30-minute departure-time buckets across the whole range.
        """
        response = get_aggregate_travel_times_v2.sync_detailed(
            client=self._client,
            start_date=_to_date(start_date),
            end_date=_to_date(end_date),
            from_stop=_to_list(from_stop),
            to_stop=_to_list(to_stop),
        )
        return _unwrap(response)

    def aggregate_headways(
        self,
        start_date: DateLike,
        end_date: DateLike,
        *,
        stop: OneOrMany | None = None,
    ) -> list[HeadwayAggregateByDate]:
        """Daily headway statistics for `stop` over an inclusive date range.

        Returns one entry per service date, with bunching and on-time counts.
        """
        response = get_aggregate_headways.sync_detailed(
            client=self._client,
            start_date=_to_date(start_date),
            end_date=_to_date(end_date),
            stop=_to_list(stop),
        )
        return _unwrap(response)

    def aggregate_dwells(
        self,
        start_date: DateLike,
        end_date: DateLike,
        *,
        stop: OneOrMany | None = None,
    ) -> list[AggregateByDate]:
        """Daily dwell-time statistics for `stop` over an inclusive date range.

        Returns one entry per service date and peak period.
        """
        response = get_aggregate_dwells.sync_detailed(
            client=self._client,
            start_date=_to_date(start_date),
            end_date=_to_date(end_date),
            stop=_to_list(stop),
        )
        return _unwrap(response)

    def current_alerts(self) -> list[LiveAlert]:
        """Alerts in effect right now, live from the MBTA."""
        response = get_current_alerts.sync_detailed(client=self._client)
        return _unwrap(response)

    def line_delays(
        self,
        start_date: DateLike,
        end_date: DateLike,
        *,
        line: str,
        agg: Literal["daily", "weekly"] = "weekly",
    ) -> list[LineDelayEntry]:
        """Alert-attributed delays on `line` over an inclusive date range.

        Returns one entry per day or week, with minutes of delay by cause.
        `line` is e.g. `"Red"` or `"CR-Fairmount"`.
        """
        response = get_line_delays.sync_detailed(
            client=self._client,
            start_date=_to_date(start_date),
            end_date=_to_date(end_date),
            line=line,
            agg=GetLineDelaysAgg(agg),
        )
        return _unwrap(response)

    def trip_metrics(
        self,
        start_date: DateLike,
        end_date: DateLike,
        *,
        line: str,
        agg: Agg,
    ) -> list[TripMetricsEntry]:
        """Speed and travel-time metrics for `line` over an inclusive date range.

        Returns one entry per day, week, or month. `line` is a rapid transit
        line, e.g. `"line-red"`.
        """
        response = get_trip_metrics.sync_detailed(
            client=self._client,
            start_date=_to_date(start_date),
            end_date=_to_date(end_date),
            line=line,
            agg=GetTripMetricsAgg(agg),
        )
        return _unwrap(response)

    def scheduled_service(
        self,
        start_date: DateLike,
        end_date: DateLike,
        *,
        route_id: str,
        agg: Agg,
    ) -> GetScheduledServiceResponse:
        """Scheduled trip counts for a route over an inclusive date range.

        `counts` has one entry per day, week, or month. `route_id` is an MBTA
        route ID, e.g. `"Red"` or `"66"`.
        """
        response = get_scheduled_service.sync_detailed(
            client=self._client,
            start_date=_to_date(start_date),
            end_date=_to_date(end_date),
            route_id=route_id,
            agg=GetScheduledServiceAgg(agg),
        )
        return _unwrap(response)

    def ridership(
        self,
        start_date: DateLike,
        end_date: DateLike,
        *,
        line_id: str,
    ) -> list[RidershipEntry]:
        """Ridership on a line over an inclusive date range.

        Returns one entry per week. `line_id` is e.g. `"line-Red"`,
        `"line-66"`, or `"line-Fairmount"`.
        """
        response = get_ridership.sync_detailed(
            client=self._client,
            start_date=_to_date(start_date),
            end_date=_to_date(end_date),
            line_id=line_id,
        )
        return _unwrap(response)

    def facilities(self) -> FacilitiesResponse:
        """Elevators and escalators, live from the MBTA."""
        response = get_facilities.sync_detailed(client=self._client)
        return _unwrap(response)

    def speed_restrictions(
        self, date: DateLike, *, line_id: str
    ) -> SpeedRestrictionsResponse:
        """Speed restrictions in effect on a rapid transit line on `date`.

        `line_id` is case-sensitive, e.g. `"line-Red"`.
        """
        response = get_speed_restrictions.sync_detailed(
            client=self._client, line_id=line_id, date=_to_date(date)
        )
        return _unwrap(response)

    def service_hours(
        self,
        start_date: DateLike,
        end_date: DateLike,
        *,
        line_id: str,
        agg: Agg,
    ) -> list[ServiceHoursEntry]:
        """Scheduled and delivered service hours on a line over a date range.

        Returns one entry per day, week, or month. `line_id` is a rapid
        transit line, e.g. `"line-red"`.
        """
        response = get_service_hours.sync_detailed(
            client=self._client,
            line_id=line_id,
            start_date=_to_date(start_date),
            end_date=_to_date(end_date),
            agg=GetServiceHoursAgg(agg),
        )
        return _unwrap(response)

    def time_predictions(self, route_id: str) -> list[TimePredictionWeek]:
        """Weekly arrival-prediction accuracy for a route, e.g. `"Red"`."""
        response = get_time_predictions.sync_detailed(
            client=self._client, route_id=route_id
        )
        return _unwrap(response)

    def service_ridership_dashboard(self) -> ServiceRidershipDashboardResponse:
        """Combined service and ridership data behind the overview dashboard."""
        response = get_service_ridership_dashboard.sync_detailed(client=self._client)
        return _unwrap(response)

    def routes(self) -> RoutesResponse:
        """All route IDs the dashboard supports, grouped by mode."""
        response = get_routes.sync_detailed(client=self._client)
        return _unwrap(response)

    def stops(self, route_id: str) -> StopsResponse:
        """Stations and stop IDs along a route, e.g. `"Red"`."""
        response = get_stops_for_route.sync_detailed(route_id, client=self._client)
        return _unwrap(response)


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

    async def healthcheck(self) -> HealthcheckResponse:
        """Run the API's health checks.

        Failing checks come back as `status == "fail"` rather than raising.
        """
        response = await get_healthcheck.asyncio_detailed(client=self._client)
        return _unwrap(response, ok=_HEALTHCHECK_OK)

    async def headways(
        self, date: DateLike, *, stop: OneOrMany | None = None
    ) -> list[HeadwayEvent]:
        """Time between consecutive departures from `stop` on `date`."""
        response = await get_headways.asyncio_detailed(
            _to_date(date), client=self._client, stop=_to_list(stop)
        )
        return _unwrap(response)

    async def dwells(
        self, date: DateLike, *, stop: OneOrMany | None = None
    ) -> list[DwellEvent]:
        """Time vehicles spent stopped at `stop` on `date`."""
        response = await get_dwells.asyncio_detailed(
            _to_date(date), client=self._client, stop=_to_list(stop)
        )
        return _unwrap(response)

    async def travel_times(
        self,
        date: DateLike,
        *,
        from_stop: OneOrMany | None = None,
        to_stop: OneOrMany | None = None,
    ) -> list[TravelTimeEvent]:
        """Travel time of each trip from `from_stop` to `to_stop` on `date`."""
        response = await get_travel_times.asyncio_detailed(
            _to_date(date),
            client=self._client,
            from_stop=_to_list(from_stop),
            to_stop=_to_list(to_stop),
        )
        return _unwrap(response)

    async def historical_alerts(
        self, date: DateLike, *, route: OneOrMany | None = None
    ) -> list[Alert]:
        """Alerts that were active on `date` for `route`."""
        response = await get_historical_alerts.asyncio_detailed(
            _to_date(date), client=self._client, route=_to_list(route)
        )
        return _unwrap(response)

    async def aggregate_travel_times(
        self,
        start_date: DateLike,
        end_date: DateLike,
        *,
        from_stop: OneOrMany | None = None,
        to_stop: OneOrMany | None = None,
    ) -> list[AggregateByDate]:
        """Daily travel-time statistics between stops over an inclusive date range."""
        response = await get_aggregate_travel_times.asyncio_detailed(
            client=self._client,
            start_date=_to_date(start_date),
            end_date=_to_date(end_date),
            from_stop=_to_list(from_stop),
            to_stop=_to_list(to_stop),
        )
        return _unwrap(response)

    async def aggregate_travel_times_v2(
        self,
        start_date: DateLike,
        end_date: DateLike,
        *,
        from_stop: OneOrMany | None = None,
        to_stop: OneOrMany | None = None,
    ) -> TravelTimeAggregate2Response:
        """Travel-time statistics between stops, by date and by time of day."""
        response = await get_aggregate_travel_times_v2.asyncio_detailed(
            client=self._client,
            start_date=_to_date(start_date),
            end_date=_to_date(end_date),
            from_stop=_to_list(from_stop),
            to_stop=_to_list(to_stop),
        )
        return _unwrap(response)

    async def aggregate_headways(
        self,
        start_date: DateLike,
        end_date: DateLike,
        *,
        stop: OneOrMany | None = None,
    ) -> list[HeadwayAggregateByDate]:
        """Daily headway statistics for `stop` over an inclusive date range."""
        response = await get_aggregate_headways.asyncio_detailed(
            client=self._client,
            start_date=_to_date(start_date),
            end_date=_to_date(end_date),
            stop=_to_list(stop),
        )
        return _unwrap(response)

    async def aggregate_dwells(
        self,
        start_date: DateLike,
        end_date: DateLike,
        *,
        stop: OneOrMany | None = None,
    ) -> list[AggregateByDate]:
        """Daily dwell-time statistics for `stop` over an inclusive date range."""
        response = await get_aggregate_dwells.asyncio_detailed(
            client=self._client,
            start_date=_to_date(start_date),
            end_date=_to_date(end_date),
            stop=_to_list(stop),
        )
        return _unwrap(response)

    async def current_alerts(self) -> list[LiveAlert]:
        """Alerts in effect right now, live from the MBTA."""
        response = await get_current_alerts.asyncio_detailed(client=self._client)
        return _unwrap(response)

    async def line_delays(
        self,
        start_date: DateLike,
        end_date: DateLike,
        *,
        line: str,
        agg: Literal["daily", "weekly"] = "weekly",
    ) -> list[LineDelayEntry]:
        """Alert-attributed delays on `line` over an inclusive date range."""
        response = await get_line_delays.asyncio_detailed(
            client=self._client,
            start_date=_to_date(start_date),
            end_date=_to_date(end_date),
            line=line,
            agg=GetLineDelaysAgg(agg),
        )
        return _unwrap(response)

    async def trip_metrics(
        self,
        start_date: DateLike,
        end_date: DateLike,
        *,
        line: str,
        agg: Agg,
    ) -> list[TripMetricsEntry]:
        """Speed and travel-time metrics for `line` over an inclusive date range."""
        response = await get_trip_metrics.asyncio_detailed(
            client=self._client,
            start_date=_to_date(start_date),
            end_date=_to_date(end_date),
            line=line,
            agg=GetTripMetricsAgg(agg),
        )
        return _unwrap(response)

    async def scheduled_service(
        self,
        start_date: DateLike,
        end_date: DateLike,
        *,
        route_id: str,
        agg: Agg,
    ) -> GetScheduledServiceResponse:
        """Scheduled trip counts for a route over an inclusive date range."""
        response = await get_scheduled_service.asyncio_detailed(
            client=self._client,
            start_date=_to_date(start_date),
            end_date=_to_date(end_date),
            route_id=route_id,
            agg=GetScheduledServiceAgg(agg),
        )
        return _unwrap(response)

    async def ridership(
        self,
        start_date: DateLike,
        end_date: DateLike,
        *,
        line_id: str,
    ) -> list[RidershipEntry]:
        """Ridership on a line over an inclusive date range."""
        response = await get_ridership.asyncio_detailed(
            client=self._client,
            start_date=_to_date(start_date),
            end_date=_to_date(end_date),
            line_id=line_id,
        )
        return _unwrap(response)

    async def facilities(self) -> FacilitiesResponse:
        """Elevators and escalators, live from the MBTA."""
        response = await get_facilities.asyncio_detailed(client=self._client)
        return _unwrap(response)

    async def speed_restrictions(
        self, date: DateLike, *, line_id: str
    ) -> SpeedRestrictionsResponse:
        """Speed restrictions in effect on a rapid transit line on `date`."""
        response = await get_speed_restrictions.asyncio_detailed(
            client=self._client, line_id=line_id, date=_to_date(date)
        )
        return _unwrap(response)

    async def service_hours(
        self,
        start_date: DateLike,
        end_date: DateLike,
        *,
        line_id: str,
        agg: Agg,
    ) -> list[ServiceHoursEntry]:
        """Scheduled and delivered service hours on a line over a date range."""
        response = await get_service_hours.asyncio_detailed(
            client=self._client,
            line_id=line_id,
            start_date=_to_date(start_date),
            end_date=_to_date(end_date),
            agg=GetServiceHoursAgg(agg),
        )
        return _unwrap(response)

    async def time_predictions(self, route_id: str) -> list[TimePredictionWeek]:
        """Weekly arrival-prediction accuracy for a route."""
        response = await get_time_predictions.asyncio_detailed(
            client=self._client, route_id=route_id
        )
        return _unwrap(response)

    async def service_ridership_dashboard(self) -> ServiceRidershipDashboardResponse:
        """Combined service and ridership data behind the overview dashboard."""
        response = await get_service_ridership_dashboard.asyncio_detailed(
            client=self._client
        )
        return _unwrap(response)

    async def routes(self) -> RoutesResponse:
        """All route IDs the dashboard supports, grouped by mode."""
        response = await get_routes.asyncio_detailed(client=self._client)
        return _unwrap(response)

    async def stops(self, route_id: str) -> StopsResponse:
        """Stations and stop IDs along a route."""
        response = await get_stops_for_route.asyncio_detailed(
            route_id, client=self._client
        )
        return _unwrap(response)
