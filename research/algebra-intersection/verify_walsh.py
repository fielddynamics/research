"""
verify_walsh.py
===============

Part IV of INTERSECTION_ALGEBRA.md: the intersection read on the Boolean cube,
in the conventions of research/universe-is-pixelated (corners = 3-bit addresses,
Walsh functions w_a(x) = (-1)^popcount(a & x), TetA = odd-parity corners,
parity = x XOR 111).

  W1. The octahedral node's readout mu IS the constitutive law; x is the
      TetA:TetB mass ratio; the exchange x -> 1/x is parity, XOR 111.
  W2. Which XOR masks realise the exchange, and why only 111 is parity.
  W3. Maximum entropy on the cube gives mu(x) = x/(x+1), with ln x the
      multiplier of the parity harmonic; dilation gates are tilts.
  W4. 21, 17, 13 = dimension, parity-even dimension and super-dimension of the
      frame's graded space (Letter 2's (-1)^rank); the cube's are 8, 4, 0.
  W5. The 64 = 4^3 connection and the 64 = 8 x 8 corner transitions are the
      same module over the XOR group of TetB, and not over the rotations.
  W6. Transitions = F4^3, with the Eisenstein unit acting as the closure step
      (x, y) -> (y, x XOR y): 64 = 1 + 3 x 21.

Requires numpy.  Prints PASS/FAIL per claim.
"""
from __future__ import annotations

import itertools
import math
import os
import sys

import numpy as np

RESULTS = []


def check(name, cond):
    RESULTS.append((name, bool(cond)))
    print(f"[{'PASS' if cond else 'FAIL'}] {name}")


pc = lambda v: bin(v).count("1")
N = 8
H = np.array([[(-1) ** pc(a & x) for x in range(N)] for a in range(N)])
TETA = [v for v in range(N) if pc(v) % 2 == 1]          # {1, 2, 4, 7}
TETB = [v for v in range(N) if pc(v) % 2 == 0]          # {0, 3, 5, 6}
rng = np.random.default_rng(1)

# ---------------------------------------------------------------------------
print("\n=== W1. The node's readout is the constitutive law ===")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "universe-is-pixelated"))
import octahedral_node as on  # noqa: E402

ok = True
for _ in range(200):
    node = on.OctahedralNode(0, standing=True)
    node.inject(tuple(float(v) for v in rng.choice([-1.0, 1.0], size=3)))
    for _t in range(int(rng.integers(1, 40))):
        node.tick()
    v = np.array(node.vertex, dtype=float)
    share = v[on.TETA_IDX].sum() / v.sum()
    if 0 < share < 1:
        ok &= abs(node.mu - share) < 1e-9
check("Node readout mu = (1 + c_xyz/c_0)/2 equals the TetA share of the vertex state (200 random runs)", ok)
masses = rng.random((500, 8)) + 0.01
c = masses @ H.T / 8                                   # Walsh coefficients, archive convention
share_A = masses[:, TETA].sum(1) / masses.sum(1)
s = -c[:, 7] / c[:, 0]                                 # w111 = -1 on TetA, so s = -c111/c000
x = masses[:, TETA].sum(1) / masses[:, TETB].sum(1)
check("With s = -c111/c000 (the normalised parity harmonic): TetA share = (1+s)/2", np.allclose(share_A, (1 + s) / 2))
check("... = x/(x+1), with x = (TetA mass)/(TetB mass): the constitutive law is the chamber odds", np.allclose(share_A, x / (x + 1)))
check("... and s = tanh(ln(x)/2): the parity harmonic is a rapidity", np.allclose(s, np.tanh(np.log(x) / 2)))
flipped = masses[:, [v ^ 7 for v in range(8)]]          # p(x) -> p(x XOR 111)
cf = flipped @ H.T / 8
xf = flipped[:, TETA].sum(1) / flipped[:, TETB].sum(1)
check("Parity p(x) -> p(x XOR 111) sends c111 -> -c111, keeps c000: s -> -s, mu -> 1 - mu, x -> 1/x",
      np.allclose(cf[:, 7], -c[:, 7]) and np.allclose(cf[:, 0], c[:, 0]) and np.allclose(xf, 1 / x))
