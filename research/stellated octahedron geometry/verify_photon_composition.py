"""Photon composition: n x n x n stellated octahedra ("photons") build one stellated octahedron n times larger.
Exact checks of the counts proved in photon_composition.md, and of the n = 2 readings (metric, contact operator).

Coordinates: doubled and centred, so every vertex is an integer vector and the block is [-n, n]^3.
  photon (star) centre S: every coordinate in {-n+1, -n+3, ..., n-1};  spike direction D in {+-1}^3
  spike vertices: tip S + D, and the three face centres S + D_k e_k
  big tetrahedra T+ = {u : u.v >= -n for v in V+},  T- likewise with V- = -V+;  large star = T+ u T-,  T+ n T- = central octahedron
Part 1 (n = 1..8): the theorem.  Part 2: the two-level composite (n = 4) is decided by coupling relations alone.
Part 3 (n = 2): tip position = the photon's Gram matrix; the photon-photon contact operator.
Run: python3 verify_photon_composition.py
"""
import itertools
from math import comb
from collections import Counter
import numpy as np

ok = []
def check(m, c): ok.append(bool(c)); print(("PASS " if c else "FAIL ") + m)

Vp = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]; Vm = [tuple(-x for x in v) for v in Vp]
SIGNS = list(itertools.product((1, -1), repeat=3))
dot = lambda a, b: sum(x * y for x, y in zip(a, b))
in_tet = lambda vs, V, n: all(dot(p, v) >= -n for p in vs for v in V)
def spike(S, D): return [tuple(s + d for s, d in zip(S, D))] + [tuple(S[i] + (D[k] if i == k else 0) for i in range(3)) for k in range(3)]
def octa(C): return [tuple(C[i] + (s if i == k else 0) for i in range(3)) for k in range(3) for s in (1, -1)]
centres = lambda n: list(itertools.product(range(-n + 1, n, 2), repeat=3))
ROT = []
for p in itertools.permutations(range(3)):
    for s in SIGNS:
        M = np.zeros((3, 3), int)
        for i in range(3): M[i, p[i]] = s[i]
        if round(np.linalg.det(M)) == 1: ROT.append(M)
t = lambda N: N * (N * N + 2) // 3          # honeycomb tetrahedra in a tetrahedron of size N: C(N+2,3) + C(N,3)

print("=== 1. The theorem, checked for n = 1..8")
res = {k: True for k in "abcdefgh"}
for n in range(1, 9):
    sp = [(S, D, spike(S, D)) for S in centres(n) for D in SIGNS]
    inP = {(S, D) for S, D, vs in sp if in_tet(vs, Vp, n)}; inM = {(S, D) for S, D, vs in sp if in_tet(vs, Vm, n)}
    inside = inP | inM; out = [(S, D) for S, D, _ in sp if (S, D) not in inside]
    axial = {(S, D) for S, D, _ in sp if all(S[i] * D[i] == S[0] * D[0] for i in range(3))}
    res["a"] &= len(inP) == len(inM) == t(2 * n) and len(inP & inM) == t(2 * n) - 4 * t(n)
    res["b"] &= len(inside) == 4 * n * (n * n + 1) and len(out) == 24 * comb(n + 1, 3)
    res["c"] &= len(axial) == 8 * n and axial <= inside
    res["d"] &= len(inside - axial) == len(out)
    def stab(S, D):
        key = sorted(spike(S, D))
        return sum(sorted(tuple(int(x) for x in M @ np.array(v)) for v in spike(S, D)) == key for M in ROT)
    res["e"] &= all(stab(S, D) == 1 for S, D, _ in sp if (S, D) not in axial) and all(stab(S, D) == 3 for S, D in axial if any(S))
    cores_in = sum(in_tet(octa(S), Vp, n) or in_tet(octa(S), Vm, n) for S in centres(n))
    cav = [C for C in itertools.product(range(-n, n + 1), repeat=3) if sum((x + n) % 2 == 0 for x in C) == 2
           and all(abs(x) <= n for v in octa(C) for x in v) and (in_tet(octa(C), Vp, n) or in_tet(octa(C), Vm, n))]
    res["f"] &= cores_in + len(cav) == comb(2 * n + 1, 3) + 4 * comb(n + 1, 3)
    res["g"] &= len(inside) + 4 * (cores_in + len(cav)) == 12 * n ** 3           # tetrahedron volume = 1, octahedron = 4
    res["h"] &= len(out) + 4 * (n ** 3 - cores_in) == 4 * len(cav)
check("1a. each big tetrahedron holds t(2n) = 2n(4n^2+2)/3 spikes and their overlap, the central octahedron, holds t(2n) - 4 t(n) "
      "(a tetrahedron of size 2n = 4 corner tetrahedra of size n + the octahedron)", res["a"])
check("1b. so the large star captures t(2n) + 4 t(n) = 4n(n^2+1) spikes and expels 8n^3 - 4n(n^2+1) = 24 C(n+1,3)", res["b"])
check("1c. the 8n spikes on the 4 body diagonals (star centre parallel to spike direction) are all captured", res["c"])
check("1d. hence off the diagonals exactly half are captured and half expelled: 4n(n^2-1) each", res["d"])
check("1e. a rotation fixing a spike fixes its star and its direction, so only diagonal spikes have a stabiliser (order 3); "
      "every expelled spike is moved freely: the expelled set is C(n+1,3) copies of the regular representation of S4", res["e"])
