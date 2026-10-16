from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.facility_stop_relationship import FacilityStopRelationship


T = TypeVar("T", bound="FacilityRelationships")


@_attrs_define
class FacilityRelationships:
    """Relationships of an MBTA facility.

    Attributes:
        stop: The stop the facility belongs to.

        Attributes:
            stop (FacilityStopRelationship | None | Unset): The stop a facility belongs to.

                Attributes:
                    data: Reference to the stop.
    """

    stop: FacilityStopRelationship | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.facility_stop_relationship import FacilityStopRelationship  # noqa: PLC0415

        stop: dict[str, Any] | None | Unset
        if isinstance(self.stop, Unset):
            stop = UNSET
        elif isinstance(self.stop, FacilityStopRelationship):
            stop = self.stop.to_dict()
        else:
            stop = self.stop

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if stop is not UNSET:
            field_dict["stop"] = stop

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.facility_stop_relationship import FacilityStopRelationship  # noqa: PLC0415

        d = dict(src_dict)

        def _parse_stop(data: object) -> FacilityStopRelationship | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_facility_stop_relationship_type_0 = (
                    FacilityStopRelationship.from_dict(data)
                )

                return componentsschemas_facility_stop_relationship_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(FacilityStopRelationship | None | Unset, data)

        stop = _parse_stop(d.pop("stop", UNSET))

        facility_relationships = cls(
            stop=stop,
        )

        facility_relationships.additional_properties = d
        return facility_relationships

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
