from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast


T = TypeVar("T", bound="TravelTimeEvent")


@_attrs_define
class TravelTimeEvent:
    """A trip's travel time between the requested origin and destination stops.

    Times are local (Eastern) wall-clock times formatted as `YYYY-MM-DDTHH:MM:SS`, with no offset.

    Attributes:
        route_id: Route of the trip (e.g. `Red`, `28`, `CR-Fairmount`).
        direction: Direction ID (`0` or `1`).
        dep_dt: Departure time from the origin.
        arr_dt: Arrival time at the destination.
        travel_time_sec: Travel time in seconds.
        benchmark_travel_time_sec: Scheduled travel time in seconds, or `null` when unavailable.
        tm_benchmark_travel_time_sec: TransitMatters benchmark travel time in seconds for the stop pair
            (the same on every event), or `null` when there is none (bus, commuter rail, ferry).
        vehicle_consist: Car numbers separated by `|`, or `null` when unavailable.
        vehicle_label: Vehicle label; may be empty.

        Attributes:
            route_id (str):
            direction (int):
            dep_dt (str):
            arr_dt (str):
            travel_time_sec (float):
            vehicle_label (str):
            benchmark_travel_time_sec (float | None | Unset):
            tm_benchmark_travel_time_sec (float | None | Unset):
            vehicle_consist (None | str | Unset):
    """

    route_id: str
    direction: int
    dep_dt: str
    arr_dt: str
    travel_time_sec: float
    vehicle_label: str
    benchmark_travel_time_sec: float | None | Unset = UNSET
    tm_benchmark_travel_time_sec: float | None | Unset = UNSET
    vehicle_consist: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        route_id = self.route_id

        direction = self.direction

        dep_dt = self.dep_dt

        arr_dt = self.arr_dt

        travel_time_sec = self.travel_time_sec

        vehicle_label = self.vehicle_label

        benchmark_travel_time_sec: float | None | Unset
        if isinstance(self.benchmark_travel_time_sec, Unset):
            benchmark_travel_time_sec = UNSET
        else:
            benchmark_travel_time_sec = self.benchmark_travel_time_sec

        tm_benchmark_travel_time_sec: float | None | Unset
        if isinstance(self.tm_benchmark_travel_time_sec, Unset):
            tm_benchmark_travel_time_sec = UNSET
        else:
            tm_benchmark_travel_time_sec = self.tm_benchmark_travel_time_sec

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
                "dep_dt": dep_dt,
                "arr_dt": arr_dt,
                "travel_time_sec": travel_time_sec,
                "vehicle_label": vehicle_label,
            }
        )
        if benchmark_travel_time_sec is not UNSET:
            field_dict["benchmark_travel_time_sec"] = benchmark_travel_time_sec
        if tm_benchmark_travel_time_sec is not UNSET:
            field_dict["tm_benchmark_travel_time_sec"] = tm_benchmark_travel_time_sec
        if vehicle_consist is not UNSET:
            field_dict["vehicle_consist"] = vehicle_consist

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        route_id = d.pop("route_id")

        direction = d.pop("direction")

        dep_dt = d.pop("dep_dt")

        arr_dt = d.pop("arr_dt")

        travel_time_sec = d.pop("travel_time_sec")

        vehicle_label = d.pop("vehicle_label")

        def _parse_benchmark_travel_time_sec(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        benchmark_travel_time_sec = _parse_benchmark_travel_time_sec(
            d.pop("benchmark_travel_time_sec", UNSET)
        )

        def _parse_tm_benchmark_travel_time_sec(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        tm_benchmark_travel_time_sec = _parse_tm_benchmark_travel_time_sec(
            d.pop("tm_benchmark_travel_time_sec", UNSET)
        )

        def _parse_vehicle_consist(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        vehicle_consist = _parse_vehicle_consist(d.pop("vehicle_consist", UNSET))

        travel_time_event = cls(
            route_id=route_id,
            direction=direction,
            dep_dt=dep_dt,
            arr_dt=arr_dt,
            travel_time_sec=travel_time_sec,
            vehicle_label=vehicle_label,
            benchmark_travel_time_sec=benchmark_travel_time_sec,
            tm_benchmark_travel_time_sec=tm_benchmark_travel_time_sec,
            vehicle_consist=vehicle_consist,
        )

        travel_time_event.additional_properties = d
        return travel_time_event

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
