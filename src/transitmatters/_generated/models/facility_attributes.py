from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.facility_property import FacilityProperty


T = TypeVar("T", bound="FacilityAttributes")


@_attrs_define
class FacilityAttributes:
    """Attributes of an MBTA facility, passed through from the MBTA v3 API.

    Attributes:
        type: Facility type (e.g. `ELEVATOR`, `ESCALATOR`, `BIKE_STORAGE`, `PARKING_AREA`).
        long_name: Full display name.
        short_name: Short display name.
        latitude: Latitude as a decimal string (e.g. `"42.352271"`), or `null`.
        longitude: Longitude as a decimal string, or `null`.
        properties: Additional facility properties.

    """

    type_: str
    long_name: None | str | Unset = UNSET
    short_name: None | str | Unset = UNSET
    latitude: None | str | Unset = UNSET
    longitude: None | str | Unset = UNSET
    properties: list[FacilityProperty] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        long_name: None | str | Unset
        if isinstance(self.long_name, Unset):
            long_name = UNSET
        else:
            long_name = self.long_name

        short_name: None | str | Unset
        if isinstance(self.short_name, Unset):
            short_name = UNSET
        else:
            short_name = self.short_name

        latitude: None | str | Unset
        if isinstance(self.latitude, Unset):
            latitude = UNSET
        else:
            latitude = self.latitude

        longitude: None | str | Unset
        if isinstance(self.longitude, Unset):
            longitude = UNSET
        else:
            longitude = self.longitude

        properties: list[dict[str, Any]] | None | Unset
        if isinstance(self.properties, Unset):
            properties = UNSET
        elif isinstance(self.properties, list):
            properties = []
            for properties_type_0_item_data in self.properties:
                properties_type_0_item = properties_type_0_item_data.to_dict()
                properties.append(properties_type_0_item)

        else:
            properties = self.properties

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
            }
        )
        if long_name is not UNSET:
            field_dict["long_name"] = long_name
        if short_name is not UNSET:
            field_dict["short_name"] = short_name
        if latitude is not UNSET:
            field_dict["latitude"] = latitude
        if longitude is not UNSET:
            field_dict["longitude"] = longitude
        if properties is not UNSET:
            field_dict["properties"] = properties

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.facility_property import FacilityProperty  # noqa: PLC0415

        d = dict(src_dict)
        type_ = d.pop("type")

        def _parse_long_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        long_name = _parse_long_name(d.pop("long_name", UNSET))

        def _parse_short_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        short_name = _parse_short_name(d.pop("short_name", UNSET))

        def _parse_latitude(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        latitude = _parse_latitude(d.pop("latitude", UNSET))

        def _parse_longitude(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        longitude = _parse_longitude(d.pop("longitude", UNSET))

        def _parse_properties(data: object) -> list[FacilityProperty] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                properties_type_0 = []
                _properties_type_0 = data
                for properties_type_0_item_data in _properties_type_0:
                    properties_type_0_item = FacilityProperty.from_dict(
                        properties_type_0_item_data
                    )

                    properties_type_0.append(properties_type_0_item)

                return properties_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[FacilityProperty] | None | Unset, data)

        properties = _parse_properties(d.pop("properties", UNSET))

        facility_attributes = cls(
            type_=type_,
            long_name=long_name,
            short_name=short_name,
            latitude=latitude,
            longitude=longitude,
            properties=properties,
        )

        facility_attributes.additional_properties = d
        return facility_attributes

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
