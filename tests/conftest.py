from __future__ import annotations

import pytest

from transitmatters import client


@pytest.fixture(autouse=True)
def sleeps(monkeypatch: pytest.MonkeyPatch) -> list[float]:
    """Skip retry backoff, recording each delay that would have been slept."""
    delays: list[float] = []

    async def asleep(delay: float) -> None:
        delays.append(delay)

    monkeypatch.setattr(client, "_sleep", delays.append)
    monkeypatch.setattr(client, "_asleep", asleep)
    return delays
