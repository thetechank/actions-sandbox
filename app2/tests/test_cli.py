from pathlib import Path

from birdtally.cli import main

SHEET = Path(__file__).parent.parent / "sightings.csv"


def test_prints_totals_most_first(capsys):
    main([str(SHEET)])
    lines = capsys.readouterr().out.splitlines()
    assert lines[0] == "birdtally: 3 sites, 6 species, 143 birds"
    assert lines[1].split() == ["lapwing", "64"]
    assert lines[-1].split() == ["little", "egret", "4"]
