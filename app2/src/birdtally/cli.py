"""birdtally SHEET: prints the birds counted per species, most first."""

import argparse

from birdtally.tally import read_sightings, totals


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="birdtally", description=__doc__)
    parser.add_argument("sheet", help="CSV with the columns date, site, species, count")
    args = parser.parse_args(argv)
    with open(args.sheet, newline="") as f:
        try:
            sightings = read_sightings(f)
        except ValueError as e:
            raise SystemExit(f"{args.sheet}: {e}") from None
    species = totals(sightings)
    sites = len({s.site for s in sightings})
    print(f"birdtally: {sites} sites, {len(species)} species, {sum(n for _, n in species)} birds")
    for name, n in species:
        print(f"  {name:<14}{n:>4}")
