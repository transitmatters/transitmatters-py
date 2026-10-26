from enum import StrEnum


class GetCommuterRailScorecardAgg(StrEnum):
    DAILY = "daily"
    MONTHLY = "monthly"
    WEEKLY = "weekly"

    def __str__(self) -> str:
        return str(self.value)
