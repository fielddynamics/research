#!/usr/bin/env python3
"""
Evaluate the pre-registered screening rule (PREREGISTRATION_screening.md)
=========================================================================

Rule: electron j screens electron i by s_ij = mu(r_i/r_j) = r_i/(r_i + r_j),
with each shell's Z_eff and radius r = n^2 a0 / Z_eff solved self-consistently.
No fitted parameter. s and p of one principal shell form one group.

Pass criteria (fixed in advance):
  1. mean |error| of outermost Z_eff vs Clementi < 10%
  2. covalent-radius log-RMS (one scale factor, non-noble) below Slater n* (0.272)
  3. Spearman rank correlation with Clementi Z_eff >= 0.95

    python screening_from_mu.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from baseline_comparison import (A0_PM, SLATER_NSTAR, fit_scale, load, log_rms,
                                 mape, slater_zeff, spearman)


def shells_for(Z):
    """Occupation of principal shells 1..4 for Z = 1-20 (s+p grouped)."""
    caps = [2, 8, 8, 2]
    occ, left = [], Z
    for cap in caps:
        k = min(cap, left)
        if k == 0:
            break
        occ.append(k)
        left -= k
    return occ                                  # occ[a] electrons in shell n = a+1


def solve_mu_screening(Z, iters=500, tol=1e-12):
    occ = shells_for(Z)
    ns = [a + 1 for a in range(len(occ))]
    zeff = [float(Z)] * len(occ)
    for _ in range(iters):
        r = [n * n * A0_PM / z for n, z in zip(ns, zeff)]
        new = []
        for a in range(len(occ)):
            s = 0.0
            for b in range(len(occ)):
                count = occ[b] - (1 if b == a else 0)     # exclude the electron itself
                s += count * r[a] / (r[a] + r[b])
            new.append(max(Z - s, 0.05))
        if max(abs(x - y) for x, y in zip(new, zeff)) < tol:
            zeff = new
            break
        zeff = [0.5 * x + 0.5 * y for x, y in zip(new, zeff)]   # damped iteration
    r = [n * n * A0_PM / z for n, z in zip(ns, zeff)]
    return zeff[-1], r[-1]


def main():
    rows = load()
    sym = [r["symbol"] for r in rows]
    z_cl = [r["zeff_clementi"] for r in rows]
    r_cov = [r["r_covalent_cordero_pm"] for r in rows]
    z_mu, r_mu = zip(*(solve_mu_screening(r["Z"]) for r in rows))
    z_sl = [slater_zeff(r["Z"]) for r in rows]
    r_sl = [SLATER_NSTAR[r["n"]] ** 2 * A0_PM / z for r, z in zip(rows, z_sl)]

    print("=" * 74)
    print("  PRE-REGISTERED TEST: screening s_ij = r_i / (r_i + r_j)  (no fitted parameter)")
    print("=" * 74)
    print(f"  {'':3} {'Z_eff Clementi':>14} {'Z_eff mu-rule':>13} {'Z_eff Slater':>12} {'r mu-rule':>10} {'r covalent':>10}")
    for i in range(len(rows)):
        print(f"  {sym[i]:3} {z_cl[i]:14.3f} {z_mu[i]:13.3f} {z_sl[i]:12.3f} {r_mu[i]:10.1f} {r_cov[i]:10.0f}")

    c1 = mape(z_mu, z_cl)
    nn = [i for i in range(len(rows)) if sym[i] not in ("He", "Ne", "Ar")]
    rm, rs, rc = [r_mu[i] for i in nn], [r_sl[i] for i in nn], [r_cov[i] for i in nn]
    c2 = log_rms([fit_scale(rm, rc) * v for v in rm], rc)
    c2_sl = log_rms([fit_scale(rs, rc) * v for v in rs], rc)
    c3 = spearman(list(z_mu), z_cl)

    print("\n  Criterion 1: mean |error| vs Clementi Z_eff < 10%")
    print(f"     mu-rule {c1:5.1f}%    (Slater's rules {mape(z_sl, z_cl):5.1f}%)   {'PASS' if c1 < 10 else 'FAIL'}")
    print("  Criterion 2: covalent-radius log-RMS below Slater n* (non-noble)")
    print(f"     mu-rule {c2:5.3f}    Slater {c2_sl:5.3f}   {'PASS' if c2 < c2_sl else 'FAIL'}")
    print("  Criterion 3: Spearman rank correlation with Clementi Z_eff >= 0.95")
    print(f"     mu-rule {c3:5.3f}   {'PASS' if c3 >= 0.95 else 'FAIL'}")
    passed = c1 < 10 and c2 < c2_sl and c3 >= 0.95
    print(f"\n  OUTCOME: {'PASS (all three criteria)' if passed else 'FAIL'}")

    # Secondary analysis (not pre-registered): is the radius result robust?
    import random
    r_cl = [r["n"] ** 2 * A0_PM / r["zeff_clementi"] for r in rows]
    def lr(model, idx):
        a = [model[i] for i in idx]; b = [r_cov[i] for i in idx]
        return log_rms([fit_scale(a, b) * v for v in a], b)
    random.seed(1)
    n_boot, beat_cl, beat_sl = 10000, 0, 0
    for _ in range(n_boot):
        idx = [random.choice(nn) for _ in nn]
        m = lr(r_mu, idx)
        beat_cl += m < lr(r_cl, idx)
        beat_sl += m < lr(r_sl, idx)
    print("\n  Secondary analysis (not pre-registered): covalent-radius log-RMS, non-noble")
    print(f"     mu-rule {c2:5.3f}   Clementi Z_eff {lr(r_cl, nn):5.3f}   Slater {c2_sl:5.3f}")
    print(f"     bootstrap ({n_boot} resamples): mu-rule lower than Clementi-based in "
          f"{100*beat_cl/n_boot:.1f}%, lower than Slater in {100*beat_sl/n_boot:.1f}%")
    return dict(c1=c1, c2=c2, c2_slater=c2_sl, c3=c3, passed=passed, z_mu=z_mu, r_mu=r_mu)


if __name__ == "__main__":
    main()
