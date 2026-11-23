from datetime import UTC, datetime, timedelta

import pytest

from tidetable.predict import EPOCH, Constituent, Harbour, height, next_high_and_low
from tidetable.table import HARBOURS

# One constituent, M2 (the moon's twice-a-day tide), with phase 0: high water exactly at the epoch,
# low water half an M2 period (6 h 12.6 min) later, the next high a period (12 h 25.2 min) later.
ONLY_M2 = Harbour("Test Quay", mean_level=2.0, constituents=(Constituent("M2", 1.5, 0.0),))


def test_height_at_the_epoch_is_mean_plus_amplitude():
    assert height(ONLY_M2, EPOCH) == pytest.approx(3.5)


def test_height_half_a_period_later_is_mean_minus_amplitude():
    assert height(ONLY_M2, EPOCH + timedelta(hours=180 / 28.9841042)) == pytest.approx(0.5)


def test_next_low_then_high_after_the_epoch():
    high, low = next_high_and_low(ONLY_M2, EPOCH + timedelta(minutes=1))
    assert low.when == datetime(2026, 1, 1, 6, 13, tzinfo=UTC)
    assert low.metres == pytest.approx(0.5, abs=0.001)
    assert high.when == datetime(2026, 1, 1, 12, 25, tzinfo=UTC)
    assert high.metres == pytest.approx(3.5, abs=0.001)


@pytest.mark.parametrize("name", sorted(HARBOURS))
def test_every_harbour_has_a_high_and_a_low_within_a_day(name):
    start = datetime(2026, 11, 23, tzinfo=UTC)
    high, low = next_high_and_low(HARBOURS[name], start)
    assert start < high.when < start + timedelta(hours=25)
    assert start < low.when < start + timedelta(hours=25)
    assert high.metres > low.metres
