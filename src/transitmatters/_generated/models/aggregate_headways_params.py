from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
import datetime


T = TypeVar("T", bound="AggregateHeadwaysParams")


@_attrs_define
class AggregateHeadwaysParams:
    """Query parameters for `/api/aggregate/headways`.

    Attributes:
        start_date: Start of date range (YYYY-MM-DD).
        end_date: End of date range (YYYY-MM-DD).
        stop: One or more stop IDs.

    """

    start_date: datetime.date
    """ Start of the date range, inclusive (YYYY-MM-DD). """
    end_date: datetime.date
    """ End of the date range, inclusive (YYYY-MM-DD). """
    stop: list[str] | Unset = UNSET
    """ MBTA stop ID. Rapid transit: 5-digit numeric (e.g. `70061`). Bus: `{route}-{direction}-{n}` (e.g.
    `1-0-110`). Commuter rail: `{route}_{direction}_{stop_code}` (e.g. `CR-Fairmount_0_DB-2205-01`). Use
    `/api/stops/{route_id}` to look up valid stop IDs for a route. """
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        start_date = self.start_date.isoformat()

        end_date = self.end_date.isoformat()

        stop: list[str] | Unset = UNSET
        if not isinstance(self.stop, Unset):
            stop = self.stop

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "start_date": start_date,
                "end_date": end_date,
            }
        )
        if stop is not UNSET:
            field_dict["stop"] = stop

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        start_date = datetime.date.fromisoformat(d.pop("start_date"))

        end_date = datetime.date.fromisoformat(d.pop("end_date"))

        stop = cast(list[str], d.pop("stop", UNSET))

        aggregate_headways_params = cls(
            start_date=start_date,
            end_date=end_date,
            stop=stop,
        )

        aggregate_headways_params.additional_properties = d
        return aggregate_headways_params

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
