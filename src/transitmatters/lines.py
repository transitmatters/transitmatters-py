"""Rapid transit lines, and the ID each endpoint expects for them.

Endpoints spell the same line differently: the Red Line is `"Red"` to
`stops`, `"line-red"` to `trip_metrics`, and `"line-Red"` to `ridership`.
Pass a `Line` and the client sends the right one.
"""

from __future__ import annotations

from collections.abc import Sequence
from enum import Enum

_GREEN_BRANCHES = ("Green-B", "Green-C", "Green-D", "Green-E")


class Line(Enum):
    """A rapid transit line.

    Methods that take a route or line ID also take a `Line`. Strings are
    passed through unchanged, so use them for buses (`"66"`), commuter rail
    (`"CR-Fairmount"`), ferries, and Green Line branches (`"Green-B"`).
    """

    RED = "Red"
    ORANGE = "Orange"
    BLUE = "Blue"
    GREEN = "Green"
    MATTAPAN = "Mattapan"

    @property
    def route_id(self) -> str:
        """Route ID, e.g. `"Red"`, as `stops` and `scheduled_service` expect."""
        return self.value

    @property
    def key(self) -> str:
        """Lowercase line key, e.g. `"line-red"`, as `trip_metrics` and
        `service_hours` expect."""
        return f"line-{self.value.lower()}"

    @property
    def gtfs_line_id(self) -> str:
        """GTFS line ID, e.g. `"line-Red"`, as `ridership` and
        `speed_restrictions` expect."""
        return f"line-{self.value}"

    @property
    def branches(self) -> tuple[str, ...]:
        """Route IDs of the line's branches: `("Green-B", ...)` for the Green
        Line, empty for the others."""
        return _GREEN_BRANCHES if self is Line.GREEN else ()


RouteLike = Line | str
"""A `Line`, or a route ID string such as `"66"` or `"CR-Fairmount"`."""


def route_id(value: RouteLike, *, method: str | None = None) -> str:
    """The route ID for `value`.

    `method` names a method that only accepts Green Line branches, so that
    passing `Line.GREEN` raises instead of sending a request that fails.
    """
    if not isinstance(value, Line):
        return value
    if method and value.branches:
        branches = ", ".join(repr(b) for b in value.branches)
        raise ValueError(
            f"{method} takes a single Green Line branch, not Line.GREEN: one of {branches}"
        )
    return value.route_id


def route_ids(values: RouteLike | Sequence[RouteLike] | None) -> list[str] | None:
    if values is None:
        return None
    if isinstance(values, Line | str):
        values = [values]
    return [route_id(v) for v in values]


def line_key(value: RouteLike) -> str:
    return value.key if isinstance(value, Line) else value


def gtfs_line_id(value: RouteLike) -> str:
    return value.gtfs_line_id if isinstance(value, Line) else value
