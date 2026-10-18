"""Python client for the TransitMatters Data Dashboard API.

.. include:: ../../README.md
   :start-after: <!-- The API docs include this file from here down. -->
"""

from . import models
from ._dataframe import to_dataframe
from .client import DEFAULT_BASE_URL, AsyncTransitMatters, TransitMatters
from .errors import (
    APIError,
    BadRequestError,
    NetworkError,
    NotFoundError,
    RangeTooLongError,
    ServerError,
    TransitMattersError,
)
from .lines import Line

__docformat__ = "google"

# Ordered for the API docs, which list members in this order.
__all__ = [  # noqa: RUF022
    "TransitMatters",
    "AsyncTransitMatters",
    "Line",
    "to_dataframe",
    "TransitMattersError",
    "APIError",
    "BadRequestError",
    "NotFoundError",
    "RangeTooLongError",
    "ServerError",
    "NetworkError",
    "DEFAULT_BASE_URL",
    "models",
]
