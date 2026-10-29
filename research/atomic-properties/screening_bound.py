#!/usr/bin/env python3
"""
Evaluate pre-registration 2 (PREREGISTRATION_bound_screening.md)
================================================================

Rule: electron j screens electron i by the bound-state share
      s_ij = mu_2(r_i / r_j),   mu_2(x) = [(2x+1) - sqrt(4x+1)] / (2x),
the root of x(1-mu)^2 = mu (Papers 11 and XIII). Each Slater group's Z_eff and
radius r = n^2 a0 / Z_eff are solved self-consistently. No fitted parameter.

Pass criteria (fixed in advance):
  1. Z = 1-20:  mean |error| of outermost Z_eff vs Clementi < 10%
  2. Z = 21-36: mean |error| < 10% AND lower than Slater's rules
  3. Spearman rank correlation with Clementi, Z = 1-36, >= 0.95
  4. covalent-radius log-RMS (one scale factor, non-noble, Z = 1-36) below Slater

    python screening_bound.py
"""
import csv
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from baseline_comparison import A0_PM, SLATER_NSTAR, fit_scale, load, log_rms, mape, spearman

NOBLE = {"He", "Ne", "Ar", "Kr"}
AR_CORE = "1s2 2s2 2p6 3s2 3p6"
CONFIG_1_20 = {
    1: "1s1", 2: "1s2", 3: "1s2 2s1", 4: "1s2 2s2", 5: "1s2 2s2 2p1", 6: "1s2 2s2 2p2",
    7: "1s2 2s2 2p3", 8: "1s2 2s2 2p4", 9: "1s2 2s2 2p5", 10: "1s2 2s2 2p6",
    11: "1s2 2s2 2p6 3s1", 12: "1s2 2s2 2p6 3s2", 13: AR_CORE[:15] + " 3p1",
    14: AR_CORE[:15] + " 3p2", 15: AR_CORE[:15] + " 3p3", 16: AR_CORE[:15] + " 3p4",
    17: AR_CORE[:15] + " 3p5", 18: AR_CORE, 19: AR_CORE + " 4s1", 20: AR_CORE + " 4s2",
}


# ---------------------------------------------------------------- data

def load_all():
    rows = []
    for r in load():
        rows.append(dict(Z=r["Z"], symbol=r["symbol"], n=r["n"], zeff=r["zeff_clementi"],
                         r_cov=r["r_covalent_cordero_pm"], config=CONFIG_1_20[r["Z"]]))
    with open(os.path.join(HERE, "data", "atomic_reference_21_36.csv")) as fh:
        for r in csv.DictReader(fh):
            rows.append(dict(Z=int(r["Z"]), symbol=r["symbol"], n=int(r["n"]),
                             zeff=float(r["zeff_clementi"]), r_cov=float(r["r_covalent_cordero_pm"]),
                             config=r["configuration"].replace("[Ar]", AR_CORE)))
    return rows


def groups(config):
    """Slater groups as [(n, kind, count)], kind in {'sp', 'd', 'f'}."""
    g = {}
    for n, l, k in re.findall(r"(\d)([spdf])(\d+)", config):
        key = (int(n), "sp" if l in "sp" else l)
        g[key] = g.get(key, 0) + int(k)
    return [(n, kind, c) for (n, kind), c in sorted(g.items())]


def outer_index(gr):
    return max(i for i, (n, kind, c) in enumerate(gr) if kind == "sp")


# ---------------------------------------------------------------- screening laws

def mu_unbound(x):
    return x / (1.0 + x)


def mu_bound(x):
    return ((2 * x + 1) - math.sqrt(4 * x + 1)) / (2 * x)


def solve(config, Z, law, power=1, iters=2000, tol=1e-12):
    """Self-consistent Z_eff and radius for every group; returns outermost (Z_eff, r)."""
    gr = groups(config)
    zeff = [float(Z)] * len(gr)
    for _ in range(iters):
        r = [n * n * A0_PM / z for (n, _, _), z in zip(gr, zeff)]
        new = []
        for a in range(len(gr)):
            s = 0.0
            for b in range(len(gr)):
                count = gr[b][2] - (1 if a == b else 0)
                if count:
                    s += count * law((r[a] / r[b]) ** power)
            new.append(max(Z - s, 0.05))
        done = max(abs(x - y) for x, y in zip(new, zeff)) < tol
        zeff = [0.5 * x + 0.5 * y for x, y in zip(new, zeff)]
        if done:
            break
    o = outer_index(gr)
    return zeff[o], gr[o][0] ** 2 * A0_PM / zeff[o]


def slater(config, Z):
    gr = groups(config)
    o = outer_index(gr)
    n_out = gr[o][0]
    s = (gr[o][2] - 1) * (0.30 if n_out == 1 else 0.35)
    for i, (n, kind, c) in enumerate(gr):
        if i == o:
            continue
        if n == n_out - 1:
            s += 0.85 * c
        elif n < n_out - 1:
            s += 1.00 * c
    z = Z - s
    return z, SLATER_NSTAR[n_out] ** 2 * A0_PM / z


# ---------------------------------------------------------------- evaluation

def radius_lrms(model_r, obs_r, idx):
    a = [model_r[i] for i in idx]
    b = [obs_r[i] for i in idx]
    k = fit_scale(a, b)
    return log_rms([k * v for v in a], b)


