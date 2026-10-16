from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_response import ErrorResponse
from ...models.travel_time_aggregate_2_response import TravelTimeAggregate2Response
from ...types import Unset
import datetime


def _get_kwargs(
    *,
    start_date: datetime.date,
    end_date: datetime.date,
    from_stop: list[str] | Unset = UNSET,
    to_stop: list[str] | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_start_date = start_date.isoformat()
    params["start_date"] = json_start_date

    json_end_date = end_date.isoformat()
    params["end_date"] = json_end_date

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
        "url": "/api/aggregate/traveltimes2",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | TravelTimeAggregate2Response | None:
    if response.status_code == 200:
        response_200 = TravelTimeAggregate2Response.from_dict(response.json())

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
) -> Response[ErrorResponse | TravelTimeAggregate2Response]:
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
    from_stop: list[str] | Unset = UNSET,
    to_stop: list[str] | Unset = UNSET,
) -> Response[ErrorResponse | TravelTimeAggregate2Response]:
    """Retrieve aggregated travel time data with by-time-of-day and by-date breakdowns.

    Args:
        start_date (datetime.date):
        end_date (datetime.date):
        from_stop (list[str] | Unset):
        to_stop (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | TravelTimeAggregate2Response]
    """

    kwargs = _get_kwargs(
        start_date=start_date,
        end_date=end_date,
        from_stop=from_stop,
        to_stop=to_stop,
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
    from_stop: list[str] | Unset = UNSET,
    to_stop: list[str] | Unset = UNSET,
) -> ErrorResponse | TravelTimeAggregate2Response | None:
    """Retrieve aggregated travel time data with by-time-of-day and by-date breakdowns.

    Args:
        start_date (datetime.date):
        end_date (datetime.date):
        from_stop (list[str] | Unset):
        to_stop (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | TravelTimeAggregate2Response
    """

    return sync_detailed(
        client=client,
        start_date=start_date,
        end_date=end_date,
        from_stop=from_stop,
        to_stop=to_stop,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    start_date: datetime.date,
    end_date: datetime.date,
    from_stop: list[str] | Unset = UNSET,
    to_stop: list[str] | Unset = UNSET,
) -> Response[ErrorResponse | TravelTimeAggregate2Response]:
    """Retrieve aggregated travel time data with by-time-of-day and by-date breakdowns.

    Args:
        start_date (datetime.date):
        end_date (datetime.date):
        from_stop (list[str] | Unset):
        to_stop (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | TravelTimeAggregate2Response]
    """

    kwargs = _get_kwargs(
        start_date=start_date,
        end_date=end_date,
        from_stop=from_stop,
        to_stop=to_stop,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    start_date: datetime.date,
    end_date: datetime.date,
    from_stop: list[str] | Unset = UNSET,
    to_stop: list[str] | Unset = UNSET,
) -> ErrorResponse | TravelTimeAggregate2Response | None:
    """Retrieve aggregated travel time data with by-time-of-day and by-date breakdowns.

    Args:
        start_date (datetime.date):
        end_date (datetime.date):
        from_stop (list[str] | Unset):
        to_stop (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | TravelTimeAggregate2Response
    """

    return (
        await asyncio_detailed(
            client=client,
            start_date=start_date,
            end_date=end_date,
            from_stop=from_stop,
            to_stop=to_stop,
        )
    ).parsed
