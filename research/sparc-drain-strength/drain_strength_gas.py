#!/usr/bin/env python3
"""
One drain, one strength in gas-dominated SPARC galaxies (method fixed in PREREGISTRATION_GAS.md).

  python drain_strength_gas.py ROTMOD_DIR
"""
import csv
import os
import sys

import numpy as np

from drain_strength import A0, GALAXY_LIST, KMS2_PER_KPC, WIDTH_MAX, fit_D

UPS_BUL = 0.7
UPS_SELECT = 0.5
UPS_TRIALS = (0.3, 0.5, 0.8)


def read(path):
    a = np.loadtxt(path, comments="#")
    return a[:, 0], a[:, 1], a[:, 2], a[:, 3], a[:, 4], a[:, 5]


def gas_dominated(r, vg, vd, vb):
    gas = vg * np.abs(vg)
    stars = UPS_SELECT * vd ** 2 + UPS_BUL * vb ** 2
    m = r > 0
    r, gas, stars = r[m], gas[m], stars[m]
    med = np.median(r)
    inner, outer = r <= med, r > med
    if inner.sum() < 3 or outer.sum() < 3:
        return False
    fi = np.median((gas / np.maximum(gas + stars, 1e-12))[inner])
    fo = np.median((gas / np.maximum(gas + stars, 1e-12))[outer])
    return fi >= 0.5 and fo >= 0.5


def compare(r, vo, ev, vg, vd, vb, ups, floor):
    vbar2 = vg * np.abs(vg) + ups * vd ** 2 + UPS_BUL * vb ** 2
    m = (r > 0) & (vo > 0) & (vbar2 > 0)
    r, vo, ev, vbar2 = r[m], vo[m], ev[m], vbar2[m]
    if len(r) < 6:
        return None
    g = vo ** 2 / r * KMS2_PER_KPC
    gb = vbar2 / r * KMS2_PER_KPC
    sg = 2 * g * np.sqrt(ev ** 2 + (floor * vo) ** 2) / vo
    med = np.median(r)
    i, o = r <= med, r > med
    if i.sum() < 3 or o.sum() < 3:
        return None
    fi, fo = fit_D(g[i], gb[i], sg[i]), fit_D(g[o], gb[o], sg[o])
    if fi[2] - fi[1] >= WIDTH_MAX or fo[2] - fo[1] >= WIDTH_MAX:
        return None
    if min(fi[1], fo[1]) <= -2 or max(fi[2], fo[2]) >= 2:
        return None
    z = (fo[0] - fi[0]) / np.hypot(max((fi[2] - fi[1]) / 2, 1e-3), max((fo[2] - fo[1]) / 2, 1e-3))
    return fi[0], fo[0], z, fit_D(g, gb, sg)[0]


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    d = sys.argv[1]
    names = sorted({row["galaxy"] for row in csv.DictReader(open(GALAXY_LIST))})
    sel = []
    for n in names:
        p = os.path.join(d, f"{n}_rotmod.dat")
        if os.path.exists(p) and gas_dominated(*(lambda a: (a[0], a[3], a[4], a[5]))(read(p))):
            sel.append(n)
    print(f"gas-dominated galaxies (selected from mass models only): {len(sel)}")
    print("   " + ", ".join(sel))
    verdicts = []
    rows = []
    for floor in (0.0, 0.05):
        for ups in UPS_TRIALS:
            res = {n: compare(*read(os.path.join(d, f"{n}_rotmod.dat")), ups, floor) for n in sel}
            res = {n: v for n, v in res.items() if v is not None}
            z = np.array([v[2] for v in res.values()])
            dd = np.array([v[1] - v[0] for v in res.values()])
            lall = np.array([v[3] for v in res.values()])
            label = f"floor {int(floor * 100)}%, Upsilon_disk {ups}"
            if len(z) < 10:
                print(f"\n[{label}] only {len(z)} galaxies measure D in both halves: too small to decide")
                verdicts.append((floor, ups, "too small"))
                continue
            sem = 1.2533 * np.std(z) / np.sqrt(len(z))
            frac = np.mean(np.abs(z) < 2)
            ok = frac >= 0.80 and abs(np.median(z)) <= 3 * sem
            verdicts.append((floor, ups, "SUPPORTS" if ok else "AGAINST"))
            print(f"\n[{label}] both halves measure D: {len(z)}")
            print(f"   |z| < 2: {frac:.2f}   median z = {np.median(z):+.2f} +- {sem:.2f}   "
                  f"median log D_out - log D_in = {np.median(dd):+.2f} dex (16-84%: {np.percentile(dd, 16):+.2f} to {np.percentile(dd, 84):+.2f})")
            print(f"   D_out > D_in in {np.mean(dd > 0):.2f};  one D for the whole curve: median log D = {np.median(lall):+.2f}")
            print(f"   verdict: {verdicts[-1][2]}")
            if floor == 0.05 and ups == 0.5:
                for n, v in sorted(res.items()):
                    rows.append((n, v[0], v[1], v[2], v[3]))
    print("\nPer galaxy (5% floor, Upsilon_disk 0.5): log D_in, log D_out, z, log D (whole curve)")
    for n, a, b, z_, c in rows:
        print(f"   {n:12s} {a:+6.2f} {b:+6.2f} {z_:+6.2f} {c:+6.2f}")
    print("\nPre-registered requirement: SUPPORTS at all three Upsilon_disk with the 5% floor.")
    need = [v for f, u, v in verdicts if f == 0.05]
    print(f"   with the 5% floor: {need}  ->  {'SUPPORTS' if all(v == 'SUPPORTS' for v in need) else 'NOT SUPPORTED'}")


if __name__ == "__main__":
    main()
