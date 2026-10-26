from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


from ..models.reliability_params_agg import ReliabilityParamsAgg
import datetime


T = TypeVar("T", bound="ReliabilityParams")


@_attrs_define
class ReliabilityParams:
    """Parameters for the `/api/reliability` endpoint.

    Attributes:
        route_id: `RIDE`, a commuter rail route, or `commuter-rail` for all of commuter rail.
        start_date: Start of date range.
        end_date: End of date range.
        agg: Aggregation level — `daily`, `weekly`, or `monthly`.

    """

    route_id: str
    """ `RIDE` for The RIDE, a commuter rail route ID (e.g. `CR-Worcester`), or `commuter-rail` for every commuter
    rail route combined. """
    start_date: datetime.date
    """ Start of the date range, inclusive (YYYY-MM-DD). """
    end_date: datetime.date
    """ End of the date range, inclusive (YYYY-MM-DD). """
    agg: ReliabilityParamsAgg
    """ Aggregation period: `daily`, `weekly`, or `monthly`. """
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        route_id = self.route_id

        start_date = self.start_date.isoformat()

        end_date = self.end_date.isoformat()

        agg = self.agg.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "route_id": route_id,
                "start_date": start_date,
                "end_date": end_date,
                "agg": agg,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        route_id = d.pop("route_id")

        start_date = datetime.date.fromisoformat(d.pop("start_date"))

        end_date = datetime.date.fromisoformat(d.pop("end_date"))

        agg = ReliabilityParamsAgg(d.pop("agg"))

        reliability_params = cls(
            route_id=route_id,
            start_date=start_date,
            end_date=end_date,
            agg=agg,
        )

        reliability_params.additional_properties = d
        return reliability_params

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
