from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.facility_attributes import FacilityAttributes
    from ..models.facility_links import FacilityLinks
    from ..models.facility_relationships import FacilityRelationships


T = TypeVar("T", bound="Facility")


@_attrs_define
class Facility:
    """An MBTA facility (elevator, escalator, parking, etc.) from the MBTA v3 API.

    Attributes:
        id: Facility identifier.
        type: JSON:API resource type, always `facility`.
        attributes: Facility attributes.
        relationships: Related resources.
        links: JSON:API links.

        Attributes:
            id (str):
            type_ (str):
            attributes (FacilityAttributes): Attributes of an MBTA facility, passed through from the MBTA v3 API.

                Attributes:
                    type: Facility type (e.g. `ELEVATOR`, `ESCALATOR`, `BIKE_STORAGE`, `PARKING_AREA`).
                    long_name: Full display name.
                    short_name: Short display name.
                    latitude: Latitude as a decimal string (e.g. `"42.352271"`), or `null`.
                    longitude: Longitude as a decimal string, or `null`.
                    properties: Additional facility properties.
            relationships (FacilityRelationships | None | Unset): Relationships of an MBTA facility.

                Attributes:
                    stop: The stop the facility belongs to.
            links (FacilityLinks | None | Unset):
    """

    id: str
    type_: str
    attributes: FacilityAttributes
    relationships: FacilityRelationships | None | Unset = UNSET
    links: FacilityLinks | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.facility_links import FacilityLinks  # noqa: PLC0415
        from ..models.facility_relationships import FacilityRelationships  # noqa: PLC0415

        id = self.id

        type_ = self.type_

        attributes = self.attributes.to_dict()

        relationships: dict[str, Any] | None | Unset
        if isinstance(self.relationships, Unset):
            relationships = UNSET
        elif isinstance(self.relationships, FacilityRelationships):
            relationships = self.relationships.to_dict()
        else:
            relationships = self.relationships

        links: dict[str, Any] | None | Unset
        if isinstance(self.links, Unset):
            links = UNSET
        elif isinstance(self.links, FacilityLinks):
            links = self.links.to_dict()
        else:
            links = self.links

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "type": type_,
                "attributes": attributes,
            }
        )
        if relationships is not UNSET:
            field_dict["relationships"] = relationships
        if links is not UNSET:
            field_dict["links"] = links

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.facility_attributes import FacilityAttributes  # noqa: PLC0415
        from ..models.facility_links import FacilityLinks  # noqa: PLC0415
        from ..models.facility_relationships import FacilityRelationships  # noqa: PLC0415

        d = dict(src_dict)
        id = d.pop("id")

        type_ = d.pop("type")

        attributes = FacilityAttributes.from_dict(d.pop("attributes"))

        def _parse_relationships(data: object) -> FacilityRelationships | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_facility_relationships_type_0 = (
                    FacilityRelationships.from_dict(data)
                )

                return componentsschemas_facility_relationships_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(FacilityRelationships | None | Unset, data)

        relationships = _parse_relationships(d.pop("relationships", UNSET))

        def _parse_links(data: object) -> FacilityLinks | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                links_type_0 = FacilityLinks.from_dict(data)

                return links_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(FacilityLinks | None | Unset, data)

        links = _parse_links(d.pop("links", UNSET))

        facility = cls(
            id=id,
            type_=type_,
            attributes=attributes,
            relationships=relationships,
            links=links,
        )

        facility.additional_properties = d
        return facility

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
