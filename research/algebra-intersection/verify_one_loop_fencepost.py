"""
verify_one_loop_fencepost.py
============================

Part VII of INTERSECTION_ALGEBRA.md: where the 2 pi of the one-loop factor
can come from, using only definitions already in the archive.

  Paper VII:  f_closure = c / r_e,  f_Compton = m_e c^2 / h  =>  f_closure / f_Compton = 2 pi / alpha
  read_sweep_synthesis.md:  one rotation of the read = one Compton period

So alpha/(2 pi) = r_e / lambda_C = f_Compton / f_closure = 1/N, with N = 2 pi / alpha
closures per rotation, and the one-loop factor 1 + alpha/2pi = (N + 1)/N.

The archive uses three different completions of that factor. They agree at
first order and differ at second order by about 1-2 ppm, which is a
prediction-shaped difference, not yet testable at G's 22 ppm.
"""
from __future__ import annotations

import math

RESULTS = []


def check(name, cond):
    RESULTS.append((name, bool(cond)))
    print(f"[{'PASS' if cond else 'FAIL'}] {name}")


# CODATA 2018 (the archive's look_elsewhere_G.py and synthesis notes use these)
ALPHA = 7.2973525693e-3
HBAR = 1.054571817e-34
H = 2 * math.pi * HBAR
C = 299792458.0
M_E = 9.1093837015e-31
A_E = 1.15965218128e-3            # electron anomaly, CODATA 2018
G_MEAS, G_UNC = 6.67430e-11, 0.00015e-11

lam_bar = HBAR / (M_E * C)
lam_C = H / (M_E * C)
r_e = ALPHA * lam_bar
N = 2 * math.pi / ALPHA

print("\n=== P1. The identity ===")
check("f_closure / f_Compton = (c/r_e) / (m_e c^2/h) = 2 pi / alpha  (Paper VII)",
      abs((C / r_e) / (M_E * C ** 2 / H) - 2 * math.pi / ALPHA) / (2 * math.pi / ALPHA) < 1e-12)
check("alpha / 2pi = r_e / lambda_C = f_Compton / f_closure = 1/N exactly", abs(ALPHA / (2 * math.pi) - r_e / lam_C) < 1e-18
      and abs(ALPHA / (2 * math.pi) - 1 / N) < 1e-18)
print(f"      N = 2 pi / alpha = {N:.3f} closures per Compton rotation")
check("So 1 + alpha/2pi = (N + 1)/N = (lambda_C + r_e)/lambda_C: one rotation of N closures read at N + 1 boundaries",
      abs((1 + ALPHA / (2 * math.pi)) - (N + 1) / N) < 1e-15 and abs((1 + ALPHA / (2 * math.pi)) - (lam_C + r_e) / lam_C) < 1e-15)

print("\n=== P2. Three completions used in the archive, and their spread ===")
tree = 17 / 13 * ALPHA ** 21 * HBAR * C / M_E ** 2
completions = {
    "(N+1)/N = 1 + alpha/2pi exactly (fencepost; g_from_topology)": (N + 1) / N,
    "g_e/2 = 1 + a_e (full QED anomaly; pyramid python/gravity.py)": 1 + A_E,
    "N/(N-1) = 1/(1 - alpha/2pi) (fencepost counted the other way)": N / (N - 1),
}
vals = {}
for nm, fac in completions.items():
    g = tree * fac
    vals[nm] = g
    print(f"      {nm:70s} G = {g:.7e}   {1e6 * (g - G_MEAS) / G_MEAS:+7.2f} ppm   z = {(g - G_MEAS) / G_UNC:+.2f}")
spread = (max(vals.values()) - min(vals.values())) / G_MEAS
check(f"All three lie within CODATA's 22 ppm; they differ from each other by {1e6 * spread:.2f} ppm", spread < 4e-6
      and all(abs(v - G_MEAS) < G_UNC for v in vals.values()))
d_qed = (1 + A_E) - (N + 1) / N
check(f"The archive's two 'one-loop' factors differ at second order: g_e/2 - (1 + alpha/2pi) = {d_qed:.3e}"
      f" = {d_qed / (ALPHA / math.pi) ** 2:.4f} (alpha/pi)^2: the QED two- and three-loop terms -0.32848 + 1.18124 (alpha/pi)",
      abs(d_qed / (ALPHA / math.pi) ** 2 - (-0.328478965 + 1.181241456 * ALPHA / math.pi)) < 2e-4)
check("A G measurement at ~1 ppm would separate the fencepost (no alpha^2 term) from the QED reading (-0.328 (alpha/pi)^2)",
      abs(vals[list(vals)[0]] - vals[list(vals)[1]]) / G_MEAS > 1.5e-6)

n_pass = sum(1 for _, ok in RESULTS if ok)
print(f"\n{n_pass}/{len(RESULTS)} checks passed")
if __name__ == "__main__":
    raise SystemExit(0 if n_pass == len(RESULTS) else 1)
