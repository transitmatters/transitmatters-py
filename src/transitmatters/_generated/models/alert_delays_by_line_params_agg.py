from enum import StrEnum


class AlertDelaysByLineParamsAgg(StrEnum):
    DAILY = "daily"
    WEEKLY = "weekly"

    def __str__(self) -> str:
        return str(self.value)
