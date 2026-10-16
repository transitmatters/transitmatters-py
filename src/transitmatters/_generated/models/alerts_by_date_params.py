from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast


T = TypeVar("T", bound="AlertsByDateParams")


@_attrs_define
class AlertsByDateParams:
    """Query parameters for `/api/alerts/{user_date}`.

    Attributes:
        route: One or more route IDs to filter alerts by.

    """

    route: list[str] | Unset = UNSET
    """ MBTA route ID. Rapid transit: `Red`, `Orange`, `Blue`, `Green-B`-`Green-E`, `Mattapan`. Bus: numeric string
    (e.g. `1`, `66`). Commuter rail: `CR-{line}` (e.g. `CR-Fairmount`). Ferry: `Boat-F1`, `Boat-F4`, etc. Use
    `/api/routes` to list all valid route IDs. """
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        route: list[str] | Unset = UNSET
        if not isinstance(self.route, Unset):
            route = self.route

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if route is not UNSET:
            field_dict["route"] = route

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        route = cast(list[str], d.pop("route", UNSET))

        alerts_by_date_params = cls(
            route=route,
        )

        alerts_by_date_params.additional_properties = d
        return alerts_by_date_params

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
