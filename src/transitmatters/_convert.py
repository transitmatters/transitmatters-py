"""Convert generated models into the public models in `transitmatters.models`.

Converters are typed against the generated classes, so a spec change that
renames or removes a field fails type checking here. A test checks that
every generated field is read here or listed in `IGNORED_FIELDS`, so a
spec change that adds one fails too.
"""

from __future__ import annotations

import datetime
from collections.abc import Callable, Iterable, Mapping
from typing import TypedDict
from zoneinfo import ZoneInfo

from . import models as m
from ._generated import models as g
from ._generated.types import Unset

EASTERN = ZoneInfo("America/New_York")

_EPOCH = datetime.datetime(1970, 1, 1)
_FLEET_MIX_PREFIX = "fleet_mix_"

IGNORED_FIELDS: dict[str, str] = {
    # Generated class and field -> why the public model leaves it out.
    "FacilitiesResponse.jsonapi": "JSON:API envelope",
    "FacilitiesResponse.links": "JSON:API envelope",
    "Facility.links": "JSON:API self link",
    "Facility.type_": "always 'facility'",
    "JsonApiResourceIdentifier.type_": "always 'stop'",
    "JsonApiVersion.version": "JSON:API envelope",
    "HealthcheckResponse.failed_checks_sum": "len(failed_checks)",
}


def each[S, T](convert: Callable[[S], T]) -> Callable[[Iterable[S]], list[T]]:
    """Lift a converter for one item to a converter for a list of them."""
    return lambda items: [convert(item) for item in items]


def _opt[T](value: T | None | Unset) -> T | None:
    return None if isinstance(value, Unset) else value


def _dt(value: str) -> datetime.datetime:
    # The API sends Eastern wall-clock times without an offset, except newer
    # alerts, which have one.
    parsed = datetime.datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=EASTERN)
    return parsed.astimezone(EASTERN)


def _opt_dt(value: str | None | Unset) -> datetime.datetime | None:
    value = _opt(value)
    return None if value is None else _dt(value)


def _date(value: str) -> datetime.date:
    return datetime.date.fromisoformat(value)


def _opt_date(value: str | None | Unset) -> datetime.date | None:
    value = _opt(value)
    return None if value is None else _date(value)


def _opt_float(value: str | None | Unset) -> float | None:
    value = _opt(value)
    return None if value is None else float(value)


def _consist(value: str | None | Unset) -> tuple[str, ...]:
    value = _opt(value)
    return tuple(value.split("|")) if value else ()


def _by_date(history: Mapping[str, float] | None) -> dict[datetime.date, float]:
    return {_date(day): value for day, value in (history or {}).items()}


def _history(
    value: g.DashboardSummaryTotalridershiphistory
    | g.DashboardSummaryTotalservicehistory
    | g.DashboardLineRidershiphistory
    | g.DashboardLineServicehistory
    | None
    | Unset,
) -> dict[datetime.date, float]:
    value = _opt(value)
    return _by_date(None if value is None else value.additional_properties)


class _Stats(TypedDict):
    count: int
    mean: float
    min: float
    max: float
    std: float
    sum: float
    p25: float
    p50: float
    p75: float


def _stats(
    s: g.AggregateByDate | g.AggregateByTime | g.HeadwayAggregateByDate,
) -> _Stats:
    return {
        "count": s.count,
        "mean": s.mean,
        "min": s.min_,
        "max": s.max_,
        "std": s.std,
        "sum": s.sum_,
        "p25": s.field_25,
        "p50": s.field_50,
        "p75": s.field_75,
    }


# Events


def headway(e: g.HeadwayEvent) -> m.Headway:
    return m.Headway(
        route_id=e.route_id,
        direction=int(e.direction),
        current_dep_dt=_dt(e.current_dep_dt),
        headway_time_sec=e.headway_time_sec,
        benchmark_headway_time_sec=_opt(e.benchmark_headway_time_sec),
        vehicle_label=e.vehicle_label,
        vehicle_consist=_consist(e.vehicle_consist),
    )


