from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast


T = TypeVar("T", bound="DashboardServiceDay")


@_attrs_define
class DashboardServiceDay:
    """Scheduled service on one day type.

    Attributes:
        cancelled: Whether service is cancelled.
        tripsPerHour: Scheduled trips per hour (index 0 = midnight), or `null` when cancelled.
        totalTrips: Total scheduled trips.

    """

    cancelled: bool
    total_trips: int
    trips_per_hour: list[float] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cancelled = self.cancelled

        total_trips = self.total_trips

        trips_per_hour: list[float] | None | Unset
        if isinstance(self.trips_per_hour, Unset):
            trips_per_hour = UNSET
        elif isinstance(self.trips_per_hour, list):
            trips_per_hour = self.trips_per_hour

        else:
            trips_per_hour = self.trips_per_hour

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cancelled": cancelled,
                "totalTrips": total_trips,
            }
        )
        if trips_per_hour is not UNSET:
            field_dict["tripsPerHour"] = trips_per_hour

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cancelled = d.pop("cancelled")

        total_trips = d.pop("totalTrips")

        def _parse_trips_per_hour(data: object) -> list[float] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                trips_per_hour_type_0 = cast(list[float], data)

                return trips_per_hour_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[float] | None | Unset, data)

        trips_per_hour = _parse_trips_per_hour(d.pop("tripsPerHour", UNSET))

        dashboard_service_day = cls(
            cancelled=cancelled,
            total_trips=total_trips,
            trips_per_hour=trips_per_hour,
        )

        dashboard_service_day.additional_properties = d
        return dashboard_service_day

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
