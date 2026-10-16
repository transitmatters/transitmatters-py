from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


from ..models.scheduled_service_params_agg import ScheduledServiceParamsAgg
import datetime


T = TypeVar("T", bound="ScheduledServiceParams")


@_attrs_define
class ScheduledServiceParams:
    """Parameters for the `/api/scheduledservice` endpoint.

    Attributes:
        start_date: Start of date range.
        end_date: End of date range.
        route_id: Route identifier (e.g., `Red`, `1`, `CR-Fairmount`).
        agg: Aggregation level — `daily`, `weekly`, or `monthly`.

        Attributes:
            start_date (datetime.date): Start of the date range, inclusive (YYYY-MM-DD).
            end_date (datetime.date): End of the date range, inclusive (YYYY-MM-DD).
            route_id (str): MBTA route ID. Rapid transit: `Red`, `Orange`, `Blue`, `Green-B`-`Green-E`, `Mattapan`. Bus:
                numeric string (e.g. `1`, `66`). Commuter rail: `CR-{line}` (e.g. `CR-Fairmount`). Ferry: `Boat-F1`, `Boat-F4`,
                etc. Use `/api/routes` to list all valid route IDs.
            agg (ScheduledServiceParamsAgg): Aggregation period: `daily`, `weekly`, or `monthly`.
    """

    start_date: datetime.date
    end_date: datetime.date
    route_id: str
    agg: ScheduledServiceParamsAgg
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        start_date = self.start_date.isoformat()

        end_date = self.end_date.isoformat()

        route_id = self.route_id

        agg = self.agg.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "start_date": start_date,
                "end_date": end_date,
                "route_id": route_id,
                "agg": agg,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        start_date = datetime.date.fromisoformat(d.pop("start_date"))

        end_date = datetime.date.fromisoformat(d.pop("end_date"))

        route_id = d.pop("route_id")

        agg = ScheduledServiceParamsAgg(d.pop("agg"))

        scheduled_service_params = cls(
            start_date=start_date,
            end_date=end_date,
            route_id=route_id,
            agg=agg,
        )

        scheduled_service_params.additional_properties = d
        return scheduled_service_params

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
