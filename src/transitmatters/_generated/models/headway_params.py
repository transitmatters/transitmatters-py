from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast


T = TypeVar("T", bound="HeadwayParams")


@_attrs_define
class HeadwayParams:
    """Query parameters for `/api/headways/{user_date}`.

    Attributes:
        stop: One or more stop IDs to retrieve headway data for.

        Attributes:
            stop (list[str] | Unset): MBTA stop ID. Rapid transit: 5-digit numeric (e.g. `70061`). Bus:
                `{route}-{direction}-{n}` (e.g. `1-0-110`). Commuter rail: `{route}_{direction}_{stop_code}` (e.g. `CR-
                Fairmount_0_DB-2205-01`). Use `/api/stops/{route_id}` to look up valid stop IDs for a route.
    """

    stop: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        stop: list[str] | Unset = UNSET
        if not isinstance(self.stop, Unset):
            stop = self.stop

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if stop is not UNSET:
            field_dict["stop"] = stop

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        stop = cast(list[str], d.pop("stop", UNSET))

        headway_params = cls(
            stop=stop,
        )

        headway_params.additional_properties = d
        return headway_params

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
