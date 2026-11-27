#!/usr/bin/env python3
"""
GP-9  Grand Gallery spectral selection and passive scattering

Independent checks of every number stated in README.md (exact rational section
moments, the analytic parity interval, finite-volume cutoffs and controls, the
array law, conservative reciprocal transfer matrices, the position-independent
slot bound, the endpoint comparison and the scale law), then the 100-case
regression suite in tests/ as one further check.
Prints PASS/FAIL per check and exits non-zero on any failure.

Run from this folder:  python verify_gp9_grand_gallery.py
"""
import re
import subprocess
import sys
from fractions import Fraction as Fr

import numpy as np

from model import (C, CUBIT, L, H_PYRAMID, VIRTUAL_RUN, ZSTAR, area, cutoff, modes, odd_bound,
                   array_factor, duct, shunt, scatter, expansion_power, slot_chain, slots,
                   shunt_reflection_bound)

RESULTS = []


def check(name, ok):
    RESULTS.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")


def close(a, b, tol):
    return abs(a - b) <= tol


# --- Section geometry, exact -------------------------------------------------
edges = [Fr(0), Fr(1), Fr(4)] + [Fr(4) + Fr(11 * j, 7) for j in range(1, 8)]
halfw = [Fr(1), Fr(2)] + [2 - Fr(j, 7) for j in range(1, 8)]
tiers = list(zip(edges, edges[1:], halfw))
A = sum(2 * w * (t - b) for b, t, w in tiers)
M1 = sum(w * (t * t - b * b) for b, t, w in tiers)
M2 = sum(2 * w * (t ** 3 - b ** 3) / 3 for b, t, w in tiers)
X2 = sum(2 * w ** 3 * (t - b) / 3 for b, t, w in tiers)
check("section area A = 318/7 cubit^2 exactly", A == Fr(318, 7) and close(area(), float(A), 1e-12))
check("moments M1 = 15181/49, M2 = 140270/49, X2 = 1990/49 exactly",
      (M1, M2, X2) == (Fr(15181, 49), Fr(140270, 49), Fr(1990, 49)))


def hz(lam_cubit):  # eigenvalue in cubit^-2 -> cutoff in Hz
    return C * np.sqrt(float(lam_cubit)) / (2 * np.pi * CUBIT)


f_even_up = hz(A / (M2 - M1 * M1 / A))
f_odd_up = hz(A / X2)
f_odd_lo = C / (2 * 4 * CUBIT)  # pi^2/W^2 with W = 4 cubits
# the stated 5-decimal values are conservative roundings: upper bounds rounded up, the lower bound down
check("T2 bounds: f_e1 <= 25.64162, 81.81427 <= f_o1 <= 110.17302 Hz (conservatively rounded)",
      25.64161 < f_even_up <= 25.64162 and 81.81427 <= f_odd_lo < 81.81428
      and 110.17301 < f_odd_up <= 110.17302 and close(odd_bound(), f_odd_lo, 1e-12))
kc = {"length": 16.3787, "height": 29.3449, "width": 32.7575}  # GP-7 axial fundamentals
check("T2 window: KC height and width inside (25.64, 81.81) Hz, length below it",
      all(f_even_up < kc[k] < f_odd_lo for k in ("height", "width")) and kc["length"] < f_even_up)

# --- Finite-volume spectra (numerical corroboration) --------------------------
ev = cutoff(modes("stepped", 4, "even")[0])
od = cutoff(modes("stepped", 4, "odd")[0])
check("r=4 cutoffs: first even 23.228 Hz, first odd 88.462 Hz, both inside the T2 bounds",
      close(ev[1], 23.22826, 5e-5) and close(od[0], 88.46169, 5e-5)
      and ev[0] == 0 and ev[1] <= f_even_up and f_odd_lo <= od[0] <= f_odd_up)
sm_e = cutoff(modes("smooth", 4, "even")[0])[1]
sm_o = cutoff(modes("smooth", 4, "odd")[0])[0]
check("smooth equal-area control within 0.2 Hz of the seven steps (first of each parity)",
      abs(sm_e - ev[1]) < 0.2 and abs(sm_o - od[0]) < 0.2)

# --- T3 array law ------------------------------------------------------------
d = 1.67
rng = np.random.default_rng(9)
ok = True
for N in (1, 2, 7, 14, 27, 28):
    k = rng.uniform(-20, 20, 50)
    k = k[np.abs(np.sin(k * d)) > 1e-6]
    closed = np.exp(1j * (N - 1) * k * d) * np.sin(N * k * d) / np.sin(k * d)
    ok = ok and np.allclose(closed, array_factor(k, np.arange(N) * d), atol=1e-10)
check("T3 F(k) = e^{i(N-1)kd} sin(Nkd)/sin(kd) against the direct sum (N = 1..28)", ok)
a, b = 0.521, 0.592
ok = True
for N in (2, 14, 27, 28):
    w = np.where(np.arange(N) % 2, b, a)
    M, odd = N // 2, N % 2
    half = (M + 1) * a - M * b if odd else M * (a - b)
    full = (M + 1) * a + M * b if odd else M * (a + b)
    p = np.arange(N) * d
    ok = ok and close(array_factor(np.pi / (2 * d), p, w), half, 1e-12) and close(array_factor(np.pi / d, p, w), full, 1e-12)
