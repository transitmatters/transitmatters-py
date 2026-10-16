from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_response import ErrorResponse
from ...models.speed_restrictions_response import SpeedRestrictionsResponse
import datetime


def _get_kwargs(
    *,
    line_id: str,
    date: datetime.date,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["line_id"] = line_id

    json_date = date.isoformat()
    params["date"] = json_date

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/speed_restrictions",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | SpeedRestrictionsResponse | None:
    if response.status_code == 200:
        response_200 = SpeedRestrictionsResponse.from_dict(response.json())

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
) -> Response[ErrorResponse | SpeedRestrictionsResponse]:
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
    date: datetime.date,
) -> Response[ErrorResponse | SpeedRestrictionsResponse]:
    """Retrieve speed restriction data for a line on a given date.

    Args:
        line_id (str):
        date (datetime.date):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | SpeedRestrictionsResponse]
    """

    kwargs = _get_kwargs(
        line_id=line_id,
        date=date,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    line_id: str,
    date: datetime.date,
) -> ErrorResponse | SpeedRestrictionsResponse | None:
    """Retrieve speed restriction data for a line on a given date.

    Args:
        line_id (str):
        date (datetime.date):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | SpeedRestrictionsResponse
    """

    return sync_detailed(
        client=client,
        line_id=line_id,
        date=date,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    line_id: str,
    date: datetime.date,
) -> Response[ErrorResponse | SpeedRestrictionsResponse]:
    """Retrieve speed restriction data for a line on a given date.

    Args:
        line_id (str):
        date (datetime.date):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | SpeedRestrictionsResponse]
    """

    kwargs = _get_kwargs(
        line_id=line_id,
        date=date,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    line_id: str,
    date: datetime.date,
) -> ErrorResponse | SpeedRestrictionsResponse | None:
    """Retrieve speed restriction data for a line on a given date.

    Args:
        line_id (str):
        date (datetime.date):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | SpeedRestrictionsResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            line_id=line_id,
            date=date,
        )
    ).parsed
