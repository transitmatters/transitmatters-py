from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.dashboard_summary import DashboardSummary
    from ..models.service_ridership_dashboard_response_linedata import (
        ServiceRidershipDashboardResponseLinedata,
    )
    from ..models.service_ridership_dashboard_response_modedata import (
        ServiceRidershipDashboardResponseModedata,
    )


T = TypeVar("T", bound="ServiceRidershipDashboardResponse")


@_attrs_define
class ServiceRidershipDashboardResponse:
    """Response for `/api/service_ridership_dashboard` — system-wide summary.

    Attributes:
        summaryData: System-wide summary.
        modeData: Summaries keyed by mode: `rapid-transit`, `regional-rail`, `bus`, `boat`.
        lineData: Per-line data keyed by line ID.

    """

    summary_data: DashboardSummary
    """ System-wide or per-mode service and ridership summary.

    Attributes:
        totalRidershipHistory: Weekly median ridership keyed by week start date (`YYYY-MM-DD`).
        totalServiceHistory: Weekly median scheduled trips keyed by week start date.
        totalRidershipPercentage: Currently always 0.
        totalServicePercentage: Currently always 0.
        totalPassengers: Weekly median ridership in the latest week.
        totalTrips: Weekly median scheduled trips in the latest week.
        totalRoutesCancelled: Number of routes with cancelled service.
        totalReducedService: Number of routes with reduced service.
        totalIncreasedService: Number of routes with increased service.
        startDate: First date covered (`YYYY-MM-DD`).
        endDate: Last date covered (`YYYY-MM-DD`). """
    mode_data: ServiceRidershipDashboardResponseModedata
    line_data: ServiceRidershipDashboardResponseLinedata
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        summary_data = self.summary_data.to_dict()

        mode_data = self.mode_data.to_dict()

        line_data = self.line_data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "summaryData": summary_data,
                "modeData": mode_data,
                "lineData": line_data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.dashboard_summary import DashboardSummary  # noqa: PLC0415
        from ..models.service_ridership_dashboard_response_linedata import (
            ServiceRidershipDashboardResponseLinedata,
        )  # noqa: PLC0415
        from ..models.service_ridership_dashboard_response_modedata import (
            ServiceRidershipDashboardResponseModedata,
        )  # noqa: PLC0415

        d = dict(src_dict)
        summary_data = DashboardSummary.from_dict(d.pop("summaryData"))

        mode_data = ServiceRidershipDashboardResponseModedata.from_dict(
            d.pop("modeData")
        )

        line_data = ServiceRidershipDashboardResponseLinedata.from_dict(
            d.pop("lineData")
        )

        service_ridership_dashboard_response = cls(
            summary_data=summary_data,
            mode_data=mode_data,
            line_data=line_data,
        )

        service_ridership_dashboard_response.additional_properties = d
        return service_ridership_dashboard_response

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
