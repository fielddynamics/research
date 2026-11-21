#!/usr/bin/env python3
"""
One drain, one strength: is TetB's pull w = D a0 the same in the inner and outer halves of each
SPARC rotation curve?  Method fixed in PREREGISTRATION.md.

  python drain_strength.py ROTMOD_DIR      (writes drain_strength_results.csv, prints the summary)

ROTMOD_DIR holds SPARC's Rotmod_LTG files (Lelli et al. 2016), e.g. a copy from
github.com/Cisneros-Galaxy/RCFM, data/Sparc/Rotmod_LTG/.
"""
import csv
import os
import sys

import numpy as np

KMS2_PER_KPC = 1.0e6 / 3.0857e19     # (km/s)^2/kpc -> m/s^2
A0 = 1.2e-10
UPS_DISK, UPS_BUL = 0.5, 0.7
GALAXY_LIST = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "../../papers/letter-radial-acceleration-relation-sparc/supplementary/sparc_rar.csv")
LOGD = np.linspace(-2, 2, 4001)      # D from 0.01 to 100
WIDTH_MAX = 0.6                      # dex: a half "measures D" if its 1-sigma range is narrower


def load(path):
    a = np.loadtxt(path, comments="#")
    r, vo, ev, vg, vd, vb = a[:, 0], a[:, 1], a[:, 2], a[:, 3], a[:, 4], a[:, 5]
    vbar2 = vg * np.abs(vg) + UPS_DISK * vd ** 2 + UPS_BUL * vb ** 2
    m = (r > 0) & (vo > 0) & (vbar2 > 0)
    r, vo, ev, vbar2 = r[m], vo[m], ev[m], vbar2[m]
    g = vo ** 2 / r * KMS2_PER_KPC
    gb = vbar2 / r * KMS2_PER_KPC
    return r, vo, ev, g, gb


def law(gb, w):
    return 0.5 * (gb + np.sqrt(gb * gb + 4 * gb * w))


def fit_D(g, gb, sg):
    chi = np.array([np.sum(((g - law(gb, 10 ** ld * A0)) / sg) ** 2) for ld in LOGD])
    i = int(np.argmin(chi))
    ok = LOGD[chi <= chi[i] + 1.0]
    lo, hi = ok.min(), ok.max()
    return LOGD[i], lo, hi, chi[i], len(g)


def run(rotmod_dir, floor=0.0):
    names = sorted({row["galaxy"] for row in csv.DictReader(open(GALAXY_LIST))})
    rows = []
    for n in names:
        p = os.path.join(rotmod_dir, f"{n}_rotmod.dat")
        if not os.path.exists(p):
            continue
        r, vo, ev, g, gb = load(p)
        if len(r) < 6:
            continue
        sv = np.sqrt(ev ** 2 + (floor * vo) ** 2)
        sg = 2 * g * sv / vo
        med = np.median(r)
        inner, outer = r <= med, r > med
        if inner.sum() < 3 or outer.sum() < 3:
            continue
        fi = fit_D(g[inner], gb[inner], sg[inner])
        fo = fit_D(g[outer], gb[outer], sg[outer])
        fa = fit_D(g, gb, sg)
        rows.append({"galaxy": n, "n": len(r), "x_in_median": float(np.median(g[inner]) / A0),
                     "x_out_median": float(np.median(g[outer]) / A0),
                     "logD_in": fi[0], "lo_in": fi[1], "hi_in": fi[2],
                     "logD_out": fo[0], "lo_out": fo[1], "hi_out": fo[2],
                     "logD_all": fa[0], "chi2_all": fa[3], "chi2_split": fi[3] + fo[3]})
    return rows


def summarise(rows, label):
    meas = [r_ for r_ in rows if (r_["hi_in"] - r_["lo_in"]) < WIDTH_MAX and (r_["hi_out"] - r_["lo_out"]) < WIDTH_MAX
            and r_["lo_in"] > -2 and r_["hi_in"] < 2 and r_["lo_out"] > -2 and r_["hi_out"] < 2]
    z = []
    for r_ in meas:
        si = (r_["hi_in"] - r_["lo_in"]) / 2
        so = (r_["hi_out"] - r_["lo_out"]) / 2
        z.append((r_["logD_out"] - r_["logD_in"]) / np.hypot(max(si, 1e-3), max(so, 1e-3)))
    z = np.array(z)
    print(f"\n[{label}] galaxies fitted: {len(rows)}; both halves measure D: {len(meas)}")
    if len(z) == 0:
        return meas, z
    sem = 1.2533 * np.std(z) / np.sqrt(len(z))
    print(f"   |z| < 2: {np.mean(np.abs(z) < 2):.2f}   |z| > 2: {np.mean(np.abs(z) > 2):.2f}   "
          f"median z = {np.median(z):+.2f} +- {sem:.2f}")
    d = np.array([r_["logD_out"] - r_["logD_in"] for r_ in meas])
    print(f"   log D_out - log D_in: median {np.median(d):+.2f} dex, 16-84%: {np.percentile(d, 16):+.2f} to {np.percentile(d, 84):+.2f}")
    print(f"   D_out > D_in in {np.mean(d > 0):.2f} of them")
    lall = np.array([r_["logD_all"] for r_ in meas])
    print(f"   one D for the whole curve: median log D = {np.median(lall):+.2f} "
          f"(quiet = 0), 16-84%: {np.percentile(lall, 16):+.2f} to {np.percentile(lall, 84):+.2f}")
    ok = (np.abs(z) < 2).mean() >= 0.80 and abs(np.median(z)) <= 3 * sem
    print(f"   pre-registered verdict: {'SUPPORTS' if ok else 'AGAINST'} one drain, one strength")
    return meas, z


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    rows = run(sys.argv[1])
    meas, z = summarise(rows, "errV only")
    with open("drain_strength_results.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r_ in rows:
            w.writerow({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r_.items()})
    rows5 = run(sys.argv[1], floor=0.05)
    summarise(rows5, "errV + 5% floor")


if __name__ == "__main__":
    main()
