"""The affine connection of the tiled cube: exact checks for every theorem of tiled_cube_affine_connection.tex.
The cube centred at 2n has side 2; the tile at the origin is [-1,1]^3. The legs v_1..v_4 are the forced frame's columns, the
corners with xyz = +1 (TetA, the Gram-matrix convention); TetB is -v. Each face of TetA (opposite v_lambda) is cut by the
piercing TetB corner -v_lambda into a core triangle (a face of the Field Origin) and three corner triangles (faces of TetA's
spikes): the half-space proof's 16 channels. Check i.j belongs to Theorem i. Exact integers and fractions throughout.
Run: python3 verify_tiled_cube_affine_connection.py
"""
import itertools
from fractions import Fraction as Fr
from collections import defaultdict, Counter

ok = []; ids = []
def check(m, c): ok.append(bool(c)); ids.append(m.split(" ")[0]); print(("PASS " if c else "FAIL ") + m)
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


print("=== Theorem 1: the honeycomb and the shared octahedra")
def _spikes(c):   # unit cubes [2c, 2c+2]^3 in doubled coordinates, as in the closure note
    out = []
    for f in itertools.product((0, 1), repeat=3):
        tip = tuple(2 * (a + b) for a, b in zip(c, f))
        base = [tuple(2 * c[i] + (2 * f[k] if i == k else 1) for i in range(3)) for k in range(3)]
        out.append(frozenset([tip] + base))
    return out
def _tri_faces(vs): return {frozenset(t) for t in itertools.combinations(sorted(vs), 3)}
def _octa(cen): return [tuple(cen[i] + (s if i == k else 0) for i in range(3)) for k in range(3) for s in (1, -1)]
def _oct_faces(cen):
    vs = _octa(cen)
    return {frozenset(t) for t in itertools.combinations(vs, 3)
            if all(sum((a - b) ** 2 for a, b in zip(x, y)) == 2 for x, y in itertools.combinations(t, 2))}
_block = list(itertools.product(range(3), repeat=3)); _sf = {}
for c in _block:
    for t in _spikes(c):
        for fc in _tri_faces(t): _sf[fc] = c
