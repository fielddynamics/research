"""
Exploratory comparison (no pass condition): where does the measured gap Delta(x) change sign?

The roll-ratio theorem puts the quiet throat (delta = 0) at the ring, x = 1: drive inside
(x > 1), drag outside (x < 1). The decode audit (version 2, the letter's pipeline) measures
Delta = log10(M_dec / M_phot) at every radius. Here the median Delta is taken in bins of
log10 x over the quality-cut galaxies, its zero crossing is located, and its uncertainty is
estimated by resampling galaxies (bootstrap, 2000 draws).

The theorem predicts rates, not masses: it gives the sign structure (where drive turns to
drag), not the size of Delta. Only the sign and the crossing are compared.

Usage: python compare_roll_ratio_sparc.py [RESULTS_DIR]
"""
from __future__ import annotations

import csv
import os
import sys

import numpy as np

A0, KPC = 1.2e-10, 3.086e19
HERE = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(2026)
EDGES = np.arange(-1.5, 1.75, 0.25)


def crossing(lx, D):
    """Upward zero crossing of the binned median Delta(log x), interpolated."""
    cen, med = [], []
    for lo, hi in zip(EDGES[:-1], EDGES[1:]):
        s = (lx >= lo) & (lx < hi)
        if s.sum() >= 20:
            cen.append(0.5 * (lo + hi)); med.append(np.median(D[s]))
    cen, med = np.array(cen), np.array(med)
    for i in range(len(med) - 1):
        if med[i] < 0 <= med[i + 1]:
            return cen[i] + (0 - med[i]) * (cen[i + 1] - cen[i]) / (med[i + 1] - med[i]), cen, med
    return np.nan, cen, med


def main(res):
    S = {r["galaxy"]: r for r in csv.DictReader(open(os.path.join(res, "galaxy_summary.csv")))}
    q = {k for k, r in S.items() if int(r["Q"]) in (1, 2) and float(r["inc"]) >= 30 and int(r["n"]) >= 5}
    P = {}
    for r in csv.DictReader(open(os.path.join(res, "profiles.csv"))):
        if r["galaxy"] in q:
            P.setdefault(r["galaxy"], []).append(r)
    gal = sorted(P)
    lx = {g: np.log10((np.array([float(p["v_smooth"]) for p in P[g]]) * 1e3) ** 2
                      / (np.array([float(p["r_kpc"]) for p in P[g]]) * KPC) / A0) for g in gal}
    D = {g: np.array([float(p["Delta_dex"]) for p in P[g]]) for g in gal}
    gas = {g: float(S[g]["gas_share"]) for g in gal}

    for lab, sel in (("all quality-cut", gal), ("not gas-dominated", [g for g in gal if gas[g] < 0.5])):
        X = np.concatenate([lx[g] for g in sel]); Y = np.concatenate([D[g] for g in sel])
        x0, cen, med = crossing(X, Y)
        boot = []
        for _ in range(2000):
            b = rng.choice(len(sel), len(sel))
            bx = np.concatenate([lx[sel[i]] for i in b]); by = np.concatenate([D[sel[i]] for i in b])
            boot.append(crossing(bx, by)[0])
        boot = np.array(boot)
        ok = boot[np.isfinite(boot)]
        lo, hi = np.percentile(ok, [2.5, 97.5])
        print(f"{lab} ({len(sel)} galaxies, {len(X)} points)")
        print("  median Delta by log10 x: " + "  ".join(f"{c:+.2f}:{m:+.3f}" for c, m in zip(cen, med)))
        print(f"  zero crossing of median Delta: log10 x = {x0:+.2f} (x = {10 ** x0:.2f}); "
              f"95% bootstrap interval log10 x [{lo:+.2f}, {hi:+.2f}] (x {10 ** lo:.2f}-{10 ** hi:.2f})")
        print(f"  ring x = 1 inside the interval: {'yes' if lo <= 0 <= hi else 'no'}")
        inside, outside = Y[X > 0], Y[X < 0]
        print(f"  sign structure: median Delta inside the ring (x > 1) {np.median(inside):+.3f} (N={len(inside)}), "
              f"outside (x < 1) {np.median(outside):+.3f} (N={len(outside)})\n")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "decode_audit", "results_paper_mphot"))
