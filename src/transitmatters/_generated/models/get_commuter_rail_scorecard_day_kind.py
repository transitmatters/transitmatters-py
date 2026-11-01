from enum import StrEnum


class GetCommuterRailScorecardDayKind(StrEnum):
    ALL = "all"
    SATURDAY = "saturday"
    SUNDAY = "sunday"
    WEEKDAY = "weekday"

    def __str__(self) -> str:
        return str(self.value)
