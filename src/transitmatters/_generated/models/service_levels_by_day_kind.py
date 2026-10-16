from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.by_day_kind_service_levels import ByDayKindServiceLevels


T = TypeVar("T", bound="ServiceLevelsByDayKind")


@_attrs_define
class ServiceLevelsByDayKind:
    """Service levels grouped by day type. A day type is `null` when the date range doesn't include one.

    Attributes:
        weekday: Weekday service breakdown.
        saturday: Saturday service breakdown.
        sunday: Sunday service breakdown.

    """

    weekday: ByDayKindServiceLevels | None | Unset = UNSET
    """ Scheduled service for a specific day type (weekday, Saturday, or Sunday).

    Attributes:
        date: Reference date (YYYY-MM-DD).
        service_levels: Scheduled trips by hour (index 0 = midnight); empty if unavailable. """
    saturday: ByDayKindServiceLevels | None | Unset = UNSET
    """ Scheduled service for a specific day type (weekday, Saturday, or Sunday).

    Attributes:
        date: Reference date (YYYY-MM-DD).
        service_levels: Scheduled trips by hour (index 0 = midnight); empty if unavailable. """
    sunday: ByDayKindServiceLevels | None | Unset = UNSET
    """ Scheduled service for a specific day type (weekday, Saturday, or Sunday).

    Attributes:
        date: Reference date (YYYY-MM-DD).
        service_levels: Scheduled trips by hour (index 0 = midnight); empty if unavailable. """
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.by_day_kind_service_levels import ByDayKindServiceLevels  # noqa: PLC0415

        weekday: dict[str, Any] | None | Unset
        if isinstance(self.weekday, Unset):
            weekday = UNSET
        elif isinstance(self.weekday, ByDayKindServiceLevels):
            weekday = self.weekday.to_dict()
        else:
            weekday = self.weekday

        saturday: dict[str, Any] | None | Unset
        if isinstance(self.saturday, Unset):
            saturday = UNSET
        elif isinstance(self.saturday, ByDayKindServiceLevels):
            saturday = self.saturday.to_dict()
        else:
            saturday = self.saturday

        sunday: dict[str, Any] | None | Unset
        if isinstance(self.sunday, Unset):
            sunday = UNSET
        elif isinstance(self.sunday, ByDayKindServiceLevels):
            sunday = self.sunday.to_dict()
        else:
            sunday = self.sunday

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if weekday is not UNSET:
            field_dict["weekday"] = weekday
        if saturday is not UNSET:
            field_dict["saturday"] = saturday
        if sunday is not UNSET:
            field_dict["sunday"] = sunday

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.by_day_kind_service_levels import ByDayKindServiceLevels  # noqa: PLC0415

        d = dict(src_dict)

        def _parse_weekday(data: object) -> ByDayKindServiceLevels | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_by_day_kind_service_levels_type_0 = (
                    ByDayKindServiceLevels.from_dict(data)
                )

                return componentsschemas_by_day_kind_service_levels_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ByDayKindServiceLevels | None | Unset, data)

        weekday = _parse_weekday(d.pop("weekday", UNSET))

        def _parse_saturday(data: object) -> ByDayKindServiceLevels | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_by_day_kind_service_levels_type_0 = (
                    ByDayKindServiceLevels.from_dict(data)
                )

                return componentsschemas_by_day_kind_service_levels_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ByDayKindServiceLevels | None | Unset, data)

        saturday = _parse_saturday(d.pop("saturday", UNSET))

        def _parse_sunday(data: object) -> ByDayKindServiceLevels | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_by_day_kind_service_levels_type_0 = (
                    ByDayKindServiceLevels.from_dict(data)
                )

                return componentsschemas_by_day_kind_service_levels_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ByDayKindServiceLevels | None | Unset, data)

        sunday = _parse_sunday(d.pop("sunday", UNSET))

        service_levels_by_day_kind = cls(
            weekday=weekday,
            saturday=saturday,
            sunday=sunday,
        )

        service_levels_by_day_kind.additional_properties = d
        return service_levels_by_day_kind

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
