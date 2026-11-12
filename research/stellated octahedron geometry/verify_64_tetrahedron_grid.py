"""Verification of the 64-Tetrahedron Grid (64-TG) as exact geometry, and its reading in the coupling algebra.

Model: a 2x2x2 block of unit cubes (cube edge 1, so the small tetrahedra have edge a/2 = sqrt2/2 and the block is the
cube of side sqrt2 a in Galeffi's units). Each small cube holds one stellated octahedron (a star of tetrahedron edge a):
a core octahedron plus 8 tetrahedral spikes, one tip at each corner of its cube. The 64 tetrahedra are labelled by an
ordered pair of cube corners (c, f): which star, which spike. The tip sits at c + f; its base is the 3 face centres of
small cube c that meet at corner f.

Part 1 (checks 1-9): the anatomy, and the coupling-algebra relations A0..A3 = Hamming distance d(c, f).
Part 2 (checks G1-G11): Galeffi's counts in "On the 14-Octahedron Backbone of the Bimetric 64-Tetrahedron Grid",
recomputed exactly, including the correction to his Table 3 (16 -> 40 tetrahedra inside the large star).

Exact arithmetic throughout (integers, Fractions, sympy). Run: python3 verify_64_tetrahedron_grid.py
See README.md in this folder and research/coupling-algebra/README.md.
"""

import itertools
from collections import Counter

ok = []
def check(m, c): ok.append(bool(c)); print(("PASS " if c else "FAIL ") + m)

bits = list(itertools.product((0, 1), repeat=3))
# star c sits in the unit cube with lowest corner c; its spike f points to that cube's corner c + f
spikes = [(c, f) for c in bits for f in bits]
tip = lambda c, f: tuple(ci + fi for ci, fi in zip(c, f))          # in the block [0,2]^3
d = lambda c, f: sum(ci != fi for ci, fi in zip(c, f))               # Hamming distance between 'which star' and 'which spike'
check("1. 8 stars x 8 spikes = 64 tetrahedra; each labelled by an ordered pair of cube corners (which star, which spike)",
      len(spikes) == 64 and len(set(spikes)) == 64)

# the large star of the block: big cube corners {0,2}^3; its core octahedron vertices = big face centres; its Field Origin = (1,1,1)
centre = (1, 1, 1)
big_corners = {p for p in itertools.product((0, 1, 2), repeat=3) if all(x in (0, 2) for x in p)}
edge_mids = {p for p in itertools.product((0, 1, 2), repeat=3) if sum(x == 1 for x in p) == 1}
face_cent = {p for p in itertools.product((0, 1, 2), repeat=3) if sum(x == 1 for x in p) == 2}
layer = {0: big_corners, 1: edge_mids, 2: face_cent, 3: {centre}}
check("2. the spike's relation d(star, spike) fixes where its tip lands: d = 0 the 8 points of the large star, d = 1 the 12 vertices "
      "of the vector equilibrium (cuboctahedron), d = 2 the 6 vertices of the large star's core octahedron, d = 3 the centre",
      all(tip(c, f) in layer[d(c, f)] for c, f in spikes))
cnt = Counter(d(c, f) for c, f in spikes)
mult = {k: Counter(tip(c, f) for c, f in spikes if d(c, f) == k) for k in range(4)}
check("3. the 64 split 8 + 24 + 24 + 8: one tip at each large-star point, two at each vector-equilibrium vertex, four at each core-octahedron "
      "vertex, eight at the centre (multiplicity 2^d)",
      [cnt[k] for k in range(4)] == [8, 24, 24, 8]
      and all(set(mult[k].values()) == {2 ** k} and len(mult[k]) == len(layer[k]) for k in range(4)))
check("4. distances from the centre: core-octahedron vertices 1, vector-equilibrium vertices sqrt2, large-star points sqrt3",
      all(sum((x - 1) ** 2 for x in p) == 2 for p in edge_mids) and all(sum((x - 1) ** 2 for x in p) == 1 for p in face_cent)
      and all(sum((x - 1) ** 2 for x in p) == 3 for p in big_corners))
check("5. tips fill the 3x3x3 lattice of the block (27 points) with per-axis multiplicities 1, 2, 1: 64 = (1 + 2 + 1)^3",
      len({tip(c, f) for c, f in spikes}) == 27 and 4 ** 3 == 64)

# chambers: global parity of the vertex lattice (x + y + z mod 2) defines TetA / TetB consistently across shared corners
chamber = lambda p: (sum(p) % 2)
check("6. the 8 inward spikes (d = 3) all meet at the centre, the large star's Field Origin", {tip(c, f) for c, f in spikes if d(c, f) == 3} == {centre})
check("6b. all 8 points of the large star sit at EVEN positions of the fine lattice, so the fine chamber label cannot split them",
      {chamber(tip(c, f)) for c, f in spikes if d(c, f) == 0} == {0})
