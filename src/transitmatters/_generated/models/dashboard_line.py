from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.dashboard_line_ridershiphistory import DashboardLineRidershiphistory
    from ..models.dashboard_line_servicehistory import DashboardLineServicehistory
    from ..models.dashboard_service_regimes import DashboardServiceRegimes


T = TypeVar("T", bound="DashboardLine")


@_attrs_define
class DashboardLine:
    """Service and ridership data for one line.

    Attributes:
        id: Line ID (e.g. `line-Red`, `line-1`, `line-Fairmount`, `line-Boat-F1`).
        shortName: Short name; may be empty.
        longName: Long name.
        routeIds: Route IDs on the line.
        startDate: First date covered (`YYYY-MM-DD`).
        lineKind: `red`, `orange`, `blue`, `green`, `silver`, `regional-rail`, `bus` or `boat`.
        ridershipHistory: Weekly median ridership keyed by week start date, or `null` when unavailable.
        serviceHistory: Weekly median scheduled trips keyed by week start date.
        serviceRegimes: Scheduled service now, a year ago, and at the pre-COVID baseline.

        Attributes:
            id (str):
            short_name (str):
            long_name (str):
            route_ids (list[str]):
            start_date (str):
            line_kind (str):
            service_regimes (DashboardServiceRegimes): A line's scheduled service at different points in time.

                Attributes:
                    current: Current service.
                    oneYearAgo: Service one year ago.
                    baseline: Pre-COVID baseline service.
            ridership_history (DashboardLineRidershiphistory | None | Unset):
            service_history (DashboardLineServicehistory | None | Unset):
    """

    id: str
    short_name: str
    long_name: str
    route_ids: list[str]
    start_date: str
    line_kind: str
    service_regimes: DashboardServiceRegimes
    ridership_history: DashboardLineRidershiphistory | None | Unset = UNSET
    service_history: DashboardLineServicehistory | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.dashboard_line_ridershiphistory import (
            DashboardLineRidershiphistory,
        )  # noqa: PLC0415
        from ..models.dashboard_line_servicehistory import DashboardLineServicehistory  # noqa: PLC0415

        id = self.id

        short_name = self.short_name

        long_name = self.long_name

        route_ids = self.route_ids

        start_date = self.start_date

        line_kind = self.line_kind

        service_regimes = self.service_regimes.to_dict()

        ridership_history: dict[str, Any] | None | Unset
        if isinstance(self.ridership_history, Unset):
            ridership_history = UNSET
        elif isinstance(self.ridership_history, DashboardLineRidershiphistory):
            ridership_history = self.ridership_history.to_dict()
        else:
            ridership_history = self.ridership_history

        service_history: dict[str, Any] | None | Unset
        if isinstance(self.service_history, Unset):
            service_history = UNSET
        elif isinstance(self.service_history, DashboardLineServicehistory):
            service_history = self.service_history.to_dict()
        else:
            service_history = self.service_history

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "shortName": short_name,
                "longName": long_name,
                "routeIds": route_ids,
                "startDate": start_date,
                "lineKind": line_kind,
                "serviceRegimes": service_regimes,
            }
        )
        if ridership_history is not UNSET:
            field_dict["ridershipHistory"] = ridership_history
        if service_history is not UNSET:
            field_dict["serviceHistory"] = service_history

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.dashboard_line_ridershiphistory import (
            DashboardLineRidershiphistory,
        )  # noqa: PLC0415
        from ..models.dashboard_line_servicehistory import DashboardLineServicehistory  # noqa: PLC0415
        from ..models.dashboard_service_regimes import DashboardServiceRegimes  # noqa: PLC0415

        d = dict(src_dict)
        id = d.pop("id")

        short_name = d.pop("shortName")

        long_name = d.pop("longName")

        route_ids = cast(list[str], d.pop("routeIds"))

        start_date = d.pop("startDate")

        line_kind = d.pop("lineKind")

        service_regimes = DashboardServiceRegimes.from_dict(d.pop("serviceRegimes"))

        def _parse_ridership_history(
            data: object,
        ) -> DashboardLineRidershiphistory | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                ridership_history_type_0 = DashboardLineRidershiphistory.from_dict(data)

                return ridership_history_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DashboardLineRidershiphistory | None | Unset, data)

        ridership_history = _parse_ridership_history(d.pop("ridershipHistory", UNSET))

        def _parse_service_history(
            data: object,
        ) -> DashboardLineServicehistory | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                service_history_type_0 = DashboardLineServicehistory.from_dict(data)

                return service_history_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DashboardLineServicehistory | None | Unset, data)

        service_history = _parse_service_history(d.pop("serviceHistory", UNSET))

        dashboard_line = cls(
            id=id,
            short_name=short_name,
            long_name=long_name,
            route_ids=route_ids,
            start_date=start_date,
            line_kind=line_kind,
            service_regimes=service_regimes,
            ridership_history=ridership_history,
            service_history=service_history,
        )

        dashboard_line.additional_properties = d
        return dashboard_line

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
