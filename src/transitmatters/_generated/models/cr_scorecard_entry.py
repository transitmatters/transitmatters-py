from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.cr_scorecard_direction import CrScorecardDirection


T = TypeVar("T", bound="CrScorecardEntry")


@_attrs_define
class CrScorecardEntry:
    """A Commuter Rail schedule measured against Regional Rail standards, averaged over `days` days.

    For a route, entries are per period and have `date`. For `commuter-rail`, entries are per route
    and have `routeId` instead.

    Attributes:
        date: Day, Monday of the week, or first day of the month (`YYYY-MM-DD`).
        routeId: Route ID.
        days: Days averaged.
        outbound: Outbound service.
        inbound: Inbound service.
        peakTrips: Peak trains, both directions.
        reversePeakTrips: Reverse-peak trains, both directions.

    """

    days: int
    outbound: CrScorecardDirection
    """ Scheduled service in one direction, measured at the Boston terminal. Values are averages over the days.

    Attributes:
        trips: Trains.
        firstTrip: First train, in seconds after midnight.
        lastTrip: Last train, in seconds after midnight.
        maxGapMidday: Longest midday wait, in minutes.
        maxGapEvening: Longest evening wait, in minutes.
        hoursAtTarget: Hours from 5am to 1am with a train at least every 30 minutes.
        clockFaceShare: Share of trains on a repeating hourly pattern (0-1).
        byHour: Trains in each hour of the day, starting at midnight. """
    inbound: CrScorecardDirection
    """ Scheduled service in one direction, measured at the Boston terminal. Values are averages over the days.

    Attributes:
        trips: Trains.
        firstTrip: First train, in seconds after midnight.
        lastTrip: Last train, in seconds after midnight.
        maxGapMidday: Longest midday wait, in minutes.
        maxGapEvening: Longest evening wait, in minutes.
        hoursAtTarget: Hours from 5am to 1am with a train at least every 30 minutes.
        clockFaceShare: Share of trains on a repeating hourly pattern (0-1).
        byHour: Trains in each hour of the day, starting at midnight. """
    date: None | str | Unset = UNSET
    route_id: None | str | Unset = UNSET
    peak_trips: float | None | Unset = UNSET
    reverse_peak_trips: float | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        days = self.days

        outbound = self.outbound.to_dict()

        inbound = self.inbound.to_dict()

        date: None | str | Unset
        if isinstance(self.date, Unset):
            date = UNSET
        else:
            date = self.date

        route_id: None | str | Unset
        if isinstance(self.route_id, Unset):
            route_id = UNSET
        else:
            route_id = self.route_id

        peak_trips: float | None | Unset
        if isinstance(self.peak_trips, Unset):
            peak_trips = UNSET
        else:
            peak_trips = self.peak_trips

        reverse_peak_trips: float | None | Unset
        if isinstance(self.reverse_peak_trips, Unset):
            reverse_peak_trips = UNSET
        else:
            reverse_peak_trips = self.reverse_peak_trips

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "days": days,
                "outbound": outbound,
                "inbound": inbound,
            }
        )
        if date is not UNSET:
            field_dict["date"] = date
        if route_id is not UNSET:
            field_dict["routeId"] = route_id
        if peak_trips is not UNSET:
            field_dict["peakTrips"] = peak_trips
        if reverse_peak_trips is not UNSET:
            field_dict["reversePeakTrips"] = reverse_peak_trips

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cr_scorecard_direction import CrScorecardDirection  # noqa: PLC0415

        d = dict(src_dict)
        days = d.pop("days")

        outbound = CrScorecardDirection.from_dict(d.pop("outbound"))

        inbound = CrScorecardDirection.from_dict(d.pop("inbound"))

        def _parse_date(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        date = _parse_date(d.pop("date", UNSET))

        def _parse_route_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        route_id = _parse_route_id(d.pop("routeId", UNSET))

        def _parse_peak_trips(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        peak_trips = _parse_peak_trips(d.pop("peakTrips", UNSET))

        def _parse_reverse_peak_trips(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        reverse_peak_trips = _parse_reverse_peak_trips(d.pop("reversePeakTrips", UNSET))

        cr_scorecard_entry = cls(
            days=days,
            outbound=outbound,
            inbound=inbound,
            date=date,
            route_id=route_id,
            peak_trips=peak_trips,
            reverse_peak_trips=reverse_peak_trips,
        )

        cr_scorecard_entry.additional_properties = d
        return cr_scorecard_entry

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
