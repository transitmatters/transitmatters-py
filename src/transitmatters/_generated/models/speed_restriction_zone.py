from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast


T = TypeVar("T", bound="SpeedRestrictionZone")


@_attrs_define
class SpeedRestrictionZone:
    """A speed restriction in effect on a line.

    Attributes:
        id: Restriction ID.
        date: Date of the data (`YYYY-MM-DD`).
        lineId: Line ID (e.g. `line-Red`).
        description: Location description.
        direction: Track direction (e.g. `NB`, `SB`).
        reason: Reason for the restriction.
        fromStopId: GTFS stop ID where the restriction starts.
        toStopId: GTFS stop ID where the restriction ends, or `null` for a single location.
        reported: Date the restriction was reported (`YYYY-MM-DD`).
        speedMph: Speed limit in miles per hour.
        trackFeet: Length of restricted track in feet.

        Attributes:
            id (str):
            date (str):
            line_id (str):
            description (str):
            direction (str):
            reason (str):
            reported (str):
            speed_mph (int):
            track_feet (int):
            from_stop_id (None | str | Unset):
            to_stop_id (None | str | Unset):
    """

    id: str
    date: str
    line_id: str
    description: str
    direction: str
    reason: str
    reported: str
    speed_mph: int
    track_feet: int
    from_stop_id: None | str | Unset = UNSET
    to_stop_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        date = self.date

        line_id = self.line_id

        description = self.description

        direction = self.direction

        reason = self.reason

        reported = self.reported

        speed_mph = self.speed_mph

        track_feet = self.track_feet

        from_stop_id: None | str | Unset
        if isinstance(self.from_stop_id, Unset):
            from_stop_id = UNSET
        else:
            from_stop_id = self.from_stop_id

        to_stop_id: None | str | Unset
        if isinstance(self.to_stop_id, Unset):
            to_stop_id = UNSET
        else:
            to_stop_id = self.to_stop_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "date": date,
                "lineId": line_id,
                "description": description,
                "direction": direction,
                "reason": reason,
                "reported": reported,
                "speedMph": speed_mph,
                "trackFeet": track_feet,
            }
        )
        if from_stop_id is not UNSET:
            field_dict["fromStopId"] = from_stop_id
        if to_stop_id is not UNSET:
            field_dict["toStopId"] = to_stop_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        date = d.pop("date")

        line_id = d.pop("lineId")

        description = d.pop("description")

        direction = d.pop("direction")

        reason = d.pop("reason")

        reported = d.pop("reported")

        speed_mph = d.pop("speedMph")

        track_feet = d.pop("trackFeet")

        def _parse_from_stop_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        from_stop_id = _parse_from_stop_id(d.pop("fromStopId", UNSET))

        def _parse_to_stop_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        to_stop_id = _parse_to_stop_id(d.pop("toStopId", UNSET))

        speed_restriction_zone = cls(
            id=id,
            date=date,
            line_id=line_id,
            description=description,
            direction=direction,
            reason=reason,
            reported=reported,
            speed_mph=speed_mph,
            track_feet=track_feet,
            from_stop_id=from_stop_id,
            to_stop_id=to_stop_id,
        )

        speed_restriction_zone.additional_properties = d
        return speed_restriction_zone

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
