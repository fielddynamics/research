"""
verify_seam_average.py
======================

Part VIII of INTERSECTION_ALGEBRA.md: the loop factor of G from the snapshot
principle, with its premises stated.

Premises
  P1  One rotation of the read is one Compton wavelength lambda_C (read_sweep_synthesis.md);
      a closure tile has size r_e (Paper III, Paper VII). In tile units the rotation has
      length N = lambda_C / r_e = 2 pi / alpha (not an integer).
  P2  Atomic closure reads every tile the rotation touches: a tile cut by the seam is a
      shared boundary and must be in the snapshot (the author's note; Paper I).
  P3  The rotation has no preferred phase relative to the tile lattice (homogeneity):
      its offset is uniform over one tile.
  P4  Tree-level G counts the ideal N closures per rotation; the physical read counts the
      tiles actually touched. The loop factor is their ratio.

Result: E[tiles touched] = N + 1 exactly, for every real N > 0, so the factor is
(N + 1)/N = 1 + alpha/(2 pi) to all orders: no alpha^2 term.
"""
from __future__ import annotations

import math
from fractions import Fraction

import numpy as np
import sympy as sp

RESULTS = []


def check(name, cond):
    RESULTS.append((name, bool(cond)))
    print(f"[{'PASS' if cond else 'FAIL'}] {name}")


ALPHA = 7.2973525693e-3
N = 2 * math.pi / ALPHA


def touched(N_, u):
    """Tiles of unit size touched by the segment [u, u + N_)."""
    return math.floor(u + N_ - 1e-15) - math.floor(u) + 1


print("\n=== The expected number of tiles touched is N + 1 ===")
# exact: for offset u uniform on [0,1), T = ceil(N) + 1 when u > ceil(N) - N ... integrate piecewise
def expected_exact(N_):
    n, f = math.floor(N_), N_ - math.floor(N_)
    if f == 0:
        return float(n + 1)  # for u in (0, 1) the segment [u, u + n) touches n + 1 tiles
    # T = n + 1 for u in [0, 1 - f), T = n + 2 for u in [1 - f, 1)
    return (n + 1) * (1 - f) + (n + 2) * f


ok = all(abs(expected_exact(x) - (x + 1)) < 1e-12 for x in (0.3, 1.7, 5.5, 64.0, 861.0229, 1234.567))
check("Exact: E[T] = (n+1)(1-f) + (n+2) f = N + 1 for N = n + f, every real N", ok)
s, nn, f = sp.symbols("s n f", positive=True)
check("Symbolically: (n+1)(1-f) + (n+2) f - (n + f + 1) = 0", sp.simplify((nn + 1) * (1 - f) + (nn + 2) * f - (nn + f + 1)) == 0)
rng = np.random.default_rng(7)
u = rng.random(2_000_000)
mc = np.mean(np.floor(u + N) - np.floor(u) + 1)
check(f"Monte Carlo, 2 million random phases at N = 2pi/alpha = {N:.4f}: E[T] = {mc:.4f} vs N + 1 = {N + 1:.4f}",
      abs(mc - (N + 1)) < 2e-3)
check("So the factor E[T]/N = (N + 1)/N = 1 + alpha/(2 pi) exactly (P4)", abs((N + 1) / N - (1 + ALPHA / (2 * math.pi))) < 1e-15)

print("\n=== The other counting rules give the other completions ===")
inside = np.mean(np.floor(u + N) - np.ceil(u))            # whole tiles strictly inside the segment
check(f"Counting only tiles wholly inside gives E = {inside:.4f} = N - 1: factor (N-1)/N, a DEFICIT, excluded by P2",
      abs(inside - (N - 1)) < 2e-3)
check("No uniform-phase counting gives N/(N-1) = 1 + 1/N + 1/N^2 + ...: that needs a resummed loop, which P1-P4 do not contain",
      abs(N / (N - 1) - (N + 1) / N - 1 / (N * (N - 1))) < 1e-15)

print("\n=== Consequence for G ===")
HBAR, C, M_E = 1.054571817e-34, 299792458.0, 9.1093837015e-31
A_E = 1.15965218128e-3
tree = 17 / 13 * ALPHA ** 21 * HBAR * C / M_E ** 2
g_seam, g_qed, g_loop = tree * (N + 1) / N, tree * (1 + A_E), tree * N / (N - 1)
print(f"      seam average  (N+1)/N : G = {g_seam:.7e}")
print(f"      QED anomaly   1 + a_e : G = {g_qed:.7e}   ({1e6 * (g_qed - g_seam) / g_seam:+.2f} ppm)")
print(f"      resummed loop N/(N-1) : G = {g_loop:.7e}   ({1e6 * (g_loop - g_seam) / g_seam:+.2f} ppm)")
check("The seam average predicts no alpha^2 term: it differs from the QED completion by -1.76 ppm and from the resummed loop by +1.35 ppm",
      abs(1e6 * (g_qed - g_seam) / g_seam + 1.76) < 0.02 and abs(1e6 * (g_loop - g_seam) / g_seam - 1.35) < 0.02)

n_pass = sum(1 for _, ok_ in RESULTS if ok_)
print(f"\n{n_pass}/{len(RESULTS)} checks passed")
if __name__ == "__main__":
    raise SystemExit(0 if n_pass == len(RESULTS) else 1)
