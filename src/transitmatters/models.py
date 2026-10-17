"""Data models returned by the client, e.g. `Headway` or `RouteStops`.

Every model is a frozen dataclass. Times are timezone-aware `datetime`s in
Eastern time (`America/New_York`), dates are `datetime.date`s, and missing
values are `None`.

`transitmatters.to_dataframe` turns a list of models into a pandas
DataFrame; `Model.to_dict` gives one model as a dict.
"""

from __future__ import annotations

import dataclasses
import datetime
from dataclasses import dataclass
from typing import Any

__docformat__ = "google"

# Ordered for the API docs, which list members in this order.
__all__ = [  # noqa: RUF022
    "Model",
    # Events
    "Headway",
    "Dwell",
    "TravelTime",
    "Alert",
    "LiveAlert",
    "ActivePeriod",
    # Statistics
    "SummaryStats",
    "DailyStats",
    "DailyHeadwayStats",
    "TimeOfDayStats",
    "TravelTimeStats",
    # Line metrics
    "TripMetrics",
    "LineDelays",
    "ServiceHours",
    "Ridership",
    "ScheduledService",
    "ScheduledServiceCount",
    "ServiceLevels",
    "DayServiceLevels",
    "TimePredictionWeek",
    "TimePredictionBucket",
    "SpeedRestrictions",
    "SpeedRestriction",
    # Reference data
    "Routes",
    "RouteStops",
    "Station",
    "Facility",
    "FacilityProperty",
    "Healthcheck",
    # Overview dashboard
    "ServiceRidershipDashboard",
    "DashboardSummary",
    "DashboardLine",
    "ServiceRegimes",
    "ServiceRegime",
    "ServiceDay",
]


@dataclass(frozen=True, slots=True)
class Model:
    """Base class for every model."""

    def to_dict(self) -> dict[str, Any]:
        """The fields as a dict, with nested models as dicts too."""
        return dataclasses.asdict(self)


# Events


@dataclass(frozen=True, slots=True, kw_only=True)
class Headway(Model):
    """The time between two consecutive departures from a stop."""

    route_id: str
    """Route of the departing trip, e.g. `"Red"`, `"28"`, `"CR-Fairmount"`."""
    direction: int
    """Direction ID, `0` or `1`. `TransitMatters.stops` names them."""
    current_dep_dt: datetime.datetime
    """Departure time."""
    headway_time_sec: float
    """Seconds since the previous departure."""
    benchmark_headway_time_sec: float | None
    """Scheduled headway in seconds, if known."""
    vehicle_label: str
    """Vehicle label; may be empty."""
    vehicle_consist: tuple[str, ...]
    """Car numbers, e.g. `("1850", "1851")`; empty when unknown."""


@dataclass(frozen=True, slots=True, kw_only=True)
class Dwell(Model):
    """The time a vehicle spent stopped at a stop."""

    route_id: str
    """Route of the trip, e.g. `"Red"`, `"1"`, `"CR-Fairmount"`."""
    direction: int
    """Direction ID, `0` or `1`."""
    arr_dt: datetime.datetime
    """Arrival time."""
    dep_dt: datetime.datetime
    """Departure time."""
    dwell_time_sec: float
    """Seconds between arrival and departure."""
    vehicle_label: str
    """Vehicle label; may be empty."""
    vehicle_consist: tuple[str, ...]
    """Car numbers; empty when unknown."""


@dataclass(frozen=True, slots=True, kw_only=True)
class TravelTime(Model):
    """One trip's travel time between an origin and a destination stop."""

    route_id: str
    """Route of the trip, e.g. `"Red"`, `"28"`, `"CR-Fairmount"`."""
    direction: int
    """Direction ID, `0` or `1`."""
    dep_dt: datetime.datetime
    """Departure time from the origin."""
    arr_dt: datetime.datetime
    """Arrival time at the destination."""
    travel_time_sec: float
    """Travel time in seconds."""
    benchmark_travel_time_sec: float | None
    """Scheduled travel time in seconds, if known."""
    tm_benchmark_travel_time_sec: float | None
    """TransitMatters' benchmark travel time in seconds for the stop pair
    (the same on every trip), or `None` for bus, commuter rail, and ferry."""
    vehicle_label: str
    """Vehicle label; may be empty."""
    vehicle_consist: tuple[str, ...]
    """Car numbers; empty when unknown."""


