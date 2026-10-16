from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast


T = TypeVar("T", bound="HeadwayEvent")


@_attrs_define
class HeadwayEvent:
    """The time between two consecutive departures from the requested stop(s).

    Times are local (Eastern) wall-clock times formatted as `YYYY-MM-DDTHH:MM:SS`, with no offset.

    Attributes:
        route_id: Route of the departing trip (e.g. `Red`, `28`, `CR-Fairmount`).
        direction: Direction ID as a string (`"0"` or `"1"`). Dwells and travel times use integers.
        current_dep_dt: Departure time.
        headway_time_sec: Seconds since the previous departure.
        benchmark_headway_time_sec: Scheduled headway in seconds, or `null` when unavailable.
        vehicle_consist: Car numbers separated by `|` (e.g. `1850|1851`), or `null` when unavailable.
        vehicle_label: Vehicle label; may be empty.

    """

    route_id: str
    direction: str
    current_dep_dt: str
    headway_time_sec: float
    vehicle_label: str
    benchmark_headway_time_sec: float | None | Unset = UNSET
    vehicle_consist: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        route_id = self.route_id

        direction = self.direction

        current_dep_dt = self.current_dep_dt

        headway_time_sec = self.headway_time_sec

        vehicle_label = self.vehicle_label

        benchmark_headway_time_sec: float | None | Unset
        if isinstance(self.benchmark_headway_time_sec, Unset):
            benchmark_headway_time_sec = UNSET
        else:
            benchmark_headway_time_sec = self.benchmark_headway_time_sec

        vehicle_consist: None | str | Unset
        if isinstance(self.vehicle_consist, Unset):
            vehicle_consist = UNSET
        else:
            vehicle_consist = self.vehicle_consist

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "route_id": route_id,
                "direction": direction,
                "current_dep_dt": current_dep_dt,
                "headway_time_sec": headway_time_sec,
                "vehicle_label": vehicle_label,
            }
        )
        if benchmark_headway_time_sec is not UNSET:
            field_dict["benchmark_headway_time_sec"] = benchmark_headway_time_sec
        if vehicle_consist is not UNSET:
            field_dict["vehicle_consist"] = vehicle_consist

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        route_id = d.pop("route_id")

        direction = d.pop("direction")

        current_dep_dt = d.pop("current_dep_dt")

        headway_time_sec = d.pop("headway_time_sec")

        vehicle_label = d.pop("vehicle_label")

        def _parse_benchmark_headway_time_sec(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        benchmark_headway_time_sec = _parse_benchmark_headway_time_sec(
            d.pop("benchmark_headway_time_sec", UNSET)
        )

        def _parse_vehicle_consist(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        vehicle_consist = _parse_vehicle_consist(d.pop("vehicle_consist", UNSET))

        headway_event = cls(
            route_id=route_id,
            direction=direction,
            current_dep_dt=current_dep_dt,
            headway_time_sec=headway_time_sec,
            vehicle_label=vehicle_label,
            benchmark_headway_time_sec=benchmark_headway_time_sec,
            vehicle_consist=vehicle_consist,
        )

        headway_event.additional_properties = d
        return headway_event

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