def dwell(e: g.DwellEvent) -> m.Dwell:
    return m.Dwell(
        route_id=e.route_id,
        direction=int(e.direction),
        arr_dt=_dt(e.arr_dt),
        dep_dt=_dt(e.dep_dt),
        dwell_time_sec=e.dwell_time_sec,
        vehicle_label=e.vehicle_label,
        vehicle_consist=_consist(e.vehicle_consist),
    )


def travel_time(e: g.TravelTimeEvent) -> m.TravelTime:
    return m.TravelTime(
        route_id=e.route_id,
        direction=int(e.direction),
        dep_dt=_dt(e.dep_dt),
        arr_dt=_dt(e.arr_dt),
        travel_time_sec=e.travel_time_sec,
        benchmark_travel_time_sec=_opt(e.benchmark_travel_time_sec),
        tm_benchmark_travel_time_sec=_opt(e.tm_benchmark_travel_time_sec),
        vehicle_label=e.vehicle_label,
        vehicle_consist=_consist(e.vehicle_consist),
    )


def alert(a: g.Alert) -> m.Alert:
    return m.Alert(
        valid_from=_dt(a.valid_from),
        valid_to=_opt_dt(a.valid_to),
        text=_opt(a.text),
    )


def _active_period(p: g.AlertActivePeriod) -> m.ActivePeriod:
    return m.ActivePeriod(
        start=_opt_dt(p.start),
        end=_opt_dt(p.end),
        current=p.current,
        upcoming=p.upcoming,
    )


def live_alert(a: g.LiveAlert) -> m.LiveAlert:
    return m.LiveAlert(
        id=a.id,
        type=a.type_,
        header=a.header,
        active_period=tuple(_active_period(p) for p in a.active_period),
        # DELAY and DETOUR alerts send platform IDs as integers.
        stops=tuple(str(stop) for stop in a.stops),
        routes=tuple(_opt(a.routes) or ()),
        description=_opt(a.description),
    )


# Statistics


def daily_stats(s: g.AggregateByDate) -> m.DailyStats:
    return m.DailyStats(
        **_stats(s),
        service_date=_date(s.service_date),
        peak=s.peak,
        holiday=s.holiday,
        weekend=s.weekend,
    )


def daily_headway_stats(s: g.HeadwayAggregateByDate) -> m.DailyHeadwayStats:
    return m.DailyHeadwayStats(
        **_stats(s),
        service_date=_date(s.service_date),
        peak=s.peak,
        holiday=s.holiday,
        weekend=s.weekend,
        bunched=s.bunched,
        on_time=s.on_time,
    )


def _time_of_day_stats(s: g.AggregateByTime) -> m.TimeOfDayStats:
    # 1970-01-01THH:MM:SS, or 1970-01-02 for service after midnight.
    return m.TimeOfDayStats(
        **_stats(s),
        dep_time=datetime.datetime.fromisoformat(s.dep_time_from_epoch) - _EPOCH,
        is_peak_day=s.is_peak_day,
    )


def travel_time_stats(r: g.TravelTimeAggregate2Response) -> m.TravelTimeStats:
    return m.TravelTimeStats(
        by_date=tuple(daily_stats(s) for s in r.by_date),
        by_time=tuple(_time_of_day_stats(s) for s in r.by_time),
    )


# Line metrics


def trip_metrics(e: g.TripMetricsEntry) -> m.TripMetrics:
    # The spec can't list the fleet_mix_<type> fields, so they arrive as extras.
    fleet_mix = {
        key.removeprefix(_FLEET_MIX_PREFIX): float(value)
        for key, value in e.additional_properties.items()
        if key.startswith(_FLEET_MIX_PREFIX) and value is not None
    }
    return m.TripMetrics(
        date=_date(e.date),
        line=e.line,
        count=e.count,
        total_time=e.total_time,
        miles_covered=e.miles_covered,
        avg_car_age=_opt(e.avg_car_age),
        pct_new_trips=_opt(e.pct_new_trips),
        fleet_mix=fleet_mix,
    )


