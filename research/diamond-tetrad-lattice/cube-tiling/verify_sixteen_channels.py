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

print("\n=== 15. One face is one slice; the lower-index exchange on the tiles")
def to_triple(it):
    (a, r), n = it
    f = [p for p in A if p != a]
    if r == "core":
        if n == (0, 0, 0): return (a, a, a)
        q, s = next((q, s) for q, s in itertools.combinations(f, 2) if tuple(int(x) for x in mid(q, s)) == n)
        return (a,) + (next(p for p in f if p not in (q, s)),) * 2
    p = r
    if n == (0, 0, 0): return (a, a, p)
    if sum(map(abs, n)) == 2: return (a, p, a)
    return (a, p, next(q for q in f if q != p and tuple(int(x) for x in mid(p, q)) == n))
D = {it: to_triple(it) for it in inc}
check("15a. a dictionary: face opposite a -> lambda = a; own core -> (a,a,a); own corner p -> (a,a,p); corner p to its edge "
      "neighbour -> (a,p,a); core to the face neighbour across mid(q,r) -> (a,p,p), p the face's third corner; corner p to "
      "the face neighbour across mid(p,q) -> (a,p,q). It is a bijection onto the 64 triples and commutes with T_d",
      set(D.values()) == set(itertools.product(A, repeat=3))
      and all(D[act(g, it)] == tuple(g(x) for x in D[it]) for g in G for it in inc))
inv = {v: k for k, v in D.items()}
tau = {it: inv[(D[it][0], D[it][2], D[it][1])] for it in inc}
check("15b. under it, exchanging the lower indices mu <-> nu is, on the tiles: swap the two corner channels that reach the "
      "same face neighbour; swap a corner channel's coupling to its own tile with its coupling to its edge neighbour; fix "
      "the core channels. Its even part is 40-dimensional (Christoffel) and its odd part 24-dimensional (torsion)",
      all(kind(tau[it]) == kind(it) and tau[it][1] == it[1] and tau[it][0][1] != it[0][1]
          for it in inc if kind(it) == "corner -> face neighbour")
      and all({kind(it), kind(tau[it])} == {"own corner", "corner -> edge neighbour"} and tau[it][0] == it[0]
              for it in inc if kind(it) in ("own corner", "corner -> edge neighbour"))
      and all(tau[it] == it for it in inc if kind(it).endswith("core") or kind(it) == "core -> face neighbour")
      and sum(tau[it] == it for it in inc) == 16)
stab = [g for g in G if g(A[0]) == A[0]]
face = [it for it in inc if it[0][0] == A[0]]
fo, seen = [], set()
for it in face:
    if it not in seen:
        o = {act(g, it) for g in stab}; seen |= o; fo.append(len(o))
check("15c. one face's 16 under its own symmetry (C3v) split 1 + 3 + 3 + 3 + 6, as the slice lambda = a's ordered index "
      "pairs (mu, nu) do under the permutations fixing a: (a,a); (a,b); (b,a); (b,b); (b,c) with b, c distinct",
      sorted(fo) == [1, 3, 3, 3, 6])
def det(g):
    M = [g(e) for e in ((1, 0, 0), (0, 1, 0), (0, 0, 1))]
    return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1]) - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
            + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
rots = [g for g in stab if det(g) == 1]
six = [it for it in face if kind(it) == "corner -> face neighbour"]
r_orbs = list({frozenset(act(g, it) for g in rots) for it in six})
check("15d. the face's 6 is chiral: its rotations split it into two orbits of 3, each corner channel's left and its right "
      "face neighbour, and every reflection exchanges the two",
      len(rots) == 3 and sorted(len(o) for o in r_orbs) == [3, 3]
      and all({act(g, it) for it in r_orbs[0]} == set(r_orbs[1]) for g in stab if det(g) == -1))

print(f"\n{sum(ok)}/{len(ok)} checks passed")
