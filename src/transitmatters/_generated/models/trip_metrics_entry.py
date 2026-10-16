from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast


T = TypeVar("T", bound="TripMetricsEntry")


@_attrs_define
class TripMetricsEntry:
    """Delivered trip metrics for a line over one day, week or month.

    Entries can also have per-fleet share fields named `fleet_mix_<type>` (e.g. `fleet_mix_red1`,
    `fleet_mix_type7`), which vary by line and are omitted when unknown.

    Attributes:
        date: Day, Monday of the week, or first day of the month (`YYYY-MM-DD`).
        line: Line ID (e.g. `line-red`).
        count: Trips delivered (the median daily count for weekly and monthly data).
        total_time: Total trip time in seconds.
        miles_covered: Total miles covered.
        avg_car_age: Average car age in years, if known.
        pct_new_trips: Percentage of trips run with new cars, if known.

    """

    date: str
    line: str
    count: float
    total_time: float
    miles_covered: float
    avg_car_age: float | None | Unset = UNSET
    pct_new_trips: float | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        date = self.date

        line = self.line

        count = self.count

        total_time = self.total_time

        miles_covered = self.miles_covered

        avg_car_age: float | None | Unset
        if isinstance(self.avg_car_age, Unset):
            avg_car_age = UNSET
        else:
            avg_car_age = self.avg_car_age

        pct_new_trips: float | None | Unset
        if isinstance(self.pct_new_trips, Unset):
            pct_new_trips = UNSET
        else:
            pct_new_trips = self.pct_new_trips

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "date": date,
                "line": line,
                "count": count,
                "total_time": total_time,
                "miles_covered": miles_covered,
            }
        )
        if avg_car_age is not UNSET:
            field_dict["avg_car_age"] = avg_car_age
        if pct_new_trips is not UNSET:
            field_dict["pct_new_trips"] = pct_new_trips

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        date = d.pop("date")

        line = d.pop("line")

        count = d.pop("count")

        total_time = d.pop("total_time")

        miles_covered = d.pop("miles_covered")

        def _parse_avg_car_age(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        avg_car_age = _parse_avg_car_age(d.pop("avg_car_age", UNSET))

        def _parse_pct_new_trips(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        pct_new_trips = _parse_pct_new_trips(d.pop("pct_new_trips", UNSET))

        trip_metrics_entry = cls(
            date=date,
            line=line,
            count=count,
            total_time=total_time,
            miles_covered=miles_covered,
            avg_car_age=avg_car_age,
            pct_new_trips=pct_new_trips,
        )

        trip_metrics_entry.additional_properties = d
        return trip_metrics_entry

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