def line_delays(e: g.LineDelayEntry) -> m.LineDelays:
    return m.LineDelays(
        date=_date(e.date),
        line=e.line,
        total_delay_time=e.total_delay_time,
        brake_problem=e.brake_problem,
        car_traffic=e.car_traffic,
        disabled_vehicle=e.disabled_vehicle,
        door_problem=e.door_problem,
        fire=e.fire,
        flooding=e.flooding,
        mechanical_problem=e.mechanical_problem,
        medical_emergency=e.medical_emergency,
        other=e.other,
        police_activity=e.police_activity,
        power_problem=e.power_problem,
        signal_problem=e.signal_problem,
        switch_problem=e.switch_problem,
        track_issue=e.track_issue,
        track_work=e.track_work,
    )


def service_hours(e: g.ServiceHoursEntry) -> m.ServiceHours:
    return m.ServiceHours(
        date=_date(e.date), scheduled=e.scheduled, delivered=e.delivered
    )


def ridership(e: g.RidershipEntry) -> m.Ridership:
    return m.Ridership(date=_date(e.date), count=e.count)


def _day_service_levels(
    d: g.ByDayKindServiceLevels | None | Unset,
) -> m.DayServiceLevels | None:
    d = _opt(d)
    if d is None:
        return None
    return m.DayServiceLevels(
        date=_date(d.date), service_levels=tuple(d.service_levels)
    )


def _service_levels(s: g.ServiceLevelsByDayKind) -> m.ServiceLevels:
    return m.ServiceLevels(
        weekday=_day_service_levels(s.weekday),
        saturday=_day_service_levels(s.saturday),
        sunday=_day_service_levels(s.sunday),
    )


def scheduled_service(r: g.GetScheduledServiceResponse) -> m.ScheduledService:
    return m.ScheduledService(
        start_date=_date(r.start_date),
        end_date=_date(r.end_date),
        start_date_service_levels=_service_levels(r.start_date_service_levels),
        end_date_service_levels=_service_levels(r.end_date_service_levels),
        counts=tuple(
            m.ScheduledServiceCount(date=_date(c.date), count=c.count) for c in r.counts
        ),
    )


def _time_prediction_bucket(b: g.TimePredictionBucket) -> m.TimePredictionBucket:
    return m.TimePredictionBucket(
        weekly=_date(b.weekly),
        mode=b.mode,
        route_id=b.route_id,
        bin=b.bin_,
        arrival_departure=b.arrival_departure,
        num_predictions=b.num_predictions,
        num_accurate_predictions=b.num_accurate_predictions,
    )


def time_prediction_week(w: g.TimePredictionWeek) -> m.TimePredictionWeek:
    return m.TimePredictionWeek(
        route_id=w.route_id,
        week=_date(w.week),
        prediction=tuple(_time_prediction_bucket(b) for b in w.prediction),
    )


def _speed_restriction(z: g.SpeedRestrictionZone) -> m.SpeedRestriction:
    return m.SpeedRestriction(
        id=z.id,
        date=_date(z.date),
        line_id=z.line_id,
        description=z.description,
        direction=z.direction,
        reason=z.reason,
        from_stop_id=_opt(z.from_stop_id),
        to_stop_id=_opt(z.to_stop_id),
        reported=_date(z.reported),
        speed_mph=z.speed_mph,
        track_feet=z.track_feet,
    )


def speed_restrictions(r: g.SpeedRestrictionsResponse) -> m.SpeedRestrictions:
    return m.SpeedRestrictions(
        available=r.available,
        date=_opt_date(r.date),
        zones=tuple(_speed_restriction(z) for z in _opt(r.zones) or ()),
    )


# Reference data


def routes(r: g.RoutesResponse) -> m.Routes:
    return m.Routes(
        rapid_transit=tuple(r.rapid_transit),
        bus=tuple(r.bus),
        commuter_rail=tuple(r.commuter_rail),
        ferry=tuple(r.ferry),
    )


def _station(s: g.StationStop) -> m.Station:
    return m.Station(
        stop_name=s.stop_name,
        station=s.station,
        order=s.order,
        stops={
            int(direction): tuple(ids)
            for direction, ids in s.stops.additional_properties.items()
        },
        branches=tuple(_opt(s.branches) or ()),
        accessible=bool(_opt(s.accessible)),
        pedal_park=bool(_opt(s.pedal_park)),
        enclosed_bike_parking=bool(_opt(s.enclosed_bike_parking)),
        terminus=bool(_opt(s.terminus)),
        disabled=bool(_opt(s.disabled)),
        short=_opt(s.short),
    )


