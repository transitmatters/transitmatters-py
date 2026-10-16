from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.route_not_found_response import RouteNotFoundResponse
from ...models.stops_response import StopsResponse


def _get_kwargs(
    route_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/stops/{route_id}".format(
            route_id=quote(str(route_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> RouteNotFoundResponse | StopsResponse | None:
    if response.status_code == 200:
        response_200 = StopsResponse.from_dict(response.json())

        return response_200

    if response.status_code == 404:
        response_404 = RouteNotFoundResponse.from_dict(response.json())

        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[RouteNotFoundResponse | StopsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    route_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[RouteNotFoundResponse | StopsResponse]:
    """Get the stop information for a specific route.

     Args:
        route_id: The route ID to look up stops for.

    Returns:
        Response: JSON response containing station/stop data including names, IDs,
            and directions, or a 404 response if the route is not found.

    Args:
        route_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RouteNotFoundResponse | StopsResponse]
    """

    kwargs = _get_kwargs(
        route_id=route_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    route_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> RouteNotFoundResponse | StopsResponse | None:
    """Get the stop information for a specific route.

     Args:
        route_id: The route ID to look up stops for.

    Returns:
        Response: JSON response containing station/stop data including names, IDs,
            and directions, or a 404 response if the route is not found.

    Args:
        route_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RouteNotFoundResponse | StopsResponse
    """

    return sync_detailed(
        route_id=route_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    route_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[RouteNotFoundResponse | StopsResponse]:
    """Get the stop information for a specific route.

     Args:
        route_id: The route ID to look up stops for.

    Returns:
        Response: JSON response containing station/stop data including names, IDs,
            and directions, or a 404 response if the route is not found.

    Args:
        route_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RouteNotFoundResponse | StopsResponse]
    """

    kwargs = _get_kwargs(
        route_id=route_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    route_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> RouteNotFoundResponse | StopsResponse | None:
    """Get the stop information for a specific route.

     Args:
        route_id: The route ID to look up stops for.

    Returns:
        Response: JSON response containing station/stop data including names, IDs,
            and directions, or a 404 response if the route is not found.

    Args:
        route_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RouteNotFoundResponse | StopsResponse
    """

    return (
        await asyncio_detailed(
            route_id=route_id,
            client=client,
        )
    ).parsed
