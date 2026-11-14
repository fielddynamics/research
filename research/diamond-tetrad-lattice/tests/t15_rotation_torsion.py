"""T15. Rotation as bond phases, and the axial torsion's sign. NOT RUN: not informative as designed.

The plan asked whether, under a uniform rotation modelled by Peierls phases on the bonds,
the TetA-leg and TetB-leg contributions to an axial (orientation-weighted) quantity are equal
and opposite. Working out the method shows the comparison is empty:

 1. On the diamond net every bond is a TetA leg read from its TetA end and a TetB leg read
    from its TetB end: it is the same bond traversed both ways. A Peierls phase is odd under
    reversing the direction (theta_ji = -theta_ij, which Hermiticity requires), so the two
    "contributions" are equal and opposite for any field at all, rotating or not.
 2. The per-bond phases are gauge-dependent; the gauge-invariant data are the fluxes through
    the hexagon rings. Those are fixed by Omega and the rings' vector areas, and carry no
    TetA/TetB label to compare.

So a pass would test nothing. The script demonstrates point 1 and stops. A meaningful lattice
version of Proposition 3 needs a lattice connection with independent frame data at each site
(a lattice tetrad and spin connection, as in Regge-type or lattice-gravity discretisations),
not a U(1) phase. Recorded as not run.
"""
import numpy as np
rng = np.random.default_rng(0)
Om = rng.normal(size=3); r = rng.normal(size=3) * 5; v = np.array([1, -1, -1.0])
A = lambda x: np.cross(Om, x)                    # rotating-frame vector potential (m/hbar = 1)
theta_AB = A(r + v / 2) @ v                       # along the TetA leg, from the A end
theta_BA = A(r + v / 2) @ (-v)                    # along the TetB leg, from the B end
print(f"theta along TetA leg {theta_AB:+.6f}, along TetB leg {theta_BA:+.6f}: opposite by definition")
print("\nT15 NOT RUN - not informative as designed (see docstring); needs a lattice tetrad and spin connection")
