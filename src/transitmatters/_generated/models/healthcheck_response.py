from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.healthcheck_response_failed_checks import (
        HealthcheckResponseFailedChecks,
    )


T = TypeVar("T", bound="HealthcheckResponse")


@_attrs_define
class HealthcheckResponse:
    """Response for `/api/healthcheck`.

    Attributes:
        status: `"pass"` or `"fail"`.
        failed_checks_sum: Number of failed checks, if any.
        failed_checks: Map of check name to failure detail.

    """

    status: str
    failed_checks_sum: int | None | Unset = UNSET
    failed_checks: HealthcheckResponseFailedChecks | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.healthcheck_response_failed_checks import (
            HealthcheckResponseFailedChecks,
        )  # noqa: PLC0415

        status = self.status

        failed_checks_sum: int | None | Unset
        if isinstance(self.failed_checks_sum, Unset):
            failed_checks_sum = UNSET
        else:
            failed_checks_sum = self.failed_checks_sum

        failed_checks: dict[str, Any] | None | Unset
        if isinstance(self.failed_checks, Unset):
            failed_checks = UNSET
        elif isinstance(self.failed_checks, HealthcheckResponseFailedChecks):
            failed_checks = self.failed_checks.to_dict()
        else:
            failed_checks = self.failed_checks

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
            }
        )
        if failed_checks_sum is not UNSET:
            field_dict["failed_checks_sum"] = failed_checks_sum
        if failed_checks is not UNSET:
            field_dict["failed_checks"] = failed_checks

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.healthcheck_response_failed_checks import (
            HealthcheckResponseFailedChecks,
        )  # noqa: PLC0415

        d = dict(src_dict)
        status = d.pop("status")

        def _parse_failed_checks_sum(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        failed_checks_sum = _parse_failed_checks_sum(d.pop("failed_checks_sum", UNSET))

        def _parse_failed_checks(
            data: object,
        ) -> HealthcheckResponseFailedChecks | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                failed_checks_type_0 = HealthcheckResponseFailedChecks.from_dict(data)

                return failed_checks_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(HealthcheckResponseFailedChecks | None | Unset, data)

        failed_checks = _parse_failed_checks(d.pop("failed_checks", UNSET))

        healthcheck_response = cls(
            status=status,
            failed_checks_sum=failed_checks_sum,
            failed_checks=failed_checks,
        )

        healthcheck_response.additional_properties = d
        return healthcheck_response

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
