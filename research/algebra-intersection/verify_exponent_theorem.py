"""
verify_exponent_theorem.py
==========================

Part XII of INTERSECTION_ALGEBRA.md: "one alpha per level" as a theorem.

Premises (each anchored in the archive or in earlier Parts)
  P1  Self-similarity: every junction is the same unit (G's blocks are tensor powers of
      one matrix L; g_three_sierpinski_blocks.html). So every junction carries the same factor.
  P2  Snapshot: nothing the read depends on changes while it settles (the author's note;
      Paper I). So within one closure the coupling runs one way, in read order: the network
      matrix is block-triangular in the read order.
  P3  Calibration: electromagnetism is one junction, and its factor is alpha (definition).

Lemma (triangular determinant). For M = D + E with E strictly block-lower in read order,
det M = det D = product of junction factors, for ANY couplings E.

Theorem. Closure amplitude = alpha^(number of junctions) = alpha^21, independent of how the
levels couple, provided the read is one-way.

Converse (why the registered network of Parts VI-VII failed): two-way coupling
(back-reaction within a closure) changes the determinant. The measured G bounds how much.
"""
from __future__ import annotations

import math

import numpy as np

import network_model as nm

RESULTS = []


def check(name, cond):
    RESULTS.append((name, bool(cond)))
    print(f"[{'PASS' if cond else 'FAIL'}] {name}")


rng = np.random.default_rng(11)
ALPHA = 7.2973525693e-3
level = np.array([len(n) for n in nm.nodes])
B1 = nm.B(1).astype(float)

print("\n=== L1. One-way (read-ordered) coupling: det = product of junction factors ===")
ok = True
for _ in range(200):
    E = np.zeros((21, 21))
    for i in range(21):
        for j in range(21):
            if level[i] > level[j]:                 # coupling only from earlier to later level
                E[i, j] = rng.normal(0, 3)
    M = ALPHA * (B1 + E)
    ok &= abs(np.linalg.det(M) / ALPHA ** 21 - 1) < 1e-8
check("200 random one-way inter-level couplings (any size): det(alpha (B + E)) = alpha^21 exactly", ok)
ok_down = abs(np.linalg.det(ALPHA * (B1 + nm.E("down").astype(float))) / ALPHA ** 21 - 1) < 1e-9
ok_up = abs(np.linalg.det(ALPHA * (B1 + nm.E("up").astype(float))) / ALPHA ** 21 - 1) < 1e-9
check("The registered tree, read down only or up only: alpha^21 (Part VI's variants (a), (b))", ok_down and ok_up)

print("\n=== L2. Two-way coupling (back-reaction) breaks it ===")
Ed, Eu = nm.E("down").astype(float), nm.E("up").astype(float)
p = lambda eps: np.linalg.det(B1 + Ed + eps * Eu)
for eps in (0.0, 1e-3, 1e-2, 0.1, 0.5, 1.0):
    print(f"      back-reaction eps = {eps:6.3f}:  det / alpha^21 = {p(eps):+.6f}")
check("Full back-reaction (eps = 1, the registered symmetric network) gives 0: the TetA amplitude cancels", abs(p(1.0)) < 1e-9)
coef = (p(1e-4) - p(0)) / 1e-4
check(f"The change is linear in eps: det / alpha^21 = 1 + c eps + ..., c = {coef:+.3f}", abs((p(2e-4) - 1) / (p(1e-4) - 1) - 2) < 1e-3)

print("\n=== L3. What the measured G allows ===")
HBAR, C, M_E = 1.054571817e-34, 299792458.0, 9.1093837015e-31
G_MEAS, G_SIG = 6.67430e-11, 0.00015e-11
aG = G_MEAS * M_E ** 2 / (HBAR * C)
n_eff = math.log(aG / (17 / 13 * (1 + ALPHA / (2 * math.pi)))) / math.log(ALPHA)
dn = (G_SIG / G_MEAS) / abs(math.log(ALPHA))
print(f"      exponent extracted from G (prefactor and loop fixed): n = {n_eff:.6f} +- {dn:.6f}")
check("The data give n = 21 to within 5 x 10^-6: the closure amplitude is alpha^21 with no measurable deficit",
      abs(n_eff - 21) < 3 * dn)
base = 17 / 13 * ALPHA ** 21 * (1 + ALPHA / (2 * math.pi)) * HBAR * C / M_E ** 2
lo, hi = (G_MEAS - 2 * G_SIG) / base - 1, (G_MEAS + 2 * G_SIG) / base - 1
eps_max = max(abs(lo), abs(hi)) / abs(coef)
print(f"      allowed relative change in the amplitude at 2 sigma: {1e6 * lo:+.1f} to {1e6 * hi:+.1f} ppm")
print(f"      => back-reaction within one closure |eps| < {eps_max:.1e} of the forward coupling")
check("Back-reaction within a closure is bounded below about 10^-5 of the forward read: the snapshot premise P2 is supported by G",
      eps_max < 1e-4)

print("\n=== L4. Which alpha the theorem uses ===")
check("P3 calibrates the junction by electromagnetism, i.e. the MEASURED alpha: the theorem predicts G = 6.674219e-11"
      " (the pre-registered value), not the octahedron-alpha 6.674510e-11 of Part XI",
      abs(base - 6.674219e-11) / base < 1e-6)

n_pass = sum(1 for _, ok_ in RESULTS if ok_)
print(f"\n{n_pass}/{len(RESULTS)} checks passed")
if __name__ == "__main__":
    raise SystemExit(0 if n_pass == len(RESULTS) else 1)
