from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


from ..models.trip_metrics_by_line_params_agg import TripMetricsByLineParamsAgg
import datetime


T = TypeVar("T", bound="TripMetricsByLineParams")


@_attrs_define
class TripMetricsByLineParams:
    """Parameters for the `/api/tripmetrics` endpoint.

    Attributes:
        start_date: Start of date range (YYYY-MM-DD).
        end_date: End of date range (YYYY-MM-DD).
        agg: Aggregation level — `daily`, `weekly`, or `monthly`.
        line: GTFS line identifier (e.g., `line-red`, `line-green`).

    """

    start_date: datetime.date
    """ Start of the date range, inclusive (YYYY-MM-DD). """
    end_date: datetime.date
    """ End of the date range, inclusive (YYYY-MM-DD). """
    agg: TripMetricsByLineParamsAgg
    """ Aggregation period: `daily`, `weekly`, or `monthly`. """
    line: str
    """ GTFS rapid transit line identifier: `line-red`, `line-orange`, `line-blue`, `line-green`, or `line-
    mattapan`. """
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        start_date = self.start_date.isoformat()

        end_date = self.end_date.isoformat()

        agg = self.agg.value

        line = self.line

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "start_date": start_date,
                "end_date": end_date,
                "agg": agg,
                "line": line,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        start_date = datetime.date.fromisoformat(d.pop("start_date"))

        end_date = datetime.date.fromisoformat(d.pop("end_date"))

        agg = TripMetricsByLineParamsAgg(d.pop("agg"))

        line = d.pop("line")

        trip_metrics_by_line_params = cls(
            start_date=start_date,
            end_date=end_date,
            agg=agg,
            line=line,
        )

        trip_metrics_by_line_params.additional_properties = d
        return trip_metrics_by_line_params

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