@dataclass(frozen=True, slots=True, kw_only=True)
class Alert(Model):
    """An archived service alert."""

    valid_from: datetime.datetime
    """Start time."""
    valid_to: datetime.datetime | None
    """End time, or `None` for an open-ended alert."""
    text: str | None
    """Alert header text."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ActivePeriod(Model):
    """A period during which a live alert is active."""

    start: datetime.datetime | None
    """Start time."""
    end: datetime.datetime | None
    """End time, or `None` if open-ended."""
    current: bool
    """Whether the period includes the current time."""
    upcoming: bool
    """Whether the period hasn't started yet, or is open-ended."""


@dataclass(frozen=True, slots=True, kw_only=True)
class LiveAlert(Model):
    """A current MBTA service alert.

    Which fields are set depends on `type`: `routes` for `DELAY` and
    `DETOUR`, and `description` for elevator and escalator closures.
    """

    id: str
    """MBTA alert ID."""
    type: str
    """Effect, e.g. `DELAY`, `DETOUR`, `SHUTTLE`, `SUSPENSION`,
    `STOP_CLOSURE`, `ELEVATOR_CLOSURE`, or `ESCALATOR_CLOSURE`."""
    header: str
    """Alert header text."""
    active_period: tuple[ActivePeriod, ...]
    """When the alert is active."""
    stops: tuple[str, ...]
    """Affected stop IDs, unordered: platform IDs like `"70061"` for
    `DELAY` and `DETOUR`, station IDs like `"place-dwnxg"` otherwise."""
    routes: tuple[str, ...]
    """Affected route IDs, possibly repeated; empty unless `DELAY` or `DETOUR`."""
    description: str | None
    """Long-form description, for elevator and escalator closures."""


# Statistics


@dataclass(frozen=True, slots=True, kw_only=True)
class SummaryStats(Model):
    """Summary statistics of a set of times, in seconds."""

    count: int
    """Number of events."""
    mean: float
    """Mean."""
    min: float
    """Minimum."""
    max: float
    """Maximum."""
    std: float
    """Population standard deviation."""
    sum: float
    """Sum."""
    p25: float
    """25th percentile."""
    p50: float
    """Median."""
    p75: float
    """75th percentile."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DailyStats(SummaryStats):
    """Statistics for one service date and peak period."""

    service_date: datetime.date
    """Service date. Service after midnight counts toward the day before."""
    peak: str
    """`"all"` for the whole day. `aggregate_travel_times_v2` also has
    `"am_peak"`, `"pm_peak"`, and `"off_peak"` entries."""
    holiday: bool
    """Whether the service date is a US federal holiday."""
    weekend: bool
    """Whether the service date is a Saturday or Sunday."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DailyHeadwayStats(DailyStats):
    """Headway statistics for one service date, with bunching and on-time counts."""

    bunched: int
    """Headways at most half the scheduled headway (0 without a schedule)."""
    on_time: int
    """Headways within 25% of the scheduled headway (0 without a schedule)."""


@dataclass(frozen=True, slots=True, kw_only=True)
class TimeOfDayStats(SummaryStats):
    """Statistics for one 30-minute departure-time slot across a date range."""

    dep_time: datetime.timedelta
    """Start of the slot, as time since the service day's midnight. Service
    after midnight is past 24 hours, so 00:30 is `timedelta(hours=24, minutes=30)`."""
    is_peak_day: bool
    """`True` for non-holiday weekdays, `False` for weekends and holidays."""


@dataclass(frozen=True, slots=True, kw_only=True)
class TravelTimeStats(Model):
    """Travel-time statistics by date and by time of day."""

    by_date: tuple[DailyStats, ...]
    """One entry per service date and peak period."""
    by_time: tuple[TimeOfDayStats, ...]
    """One entry per 30-minute departure-time slot."""


