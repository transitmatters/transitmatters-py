from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.dashboard_summary_totalridershiphistory import (
        DashboardSummaryTotalridershiphistory,
    )
    from ..models.dashboard_summary_totalservicehistory import (
        DashboardSummaryTotalservicehistory,
    )


T = TypeVar("T", bound="DashboardSummary")


@_attrs_define
class DashboardSummary:
    """System-wide or per-mode service and ridership summary.

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
        endDate: Last date covered (`YYYY-MM-DD`).

        Attributes:
            total_ridership_percentage (float):
            total_service_percentage (float):
            total_passengers (float):
            total_trips (float):
            total_routes_cancelled (int):
            total_reduced_service (int):
            total_increased_service (int):
            start_date (str):
            end_date (str):
            total_ridership_history (DashboardSummaryTotalridershiphistory | None | Unset):
            total_service_history (DashboardSummaryTotalservicehistory | None | Unset):
    """

    total_ridership_percentage: float
    total_service_percentage: float
    total_passengers: float
    total_trips: float
    total_routes_cancelled: int
    total_reduced_service: int
    total_increased_service: int
    start_date: str
    end_date: str
    total_ridership_history: DashboardSummaryTotalridershiphistory | None | Unset = (
        UNSET
    )
    total_service_history: DashboardSummaryTotalservicehistory | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.dashboard_summary_totalridershiphistory import (
            DashboardSummaryTotalridershiphistory,
        )  # noqa: PLC0415
        from ..models.dashboard_summary_totalservicehistory import (
            DashboardSummaryTotalservicehistory,
        )  # noqa: PLC0415

        total_ridership_percentage = self.total_ridership_percentage

        total_service_percentage = self.total_service_percentage

        total_passengers = self.total_passengers

        total_trips = self.total_trips

        total_routes_cancelled = self.total_routes_cancelled

        total_reduced_service = self.total_reduced_service

        total_increased_service = self.total_increased_service

        start_date = self.start_date

        end_date = self.end_date

        total_ridership_history: dict[str, Any] | None | Unset
        if isinstance(self.total_ridership_history, Unset):
            total_ridership_history = UNSET
        elif isinstance(
            self.total_ridership_history, DashboardSummaryTotalridershiphistory
        ):
            total_ridership_history = self.total_ridership_history.to_dict()
        else:
            total_ridership_history = self.total_ridership_history

        total_service_history: dict[str, Any] | None | Unset
        if isinstance(self.total_service_history, Unset):
            total_service_history = UNSET
        elif isinstance(
            self.total_service_history, DashboardSummaryTotalservicehistory
        ):
            total_service_history = self.total_service_history.to_dict()
        else:
            total_service_history = self.total_service_history

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "totalRidershipPercentage": total_ridership_percentage,
                "totalServicePercentage": total_service_percentage,
                "totalPassengers": total_passengers,
                "totalTrips": total_trips,
                "totalRoutesCancelled": total_routes_cancelled,
                "totalReducedService": total_reduced_service,
                "totalIncreasedService": total_increased_service,
                "startDate": start_date,
                "endDate": end_date,
            }
        )
        if total_ridership_history is not UNSET:
            field_dict["totalRidershipHistory"] = total_ridership_history
        if total_service_history is not UNSET:
            field_dict["totalServiceHistory"] = total_service_history

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.dashboard_summary_totalridershiphistory import (
            DashboardSummaryTotalridershiphistory,
        )  # noqa: PLC0415
        from ..models.dashboard_summary_totalservicehistory import (
            DashboardSummaryTotalservicehistory,
        )  # noqa: PLC0415

        d = dict(src_dict)
        total_ridership_percentage = d.pop("totalRidershipPercentage")

        total_service_percentage = d.pop("totalServicePercentage")

        total_passengers = d.pop("totalPassengers")

        total_trips = d.pop("totalTrips")

        total_routes_cancelled = d.pop("totalRoutesCancelled")

        total_reduced_service = d.pop("totalReducedService")

        total_increased_service = d.pop("totalIncreasedService")

        start_date = d.pop("startDate")

        end_date = d.pop("endDate")

        def _parse_total_ridership_history(
            data: object,
        ) -> DashboardSummaryTotalridershiphistory | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                total_ridership_history_type_0 = (
                    DashboardSummaryTotalridershiphistory.from_dict(data)
                )

                return total_ridership_history_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DashboardSummaryTotalridershiphistory | None | Unset, data)

        total_ridership_history = _parse_total_ridership_history(
            d.pop("totalRidershipHistory", UNSET)
        )

        def _parse_total_service_history(
            data: object,
        ) -> DashboardSummaryTotalservicehistory | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                total_service_history_type_0 = (
                    DashboardSummaryTotalservicehistory.from_dict(data)
                )

                return total_service_history_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DashboardSummaryTotalservicehistory | None | Unset, data)

        total_service_history = _parse_total_service_history(
            d.pop("totalServiceHistory", UNSET)
        )

        dashboard_summary = cls(
            total_ridership_percentage=total_ridership_percentage,
            total_service_percentage=total_service_percentage,
            total_passengers=total_passengers,
            total_trips=total_trips,
            total_routes_cancelled=total_routes_cancelled,
            total_reduced_service=total_reduced_service,
            total_increased_service=total_increased_service,
            start_date=start_date,
            end_date=end_date,
            total_ridership_history=total_ridership_history,
            total_service_history=total_service_history,
        )

        dashboard_summary.additional_properties = d
        return dashboard_summary

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
