from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.station_stop import StationStop
    from ..models.stops_response_direction import StopsResponseDirection


T = TypeVar("T", bound="StopsResponse")


@_attrs_define
class StopsResponse:
    """Response for `/api/stops/{route_id}` — station/stop info for a route.

    Attributes:
        type: Route type: `rapidtransit`, `bus`, `commuter-rail` or `ferry`.
        direction: Map of direction ID to direction name (e.g., `{"0": "Southbound"}`).
        stations: Ordered list of stations/stops along the route.
        service_start: Service start date, if applicable.
        service_end: Service end date, if applicable.

    """

    type_: str
    direction: StopsResponseDirection
    stations: list[StationStop]
    service_start: None | str | Unset = UNSET
    service_end: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        direction = self.direction.to_dict()

        stations = []
        for stations_item_data in self.stations:
            stations_item = stations_item_data.to_dict()
            stations.append(stations_item)

        service_start: None | str | Unset
        if isinstance(self.service_start, Unset):
            service_start = UNSET
        else:
            service_start = self.service_start

        service_end: None | str | Unset
        if isinstance(self.service_end, Unset):
            service_end = UNSET
        else:
            service_end = self.service_end

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "direction": direction,
                "stations": stations,
            }
        )
        if service_start is not UNSET:
            field_dict["service_start"] = service_start
        if service_end is not UNSET:
            field_dict["service_end"] = service_end

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.station_stop import StationStop  # noqa: PLC0415
        from ..models.stops_response_direction import StopsResponseDirection  # noqa: PLC0415

        d = dict(src_dict)
        type_ = d.pop("type")

        direction = StopsResponseDirection.from_dict(d.pop("direction"))

        stations = []
        _stations = d.pop("stations")
        for stations_item_data in _stations:
            stations_item = StationStop.from_dict(stations_item_data)

            stations.append(stations_item)

        def _parse_service_start(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        service_start = _parse_service_start(d.pop("service_start", UNSET))

        def _parse_service_end(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        service_end = _parse_service_end(d.pop("service_end", UNSET))

        stops_response = cls(
            type_=type_,
            direction=direction,
            stations=stations,
            service_start=service_start,
            service_end=service_end,
        )

        stops_response.additional_properties = d
        return stops_response

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
