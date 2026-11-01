"""Split date ranges into the requests the API accepts."""

from __future__ import annotations

import datetime
from collections.abc import Callable, Hashable, Iterable

_DAY = datetime.timedelta(days=1)


def _check(start: datetime.date, end: datetime.date) -> None:
    if end < start:
        raise ValueError(f"end date {end} is before start date {start}")


def days(start: datetime.date, end: datetime.date) -> list[datetime.date]:
    """Every date from `start` through `end`."""
    _check(start, end)
    return [start + i * _DAY for i in range((end - start).days + 1)]


def week_start(day: datetime.date) -> datetime.date:
    """The Monday of `day`'s week."""
    return day - day.weekday() * _DAY


def month_start(day: datetime.date) -> datetime.date:
    """The first day of `day`'s month."""
    return day.replace(day=1)


def spans(
    start: datetime.date,
    end: datetime.date,
    max_days: int,
    period_start: Callable[[datetime.date], datetime.date] | None = None,
) -> list[tuple[datetime.date, datetime.date]]:
    """Contiguous inclusive ranges covering `start` through `end`, none
    longer than `max_days` days.

    With `period_start`, such as `week_start`, ranges only split where a
    period starts, so no period is divided between two of them.
    """
    _check(start, end)
    result = []
    while start <= end:
        stop = min(start + (max_days - 1) * _DAY, end)
        if period_start is not None and stop < end:
            boundary = period_start(stop + _DAY)
            if boundary > start:
                stop = boundary - _DAY
        result.append((start, stop))
        start = stop + _DAY
    return result


def unique[T](items: Iterable[T], key: Callable[[T], Hashable]) -> list[T]:
    """`items` without repeats by `key`, keeping the first of each."""
    seen: set[Hashable] = set()
    result = []
    for item in items:
        k = key(item)
        if k not in seen:
            seen.add(k)
            result.append(item)
    return result
