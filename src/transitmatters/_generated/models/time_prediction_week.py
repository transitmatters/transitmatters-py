from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.time_prediction_bucket import TimePredictionBucket


T = TypeVar("T", bound="TimePredictionWeek")


@_attrs_define
class TimePredictionWeek:
    """Prediction accuracy for a route over one week.

    Attributes:
        routeId: Route ID.
        week: Week start date (`YYYY-MM-DD`).
        prediction: Accuracy per prediction-horizon bin.

    """

    route_id: str
    week: str
    prediction: list[TimePredictionBucket]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        route_id = self.route_id

        week = self.week

        prediction = []
        for prediction_item_data in self.prediction:
            prediction_item = prediction_item_data.to_dict()
            prediction.append(prediction_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "routeId": route_id,
                "week": week,
                "prediction": prediction,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.time_prediction_bucket import TimePredictionBucket  # noqa: PLC0415

        d = dict(src_dict)
        route_id = d.pop("routeId")

        week = d.pop("week")

        prediction = []
        _prediction = d.pop("prediction")
        for prediction_item_data in _prediction:
            prediction_item = TimePredictionBucket.from_dict(prediction_item_data)

            prediction.append(prediction_item)

        time_prediction_week = cls(
            route_id=route_id,
            week=week,
            prediction=prediction,
        )

        time_prediction_week.additional_properties = d
        return time_prediction_week

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