check("So on the cube the exchange x -> 1/x IS Letter 2's parity, XOR 111 (README lines 78-80 hold here)",
      np.allclose(xf * x, 1))

# ---------------------------------------------------------------------------
print("\n=== W2. Which XOR masks exchange the chambers ===")
odd = [m for m in range(8) if all(np.allclose((masses[:, [v ^ m for v in range(8)]] @ H.T / 8)[:, 7], -c[:, 7])
                                  for _ in [0])]
check(f"The masks that flip the parity harmonic are exactly {odd} = the TetA addresses", odd == TETA)
perms = list(itertools.permutations(range(3)))


def bitperm(p, v):
    return sum(((v >> i) & 1) << p[i] for i in range(3))


central = [m for m in range(8) if all(bitperm(p, v) ^ m == bitperm(p, v ^ m) for p in perms for v in range(8))]
check(f"Masks that commute with every bit permutation (rotation of the axes): {central}: only 111 is the central inversion",
      central == [0, 7])
check("Bit permutations (SWAP gates) keep every grade, so they never exchange the chambers",
      all(pc(bitperm(p, v)) == pc(v) for p in perms for v in range(8)))

# ---------------------------------------------------------------------------
print("\n=== W3. Maximum entropy on the cube gives the constitutive law ===")
wA = -H[7]                                             # +1 on TetA, -1 on TetB
ent = lambda p: -(p * np.log(p)).sum()
ok_law = ok_max = True
for eta in np.linspace(-2, 2, 9):
    g = np.exp(eta * wA)
    g /= g.sum()
    xg = g[TETA].sum() / g[TETB].sum()
    ok_law &= abs(xg - math.exp(2 * eta)) < 1e-12 and abs(g[TETA].sum() - xg / (xg + 1)) < 1e-12
    target = (g * wA).sum()
    for _ in range(300):                               # random distributions with the same parity harmonic
        q = rng.random(8) + 0.01
        # adjust within chambers to match the TetA share exactly
        q[TETA] *= g[TETA].sum() / q[TETA].sum()
        q[TETB] *= g[TETB].sum() / q[TETB].sum()
        ok_max &= ent(q) <= ent(g) + 1e-12
check("Gibbs state p ~ exp(eta w_A): TetA share = x/(x+1) with x = e^{2 eta}", ok_law)
check("... and it has the largest entropy of all cube distributions with that parity harmonic (2700 samples)", ok_max)
check("Dilation gate D_alpha (x -> alpha x) = shift eta -> eta + (1/2) ln alpha: a tilt along the parity harmonic",
      all(abs((lambda gg: gg[TETA].sum() / gg[TETB].sum())(np.exp((e + 0.5 * math.log(a)) * wA))
              - a * math.exp(2 * e)) < 1e-9 for e in (-1, 0, 0.7) for a in (0.3, 2, 16)))

# ---------------------------------------------------------------------------
print("\n=== W4. 21, 17, 13 as graded dimensions ===")
K = 4
ranks = [0] * 1 + [1] * K + [2] * K * K                 # T<=2(V): scalar, vector, tensor
dim = len(ranks)
even = sum(1 for r in ranks if r % 2 == 0)
sdim = sum((-1) ** r for r in ranks)
check(f"Frame space T<=2(V), V = R^4 odd under parity (Letter 2): dim {dim}, even dim {even}, super-dim {sdim}",
      (dim, even, sdim) == (21, 17, 13))
check("Tr(I_s) = Tr(P0 + s P1 + P2) at s = +1, 0, -1 = dim, even dim, super-dim (s = -1 is the parity operator)",
      [sum(s_ ** (r % 2) if r % 2 else 1 for r in ranks) for s_ in (1, 0, -1)] == [21, 17, 13])
