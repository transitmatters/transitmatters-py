from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.aggregate_by_date import AggregateByDate
    from ..models.aggregate_by_time import AggregateByTime


T = TypeVar("T", bound="TravelTimeAggregate2Response")


@_attrs_define
class TravelTimeAggregate2Response:
    """Response for `/api/aggregate/traveltimes2`: travel time statistics by date and by time of day.

    Attributes:
        by_date: Per-date statistics: an `all` row for each date, then a row per peak period.
        by_time: Statistics per 30-minute departure-time bucket, separately for peak and non-peak days.

        Attributes:
            by_date (list[AggregateByDate]):
            by_time (list[AggregateByTime]):
    """

    by_date: list[AggregateByDate]
    by_time: list[AggregateByTime]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        by_date = []
        for by_date_item_data in self.by_date:
            by_date_item = by_date_item_data.to_dict()
            by_date.append(by_date_item)

        by_time = []
        for by_time_item_data in self.by_time:
            by_time_item = by_time_item_data.to_dict()
            by_time.append(by_time_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "by_date": by_date,
                "by_time": by_time,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.aggregate_by_date import AggregateByDate  # noqa: PLC0415
        from ..models.aggregate_by_time import AggregateByTime  # noqa: PLC0415

        d = dict(src_dict)
        by_date = []
        _by_date = d.pop("by_date")
        for by_date_item_data in _by_date:
            by_date_item = AggregateByDate.from_dict(by_date_item_data)

            by_date.append(by_date_item)

        by_time = []
        _by_time = d.pop("by_time")
        for by_time_item_data in _by_time:
            by_time_item = AggregateByTime.from_dict(by_time_item_data)

            by_time.append(by_time_item)

        travel_time_aggregate_2_response = cls(
            by_date=by_date,
            by_time=by_time,
        )

        travel_time_aggregate_2_response.additional_properties = d
        return travel_time_aggregate_2_response

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
