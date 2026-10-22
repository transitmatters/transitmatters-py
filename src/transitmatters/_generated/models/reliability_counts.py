from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


T = TypeVar("T", bound="ReliabilityCounts")


@_attrs_define
class ReliabilityCounts:
    """On-time and cancellation counts for one commuter rail time period.

    Attributes:
        otpNumerator: Trips that ran on time.
        otpDenominator: Trips measured for on-time performance.
        cancelled: Cancelled trips.

    """

    otp_numerator: int
    otp_denominator: int
    cancelled: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        otp_numerator = self.otp_numerator

        otp_denominator = self.otp_denominator

        cancelled = self.cancelled

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "otpNumerator": otp_numerator,
                "otpDenominator": otp_denominator,
                "cancelled": cancelled,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        otp_numerator = d.pop("otpNumerator")

        otp_denominator = d.pop("otpDenominator")

        cancelled = d.pop("cancelled")

        reliability_counts = cls(
            otp_numerator=otp_numerator,
            otp_denominator=otp_denominator,
            cancelled=cancelled,
        )

        reliability_counts.additional_properties = d
        return reliability_counts

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
