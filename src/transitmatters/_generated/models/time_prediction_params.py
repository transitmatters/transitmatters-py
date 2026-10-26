from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
import datetime


T = TypeVar("T", bound="TimePredictionParams")


@_attrs_define
class TimePredictionParams:
    """Parameters for the `/api/time_predictions` endpoint.

    Attributes:
        route_id: Route identifier (e.g., `Red`, `CR-Fairmount`).
        start_date: Optional start of the range of weeks to return.
        end_date: Optional end of the range of weeks to return.

    """

    route_id: str
    """ MBTA route ID. Rapid transit: `Red`, `Orange`, `Blue`, `Green-B`-`Green-E`, `Mattapan`. Bus: numeric string
    (e.g. `1`, `66`). Commuter rail: `CR-{line}` (e.g. `CR-Fairmount`). Ferry: `Boat-F1`, `Boat-F4`, etc. Use
    `/api/routes` to list all valid route IDs. """
    start_date: datetime.date | None | Unset = UNSET
    """ Keep only weeks starting on or after this date (YYYY-MM-DD). Omit it for the full history. """
    end_date: datetime.date | None | Unset = UNSET
    """ Keep only weeks starting on or before this date (YYYY-MM-DD). Omit it for the full history. """
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        route_id = self.route_id

        start_date: None | str | Unset
        if isinstance(self.start_date, Unset):
            start_date = UNSET
        elif isinstance(self.start_date, datetime.date):
            start_date = self.start_date.isoformat()
        else:
            start_date = self.start_date

        end_date: None | str | Unset
        if isinstance(self.end_date, Unset):
            end_date = UNSET
        elif isinstance(self.end_date, datetime.date):
            end_date = self.end_date.isoformat()
        else:
            end_date = self.end_date

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "route_id": route_id,
            }
        )
        if start_date is not UNSET:
            field_dict["start_date"] = start_date
        if end_date is not UNSET:
            field_dict["end_date"] = end_date

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        route_id = d.pop("route_id")

        def _parse_start_date(data: object) -> datetime.date | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                start_date_type_0 = datetime.date.fromisoformat(data)

                return start_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.date | None | Unset, data)

        start_date = _parse_start_date(d.pop("start_date", UNSET))

        def _parse_end_date(data: object) -> datetime.date | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                end_date_type_0 = datetime.date.fromisoformat(data)

                return end_date_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.date | None | Unset, data)

        end_date = _parse_end_date(d.pop("end_date", UNSET))

        time_prediction_params = cls(
            route_id=route_id,
            start_date=start_date,
            end_date=end_date,
        )

        time_prediction_params.additional_properties = d
        return time_prediction_params

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
