"""tidetable HARBOUR [--from TIME]: prints the next high and low water, in time order."""

import argparse
from datetime import UTC, datetime

from tidetable.predict import next_high_and_low
from tidetable.table import HARBOURS


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="tidetable", description=__doc__)
    parser.add_argument("harbour")
    parser.add_argument("--from", dest="start", help="ISO 8601 time (default: now, UTC)")
    args = parser.parse_args(argv)
    if args.harbour not in HARBOURS:
        raise SystemExit(f"unknown harbour '{args.harbour}'; known: {', '.join(sorted(HARBOURS))}")
    start = datetime.fromisoformat(args.start) if args.start else datetime.now(UTC)
    print(f"{args.harbour}, from {start:%Y-%m-%d %H:%M} UTC")
    for tide in sorted(next_high_and_low(HARBOURS[args.harbour], start), key=lambda t: t.when):
        print(f"  {tide.kind:<4}  {tide.when:%Y-%m-%d %H:%M} UTC  {tide.metres:.2f} m")
