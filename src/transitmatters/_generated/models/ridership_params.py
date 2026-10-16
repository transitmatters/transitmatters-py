from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


import datetime


T = TypeVar("T", bound="RidershipParams")


@_attrs_define
class RidershipParams:
    """Parameters for the `/api/ridership` endpoint.

    Attributes:
        start_date: Start of date range.
        end_date: End of date range.
        line_id: Line identifier (e.g., `line-Red`, `line-1`, `line-Fairmount`).

    """

    start_date: datetime.date
    """ Start of the date range, inclusive (YYYY-MM-DD). """
    end_date: datetime.date
    """ End of the date range, inclusive (YYYY-MM-DD). """
    line_id: str
    """ Line identifier for ridership data. Rapid transit: `line-Red`, `line-Orange`, `line-Blue`, `line-Green`.
    Bus: `line-{route}` (e.g. `line-1`, `line-66`). Commuter rail: `line-{line}` (e.g. `line-Fairmount`). Ferry:
    `line-F1`, `line-F4`, etc. """
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        start_date = self.start_date.isoformat()

        end_date = self.end_date.isoformat()

        line_id = self.line_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "start_date": start_date,
                "end_date": end_date,
                "line_id": line_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        start_date = datetime.date.fromisoformat(d.pop("start_date"))

        end_date = datetime.date.fromisoformat(d.pop("end_date"))

        line_id = d.pop("line_id")

        ridership_params = cls(
            start_date=start_date,
            end_date=end_date,
            line_id=line_id,
        )

        ridership_params.additional_properties = d
        return ridership_params

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
