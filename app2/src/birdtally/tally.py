"""Sightings in, totals out: one row per sighting (date, site, species, count)."""

import csv
from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass


@dataclass(frozen=True)
class Sighting:
    date: str
    site: str
    species: str
    count: int


def read_sightings(lines: Iterable[str]) -> list[Sighting]:
    rows = csv.DictReader(lines)
    sightings = []
    for n, row in enumerate(rows, start=2):
        try:
            count = int(row["count"])
        except ValueError:
            raise ValueError(f"line {n}: count '{row['count']}' is not a whole number") from None
        if count < 1:
            raise ValueError(f"line {n}: count {count} must be at least 1")
        sightings.append(Sighting(row["date"], row["site"], row["species"].strip().lower(), count))
    return sightings


def totals(sightings: Iterable[Sighting]) -> list[tuple[str, int]]:
    """Birds per species, most first; ties in alphabetical order."""
    counter: Counter[str] = Counter()
    for s in sightings:
        counter[s.species] += s.count
    return sorted(counter.items(), key=lambda item: (-item[1], item[0]))
