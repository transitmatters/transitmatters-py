"""Exceptions raised by the TransitMatters client."""

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
