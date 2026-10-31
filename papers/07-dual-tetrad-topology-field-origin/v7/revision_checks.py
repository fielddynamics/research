#!/usr/bin/env python3
"""
Checks behind REVISION_NOTES.md (Paper VII, v7)
===============================================

  1. V + E + F = k(k + d) for the compound of two d-simplices: which d?
  2. Section II.E Route 2, the Section IV.B ratio check and Eq. (a0) are one
     relation, a0 = k^2 G m_e / r_e^2, read three ways.
  3. Outer Milky Way: the paper's prediction at 25 kpc against Eilers et al.
     (2019) and Jiao et al. (2023).

Python 3.8+, standard library only.

    python revision_checks.py
"""
from math import comb, sqrt

G = 6.67430e-11
M_E = 9.1093837139e-31
R_E = 2.8179403205e-15
A0_PAPER = 1.22e-10          # value used in the paper


def main():
    print("1. V + E + F for two interlocking d-simplices (2-faces counted) vs k(k + d)")
    holds = []
    for d in range(1, 8):
        k = d + 1
        v, e, f = 2 * (d + 1), 2 * comb(d + 1, 2), 2 * comb(d + 1, 3)
        ok = v + e + f == k * (k + d)
        holds.append(d) if ok else None
        print(f"   d = {d}: {v} + {e} + {f} = {v + e + f:4d}   k(k+d) = {k * (k + d):4d}   {'equal' if ok else ''}")
    print(f"   equal only for d = {holds}  (among d >= 2, only d = 3)")

    print("\n2. One relation, three readings: a0 = k^2 G m_e / r_e^2")
    a0_pred = 16 * G * M_E / R_E ** 2
    r_route2 = 4 * sqrt(G * M_E / A0_PAPER)
    ratio = A0_PAPER / (G * M_E / R_E ** 2)
    print(f"   a0 from the relation:            {a0_pred:.4e} m/s^2  (paper quotes 1.22e-10)")
    print(f"   Route 2, r_e = k sqrt(G m_e/a0): {r_route2 * 1e15:.4f} fm   deviation {100 * (r_route2 - R_E) / R_E:+.3f}%")
    print(f"   Section IV.B ratio a0/(G m_e/r_e^2) = {ratio:.3f}   deviation from 16 {100 * (ratio - 16) / 16:+.3f}%")
    print("   The 0.21% and 0.41% are the same comparison: a0 scales as r^-2, so 2 x 0.21% = 0.41%.")
    print("   Empirical a0 = (1.20 +/- 0.02 stat +/- 0.24 sys) x 1e-10 m/s^2 (McGaugh, Lelli & Schombert 2016)")

    print("\n3. Outer Milky Way rotation speed near 25 kpc (km/s)")
    v20, v30 = 208, 201                      # paper, Table (AQUAL, mu = x/(1+x))
    v25 = v20 + (v30 - v20) * 0.5
    print(f"   Paper VII prediction (interpolated): {v25:.0f}")
    print("   Eilers et al. 2019 (data point used in the paper's figure): 200 +/- 15")
    print("   Jiao et al. 2023, Gaia DR3, 25.5 kpc: 181; flat curve rejected at 3 sigma")


if __name__ == "__main__":
    main()