def route_stops(r: g.StopsResponse) -> m.RouteStops:
    return m.RouteStops(
        type=r.type_,
        directions={
            int(direction): name
            for direction, name in r.direction.additional_properties.items()
        },
        stations=tuple(_station(s) for s in r.stations),
        service_start=_opt_date(r.service_start),
        service_end=_opt_date(r.service_end),
    )


def _facility_stop_id(r: g.FacilityRelationships | None | Unset) -> str | None:
    r = _opt(r)
    stop = None if r is None else _opt(r.stop)
    data = None if stop is None else _opt(stop.data)
    return None if data is None else data.id


def _facility(f: g.Facility) -> m.Facility:
    a: g.FacilityAttributes = f.attributes
    return m.Facility(
        id=f.id,
        type=a.type_,
        long_name=_opt(a.long_name),
        short_name=_opt(a.short_name),
        latitude=_opt_float(a.latitude),
        longitude=_opt_float(a.longitude),
        stop_id=_facility_stop_id(f.relationships),
        properties=tuple(
            m.FacilityProperty(name=p.name, value=_opt(p.value))
            for p in _opt(a.properties) or ()
        ),
    )


def facilities(r: g.FacilitiesResponse) -> list[m.Facility]:
    return [_facility(f) for f in r.data]


def healthcheck(r: g.HealthcheckResponse) -> m.Healthcheck:
    failed = _opt(r.failed_checks)
    return m.Healthcheck(
        status=r.status,
        failed_checks={} if failed is None else dict(failed.additional_properties),
    )


# Overview dashboard


def _service_day(d: g.DashboardServiceDay) -> m.ServiceDay:
    return m.ServiceDay(
        cancelled=d.cancelled,
        total_trips=d.total_trips,
        trips_per_hour=tuple(_opt(d.trips_per_hour) or ()),
    )


def _service_regime(r: g.DashboardServiceRegime) -> m.ServiceRegime:
    return m.ServiceRegime(
        weekday=_service_day(r.weekday),
        saturday=_service_day(r.saturday),
        sunday=_service_day(r.sunday),
    )


def _dashboard_line(line: g.DashboardLine) -> m.DashboardLine:
    regimes = line.service_regimes
    return m.DashboardLine(
        id=line.id,
        short_name=line.short_name,
        long_name=line.long_name,
        route_ids=tuple(line.route_ids),
        start_date=_date(line.start_date),
        line_kind=line.line_kind,
        ridership_history=_history(line.ridership_history),
        service_history=_history(line.service_history),
        service_regimes=m.ServiceRegimes(
            current=_service_regime(regimes.current),
            one_year_ago=_service_regime(regimes.one_year_ago),
            baseline=_service_regime(regimes.baseline),
        ),
    )


def _dashboard_summary(s: g.DashboardSummary) -> m.DashboardSummary:
    return m.DashboardSummary(
        total_ridership_history=_history(s.total_ridership_history),
        total_service_history=_history(s.total_service_history),
        total_ridership_percentage=s.total_ridership_percentage,
        total_service_percentage=s.total_service_percentage,
        total_passengers=s.total_passengers,
        total_trips=s.total_trips,
        total_routes_cancelled=s.total_routes_cancelled,
        total_reduced_service=s.total_reduced_service,
        total_increased_service=s.total_increased_service,
        start_date=_date(s.start_date),
        end_date=_date(s.end_date),
    )


def service_ridership_dashboard(
    r: g.ServiceRidershipDashboardResponse,
) -> m.ServiceRidershipDashboard:
    return m.ServiceRidershipDashboard(
        summary_data=_dashboard_summary(r.summary_data),
        mode_data={
            mode: _dashboard_summary(summary)
            for mode, summary in r.mode_data.additional_properties.items()
        },
        line_data={
            line_id: _dashboard_line(line)
            for line_id, line in r.line_data.additional_properties.items()
        },
    )
