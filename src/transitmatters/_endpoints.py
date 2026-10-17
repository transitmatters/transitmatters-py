"""One request builder per endpoint, shared by the sync and async clients.

Each builder coerces its arguments and returns a `Call`: the request, ready
to send either way, plus how to turn a successful body into the public
return type. The clients only decide how to send it.
"""

from __future__ import annotations

import datetime
from collections.abc import Awaitable, Callable, Container, Sequence
from dataclasses import dataclass, replace
from functools import partial
from http import HTTPStatus
from typing import Any, Literal

from . import _convert as convert
from . import models as m
from ._convert import each
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
    GetLineDelaysAgg,
    GetScheduledServiceAgg,
    GetServiceHoursAgg,
    GetTripMetricsAgg,
)
from ._generated.types import UNSET, Response, Unset

DateLike = datetime.date | str
"""A date, or an ISO 8601 `YYYY-MM-DD` string."""

OneOrMany = str | Sequence[str]
"""A single ID, or several."""

Agg = Literal["daily", "weekly", "monthly"]

_OK = (HTTPStatus.OK,)
# The healthcheck reports failing checks with a 500 and a normal body.
_HEALTHCHECK_OK = (HTTPStatus.OK, HTTPStatus.INTERNAL_SERVER_ERROR)


@dataclass(frozen=True, slots=True)
class Call[T]:
    """A request to one endpoint, and how to convert its successful body."""

    sync: Callable[[], Response[Any]]
    asyncio: Callable[[], Awaitable[Response[Any]]]
    convert: Callable[[Any], T]
    ok: Container[int] = _OK
    """Statuses whose parsed body is a result rather than an error."""


def _call[**P, T](
    sync: Callable[P, Response[Any]],
    asyncio: Callable[P, Awaitable[Response[Any]]],
    convert: Callable[[Any], T],
    /,
    *args: P.args,
    **kwargs: P.kwargs,
) -> Call[T]:
    return Call(
        partial(sync, *args, **kwargs), partial(asyncio, *args, **kwargs), convert
    )


def to_date(value: DateLike) -> datetime.date:
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


def healthcheck(client: Client) -> Call[m.Healthcheck]:
    call = _call(
        get_healthcheck.sync_detailed,
        get_healthcheck.asyncio_detailed,
        convert.healthcheck,
        client=client,
    )
    return replace(call, ok=_HEALTHCHECK_OK)


def headways(
    client: Client, date: DateLike, *, stop: OneOrMany | None
) -> Call[list[m.Headway]]:
    return _call(
        get_headways.sync_detailed,
        get_headways.asyncio_detailed,
        each(convert.headway),
        to_date(date),
        client=client,
        stop=_to_list(stop),
    )


def dwells(
    client: Client, date: DateLike, *, stop: OneOrMany | None
) -> Call[list[m.Dwell]]:
    return _call(
        get_dwells.sync_detailed,
        get_dwells.asyncio_detailed,
        each(convert.dwell),
        to_date(date),
        client=client,
        stop=_to_list(stop),
    )


def travel_times(
    client: Client,
    date: DateLike,
    *,
    from_stop: OneOrMany | None,
    to_stop: OneOrMany | None,
) -> Call[list[m.TravelTime]]:
    return _call(
        get_travel_times.sync_detailed,
        get_travel_times.asyncio_detailed,
        each(convert.travel_time),
        to_date(date),
        client=client,
        from_stop=_to_list(from_stop),
        to_stop=_to_list(to_stop),
    )


def historical_alerts(
    client: Client, date: DateLike, *, route: OneOrMany | None
) -> Call[list[m.Alert]]:
    return _call(
        get_historical_alerts.sync_detailed,
        get_historical_alerts.asyncio_detailed,
        each(convert.alert),
        to_date(date),
        client=client,
        route=_to_list(route),
    )


def aggregate_travel_times(
    client: Client,
    start_date: DateLike,
    end_date: DateLike,
    *,
    from_stop: OneOrMany | None,
    to_stop: OneOrMany | None,
) -> Call[list[m.DailyStats]]:
    return _call(
        get_aggregate_travel_times.sync_detailed,
        get_aggregate_travel_times.asyncio_detailed,
        each(convert.daily_stats),
        client=client,
        start_date=to_date(start_date),
        end_date=to_date(end_date),
        from_stop=_to_list(from_stop),
        to_stop=_to_list(to_stop),
    )


def aggregate_travel_times_v2(
    client: Client,
    start_date: DateLike,
    end_date: DateLike,
    *,
    from_stop: OneOrMany | None,
    to_stop: OneOrMany | None,
) -> Call[m.TravelTimeStats]:
    return _call(
        get_aggregate_travel_times_v2.sync_detailed,
        get_aggregate_travel_times_v2.asyncio_detailed,
        convert.travel_time_stats,
        client=client,
        start_date=to_date(start_date),
        end_date=to_date(end_date),
        from_stop=_to_list(from_stop),
        to_stop=_to_list(to_stop),
    )


