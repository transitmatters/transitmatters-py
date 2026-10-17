# transitmatters-py

<!-- The API docs include this file from here down. -->

MBTA performance data from the [TransitMatters Data Dashboard](https://dashboard.transitmatters.org),
as Python objects: travel times, headways, dwells, ridership, service levels,
delays, speed restrictions, and alerts.

```sh
pip install transitmatters            # or 'transitmatters[pandas]' for to_dataframe
```

```python
from transitmatters import Line, TransitMatters, to_dataframe

tm = TransitMatters()

# Southbound Red Line platforms from Davis to Porter
pair = tm.stops(Line.RED).trip("Davis", "Porter")

# Every trip between them in March 2025
trips = tm.travel_times(
    "2025-03-01", "2025-03-31", from_stop=pair.from_stop, to_stop=pair.to_stop
)
print(trips[0].dep_dt, trips[0].travel_time_sec)
# 2025-03-01 05:18:01-05:00 82.0

df = to_dataframe(trips)
```

Dates can be `datetime.date` objects or `"YYYY-MM-DD"` strings. Date ranges
include both ends, and dates are service dates: trips after midnight, until
about 3:30 AM, count toward the day before. Times are timezone-aware
`datetime`s in Eastern time.

## Which method do I want?

**What happened, trip by trip.** Each item is one event. Pass one date, or a
start and end date to get every day in between; days are fetched
concurrently.

| Question | Method | Each item is |
| --- | --- | --- |
| How long did trips between two stops take? | `TransitMatters.travel_times` | a trip |
| How long between departures at a stop? | `TransitMatters.headways` | a departure |
| How long did vehicles sit at a stop? | `TransitMatters.dwells` | a stop a vehicle made |
| Which alerts were posted for a route? | `TransitMatters.historical_alerts` | an alert |
| Where were speed restrictions on a line? | `TransitMatters.speed_restrictions` | a zone, in `.zones` |

**Trends over a date range.** Each item summarizes one day, week, or month.

| Question | Method | Each item is |
| --- | --- | --- |
| Travel-time statistics between two stops | `TransitMatters.aggregate_travel_times` | a day |
| ...also broken down by time of day | `TransitMatters.aggregate_travel_times_v2` | a day, or a 30-minute slot |
| Headway statistics, bunching, and on-time counts at a stop | `TransitMatters.aggregate_headways` | a day |
| Dwell-time statistics at a stop | `TransitMatters.aggregate_dwells` | a day |
| Trip count, speed, and miles for a rapid transit line | `TransitMatters.trip_metrics` | a day, week, or month |
| Minutes of delay on a line, by cause | `TransitMatters.line_delays` | a day or week |
| Number of scheduled trips on a route | `TransitMatters.scheduled_service` | a day, week, or month, in `.counts` |
| Scheduled vs. delivered service hours | `TransitMatters.service_hours` | a day, week, or month |
| Ridership on a line | `TransitMatters.ridership` | a week |
| How accurate arrival predictions were | `TransitMatters.time_predictions` | a week |

**Right now, and system-wide.**

| Question | Method |
| --- | --- |
| Which alerts are in effect now? | `TransitMatters.current_alerts` |
| Where are the elevators and escalators? | `TransitMatters.facilities` |
| Service and ridership across the whole system | `TransitMatters.service_ridership_dashboard` |
| Is the API healthy? | `TransitMatters.healthcheck` |

## Lines, routes, and stops

For the subway, pass a `Line` wherever a method takes a route or line:

```python
tm.ridership("2024-01-01", "2024-12-31", line=Line.ORANGE)
tm.trip_metrics("2024-01-01", "2024-12-31", line=Line.RED, agg="monthly")
```

The API spells lines differently by endpoint (`"Red"`, `"line-red"`,
`"line-Red"`); a `Line` is sent the right way to each. For buses, commuter
rail, and ferries, pass the route ID as a string, e.g. `"66"`,
`"CR-Fairmount"`, or `"Boat-F1"`. `TransitMatters.routes` lists them all.

The Green Line's delays and prediction accuracy are reported by branch, so
`line_delays` and `time_predictions` take `"Green-B"` through `"Green-E"`
instead of `Line.GREEN`.

### Stop IDs

Events are recorded per platform, and each direction has its own platform
ID. `TransitMatters.stops` lists a route's stations with their platforms, and
`transitmatters.models.RouteStops.trip` picks the right ones for travel between two stations:

```python
red = tm.stops(Line.RED)

red.station("Davis").stops
# {0: ('70064',), 1: ('70063',)}
red.directions
# {0: 'northbound', 1: 'southbound'}
red.trip("Davis", "Porter")
# StopPair(from_stop=('70063',), to_stop=('70065',), direction=1)

tm.headways("2025-03-04", stop=red.station("Davis").stops[1])
```

Stations can be named as on the dashboard (`"Davis"`) or by station ID
(`"place-davis"`). A stop ID that doesn't exist isn't an error; you just get
an empty list back.

## Working with pandas

`to_dataframe` turns a list of results into a DataFrame, with one column per
field. It needs pandas: `pip install 'transitmatters[pandas]'`.

```python
from transitmatters import to_dataframe

df = to_dataframe(tm.headways("2025-03-03", "2025-03-07", stop="70061"))
df.set_index("current_dep_dt")["headway_time_sec"].resample("1h").median()
```

- Time columns are timezone-aware, in `America/New_York`.
- Date columns, like `service_date`, are `datetime64` at midnight.
- When a result wraps its list in a field, such as
  `scheduled_service(...).counts` or `speed_restrictions(...).zones`, pass
  that field to `to_dataframe`.

Every result is a frozen dataclass from `transitmatters.models`, and has
`to_dict()` too.

## Errors and retries

When the API rejects a request, methods raise a subclass of
`transitmatters.APIError`:

```python
from transitmatters import NotFoundError

try:
    tm.stops("Purple")
except NotFoundError as e:
    print(e.status_code, e.message)  # 404 Route 'Purple' not found
```

| Exception | When |
| --- | --- |
| `BadRequestError` | A parameter is missing or invalid (400). |
| `NotFoundError` | The route doesn't exist (404). |
| `RangeTooLongError` | The date range is too long (403). `trip_metrics` splits long ranges to avoid this. |
| `ServerError` | The API failed (5xx). |
| `NetworkError` | No response arrived: the connection failed or timed out. |

All of them subclass `TransitMattersError`. Timeouts, connection failures,
and 429, 502, 503, and 504 responses are retried up to three times with
exponential backoff before raising; set `TransitMatters(max_retries=0)` to
turn that off.

## Async

`transitmatters.AsyncTransitMatters` has the same methods, as coroutines. In
Jupyter you can `await` directly in a cell.

```python
import asyncio
from transitmatters import AsyncTransitMatters, Line


async def main():
    async with AsyncTransitMatters() as tm:
        return await asyncio.gather(
            tm.ridership("2024-01-01", "2024-12-31", line=Line.RED),
            tm.ridership("2024-01-01", "2024-12-31", line=Line.ORANGE),
        )


red, orange = asyncio.run(main())
```

Both clients fetch date ranges concurrently already, up to `max_concurrency`
requests at once (8 by default).

## Development

```sh
uv sync
uv run pytest
uv run ruff check && uv run pyright src tests
uv run python scripts/docs.py  # preview the API docs at http://localhost:8080
```

The API docs are built from this README and the docstrings in
`src/transitmatters/`, and are published to GitHub Pages on every push to
`main`.

`src/transitmatters/_generated/` is generated from the upstream OpenAPI spec by
`openapi-python-client`; don't edit it by hand. A weekly workflow syncs the
spec and opens a PR (see `scripts/sync_spec.py`). The public API wraps it:

- `client.py` holds the clients, and `_endpoints.py` builds each request.
- `models.py` holds the public models, and `_convert.py` builds them from the
  generated ones.

When a spec sync adds an endpoint or a field, tests fail until it's wrapped
and converted. `tests/fixtures/` holds real responses for the model tests;
refresh one with `uv run python scripts/record_fixtures.py <endpoint>`.
