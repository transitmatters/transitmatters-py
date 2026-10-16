from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


T = TypeVar("T", bound="AggregateByTime")


@_attrs_define
class AggregateByTime:
    """Statistics for one 30-minute departure-time bucket across the date range.

    Attributes:
        count (int): Number of events.
        mean (float): Mean, in seconds.
        min_ (float): Minimum, in seconds.
        max_ (float): Maximum, in seconds.
        std (float): Population standard deviation, in seconds.
        sum_ (float): Sum, in seconds.
        field_25 (float): 25th percentile, in seconds.
        field_50 (float): Median, in seconds.
        field_75 (float): 75th percentile, in seconds.
        dep_time_from_epoch (str): Bucket start as `1970-01-01THH:MM:SS`. Departures after midnight and before 03:30 use
            `1970-01-02`.
        is_peak_day (bool): `true` for non-holiday weekdays, `false` for weekends and holidays.
    """

    count: int
    mean: float
    min_: float
    max_: float
    std: float
    sum_: float
    field_25: float
    field_50: float
    field_75: float
    dep_time_from_epoch: str
    is_peak_day: bool
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

        dep_time_from_epoch = self.dep_time_from_epoch

        is_peak_day = self.is_peak_day

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
                "dep_time_from_epoch": dep_time_from_epoch,
                "is_peak_day": is_peak_day,
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

        dep_time_from_epoch = d.pop("dep_time_from_epoch")

        is_peak_day = d.pop("is_peak_day")

        aggregate_by_time = cls(
            count=count,
            mean=mean,
            min_=min_,
            max_=max_,
            std=std,
            sum_=sum_,
            field_25=field_25,
            field_50=field_50,
            field_75=field_75,
            dep_time_from_epoch=dep_time_from_epoch,
            is_peak_day=is_peak_day,
        )

        aggregate_by_time.additional_properties = d
        return aggregate_by_time

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
