from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast


T = TypeVar("T", bound="DwellEvent")


@_attrs_define
class DwellEvent:
    """The time a vehicle spent stopped at the requested stop(s).

    Times are local (Eastern) wall-clock times formatted as `YYYY-MM-DDTHH:MM:SS`, with no offset.

    Attributes:
        route_id: Route of the trip (e.g. `Red`, `1`, `CR-Fairmount`).
        direction: Direction ID (`0` or `1`).
        arr_dt: Arrival time.
        dep_dt: Departure time.
        dwell_time_sec: Seconds between arrival and departure.
        vehicle_consist: Car numbers separated by `|`, or `null` when unavailable.
        vehicle_label: Vehicle label; may be empty.

        Attributes:
            route_id (str):
            direction (int):
            arr_dt (str):
            dep_dt (str):
            dwell_time_sec (float):
            vehicle_label (str):
            vehicle_consist (None | str | Unset):
    """

    route_id: str
    direction: int
    arr_dt: str
    dep_dt: str
    dwell_time_sec: float
    vehicle_label: str
    vehicle_consist: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        route_id = self.route_id

        direction = self.direction

        arr_dt = self.arr_dt

        dep_dt = self.dep_dt

        dwell_time_sec = self.dwell_time_sec

        vehicle_label = self.vehicle_label

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
                "arr_dt": arr_dt,
                "dep_dt": dep_dt,
                "dwell_time_sec": dwell_time_sec,
                "vehicle_label": vehicle_label,
            }
        )
        if vehicle_consist is not UNSET:
            field_dict["vehicle_consist"] = vehicle_consist

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        route_id = d.pop("route_id")

        direction = d.pop("direction")

        arr_dt = d.pop("arr_dt")

        dep_dt = d.pop("dep_dt")

        dwell_time_sec = d.pop("dwell_time_sec")

        vehicle_label = d.pop("vehicle_label")

        def _parse_vehicle_consist(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        vehicle_consist = _parse_vehicle_consist(d.pop("vehicle_consist", UNSET))

        dwell_event = cls(
            route_id=route_id,
            direction=direction,
            arr_dt=arr_dt,
            dep_dt=dep_dt,
            dwell_time_sec=dwell_time_sec,
            vehicle_label=vehicle_label,
            vehicle_consist=vehicle_consist,
        )

        dwell_event.additional_properties = d
        return dwell_event

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
