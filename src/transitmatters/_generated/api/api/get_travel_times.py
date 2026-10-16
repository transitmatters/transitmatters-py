from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_response import ErrorResponse
from ...models.travel_time_event import TravelTimeEvent
from ...types import Unset
import datetime


def _get_kwargs(
    user_date: datetime.date,
    *,
    from_stop: list[str] | Unset = UNSET,
    to_stop: list[str] | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_from_stop: list[str] | Unset = UNSET
    if not isinstance(from_stop, Unset):
        json_from_stop = from_stop

    params["from_stop"] = json_from_stop

    json_to_stop: list[str] | Unset = UNSET
    if not isinstance(to_stop, Unset):
        json_to_stop = to_stop

    params["to_stop"] = json_to_stop

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/traveltimes/{user_date}".format(
            user_date=quote(str(user_date), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | list[TravelTimeEvent] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_travel_time_response_item_data in _response_200:
            componentsschemas_travel_time_response_item = TravelTimeEvent.from_dict(
                componentsschemas_travel_time_response_item_data
            )

            response_200.append(componentsschemas_travel_time_response_item)

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
) -> Response[ErrorResponse | list[TravelTimeEvent]]:
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
    from_stop: list[str] | Unset = UNSET,
    to_stop: list[str] | Unset = UNSET,
) -> Response[ErrorResponse | list[TravelTimeEvent]]:
    """Retrieve travel time data between stop pairs for the given date.

     Args:
      user_date: Date string in "YYYY-MM-DD" format.
      Query params - from_stop: One or more origin stop IDs.
      Query params - to_stop: One or more destination stop IDs.

    Returns:
      Response: JSON response containing travel time event data.

    Args:
        user_date (datetime.date):
        from_stop (list[str] | Unset):
        to_stop (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | list[TravelTimeEvent]]
    """

    kwargs = _get_kwargs(
        user_date=user_date,
        from_stop=from_stop,
        to_stop=to_stop,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    user_date: datetime.date,
    *,
    client: AuthenticatedClient | Client,
    from_stop: list[str] | Unset = UNSET,
    to_stop: list[str] | Unset = UNSET,
) -> ErrorResponse | list[TravelTimeEvent] | None:
    """Retrieve travel time data between stop pairs for the given date.

     Args:
      user_date: Date string in "YYYY-MM-DD" format.
      Query params - from_stop: One or more origin stop IDs.
      Query params - to_stop: One or more destination stop IDs.

    Returns:
      Response: JSON response containing travel time event data.

    Args:
        user_date (datetime.date):
        from_stop (list[str] | Unset):
        to_stop (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | list[TravelTimeEvent]
    """

    return sync_detailed(
        user_date=user_date,
        client=client,
        from_stop=from_stop,
        to_stop=to_stop,
    ).parsed


async def asyncio_detailed(
    user_date: datetime.date,
    *,
    client: AuthenticatedClient | Client,
    from_stop: list[str] | Unset = UNSET,
    to_stop: list[str] | Unset = UNSET,
) -> Response[ErrorResponse | list[TravelTimeEvent]]:
    """Retrieve travel time data between stop pairs for the given date.

     Args:
      user_date: Date string in "YYYY-MM-DD" format.
      Query params - from_stop: One or more origin stop IDs.
      Query params - to_stop: One or more destination stop IDs.

    Returns:
      Response: JSON response containing travel time event data.

    Args:
        user_date (datetime.date):
        from_stop (list[str] | Unset):
        to_stop (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | list[TravelTimeEvent]]
    """

    kwargs = _get_kwargs(
        user_date=user_date,
        from_stop=from_stop,
        to_stop=to_stop,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    user_date: datetime.date,
    *,
    client: AuthenticatedClient | Client,
    from_stop: list[str] | Unset = UNSET,
    to_stop: list[str] | Unset = UNSET,
) -> ErrorResponse | list[TravelTimeEvent] | None:
    """Retrieve travel time data between stop pairs for the given date.

     Args:
      user_date: Date string in "YYYY-MM-DD" format.
      Query params - from_stop: One or more origin stop IDs.
      Query params - to_stop: One or more destination stop IDs.

    Returns:
      Response: JSON response containing travel time event data.

    Args:
        user_date (datetime.date):
        from_stop (list[str] | Unset):
        to_stop (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | list[TravelTimeEvent]
    """

    return (
        await asyncio_detailed(
            user_date=user_date,
            client=client,
            from_stop=from_stop,
            to_stop=to_stop,
        )
    ).parsed