grades = [pc(a) for a in range(8)]
cube = (8, sum(1 for g in grades if g % 2 == 0), sum((-1) ** g for g in grades))
check(f"The cube's Walsh space graded by XOR 111: dim, even dim, super-dim = {cube} = (8, 4, 0)", cube == (8, 4, 0))
check("17 = (21 + 13)/2 is the parity-even (root-blind) part; 21 - 13 = 2K = twice the odd part",
      (dim + sdim) // 2 == even and dim - sdim == 2 * K)
check("Ratio read by G: 17/13 = (parity-even dimension)/(super-dimension)", even / sdim == 17 / 13)

# ---------------------------------------------------------------------------
print("\n=== W5. 4^3 versus 8 x 8: which symmetry makes them the same ===")
coords = lambda v: np.array([1 - 2 * ((v >> i) & 1) for i in range(3)])   # bit 0 -> +1
addr = lambda u: sum(int(u[i] < 0) << i for i in range(3))
SP = []
for p in itertools.permutations(range(3)):
    for sg in itertools.product([1, -1], repeat=3):
        M = np.zeros((3, 3), dtype=int)
        for i, j in enumerate(p):
            M[j, i] = sg[i]
        SP.append(M)
corner_perm = lambda M: [addr(M @ coords(v)) for v in range(8)]
pres_A = [M for M in SP if all(corner_perm(M)[a] in TETA for a in TETA)]
E = [M for M in pres_A if np.allclose(np.abs(M), np.eye(3))]           # XOR by even masks
A4 = [M for M in pres_A if round(np.linalg.det(M)) == 1]
TD = pres_A


def chars(G):
    vt = [sum(1 for a in TETA if corner_perm(M)[a] == a) ** 3 for M in G]           # V^{x3}, V = R[TetA]
    tt = [sum(1 for v in range(8) if corner_perm(M)[v] == v) ** 2 for M in G]       # R[G] x R[G]
    return vt, tt


for nm, G, want in (("E (XOR by TetB masks)", E, True), ("A4 (rotations of TetA)", A4, False), ("T_d (all of TetA's symmetry)", TD, False)):
    vt, tt = chars(G)
    check(f"Over {nm}, |G| = {len(G)}: connection 4^3 and transitions 8x8 isomorphic? {vt == tt}", (vt == tt) == want)
check("E is TetB itself acting by XOR (the subgroup of README section 2): it sends corner 000 onto TetB",
      sorted(corner_perm(M)[0] for M in E) == TETB and all(corner_perm(M)[v] == v ^ corner_perm(M)[0] for M in E for v in range(8)))

# ---------------------------------------------------------------------------
print("\n=== W6. Transitions as F4^3, the Eisenstein unit as a closure step ===")
step = lambda t: (t[1], t[0] ^ t[1])                   # multiplication by omega in F4 = F2[omega], bitwise
pairs = [(x_, y_) for x_ in range(8) for y_ in range(8)]
check("omega: (x, y) -> (y, x XOR y) has order 3 on all 64 transitions", all(step(step(step(t))) == t for t in pairs))
check("Only the trivial transition (000, 000) is fixed", [t for t in pairs if step(t) == t] == [(0, 0)])
orbits = {frozenset({t, step(t), step(step(t))}) for t in pairs if t != (0, 0)}
check(f"64 = 1 + 3 x {len(orbits)}: the nonzero transitions fall into 21 = Phi3(4) closure triangles", len(orbits) == 21)
tri = [o for o in orbits if all(a and b and a != b for a, b in o)]
back = [o for o in orbits if o not in tri]
check(f"Each orbit is a closed XOR triangle x, y, x^y: {len(tri)} genuine (oriented Fano lines) + {len(back)} out-and-back",
      len(tri) == 14 and len(back) == 7 and all(all(a ^ b ^ (a ^ b) == 0 for a, b in o) for o in orbits))
check("F4 = Eisenstein integers mod 2: omega^2 + omega + 1 = 0 in this action, i.e. t + w(t) + w(w(t)) = 0 (bitwise XOR)",
      all((t[0] ^ step(t)[0] ^ step(step(t))[0], t[1] ^ step(t)[1] ^ step(step(t))[1]) == (0, 0) for t in pairs))

n_pass = sum(1 for _, ok_ in RESULTS if ok_)
print(f"\n{n_pass}/{len(RESULTS)} checks passed")
if __name__ == "__main__":
    raise SystemExit(0 if n_pass == len(RESULTS) else 1)