# Line metrics


@dataclass(frozen=True, slots=True, kw_only=True)
class TripMetrics(Model):
    """Delivered trips on a line for one day, week, or month."""

    date: datetime.date
    """Day, Monday of the week, or first day of the month."""
    line: str
    """Line ID, e.g. `"line-red"`."""
    count: float
    """Trips delivered; the median daily count for weekly and monthly data."""
    total_time: float
    """Total trip time in seconds."""
    miles_covered: float
    """Total miles covered."""
    avg_car_age: float | None
    """Average car age in years, if known."""
    pct_new_trips: float | None
    """Percentage of trips run with new cars, if known."""
    fleet_mix: dict[str, float]
    """Percentage of trips by fleet type, e.g. `{"red1": 25.5, "red4": 30.1}`;
    empty when unknown."""


@dataclass(frozen=True, slots=True, kw_only=True)
class LineDelays(Model):
    """Alert-reported delay on a line for one day or week, in minutes, by cause."""

    date: datetime.date
    """Day, or the Monday starting the week."""
    line: str
    """Line as requested, e.g. `"Red"`, `"Green-B"`, `"CR-Fairmount"`."""
    total_delay_time: int
    brake_problem: int
    car_traffic: int
    disabled_vehicle: int
    door_problem: int
    fire: int
    flooding: int
    mechanical_problem: int
    medical_emergency: int
    other: int
    police_activity: int
    power_problem: int
    signal_problem: int
    switch_problem: int
    track_issue: int
    track_work: int


@dataclass(frozen=True, slots=True, kw_only=True)
class ServiceHours(Model):
    """Scheduled and delivered service hours for one day, week, or month."""

    date: datetime.date
    """Day, Monday of the week, or last day of the month."""
    scheduled: float
    """Scheduled service hours."""
    delivered: float
    """Delivered service hours."""


@dataclass(frozen=True, slots=True, kw_only=True)
class Ridership(Model):
    """Ridership on a line for one week."""

    date: datetime.date
    """Week start date."""
    count: int
    """Ridership count."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ScheduledServiceCount(Model):
    """Scheduled trips for one day, week, or month."""

    date: datetime.date
    """Day, Monday of the week, or last day of the month."""
    count: float
    """Scheduled trips; the median daily count for weekly and monthly data."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DayServiceLevels(Model):
    """Scheduled trips by hour on one reference day."""

    date: datetime.date
    """Reference date."""
    service_levels: tuple[int, ...]
    """Scheduled trips by hour, index 0 = midnight; empty if unavailable."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ServiceLevels(Model):
    """Scheduled service on a weekday, Saturday, and Sunday."""

    weekday: DayServiceLevels | None
    """`None` when the date range has no weekday."""
    saturday: DayServiceLevels | None
    """`None` when the date range has no Saturday."""
    sunday: DayServiceLevels | None
    """`None` when the date range has no Sunday."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ScheduledService(Model):
    """Scheduled trips on a route over a date range."""

    start_date: datetime.date
    """Requested start date."""
    end_date: datetime.date
    """Requested end date."""
    start_date_service_levels: ServiceLevels
    """Service on the first weekday, Saturday, and Sunday in the range."""
    end_date_service_levels: ServiceLevels
    """Service on the last weekday, Saturday, and Sunday in the range."""
    counts: tuple[ScheduledServiceCount, ...]
    """Scheduled trips at the requested aggregation level."""


@dataclass(frozen=True, slots=True, kw_only=True)
class TimePredictionBucket(Model):
    """Prediction accuracy for one week and prediction horizon."""

    weekly: datetime.date
    """Week start date."""
    mode: str
    """Mode, e.g. `"subway"` or `"bus"`."""
    route_id: str
    """Route ID."""
    bin: str
    """Prediction horizon: `"0-3 min"`, `"3-6 min"`, `"6-12 min"`, or `"12-30 min"`."""
    arrival_departure: str
    """Prediction type, e.g. `"blended"`."""
    num_predictions: int
    """Number of predictions."""
    num_accurate_predictions: int
    """Number of accurate predictions."""


