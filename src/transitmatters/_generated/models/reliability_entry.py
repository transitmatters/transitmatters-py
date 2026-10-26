from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.reliability_counts import ReliabilityCounts


T = TypeVar("T", bound="ReliabilityEntry")


@_attrs_define
class ReliabilityEntry:
    """Summed on-time performance counts for one day, week, or month.

    The RIDE entries have `completed` and `onTime`, plus `requests`, `noShows` and `missed` for periods
    where every day recorded them. Commuter rail entries have `otpNumerator`, `otpDenominator`,
    `cancelled`, `peak` and `offPeak`.

    Attributes:
        date: Day, Monday of the week, or first day of the month (`YYYY-MM-DD`).
        days: Service days with data in the period.
        completed: The RIDE completed trips.
        onTime: The RIDE trips completed on time.
        requests: The RIDE trip requests.
        noShows: The RIDE rider no-shows.
        missed: The RIDE missed trips.
        otpNumerator: Commuter rail trips that ran on time.
        otpDenominator: Commuter rail trips measured.
        cancelled: Commuter rail cancelled trips.
        peak: Commuter rail peak-period counts.
        offPeak: Commuter rail off-peak counts.

    """

    date: str
    days: int
    completed: int | None | Unset = UNSET
    on_time: int | None | Unset = UNSET
    requests: int | None | Unset = UNSET
    no_shows: int | None | Unset = UNSET
    missed: int | None | Unset = UNSET
    otp_numerator: int | None | Unset = UNSET
    otp_denominator: int | None | Unset = UNSET
    cancelled: int | None | Unset = UNSET
    peak: None | ReliabilityCounts | Unset = UNSET
    """ On-time and cancellation counts for one commuter rail time period.

    Attributes:
        otpNumerator: Trips that ran on time.
        otpDenominator: Trips measured for on-time performance.
        cancelled: Cancelled trips. """
    off_peak: None | ReliabilityCounts | Unset = UNSET
    """ On-time and cancellation counts for one commuter rail time period.

    Attributes:
        otpNumerator: Trips that ran on time.
        otpDenominator: Trips measured for on-time performance.
        cancelled: Cancelled trips. """
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.reliability_counts import ReliabilityCounts  # noqa: PLC0415

        date = self.date

        days = self.days

        completed: int | None | Unset
        if isinstance(self.completed, Unset):
            completed = UNSET
        else:
            completed = self.completed

        on_time: int | None | Unset
        if isinstance(self.on_time, Unset):
            on_time = UNSET
        else:
            on_time = self.on_time

        requests: int | None | Unset
        if isinstance(self.requests, Unset):
            requests = UNSET
        else:
            requests = self.requests

        no_shows: int | None | Unset
        if isinstance(self.no_shows, Unset):
            no_shows = UNSET
        else:
            no_shows = self.no_shows

        missed: int | None | Unset
        if isinstance(self.missed, Unset):
            missed = UNSET
        else:
            missed = self.missed

        otp_numerator: int | None | Unset
        if isinstance(self.otp_numerator, Unset):
            otp_numerator = UNSET
        else:
            otp_numerator = self.otp_numerator

        otp_denominator: int | None | Unset
        if isinstance(self.otp_denominator, Unset):
            otp_denominator = UNSET
        else:
            otp_denominator = self.otp_denominator

        cancelled: int | None | Unset
        if isinstance(self.cancelled, Unset):
            cancelled = UNSET
        else:
            cancelled = self.cancelled

        peak: dict[str, Any] | None | Unset
        if isinstance(self.peak, Unset):
            peak = UNSET
        elif isinstance(self.peak, ReliabilityCounts):
            peak = self.peak.to_dict()
        else:
            peak = self.peak

        off_peak: dict[str, Any] | None | Unset
        if isinstance(self.off_peak, Unset):
            off_peak = UNSET
        elif isinstance(self.off_peak, ReliabilityCounts):
            off_peak = self.off_peak.to_dict()
        else:
            off_peak = self.off_peak

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "date": date,
                "days": days,
            }
        )
        if completed is not UNSET:
            field_dict["completed"] = completed
        if on_time is not UNSET:
            field_dict["onTime"] = on_time
        if requests is not UNSET:
            field_dict["requests"] = requests
        if no_shows is not UNSET:
            field_dict["noShows"] = no_shows
        if missed is not UNSET:
            field_dict["missed"] = missed
        if otp_numerator is not UNSET:
            field_dict["otpNumerator"] = otp_numerator
        if otp_denominator is not UNSET:
            field_dict["otpDenominator"] = otp_denominator
        if cancelled is not UNSET:
            field_dict["cancelled"] = cancelled
        if peak is not UNSET:
            field_dict["peak"] = peak
        if off_peak is not UNSET:
            field_dict["offPeak"] = off_peak

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.reliability_counts import ReliabilityCounts  # noqa: PLC0415

        d = dict(src_dict)
        date = d.pop("date")

        days = d.pop("days")

        def _parse_completed(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        completed = _parse_completed(d.pop("completed", UNSET))

        def _parse_on_time(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        on_time = _parse_on_time(d.pop("onTime", UNSET))

        def _parse_requests(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        requests = _parse_requests(d.pop("requests", UNSET))

        def _parse_no_shows(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        no_shows = _parse_no_shows(d.pop("noShows", UNSET))

        def _parse_missed(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        missed = _parse_missed(d.pop("missed", UNSET))

        def _parse_otp_numerator(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        otp_numerator = _parse_otp_numerator(d.pop("otpNumerator", UNSET))

        def _parse_otp_denominator(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        otp_denominator = _parse_otp_denominator(d.pop("otpDenominator", UNSET))

        def _parse_cancelled(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        cancelled = _parse_cancelled(d.pop("cancelled", UNSET))

        def _parse_peak(data: object) -> None | ReliabilityCounts | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_reliability_counts_type_0 = (
                    ReliabilityCounts.from_dict(data)
                )

                return componentsschemas_reliability_counts_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ReliabilityCounts | Unset, data)

        peak = _parse_peak(d.pop("peak", UNSET))

        def _parse_off_peak(data: object) -> None | ReliabilityCounts | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_reliability_counts_type_0 = (
                    ReliabilityCounts.from_dict(data)
                )

                return componentsschemas_reliability_counts_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ReliabilityCounts | Unset, data)

        off_peak = _parse_off_peak(d.pop("offPeak", UNSET))

        reliability_entry = cls(
            date=date,
            days=days,
            completed=completed,
            on_time=on_time,
            requests=requests,
            no_shows=no_shows,
            missed=missed,
            otp_numerator=otp_numerator,
            otp_denominator=otp_denominator,
            cancelled=cancelled,
            peak=peak,
            off_peak=off_peak,
        )

        reliability_entry.additional_properties = d
        return reliability_entry

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
