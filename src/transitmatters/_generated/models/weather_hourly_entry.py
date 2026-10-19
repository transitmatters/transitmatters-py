from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast


T = TypeVar("T", bound="WeatherHourlyEntry")


@_attrs_define
class WeatherHourlyEntry:
    """One hour's weather in downtown Boston.

    Attributes:
        timestamp: Local-time ISO hour (America/New_York, no offset), e.g. `2026-04-22T14:00`.
        temperature_f: Air temperature in °F.
        weather_code: WMO weather code from Open-Meteo.
        condition: Coarse label, e.g. `clear`, `cloudy`, `fog`, `rain`, `snow`, `storm` or `unknown`.
        precipitation_in: Precipitation in inches for the hour.
        humidity_pct: Relative humidity at 2m (0-100).
        wind_mph: Wind speed at 10m in mph.

    """

    timestamp: str
    temperature_f: float | None | Unset = UNSET
    weather_code: int | None | Unset = UNSET
    condition: None | str | Unset = UNSET
    precipitation_in: float | None | Unset = UNSET
    humidity_pct: int | None | Unset = UNSET
    wind_mph: float | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        timestamp = self.timestamp

        temperature_f: float | None | Unset
        if isinstance(self.temperature_f, Unset):
            temperature_f = UNSET
        else:
            temperature_f = self.temperature_f

        weather_code: int | None | Unset
        if isinstance(self.weather_code, Unset):
            weather_code = UNSET
        else:
            weather_code = self.weather_code

        condition: None | str | Unset
        if isinstance(self.condition, Unset):
            condition = UNSET
        else:
            condition = self.condition

        precipitation_in: float | None | Unset
        if isinstance(self.precipitation_in, Unset):
            precipitation_in = UNSET
        else:
            precipitation_in = self.precipitation_in

        humidity_pct: int | None | Unset
        if isinstance(self.humidity_pct, Unset):
            humidity_pct = UNSET
        else:
            humidity_pct = self.humidity_pct

        wind_mph: float | None | Unset
        if isinstance(self.wind_mph, Unset):
            wind_mph = UNSET
        else:
            wind_mph = self.wind_mph

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "timestamp": timestamp,
            }
        )
        if temperature_f is not UNSET:
            field_dict["temperature_f"] = temperature_f
        if weather_code is not UNSET:
            field_dict["weather_code"] = weather_code
        if condition is not UNSET:
            field_dict["condition"] = condition
        if precipitation_in is not UNSET:
            field_dict["precipitation_in"] = precipitation_in
        if humidity_pct is not UNSET:
            field_dict["humidity_pct"] = humidity_pct
        if wind_mph is not UNSET:
            field_dict["wind_mph"] = wind_mph

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        timestamp = d.pop("timestamp")

        def _parse_temperature_f(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        temperature_f = _parse_temperature_f(d.pop("temperature_f", UNSET))

        def _parse_weather_code(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        weather_code = _parse_weather_code(d.pop("weather_code", UNSET))

        def _parse_condition(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        condition = _parse_condition(d.pop("condition", UNSET))

        def _parse_precipitation_in(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        precipitation_in = _parse_precipitation_in(d.pop("precipitation_in", UNSET))

        def _parse_humidity_pct(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        humidity_pct = _parse_humidity_pct(d.pop("humidity_pct", UNSET))

        def _parse_wind_mph(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        wind_mph = _parse_wind_mph(d.pop("wind_mph", UNSET))

        weather_hourly_entry = cls(
            timestamp=timestamp,
            temperature_f=temperature_f,
            weather_code=weather_code,
            condition=condition,
            precipitation_in=precipitation_in,
            humidity_pct=humidity_pct,
            wind_mph=wind_mph,
        )

        weather_hourly_entry.additional_properties = d
        return weather_hourly_entry

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