@dataclass(frozen=True, slots=True, kw_only=True)
class TimePredictionWeek(Model):
    """Prediction accuracy for a route over one week."""

    route_id: str
    """Route ID."""
    week: datetime.date
    """Week start date."""
    prediction: tuple[TimePredictionBucket, ...]
    """Accuracy per prediction horizon."""


@dataclass(frozen=True, slots=True, kw_only=True)
class SpeedRestriction(Model):
    """A speed restriction in effect on a line."""

    id: str
    """Restriction ID."""
    date: datetime.date
    """Date of the data."""
    line_id: str
    """Line ID, e.g. `"line-Red"`."""
    description: str
    """Location description."""
    direction: str
    """Track direction, e.g. `"NB"` or `"SB"`."""
    reason: str
    """Reason for the restriction."""
    from_stop_id: str | None
    """Station ID where the restriction starts, e.g. `"place-cntsq"`."""
    to_stop_id: str | None
    """Station ID where it ends, or `None` for a single location."""
    reported: datetime.date
    """Date the restriction was reported."""
    speed_mph: int
    """Speed limit in miles per hour."""
    track_feet: int
    """Length of restricted track in feet."""


@dataclass(frozen=True, slots=True, kw_only=True)
class SpeedRestrictions(Model):
    """Speed restrictions on a line on one date."""

    available: bool
    """Whether there is speed restriction data for the date."""
    date: datetime.date | None
    """Date of the data, which may be earlier than the requested date."""
    zones: tuple[SpeedRestriction, ...]
    """Restrictions in effect; empty when unavailable."""


# Reference data


@dataclass(frozen=True, slots=True, kw_only=True)
class Routes(Model):
    """Every route ID the dashboard supports, by mode."""

    rapid_transit: tuple[str, ...]
    """E.g. `"Red"`, `"Green"`."""
    bus: tuple[str, ...]
    """E.g. `"1"`, `"104/109"`."""
    commuter_rail: tuple[str, ...]
    """E.g. `"CR-Fairmount"`."""
    ferry: tuple[str, ...]
    """E.g. `"Boat-F1"`."""


@dataclass(frozen=True, slots=True, kw_only=True)
class Station(Model):
    """A station or stop along a route."""

    stop_name: str
    """Display name, e.g. `"Davis"`."""
    station: str
    """Station ID, e.g. `"place-davis"`."""
    order: float
    """Position along the route, starting at 1. Usually a whole number."""
    stops: dict[int, tuple[str, ...]]
    """Platform stop IDs by direction ID."""
    branches: tuple[str, ...]
    """Branches serving the station, e.g. `("A", "B")`; empty if the route
    doesn't branch."""
    accessible: bool
    """Whether the station is ADA accessible."""
    pedal_park: bool
    """Whether the station has bike parking."""
    enclosed_bike_parking: bool
    """Whether the station has enclosed bike storage."""
    terminus: bool
    """Whether this is a terminal station."""
    disabled: bool
    """Whether this stop is currently disabled."""
    short: str | None
    """Short display name, if any."""


@dataclass(frozen=True, slots=True, kw_only=True)
class RouteStops(Model):
    """The stations along a route, with stop IDs by direction."""

    type: str
    """`"rapidtransit"`, `"bus"`, `"commuter-rail"`, or `"ferry"`."""
    directions: dict[int, str]
    """Direction names by direction ID, e.g. `{0: "northbound", 1: "southbound"}`."""
    stations: tuple[Station, ...]
    """Stations in route order."""
    service_start: datetime.date | None
    """When the route started running, for routes that changed."""
    service_end: datetime.date | None
    """When the route stopped running, for routes that changed."""


@dataclass(frozen=True, slots=True, kw_only=True)
class FacilityProperty(Model):
    """A name/value property of a facility."""

    name: str
    """Property name, e.g. `"capacity"` or `"excludes-stop"`."""
    value: str | None
    """Property value. Numbers are strings, e.g. `"20"`."""


