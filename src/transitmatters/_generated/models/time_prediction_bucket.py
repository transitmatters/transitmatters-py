from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


T = TypeVar("T", bound="TimePredictionBucket")


@_attrs_define
class TimePredictionBucket:
    """Prediction accuracy for one week and prediction-horizon bin.

    Attributes:
        weekly: Week start date (`YYYY-MM-DD`).
        mode: Mode (e.g. `subway`, `bus`).
        route_id: Route ID.
        bin: Prediction horizon: `0-3 min`, `3-6 min`, `6-12 min` or `12-30 min`.
        arrival_departure: Prediction type (e.g. `blended`).
        num_predictions: Number of predictions.
        num_accurate_predictions: Number of accurate predictions.

    """

    weekly: str
    mode: str
    route_id: str
    bin_: str
    arrival_departure: str
    num_predictions: int
    num_accurate_predictions: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        weekly = self.weekly

        mode = self.mode

        route_id = self.route_id

        bin_ = self.bin_

        arrival_departure = self.arrival_departure

        num_predictions = self.num_predictions

        num_accurate_predictions = self.num_accurate_predictions

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "weekly": weekly,
                "mode": mode,
                "route_id": route_id,
                "bin": bin_,
                "arrival_departure": arrival_departure,
                "num_predictions": num_predictions,
                "num_accurate_predictions": num_accurate_predictions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        weekly = d.pop("weekly")

        mode = d.pop("mode")

        route_id = d.pop("route_id")

        bin_ = d.pop("bin")

        arrival_departure = d.pop("arrival_departure")

        num_predictions = d.pop("num_predictions")

        num_accurate_predictions = d.pop("num_accurate_predictions")

        time_prediction_bucket = cls(
            weekly=weekly,
            mode=mode,
            route_id=route_id,
            bin_=bin_,
            arrival_departure=arrival_departure,
            num_predictions=num_predictions,
            num_accurate_predictions=num_accurate_predictions,
        )

        time_prediction_bucket.additional_properties = d
        return time_prediction_bucket

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
