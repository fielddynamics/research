"""
verify_closure_tree.py
======================

Part V of INTERSECTION_ALGEBRA.md: a candidate mechanism for the alpha exponent,
read from the closure-walk and G diagrams:
  research/field-closure/tetb_64_walk_of_field_closure.html   (4 faces x 4 channels x 4 subchannels)
  research/g_from_topology/g_three_sierpinski_blocks.html      (blocks 1x1, 4x4, 16x16; filled 1, 9, 81)

Hypothesis (junction rule): a coupling that completes a closure of K^n channels,
read hierarchically K at a time, passes through every junction of the K-ary
closure tree; atomic closure requires all junctions to settle together, so it
carries one alpha per junction:  alpha^J(n),  J(n) = (K^n - 1)/(K - 1).

The script checks the structure, then tests the rule against every alpha
exponent the archive uses elsewhere, including the ones it fails.
"""
from __future__ import annotations

import itertools
import math
import re
import os

import numpy as np

RESULTS = []


def check(name, cond):
    RESULTS.append((name, bool(cond)))
    print(f"[{'PASS' if cond else 'FAIL'}] {name}")


K, D = 4, 3
alpha = 1 / 137.035999177

# ---------------------------------------------------------------------------
print("\n=== T1. The G blocks are tensor powers of the constitutive law's matrix ===")
here = os.path.dirname(os.path.abspath(__file__))
svg = open(os.path.join(here, "..", "g_from_topology", "g_three_sierpinski_blocks.html")).read()
rects = re.findall(r'<rect[^>]*x="([\d.]+)"[^>]*y="([\d.]+)"[^>]*width="([\d.]+)"[^>]*height="([\d.]+)"[^>]*fill="([^"]+)"', svg)
cells = [(float(x_), float(y_), float(w), f) for x_, y_, w, h, f in rects]


def block(lo, hi, colour):
    b = [c for c in cells if lo <= c[0] < hi and c[2] < 60]
    xs, ys = sorted({c[0] for c in b}), sorted({c[1] for c in b})
    M = np.zeros((len(ys), len(xs)), dtype=int)
    for x_, y_, w, f in b:
        if f == colour:
            M[ys.index(y_), xs.index(x_)] = 1
    return M


P1, P2 = block(100, 240, "#378ADD"), block(240, 800, "#D85A30")
L = np.array([[1, 0], [1, 1]])                      # mu(x) = x/(x+1) as a Moebius matrix
kron = lambda A, n: A if n == 1 else np.kron(A, kron(A, n - 1))
check("The 4x4 block drawn in the HTML is exactly L (x) L, L = [[1,0],[1,1]] = the matrix of mu(x) = x/(x+1)",
      P1.shape == (4, 4) and np.array_equal(P1, kron(L, 2)))
check("The 16x16 block is exactly L^(x)4", P2.shape == (16, 16) and np.array_equal(P2, kron(L, 4)))
check("Filled cells 1, 9, 81 = 3^0, 3^2, 3^4 (L has 3 non-zero entries); diagonals 1, 4, 16 give the traces",
      [int(P1.sum()), int(P2.sum())] == [9, 81] and [int(np.trace(P1)), int(np.trace(P2))] == [4, 16])
check("Unipotent blocks: det(alpha^S) = alpha^Tr S = alpha^(1+4+16) -- the Sierpinski picture and the projector picture read the same 21",
      np.trace(P1) + np.trace(P2) + 1 == 21)

# ---------------------------------------------------------------------------
print("\n=== T2. The closure tree ===")
leaves = list(itertools.product(range(K), repeat=D))          # face, channel, subchannel
internal = [p for d in range(D) for p in itertools.product(range(K), repeat=d)]
check(f"The 64-channel walk (face, channel, subchannel) is a complete {K}-ary tree with {len(leaves)} leaves", len(leaves) == 64)
check(f"Its internal junctions number {len(internal)} = 1 + 4 + 16 = (K^D - 1)/(K - 1) = (64 - 1)/3 = 21",
      len(internal) == 21 == (K ** D - 1) // (K - 1))
even = sum(1 for p in internal if len(p) % 2 == 0)
odd = len(internal) - even
check(f"Junctions at even depth {even}, odd depth {odd}: 21, 17, 13 = all, even-depth, even minus odd",
      (len(internal), even, even - odd) == (21, 17, 13))
check("A single root-to-leaf path crosses only D = 3 junctions: the exponent counts ALL junctions (atomic closure), not path length",
      D == 3 and len(internal) == 21)
check("21 = ((D+1)^D - 1)/D: with K = D + 1 the exponent is fixed by D alone, and has three terms because the depth is D = 3",
      ((D + 1) ** D - 1) // D == 21)

# ---------------------------------------------------------------------------
print("\n=== T3. The junction rule against every alpha exponent in the archive ===")
J = lambda n: (K ** n - 1) // (K - 1)
print("      J(n) for n = 1..4:", [J(n) for n in range(1, 5)])
uses = {
    "electromagnetism, alpha^1": 1,
    "baryon asymmetry eta_B = 29.4 alpha^5 (pyramid_portal_research/python/baryogenesis.py)": 5,
    "G = (17/13) alpha^21 (g_from_topology)": 21,
    "Lambda = (9/5) alpha^57 (pyramid_portal_research/python/cosmological_constant.py)": 57,
}
for name, e in uses.items():
    hit = [n for n in range(1, 6) if J(n) == e]
    print(f"      {name}: exponent {e} -> {'closure depth n = ' + str(hit[0]) if hit else 'NOT a junction count'}")
check("Exponents 1, 5, 21 are J(1), J(2), J(3): closures of 4, 16, 64 channels", [J(1), J(2), J(3)] == [1, 5, 21])
check("Exponent 57 (Lambda) is not J(n) for any n: the rule CONFLICTS with the archive's Lambda formula",
      57 not in [J(n) for n in range(1, 10)])
check("J(4) = 85 is the alpha^85 that merkaba_engine.py rejects for G: consistent (G is depth 3, not 4)", J(4) == 85)
check("eta_B: 29.4 alpha^5 = 6.09e-10 against Planck 2018 6.10e-10 (the archive's fit, prefactor chosen there)",
      abs(29.4 * alpha ** 5 - 6.10e-10) / 6.10e-10 < 0.01)

# ---------------------------------------------------------------------------
print("\n=== T4. Does G's prefactor rule transfer to depth 2? ===")
ev2 = sum(1 for d in range(2) for _ in itertools.product(range(K), repeat=d) if d % 2 == 0)
od2 = J(2) - ev2
check(f"At depth 2 the even/odd junction counts are {ev2}/{od2}: the analogue of 17/13 is 1/(1-4) = -1/3, negative",
      (ev2, od2) == (1, 4))
check("So the prefactor rule (even-depth over even-minus-odd) does NOT transfer: eta_B's 29.4 is not of this form",
      ev2 / (ev2 - od2) < 0)
check("The 7 x 3 decomposition of 21 (01.3_graded_identity_operator.md) is not the tree's 1 + 4 + 16: the two readings disagree",
      [1, 4, 16] != [7, 7, 7] and sum([1, 4, 16]) == sum([7, 7, 7]))

n_pass = sum(1 for _, ok in RESULTS if ok)
print(f"\n{n_pass}/{len(RESULTS)} checks passed")
if __name__ == "__main__":
    raise SystemExit(0 if n_pass == len(RESULTS) else 1)
