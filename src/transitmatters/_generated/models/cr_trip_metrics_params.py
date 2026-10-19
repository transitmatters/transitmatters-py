from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.cr_trip_metrics_params_agg import CrTripMetricsParamsAgg
import datetime


T = TypeVar("T", bound="CrTripMetricsParams")


@_attrs_define
class CrTripMetricsParams:
    """Parameters for the `/api/crtripmetrics` endpoint.

    Attributes:
        start_date: Start of date range (YYYY-MM-DD).
        end_date: End of date range (YYYY-MM-DD).
        route: Commuter Rail route ID, or `all` for the whole system.
        agg: Aggregation level — `daily`, `weekly`, or `monthly`. Defaults to `daily`.

    """

    start_date: datetime.date
    """ Start of the date range, inclusive (YYYY-MM-DD). """
    end_date: datetime.date
    """ End of the date range, inclusive (YYYY-MM-DD). """
    route: str
    """ Commuter Rail route ID (e.g. `CR-Fairmount`), or `all` for the whole system. """
    agg: CrTripMetricsParamsAgg | Unset = CrTripMetricsParamsAgg.DAILY
    """ Aggregation period: `daily`, `weekly`, or `monthly`. """
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        start_date = self.start_date.isoformat()

        end_date = self.end_date.isoformat()

        route = self.route

        agg: str | Unset = UNSET
        if not isinstance(self.agg, Unset):
            agg = self.agg.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "start_date": start_date,
                "end_date": end_date,
                "route": route,
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

        route = d.pop("route")

        _agg = d.pop("agg", UNSET)
        agg: CrTripMetricsParamsAgg | Unset
        if isinstance(_agg, Unset):
            agg = UNSET
        else:
            agg = CrTripMetricsParamsAgg(_agg)

        cr_trip_metrics_params = cls(
            start_date=start_date,
            end_date=end_date,
            route=route,
            agg=agg,
        )

        cr_trip_metrics_params.additional_properties = d
        return cr_trip_metrics_params

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