def aggregate_headways(
    client: Client,
    start_date: DateLike,
    end_date: DateLike,
    *,
    stop: OneOrMany | None,
) -> Call[list[m.DailyHeadwayStats]]:
    return _call(
        get_aggregate_headways.sync_detailed,
        get_aggregate_headways.asyncio_detailed,
        each(convert.daily_headway_stats),
        client=client,
        start_date=to_date(start_date),
        end_date=to_date(end_date),
        stop=_to_list(stop),
    )


def aggregate_dwells(
    client: Client,
    start_date: DateLike,
    end_date: DateLike,
    *,
    stop: OneOrMany | None,
) -> Call[list[m.DailyStats]]:
    return _call(
        get_aggregate_dwells.sync_detailed,
        get_aggregate_dwells.asyncio_detailed,
        each(convert.daily_stats),
        client=client,
        start_date=to_date(start_date),
        end_date=to_date(end_date),
        stop=_to_list(stop),
    )


def current_alerts(client: Client) -> Call[list[m.LiveAlert]]:
    return _call(
        get_current_alerts.sync_detailed,
        get_current_alerts.asyncio_detailed,
        each(convert.live_alert),
        client=client,
    )


def line_delays(
    client: Client,
    start_date: DateLike,
    end_date: DateLike,
    *,
    line: str,
    agg: Literal["daily", "weekly"],
) -> Call[list[m.LineDelays]]:
    return _call(
        get_line_delays.sync_detailed,
        get_line_delays.asyncio_detailed,
        each(convert.line_delays),
        client=client,
        start_date=to_date(start_date),
        end_date=to_date(end_date),
        line=line,
        agg=GetLineDelaysAgg(agg),
    )


def trip_metrics(
    client: Client,
    start_date: DateLike,
    end_date: DateLike,
    *,
    line: str,
    agg: Agg,
) -> Call[list[m.TripMetrics]]:
    return _call(
        get_trip_metrics.sync_detailed,
        get_trip_metrics.asyncio_detailed,
        each(convert.trip_metrics),
        client=client,
        start_date=to_date(start_date),
        end_date=to_date(end_date),
        line=line,
        agg=GetTripMetricsAgg(agg),
    )


def scheduled_service(
    client: Client,
    start_date: DateLike,
    end_date: DateLike,
    *,
    route_id: str,
    agg: Agg,
) -> Call[m.ScheduledService]:
    return _call(
        get_scheduled_service.sync_detailed,
        get_scheduled_service.asyncio_detailed,
        convert.scheduled_service,
        client=client,
        start_date=to_date(start_date),
        end_date=to_date(end_date),
        route_id=route_id,
        agg=GetScheduledServiceAgg(agg),
    )


def ridership(
    client: Client, start_date: DateLike, end_date: DateLike, *, line_id: str
) -> Call[list[m.Ridership]]:
    return _call(
        get_ridership.sync_detailed,
        get_ridership.asyncio_detailed,
        each(convert.ridership),
        client=client,
        start_date=to_date(start_date),
        end_date=to_date(end_date),
        line_id=line_id,
    )


def facilities(client: Client) -> Call[list[m.Facility]]:
    return _call(
        get_facilities.sync_detailed,
        get_facilities.asyncio_detailed,
        convert.facilities,
        client=client,
    )


def speed_restrictions(
    client: Client, date: DateLike, *, line_id: str
) -> Call[m.SpeedRestrictions]:
    return _call(
        get_speed_restrictions.sync_detailed,
        get_speed_restrictions.asyncio_detailed,
        convert.speed_restrictions,
        client=client,
        line_id=line_id,
        date=to_date(date),
    )


def service_hours(
    client: Client,
    start_date: DateLike,
    end_date: DateLike,
    *,
    line_id: str,
    agg: Agg,
) -> Call[list[m.ServiceHours]]:
    return _call(
        get_service_hours.sync_detailed,
        get_service_hours.asyncio_detailed,
        each(convert.service_hours),
        client=client,
        line_id=line_id,
        start_date=to_date(start_date),
        end_date=to_date(end_date),
        agg=GetServiceHoursAgg(agg),
    )


def time_predictions(client: Client, route_id: str) -> Call[list[m.TimePredictionWeek]]:
    return _call(
        get_time_predictions.sync_detailed,
        get_time_predictions.asyncio_detailed,
        each(convert.time_prediction_week),
        client=client,
        route_id=route_id,
    )


def service_ridership_dashboard(
    client: Client,
) -> Call[m.ServiceRidershipDashboard]:
    return _call(
        get_service_ridership_dashboard.sync_detailed,
        get_service_ridership_dashboard.asyncio_detailed,
        convert.service_ridership_dashboard,
        client=client,
    )


def routes(client: Client) -> Call[m.Routes]:
    return _call(
        get_routes.sync_detailed,
        get_routes.asyncio_detailed,
        convert.routes,
        client=client,
    )


def stops(client: Client, route_id: str) -> Call[m.RouteStops]:
    return _call(
        get_stops_for_route.sync_detailed,
        get_stops_for_route.asyncio_detailed,
        convert.route_stops,
        route_id,
        client=client,
    )
