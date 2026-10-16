from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.station_stop_stops import StationStopStops


T = TypeVar("T", bound="StationStop")


@_attrs_define
class StationStop:
    """A station or stop along a route.

    Attributes:
        stop_name: Display name of the station.
        branches: Branch identifiers (used for Green Line), or `None`.
        station: Station identifier (e.g., `place-alfcl`).
        order: Position in route order, starting at 1. Usually a whole number, but may be fractional.
        stops: Map of direction ID to list of stop IDs.
        accessible: Whether the station is ADA accessible.
        pedal_park: Whether the station has bike parking.
        enclosed_bike_parking: Whether the station has enclosed bike storage.
        terminus: Whether this is a terminal station.
        disabled: Whether this stop is currently disabled.
        short: Short display name.

    """

    stop_name: str
    station: str
    order: float
    stops: StationStopStops
    branches: list[str] | None | Unset = UNSET
    accessible: bool | None | Unset = UNSET
    pedal_park: bool | None | Unset = UNSET
    enclosed_bike_parking: bool | None | Unset = UNSET
    terminus: bool | None | Unset = UNSET
    disabled: bool | None | Unset = UNSET
    short: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        stop_name = self.stop_name

        station = self.station

        order = self.order

        stops = self.stops.to_dict()

        branches: list[str] | None | Unset
        if isinstance(self.branches, Unset):
            branches = UNSET
        elif isinstance(self.branches, list):
            branches = self.branches

        else:
            branches = self.branches

        accessible: bool | None | Unset
        if isinstance(self.accessible, Unset):
            accessible = UNSET
        else:
            accessible = self.accessible

        pedal_park: bool | None | Unset
        if isinstance(self.pedal_park, Unset):
            pedal_park = UNSET
        else:
            pedal_park = self.pedal_park

        enclosed_bike_parking: bool | None | Unset
        if isinstance(self.enclosed_bike_parking, Unset):
            enclosed_bike_parking = UNSET
        else:
            enclosed_bike_parking = self.enclosed_bike_parking

        terminus: bool | None | Unset
        if isinstance(self.terminus, Unset):
            terminus = UNSET
        else:
            terminus = self.terminus

        disabled: bool | None | Unset
        if isinstance(self.disabled, Unset):
            disabled = UNSET
        else:
            disabled = self.disabled

        short: None | str | Unset
        if isinstance(self.short, Unset):
            short = UNSET
        else:
            short = self.short

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "stop_name": stop_name,
                "station": station,
                "order": order,
                "stops": stops,
            }
        )
        if branches is not UNSET:
            field_dict["branches"] = branches
        if accessible is not UNSET:
            field_dict["accessible"] = accessible
        if pedal_park is not UNSET:
            field_dict["pedal_park"] = pedal_park
        if enclosed_bike_parking is not UNSET:
            field_dict["enclosed_bike_parking"] = enclosed_bike_parking
        if terminus is not UNSET:
            field_dict["terminus"] = terminus
        if disabled is not UNSET:
            field_dict["disabled"] = disabled
        if short is not UNSET:
            field_dict["short"] = short

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.station_stop_stops import StationStopStops  # noqa: PLC0415

        d = dict(src_dict)
        stop_name = d.pop("stop_name")

        station = d.pop("station")

        order = d.pop("order")

        stops = StationStopStops.from_dict(d.pop("stops"))

        def _parse_branches(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                branches_type_0 = cast(list[str], data)

                return branches_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        branches = _parse_branches(d.pop("branches", UNSET))

        def _parse_accessible(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        accessible = _parse_accessible(d.pop("accessible", UNSET))

        def _parse_pedal_park(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        pedal_park = _parse_pedal_park(d.pop("pedal_park", UNSET))

        def _parse_enclosed_bike_parking(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        enclosed_bike_parking = _parse_enclosed_bike_parking(
            d.pop("enclosed_bike_parking", UNSET)
        )

        def _parse_terminus(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        terminus = _parse_terminus(d.pop("terminus", UNSET))

        def _parse_disabled(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        disabled = _parse_disabled(d.pop("disabled", UNSET))

        def _parse_short(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        short = _parse_short(d.pop("short", UNSET))

        station_stop = cls(
            stop_name=stop_name,
            station=station,
            order=order,
            stops=stops,
            branches=branches,
            accessible=accessible,
            pedal_park=pedal_park,
            enclosed_bike_parking=enclosed_bike_parking,
            terminus=terminus,
            disabled=disabled,
            short=short,
        )

        station_stop.additional_properties = d
        return station_stop

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
