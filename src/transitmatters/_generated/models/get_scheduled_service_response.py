from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.scheduled_service_count import ScheduledServiceCount
    from ..models.service_levels_by_day_kind import ServiceLevelsByDayKind


T = TypeVar("T", bound="GetScheduledServiceResponse")


@_attrs_define
class GetScheduledServiceResponse:
    """Response for `/api/scheduledservice` — scheduled service counts.

    Attributes:
        start_date: Requested start date (`YYYY-MM-DD`).
        end_date: Requested end date (`YYYY-MM-DD`).
        start_date_service_levels: Service levels for the first weekday, Saturday and Sunday in the range.
        end_date_service_levels: Service levels for the last weekday, Saturday and Sunday in the range.
        counts: Scheduled trip counts at the requested aggregation level.

        Attributes:
            start_date (str):
            end_date (str):
            start_date_service_levels (ServiceLevelsByDayKind): Service levels grouped by day type. A day type is `null`
                when the date range doesn't include one.

                Attributes:
                    weekday: Weekday service breakdown.
                    saturday: Saturday service breakdown.
                    sunday: Sunday service breakdown.
            end_date_service_levels (ServiceLevelsByDayKind): Service levels grouped by day type. A day type is `null` when
                the date range doesn't include one.

                Attributes:
                    weekday: Weekday service breakdown.
                    saturday: Saturday service breakdown.
                    sunday: Sunday service breakdown.
            counts (list[ScheduledServiceCount]):
    """

    start_date: str
    end_date: str
    start_date_service_levels: ServiceLevelsByDayKind
    end_date_service_levels: ServiceLevelsByDayKind
    counts: list[ScheduledServiceCount]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        start_date = self.start_date

        end_date = self.end_date

        start_date_service_levels = self.start_date_service_levels.to_dict()

        end_date_service_levels = self.end_date_service_levels.to_dict()

        counts = []
        for counts_item_data in self.counts:
            counts_item = counts_item_data.to_dict()
            counts.append(counts_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "start_date": start_date,
                "end_date": end_date,
                "start_date_service_levels": start_date_service_levels,
                "end_date_service_levels": end_date_service_levels,
                "counts": counts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.scheduled_service_count import ScheduledServiceCount  # noqa: PLC0415
        from ..models.service_levels_by_day_kind import ServiceLevelsByDayKind  # noqa: PLC0415

        d = dict(src_dict)
        start_date = d.pop("start_date")

        end_date = d.pop("end_date")

        start_date_service_levels = ServiceLevelsByDayKind.from_dict(
            d.pop("start_date_service_levels")
        )

        end_date_service_levels = ServiceLevelsByDayKind.from_dict(
            d.pop("end_date_service_levels")
        )

        counts = []
        _counts = d.pop("counts")
        for counts_item_data in _counts:
            counts_item = ScheduledServiceCount.from_dict(counts_item_data)

            counts.append(counts_item)

        get_scheduled_service_response = cls(
            start_date=start_date,
            end_date=end_date,
            start_date_service_levels=start_date_service_levels,
            end_date_service_levels=end_date_service_levels,
            counts=counts,
        )

        get_scheduled_service_response.additional_properties = d
        return get_scheduled_service_response

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
