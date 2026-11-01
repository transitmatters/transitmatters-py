"""Exceptions raised by the TransitMatters client.

```
TransitMattersError
├── APIError             the API responded with an error status
│   ├── BadRequestError    400: a parameter is missing or invalid
│   ├── RangeTooLongError  403: the date range has too many entries
│   ├── NotFoundError      404: no route has this ID
│   └── ServerError        5xx: the API failed
└── NetworkError         no usable response: connection failure, timeout, etc.
```
"""

from __future__ import annotations


class TransitMattersError(Exception):
    """Base class for all errors raised by this library."""


class APIError(TransitMattersError):
    """The API responded with an error status.

    Attributes:
        status_code: HTTP status of the response.
        message: Description of the problem, taken from the response body.
        code: Error type reported by the API (e.g. `BadRequestError`), if any.
        content: Raw response body.
    """

    def __init__(
        self,
        status_code: int,
        message: str,
        *,
        code: str | None = None,
        content: bytes = b"",
    ) -> None:
        self.status_code = status_code
        self.message = message
        self.code = code
        self.content = content
        prefix = f"{status_code} {code}" if code else str(status_code)
        super().__init__(f"{prefix}: {message}")


class BadRequestError(APIError):
    """The API rejected a parameter as missing or invalid (HTTP 400)."""


class RangeTooLongError(APIError):
    """The date range is too long for the endpoint (HTTP 403).

    The trip metrics methods, such as `TransitMatters.trip_metrics`, split
    long ranges to avoid this. `TransitMatters.bus_speed_leaderboard` can't,
    so it raises this for ranges over 150 days.
    """


class NotFoundError(APIError):
    """The requested route doesn't exist (HTTP 404)."""


class ServerError(APIError):
    """The API failed to handle the request (HTTP 5xx)."""


class NetworkError(TransitMattersError):
    """The request failed before a response arrived, e.g. a timeout.

    The underlying `httpx` exception is the `__cause__`.
    """
