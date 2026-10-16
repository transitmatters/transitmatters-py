# transitmatters-py

<!-- The API docs include this file from here down. -->

MBTA performance data from the [TransitMatters Data Dashboard](https://dashboard.transitmatters.org),
as Python objects: travel times, headways, dwells, ridership, service levels,
delays, speed restrictions, and alerts.

```sh
pip install transitmatters
```

```python
from transitmatters import TransitMatters

tm = TransitMatters()

# Every southbound Red Line trip from Alewife to Braintree on March 4, 2025
trips = tm.travel_times("2025-03-04", from_stop="70061", to_stop="70105")
print(trips[0].dep_dt, trips[0].travel_time_sec)
```

Dates can be `datetime.date` objects or `"YYYY-MM-DD"` strings, and date ranges
include both ends. Parameters that take IDs accept one string or a list.

## Which method do I want?

**What happened on one day.** Each item is a single event.

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

## Finding IDs

Each kind of ID has its own format, and some endpoints spell the same line
differently. Check this table before guessing:

| Parameter | Used by | Looks like |
| --- | --- | --- |
| `stop`, `from_stop`, `to_stop` | `headways`, `dwells`, `travel_times`, `aggregate_*` | `"70061"` (rapid transit), `"1-0-110"` (bus), `"CR-Fairmount_0_DB-2205-01"` (commuter rail) |
| `route`, `route_id` | `historical_alerts`, `scheduled_service`, `time_predictions`, `stops` | `"Red"`, `"66"`, `"CR-Fairmount"`, `"Boat-F1"` |
| `line` | `line_delays` | `"Red"`, `"CR-Fairmount"` |
| `line`, `line_id` | `trip_metrics`, `service_hours` | `"line-red"` (lowercase; rapid transit only) |
| `line_id` | `ridership` | `"line-Red"`, `"line-66"`, `"line-Fairmount"` |
| `line_id` | `speed_restrictions` | `"line-Red"` (case-sensitive; rapid transit only) |

`TransitMatters.routes` lists every route ID. `TransitMatters.stops` lists the
stations on a route, with the stop ID of each platform by direction:

```python
red = tm.stops("Red")
print(red.direction.to_dict())  # {'0': 'northbound', '1': 'southbound'}
for station in red.stations[:3]:
    print(station.stop_name, station.stops.to_dict())
# Alewife {'0': ['70061'], '1': ['70061']}
# Davis {'0': ['70064'], '1': ['70063']}
# Porter {'0': ['70066'], '1': ['70065']}
```

Platforms have separate IDs for each direction, so `from_stop` and `to_stop`
must both be platforms for the direction you're traveling. Southbound from
Davis to Porter is `from_stop="70063", to_stop="70065"`.

A stop ID that doesn't exist isn't an error; you just get an empty list back.

## Working with pandas

Every result is a model object (see `transitmatters.models`), and every model
has `to_dict()`:

```python
import pandas as pd

events = tm.headways("2025-03-04", stop="70061")
df = pd.DataFrame([e.to_dict() for e in events])
df["current_dep_dt"] = pd.to_datetime(df["current_dep_dt"])
```

- Timestamps are Eastern local time, formatted `YYYY-MM-DDTHH:MM:SS` with no
  offset.
- `to_dict()` uses the API's field names. A few differ from the Python
  attribute names, e.g. `min` and `25%` instead of `min_` and `field_25`.
- When a response wraps its list in a field, such as
  `scheduled_service(...).counts` or `speed_restrictions(...).zones`, build
  the DataFrame from that field.

## Errors

When the API rejects a request, methods raise `transitmatters.APIError`:

```python
from transitmatters import APIError

try:
    tm.stops("Purple")
except APIError as e:
    print(e.status_code, e.message)  # 404 Route 'Purple' not found
```

## Async

`transitmatters.AsyncTransitMatters` has the same methods, as coroutines. It's
useful for fetching many days at once. In Jupyter you can `await` directly in
a cell.

```python
import asyncio
from transitmatters import AsyncTransitMatters

async def main():
    async with AsyncTransitMatters() as tm:
        days = ["2025-03-03", "2025-03-04", "2025-03-05"]
        return await asyncio.gather(*(tm.headways(d, stop="70061") for d in days))

per_day = asyncio.run(main())
```

## Development

```sh
uv sync
uv run pytest
uv run python scripts/docs.py  # preview the API docs at http://localhost:8080
```

The API docs are built from this README and the docstrings in
`src/transitmatters/`, and are published to GitHub Pages on every push to
`main`.

`src/transitmatters/_generated/` is generated from the upstream OpenAPI spec by
`openapi-python-client`; don't edit it by hand. A weekly workflow syncs the
spec and opens a PR (see `scripts/sync_spec.py`). The public API lives in
`src/transitmatters/client.py`.
