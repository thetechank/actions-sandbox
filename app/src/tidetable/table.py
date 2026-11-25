"""The harmonic table: invented harbours with invented constants (metres, degrees)."""

from tidetable.predict import Constituent, Harbour


def _harbour(name: str, mean_level: float, **constants: tuple[float, float]) -> Harbour:
    return Harbour(name, mean_level, tuple(Constituent(k, a, p) for k, (a, p) in constants.items()))


HARBOURS = {
    h.name: h
    for h in (
        _harbour("Kestrel Bay", 2.6, M2=(1.42, 112.0), S2=(0.48, 151.0), K1=(0.11, 302.0)),
        _harbour("Greyhaven", 3.1, M2=(1.95, 64.0), S2=(0.61, 98.0), N2=(0.37, 41.0)),
        _harbour("Port Amsel", 1.8, M2=(0.92, 207.0), S2=(0.30, 240.0), O1=(0.08, 15.0)),
        _harbour("Saltmarsh Quay", 2.2, M2=(1.20, 333.0), K1=(0.15, 120.0), O1=(0.12, 101.0)),
        _harbour("Port Merrow", 2.9, M2=(1.61, 18.0), S2=(0.52, 47.0), K1=(0.09, 260.0)),
    )
}
