from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
import datetime


T = TypeVar("T", bound="AggregateTravelTimesParams")


@_attrs_define
class AggregateTravelTimesParams:
    """Query parameters for `/api/aggregate/traveltimes` and `/api/aggregate/traveltimes2`.

    Attributes:
        start_date: Start of date range (YYYY-MM-DD).
        end_date: End of date range (YYYY-MM-DD).
        from_stop: One or more origin stop IDs.
        to_stop: One or more destination stop IDs.

    """

    start_date: datetime.date
    """ Start of the date range, inclusive (YYYY-MM-DD). """
    end_date: datetime.date
    """ End of the date range, inclusive (YYYY-MM-DD). """
    from_stop: list[str] | Unset = UNSET
    """ Origin MBTA stop ID. Rapid transit: 5-digit numeric (e.g. `70061`). Bus: `{route}-{direction}-{n}` (e.g.
    `1-0-110`). Commuter rail: `{route}_{direction}_{stop_code}` (e.g. `CR-Fairmount_0_DB-2205-01`). Use
    `/api/stops/{route_id}` to look up valid stop IDs for a route. """
    to_stop: list[str] | Unset = UNSET
    """ Destination MBTA stop ID. Rapid transit: 5-digit numeric (e.g. `70061`). Bus: `{route}-{direction}-{n}`
    (e.g. `1-0-110`). Commuter rail: `{route}_{direction}_{stop_code}` (e.g. `CR-Fairmount_0_DB-2205-01`). Use
    `/api/stops/{route_id}` to look up valid stop IDs for a route. """
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        start_date = self.start_date.isoformat()

        end_date = self.end_date.isoformat()

        from_stop: list[str] | Unset = UNSET
        if not isinstance(self.from_stop, Unset):
            from_stop = self.from_stop

        to_stop: list[str] | Unset = UNSET
        if not isinstance(self.to_stop, Unset):
            to_stop = self.to_stop

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "start_date": start_date,
                "end_date": end_date,
            }
        )
        if from_stop is not UNSET:
            field_dict["from_stop"] = from_stop
        if to_stop is not UNSET:
            field_dict["to_stop"] = to_stop

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        start_date = datetime.date.fromisoformat(d.pop("start_date"))

        end_date = datetime.date.fromisoformat(d.pop("end_date"))

        from_stop = cast(list[str], d.pop("from_stop", UNSET))

        to_stop = cast(list[str], d.pop("to_stop", UNSET))

        aggregate_travel_times_params = cls(
            start_date=start_date,
            end_date=end_date,
            from_stop=from_stop,
            to_stop=to_stop,
        )

        aggregate_travel_times_params.additional_properties = d
        return aggregate_travel_times_params

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
