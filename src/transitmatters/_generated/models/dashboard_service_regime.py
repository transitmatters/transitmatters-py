from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.dashboard_service_day import DashboardServiceDay


T = TypeVar("T", bound="DashboardServiceRegime")


@_attrs_define
class DashboardServiceRegime:
    """Scheduled service by day type.

    Attributes:
        weekday: Weekday service.
        saturday: Saturday service.
        sunday: Sunday service.

        Attributes:
            weekday (DashboardServiceDay): Scheduled service on one day type.

                Attributes:
                    cancelled: Whether service is cancelled.
                    tripsPerHour: Scheduled trips per hour (index 0 = midnight), or `null` when cancelled.
                    totalTrips: Total scheduled trips.
            saturday (DashboardServiceDay): Scheduled service on one day type.

                Attributes:
                    cancelled: Whether service is cancelled.
                    tripsPerHour: Scheduled trips per hour (index 0 = midnight), or `null` when cancelled.
                    totalTrips: Total scheduled trips.
            sunday (DashboardServiceDay): Scheduled service on one day type.

                Attributes:
                    cancelled: Whether service is cancelled.
                    tripsPerHour: Scheduled trips per hour (index 0 = midnight), or `null` when cancelled.
                    totalTrips: Total scheduled trips.
    """

    weekday: DashboardServiceDay
    saturday: DashboardServiceDay
    sunday: DashboardServiceDay
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        weekday = self.weekday.to_dict()

        saturday = self.saturday.to_dict()

        sunday = self.sunday.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "weekday": weekday,
                "saturday": saturday,
                "sunday": sunday,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.dashboard_service_day import DashboardServiceDay  # noqa: PLC0415

        d = dict(src_dict)
        weekday = DashboardServiceDay.from_dict(d.pop("weekday"))

        saturday = DashboardServiceDay.from_dict(d.pop("saturday"))

        sunday = DashboardServiceDay.from_dict(d.pop("sunday"))

        dashboard_service_regime = cls(
            weekday=weekday,
            saturday=saturday,
            sunday=sunday,
        )

        dashboard_service_regime.additional_properties = d
        return dashboard_service_regime

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
