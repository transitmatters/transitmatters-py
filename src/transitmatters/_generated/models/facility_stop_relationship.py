from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.json_api_resource_identifier import JsonApiResourceIdentifier


T = TypeVar("T", bound="FacilityStopRelationship")


@_attrs_define
class FacilityStopRelationship:
    """The stop a facility belongs to.

    Attributes:
        data: Reference to the stop.

        Attributes:
            data (JsonApiResourceIdentifier | None | Unset): A JSON:API reference to another resource.

                Attributes:
                    id: Resource ID (e.g. `place-alfcl`).
                    type: Resource type (e.g. `stop`).
    """

    data: JsonApiResourceIdentifier | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.json_api_resource_identifier import JsonApiResourceIdentifier  # noqa: PLC0415

        data: dict[str, Any] | None | Unset
        if isinstance(self.data, Unset):
            data = UNSET
        elif isinstance(self.data, JsonApiResourceIdentifier):
            data = self.data.to_dict()
        else:
            data = self.data

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.json_api_resource_identifier import JsonApiResourceIdentifier  # noqa: PLC0415

        d = dict(src_dict)

        def _parse_data(data: object) -> JsonApiResourceIdentifier | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_json_api_resource_identifier_type_0 = (
                    JsonApiResourceIdentifier.from_dict(data)
                )

                return componentsschemas_json_api_resource_identifier_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(JsonApiResourceIdentifier | None | Unset, data)

        data = _parse_data(d.pop("data", UNSET))

        facility_stop_relationship = cls(
            data=data,
        )

        facility_stop_relationship.additional_properties = d
        return facility_stop_relationship

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