check("1f. octahedra in the large star = C(2n+1,3) + 4 C(n+1,3) (photon cores inside + new cavities between photons)", res["f"])
check("1g. the large star is filled exactly: spikes + 4 x octahedra = 12 n^3 = the photons' total volume", res["g"])
check("1h. so the expelled volume (spikes and cores outside) equals the volume of the new cavities between photons", res["h"])

print("\n=== 2. Two levels (n = 4): the composite is decided by coupling relations alone")
H = lambda a, b: sum(x != y for x, y in zip(a, b))
bits = list(itertools.product((0, 1), repeat=3))
tab = {}
for C, c, f in itertools.product(bits, repeat=3):
    S = tuple(4 * Ci + 2 * ci + 1 - 4 for Ci, ci in zip(C, c)); D = tuple(2 * fi - 1 for fi in f)
    vs = spike(S, D); ins = in_tet(vs, Vp, 4) or in_tet(vs, Vm, 4)
    tab.setdefault((H(C, c), H(c, f), H(C, f)), set()).add(ins)
check("2. with composite C, photon c and spike f, captured or expelled depends only on the three Hamming relations "
      "(d(C,c), d(c,f), d(C,f)): the second-level anatomy is again an element of the coupling scheme", all(len(v) == 1 for v in tab.values()))

print("\n=== 3. n = 2: the composite lays out the photon's metric")
pm = list(itertools.product((1, -1), repeat=3))           # photon frame: the cube corners e_v
check("3a. every spike tip sits at (e_c + e_f)/2 and its squared distance from the Field Origin is 3 - d(c,f) = (3 + e_c.e_f)/2, "
      "a Gram entry of the photon", all(sum(((a + b) / 2) ** 2 for a, b in zip(ec, ef)) == 3 - H(ec, ef) == (3 + dot(ec, ef)) / 2
                                        for ec in pm for ef in pm))
tips = Counter(tuple((a + b) // 2 for a, b in zip(ec, ef)) for ec in pm for ef in pm)
check("3b. tips per point = 2^(3 - r^2): 8 at the Field Origin, 4, 2, 1 outward", all(m == 2 ** (3 - sum(x * x for x in p)) for p, m in tips.items()))
check("3c. polarity balances: 32 spikes point to even corners, 32 to odd", Counter(f.count(-1) % 2 for _ in pm for f in pm) == Counter({0: 32, 1: 32}))
B = np.array([[2 ** (3 - H(a, b)) for b in pm] for a in pm])          # points shared by photons a and b
share = all(len({tuple((x + y) // 2 for x, y in zip(a, f)) for f in pm} & {tuple((x + y) // 2 for x, y in zip(b, f)) for f in pm}) == B[i, j]
            for i, a in enumerate(pm) for j, b in enumerate(pm))
W = np.array([[np.prod([v[i] for i in S]) for v in pm] for k in range(4) for S in itertools.combinations(range(3), k)])
grade = [k for k in range(4) for _ in itertools.combinations(range(3), k)]
eig = [(W[r] @ B @ W[r]) / 8 for r in range(8)]
check("3d. two photons share 2^(3-d) tip points; this contact operator sum_d 2^(3-d) A_d has eigenvalue 3^(3-k) on Walsh grade k "
      "(27, 9, 3, 1): the grade-0 mode is strongest", share and all(abs(e - 3 ** (3 - g)) < 1e-9 for e, g in zip(eig, grade))
      and np.allclose(W @ B @ W.T / 8, np.diag(eig)))


# characters on S4 classes: rotations act on the 4 body diagonals; the connection's 40 = a x {b, c} (symmetric pair) on 4 legs
diag = [(1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1)]
def as_perm(M):
    img = [tuple(int(x) for x in M @ np.array(d)) for d in diag]
    return tuple(next(j for j, e in enumerate(diag) if e == im or e == tuple(-x for x in im)) for im in img)
def cls(p):
    seen, cyc = set(), []
    for i in range(4):
        if i in seen: continue
        L, j = 0, i
        while j not in seen: seen.add(j); j = p[j]; L += 1
        cyc.append(L)
    return tuple(sorted(cyc))
inside2 = [(S, D) for S in centres(2) for D in SIGNS if in_tet(spike(S, D), Vp, 2) or in_tet(spike(S, D), Vm, 2)]
grid_chi, conn_chi = {}, {}
for M in ROT:
    p = as_perm(M)
    grid_chi[cls(p)] = sum(sorted(tuple(int(x) for x in M @ np.array(v)) for v in spike(S, D)) == sorted(spike(S, D)) for S, D in inside2)
for p in itertools.permutations(range(4)):
    conn_chi[cls(p)] = sum(p[a] == a and {p[b], p[c]} == {b, c} for a in range(4) for b in range(4) for c in range(b, 4))
order = [(1, 1, 1, 1), (1, 1, 2), (2, 2), (1, 3), (4,)]
check("3e. limit of the match: the 40 captured spikes and the connection's 40 symmetric components differ as S4 representations, "
      f"characters {[grid_chi[k] for k in order]} vs {[conn_chi[k] for k in order]}",
      [grid_chi[k] for k in order] == [40, 0, 0, 4, 0] and [conn_chi[k] for k in order] == [40, 8, 0, 1, 0])

print(f"\n{sum(ok)}/{len(ok)} checks passed")
