"""The 16 channels of a face in the tiling: exact checks for results 13-15 of README.md (research, not a proof).
The tile at the origin is the cube [-1,1]^3; tile n is centred at 2n. TetA = the corners with xyz = +1 (Gram-matrix
convention). Each face of TetA (the face opposite the TetA corner a) is cut by the piercing TetB corner -a into a core
triangle (a face of the Field Origin) and three corner triangles (faces of TetA's spikes): Letter 1's 4 x 4 = 16 channels.
The sharing used here is geometric, so every result holds for either labelling of the tiling.
Run: python3 verify_sixteen_channels.py
"""
import itertools
from fractions import Fraction as Fr
from collections import defaultdict

ok = []
def check(m, c): ok.append(bool(c)); print(("PASS " if c else "FAIL ") + m)
S = list(itertools.product((1, -1), repeat=3))
def xyz(v): return v[0] * v[1] * v[2]
A = [s for s in S if xyz(s) == 1]
def neg(v): return tuple(-x for x in v)
def mid(u, v): return tuple(Fr(x + y, 2) for x, y in zip(u, v))
def F(v): return tuple(Fr(x) for x in v)
EDGES = [v for v in itertools.product((-1, 0, 1), repeat=3) if sorted(map(abs, v)) == [0, 1, 1]]   # cube-edge midpoints
def octa(e): return {tuple(Fr(e[i] + (d if i == k else 0)) for i in range(3)) for k in range(3) for d in (1, -1)}
def tiles_holding(e): return frozenset(n for n in itertools.product((-1, 0, 1), repeat=3)
                                       if all(abs(Fr(e[i]) - 2 * n[i]) <= 1 for i in range(3)))
def kind(it):
    (a, r), n = it
    if n == (0, 0, 0): return "own core" if r == "core" else "own corner"
    return ("core" if r == "core" else "corner") + (" -> face neighbour" if sum(map(abs, n)) == 1 else " -> edge neighbour")

print("=== 13. What each channel couples to")
sub, octa_of = {}, {}
for a in A:
    f = [p for p in A if p != a]
    sub[(a, "core")] = frozenset({(0, 0, 0)} | {tuple(int(x) for x in mid(p, q)) for p, q in itertools.combinations(f, 2)})
    for p in f:
        tri = {F(p)} | {mid(p, q) for q in f if q != p}
        e = [e for e in EDGES if tri <= octa(e)]
        assert len(e) == 1
        octa_of[(a, p)] = e[0]; sub[(a, p)] = tiles_holding(e[0])
inc = [(k, n) for k, ts in sub.items() for n in ts]
check("13a. a corner channel is a face of exactly one shared octahedron, so it is shared by the 4 tiles around that cube "
      "edge; the core channel bounds the tile's Field Origin and touches, at its 3 vertices (cube face centres), the Field "
      "Origins of 3 face neighbours. Every channel is shared by exactly 4 tiles", all(len(t) == 4 for t in sub.values()))
per_face = defaultdict(int)
for (a, _), _ in inc: per_face[a] += 1
check("13b. each face carries 4 channels x 4 tiles = 16 couplings, and the tetrahedron 4 x 16 = 64 = K^3, the number of "
      "components of the affine connection", set(per_face.values()) == {16} and len(inc) == 64)
check("13c. every channel of the face opposite a leads to the TetB corner -a that pierces it: the core channel is the base "
      "of TetB's spike at -a, and each corner channel's shared octahedron runs from its TetA corner p to -a",
      all((octa(octa_of[(a, p)]) & {F(s) for s in S}) == {F(p), F(neg(a))} for (a, p) in octa_of))
