from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


import datetime


T = TypeVar("T", bound="SpeedRestrictionsParams")


@_attrs_define
class SpeedRestrictionsParams:
    """Parameters for the `/api/speed_restrictions` endpoint.

    Attributes:
        line_id: GTFS line identifier (e.g., `line-Red`, `line-Orange`).
        date: Date to query (YYYY-MM-DD).

    """

    line_id: str
    """ GTFS rapid transit line identifier: `line-Red`, `line-Orange`, `line-Blue`, or `line-Green`. IDs are case-
    sensitive. Speed restriction data is only available for rapid transit lines. """
    date: datetime.date
    """ Date to query (YYYY-MM-DD). """
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        line_id = self.line_id

        date = self.date.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "line_id": line_id,
                "date": date,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        line_id = d.pop("line_id")

        date = datetime.date.fromisoformat(d.pop("date"))

        speed_restrictions_params = cls(
            line_id=line_id,
            date=date,
        )

        speed_restrictions_params.additional_properties = d
        return speed_restrictions_params

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
