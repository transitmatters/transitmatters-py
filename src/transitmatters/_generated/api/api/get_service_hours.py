from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_response import ErrorResponse
from ...models.get_service_hours_agg import GetServiceHoursAgg
from ...models.service_hours_entry import ServiceHoursEntry
import datetime


def _get_kwargs(
    *,
    line_id: str,
    start_date: datetime.date,
    end_date: datetime.date,
    agg: GetServiceHoursAgg,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["line_id"] = line_id

    json_start_date = start_date.isoformat()
    params["start_date"] = json_start_date

    json_end_date = end_date.isoformat()
    params["end_date"] = json_end_date

    json_agg = agg.value
    params["agg"] = json_agg

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/service_hours",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | list[ServiceHoursEntry] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_service_hours_response_item_data in _response_200:
            componentsschemas_service_hours_response_item = ServiceHoursEntry.from_dict(
                componentsschemas_service_hours_response_item_data
            )

            response_200.append(componentsschemas_service_hours_response_item)

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
) -> Response[ErrorResponse | list[ServiceHoursEntry]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    line_id: str,
    start_date: datetime.date,
    end_date: datetime.date,
    agg: GetServiceHoursAgg,
) -> Response[ErrorResponse | list[ServiceHoursEntry]]:
    """Retrieve delivered service hours for a line over a date range.

    Args:
        line_id (str):
        start_date (datetime.date):
        end_date (datetime.date):
        agg (GetServiceHoursAgg):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | list[ServiceHoursEntry]]
    """

    kwargs = _get_kwargs(
        line_id=line_id,
        start_date=start_date,
        end_date=end_date,
        agg=agg,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    line_id: str,
    start_date: datetime.date,
    end_date: datetime.date,
    agg: GetServiceHoursAgg,
) -> ErrorResponse | list[ServiceHoursEntry] | None:
    """Retrieve delivered service hours for a line over a date range.

    Args:
        line_id (str):
        start_date (datetime.date):
        end_date (datetime.date):
        agg (GetServiceHoursAgg):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | list[ServiceHoursEntry]
    """

    return sync_detailed(
        client=client,
        line_id=line_id,
        start_date=start_date,
        end_date=end_date,
        agg=agg,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    line_id: str,
    start_date: datetime.date,
    end_date: datetime.date,
    agg: GetServiceHoursAgg,
) -> Response[ErrorResponse | list[ServiceHoursEntry]]:
    """Retrieve delivered service hours for a line over a date range.

    Args:
        line_id (str):
        start_date (datetime.date):
        end_date (datetime.date):
        agg (GetServiceHoursAgg):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | list[ServiceHoursEntry]]
    """

    kwargs = _get_kwargs(
        line_id=line_id,
        start_date=start_date,
        end_date=end_date,
        agg=agg,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    line_id: str,
    start_date: datetime.date,
    end_date: datetime.date,
    agg: GetServiceHoursAgg,
) -> ErrorResponse | list[ServiceHoursEntry] | None:
    """Retrieve delivered service hours for a line over a date range.

    Args:
        line_id (str):
        start_date (datetime.date):
        end_date (datetime.date):
        agg (GetServiceHoursAgg):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | list[ServiceHoursEntry]
    """

    return (
        await asyncio_detailed(
            client=client,
            line_id=line_id,
            start_date=start_date,
            end_date=end_date,
            agg=agg,
        )
    ).parsed
