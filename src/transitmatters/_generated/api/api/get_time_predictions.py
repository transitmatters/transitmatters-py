from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_response import ErrorResponse
from ...models.time_prediction_week import TimePredictionWeek
from ...types import Unset
import datetime


def _get_kwargs(
    *,
    route_id: str,
    start_date: datetime.date | None | Unset = UNSET,
    end_date: datetime.date | None | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["route_id"] = route_id

    json_start_date: None | str | Unset
    if isinstance(start_date, Unset):
        json_start_date = UNSET
    elif isinstance(start_date, datetime.date):
        json_start_date = start_date.isoformat()
    else:
        json_start_date = start_date
    params["start_date"] = json_start_date

    json_end_date: None | str | Unset
    if isinstance(end_date, Unset):
        json_end_date = UNSET
    elif isinstance(end_date, datetime.date):
        json_end_date = end_date.isoformat()
    else:
        json_end_date = end_date
    params["end_date"] = json_end_date

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/time_predictions",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | list[TimePredictionWeek] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_time_prediction_response_item_data in _response_200:
            componentsschemas_time_prediction_response_item = (
                TimePredictionWeek.from_dict(
                    componentsschemas_time_prediction_response_item_data
                )
            )

            response_200.append(componentsschemas_time_prediction_response_item)

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
) -> Response[ErrorResponse | list[TimePredictionWeek]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    route_id: str,
    start_date: datetime.date | None | Unset = UNSET,
    end_date: datetime.date | None | Unset = UNSET,
) -> Response[ErrorResponse | list[TimePredictionWeek]]:
    """Retrieve time prediction accuracy data for a route.

    Args:
        route_id (str):
        start_date (datetime.date | None | Unset):
        end_date (datetime.date | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | list[TimePredictionWeek]]
    """

    kwargs = _get_kwargs(
        route_id=route_id,
        start_date=start_date,
        end_date=end_date,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    route_id: str,
    start_date: datetime.date | None | Unset = UNSET,
    end_date: datetime.date | None | Unset = UNSET,
) -> ErrorResponse | list[TimePredictionWeek] | None:
    """Retrieve time prediction accuracy data for a route.

    Args:
        route_id (str):
        start_date (datetime.date | None | Unset):
        end_date (datetime.date | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | list[TimePredictionWeek]
    """

    return sync_detailed(
        client=client,
        route_id=route_id,
        start_date=start_date,
        end_date=end_date,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    route_id: str,
    start_date: datetime.date | None | Unset = UNSET,
    end_date: datetime.date | None | Unset = UNSET,
) -> Response[ErrorResponse | list[TimePredictionWeek]]:
    """Retrieve time prediction accuracy data for a route.

    Args:
        route_id (str):
        start_date (datetime.date | None | Unset):
        end_date (datetime.date | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | list[TimePredictionWeek]]
    """

    kwargs = _get_kwargs(
        route_id=route_id,
        start_date=start_date,
        end_date=end_date,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    route_id: str,
    start_date: datetime.date | None | Unset = UNSET,
    end_date: datetime.date | None | Unset = UNSET,
) -> ErrorResponse | list[TimePredictionWeek] | None:
    """Retrieve time prediction accuracy data for a route.

    Args:
        route_id (str):
        start_date (datetime.date | None | Unset):
        end_date (datetime.date | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | list[TimePredictionWeek]
    """

    return (
        await asyncio_detailed(
            client=client,
            route_id=route_id,
            start_date=start_date,
            end_date=end_date,
        )
    ).parsed
