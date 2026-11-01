from enum import StrEnum


class BusTripMetricsParamsAgg(StrEnum):
    DAILY = "daily"
    MONTHLY = "monthly"
    WEEKLY = "weekly"

    def __str__(self) -> str:
        return str(self.value)
