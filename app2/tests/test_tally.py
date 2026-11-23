import pytest

from birdtally.tally import read_sightings, totals

SHEET = """date,site,species,count
2026-11-22,Marsh Lane hide,Lapwing,41
2026-11-22,Estuary wall,lapwing ,23
2026-11-22,Estuary wall,Curlew,11
2026-11-22,Marsh Lane hide,Teal,11
"""


def test_species_names_are_folded_and_summed():
    want = [("lapwing", 64), ("curlew", 11), ("teal", 11)]
    assert totals(read_sightings(SHEET.splitlines())) == want


def test_a_count_that_is_not_a_number_names_its_line():
    sheet = "date,site,species,count\n2026-11-22,Estuary wall,Curlew,a few\n"
    with pytest.raises(ValueError, match="line 2: count 'a few' is not a whole number"):
        read_sightings(sheet.splitlines())


def test_a_count_below_one_is_refused():
    sheet = "date,site,species,count\n2026-11-22,Estuary wall,Curlew,0\n"
    with pytest.raises(ValueError, match="line 2: count 0 must be at least 1"):
        read_sightings(sheet.splitlines())
