# Changelog

## 0.2.1

### Added

- Python 3.12 support. The package now supports Python 3.12, 3.13, and 3.14.
- A [getting-started notebook](examples/getting-started.ipynb) that runs in
  Google Colab.

## 0.2.0

This release replaces the generated models with the package's own, and
makes route and line parameters consistent. Both are breaking changes; see
**Upgrading from 0.1.0** below.

### Added

- `Line`: pass `Line.RED` and so on wherever a method takes a route or line,
  and the client sends the ID each endpoint expects (`"Red"`, `"line-red"`,
  or `"line-Red"`).
- `RouteStops.station` finds a station by name or station ID, and
  `RouteStops.trip` returns the platform stop IDs for travel between two
  stations.
- `headways`, `dwells`, `travel_times`, and `historical_alerts` take an
  optional `end_date`, and fetch every day in the range concurrently.
- `trip_metrics` accepts ranges longer than the API's 150-entry limit, by
  fetching them in pieces.
- `to_dataframe` turns a list of results into a pandas DataFrame. Install
  pandas with `pip install 'transitmatters[pandas]'`.
- Error subclasses of `APIError`: `BadRequestError`, `NotFoundError`,
  `RangeTooLongError`, and `ServerError`. Failures with no response raise
  `NetworkError` instead of an `httpx` exception.
- Retries with exponential backoff for timeouts, connection failures, and
  429, 502, 503, and 504 responses. Set with `max_retries` (default 3).
- `max_concurrency` (default 8) limits requests in flight for date ranges.

### Changed

- Results are frozen dataclasses from `transitmatters.models`:
  - Times are timezone-aware `datetime`s in Eastern time, and dates are
    `datetime.date`s, rather than strings.
  - Missing values are `None`, never `Unset`.
  - `direction` is an `int` on every event; headways used to have `"0"`.
  - `vehicle_consist` is a tuple of car numbers, e.g. `("1850", "1851")`.
  - Lists inside results are tuples.
- `to_dict()` returns Python values with the new field names, not the API's
  JSON.

### Removed

- The generated models are no longer exported from `transitmatters.models`.
- `additional_properties` and item access (`event["field"]`) on results.

### Upgrading from 0.1.0

Parameters:

| 0.1.0 | 0.2.0 |
| --- | --- |
| `scheduled_service(..., route_id="Red")` | `scheduled_service(..., route=Line.RED)` |
| `ridership(..., line_id="line-Red")` | `ridership(..., line=Line.RED)` |
| `speed_restrictions(date, line_id="line-Red")` | `speed_restrictions(date, line=Line.RED)` |
| `service_hours(..., line_id="line-red")` | `service_hours(..., line=Line.RED)` |
| `time_predictions(route_id="Red")` | `time_predictions(Line.RED)` |
| `stops(route_id="Red")` | `stops(Line.RED)` |

The old ID strings still work, passed under the new parameter names.

Result types and fields:

| 0.1.0 | 0.2.0 |
| --- | --- |
| `HeadwayEvent`, `DwellEvent`, `TravelTimeEvent` | `Headway`, `Dwell`, `TravelTime` |
| `AggregateByDate` | `DailyStats` |
| `HeadwayAggregateByDate` | `DailyHeadwayStats` |
| `TravelTimeAggregate2Response` | `TravelTimeStats` (`by_time` items are `TimeOfDayStats`) |
| `min_`, `max_`, `sum_`, `field_25`, `field_50`, `field_75` | `min`, `max`, `sum`, `p25`, `p50`, `p75` |
| `AggregateByTime.dep_time_from_epoch` (`"1970-01-01T05:30:00"`) | `TimeOfDayStats.dep_time` (`timedelta(hours=5, minutes=30)`) |
| `TripMetricsEntry`, `LineDelayEntry`, `ServiceHoursEntry`, `RidershipEntry` | `TripMetrics`, `LineDelays`, `ServiceHours`, `Ridership` |
| `TripMetricsEntry["fleet_mix_red1"]` | `TripMetrics.fleet_mix["red1"]` |
| `GetScheduledServiceResponse` | `ScheduledService` |
| `SpeedRestrictionsResponse.zones` (`None` when unavailable) | `SpeedRestrictions.zones` (empty) |
| `StopsResponse.direction`, `StationStop.stops` (string keys) | `RouteStops.directions`, `Station.stops` (int keys) |
| `FacilitiesResponse.data` | `facilities()` returns the list directly, as `Facility` |
| `Facility.attributes.long_name`, `.relationships.stop.data.id` | `Facility.long_name`, `Facility.stop_id` |
| `TimePredictionBucket.bin_`, `LiveAlert.type_` | `bin`, `type` |
| `LiveAlert.stops` (ints for delays and detours) | `LiveAlert.stops` (always strings) |
| `HealthcheckResponse.status == "pass"` | `Healthcheck.ok` |
| `ServiceRidershipDashboardResponse` | `ServiceRidershipDashboard`, with history keyed by `date` |

If you built DataFrames with `pd.DataFrame([e.to_dict() for e in events])`,
use `to_dataframe(events)`. It keeps time columns timezone-aware, so drop
the `pd.to_datetime` step.

## 0.1.0

First release.
