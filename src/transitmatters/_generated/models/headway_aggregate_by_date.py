from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


T = TypeVar("T", bound="HeadwayAggregateByDate")


@_attrs_define
class HeadwayAggregateByDate:
    """Headway statistics for one service date, with bunching and on-time counts."""

    count: int
    """ Number of events. """
    mean: float
    """ Mean, in seconds. """
    min_: float
    """ Minimum, in seconds. """
    max_: float
    """ Maximum, in seconds. """
    std: float
    """ Population standard deviation, in seconds. """
    sum_: float
    """ Sum, in seconds. """
    field_25: float
    """ 25th percentile, in seconds. """
    field_50: float
    """ Median, in seconds. """
    field_75: float
    """ 75th percentile, in seconds. """
    service_date: str
    """ Service date (`YYYY-MM-DD`). """
    peak: str
    """ `all` for the whole day. `/api/aggregate/traveltimes2` also has `am_peak`, `pm_peak` and `off_peak` rows.
    """
    holiday: bool
    """ Whether the service date is a US federal holiday. """
    weekend: bool
    """ Whether the service date is a Saturday or Sunday. """
    bunched: int
    """ Number of headways at most half the scheduled headway (0 when there is no schedule). """
    on_time: int
    """ Number of headways within 25% of the scheduled headway (0 when there is no schedule). """
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        mean = self.mean

        min_ = self.min_

        max_ = self.max_

        std = self.std

        sum_ = self.sum_

        field_25 = self.field_25

        field_50 = self.field_50

        field_75 = self.field_75

        service_date = self.service_date

        peak = self.peak

        holiday = self.holiday

        weekend = self.weekend

        bunched = self.bunched

        on_time = self.on_time

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "count": count,
                "mean": mean,
                "min": min_,
                "max": max_,
                "std": std,
                "sum": sum_,
                "25%": field_25,
                "50%": field_50,
                "75%": field_75,
                "service_date": service_date,
                "peak": peak,
                "holiday": holiday,
                "weekend": weekend,
                "bunched": bunched,
                "on_time": on_time,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        count = d.pop("count")

        mean = d.pop("mean")

        min_ = d.pop("min")

        max_ = d.pop("max")

        std = d.pop("std")

        sum_ = d.pop("sum")

        field_25 = d.pop("25%")

        field_50 = d.pop("50%")

        field_75 = d.pop("75%")

        service_date = d.pop("service_date")

        peak = d.pop("peak")

        holiday = d.pop("holiday")

        weekend = d.pop("weekend")

        bunched = d.pop("bunched")

        on_time = d.pop("on_time")

        headway_aggregate_by_date = cls(
            count=count,
            mean=mean,
            min_=min_,
            max_=max_,
            std=std,
            sum_=sum_,
            field_25=field_25,
            field_50=field_50,
            field_75=field_75,
            service_date=service_date,
            peak=peak,
            holiday=holiday,
            weekend=weekend,
            bunched=bunched,
            on_time=on_time,
        )

        headway_aggregate_by_date.additional_properties = d
        return headway_aggregate_by_date

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
