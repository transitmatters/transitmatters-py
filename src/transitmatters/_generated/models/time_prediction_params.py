from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


T = TypeVar("T", bound="TimePredictionParams")


@_attrs_define
class TimePredictionParams:
    """Parameters for the `/api/time_predictions` endpoint.

    Attributes:
        route_id: Route identifier (e.g., `Red`, `CR-Fairmount`).

        Attributes:
            route_id (str): MBTA route ID. Rapid transit: `Red`, `Orange`, `Blue`, `Green-B`-`Green-E`, `Mattapan`. Bus:
                numeric string (e.g. `1`, `66`). Commuter rail: `CR-{line}` (e.g. `CR-Fairmount`). Ferry: `Boat-F1`, `Boat-F4`,
                etc. Use `/api/routes` to list all valid route IDs.
    """

    route_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        route_id = self.route_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "route_id": route_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        route_id = d.pop("route_id")

        time_prediction_params = cls(
            route_id=route_id,
        )

        time_prediction_params.additional_properties = d
        return time_prediction_params

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
