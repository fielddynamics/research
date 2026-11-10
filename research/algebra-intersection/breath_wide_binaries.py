"""
breath_wide_binaries.py
=======================

What H_breath (BREATH_SPARC_PREREG.md) predicts for the pre-registered Gaia DR4 wide-binary
statistic R, using the archive's own solver (research/wide-binaries/gfd_field_solver.py) unchanged.

H_breath in the field equation: mu_eff(x) = mu(x) (x + 1)/(x + 13/17) = x/(x + 13/17),
which is mu with a0 -> a0_eff = (13/17) a0. So only the scale changes:
  a0_eff = (13/17) 1.2e-10 = 0.918e-10 m/s^2,  g_e = 2.09e-10 / a0_eff = 2.28 a0_eff.
"""
from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "wide-binaries"))
import wide_binary_prediction as wb  # noqa: E402

A0_EFF = 13 / 17 * wb.A0
G_E_PHYS = wb.G_E * wb.A0                     # 2.09e-10 m/s^2, unchanged
ge_eff = G_E_PHYS / A0_EFF

if __name__ == "__main__":
    print(f"a0_eff = {A0_EFF:.4e} m/s^2;  Galactic field = {ge_eff:.3f} a0_eff (baseline {wb.G_E:.3f} a0)")
    wb.A0 = A0_EFF                            # gamma_at uses wb.A0 for the MOND radius
    ss, gam = wb.curve(ge_eff)
    print("gamma(s), H_breath, M = 1.5 Msun:", " ".join(f"{g:.3f}" for g in wb.gamma_at(wb.SEPS, 1.5, ss, gam)))
    for M in (1.0, 1.5, 2.0):
        print(f"  M = {M:.1f}:  R = {wb.R_statistic(M, ss, gam):.3f}")
    print("baseline GFD (registered): R = 1.163 (range 1.138-1.184); Newton R = 1.000")