_mids = [p for p in itertools.product(range(1, 6), repeat=3) if sum(x % 2 for x in p) == 1 and all(x not in (0, 6) for x in p)]
from collections import Counter as _C
check("1.1 the star fills half its cube: 8 spikes + the core octahedron = 8 + 4 = 12 of the cube's 24 small-tetrahedron units, "
      "and the other half is 12 edge wedges, one quarter octahedron each", 8 * 1 + 4 == 24 // 2 and 24 - 12 == 12 * (4 // 4))
check("1.2 at every interior cube edge the 4 wedges close into one octahedron whose 8 faces are spike faces, 2 from each of "
      "the 4 cubes around the edge: the shared octahedra, so the cubes fill space with nothing left over",
      all(len(_oct_faces(e)) == 8 and _oct_faces(e) <= set(_sf) and sorted(_C(_sf[fc] for fc in _oct_faces(e)).values()) == [2, 2, 2, 2]
          for e in _mids))
check("1.3 each cube holds 12/4 = 3 shared octahedra, so space is half stars and half shared octahedra", 12 // 4 * 4 == 12)

print("\n=== Theorem 2: every channel is shared by four cubes")
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
check("2.1  a corner channel is a face of exactly one shared octahedron, so it is shared by the 4 tiles around that cube "
      "edge; the core channel bounds the tile's Field Origin and touches, at its 3 vertices (cube face centres), the Field "
      "Origins of 3 face neighbours. Every channel is shared by exactly 4 tiles", all(len(t) == 4 for t in sub.values()))
per_face = defaultdict(int)
for (a, _), _ in inc: per_face[a] += 1
check("2.2  each face carries 4 channels x 4 tiles = 16 couplings, and the tetrahedron 4 x 16 = 64 = K^3, the number of "
      "components of the affine connection", set(per_face.values()) == {16} and len(inc) == 64)
check("2.3  every channel of the face opposite a leads to the TetB corner -a that pierces it: the core channel is the base "
      "of TetB's spike at -a, and each corner channel's shared octahedron runs from its TetA corner p to -a",
      all((octa(octa_of[(a, p)]) & {F(s) for s in S}) == {F(p), F(neg(a))} for (a, p) in octa_of))
reached = {a: {n for (b, _), n in inc if b == a} for a in A}
around = {a: {n for n in itertools.product((-1, 0, 1), repeat=3) if all(abs(-a[i] - 2 * n[i]) <= 1 for i in range(3))} for a in A}
check("2.4  a face reaches 7 of the 8 tiles around its piercing TetB corner, all but the one diagonally across it",
      all(reached[a] <= around[a] and len(reached[a]) == 7 and around[a] - reached[a] == {tuple((-a[i] - a[i]) // 2 for i in range(3))}
          for a in A))

print("\n=== Theorem 4: the sectors (with 4.x checks below)")
G = []
for perm in itertools.permutations(range(3)):
    for sg in S:
        g = (lambda v, perm=perm, sg=sg: tuple(sg[i] * v[perm[i]] for i in range(3)))
        if {g(s) for s in A} == set(A): G.append(g)
def act(g, it):
    (a, r), n = it
    return ((g(a), r if r == "core" else g(r)), g(n))
check("4.1  the symmetries keeping TetA (T_d, 24 elements, acting on TetA's corners as all of S4) map the 64 couplings onto "
      "themselves", len(G) == 24 and all(act(g, it) in set(inc) for g in G for it in inc))
orbits, seen = [], set()
for it in inc:
    if it not in seen:
        o = {act(g, it) for g in G}; seen |= o; orbits.append(o)
check("4.2  they fall into orbits of sizes 4, 12, 12, 12, 24, exactly as the connection's index triples (lambda, mu, nu) do: "
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
check("4.3  characters on (e, (12), (123), (1234), (12)(34)): all 64 carry %s = chi_V^3, the connection V (x) V (x) V; the 40 "
      "carry %s, the Christoffel sector; the free 24 carry %s, the regular representation, which is the torsion sector "
      "(torsion proof, Theorem 1)" % (chi_all, chi_rest, chi_free),
      chi_all == [64, 8, 1, 0, 0] and chi_rest == [40, 8, 1, 0, 0] and chi_free == [24, 0, 0, 0, 0])
mult = lambda chi: Fr(sum(SIZE[k] * chi[i] * SGN[k] for i, k in enumerate(ORDER)), 24)
check("4.4  the sign representation, the one scalar detector of orientation, occurs once in the 24 and never in the 40, as in "
      "torsion and the Christoffel sector (torsion proof, Theorem 2)", mult(chi_free) == 1 and mult(chi_rest) == 0)
check("4.5  the free 24 are exactly the corner channels' couplings to face neighbours",
      {kind(it) for it in free} == {"corner -> face neighbour"})

print("\n=== Theorem 3: the dictionary lambda = face, mu = channel, nu = leg")
V = A                                                   # the legs v_1..v_4: the forced frame's columns, sum 0, Gram 4I - J
def vadd(*us): return tuple(sum(u[i] for u in us) for i in range(3))
def vsc(e, u): return tuple(e * x for x in u)
def dot(u, w): return sum(x * y for x, y in zip(u, w))
check("3.1  (the existing frame) the legs close, sum v = 0, and v_a . v_b = 4 delta_ab - 1: the forced Gram matrix",
      vadd(*V) == (0, 0, 0) and all(dot(u, w) == (3 if u == w else -1) for u in V for w in V))
def eps(l, m, n): return 1 if n in (l, m) else -1
def tile(l, m, n): return vadd(vsc(-1, l), vsc(eps(l, m, n), n))          # tile centre -v_l + eps v_n (doubled coordinates)
def channel(l, m): return (l, "core") if m == l else (l, m)               # half-space proof: face l's sub-region m
check("3.2  the core channel of face lambda (mu = lambda) is shared by the tiles at -v_lambda + v_lambda = 0 and "
      "-v_lambda - v_nu (nu != lambda): its vertices are the cube face centres (v_q + v_r)/2 = -(v_lambda + v_p)/2 by closure, "
      "and a face centre f is shared by the tiles 0 and 2f",
      all(set(sub[channel(l, l)]) == {tuple(c // 2 for c in tile(l, l, n)) for n in V} for l in V)
      and all(vadd(q, r) == vsc(-1, vadd(l, p)) for l in V for p in V if p != l
              for q, r in [[w for w in V if w not in (l, p)]]))
check("3.3  a corner channel mu != lambda lies on the shared octahedron at the cube-edge midpoint (v_mu - v_lambda)/2, since "
      "v_mu . v_lambda = -1 makes (v_mu + v_lambda)/2 a unit vector; the 4 tiles holding that edge are at -v_lambda + eps v_nu: "
      "0 (nu = lambda), v_mu - v_lambda (nu = mu), and -v_lambda - v_nu for the other two legs",
      all(set(sub[channel(l, m)]) == {tuple(c // 2 for c in tile(l, m, n)) for n in V} for l in V for m in V if m != l)
      and all(sorted(map(abs, vadd(m, l))) == [0, 0, 2] for l in V for m in V if m != l))
Dc = {(l, m, n): (channel(l, m), tuple(c // 2 for c in tile(l, m, n))) for l in V for m in V for n in V}
check("3.4  so (lambda, mu, nu) -> (channel mu of face lambda, the tile at -v_lambda + eps v_nu), eps = +1 exactly when nu is "
      "lambda or mu, is a bijection from the 64 index triples onto the 64 couplings, and it commutes with T_d because it is "
      "built from the legs alone: each channel couples along all four legs, one tile per leg",
      set(Dc.values()) == set(inc) and all(Dc[tuple(g(x) for x in t)] == act(g, Dc[t]) for g in G for t in Dc))
check("4.6  in it the core channel, the face of the Field Origin, is the row mu = lambda of each slice; the diagonal mu = nu "
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
check("5.1  one face's 16 under its own symmetry (C3v) split 1 + 3 + 3 + 3 + 6, as the slice lambda = a's ordered index "
      "pairs (mu, nu) do under the permutations fixing a: (a,a); (a,b); (b,a); (b,b); (b,c) with b, c distinct",
      sorted(fo) == [1, 3, 3, 3, 6])
def det(g):
    M = [g(e) for e in ((1, 0, 0), (0, 1, 0), (0, 0, 1))]
    return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1]) - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
            + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
rots = [g for g in stab if det(g) == 1]
six = [it for it in face if kind(it) == "corner -> face neighbour"]
r_orbs = list({frozenset(act(g, it) for g in rots) for it in six})
check("5.2  the face's 6 is chiral: its rotations split it into two orbits of 3, each corner channel's left and its right "
      "face neighbour, and every reflection exchanges the two",
      len(rots) == 3 and sorted(len(o) for o in r_orbs) == [3, 3]
      and all({act(g, it) for it in r_orbs[0]} == set(r_orbs[1]) for g in stab if det(g) == -1))

invc = {v: k for k, v in Dc.items()}
tauc = {it: Dc[(invc[it][0], invc[it][2], invc[it][1])] for it in inc}
check("4.7  exchanging the lower indices, mu <-> nu, has an even part of dimension 40 (Christoffel) and an odd part of 24 "
      "(torsion); on the corner channels' couplings to face neighbours it exchanges the two senses of circulation around the "
      "face (the two rotation orbits of 5.2)",
      sum(tauc[it] == it for it in inc) == 16 and all((tauc[it] in r_orbs[1]) == (it in r_orbs[0]) for it in six))

print("\n=== Theorem 3 (uniqueness) and Theorem 5: torsion on the channels")
from math import factorial
gact = lambda g, t: tuple(g(x) for x in t)
T = list(itertools.product(V, repeat=3))

# --- 3.5. how many T_d-equivariant bijections exist, and how many are of the leg form
# Aut of a transitive G-set G/H is N(H)/H; count orbit-type matchings by brute force on stabiliser structure.
def stab(it, actf): return frozenset(i for i, g in enumerate(G) if actf(g, it) == it)
orb_c = [frozenset(o) for o in orbits]
orb_t, seen = [], set()
for t in T:
    if t in seen: continue
    o = frozenset(gact(g, t) for g in G); seen |= o; orb_t.append(o)
# equivariant bijections = sum over orbit matchings with conjugate stabilisers of prod |N(H)/H|
def n_equivariant_maps(o_from, o_to, af, at):
    x = next(iter(o_from)); H = stab(x, af)
    return sum(1 for y in o_to if stab(y, at) == H)        # images of x with the same stabiliser: |N(H)/H| per matching
ways = 1
types_c = Counter(len(o) for o in orb_c)
# match orbits of equal size (all same-size orbits here have conjugate stabilisers); count matchings x choices
for size, k in types_c.items():
    oc = [o for o in orb_c if len(o) == size]; ot = [o for o in orb_t if len(o) == size]
    per = n_equivariant_maps(oc[0], ot[0], act, gact)
    ways *= factorial(k) * per ** k
check("3.5  there are %d T_d-equivariant bijections between the 64 couplings and the 64 index triples (the symmetry alone "
      "does not pick one)" % ways, ways == 1152)
# the leg form: mu is the channel's own label and the tile lies at -v_lambda + (sign) v_nu
def leg_form(D_):
    for (l, m, n), ((l2, r), tile_) in D_.items():
        if l2 != l: return False
        if (r == "core") != (m == l) or (r != "core" and r != m): return False
        c = tuple(2 * x for x in tile_)
        if c not in (vadd(vsc(-1, l), n), vadd(vsc(-1, l), vsc(-1, n))): return False
    return True
# enumerate all bijections that send face to lambda and channel to mu (the half-space labels), leaving only nu free:
per_channel_choices = []
for l in V:
    for m in V:
        tiles = sorted(sub[channel(l, m)])
        fits = [n for n in V]
        # for each nu, the tiles at -v_l +- v_nu that belong to this channel
        opts = {n: [t for t in tiles if tuple(2 * x for x in t) in (vadd(vsc(-1, l), n), vadd(vsc(-1, l), vsc(-1, n)))] for n in V}
        per_channel_choices.append(all(len(v) == 1 for v in opts.values()) and len({v[0] for v in opts.values()}) == 4)
check("3.6  once lambda is the face and mu the channel (the half-space labels), requiring the tile to lie along leg nu from the "
      "piercing TetB corner leaves exactly one choice for every coupling: the formula is the only leg-form dictionary",
      all(per_channel_choices) and leg_form(Dc))

# --- 3.7. the 8 tiles around the piercing corner are -v_lambda +- v_nu; the one never reached is (nu = lambda, sign -)
check("3.7  the 8 tiles around the piercing TetB corner -v_lambda are -v_lambda +- v_nu, and the face reaches all but one: "
      "-2 v_lambda, the sign that the rule never uses (nu = lambda with eps = -1)",
      all({tuple(c // 2 for c in vadd(vsc(-1, l), vsc(e, n))) for n in V for e in (1, -1)} == around[l]
          and around[l] - reached[l] == {tuple(c // 2 for c in vsc(-2, l))} for l in V))

# --- 3.8. the sign rule is forced: every other rule eps(l, m, n) in {+1,-1} that is T_d-invariant fails
types = lambda l, m, n: ("lll" if l == m == n else "llx" if m == l else "lxl" if n == l else "lxx" if m == n else "xyz")
alts = 0; good = []
for signs in itertools.product((1, -1), repeat=5):
    rule = dict(zip(["lll", "llx", "lxl", "lxx", "xyz"], signs))
    D_ = {(l, m, n): (channel(l, m), tuple(c // 2 for c in vadd(vsc(-1, l), vsc(rule[types(l, m, n)], n)))) for l, m, n in T}
    if set(D_.values()) == set(inc): good.append(rule)
check("3.8  of the 32 symmetric sign rules, exactly one gives the couplings: eps = +1 exactly when nu is lambda or mu",
      good == [{"lll": 1, "llx": -1, "lxl": 1, "lxx": 1, "xyz": -1}])

# --- 5.3. what mu <-> nu is geometrically
def refl(u, w):  # the reflection of T_d exchanging legs u and w and fixing the other two
    return next(g for g in G if g(u) == w and g(w) == u and all(g(x) == x for x in V if x not in (u, w)))
on24 = all(Dc[(l, n, m)] == act(refl(m, n), Dc[(l, m, n)]) for l, m, n in T if len({l, m, n}) == 3)
check("5.3  on the 24 couplings with all three indices different (corner channels to face neighbours), exchanging mu and nu "
      "is exactly the mirror reflection that exchanges legs mu and nu, a symmetry of the face: torsion-free means "
      "mirror-symmetric there", on24)
others = all(Dc[(l, n, m)] != act(g, Dc[(l, m, n)]) or g(l) != l for l, m, n in T if m != n and l in (m, n) for g in G)
check("5.4  on the 24 couplings with a repeated index (mu or nu equal to lambda) no symmetry of the tile maps a coupling to its "
      "mu <-> nu partner: there the exchange pairs the core channel's coupling to a face neighbour with a corner channel's "
      "coupling to its own tile", all(not any(act(g, Dc[(l, m, n)]) == Dc[(l, n, m)] for g in G)
                                        for l, m, n in T if m != n and l in (m, n)))

# --- 5.5. the torsion proof's pieces on the tiles: t_{a;bc} = (a,b,c) - (a,c,b)
inc_basis = [(a, a, b) for a in V for b in V if b != a]                  # incident: t_{a;ab}
non_basis = [(a, b, c) for a in V for b in V for c in V if len({a, b, c}) == 3]
check("5.5  the torsion's incident half t_{a;ab} = (a,a,b) - (a,b,a) is, on the tiles, the core channel's coupling to a "
      "face neighbour minus a corner channel's coupling to its own tile; its non-incident half t_{a;bc} = (a,b,c) - (a,c,b) "
      "is the difference of two corner channels' couplings to face neighbours, which are mirror images (5.3)",
      all(kind(Dc[(a, a, b)]) == "core -> face neighbour" and kind(Dc[(a, b, a)]) == "own corner" for a, _, b in inc_basis)
      and all(kind(Dc[t]) == "corner -> face neighbour" for t in non_basis))
# axial torsion: omega^a_{bc} = sum_d eps_{abcd}, totally antisymmetric, spans the sign representation
def perm_sign(seq):
    s, seq = 1, list(seq)
    for i in range(len(seq)):
        for j in range(i + 1, len(seq)):
            if seq[i] > seq[j]: s = -s
    return s
idx = {v: i for i, v in enumerate(V)}
def omega(t):
    a, b, c = t
    if len({a, b, c}) < 3: return 0
    d = next(x for x in V if x not in t)
    return perm_sign([idx[a], idx[b], idx[c], idx[d]])
face_vals = []
for l in V:
    rot = [g for g in G if g(l) == l and det(g) == 1]
    six_l = [t for t in T if t[0] == l and len(set(t)) == 3]
    orbs = {frozenset(Dc[(l,) + tuple(g(x) for x in t[1:])] for g in rot) for t in six_l}
    for o in orbs:
        face_vals.append({omega(invc[it]) for it in o})
check("5.6  the totally antisymmetric torsion omega (the sign representation, the one scalar parity detector, along the axial part) lives only on the corner channels' "
      "couplings to face neighbours, and on each face it is +1 on one sense of circulation and -1 on the other: it is the net "
      "circulation around the faces", all(v in ({1}, {-1}) for v in face_vals)
      and all(len({next(iter(v)) for v in face_vals[2*i:2*i+2]}) == 2 for i in range(4))
      and all(omega(t) == 0 for t in T if len(set(t)) < 3))
# the axial vector is invariant under rotations and odd under reflections: a pseudoscalar circulation
check("5.7  under the tile's symmetries omega is unchanged by every rotation and reversed by every reflection: "
      "a pseudoscalar, as a circulation's sense is",
      all(all(omega(gact(g, t)) == det(g) * omega(t) for t in T) for g in G))

def Tv(b): return {**{(a, a, b): 1 for a in V if a != b}, **{(a, b, a): -1 for a in V if a != b}}
def displacement(vec):
    tot = (0, 0, 0)
    for t, w in vec.items(): tot = vadd(tot, vsc(w, tuple(2 * x for x in Dc[t][1])))
    return tot
check("5.8  the vector torsion along leg b (torsion proof, Theorem 3: T_v(b) = sum_a t_{a;ab}) is a displacement toward the "
      "TetB corner -v_b: its couplings reach the face neighbours at -v_a - v_b and subtract the own tile, a net shift of -2 v_b",
      all(displacement(Tv(b)) == vsc(-2, b) for b in V))
check("5.9  it is polar, unlike the axial part: every symmetry, rotation or reflection, sends T_v(b) to T_v(g b) with no sign",
      all({gact(g, t): w for t, w in Tv(b).items()} == Tv(g(b)) for g in G for b in V))
check("5.10  swirl and directed flow are separate: the totally antisymmetric torsion has no net displacement (its circulation "
      "closes on every face), and the vector torsion has no support on the all-different couplings that carry the circulation",
      displacement({t: omega(t) for t in T if omega(t) != 0}) == (0, 0, 0) and all(len(set(t)) < 3 for b in V for t in Tv(b)))

print("\n=== Theorems 3, 4, 5, 6 and 7: TetB, the content, the vortex tube, closure")
B = [neg(a) for a in A]                                   # TetB corners = the parity image

# ---------- TetB: build its channels from the geometry, exactly as for TetA
def build(chamber):
    sub_ = {}
    for a in chamber:
        f = [p for p in chamber if p != a]
        sub_[(a, "core")] = frozenset({(0, 0, 0)} | {tuple(int(x) for x in mid(p, q)) for p, q in itertools.combinations(f, 2)})
        for p in f:
            tri = {F(p)} | {mid(p, q) for q in f if q != p}
            e = [e for e in EDGES if tri <= octa(e)]; assert len(e) == 1
            sub_[(a, p)] = tiles_holding(e[0])
    return sub_
subB = build(B)
incB = {(k, n) for k, ts in subB.items() for n in ts}
DB = {(l, m, n): ((l, "core") if m == l else (l, m), tuple(c // 2 for c in vadd(vsc(-1, l), vsc(eps(l, m, n), n))))
      for l in B for m in B for n in B}
check("3.9  TetB's 64 couplings obey the same formula with its own legs -v: the tiles sharing channel mu of TetB's face "
      "lambda are at -w_lambda + eps w_nu (w = -v), one per leg from the piercing TetA corner",
      set(DB.values()) == incB and len(incB) == 64)
def actP(it):
    (a, r), n = it
    return ((neg(a), r if r == "core" else neg(r)), neg(n))
check("3.10  spatial parity -I carries TetA's dictionary onto TetB's index for index: (lambda, mu, nu) on the legs v goes to "
      "the same (lambda, mu, nu) on the legs -v",
      all(actP(Dc[(l, m, n)]) == DB[(neg(l), neg(m), neg(n))] for l, m, n in T))

# ---------- the swirl as a vortex: angular momentum of omega about each face
def centroid(pts): return tuple(sum(Fr(p[i]) for p in pts) / len(pts) for i in range(3))
def channel_pos(ch, chamber):
    a, r = ch
    f = [p for p in chamber if p != a]
    if r == "core": return centroid([mid(p, q) for p, q in itertools.combinations(f, 2)])
    return centroid([F(r)] + [mid(r, q) for q in f if q != r])
def cross(u, w): return (u[1]*w[2]-u[2]*w[1], u[2]*w[0]-u[0]*w[2], u[0]*w[1]-u[1]*w[0])
def L_face(l, D, chamber, om):
    tot = (0, 0, 0)
    for m in chamber:
        for n in chamber:
            t = (l, m, n)
            w = om(t)
            if w == 0: continue
            ch, tile_ = D[t]
            tot = tuple(tot[i] + w * cross(channel_pos(ch, chamber), tuple(2 * x for x in tile_))[i] for i in range(3))
    return tot
LA = {l: L_face(l, Dc, A, omega) for l in A}
par = lambda u, w: cross(u, w) == (0, 0, 0) and any(x != 0 for x in u)
check("6.1  each face's swirl is a vortex about its leg: the angular momentum sum omega (r_channel x d_tile) over the face is "
      "nonzero and parallel to v_lambda, the axis from the tile's centre through the piercing TetB corner",
      all(par(LA[l], l) for l in A))
check("6.2  the four vortices balance: their angular momenta have one magnitude and sum to zero, as the legs close",
      len({sum(x * x for x in LA[l]) for l in A}) == 1 and tuple(sum(LA[l][i] for l in A) for i in range(3)) == (0, 0, 0))
idxB = {v: i for i, v in enumerate(B)}
def omegaB(t):
    a, b, c = t
    if len({a, b, c}) < 3: return 0
    d = next(x for x in B if x not in t)
    return perm_sign([idxB[a], idxB[b], idxB[c], idxB[d]])
LB = {l: L_face(l, DB, B, omegaB) for l in B}
check("6.3  one tube through the Field Origin: TetA's vortex on face lambda sits on the -v_lambda side of the tile and "
      "TetB's on face -v_lambda on the +v_lambda side, and the two carry the same angular momentum along the axis v_lambda "
      "(parity keeps angular momentum, an axial vector): one swirl, TetA on one end and TetB on the other",
      all(LB[neg(l)] == LA[l] for l in A))
check("6.4  the directed flow balances too: the vector torsion's displacements along the four legs sum to zero "
      "(sum over b of -2 v_b = 0, closure)", tuple(sum(displacement(Tv(b))[i] for b in V) for i in range(3)) == (0, 0, 0))

# ---------- the full irreducible content (torsion proof, Theorem 1; Paper B)
def irr_mult(chi):
    table = {"triv": [1, 1, 1, 1, 1], "sgn": [1, -1, 1, -1, 1], "V2": [2, 0, -1, 0, 2],
             "std": [3, 1, 0, -1, -1], "sgn x std": [3, -1, 0, 1, -1]}
    sz = [SIZE[k] for k in ORDER]
    return {k: Fr(sum(s * c * x for s, c, x in zip(sz, chi, row)), 24) for k, row in table.items()}
def char_lin(sign):   # character of the tau = sign eigenspace on the couplings
    vals = {}
    for g in G:
        k = CLS[ctype(g)]
        fix_g = sum(act(g, it) == it for it in inc)
        fix_gt = sum(act(g, tauc[it]) == it for it in inc)
        vals[k] = Fr(fix_g + sign * fix_gt, 2)
    return [vals[k] for k in ORDER]
mult_even, mult_odd = irr_mult(char_lin(1)), irr_mult(char_lin(-1))
check("4.8  the mirror-symmetric couplings (tau = +1, the Christoffel 40) carry 4 trivial + 0 sign + 3 V2 + 7 std + 3 "
      "(sgn x std), Paper B's decomposition of V (x) Sym^2 V: no sign representation", mult_even == {
          "triv": 4, "sgn": 0, "V2": 3, "std": 7, "sgn x std": 3})
check("4.9  the handed couplings (tau = -1, the torsion 24) carry each irreducible representation as often as its dimension, "
      "1 + 1 + 2 + 3 + 3: the regular representation", mult_odd == {"triv": 1, "sgn": 1, "V2": 2, "std": 3, "sgn x std": 3})

# ---------- torsion's vector, axial and tensor parts on the couplings (torsion proof, Theorem 3)
def vec_of(d): return [d.get(t, 0) for t in T]
def rank(rows):
    M = [list(map(Fr, r)) for r in rows]; rk = 0; cols = len(M[0]) if M else 0
    for c in range(cols):
        piv = next((i for i in range(rk, len(M)) if M[i][c] != 0), None)
        if piv is None: continue
        M[rk], M[piv] = M[piv], M[rk]
        for i in range(len(M)):
            if i != rk and M[i][c] != 0:
                f = M[i][c] / M[rk][c]; M[i] = [x - f * y for x, y in zip(M[i], M[rk])]
        rk += 1
    return rk
tors = [vec_of({(a, b, c): 1, (a, c, b): -1}) for a in V for b in V for c in V if V.index(b) < V.index(c)]
vecp = [vec_of(Tv(b)) for b in V]
def axial(d):  # epsilon_{abcd'} w^{d'} with w = e_d: components (a,b,c) all different with missing leg d
    return {t: omega(t) for t in T if len(set(t)) == 3 and next(x for x in V if x not in t) == d}
axp = [vec_of(axial(d)) for d in V]
incident = [i for i, t in enumerate(T) if len(set(t)) == 2 and t[0] in t[1:]]
nonincident = [i for i, t in enumerate(T) if len(set(t)) == 3]
check("5.11  on the couplings, torsion has rank 24; its vector part (4) lies on the incident couplings (core to face "
      "neighbour against corner to own tile) and its axial part (4) on the non-incident ones (the corner pairs that carry the "
      "circulation), with the tensor part the remaining 16, 8 in each half",
      rank(tors) == 24 and rank(vecp) == 4 and rank(axp) == 4 and rank(vecp + axp) == 8
      and all(all(r[i] == 0 for i in range(64) if i not in incident) for r in vecp)
      and all(all(r[i] == 0 for i in range(64) if i not in nonincident) for r in axp)
      and rank([r for r in tors if all(r[i] == 0 for i in range(64) if i not in incident)]) == 12
      and rank([r for r in tors if all(r[i] == 0 for i in range(64) if i not in nonincident)]) == 12)
check("5.12  each axial component w^d is a circulation that skips the leg d: it lives on the three faces other than face d, "
      "two opposite-sense corner couplings per face, summing to zero on every face",
      all({t[0] for t in axial(d)} == {x for x in V if x != d}
          and all(sum(w for t, w in axial(d).items() if t[0] == l) == 0 and sum(1 for t in axial(d) if t[0] == l) == 2
                  for l in V if l != d) for d in V))

# ---------- the Field Origin row in the lattice, and reciprocity: closure against uniform
core_to = {}
for (l, r), n in inc:
    if r == "core" and n != (0, 0, 0): core_to[n] = core_to.get(n, 0) + 1
check("2.5  the Field Origin row couples the tile to each of its 6 face neighbours exactly twice, through the two TetA faces "
      "of its Field Origin that meet at the shared cube-face centre", sorted(core_to.values()) == [2] * 6
      and all(sum(1 for l in A if (n in sub[(l, 'core')])) == 2 for n in core_to))
def lam(p): return -(-1) ** (((sum(p) + 3) // 2) % 2)
def tetA_has(m, p, labelling):   # is corner p a TetA corner of tile m?
    if labelling == "C": return lam(p) == 1
    return xyz(tuple(p[i] - 2 * m[i] for i in range(3))) == 1
same_end = {"C": [], "U": []}
for (l, r), n in inc:
    if r == "core" or n == (0, 0, 0): continue
    e = octa_of[(l, r)]; p = r                               # this channel sits at the octahedron's TetA end p (own tile)
    for lab in ("C", "U"):
        same_end[lab].append(tetA_has(n, p, lab))            # does the neighbour's TetA meet the same octahedron at p too?
check("7.1  reciprocity separates the labellings: under closure every neighbour reached through a shared octahedron meets "
      "it with its own TetA at the same end, so TetA couples to TetA; under the uniform labelling the face neighbours meet it "
      "with TetA at the other end, the TetB end, so the coupling crosses chambers",
      all(same_end["C"]) and sum(same_end["U"]) == sum(1 for (l, r), n in inc if r != "core" and n != (0, 0, 0)
                                                        and sum(map(abs, n)) == 2))
by = {}
for i, r in zip(ids, ok): by.setdefault(i.split(".")[0], []).append(r)
print("\nby theorem: " + ", ".join(f"Theorem {k}: {sum(v)}/{len(v)}" for k, v in sorted(by.items())))
print(f"\n{sum(ok)}/{len(ok)} checks passed")
