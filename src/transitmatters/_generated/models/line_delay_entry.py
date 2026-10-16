from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


T = TypeVar("T", bound="LineDelayEntry")


@_attrs_define
class LineDelayEntry:
    """Alert-reported delay on a line for one day or week, in minutes, by cause.

    Attributes:
        date: Day, or the Monday starting the week (`YYYY-MM-DD`).
        line: Line as requested (e.g. `Red`, `Green-B`, `CR-Fairmount`).
        total_delay_time: Total delay.
        brake_problem: Delay attributed to brake problems.
        car_traffic: Delay attributed to car traffic.
        disabled_vehicle: Delay attributed to disabled vehicles.
        door_problem: Delay attributed to door problems.
        fire: Delay attributed to fires.
        flooding: Delay attributed to flooding.
        mechanical_problem: Delay attributed to mechanical problems.
        medical_emergency: Delay attributed to medical emergencies.
        other: Delay attributed to other causes.
        police_activity: Delay attributed to police activity.
        power_problem: Delay attributed to power problems.
        signal_problem: Delay attributed to signal problems.
        switch_problem: Delay attributed to switch problems.
        track_issue: Delay attributed to track issues.
        track_work: Delay attributed to track work.

    """

    date: str
    line: str
    total_delay_time: int
    brake_problem: int
    car_traffic: int
    disabled_vehicle: int
    door_problem: int
    fire: int
    flooding: int
    mechanical_problem: int
    medical_emergency: int
    other: int
    police_activity: int
    power_problem: int
    signal_problem: int
    switch_problem: int
    track_issue: int
    track_work: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        date = self.date

        line = self.line

        total_delay_time = self.total_delay_time

        brake_problem = self.brake_problem

        car_traffic = self.car_traffic

        disabled_vehicle = self.disabled_vehicle

        door_problem = self.door_problem

        fire = self.fire

        flooding = self.flooding

        mechanical_problem = self.mechanical_problem

        medical_emergency = self.medical_emergency

        other = self.other

        police_activity = self.police_activity

        power_problem = self.power_problem

        signal_problem = self.signal_problem

        switch_problem = self.switch_problem

        track_issue = self.track_issue

        track_work = self.track_work

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "date": date,
                "line": line,
                "total_delay_time": total_delay_time,
                "brake_problem": brake_problem,
                "car_traffic": car_traffic,
                "disabled_vehicle": disabled_vehicle,
                "door_problem": door_problem,
                "fire": fire,
                "flooding": flooding,
                "mechanical_problem": mechanical_problem,
                "medical_emergency": medical_emergency,
                "other": other,
                "police_activity": police_activity,
                "power_problem": power_problem,
                "signal_problem": signal_problem,
                "switch_problem": switch_problem,
                "track_issue": track_issue,
                "track_work": track_work,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        date = d.pop("date")

        line = d.pop("line")

        total_delay_time = d.pop("total_delay_time")

        brake_problem = d.pop("brake_problem")

        car_traffic = d.pop("car_traffic")

        disabled_vehicle = d.pop("disabled_vehicle")

        door_problem = d.pop("door_problem")

        fire = d.pop("fire")

        flooding = d.pop("flooding")

        mechanical_problem = d.pop("mechanical_problem")

        medical_emergency = d.pop("medical_emergency")

        other = d.pop("other")

        police_activity = d.pop("police_activity")

        power_problem = d.pop("power_problem")

        signal_problem = d.pop("signal_problem")

        switch_problem = d.pop("switch_problem")

        track_issue = d.pop("track_issue")

        track_work = d.pop("track_work")

        line_delay_entry = cls(
            date=date,
            line=line,
            total_delay_time=total_delay_time,
            brake_problem=brake_problem,
            car_traffic=car_traffic,
            disabled_vehicle=disabled_vehicle,
            door_problem=door_problem,
            fire=fire,
            flooding=flooding,
            mechanical_problem=mechanical_problem,
            medical_emergency=medical_emergency,
            other=other,
            police_activity=police_activity,
            power_problem=power_problem,
            signal_problem=signal_problem,
            switch_problem=switch_problem,
            track_issue=track_issue,
            track_work=track_work,
        )

        line_delay_entry.additional_properties = d
        return line_delay_entry

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
