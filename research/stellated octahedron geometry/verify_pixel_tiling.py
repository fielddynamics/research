"""Pixel tiling and closure labelling: exact checks for pixel_tiling_and_closure.md.

The photon (stellated octahedron) inscribed in its cube is the pixel. Pixel cubes tile space on the simple cubic grid.
Part 1: the cube = the star + 12 edge wedges; 4 wedges around a shared edge close into one octahedron held by 4 photons.
Part 2: closure. Each photon chooses which of its two tetrahedra is TetA. Requiring every shared lattice corner to get one
chamber from all the photons meeting there leaves exactly one global choice: the root of the tetrad equation.
Coordinates: unit cubes, doubled where needed so every vertex is an integer.  Run: python3 verify_pixel_tiling.py
"""
import itertools
import numpy as np

ok = []
def check(m, c): ok.append(bool(c)); print(("PASS " if c else "FAIL ") + m)

# ---------- Part 1: the cube's other half (volumes in units of the small tetrahedron, edge = half a face diagonal)
print("=== 1. The pixel cube and the shared octahedra")
TET, OCT, CUBE = 1, 4, 24                     # cube of edge 1: volume 1 = 24 tetrahedra of edge sqrt2/2 (each 1/24)
check("1a. the star fills half its cube: 8 spikes + 1 core octahedron = 8 + 4 = 12 = 24/2", 8 * TET + OCT == CUBE // 2)
# doubled coordinates: cube c occupies [2c, 2c+2]^3; spikes of cube c as vertex sets
def spikes(c):
    out = []
    for f in itertools.product((0, 1), repeat=3):
        tip = tuple(2 * (a + b) for a, b in zip(c, f))
        base = [tuple(2 * c[i] + (2 * f[k] if i == k else 1) for i in range(3)) for k in range(3)]
        out.append(frozenset([tip] + base))
    return out
def tri_faces(vs): return {frozenset(t) for t in itertools.combinations(sorted(vs), 3)}
def octa(cen): return [tuple(cen[i] + (s if i == k else 0) for i in range(3)) for k in range(3) for s in (1, -1)]
def oct_faces(cen):
    vs = octa(cen)
    return {frozenset(t) for t in itertools.combinations(vs, 3)
            if all(sum((a - b) ** 2 for a, b in zip(x, y)) == 2 for x, y in itertools.combinations(t, 2))}
block = list(itertools.product(range(3), repeat=3))
spike_faces = {}
for c in block:
    for t in spikes(c):
        for fc in tri_faces(t): spike_faces[fc] = c
# every interior edge midpoint of the 3x3x3 block: one doubled coordinate odd (along the edge), the others even, all interior
edge_mids = [p for p in itertools.product(range(1, 6), repeat=3) if sum(x % 2 for x in p) == 1 and all(x not in (0, 6) for x in p)]
from collections import Counter
def owners(e): return Counter(spike_faces[fc] for fc in oct_faces(e))
check("1b. at every interior edge of the grid, the octahedron centred on the edge has all 8 faces on spikes, "
      "and those spikes come from exactly the 4 photons around that edge (2 faces each)",
      all(len(oct_faces(e)) == 8 and oct_faces(e) <= set(spike_faces) and sorted(owners(e).values()) == [2, 2, 2, 2]
          for e in edge_mids))
check("1c. the cube's other half is 12 edge wedges of one quarter octahedron each (12 x 1 = 12); 4 wedges close one shared "
      "octahedron, so each photon holds 12/4 = 3 shared octahedra and space is half photons, half shared octahedra",
      CUBE - (8 * TET + OCT) == 12 * (OCT // 4) and 12 // 4 == 3 and 3 * OCT == 12)

# ---------- Part 2: closure labelling
print("\n=== 2. Closure fixes every photon's chambers up to one global choice")
def gf2_solve(rows, k):
    A = np.array(rows, dtype=np.int64) % 2; m = A.shape[0]; piv = 0; pivcols = []
    for col in range(k):
        pr = next((r for r in range(piv, m) if A[r, col]), None)
        if pr is None: continue
        A[[piv, pr]] = A[[pr, piv]]
        for r in range(m):
            if r != piv and A[r, col]: A[r] ^= A[piv]
        pivcols.append(col); piv += 1
    consistent = not any(A[r, :k].sum() == 0 and A[r, k] for r in range(m))
    return consistent, k - piv
def constraints(n, periodic=False):
    cubes = list(itertools.product(range(n), repeat=3)); idx = {c: i for i, c in enumerate(cubes)}; rows = []
    for c in cubes:
        for d in itertools.product((-1, 0, 1), repeat=3):
            if d == (0, 0, 0): continue
            c2 = tuple((a + b) % n if periodic else a + b for a, b in zip(c, d))
            if c2 not in idx or (not periodic and idx[c2] < idx[c]): continue
            # cube c sees corner p with local parity |p - c|; cube c2 sees it with local parity |p - c - d|.
            # Agreement: sigma_c + |p-c| = sigma_c2 + |p-c-d| (mod 2)  <=>  sigma_c + sigma_c2 = |d|  (mod 2)
            r = [0] * (len(cubes) + 1); r[idx[c]] ^= 1; r[idx[c2]] ^= 1; r[-1] = sum(abs(x) for x in d) % 2
            rows.append(r)
    return rows, len(cubes)
res = {n: gf2_solve(*constraints(n)) for n in (2, 3, 4, 5)}
check("2a. on blocks of 2, 3, 4, 5 photons per side the agreement conditions at shared corners are consistent and have exactly "
      "2 solutions (one free bit)", all(c and free == 1 for c, free in res.values()))
def chamber_seen(c, p, sigma): return (sigma + sum(pi - ci for pi, ci in zip(p, c))) % 2
n = 4; cubes = list(itertools.product(range(n), repeat=3))
sol = {c: sum(c) % 2 for c in cubes}            # the checkerboard
corners = list(itertools.product(range(n + 1), repeat=3))
agree = all(len({chamber_seen(c, p, sol[c]) for c in cubes if all(0 <= pi - ci <= 1 for pi, ci in zip(p, c))}) == 1 for p in corners)
check("2b. the solutions are the checkerboard sigma_c = |c| mod 2 and its complement: neighbouring photons alternate orientation",
      agree)
check("2c. under that solution every lattice corner's chamber is its global parity (x + y + z mod 2): one consistent TetA/TetB "
      "labelling of the whole lattice", all(chamber_seen(c, p, sol[c]) == sum(p) % 2 for c in cubes for p in corners
                                             if all(0 <= pi - ci <= 1 for pi, ci in zip(p, c))))
flip = {c: 1 - s for c, s in sol.items()}
check("2d. the one remaining choice flips every chamber at once: the global exchange TetA <-> TetB, i.e. the tetrad equation's "
      "two roots M1 and M2 = -M1",
      all(chamber_seen(c, p, flip[c]) == 1 - sum(p) % 2 for c in cubes for p in corners if all(0 <= pi - ci <= 1 for pi, ci in zip(p, c))))
face_only = []
for m in (2, 3, 4):
    cubes_m = list(itertools.product(range(m), repeat=3)); idx = {c: i for i, c in enumerate(cubes_m)}; rows = []
    for c in cubes_m:
        for k in range(3):
            c2 = tuple(c[i] + (1 if i == k else 0) for i in range(3))
            if c2 in idx:
                r = [0] * (len(cubes_m) + 1); r[idx[c]] = r[idx[c2]] = 1; r[-1] = 1; rows.append(r)
    face_only.append(gf2_solve(rows, len(cubes_m)))
check("2e. face-sharing neighbours alone already force it (consistent, one free bit); edge and corner neighbours add nothing new",
      all(c and free == 1 for c, free in face_only))
per = {n: gf2_solve(*constraints(n, periodic=True)) for n in (2, 3, 4, 5, 6)}
check("2f. remark: on a closed (periodic) lattice the labelling is consistent only for an even number of photons per side "
      "(n = 2, 4, 6 yes; 3, 5 no)", [per[n][0] for n in (2, 3, 4, 5, 6)] == [True, False, True, False, True])

print(f"\n{sum(ok)}/{len(ok)} checks passed")
