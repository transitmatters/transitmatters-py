from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_response import ErrorResponse
from ...models.get_scheduled_service_agg import GetScheduledServiceAgg
from ...models.get_scheduled_service_response import GetScheduledServiceResponse
import datetime


def _get_kwargs(
    *,
    start_date: datetime.date,
    end_date: datetime.date,
    route_id: str,
    agg: GetScheduledServiceAgg,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_start_date = start_date.isoformat()
    params["start_date"] = json_start_date

    json_end_date = end_date.isoformat()
    params["end_date"] = json_end_date

    params["route_id"] = route_id

    json_agg = agg.value
    params["agg"] = json_agg

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/scheduledservice",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | GetScheduledServiceResponse | None:
    if response.status_code == 200:
        response_200 = GetScheduledServiceResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | GetScheduledServiceResponse]:
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
    route_id: str,
    agg: GetScheduledServiceAgg,
) -> Response[ErrorResponse | GetScheduledServiceResponse]:
    """Retrieve scheduled service counts for a route over a date range.

    Args:
        start_date (datetime.date):
        end_date (datetime.date):
        route_id (str):
        agg (GetScheduledServiceAgg):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | GetScheduledServiceResponse]
    """

    kwargs = _get_kwargs(
        start_date=start_date,
        end_date=end_date,
        route_id=route_id,
        agg=agg,
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
    route_id: str,
    agg: GetScheduledServiceAgg,
) -> ErrorResponse | GetScheduledServiceResponse | None:
    """Retrieve scheduled service counts for a route over a date range.

    Args:
        start_date (datetime.date):
        end_date (datetime.date):
        route_id (str):
        agg (GetScheduledServiceAgg):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | GetScheduledServiceResponse
    """

    return sync_detailed(
        client=client,
        start_date=start_date,
        end_date=end_date,
        route_id=route_id,
        agg=agg,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    start_date: datetime.date,
    end_date: datetime.date,
    route_id: str,
    agg: GetScheduledServiceAgg,
) -> Response[ErrorResponse | GetScheduledServiceResponse]:
    """Retrieve scheduled service counts for a route over a date range.

    Args:
        start_date (datetime.date):
        end_date (datetime.date):
        route_id (str):
        agg (GetScheduledServiceAgg):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | GetScheduledServiceResponse]
    """

    kwargs = _get_kwargs(
        start_date=start_date,
        end_date=end_date,
        route_id=route_id,
        agg=agg,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    start_date: datetime.date,
    end_date: datetime.date,
    route_id: str,
    agg: GetScheduledServiceAgg,
) -> ErrorResponse | GetScheduledServiceResponse | None:
    """Retrieve scheduled service counts for a route over a date range.

    Args:
        start_date (datetime.date):
        end_date (datetime.date):
        route_id (str):
        agg (GetScheduledServiceAgg):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | GetScheduledServiceResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            start_date=start_date,
            end_date=end_date,
            route_id=route_id,
            agg=agg,
        )
    ).parsed
