from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.alert_active_period import AlertActivePeriod


T = TypeVar("T", bound="LiveAlert")


@_attrs_define
class LiveAlert:
    """A current MBTA service alert, reformatted by the dashboard.

    Which fields are set depends on `type`:
    - `DELAY`, `DETOUR`: `stops` holds numeric rapid transit stop IDs as integers, and `routes` is set.
    - `SHUTTLE`, `SUSPENSION`, `STOP_CLOSURE`: `stops` holds non-numeric stop IDs (e.g. `place-dwnxg`).
    - `ELEVATOR_CLOSURE`, `ESCALATOR_CLOSURE`: `stops` holds non-numeric stop IDs, and `description` is set.

    Attributes:
        id: MBTA alert ID.
        type: MBTA alert effect (see above).
        header: Alert header text.
        active_period: Periods during which the alert is active.
        stops: Affected stop IDs, unordered. Integers for `DELAY` and `DETOUR`, strings otherwise.
        routes: Affected route IDs, possibly repeated (`DELAY` and `DETOUR` only).
        description: Long-form description (elevator and escalator closures only).

        Attributes:
            id (str):
            type_ (str):
            header (str):
            active_period (list[AlertActivePeriod]):
            stops (list[int | str]):
            routes (list[str] | None | Unset):
            description (None | str | Unset):
    """

    id: str
    type_: str
    header: str
    active_period: list[AlertActivePeriod]
    stops: list[int | str]
    routes: list[str] | None | Unset = UNSET
    description: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        type_ = self.type_

        header = self.header

        active_period = []
        for active_period_item_data in self.active_period:
            active_period_item = active_period_item_data.to_dict()
            active_period.append(active_period_item)

        stops = []
        for stops_item_data in self.stops:
            stops_item: int | str
            stops_item = stops_item_data
            stops.append(stops_item)

        routes: list[str] | None | Unset
        if isinstance(self.routes, Unset):
            routes = UNSET
        elif isinstance(self.routes, list):
            routes = self.routes

        else:
            routes = self.routes

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "type": type_,
                "header": header,
                "active_period": active_period,
                "stops": stops,
            }
        )
        if routes is not UNSET:
            field_dict["routes"] = routes
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.alert_active_period import AlertActivePeriod  # noqa: PLC0415

        d = dict(src_dict)
        id = d.pop("id")

        type_ = d.pop("type")

        header = d.pop("header")

        active_period = []
        _active_period = d.pop("active_period")
        for active_period_item_data in _active_period:
            active_period_item = AlertActivePeriod.from_dict(active_period_item_data)

            active_period.append(active_period_item)

        stops = []
        _stops = d.pop("stops")
        for stops_item_data in _stops:

            def _parse_stops_item(data: object) -> int | str:
                return cast(int | str, data)

            stops_item = _parse_stops_item(stops_item_data)

            stops.append(stops_item)

        def _parse_routes(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                routes_type_0 = cast(list[str], data)

                return routes_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        routes = _parse_routes(d.pop("routes", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        live_alert = cls(
            id=id,
            type_=type_,
            header=header,
            active_period=active_period,
            stops=stops,
            routes=routes,
            description=description,
        )

        live_alert.additional_properties = d
        return live_alert

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
