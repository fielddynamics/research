#!/usr/bin/env python3
"""
a0 from the shape of SPARC rotation curves (method fixed in PREREGISTRATION_A0.md).

Where a galaxy's enclosed visible mass has levelled off (growth gamma = dlnM/dlnr < 0.1), the flux
involution of the net-field proof turns the slope of the rotation curve into mu, with no stellar
mass-to-light ratio:  s = 1 + dln v^2/dln r,  mu = 2 - (2 - gamma)/(2 - s),  x = mu/(1 - mu),  a0 = g/x.

  python a0_from_slope.py ROTMOD_DIR
"""
import csv
import math
import os
import sys

import numpy as np

import sparc_survey as S

HERE = os.path.dirname(os.path.abspath(__file__))
GAMMA_MAX, MIN_POINTS, NBOOT = 0.10, 4, 2000
MU_LO, MU_HI = 0.05, 0.95
C, MPC = 2.99792458e8, 3.0857e22
GAP = 0.5 - 1 / ((1 + 5 ** 0.5) / 2) ** 2


def mu_from_slope(s, gamma):
    return 2 - (2 - gamma) / (2 - s)


def self_test(L):
    """Synthetic galaxy: exponential disk plus gas, true a0 = 1.2e-10. The method must return it."""
    G, KPC, MSUN = L["G"], L["KPC"], L["MSUN"]
    a0 = 1.2e-10
    r = np.linspace(0.5, 60, 60)
    rm = r * KPC
    M = 3e10 * MSUN * (1 - (1 + r / 3) * np.exp(-r / 3)) + 1e10 * MSUN * (1 - (1 + r / 6) * np.exp(-r / 6))
    gN = G * M / rm ** 2
    g = 0.5 * (gN + np.sqrt(gN ** 2 + 4 * gN * a0))
    v2 = g * rm
    gam = np.gradient(np.log(M), np.log(r))
    sel = gam < GAMMA_MAX
    b = np.polyfit(np.log(r[sel]), np.log(v2[sel]), 1)[0]
    mu = mu_from_slope(1 + b, np.median(gam[sel]))
    rmed = np.median(r[sel])
    gm = np.interp(rmed, r, g)
    return gm / (mu / (1 - mu))


def measure(rot, ups):
    L = S.letter_functions()
    smooth, MSUN, KPC = L["diffraction_smooth"], L["MSUN"], L["KPC"]
    t1 = S.table1()
    out = []
    for x in csv.DictReader(open(os.path.join(HERE, "sparc_survey_results.csv"))):
        if x["flags"] or int(x["quality"]) > 2:
            continue
        n = x["galaxy"]
        lum, rd, mhi, rhi, q = t1[n]
        a = np.loadtxt(os.path.join(rot, f"{n}_rotmod.dat"), comments="#")
        r, v = a[:, 0], a[:, 1]
        m = (r > 0) & (v > 0)
        r, v = r[m], v[m]
        vs = smooth(r, v)
        rm = r * KPC
        Mp = ups * lum * MSUN * (1 - (1 + r / rd) * np.exp(-r / rd)) + \
            1.33 * mhi * MSUN * (1 - (1 + r / (rhi / 3)) * np.exp(-r / (rhi / 3)))
        gam = np.gradient(np.log(Mp), np.log(r))
        sel = gam < GAMMA_MAX
        if sel.sum() < MIN_POINTS:
            continue
        b = np.polyfit(np.log(r[sel]), np.log(vs[sel] ** 2), 1)[0]
        mu = mu_from_slope(1 + b, float(np.median(gam[sel])))
        if not (MU_LO < mu < MU_HI):
            out.append((n, None, b, mu))
            continue
        rmed = float(np.median(r[sel]))
        g = np.interp(rmed, r, vs) ** 2 * 1e6 / (rmed * KPC)
        out.append((n, g / (mu / (1 - mu)), b, mu))
    return out


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    L = S.letter_functions()
    print(f"Self-test on a synthetic galaxy (true a0 = 1.200e-10): recovered {self_test(L):.3e}\n")
    for H in (67.4, 70.0, 73.0):
        a = C * H * 1e3 / MPC / (2 * math.pi)
        print(f"Candidates at H0 = {H}: cH0/2pi = {a:.3e}, x(1 + {GAP:.3f}) = {a * (1 + GAP):.3e}, "
              f"x sqrt(4/pi) = {a * math.sqrt(4 / math.pi):.3e}")
    rng = np.random.default_rng(2026)
    rows = []
    for ups in (0.5, 0.3, 0.7):
        res = measure(sys.argv[1], ups)
        vals = np.array([a_ for _, a_, _, _ in res if a_ is not None])
        nlev = len(res)
        print(f"\nUpsilon = {ups}: {nlev} galaxies with >= {MIN_POINTS} points where the enclosed mass has levelled off; "
              f"{len(vals)} give a value (0.05 < mu < 0.95); "
              f"{sum(1 for _, a_, b, mu in res if a_ is None and mu <= MU_LO)} have flat or rising outer curves (mu <= 0.05)")
        if len(vals) < 15:
            print("   fewer than 15 galaxies: the method fails here")
            continue
        boots = [np.median(rng.choice(vals, len(vals))) for _ in range(NBOOT)]
        lo, hi = np.percentile(boots, [16, 84])
        print(f"   median a0 = {np.median(vals):.3e}  (68% bootstrap interval {lo:.3e} to {hi:.3e}); "
              f"galaxy-to-galaxy 16-84%: {np.percentile(vals, 16):.2e} to {np.percentile(vals, 84):.2e}")
        a70 = C * 70e3 / MPC / (2 * math.pi)
        for lab, val in (("cH0/2pi", a70), ("x(1+0.118)", a70 * (1 + GAP)), ("x sqrt(4/pi)", a70 * math.sqrt(4 / math.pi))):
            print(f"      {lab:13s} {val:.3e}: {'inside' if lo <= val <= hi else 'outside'} the 68% interval")
        if ups == 0.5:
            rows = res
    with open(os.path.join(HERE, "a0_from_slope_results.csv"), "w", newline="") as fo:
        w = csv.writer(fo)
        w.writerow(["galaxy", "a0_ms2", "slope_dlnv2_dlnr", "mu"])
        for n, a_, b, mu in rows:
            w.writerow([n, "" if a_ is None else f"{a_:.4e}", f"{b:.4f}", f"{mu:.4f}"])


if __name__ == "__main__":
    main()
