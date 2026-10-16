from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.facilities_response_links import FacilitiesResponseLinks
    from ..models.facility import Facility
    from ..models.json_api_version import JsonApiVersion


T = TypeVar("T", bound="FacilitiesResponse")


@_attrs_define
class FacilitiesResponse:
    """Response for `/api/facilities`: the MBTA v3 `/facilities` JSON:API document, passed through.

    Keys are sorted, and every JSON number in the MBTA response is sent as a string.

    Attributes:
        data: Matching facilities.
        jsonapi: JSON:API version information.
        links: JSON:API links.

        Attributes:
            data (list[Facility]):
            jsonapi (JsonApiVersion | None | Unset): JSON:API version information.

                Attributes:
                    version: JSON:API version (e.g. `1.0`).
            links (FacilitiesResponseLinks | None | Unset):
    """

    data: list[Facility]
    jsonapi: JsonApiVersion | None | Unset = UNSET
    links: FacilitiesResponseLinks | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.facilities_response_links import FacilitiesResponseLinks  # noqa: PLC0415
        from ..models.json_api_version import JsonApiVersion  # noqa: PLC0415

        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)

        jsonapi: dict[str, Any] | None | Unset
        if isinstance(self.jsonapi, Unset):
            jsonapi = UNSET
        elif isinstance(self.jsonapi, JsonApiVersion):
            jsonapi = self.jsonapi.to_dict()
        else:
            jsonapi = self.jsonapi

        links: dict[str, Any] | None | Unset
        if isinstance(self.links, Unset):
            links = UNSET
        elif isinstance(self.links, FacilitiesResponseLinks):
            links = self.links.to_dict()
        else:
            links = self.links

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )
        if jsonapi is not UNSET:
            field_dict["jsonapi"] = jsonapi
        if links is not UNSET:
            field_dict["links"] = links

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.facilities_response_links import FacilitiesResponseLinks  # noqa: PLC0415
        from ..models.facility import Facility  # noqa: PLC0415
        from ..models.json_api_version import JsonApiVersion  # noqa: PLC0415

        d = dict(src_dict)
        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = Facility.from_dict(data_item_data)

            data.append(data_item)

        def _parse_jsonapi(data: object) -> JsonApiVersion | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_json_api_version_type_0 = JsonApiVersion.from_dict(
                    data
                )

                return componentsschemas_json_api_version_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(JsonApiVersion | None | Unset, data)

        jsonapi = _parse_jsonapi(d.pop("jsonapi", UNSET))

        def _parse_links(data: object) -> FacilitiesResponseLinks | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                links_type_0 = FacilitiesResponseLinks.from_dict(data)

                return links_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(FacilitiesResponseLinks | None | Unset, data)

        links = _parse_links(d.pop("links", UNSET))

        facilities_response = cls(
            data=data,
            jsonapi=jsonapi,
            links=links,
        )

        facilities_response.additional_properties = d
        return facilities_response

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
