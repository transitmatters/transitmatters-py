from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


T = TypeVar("T", bound="BusTripMetricsEntry")


@_attrs_define
class BusTripMetricsEntry:
    """Delivered trip metrics for a bus route (or group of routes) over one day, week or month.

    Entries can also have fleet fields: `fleet_trips` (trips with a known vehicle), `avg_bus_age`,
    `pct_<type>_trips` and per-propulsion shares named `fleet_mix_<type>` (e.g. `fleet_mix_hybrid`).
    These are omitted when unknown. Daily entries for the whole day (no `time_band`) also have
    `median_speed_mph` and `mean_speed_mph`.

    Attributes:
        date: Day, Monday of the week, or first day of the month (`YYYY-MM-DD`).
        route: Route ID, or the comma-separated group that was requested.
        count: Trips delivered.
        total_time: Total trip time in seconds.
        miles_covered: Total miles covered.
        n_traversals: Segment traversals measured.

    """

    date: str
    route: str
    count: float
    total_time: float
    miles_covered: float
    n_traversals: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        date = self.date

        route = self.route

        count = self.count

        total_time = self.total_time

        miles_covered = self.miles_covered

        n_traversals = self.n_traversals

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "date": date,
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
        date = d.pop("date")

        route = d.pop("route")

        count = d.pop("count")

        total_time = d.pop("total_time")

        miles_covered = d.pop("miles_covered")

        n_traversals = d.pop("n_traversals")

        bus_trip_metrics_entry = cls(
            date=date,
            route=route,
            count=count,
            total_time=total_time,
            miles_covered=miles_covered,
            n_traversals=n_traversals,
        )

        bus_trip_metrics_entry.additional_properties = d
        return bus_trip_metrics_entry

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
