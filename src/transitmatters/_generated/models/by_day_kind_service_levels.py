from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import cast


T = TypeVar("T", bound="ByDayKindServiceLevels")


@_attrs_define
class ByDayKindServiceLevels:
    """Scheduled service for a specific day type (weekday, Saturday, or Sunday).

    Attributes:
        date: Reference date (YYYY-MM-DD).
        service_levels: Scheduled trips by hour (index 0 = midnight); empty if unavailable.

    """

    date: str
    service_levels: list[int]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        date = self.date

        service_levels = self.service_levels

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "date": date,
                "service_levels": service_levels,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        date = d.pop("date")

        service_levels = cast(list[int], d.pop("service_levels"))

        by_day_kind_service_levels = cls(
            date=date,
            service_levels=service_levels,
        )

        by_day_kind_service_levels.additional_properties = d
        return by_day_kind_service_levels

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
