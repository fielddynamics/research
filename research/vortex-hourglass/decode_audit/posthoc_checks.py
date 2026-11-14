"""
Post-hoc checks on H3 (run after the pre-registered result; no pass conditions were fixed).

Question: is the ring-share / drive correlation a galaxy-level effect, or the same
acceleration-dependent gap Delta(x) in every galaxy (which a mismatch between mu(x) and
the data's g_bar-g_obs relation, a global M/L error or the gas estimate would also produce)?

  P1  Delta binned by x = g_obs/a0 over all points of the quality-cut galaxies.
  P2  Remove the shared trend: A_resid = area of (Delta - median Delta(x)); re-test against f_in.
  P3  Decode with McGaugh et al. (2016)'s empirical RAR, g_obs = g_bar / (1 - exp(-sqrt(g_bar/a0))),
      instead of mu(x) = x/(x+1); re-test.

Usage: python posthoc_checks.py RESULTS_DIR
"""
from __future__ import annotations

import csv
import os
import sys

import numpy as np
from scipy.optimize import brentq

A0, G, KPC, MSUN = 1.2e-10, 6.674e-11, 3.086e19, 1.989e30
rng = np.random.default_rng(2026)


def spearman(a, b, n_perm=20000):
    ra, rb = np.argsort(np.argsort(a)), np.argsort(np.argsort(b))
    rho = np.corrcoef(ra, rb)[0, 1]
    perm = np.array([np.corrcoef(ra, rng.permutation(rb))[0, 1] for _ in range(n_perm)])
    return float(rho), float((np.sum(perm >= rho) + 1) / (n_perm + 1))


def net_area(R, D):
    lr = np.log(R)
    return float(np.sum(0.5 * (D[1:] + D[:-1]) * np.diff(lr)) / (lr[-1] - lr[0]))


def gbar_mcgaugh(gobs):
    f = lambda gb: gb / (1 - np.exp(-np.sqrt(gb / A0))) - gobs
    return brentq(f, 1e-20, gobs * 1.0000001)


def main(res):
    S = {r["galaxy"]: r for r in csv.DictReader(open(os.path.join(res, "galaxy_summary.csv")))}
    q = {k for k, r in S.items() if int(r["Q"]) in (1, 2) and float(r["inc"]) >= 30 and int(r["n"]) >= 5}
    P = {}
    for r in csv.DictReader(open(os.path.join(res, "profiles.csv"))):
        if r["galaxy"] in q:
            P.setdefault(r["galaxy"], []).append(r)
    arr = lambda g, k: np.array([float(p[k]) for p in P[g]])

    # P1
    X = np.concatenate([(arr(g, "v_smooth") * 1e3) ** 2 / (arr(g, "r_kpc") * KPC) / A0 for g in P])
    D = np.concatenate([arr(g, "Delta_dex") for g in P])
    edges = np.array([-2.5, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 2.0])
    print("P1  median Delta (dex) by x = g_obs/a0, all points of the quality-cut galaxies")
    centres, meds = [], []
    for lo, hi in zip(edges[:-1], edges[1:]):
        s = (np.log10(X) >= lo) & (np.log10(X) < hi)
        if s.sum() >= 20:
            centres.append(0.5 * (lo + hi)); meds.append(np.median(D[s]))
            print(f"    log10 x in [{lo:+.1f}, {hi:+.1f}): N = {s.sum():4d}  median Delta {np.median(D[s]):+.3f}"
                  f"  (16-84%: {np.percentile(D[s], 16):+.2f} .. {np.percentile(D[s], 84):+.2f})")
    rho_x, p_x = spearman(np.log10(X), D, n_perm=2000)
    print(f"    point-level rho(log x, Delta) = {rho_x:+.2f} (p = {p_x:.4f})")
    trend = lambda x: np.interp(np.log10(x), centres, meds)

    fin = np.array([float(S[g]["f_in"]) for g in P])
    gas = np.array([float(S[g]["gas_share"]) for g in P])
    A = np.array([float(S[g]["A_net"]) for g in P])

    # P2
    Ar = np.array([net_area(arr(g, "r_kpc"), arr(g, "Delta_dex")
                            - trend((arr(g, "v_smooth") * 1e3) ** 2 / (arr(g, "r_kpc") * KPC) / A0)) for g in P])
    print("\nP2  shared trend removed: area of (Delta - median Delta(x))")
    for lab, s in (("all quality-cut", np.ones_like(gas, bool)), ("not gas-dominated", gas < 0.5)):
        print(f"    {lab:18s} N = {s.sum():3d}  rho(f_in, A) = {spearman(fin[s], A[s])[0]:+.2f}   "
              f"rho(f_in, A_resid) = {spearman(fin[s], Ar[s])[0]:+.2f} (p = {spearman(fin[s], Ar[s])[1]:.4f})")
    print(f"    galaxy-to-galaxy scatter of A: {np.std(A):.3f} dex; of A_resid: {np.std(Ar):.3f} dex")

    # P3
    Am = []
    for g in P:
        R, v = arr(g, "r_kpc"), arr(g, "v_smooth") * 1e3
        gobs = v ** 2 / (R * KPC)
        Md = np.array([gbar_mcgaugh(x) for x in gobs]) * (R * KPC) ** 2 / G / MSUN
        Am.append(net_area(R, np.log10(Md / arr(g, "M_phot"))))
    Am = np.array(Am)
    Dm = np.concatenate([np.log10(np.array([gbar_mcgaugh(x) for x in (arr(g, "v_smooth") * 1e3) ** 2 / (arr(g, "r_kpc") * KPC)])
                                  * (arr(g, "r_kpc") * KPC) ** 2 / G / MSUN / arr(g, "M_phot")) for g in P])
    print("\nP3  decoded with McGaugh et al. (2016)'s empirical RAR instead of mu(x) = x/(x+1)")
    print(f"    point-level rho(log x, Delta) = {spearman(np.log10(X), Dm, n_perm=2000)[0]:+.2f}")
    for lab, s in (("all quality-cut", np.ones_like(gas, bool)), ("not gas-dominated", gas < 0.5)):
        rho, p = spearman(fin[s], Am[s])
        print(f"    {lab:18s} N = {s.sum():3d}  rho(f_in, A) = {rho:+.2f} (p = {p:.4f})   median A {np.median(Am[s]):+.3f}")


if __name__ == "__main__":
    main(sys.argv[1])
