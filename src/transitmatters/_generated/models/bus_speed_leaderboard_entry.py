from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


T = TypeVar("T", bound="BusSpeedLeaderboardEntry")


@_attrs_define
class BusSpeedLeaderboardEntry:
    """A bus route's totals over the date range. Speed in mph is `miles_covered / (total_time / 3600)`.

    Attributes:
        route: Route ID.
        count: Trips delivered.
        total_time: Total trip time in seconds.
        miles_covered: Total miles covered.
        n_traversals: Segment traversals measured.

    """

    route: str
    count: float
    total_time: float
    miles_covered: float
    n_traversals: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        route = self.route

        count = self.count

        total_time = self.total_time

        miles_covered = self.miles_covered

        n_traversals = self.n_traversals

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "route": route,
                "count": count,
                "total_time": total_time,
                "miles_covered": miles_covered,
                "n_traversals": n_traversals,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        route = d.pop("route")

        count = d.pop("count")

        total_time = d.pop("total_time")

        miles_covered = d.pop("miles_covered")

        n_traversals = d.pop("n_traversals")

        bus_speed_leaderboard_entry = cls(
            route=route,
            count=count,
            total_time=total_time,
            miles_covered=miles_covered,
            n_traversals=n_traversals,
        )

        bus_speed_leaderboard_entry.additional_properties = d
        return bus_speed_leaderboard_entry

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
