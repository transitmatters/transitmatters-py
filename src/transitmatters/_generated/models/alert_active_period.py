from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast


T = TypeVar("T", bound="AlertActivePeriod")


@_attrs_define
class AlertActivePeriod:
    """A period during which a live alert is active.

    Attributes:
        start: Start time, ISO 8601 with offset.
        end: End time, ISO 8601 with offset, or `null` if open-ended.
        current: Whether the period includes the current time.
        upcoming: Whether the period has not started yet, or is open-ended.

        Attributes:
            current (bool):
            upcoming (bool):
            start (None | str | Unset):
            end (None | str | Unset):
    """

    current: bool
    upcoming: bool
    start: None | str | Unset = UNSET
    end: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        current = self.current

        upcoming = self.upcoming

        start: None | str | Unset
        if isinstance(self.start, Unset):
            start = UNSET
        else:
            start = self.start

        end: None | str | Unset
        if isinstance(self.end, Unset):
            end = UNSET
        else:
            end = self.end

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "current": current,
                "upcoming": upcoming,
            }
        )
        if start is not UNSET:
            field_dict["start"] = start
        if end is not UNSET:
            field_dict["end"] = end

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        current = d.pop("current")

        upcoming = d.pop("upcoming")

        def _parse_start(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        start = _parse_start(d.pop("start", UNSET))

        def _parse_end(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        end = _parse_end(d.pop("end", UNSET))

        alert_active_period = cls(
            current=current,
            upcoming=upcoming,
            start=start,
            end=end,
        )

        alert_active_period.additional_properties = d
        return alert_active_period

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
