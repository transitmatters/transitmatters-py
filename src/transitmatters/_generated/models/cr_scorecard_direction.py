from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast


T = TypeVar("T", bound="CrScorecardDirection")


@_attrs_define
class CrScorecardDirection:
    """Scheduled service in one direction, measured at the Boston terminal. Values are averages over the days.

    Attributes:
        trips: Trains.
        firstTrip: First train, in seconds after midnight.
        lastTrip: Last train, in seconds after midnight.
        maxGapMidday: Longest midday wait, in minutes.
        maxGapEvening: Longest evening wait, in minutes.
        hoursAtTarget: Hours from 5am to 1am with a train at least every 30 minutes.
        clockFaceShare: Share of trains on a repeating hourly pattern (0-1).
        byHour: Trains in each hour of the day, starting at midnight.

    """

    trips: float | None | Unset = UNSET
    first_trip: float | None | Unset = UNSET
    last_trip: float | None | Unset = UNSET
    max_gap_midday: float | None | Unset = UNSET
    max_gap_evening: float | None | Unset = UNSET
    hours_at_target: float | None | Unset = UNSET
    clock_face_share: float | None | Unset = UNSET
    by_hour: list[float | None] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        trips: float | None | Unset
        if isinstance(self.trips, Unset):
            trips = UNSET
        else:
            trips = self.trips

        first_trip: float | None | Unset
        if isinstance(self.first_trip, Unset):
            first_trip = UNSET
        else:
            first_trip = self.first_trip

        last_trip: float | None | Unset
        if isinstance(self.last_trip, Unset):
            last_trip = UNSET
        else:
            last_trip = self.last_trip

        max_gap_midday: float | None | Unset
        if isinstance(self.max_gap_midday, Unset):
            max_gap_midday = UNSET
        else:
            max_gap_midday = self.max_gap_midday

        max_gap_evening: float | None | Unset
        if isinstance(self.max_gap_evening, Unset):
            max_gap_evening = UNSET
        else:
            max_gap_evening = self.max_gap_evening

        hours_at_target: float | None | Unset
        if isinstance(self.hours_at_target, Unset):
            hours_at_target = UNSET
        else:
            hours_at_target = self.hours_at_target

        clock_face_share: float | None | Unset
        if isinstance(self.clock_face_share, Unset):
            clock_face_share = UNSET
        else:
            clock_face_share = self.clock_face_share

        by_hour: list[float | None] | None | Unset
        if isinstance(self.by_hour, Unset):
            by_hour = UNSET
        elif isinstance(self.by_hour, list):
            by_hour = []
            for by_hour_type_0_item_data in self.by_hour:
                by_hour_type_0_item: float | None
                by_hour_type_0_item = by_hour_type_0_item_data
                by_hour.append(by_hour_type_0_item)

        else:
            by_hour = self.by_hour

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if trips is not UNSET:
            field_dict["trips"] = trips
        if first_trip is not UNSET:
            field_dict["firstTrip"] = first_trip
        if last_trip is not UNSET:
            field_dict["lastTrip"] = last_trip
        if max_gap_midday is not UNSET:
            field_dict["maxGapMidday"] = max_gap_midday
        if max_gap_evening is not UNSET:
            field_dict["maxGapEvening"] = max_gap_evening
        if hours_at_target is not UNSET:
            field_dict["hoursAtTarget"] = hours_at_target
        if clock_face_share is not UNSET:
            field_dict["clockFaceShare"] = clock_face_share
        if by_hour is not UNSET:
            field_dict["byHour"] = by_hour

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_trips(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        trips = _parse_trips(d.pop("trips", UNSET))

        def _parse_first_trip(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        first_trip = _parse_first_trip(d.pop("firstTrip", UNSET))

        def _parse_last_trip(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        last_trip = _parse_last_trip(d.pop("lastTrip", UNSET))

        def _parse_max_gap_midday(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        max_gap_midday = _parse_max_gap_midday(d.pop("maxGapMidday", UNSET))

        def _parse_max_gap_evening(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        max_gap_evening = _parse_max_gap_evening(d.pop("maxGapEvening", UNSET))

        def _parse_hours_at_target(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        hours_at_target = _parse_hours_at_target(d.pop("hoursAtTarget", UNSET))

        def _parse_clock_face_share(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        clock_face_share = _parse_clock_face_share(d.pop("clockFaceShare", UNSET))

        def _parse_by_hour(data: object) -> list[float | None] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                by_hour_type_0 = []
                _by_hour_type_0 = data
                for by_hour_type_0_item_data in _by_hour_type_0:

                    def _parse_by_hour_type_0_item(data: object) -> float | None:
                        if data is None:
                            return data
                        return cast(float | None, data)

                    by_hour_type_0_item = _parse_by_hour_type_0_item(
                        by_hour_type_0_item_data
                    )

                    by_hour_type_0.append(by_hour_type_0_item)

                return by_hour_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[float | None] | None | Unset, data)

        by_hour = _parse_by_hour(d.pop("byHour", UNSET))

        cr_scorecard_direction = cls(
            trips=trips,
            first_trip=first_trip,
            last_trip=last_trip,
            max_gap_midday=max_gap_midday,
            max_gap_evening=max_gap_evening,
            hours_at_target=hours_at_target,
            clock_face_share=clock_face_share,
            by_hour=by_hour,
        )

        cr_scorecard_direction.additional_properties = d
        return cr_scorecard_direction

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
