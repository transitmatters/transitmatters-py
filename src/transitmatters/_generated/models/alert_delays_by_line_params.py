from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.alert_delays_by_line_params_agg import AlertDelaysByLineParamsAgg
import datetime


T = TypeVar("T", bound="AlertDelaysByLineParams")


@_attrs_define
class AlertDelaysByLineParams:
    """Parameters for the `/api/linedelays` endpoint.

    Attributes:
        start_date: Start of date range (YYYY-MM-DD).
        end_date: End of date range (YYYY-MM-DD).
        line: Line identifier (e.g., `Red`, `Orange`, `Green-B`).
        agg: Aggregation level — `daily` or `weekly`. Defaults to `weekly`.

        Attributes:
            start_date (datetime.date): Start of the date range, inclusive (YYYY-MM-DD).
            end_date (datetime.date): End of the date range, inclusive (YYYY-MM-DD).
            line (str): MBTA line identifier. Rapid transit: `Red`, `Orange`, `Blue`, `Green-B`-`Green-E`, `Mattapan`.
                Commuter rail: `CR-Fairmount`, `CR-Lowell`, etc.
            agg (AlertDelaysByLineParamsAgg | Unset): Aggregation period: `daily` or `weekly`. Default:
                AlertDelaysByLineParamsAgg.WEEKLY.
    """

    start_date: datetime.date
    end_date: datetime.date
    line: str
    agg: AlertDelaysByLineParamsAgg | Unset = AlertDelaysByLineParamsAgg.WEEKLY
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        start_date = self.start_date.isoformat()

        end_date = self.end_date.isoformat()

        line = self.line

        agg: str | Unset = UNSET
        if not isinstance(self.agg, Unset):
            agg = self.agg.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "start_date": start_date,
                "end_date": end_date,
                "line": line,
            }
        )
        if agg is not UNSET:
            field_dict["agg"] = agg

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        start_date = datetime.date.fromisoformat(d.pop("start_date"))

        end_date = datetime.date.fromisoformat(d.pop("end_date"))

        line = d.pop("line")

        _agg = d.pop("agg", UNSET)
        agg: AlertDelaysByLineParamsAgg | Unset
        if isinstance(_agg, Unset):
            agg = UNSET
        else:
            agg = AlertDelaysByLineParamsAgg(_agg)

        alert_delays_by_line_params = cls(
            start_date=start_date,
            end_date=end_date,
            line=line,
            agg=agg,
        )

        alert_delays_by_line_params.additional_properties = d
        return alert_delays_by_line_params

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
