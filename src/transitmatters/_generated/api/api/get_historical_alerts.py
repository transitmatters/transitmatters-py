from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.alert import Alert
from ...models.error_response import ErrorResponse
from ...types import Unset
import datetime


def _get_kwargs(
    user_date: datetime.date,
    *,
    route: list[str] | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_route: list[str] | Unset = UNSET
    if not isinstance(route, Unset):
        json_route = route

    params["route"] = json_route

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/alerts/{user_date}".format(
            user_date=quote(str(user_date), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | list[Alert] | None | None:
    if response.status_code == 200:

        def _parse_response_200(data: object) -> list[Alert] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                componentsschemas_alerts_route_response_type_0 = []
                _componentsschemas_alerts_route_response_type_0 = data
                for (
                    componentsschemas_alerts_route_response_type_0_item_data
                ) in _componentsschemas_alerts_route_response_type_0:
                    componentsschemas_alerts_route_response_type_0_item = (
                        Alert.from_dict(
                            componentsschemas_alerts_route_response_type_0_item_data
                        )
                    )

                    componentsschemas_alerts_route_response_type_0.append(
                        componentsschemas_alerts_route_response_type_0_item
                    )

                return componentsschemas_alerts_route_response_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[Alert] | None, data)

        response_200 = _parse_response_200(response.json())

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
) -> Response[ErrorResponse | list[Alert] | None]:
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
    route: list[str] | Unset = UNSET,
) -> Response[ErrorResponse | list[Alert] | None]:
    """Retrieve transit alerts for the given date and route(s).

     Args:
      user_date: Date string in "YYYY-MM-DD" format.
      Query params - route: One or more route IDs.

    Returns:
      Response: JSON response containing alert data.

    Args:
        user_date (datetime.date):
        route (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | list[Alert] | None]
    """

    kwargs = _get_kwargs(
        user_date=user_date,
        route=route,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    user_date: datetime.date,
    *,
    client: AuthenticatedClient | Client,
    route: list[str] | Unset = UNSET,
) -> ErrorResponse | list[Alert] | None | None:
    """Retrieve transit alerts for the given date and route(s).

     Args:
      user_date: Date string in "YYYY-MM-DD" format.
      Query params - route: One or more route IDs.

    Returns:
      Response: JSON response containing alert data.

    Args:
        user_date (datetime.date):
        route (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | list[Alert] | None
    """

    return sync_detailed(
        user_date=user_date,
        client=client,
        route=route,
    ).parsed


async def asyncio_detailed(
    user_date: datetime.date,
    *,
    client: AuthenticatedClient | Client,
    route: list[str] | Unset = UNSET,
) -> Response[ErrorResponse | list[Alert] | None]:
    """Retrieve transit alerts for the given date and route(s).

     Args:
      user_date: Date string in "YYYY-MM-DD" format.
      Query params - route: One or more route IDs.

    Returns:
      Response: JSON response containing alert data.

    Args:
        user_date (datetime.date):
        route (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | list[Alert] | None]
    """

    kwargs = _get_kwargs(
        user_date=user_date,
        route=route,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    user_date: datetime.date,
    *,
    client: AuthenticatedClient | Client,
    route: list[str] | Unset = UNSET,
) -> ErrorResponse | list[Alert] | None | None:
    """Retrieve transit alerts for the given date and route(s).

     Args:
      user_date: Date string in "YYYY-MM-DD" format.
      Query params - route: One or more route IDs.

    Returns:
      Response: JSON response containing alert data.

    Args:
        user_date (datetime.date):
        route (list[str] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | list[Alert] | None
    """

    return (
        await asyncio_detailed(
            user_date=user_date,
            client=client,
            route=route,
        )
    ).parsed
