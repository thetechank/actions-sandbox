"""Harmonic tide prediction: the height of the water is a mean level plus a sum of cosines.

Each constituent is one regular pull of the moon or sun, with its own speed (degrees per hour),
and each harbour has its own amplitude (metres) and phase (degrees) for it:
    height(t) = mean_level + sum(amplitude * cos(speed * hours_since_epoch - phase))
"""

import math
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

EPOCH = datetime(2026, 1, 1, tzinfo=UTC)

# Speeds in degrees per hour of the five constituents the table uses.
SPEEDS = {"M2": 28.9841042, "S2": 30.0, "N2": 28.4397295, "K1": 15.0410686, "O1": 13.9430356}


@dataclass(frozen=True)
class Constituent:
    name: str
    amplitude: float
    phase: float


@dataclass(frozen=True)
class Harbour:
    name: str
    mean_level: float
    constituents: tuple[Constituent, ...]


@dataclass(frozen=True)
class Tide:
    kind: str
    when: datetime
    metres: float


def height(harbour: Harbour, when: datetime) -> float:
    hours = (when - EPOCH) / timedelta(hours=1)
    return harbour.mean_level + sum(
        c.amplitude * math.cos(math.radians(SPEEDS[c.name] * hours - c.phase))
        for c in harbour.constituents
    )


def next_high_and_low(harbour: Harbour, start: datetime) -> tuple[Tide, Tide]:
    """The first high water and the first low water after start, to the minute (within 25 hours)."""
    minute = timedelta(minutes=1)
    high = low = None
    before, here = height(harbour, start - minute), height(harbour, start)
    for i in range(1, 25 * 60):
        when = start + i * minute
        after = height(harbour, when)
        if high is None and here > before and here >= after:
            high = Tide("high", when - minute, round(here, 3))
        if low is None and here < before and here <= after:
            low = Tide("low", when - minute, round(here, 3))
        if high and low:
            return high, low
        before, here = here, after
    raise ValueError(f"{harbour.name}: no high and low within 25 hours")
