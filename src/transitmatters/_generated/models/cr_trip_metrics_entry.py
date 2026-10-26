from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast


T = TypeVar("T", bound="CrTripMetricsEntry")


@_attrs_define
class CrTripMetricsEntry:
    """Commuter Rail fleet metrics for a route over one day, week or month.

    Entries also have per-fleet shares named `fleet_mix_<type>` (e.g. `fleet_mix_rotem`), and
    `avg_cab_car_age` when known.

    Attributes:
        date: Day, Monday of the week, or first day of the month (`YYYY-MM-DD`).
        route: Route ID, or `all`.
        fleet_trips: Trips with a known cab car.

    """

    date: str
    route: str
    fleet_trips: float | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        date = self.date

        route = self.route

        fleet_trips: float | None | Unset
        if isinstance(self.fleet_trips, Unset):
            fleet_trips = UNSET
        else:
            fleet_trips = self.fleet_trips

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "date": date,
                "route": route,
            }
        )
        if fleet_trips is not UNSET:
            field_dict["fleet_trips"] = fleet_trips

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        date = d.pop("date")

        route = d.pop("route")

        def _parse_fleet_trips(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        fleet_trips = _parse_fleet_trips(d.pop("fleet_trips", UNSET))

        cr_trip_metrics_entry = cls(
            date=date,
            route=route,
            fleet_trips=fleet_trips,
        )

        cr_trip_metrics_entry.additional_properties = d
        return cr_trip_metrics_entry

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
