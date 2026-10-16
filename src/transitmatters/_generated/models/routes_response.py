from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import cast


T = TypeVar("T", bound="RoutesResponse")


@_attrs_define
class RoutesResponse:
    """Response for `/api/routes` — lists all available routes by transit mode.

    Attributes:
        rapid_transit: Rapid transit route IDs (e.g., `Red`, `Orange`, `Green`).
        bus: Bus route IDs.
        commuter_rail: Commuter rail route IDs (e.g., `CR-Fairmount`).
        ferry: Ferry route IDs (e.g., `Boat-F1`).

    """

    rapid_transit: list[str]
    bus: list[str]
    commuter_rail: list[str]
    ferry: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        rapid_transit = self.rapid_transit

        bus = self.bus

        commuter_rail = self.commuter_rail

        ferry = self.ferry

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "rapid_transit": rapid_transit,
                "bus": bus,
                "commuter_rail": commuter_rail,
                "ferry": ferry,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        rapid_transit = cast(list[str], d.pop("rapid_transit"))

        bus = cast(list[str], d.pop("bus"))

        commuter_rail = cast(list[str], d.pop("commuter_rail"))

        ferry = cast(list[str], d.pop("ferry"))

        routes_response = cls(
            rapid_transit=rapid_transit,
            bus=bus,
            commuter_rail=commuter_rail,
            ferry=ferry,
        )

        routes_response.additional_properties = d
        return routes_response

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
