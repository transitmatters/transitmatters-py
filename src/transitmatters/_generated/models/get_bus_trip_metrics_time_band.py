from enum import StrEnum


class GetBusTripMetricsTimeBand(StrEnum):
    AM_PEAK = "am_peak"
    EARLY_AM = "early_am"
    EVENING = "evening"
    LATE_NIGHT = "late_night"
    MIDDAY = "midday"
    PM_PEAK = "pm_peak"

    def __str__(self) -> str:
        return str(self.value)
