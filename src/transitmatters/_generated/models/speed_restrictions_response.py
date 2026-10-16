from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.speed_restriction_zone import SpeedRestrictionZone


T = TypeVar("T", bound="SpeedRestrictionsResponse")


@_attrs_define
class SpeedRestrictionsResponse:
    """Response for `/api/speed_restrictions` — speed restriction zones.

    Attributes:
        available: Whether speed restriction data exists for this date.
        date: Actual date of the data (may be earlier than the requested date). Omitted when unavailable.
        zones: Speed restrictions in effect. Omitted when unavailable.

    """

    available: bool
    date: None | str | Unset = UNSET
    zones: list[SpeedRestrictionZone] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        available = self.available

        date: None | str | Unset
        if isinstance(self.date, Unset):
            date = UNSET
        else:
            date = self.date

        zones: list[dict[str, Any]] | None | Unset
        if isinstance(self.zones, Unset):
            zones = UNSET
        elif isinstance(self.zones, list):
            zones = []
            for zones_type_0_item_data in self.zones:
                zones_type_0_item = zones_type_0_item_data.to_dict()
                zones.append(zones_type_0_item)

        else:
            zones = self.zones

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "available": available,
            }
        )
        if date is not UNSET:
            field_dict["date"] = date
        if zones is not UNSET:
            field_dict["zones"] = zones

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.speed_restriction_zone import SpeedRestrictionZone  # noqa: PLC0415

        d = dict(src_dict)
        available = d.pop("available")

        def _parse_date(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        date = _parse_date(d.pop("date", UNSET))

        def _parse_zones(data: object) -> list[SpeedRestrictionZone] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                zones_type_0 = []
                _zones_type_0 = data
                for zones_type_0_item_data in _zones_type_0:
                    zones_type_0_item = SpeedRestrictionZone.from_dict(
                        zones_type_0_item_data
                    )

                    zones_type_0.append(zones_type_0_item)

                return zones_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[SpeedRestrictionZone] | None | Unset, data)

        zones = _parse_zones(d.pop("zones", UNSET))

        speed_restrictions_response = cls(
            available=available,
            date=date,
            zones=zones,
        )

        speed_restrictions_response.additional_properties = d
        return speed_restrictions_response

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
