"""Data models returned by the client, e.g. `HeadwayEvent` or `StopsResponse`.

Every model has `to_dict()`, which returns the fields under the API's own
names (e.g. `min`, `25%`), ready for `pandas.DataFrame`.
"""

from ._generated import models as _models
from ._generated.models import *

__all__: list[str] = []
__all__ += _models.__all__
__docformat__ = "google"