check("T3 alternating superperiod: M(a-b), M(a+b) and the odd-N forms", ok)
fB = C / (2 * d)
check("Bragg 102.69461 Hz, half order 51.34731 Hz; five even and one odd mode already below it",
      close(fB, 102.69461, 5e-6) and close(fB / 2, 51.34731, 5e-6)
      and (ev < fB).sum() >= 5 and (od < fB).sum() >= 1)

# --- T4 reciprocal conservative network ---------------------------------------
J = np.array([[0, 1], [1, 0]])
ok = True
for _ in range(200):
    T = np.eye(2, dtype=complex)
    for _ in range(6):
        f = rng.uniform(.1, 30)
        T = T @ duct(f, rng.uniform(.1, 10), rng.uniform(.3, 15)) @ shunt(f, rng.uniform(0, .05))
    S = scatter(T, rng.uniform(.3, 3), rng.uniform(.3, 3))
    ok = ok and np.allclose(T.conj().T @ J @ T, J, atol=1e-9) and close(np.linalg.det(T), 1, 1e-9) \
        and np.allclose(S, S.T, atol=1e-9) and np.allclose(S.conj().T @ S, np.eye(2), atol=1e-9)
check("T4 200 random cascades: det 1, flux-preserving, S symmetric and unitary", ok)
ok = all(close(abs(scatter(duct(f, L, m), 1, 1)[1, 0]) ** 2, expansion_power(f, L, m), 1e-12)
         for m in (.2, 3, 12.4) for f in np.linspace(0, 20, 41))
check("T4 expansion chamber T = 1/(1 + (m - 1/m)^2 sin^2(kl)/4)", ok)
check("C4 88-cubit comb: spacing 3.718831 Hz, round trip 0.268902 s",
      close(C / (2 * L), 3.718831, 5e-7) and close(2 * L / C, 0.268902, 5e-7))

# --- T5 slot reflection bound -------------------------------------------------
Ag = area() * CUBIT ** 2
_, V = slots()
R20 = shunt_reflection_bound(20, Ag, V)
check("T5 gallery area 12.4761 m^2, slot proxy 0.755496 m^3, bound at 20 Hz = 1.23039e-4",
      close(Ag, 12.4761, 5e-5) and close(V.sum(), 0.755496, 5e-7) and close(R20, 1.23039e-4, 5e-10)
      and R20 <= (2 * np.pi * 20 / C * V.sum() / (2 * Ag)) ** 2)
ok = True
for f in (1, 5, 10, 20, 60, 100):
    for _ in range(20):
        p = np.sort(rng.uniform(0, L, len(V)))
        ok = ok and abs(scatter(slot_chain(f, Ag, L, p, V), Ag, Ag)[0, 0]) ** 2 <= shunt_reflection_bound(f, Ag, V) + 1e-12
    ok = ok and close(abs(scatter(shunt(f, V[0]), Ag, Ag)[0, 0]) ** 2, shunt_reflection_bound(f, Ag, V[:1]), 1e-13)
check("T5 120 random slot positions never exceed the bound; one shunt attains it", ok)

# --- T6 endpoints and scaling -------------------------------------------------
gp1 = 5776 * (1 - 1 / np.sqrt(2))
check("T6 virtual run - GP-1 = -2.85123 in; floor - run = 3.65 in; allowance +/-2.05 in",
      close(gp1, 1691.75123, 5e-6) and close(1688.9 - gp1, -2.85123, 5e-6)
      and close(1692.55 - 1688.9, 3.65, 1e-9) and close(7 * (1 - 1 / np.sqrt(2)), 2.05, 1e-3)
      and close((VIRTUAL_RUN - ZSTAR) / .0254, -2.85123, 5e-6))
ok = True
for s in (0.1, 2.0, 10.0):
    lam = float(A / X2)
    ok = ok and close(C * np.sqrt(lam / s ** 2) / (2 * np.pi * CUBIT), hz(lam) / s, 1e-9)
    ok = ok and close((H_PYRAMID * s - H_PYRAMID * s * (1 - 1 / np.sqrt(2))) / (H_PYRAMID * s), 1 / np.sqrt(2), 1e-12)
    # kV/A invariant: V ~ s^3, A ~ s^2, k ~ 1/s at corresponding frequency
    ok = ok and close((2 * np.pi * 20 / s / C) * (V.sum() * s ** 3) / (Ag * s ** 2), 2 * np.pi * 20 / C * V.sum() / Ag, 1e-12)
check("T6 dilation: cutoffs divide by b, balance fraction fixed, kV/A invariant", ok)

# --- Regression suite ---------------------------------------------------------
proc = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"], capture_output=True, text=True)
m = re.search(r"(\d+) passed", proc.stdout)
npass = int(m.group(1)) if m else 0
check(f"regression suite tests/: {npass} pytest cases passed, none failed", proc.returncode == 0 and npass == 100)

print("\n" + "=" * 78)
print(f"GP-9: {sum(RESULTS)}/{len(RESULTS)} checks passed")
sys.exit(0 if all(RESULTS) else 1)
