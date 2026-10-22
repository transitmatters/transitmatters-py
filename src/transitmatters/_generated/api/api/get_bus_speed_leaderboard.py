from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.bus_speed_leaderboard_entry import BusSpeedLeaderboardEntry
from ...models.error_response import ErrorResponse
from ...types import Unset
import datetime


def _get_kwargs(
    *,
    start_date: datetime.date,
    end_date: datetime.date,
    limit: int | Unset = 10,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_start_date = start_date.isoformat()
    params["start_date"] = json_start_date

    json_end_date = end_date.isoformat()
    params["end_date"] = json_end_date

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/busspeedleaderboard",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | list[BusSpeedLeaderboardEntry] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_bus_speed_leaderboard_response_item_data in _response_200:
            componentsschemas_bus_speed_leaderboard_response_item = (
                BusSpeedLeaderboardEntry.from_dict(
                    componentsschemas_bus_speed_leaderboard_response_item_data
                )
            )

            response_200.append(componentsschemas_bus_speed_leaderboard_response_item)

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
) -> Response[ErrorResponse | list[BusSpeedLeaderboardEntry]]:
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
    limit: int | Unset = 10,
) -> Response[ErrorResponse | list[BusSpeedLeaderboardEntry]]:
    """Retrieve the slowest bus routes (by average speed) over a date range.

    Args:
        start_date (datetime.date):
        end_date (datetime.date):
        limit (int | Unset):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | list[BusSpeedLeaderboardEntry]]
    """

    kwargs = _get_kwargs(
        start_date=start_date,
        end_date=end_date,
        limit=limit,
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
    limit: int | Unset = 10,
) -> ErrorResponse | list[BusSpeedLeaderboardEntry] | None:
    """Retrieve the slowest bus routes (by average speed) over a date range.

    Args:
        start_date (datetime.date):
        end_date (datetime.date):
        limit (int | Unset):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | list[BusSpeedLeaderboardEntry]
    """

    return sync_detailed(
        client=client,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    start_date: datetime.date,
    end_date: datetime.date,
    limit: int | Unset = 10,
) -> Response[ErrorResponse | list[BusSpeedLeaderboardEntry]]:
    """Retrieve the slowest bus routes (by average speed) over a date range.

    Args:
        start_date (datetime.date):
        end_date (datetime.date):
        limit (int | Unset):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | list[BusSpeedLeaderboardEntry]]
    """

    kwargs = _get_kwargs(
        start_date=start_date,
        end_date=end_date,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    start_date: datetime.date,
    end_date: datetime.date,
    limit: int | Unset = 10,
) -> ErrorResponse | list[BusSpeedLeaderboardEntry] | None:
    """Retrieve the slowest bus routes (by average speed) over a date range.

    Args:
        start_date (datetime.date):
        end_date (datetime.date):
        limit (int | Unset):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | list[BusSpeedLeaderboardEntry]
    """

    return (
        await asyncio_detailed(
            client=client,
            start_date=start_date,
            end_date=end_date,
            limit=limit,
        )
    ).parsed
