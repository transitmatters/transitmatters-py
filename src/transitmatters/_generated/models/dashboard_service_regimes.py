from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.dashboard_service_regime import DashboardServiceRegime


T = TypeVar("T", bound="DashboardServiceRegimes")


@_attrs_define
class DashboardServiceRegimes:
    """A line's scheduled service at different points in time.

    Attributes:
        current: Current service.
        oneYearAgo: Service one year ago.
        baseline: Pre-COVID baseline service.

    """

    current: DashboardServiceRegime
    """ Scheduled service by day type.

    Attributes:
        weekday: Weekday service.
        saturday: Saturday service.
        sunday: Sunday service. """
    one_year_ago: DashboardServiceRegime
    """ Scheduled service by day type.

    Attributes:
        weekday: Weekday service.
        saturday: Saturday service.
        sunday: Sunday service. """
    baseline: DashboardServiceRegime
    """ Scheduled service by day type.

    Attributes:
        weekday: Weekday service.
        saturday: Saturday service.
        sunday: Sunday service. """
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        current = self.current.to_dict()

        one_year_ago = self.one_year_ago.to_dict()

        baseline = self.baseline.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "current": current,
                "oneYearAgo": one_year_ago,
                "baseline": baseline,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.dashboard_service_regime import DashboardServiceRegime  # noqa: PLC0415

        d = dict(src_dict)
        current = DashboardServiceRegime.from_dict(d.pop("current"))

        one_year_ago = DashboardServiceRegime.from_dict(d.pop("oneYearAgo"))

        baseline = DashboardServiceRegime.from_dict(d.pop("baseline"))

        dashboard_service_regimes = cls(
            current=current,
            one_year_ago=one_year_ago,
            baseline=baseline,
        )

        dashboard_service_regimes.additional_properties = d
        return dashboard_service_regimes

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
