#!/usr/bin/env python3
"""Record one real response per endpoint into tests/fixtures/, for the model tests.

Each fixture is named after its module in `transitmatters._generated.api.api`
and holds the response body, trimmed to keep the files small: long lists keep
their first few items plus one of every other shape (which fields are null),
and large maps keep their first few keys.

Usage:
    uv run python scripts/record_fixtures.py               # every endpoint
    uv run python scripts/record_fixtures.py get_routes    # just these
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import httpx

BASE_URL = "https://dashboard-api.labs.transitmatters.org"
FIXTURES = Path(__file__).resolve().parent.parent / "tests" / "fixtures"

KEEP_ITEMS = 5
# Objects with more keys than this are maps keyed by ID or date, not records.
MAP_MIN_KEYS = 25
# Kept whole: tests use every station on the route.
UNTRIMMED = {"get_stops_for_route"}

_RANGE = {"start_date": "2025-03-03", "end_date": "2025-03-07"}
_MONTH = {"start_date": "2025-03-01", "end_date": "2025-03-31"}
_QUARTER = {"start_date": "2025-01-01", "end_date": "2025-03-31"}

# Endpoint module -> (path, query params). Red Line, Alewife to Braintree.
REQUESTS: dict[str, tuple[str, dict[str, Any]]] = {
    "get_healthcheck": ("/api/healthcheck", {}),
    "get_headways": ("/api/headways/2025-03-04", {"stop": "70061"}),
    "get_dwells": ("/api/dwells/2025-03-04", {"stop": "70063"}),
    "get_travel_times": (
        "/api/traveltimes/2025-03-04",
        {"from_stop": "70061", "to_stop": "70105"},
    ),
    "get_historical_alerts": ("/api/alerts/2025-03-04", {"route": "Red"}),
    "get_aggregate_travel_times": (
        "/api/aggregate/traveltimes",
        {**_RANGE, "from_stop": "70061", "to_stop": "70105"},
    ),
    "get_aggregate_travel_times_v2": (
        "/api/aggregate/traveltimes2",
        {**_RANGE, "from_stop": "70061", "to_stop": "70105"},
    ),
    "get_aggregate_headways": ("/api/aggregate/headways", {**_RANGE, "stop": "70061"}),
    "get_aggregate_dwells": ("/api/aggregate/dwells", {**_RANGE, "stop": "70063"}),
    "get_current_alerts": ("/api/alerts", {}),
    "get_line_delays": (
        "/api/linedelays",
        {**_QUARTER, "line": "Red", "agg": "weekly"},
    ),
    "get_trip_metrics": (
        "/api/tripmetrics",
        {**_MONTH, "line": "line-red", "agg": "daily"},
    ),
    "get_scheduled_service": (
        "/api/scheduledservice",
        {**_MONTH, "route_id": "Red", "agg": "daily"},
    ),
    "get_ridership": ("/api/ridership", {**_QUARTER, "line_id": "line-Red"}),
    "get_facilities": ("/api/facilities", {}),
    "get_speed_restrictions": (
        "/api/speed_restrictions",
        {"line_id": "line-Red", "date": "2025-03-04"},
    ),
    "get_service_hours": (
        "/api/service_hours",
        {**_MONTH, "line_id": "line-red", "agg": "daily"},
    ),
    "get_time_predictions": ("/api/time_predictions", {"route_id": "Red"}),
    "get_service_ridership_dashboard": ("/api/service_ridership_dashboard", {}),
    "get_routes": ("/api/routes", {}),
    "get_stops_for_route": ("/api/stops/Red", {}),
}


def _shape(value: Any) -> Any:
    """Which fields are present and null, recursively; items with a new shape are kept."""
    if isinstance(value, dict) and len(value) < MAP_MIN_KEYS:
        return frozenset((k, _shape(v)) for k, v in value.items())
    if isinstance(value, list):
        return frozenset(_shape(v) for v in value)
    return value is None


def trim(value: Any) -> Any:
    if isinstance(value, list):
        kept, seen = [], set()
        for i, item in enumerate(value):
            shape = _shape(item)
            if i < KEEP_ITEMS or shape not in seen:
                kept.append(item)
            seen.add(shape)
        return [trim(item) for item in kept]
    if isinstance(value, dict):
        items = list(value.items())
        if len(items) >= MAP_MIN_KEYS:
            items = items[:KEEP_ITEMS]
        return {k: trim(v) for k, v in items}
    return value


def main() -> None:
    names = sys.argv[1:] or list(REQUESTS)
    if unknown := set(names) - set(REQUESTS):
        sys.exit(f"error: unknown endpoint(s): {', '.join(sorted(unknown))}")
    FIXTURES.mkdir(parents=True, exist_ok=True)
    with httpx.Client(base_url=BASE_URL, timeout=60) as client:
        for name in names:
            path, params = REQUESTS[name]
            response = client.get(path, params=params)
            response.raise_for_status()
            body = response.json() if name in UNTRIMMED else trim(response.json())
            out = FIXTURES / f"{name}.json"
            out.write_text(json.dumps(body, indent=1, ensure_ascii=False) + "\n")
            print(
                f"{out.relative_to(FIXTURES.parent.parent)}: {out.stat().st_size} bytes"
            )


if __name__ == "__main__":
    main()