check("6c. the large star's two tetrahedra are told apart by the COARSE label instead: the parity of 'which star' (4 and 4)",
      Counter(sum(c) % 2 for c, f in spikes if d(c, f) == 0) == Counter({0: 4, 1: 4}))
# symmetry: rotating/reflecting the whole grid acts on (star, spike) by the same cube symmetry on both labels
def cube_syms():
    for p in itertools.permutations(range(3)):
        for s in itertools.product((0, 1), repeat=3):
            yield lambda v, p=p, s=s: tuple((v[p[i]] + s[i]) % 2 for i in range(3))     # bit form of the 48 signed permutations
G = list(cube_syms())
orbits = []
seen = set()
for x in spikes:
    if x in seen: continue
    o = {(g(x[0]), g(x[1])) for g in G}; seen |= o; orbits.append(o)
check("7. under the grid's 48 symmetries the 64 tetrahedra fall into exactly 4 kinds, one per relation d = 0, 1, 2, 3 "
      "(the coupling algebra's A0..A3)", len(orbits) == 4 and sorted(len(o) for o in orbits) == [8, 8, 24, 24]
      and all(len({d(c, f) for c, f in o}) == 1 for o in orbits))
check("8. between-chamber relations (d odd: vector links and Field Origin) are the 24 + 8 spikes tipped at the vector equilibrium and "
      "the centre; within-chamber (d even) the 8 + 24 tipped at the large star's points and core octahedron",
      all((d(c, f) % 2 == 1) == (chamber(c) != chamber(f)) for c, f in spikes))
# commutant (coupling operators on the 64 grid tetrahedra respecting the grid's symmetry) = number of orbits on ordered pairs
pairs_orbits = set()
canon = {}
for x in spikes:
    for y in spikes:
        key = min(((g(x[0]), g(x[1])), (g(y[0]), g(y[1]))) for g in G)
        pairs_orbits.add(key)
print(f"     dimension of the grid's symmetric coupling algebra on its 64 tetrahedra: {len(pairs_orbits)}")
check("9. that algebra (operators on the 64 tetrahedra commuting with the grid's 48 symmetries) has dimension 120 (computed, not predicted)",
      len(pairs_orbits) == 120)
# ===================== cross-check against Galeffi, "On the 14-Octahedron Backbone of the Bimetric 64-Tetrahedron Grid"
from fractions import Fraction as Fr
print("\n--- Galeffi's counts, recomputed from the model")
def face_centre(c, k, s):     # centre of face k (s = 0/1) of small cube c
    p = [Fr(ci) + Fr(1, 2) for ci in c]; p[k] = Fr(c[k] + s); return tuple(p)
def spike_vertices(c, f):     # tip at the corner c + f; base = the 3 faces of the small cube meeting at that corner
    t = tuple(Fr(x) for x in tip(c, f))
    return [t] + [face_centre(c, k, f[k]) for k in range(3)]
tets = {(c, f): spike_vertices(c, f) for c, f in spikes}
nodes = {v for vs in tets.values() for v in vs}
edges = {frozenset((a, b)) for vs in tets.values() for a, b in itertools.combinations(vs, 2)}
check("G1. 63 nodes (Galeffi): 27 tips + 36 small-cube face centres", len(nodes) == 63)
check("G2. 240 segments (Galeffi)", len(edges) == 240)
faces = Counter(frozenset(t) for vs in tets.values() for t in itertools.combinations(vs, 3))
check("G3. 256 tetrahedron faces, no face shared by two tetrahedra (every face borders an octahedron or is bare)",
      sum(faces.values()) == 256 and set(faces.values()) == {1})
u = lambda p: tuple(x - 1 for x in p)                        # coordinates centred on the Field Origin
in_cubo = lambda p: all(abs(x) <= 1 for x in u(p)) and sum(abs(x) for x in u(p)) <= 2
in_octa = lambda p: sum(abs(x) for x in u(p)) <= 1
Vp = [v for v in itertools.product((1, -1), repeat=3) if v[0] * v[1] * v[2] == 1]; Vm = [tuple(-x for x in v) for v in Vp]
in_tet = lambda p, V: all(sum(a * b for a, b in zip(u(p), v)) >= -1 for v in V)
inside = lambda test: [(c, f) for (c, f), vs in tets.items() if all(test(v) for v in vs)]
cubo, octa = inside(in_cubo), inside(in_octa)
big = [(c, f) for (c, f), vs in tets.items() if all(in_tet(v, Vp) for v in vs) or all(in_tet(v, Vm) for v in vs)]
check("G4. 56 tetrahedra inside the cuboctahedron (vector equilibrium), 8 outside (Galeffi)", len(cubo) == 56)
check("G5. the 8 outside are exactly the outward spikes, relation d = 0 (A0): the large star's points",
      sorted(set(spikes) - set(cubo)) == sorted(x for x in spikes if d(*x) == 0))
