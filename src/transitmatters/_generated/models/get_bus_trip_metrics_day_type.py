from enum import StrEnum


class GetBusTripMetricsDayType(StrEnum):
    BUSINESS_DAY = "business_day"
    WEEKEND_OR_HOLIDAY = "weekend_or_holiday"

    def __str__(self) -> str:
        return str(self.value)
