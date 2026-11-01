from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


from ..models.cr_scorecard_params_agg import CrScorecardParamsAgg
from ..models.cr_scorecard_params_day_kind import CrScorecardParamsDayKind
import datetime


T = TypeVar("T", bound="CrScorecardParams")


@_attrs_define
class CrScorecardParams:
    """Parameters for the `/api/crscorecard` endpoint.

    Attributes:
        route_id: A Commuter Rail route, or `commuter-rail` to compare every route.
        start_date: Start of date range.
        end_date: End of date range.
        agg: Aggregation level — `daily`, `weekly`, or `monthly`. Ignored for `commuter-rail`.
        day_kind: Which schedule to measure, or `all` for every day.

    """

    route_id: str
    """ Commuter Rail route ID (e.g. `CR-Worcester`), or `commuter-rail` for one summary per route over the whole
    range. """
    start_date: datetime.date
    """ Start of the date range, inclusive (YYYY-MM-DD). """
    end_date: datetime.date
    """ End of the date range, inclusive (YYYY-MM-DD). """
    agg: CrScorecardParamsAgg
    """ Aggregation period: `daily`, `weekly`, or `monthly`. Ignored for `commuter-rail`. """
    day_kind: CrScorecardParamsDayKind
    """ Which schedule to measure: `weekday`, `saturday` or `sunday`, or `all` to mix every day. """
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        route_id = self.route_id

        start_date = self.start_date.isoformat()

        end_date = self.end_date.isoformat()

        agg = self.agg.value

        day_kind = self.day_kind.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "route_id": route_id,
                "start_date": start_date,
                "end_date": end_date,
                "agg": agg,
                "day_kind": day_kind,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        route_id = d.pop("route_id")

        start_date = datetime.date.fromisoformat(d.pop("start_date"))

        end_date = datetime.date.fromisoformat(d.pop("end_date"))

        agg = CrScorecardParamsAgg(d.pop("agg"))

        day_kind = CrScorecardParamsDayKind(d.pop("day_kind"))

        cr_scorecard_params = cls(
            route_id=route_id,
            start_date=start_date,
            end_date=end_date,
            agg=agg,
            day_kind=day_kind,
        )

        cr_scorecard_params.additional_properties = d
        return cr_scorecard_params

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