reached = {a: {n for (b, _), n in inc if b == a} for a in A}
around = {a: {n for n in itertools.product((-1, 0, 1), repeat=3) if all(abs(-a[i] - 2 * n[i]) <= 1 for i in range(3))} for a in A}
check("13d. a face reaches 7 of the 8 tiles around its piercing TetB corner, all but the one diagonally across it",
      all(reached[a] <= around[a] and len(reached[a]) == 7 and around[a] - reached[a] == {tuple((-a[i] - a[i]) // 2 for i in range(3))}
          for a in A))

print("\n=== 14. The 64 couplings as the affine connection")
G = []
for perm in itertools.permutations(range(3)):
    for sg in S:
        g = (lambda v, perm=perm, sg=sg: tuple(sg[i] * v[perm[i]] for i in range(3)))
        if {g(s) for s in A} == set(A): G.append(g)
def act(g, it):
    (a, r), n = it
    return ((g(a), r if r == "core" else g(r)), g(n))
check("14a. the symmetries keeping TetA (T_d, 24 elements, acting on TetA's corners as all of S4) map the 64 couplings onto "
      "themselves", len(G) == 24 and all(act(g, it) in set(inc) for g in G for it in inc))
orbits, seen = [], set()
for it in inc:
    if it not in seen:
        o = {act(g, it) for g in G}; seen |= o; orbits.append(o)
check("14b. they fall into orbits of sizes 4, 12, 12, 12, 24, exactly as the connection's index triples (lambda, mu, nu) do: "
      "all equal; three kinds with one repeat; all different", sorted(len(o) for o in orbits) == [4, 12, 12, 12, 24])
def ctype(g):
    p = [A.index(g(s)) for s in A]; seen2, cyc = set(), []
    for i in range(4):
        if i in seen2: continue
        l, j = 0, i
        while j not in seen2: seen2.add(j); j = p[j]; l += 1
        cyc.append(l)
    return tuple(sorted(cyc, reverse=True))
CLS = {(1, 1, 1, 1): "e", (2, 1, 1): "(12)", (3, 1): "(123)", (4,): "(1234)", (2, 2): "(12)(34)"}
ORDER = ["e", "(12)", "(123)", "(1234)", "(12)(34)"]
SIZE = {"e": 1, "(12)": 6, "(123)": 8, "(1234)": 6, "(12)(34)": 3}
SGN = {"e": 1, "(12)": -1, "(123)": 1, "(1234)": -1, "(12)(34)": 1}
def char(fixcount):
    vals = defaultdict(set)
    for g in G: vals[CLS[ctype(g)]].add(fixcount(g))
    assert all(len(v) == 1 for v in vals.values())
    return [next(iter(vals[k])) for k in ORDER]
free = next(o for o in orbits if len(o) == 24); rest = [it for o in orbits if len(o) != 24 for it in o]
chi_all = char(lambda g: sum(act(g, it) == it for it in inc))
chi_rest = char(lambda g: sum(act(g, it) == it for it in rest))
chi_free = char(lambda g: sum(act(g, it) == it for it in free))
check("14c. characters on (e, (12), (123), (1234), (12)(34)): all 64 carry %s = chi_V^3, the connection V (x) V (x) V; the 40 "
      "carry %s, the Christoffel sector; the free 24 carry %s, the regular representation, which is the torsion sector "
      "(torsion proof, Theorem 1)" % (chi_all, chi_rest, chi_free),
      chi_all == [64, 8, 1, 0, 0] and chi_rest == [40, 8, 1, 0, 0] and chi_free == [24, 0, 0, 0, 0])
mult = lambda chi: Fr(sum(SIZE[k] * chi[i] * SGN[k] for i, k in enumerate(ORDER)), 24)
check("14d. the sign representation, the one scalar detector of orientation, occurs once in the 24 and never in the 40, as in "
      "torsion and the Christoffel sector (torsion proof, Theorem 2)", mult(chi_free) == 1 and mult(chi_rest) == 0)
check("14e. the free 24 are exactly the corner channels' couplings to face neighbours",
      {kind(it) for it in free} == {"corner -> face neighbour"})

print("\n=== 15. The algebraic dictionary: lambda = face, mu = channel, nu = leg")
V = A                                                   # the legs v_1..v_4: the forced frame's columns, sum 0, Gram 4I - J
def vadd(*us): return tuple(sum(u[i] for u in us) for i in range(3))
def vsc(e, u): return tuple(e * x for x in u)
def dot(u, w): return sum(x * y for x, y in zip(u, w))
check("15a. (the existing frame) the legs close, sum v = 0, and v_a . v_b = 4 delta_ab - 1: the forced Gram matrix",
      vadd(*V) == (0, 0, 0) and all(dot(u, w) == (3 if u == w else -1) for u in V for w in V))
def eps(l, m, n): return 1 if n in (l, m) else -1
def tile(l, m, n): return vadd(vsc(-1, l), vsc(eps(l, m, n), n))          # tile centre -v_l + eps v_n (doubled coordinates)
def channel(l, m): return (l, "core") if m == l else (l, m)               # half-space proof: face l's sub-region m
check("15b. the core channel of face lambda (mu = lambda) is shared by the tiles at -v_lambda + v_lambda = 0 and "
      "-v_lambda - v_nu (nu != lambda): its vertices are the cube face centres (v_q + v_r)/2 = -(v_lambda + v_p)/2 by closure, "
      "and a face centre f is shared by the tiles 0 and 2f",
      all(set(sub[channel(l, l)]) == {tuple(c // 2 for c in tile(l, l, n)) for n in V} for l in V)
      and all(vadd(q, r) == vsc(-1, vadd(l, p)) for l in V for p in V if p != l
              for q, r in [[w for w in V if w not in (l, p)]]))
check("15c. a corner channel mu != lambda lies on the shared octahedron at the cube-edge midpoint (v_mu - v_lambda)/2, since "
      "v_mu . v_lambda = -1 makes (v_mu + v_lambda)/2 a unit vector; the 4 tiles holding that edge are at -v_lambda + eps v_nu: "
      "0 (nu = lambda), v_mu - v_lambda (nu = mu), and -v_lambda - v_nu for the other two legs",
      all(set(sub[channel(l, m)]) == {tuple(c // 2 for c in tile(l, m, n)) for n in V} for l in V for m in V if m != l)
      and all(sorted(map(abs, vadd(m, l))) == [0, 0, 2] for l in V for m in V if m != l))
Dc = {(l, m, n): (channel(l, m), tuple(c // 2 for c in tile(l, m, n))) for l in V for m in V for n in V}
check("15d. so (lambda, mu, nu) -> (channel mu of face lambda, the tile at -v_lambda + eps v_nu), eps = +1 exactly when nu is "
      "lambda or mu, is a bijection from the 64 index triples onto the 64 couplings, and it commutes with T_d because it is "
      "built from the legs alone: each channel couples along all four legs, one tile per leg",
      set(Dc.values()) == set(inc) and all(Dc[tuple(g(x) for x in t)] == act(g, Dc[t]) for g in G for t in Dc))
check("15e. in it the core channel, the face of the Field Origin, is the row mu = lambda of each slice; the diagonal mu = nu "
      "is each channel's coupling straight through, along its own leg: the core to its own tile, a corner channel through its "
      "shared octahedron to the tile diagonally across",
      {kind(Dc[(l, l, n)]) for l in V for n in V} == {"own core", "core -> face neighbour"}
      and {kind(Dc[(l, m, m)]) for l in V for m in V} == {"own core", "corner -> edge neighbour"})
stab = [g for g in G if g(A[0]) == A[0]]
face = [it for it in inc if it[0][0] == A[0]]
fo, seen = [], set()
for it in face:
    if it not in seen:
        o = {act(g, it) for g in stab}; seen |= o; fo.append(len(o))
check("15f. one face's 16 under its own symmetry (C3v) split 1 + 3 + 3 + 3 + 6, as the slice lambda = a's ordered index "
      "pairs (mu, nu) do under the permutations fixing a: (a,a); (a,b); (b,a); (b,b); (b,c) with b, c distinct",
      sorted(fo) == [1, 3, 3, 3, 6])
def det(g):
    M = [g(e) for e in ((1, 0, 0), (0, 1, 0), (0, 0, 1))]
    return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1]) - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
            + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
rots = [g for g in stab if det(g) == 1]
six = [it for it in face if kind(it) == "corner -> face neighbour"]
r_orbs = list({frozenset(act(g, it) for g in rots) for it in six})
check("15g. the face's 6 is chiral: its rotations split it into two orbits of 3, each corner channel's left and its right "
      "face neighbour, and every reflection exchanges the two",
      len(rots) == 3 and sorted(len(o) for o in r_orbs) == [3, 3]
      and all({act(g, it) for it in r_orbs[0]} == set(r_orbs[1]) for g in stab if det(g) == -1))

invc = {v: k for k, v in Dc.items()}
tauc = {it: Dc[(invc[it][0], invc[it][2], invc[it][1])] for it in inc}
check("15h. exchanging the lower indices, mu <-> nu, has an even part of dimension 40 (Christoffel) and an odd part of 24 "
      "(torsion); on the corner channels' couplings to face neighbours it exchanges the two senses of circulation around the "
      "face (the two rotation orbits of 15g)",
      sum(tauc[it] == it for it in inc) == 16 and all((tauc[it] in r_orbs[1]) == (it in r_orbs[0]) for it in six))

print(f"\n{sum(ok)}/{len(ok)} checks passed")