check("G6. 8 tetrahedra inside the central octahedron (Galeffi): exactly the inward spikes, d = 3 (A3), meeting at the Field Origin",
      sorted(octa) == sorted(x for x in spikes if d(*x) == 3))
print("     tetrahedra inside the large stellated octahedron (2a):", len(big), " by relation d:", dict(Counter(d(*x) for x in big)))
import sympy as sp
r2 = sp.sqrt(2); A = sp.Symbol('a', positive=True)
v_tet, v_oct = r2 / 12 * (A / 2) ** 3, r2 / 3 * (A / 2) ** 3          # regular tetrahedron and octahedron of edge a/2
v_star = lambda L: r2 / 8 * L ** 3                                   # stellated octahedron with tetrahedron edge L
check("G7. inside the large stellated octahedron (2a): 40 tetrahedra, the A0 (8), A2 (24) and A3 (8) spikes. Galeffi's Table 3 gives 16",
      len(big) == 40 and Counter(d(*x) for x in big) == Counter({0: 8, 2: 24, 3: 8}))
check("G7b. volume settles it: 40 tetrahedra + the 14 octahedra fill the large star exactly (40 v_tet + 14 v_oct = sqrt2 a^3)",
      sp.simplify(40 * v_tet + 14 * v_oct - v_star(2 * A)) == 0 and sp.simplify(16 * v_tet + 14 * v_oct - v_star(2 * A)) != 0)
check("G7c. and the 24 A1 spikes are the only tetrahedra outside the large star: large star + 24 v_tet = 5 sqrt2 a^3 / 4, "
      "Galeffi's own total volume of the 64-TG (so his Table 3 count of 16, and its packing density 1/6, should read 40 and 5/12)",
      sorted(set(spikes) - set(big)) == sorted(x for x in spikes if d(*x) == 1)
      and sp.simplify(v_star(2 * A) + 24 * v_tet - 5 * r2 / 4 * A ** 3) == 0 and sp.nsimplify(40 * v_tet / v_star(2 * A)) == sp.Rational(5, 12))
check("G11. Galeffi's other three Table 3 densities are confirmed: 64-TG 64/(5sqrt2/4) -> 8/15, cuboctahedron 56 -> 7/20, "
      "octahedron 8 -> 1/4 (volumes of the cuboctahedron 5sqrt2 a^3/3 and octahedron sqrt2 a^3/3, edge a)",
      [sp.nsimplify(n * v_tet / V) for n, V in ((64, 5 * r2 / 4 * A ** 3), (len(cubo), 5 * r2 / 3 * A ** 3), (len(octa), r2 / 3 * A ** 3))]
      == [sp.Rational(8, 15), sp.Rational(7, 20), sp.Rational(1, 4)])
# the 14 octahedra: the 8 star cores (centred on the small-cube centres) and 6 more around the Field Origin
cores = {tuple(Fr(ci) + Fr(1, 2) for ci in c) for c in bits}
central = {tuple(Fr(1) + (Fr(1, 2) * s if i == k else 0) for i in range(3)) for k in range(3) for s in (1, -1)}
def octa_faces(cen, r):
    vs = [tuple(cen[i] + (r if i == k else 0) * s for i in range(3)) for k in range(3) for s in (1, -1)]
    return {frozenset(t) for t in itertools.combinations(vs, 3)
            if all(sum((a - b) ** 2 for a, b in zip(x, y)) == 2 * r * r for x, y in itertools.combinations(t, 2))}
oct_faces = set().union(*[octa_faces(cc, Fr(1, 2)) for cc in cores | central])
check("G8. 14 octahedral cavities = 8 star cores + 6 around the Field Origin; their 14 x 8 = 112 faces are all tetrahedron faces, "
      "leaving 144 bare (Galeffi)", len(cores | central) == 14 and len(oct_faces) == 112 and oct_faces <= set(faces) and 256 - 112 == 144)
check("G9. the 6 central octahedra point from the Field Origin to the 6 face centres, i.e. to the A2 tip points (the core octahedron's vertices)",
      {tuple(1 + 2 * (x - 1) for x in cen) for cen in central} == {tuple(int(v) for v in p) for p in face_cent})
pol = Counter(sum(f) % 2 for c, f in spikes)
check("G10. Galeffi's two polarities: the spikes split 32 + 32 by orientation, which is the chamber of the spike's own corner (f)",
      pol == Counter({0: 32, 1: 32}))
print(f"\n{sum(ok)}/{len(ok)} checks passed")
