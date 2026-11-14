"""
Diagnostic D1: does H3 depend on the photometric method?

H3 (CRITERIA.md) correlates the ring share f_in with the net area A of Delta = log10(M_dec/M_phot)
over each galaxy's profile. The decoding-mass letter works in the spherical limit: M_phot becomes an
acceleration as g_bar = G M_phot / r^2, with the Gravis mass model (exponential disks). Here the same
test is rerun with SPARC's own Newtonian g_bar (thin disks, measured HI maps) in its place:
Delta' = log10(mu(x) / mu') with mu' = g_bar,SPARC / g_obs; everything else unchanged (smoothed
g_obs, f_in and the quality cut from the v2 audit).

This is a diagnostic of the letter's declared simplification, not a replacement for its method.
Usage: python diagnostic_d1.py ROTMOD_DIR [RESULTS_DIR]
"""
from __future__ import annotations

import csv
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import decode_audit as da  # noqa: E402
import measured_partition as mp  # noqa: E402


def main(rotmod_dir, res):
    S = {r["galaxy"]: r for r in csv.DictReader(open(os.path.join(res, "galaxy_summary.csv")))}
    D = mp.load(res)
    T = mp.load_thin_disk(D, rotmod_dir)
    R = {}
    for p in csv.DictReader(open(os.path.join(res, "profiles.csv"))):
        R.setdefault(p["galaxy"], []).append(float(p["r_kpc"]))
    rows = []
    for g in sorted(T):
        x = 10 ** T[g]["lx"]
        mu_t, mu_o = x / (1 + x), T[g]["mu"]
        ok = mu_o > 0
        r = np.array(R[g])[ok]
        if len(r) < 3:
            continue
        Ap, Am = da.areas(r, np.log10(mu_t[ok] / mu_o[ok]))
        rows.append((g, float(S[g]["A_net"]), Ap - Am, float(S[g]["f_in"]), float(S[g]["gas_share"])))
    A = np.array([r[1] for r in rows]); At = np.array([r[2] for r in rows])
    fin = np.array([r[3] for r in rows]); gas = np.array([r[4] for r in rows])
    print(f"Diagnostic D1: {len(rows)} quality-cut galaxies")
    for lab, s in (("all", np.ones_like(gas, bool)), ("not gas-dominated", gas < 0.5)):
        r1, r2 = da.spearman(fin[s], A[s]), da.spearman(fin[s], At[s])
        print(f"  {lab:18s} N={s.sum():3d}  H3, letter's g_bar: rho {r1[0]:+.2f} (p {r1[1]:.4f})   "
              f"SPARC g_bar: rho {r2[0]:+.2f} (p {r2[1]:.4f})")
    for lab, s in (("whole galaxy outside the ring (f_in = 0)", fin == 0), ("ring inside the data", (fin > 0) & (fin < 1))):
        print(f"  {lab:42s} N={s.sum():3d}  median A: letter {np.median(A[s]):+.3f}, SPARC g_bar {np.median(At[s]):+.3f}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "results_paper_mphot"))
