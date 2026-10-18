"""Turn lists of models into pandas DataFrames."""

from __future__ import annotations

import dataclasses
import datetime
from collections.abc import Iterable
from typing import TYPE_CHECKING

from .models import Model

if TYPE_CHECKING:
    import pandas


def to_dataframe(items: Iterable[Model]) -> pandas.DataFrame:
    """A DataFrame with one row per model and one column per field.

    ```python
    from transitmatters import to_dataframe

    df = to_dataframe(tm.headways("2025-03-04", stop="70061"))
    df.set_index("current_dep_dt")["headway_time_sec"].plot()
    ```

    Times become timezone-aware `datetime64` columns in Eastern time, and
    dates become `datetime64` columns at midnight. Nested models, such as
    `transitmatters.models.TimePredictionWeek.prediction`, stay as objects;
    pass the nested list to `to_dataframe` instead. An empty list gives an
    empty DataFrame.

    Needs pandas: `pip install 'transitmatters[pandas]'`.

    Raises:
        TypeError: The items aren't all the same model.
    """
    try:
        import pandas
    except ImportError as e:
        raise ImportError(
            "to_dataframe needs pandas: pip install 'transitmatters[pandas]'"
        ) from e

    items = list(items)
    if not items:
        return pandas.DataFrame()
    model = type(items[0])
    if not all(type(item) is model for item in items):
        kinds = sorted({type(item).__name__ for item in items})
        raise TypeError(f"items must all be the same model, not {', '.join(kinds)}")

    columns = [field.name for field in dataclasses.fields(model)]
    df = pandas.DataFrame(
        [[getattr(item, column) for column in columns] for item in items],
        columns=columns,
    )
    for column in columns:
        values = df[column].dropna()
        # pandas infers datetime and timedelta columns, but leaves dates as objects.
        if len(values) and all(_is_date(value) for value in values):
            df[column] = pandas.to_datetime(df[column])
    return df


def _is_date(value: object) -> bool:
    return isinstance(value, datetime.date) and not isinstance(value, datetime.datetime)
