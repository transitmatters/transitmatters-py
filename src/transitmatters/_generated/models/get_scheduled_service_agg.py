from enum import StrEnum


class GetScheduledServiceAgg(StrEnum):
    DAILY = "daily"
    MONTHLY = "monthly"
    WEEKLY = "weekly"

    def __str__(self) -> str:
        return str(self.value)
