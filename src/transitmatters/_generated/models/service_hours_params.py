from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


from ..models.service_hours_params_agg import ServiceHoursParamsAgg
import datetime


T = TypeVar("T", bound="ServiceHoursParams")


@_attrs_define
class ServiceHoursParams:
    """Parameters for the `/api/service_hours` endpoint.

    Attributes:
        line_id: GTFS line identifier (e.g., `line-red`).
        start_date: Start of date range.
        end_date: End of date range.
        agg: Aggregation level — `daily`, `weekly`, or `monthly`.

        Attributes:
            line_id (str): GTFS rapid transit line identifier: `line-red`, `line-orange`, `line-blue`, `line-green`, or
                `line-mattapan`.
            start_date (datetime.date): Start of the date range, inclusive (YYYY-MM-DD).
            end_date (datetime.date): End of the date range, inclusive (YYYY-MM-DD).
            agg (ServiceHoursParamsAgg): Aggregation period: `daily`, `weekly`, or `monthly`.
    """

    line_id: str
    start_date: datetime.date
    end_date: datetime.date
    agg: ServiceHoursParamsAgg
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        line_id = self.line_id

        start_date = self.start_date.isoformat()

        end_date = self.end_date.isoformat()

        agg = self.agg.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "line_id": line_id,
                "start_date": start_date,
                "end_date": end_date,
                "agg": agg,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        line_id = d.pop("line_id")

        start_date = datetime.date.fromisoformat(d.pop("start_date"))

        end_date = datetime.date.fromisoformat(d.pop("end_date"))

        agg = ServiceHoursParamsAgg(d.pop("agg"))

        service_hours_params = cls(
            line_id=line_id,
            start_date=start_date,
            end_date=end_date,
            agg=agg,
        )

        service_hours_params.additional_properties = d
        return service_hours_params

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
