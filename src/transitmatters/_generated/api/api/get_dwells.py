from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.dwell_event import DwellEvent
from ...models.error_response import ErrorResponse
from ...types import Unset
import datetime


def _get_kwargs(
    user_date: datetime.date,
    *,
    stop: list[str] | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_stop: list[str] | Unset = UNSET
    if not isinstance(stop, Unset):
        json_stop = stop

    params["stop"] = json_stop

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/dwells/{user_date}".format(
            user_date=quote(str(user_date), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | list[DwellEvent] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_dwell_response_item_data in _response_200:
            componentsschemas_dwell_response_item = DwellEvent.from_dict(
                componentsschemas_dwell_response_item_data
            )

            response_200.append(componentsschemas_dwell_response_item)

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
) -> Response[ErrorResponse | list[DwellEvent]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    user_date: datetime.date,
    *,
    client: AuthenticatedClient | Client,
    stop: list[str] | Unset = UNSET,
) -> Response[ErrorResponse | list[DwellEvent]]:
    """Retrieve dwell time data for the given date and stop(s).

     Args:
      user_date: Date string in "YYYY-MM-DD" format.
      Query params - stop: One or more stop IDs.

    Returns:
      Response: JSON response containing dwell time event data.

    Args:
        user_date (datetime.date):
        stop (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | list[DwellEvent]]
    """

    kwargs = _get_kwargs(
        user_date=user_date,
        stop=stop,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    user_date: datetime.date,
    *,
    client: AuthenticatedClient | Client,
    stop: list[str] | Unset = UNSET,
) -> ErrorResponse | list[DwellEvent] | None:
    """Retrieve dwell time data for the given date and stop(s).

     Args:
      user_date: Date string in "YYYY-MM-DD" format.
      Query params - stop: One or more stop IDs.

    Returns:
      Response: JSON response containing dwell time event data.

    Args:
        user_date (datetime.date):
        stop (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | list[DwellEvent]
    """

    return sync_detailed(
        user_date=user_date,
        client=client,
        stop=stop,
    ).parsed


async def asyncio_detailed(
    user_date: datetime.date,
    *,
    client: AuthenticatedClient | Client,
    stop: list[str] | Unset = UNSET,
) -> Response[ErrorResponse | list[DwellEvent]]:
    """Retrieve dwell time data for the given date and stop(s).

     Args:
      user_date: Date string in "YYYY-MM-DD" format.
      Query params - stop: One or more stop IDs.

    Returns:
      Response: JSON response containing dwell time event data.

    Args:
        user_date (datetime.date):
        stop (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | list[DwellEvent]]
    """

    kwargs = _get_kwargs(
        user_date=user_date,
        stop=stop,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    user_date: datetime.date,
    *,
    client: AuthenticatedClient | Client,
    stop: list[str] | Unset = UNSET,
) -> ErrorResponse | list[DwellEvent] | None:
    """Retrieve dwell time data for the given date and stop(s).

     Args:
      user_date: Date string in "YYYY-MM-DD" format.
      Query params - stop: One or more stop IDs.

    Returns:
      Response: JSON response containing dwell time event data.

    Args:
        user_date (datetime.date):
        stop (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | list[DwellEvent]
    """

    return (
        await asyncio_detailed(
            user_date=user_date,
            client=client,
            stop=stop,
        )
    ).parsed
