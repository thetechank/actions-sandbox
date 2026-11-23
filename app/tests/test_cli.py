import pytest

from tidetable.cli import main


def test_prints_the_next_high_and_low_in_time_order(capsys):
    main(["Kestrel Bay", "--from", "2026-11-23T00:00Z"])
    header, first, second = capsys.readouterr().out.splitlines()
    assert header == "Kestrel Bay, from 2026-11-23 00:00 UTC"
    assert {first.split()[0], second.split()[0]} == {"high", "low"}
    assert first.split()[1:3] < second.split()[1:3]
    assert first.endswith(" m") and second.endswith(" m")


def test_an_unknown_harbour_names_the_known_ones():
    with pytest.raises(SystemExit, match="unknown harbour 'Atlantis'; known: Greyhaven, Kestrel"):
        main(["Atlantis"])
