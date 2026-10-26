from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.bus_trip_metrics_entry import BusTripMetricsEntry
from ...models.error_response import ErrorResponse
from ...models.get_bus_trip_metrics_agg import GetBusTripMetricsAgg
from ...models.get_bus_trip_metrics_day_type import GetBusTripMetricsDayType
from ...models.get_bus_trip_metrics_time_band import GetBusTripMetricsTimeBand
from ...types import Unset
import datetime


def _get_kwargs(
    *,
    start_date: datetime.date,
    end_date: datetime.date,
    route: str,
    agg: GetBusTripMetricsAgg | Unset = GetBusTripMetricsAgg.DAILY,
    time_band: GetBusTripMetricsTimeBand | Unset = UNSET,
    day_type: GetBusTripMetricsDayType | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_start_date = start_date.isoformat()
    params["start_date"] = json_start_date

    json_end_date = end_date.isoformat()
    params["end_date"] = json_end_date

    params["route"] = route

    json_agg: str | Unset = UNSET
    if not isinstance(agg, Unset):
        json_agg = agg.value

    params["agg"] = json_agg

    json_time_band: str | Unset = UNSET
    if not isinstance(time_band, Unset):
        json_time_band = time_band.value

    params["time_band"] = json_time_band

    json_day_type: str | Unset = UNSET
    if not isinstance(day_type, Unset):
        json_day_type = day_type.value

    params["day_type"] = json_day_type

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/bustripmetrics",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | list[BusTripMetricsEntry] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_bus_trip_metrics_response_item_data in _response_200:
            componentsschemas_bus_trip_metrics_response_item = (
                BusTripMetricsEntry.from_dict(
                    componentsschemas_bus_trip_metrics_response_item_data
                )
            )

            response_200.append(componentsschemas_bus_trip_metrics_response_item)

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | list[BusTripMetricsEntry]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    start_date: datetime.date,
    end_date: datetime.date,
    route: str,
    agg: GetBusTripMetricsAgg | Unset = GetBusTripMetricsAgg.DAILY,
    time_band: GetBusTripMetricsTimeBand | Unset = UNSET,
    day_type: GetBusTripMetricsDayType | Unset = UNSET,
) -> Response[ErrorResponse | list[BusTripMetricsEntry]]:
    """Retrieve daily speed/trip metrics for a single bus route over a date range.

    Args:
        start_date (datetime.date):
        end_date (datetime.date):
        route (str):
        agg (GetBusTripMetricsAgg | Unset):  Default: GetBusTripMetricsAgg.DAILY.
        time_band (GetBusTripMetricsTimeBand | Unset):
        day_type (GetBusTripMetricsDayType | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | list[BusTripMetricsEntry]]
    """

    kwargs = _get_kwargs(
        start_date=start_date,
        end_date=end_date,
        route=route,
        agg=agg,
        time_band=time_band,
        day_type=day_type,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    start_date: datetime.date,
    end_date: datetime.date,
    route: str,
    agg: GetBusTripMetricsAgg | Unset = GetBusTripMetricsAgg.DAILY,
    time_band: GetBusTripMetricsTimeBand | Unset = UNSET,
    day_type: GetBusTripMetricsDayType | Unset = UNSET,
) -> ErrorResponse | list[BusTripMetricsEntry] | None:
    """Retrieve daily speed/trip metrics for a single bus route over a date range.

    Args:
        start_date (datetime.date):
        end_date (datetime.date):
        route (str):
        agg (GetBusTripMetricsAgg | Unset):  Default: GetBusTripMetricsAgg.DAILY.
        time_band (GetBusTripMetricsTimeBand | Unset):
        day_type (GetBusTripMetricsDayType | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | list[BusTripMetricsEntry]
    """

    return sync_detailed(
        client=client,
        start_date=start_date,
        end_date=end_date,
        route=route,
        agg=agg,
        time_band=time_band,
        day_type=day_type,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    start_date: datetime.date,
    end_date: datetime.date,
    route: str,
    agg: GetBusTripMetricsAgg | Unset = GetBusTripMetricsAgg.DAILY,
    time_band: GetBusTripMetricsTimeBand | Unset = UNSET,
    day_type: GetBusTripMetricsDayType | Unset = UNSET,
) -> Response[ErrorResponse | list[BusTripMetricsEntry]]:
    """Retrieve daily speed/trip metrics for a single bus route over a date range.

    Args:
        start_date (datetime.date):
        end_date (datetime.date):
        route (str):
        agg (GetBusTripMetricsAgg | Unset):  Default: GetBusTripMetricsAgg.DAILY.
        time_band (GetBusTripMetricsTimeBand | Unset):
        day_type (GetBusTripMetricsDayType | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | list[BusTripMetricsEntry]]
    """

    kwargs = _get_kwargs(
        start_date=start_date,
        end_date=end_date,
        route=route,
        agg=agg,
        time_band=time_band,
        day_type=day_type,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    start_date: datetime.date,
    end_date: datetime.date,
    route: str,
    agg: GetBusTripMetricsAgg | Unset = GetBusTripMetricsAgg.DAILY,
    time_band: GetBusTripMetricsTimeBand | Unset = UNSET,
    day_type: GetBusTripMetricsDayType | Unset = UNSET,
) -> ErrorResponse | list[BusTripMetricsEntry] | None:
    """Retrieve daily speed/trip metrics for a single bus route over a date range.

    Args:
        start_date (datetime.date):
        end_date (datetime.date):
        route (str):
        agg (GetBusTripMetricsAgg | Unset):  Default: GetBusTripMetricsAgg.DAILY.
        time_band (GetBusTripMetricsTimeBand | Unset):
        day_type (GetBusTripMetricsDayType | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | list[BusTripMetricsEntry]
    """

    return (
        await asyncio_detailed(
            client=client,
            start_date=start_date,
            end_date=end_date,
            route=route,
            agg=agg,
            time_band=time_band,
            day_type=day_type,
        )
    ).parsed