@dataclass(frozen=True, slots=True, kw_only=True)
class Facility(Model):
    """An MBTA facility, such as an elevator, escalator, or bike rack."""

    id: str
    """Facility ID."""
    type: str
    """E.g. `"ELEVATOR"`, `"ESCALATOR"`, `"BIKE_STORAGE"`, `"PARKING_AREA"`."""
    long_name: str | None
    """Full display name."""
    short_name: str | None
    """Short display name."""
    latitude: float | None
    longitude: float | None
    stop_id: str | None
    """Station the facility belongs to, e.g. `"place-andrw"`."""
    properties: tuple[FacilityProperty, ...]
    """Other properties. A name can appear more than once."""


@dataclass(frozen=True, slots=True, kw_only=True)
class Healthcheck(Model):
    """The result of the API's health checks."""

    status: str
    """`"pass"` or `"fail"`."""
    failed_checks: dict[str, str]
    """Failure detail by check name; empty when all pass."""

    @property
    def ok(self) -> bool:
        """Whether every check passed."""
        return self.status == "pass"


# Overview dashboard


@dataclass(frozen=True, slots=True, kw_only=True)
class ServiceDay(Model):
    """Scheduled service on one kind of day."""

    cancelled: bool
    """Whether service is cancelled."""
    total_trips: int
    """Total scheduled trips."""
    trips_per_hour: tuple[float, ...]
    """Scheduled trips by hour, index 0 = midnight; empty when cancelled."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ServiceRegime(Model):
    """Scheduled service on a weekday, Saturday, and Sunday."""

    weekday: ServiceDay
    saturday: ServiceDay
    sunday: ServiceDay


@dataclass(frozen=True, slots=True, kw_only=True)
class ServiceRegimes(Model):
    """A line's scheduled service at three points in time."""

    current: ServiceRegime
    """Current service."""
    one_year_ago: ServiceRegime
    """Service one year ago."""
    baseline: ServiceRegime
    """Pre-COVID baseline service."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DashboardLine(Model):
    """Service and ridership for one line."""

    id: str
    """Line ID, e.g. `"line-Red"`, `"line-1"`, `"line-Fairmount"`."""
    short_name: str
    """Short name; may be empty."""
    long_name: str
    """Long name, e.g. `"Red Line"`."""
    route_ids: tuple[str, ...]
    """Route IDs on the line."""
    start_date: datetime.date
    """First date covered."""
    line_kind: str
    """`"red"`, `"orange"`, `"blue"`, `"green"`, `"silver"`,
    `"regional-rail"`, `"bus"`, or `"boat"`."""
    ridership_history: dict[datetime.date, float]
    """Weekly median ridership by week start date; empty if unavailable."""
    service_history: dict[datetime.date, float]
    """Weekly median scheduled trips by week start date."""
    service_regimes: ServiceRegimes
    """Scheduled service now, a year ago, and before COVID."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DashboardSummary(Model):
    """Service and ridership across the system or one mode."""

    total_ridership_history: dict[datetime.date, float]
    """Weekly median ridership by week start date."""
    total_service_history: dict[datetime.date, float]
    """Weekly median scheduled trips by week start date."""
    total_ridership_percentage: float
    """Currently always 0."""
    total_service_percentage: float
    """Currently always 0."""
    total_passengers: float
    """Weekly median ridership in the latest week."""
    total_trips: float
    """Weekly median scheduled trips in the latest week."""
    total_routes_cancelled: int
    """Routes with cancelled service."""
    total_reduced_service: int
    """Routes with reduced service."""
    total_increased_service: int
    """Routes with increased service."""
    start_date: datetime.date
    """First date covered."""
    end_date: datetime.date
    """Last date covered."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ServiceRidershipDashboard(Model):
    """The data behind the dashboard's service and ridership overview."""

    summary_data: DashboardSummary
    """System-wide summary."""
    mode_data: dict[str, DashboardSummary]
    """Summaries by mode: `"rapid-transit"`, `"regional-rail"`, `"bus"`, `"boat"`."""
    line_data: dict[str, DashboardLine]
    """Lines by line ID, e.g. `"line-Red"`."""
