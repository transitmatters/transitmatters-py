from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.bus_trip_metrics_params_agg import BusTripMetricsParamsAgg
from ..models.bus_trip_metrics_params_day_type import BusTripMetricsParamsDayType
from ..models.bus_trip_metrics_params_time_band import BusTripMetricsParamsTimeBand
import datetime


T = TypeVar("T", bound="BusTripMetricsParams")


@_attrs_define
class BusTripMetricsParams:
    """Parameters for the `/api/bustripmetrics` endpoint.

    Attributes:
        start_date: Start of date range (YYYY-MM-DD).
        end_date: End of date range (YYYY-MM-DD).
        route: Bus route ID, or a comma-separated group of routes.
        agg: Aggregation level — `daily`, `weekly`, or `monthly`. Defaults to `daily`.
        time_band: Optional time of day to report instead of the whole day.
        day_type: Optional day type to keep, dropping every other day.

    """

    start_date: datetime.date
    """ Start of the date range, inclusive (YYYY-MM-DD). """
    end_date: datetime.date
    """ End of the date range, inclusive (YYYY-MM-DD). """
    route: str
    """ Bus route ID (e.g. `1`, `57`, `111`), or a comma-separated list (e.g. `114,116,117`) whose routes are summed
    per period. """
    agg: BusTripMetricsParamsAgg | Unset = BusTripMetricsParamsAgg.DAILY
    """ Aggregation period: `daily`, `weekly`, or `monthly`. """
    time_band: BusTripMetricsParamsTimeBand | Unset = UNSET
    """ Time of day. Each figure is then that band's alone, and daily entries drop `median_speed_mph` and
    `mean_speed_mph`, which have no per-band version. Omit it for the whole day. """
    day_type: BusTripMetricsParamsDayType | Unset = UNSET
    """ Keep only business days, or only weekends and MBTA holidays. Omit it for every day. """
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        start_date = self.start_date.isoformat()

        end_date = self.end_date.isoformat()

        route = self.route

        agg: str | Unset = UNSET
        if not isinstance(self.agg, Unset):
            agg = self.agg.value

        time_band: str | Unset = UNSET
        if not isinstance(self.time_band, Unset):
            time_band = self.time_band.value

        day_type: str | Unset = UNSET
        if not isinstance(self.day_type, Unset):
            day_type = self.day_type.value

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
        if time_band is not UNSET:
            field_dict["time_band"] = time_band
        if day_type is not UNSET:
            field_dict["day_type"] = day_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        start_date = datetime.date.fromisoformat(d.pop("start_date"))

        end_date = datetime.date.fromisoformat(d.pop("end_date"))

        route = d.pop("route")

        _agg = d.pop("agg", UNSET)
        agg: BusTripMetricsParamsAgg | Unset
        if isinstance(_agg, Unset):
            agg = UNSET
        else:
            agg = BusTripMetricsParamsAgg(_agg)

        _time_band = d.pop("time_band", UNSET)
        time_band: BusTripMetricsParamsTimeBand | Unset
        if isinstance(_time_band, Unset):
            time_band = UNSET
        else:
            time_band = BusTripMetricsParamsTimeBand(_time_band)

        _day_type = d.pop("day_type", UNSET)
        day_type: BusTripMetricsParamsDayType | Unset
        if isinstance(_day_type, Unset):
            day_type = UNSET
        else:
            day_type = BusTripMetricsParamsDayType(_day_type)

        bus_trip_metrics_params = cls(
            start_date=start_date,
            end_date=end_date,
            route=route,
            agg=agg,
            time_band=time_band,
            day_type=day_type,
        )

        bus_trip_metrics_params.additional_properties = d
        return bus_trip_metrics_params

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