def main():
    rows = load_all()
    N = len(rows)
    sym = [r["symbol"] for r in rows]
    zc = [r["zeff"] for r in rows]
    rcov = [r["r_cov"] for r in rows]
    zb, rb = zip(*(solve(r["config"], r["Z"], mu_bound) for r in rows))
    zb2, rb2 = zip(*(solve(r["config"], r["Z"], mu_bound, power=2) for r in rows))
    za, ra = zip(*(solve(r["config"], r["Z"], mu_unbound) for r in rows))
    zs, rs = zip(*(slater(r["config"], r["Z"]) for r in rows))
    rcl = [r["n"] ** 2 * A0_PM / r["zeff"] for r in rows]

    first = list(range(20))
    second = list(range(20, N))
    nn = [i for i in range(N) if sym[i] not in NOBLE]

    print("=" * 78)
    print("  PRE-REGISTRATION 2: screening s_ij = mu_2(r_i/r_j), bound-state law")
    print("=" * 78)
    print(f"  {'':3} {'Z':>3} {'Clementi':>9} {'bound':>7} {'err%':>6} {'Slater':>7} {'err%':>6}"
          f" {'unbound':>8} {'r bound':>8} {'r cov':>6}")
    for i in range(N):
        if i == 20:
            print("  " + "-" * 74 + "  out of sample below")
        eb = 100 * (zb[i] - zc[i]) / zc[i]
        es = 100 * (zs[i] - zc[i]) / zc[i]
        print(f"  {sym[i]:3} {rows[i]['Z']:3d} {zc[i]:9.3f} {zb[i]:7.3f} {eb:+6.1f} {zs[i]:7.3f} {es:+6.1f}"
              f" {za[i]:8.3f} {rb[i]:8.1f} {rcov[i]:6.0f}")

    pick = lambda v, idx: [v[i] for i in idx]
    c1 = mape(pick(zb, first), pick(zc, first))
    c2 = mape(pick(zb, second), pick(zc, second))
    c2_sl = mape(pick(zs, second), pick(zc, second))
    c3 = spearman(list(zb), zc)
    c4 = radius_lrms(rb, rcov, nn)
    c4_sl = radius_lrms(rs, rcov, nn)

    ok1, ok2, ok3, ok4 = c1 < 10, (c2 < 10 and c2 < c2_sl), c3 >= 0.95, c4 < c4_sl
    v = lambda ok: "PASS" if ok else "FAIL"
    print("\n  Criterion 1  Z = 1-20 mean |error| vs Clementi < 10%")
    print(f"     bound {c1:5.1f}%   (Slater {mape(pick(zs, first), pick(zc, first)):4.1f}%,"
          f" unbound rule {mape(pick(za, first), pick(zc, first)):4.1f}%)   {v(ok1)}")
    print("  Criterion 2  Z = 21-36 mean |error| < 10% and below Slater")
    print(f"     bound {c2:5.1f}%   Slater {c2_sl:4.1f}%   {v(ok2)}")
    print("  Criterion 3  Spearman with Clementi, Z = 1-36, >= 0.95")
    print(f"     bound {c3:5.3f}   {v(ok3)}")
    print("  Criterion 4  covalent-radius log-RMS, non-noble Z = 1-36, below Slater")
    print(f"     bound {c4:5.3f}   Slater {c4_sl:5.3f}   {v(ok4)}")
    passed = ok1 and ok2 and ok3 and ok4
    print(f"\n  OUTCOME: {'PASS (all four criteria)' if passed else 'FAIL'}")

    # ---------------- secondary analyses (pre-registered, not pass/fail)
    print("\n  Secondary (pre-registered, not part of pass/fail)")
    print(f"     B' x = (r_i/r_j)^2: error Z=1-20 {mape(pick(zb2, first), pick(zc, first)):4.1f}%,"
          f" Z=21-36 {mape(pick(zb2, second), pick(zc, second)):4.1f}%,"
          f" radius log-RMS {radius_lrms(rb2, rcov, nn):5.3f}")
    alt = {}
    for label, vals in (("low-spin", {"Mn": 139, "Fe": 132, "Co": 126}),
                        ("high-spin", {"Mn": 161, "Fe": 152, "Co": 150})):
        rc2 = [vals.get(s, x) for s, x in zip(sym, rcov)]
        alt[label] = (radius_lrms(rb, rc2, nn), radius_lrms(rs, rc2, nn))
        print(f"     Mn/Fe/Co {label:9} radii: bound {alt[label][0]:5.3f}   Slater {alt[label][1]:5.3f}")

    print("\n  Context (not pre-registered)")
    print(f"     unbound rule (pre-registration 1) on Z=21-36: {mape(pick(za, second), pick(zc, second)):4.1f}%")
    print(f"     radius log-RMS, non-noble Z=1-36: Clementi Z_eff {radius_lrms(rcl, rcov, nn):5.3f},"
          f" unbound rule {radius_lrms(ra, rcov, nn):5.3f}")
    return dict(c1=c1, c2=c2, c2_slater=c2_sl, c3=c3, c4=c4, c4_slater=c4_sl, passed=passed,
                zb=zb, rb=rb, alt=alt)


if __name__ == "__main__":
    main()
