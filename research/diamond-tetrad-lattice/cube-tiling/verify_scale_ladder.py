"""The closure tiling one level up: exact checks for results 10-12 of README.md (research, not a proof).
Cubes centred at 2n, side 2; corners p in (2Z+1)^3. Closure label of a corner: lambda(p) = -(-1)^((p1+p2+p3+3)/2)
(result 2 of README.md). Uniform label of a corner of the cube centred at c: xyz(p - c).
Run: python3 verify_scale_ladder.py
"""
import itertools
from fractions import Fraction as Fr

ok = []
def check(m, c): ok.append(bool(c)); print(("PASS " if c else "FAIL ") + m)
S = list(itertools.product((1, -1), repeat=3))
def xyz(v): return v[0] * v[1] * v[2]
def lam(p): return -(-1) ** (((sum(p) + 3) // 2) % 2)
def l1(v): return sum(abs(x) for x in v)
corners = list(itertools.product(range(-11, 12, 2), repeat=3))

print("=== 10. Dilation")
check("10a. dilation about a cube centre by k sends corners to corners exactly when k is odd; even k sends them onto "
      "cube centres", all(all((k * x) % 2 == 1 for x in p) == (k % 2 == 1) for k in range(1, 9) for p in corners))
check("10b. closure labels under odd dilation: lambda(k p) = (-1)^((k-1)/2) lambda(p). k = 1 mod 4 keeps every label, "
      "k = 3 mod 4 exchanges TetA and TetB",
      all(lam(tuple(k * x for x in p)) == (-1) ** ((k - 1) // 2) * lam(p) for k in (1, 3, 5, 7, 9, 11) for p in corners))

print("\n=== 11. Blocks of tiles as tiles")
def block_labels(n, o):
    """Block of n^3 tiles whose lowest cube is centred at 2o: labels of its 8 corners, keyed by direction s."""
    lo = [2 * o[i] - 1 for i in range(3)]; hi = [2 * (o[i] + n - 1) + 1 for i in range(3)]
    return {s: lam(tuple(lo[i] if s[i] < 0 else hi[i] for i in range(3))) for s in S}
def star(labs):
    A = [s for s, l in labs.items() if l == 1]
    return (len(A) == 4 and len({xyz(s) for s in A}) == 1), (xyz(A[0]) if A else 0)
origins = list(itertools.product(range(-3, 4), repeat=3))
check("11a. an n x n x n block's 8 corners form a labelled star (4 TetA corners making a tetrahedron) exactly when n is "
      "odd; for even n all 8 carry one chamber, which is the 64-grid note's observation for its 2 x 2 x 2 block",
      all({star(block_labels(n, o))[0] for o in origins} == ({True} if n % 2 else {False}) for n in range(1, 9))
      and all(len(set(block_labels(n, o).values())) == 1 for n in (2, 4, 6) for o in origins))
o0 = (-1, -1, -1)                                        # the 3 x 3 x 3 block centred on the tile at the origin
ref = star(block_labels(3, o0))[1]
blocks = list(itertools.product(range(-2, 3), repeat=3))
check("11b. the 3 x 3 x 3 blocks obey the closure rule as tiles: a block m steps away has its TetA orientation multiplied by "
      "(-1)^(m1+m2+m3), and neighbouring blocks agree at every shared corner because lambda is one global labelling",
      all(star(block_labels(3, tuple(3 * m[i] - 1 for i in range(3))))[1] == (-1) ** (sum(m) % 2) * ref for m in blocks))
check("11c. the block centred on a tile has the exchanged root: its TetA corners lie in the directions of the centre "
      "tile's TetB corners", ref == -xyz(next(s for s in S if lam(s) == 1)))
lad = [star({s: lam(tuple(3 ** L * x for x in s)) for s in S}) for L in range(7)]
check("11d. the ladder: tiles of side 2 x 3^L, L = 0..6, are all labelled stars, and the root exchanges at each step: "
      + str([o for _, o in lad]), all(a for a, _ in lad) and all(lad[i][1] == -lad[i + 1][1] for i in range(6)))

print("\n=== 12. The tile inside the composite's Field Origin (block centred at the origin, corners (+-3)^3)")
# the composite's core octahedron is |x|+|y|+|z| <= 3; its face with normal s is the triangle with vertices 3 s_j e_j
def face_centroid(s): return tuple(Fr(3 * s[i], 3) for i in range(3))
check("12a. the centre tile lies inside the composite's Field Origin, and its 8 corners are exactly the centroids of the "
      "Field Origin's 8 faces", all(l1(s) <= 3 for s in S) and {face_centroid(s) for s in S} == {tuple(Fr(x) for x in s) for s in S})
tiles27 = list(itertools.product((-1, 0, 1), repeat=3))
inside = [m for m in tiles27 if all(l1(tuple(2 * m[i] + s[i] for i in range(3))) <= 3 for s in S)]
check("12b. it is the only whole tile inside the composite's Field Origin: every other tile of the block has a corner outside",
      inside == [(0, 0, 0)])
compA = [s for s in S if lam(tuple(3 * x for x in s)) == 1]             # composite TetA vertices 3t
# the composite TetA's face opposite vertex 3t lies in the plane (-t).x = 3, i.e. its outward normal is -t
check("12c. (geometry) each composite-TetA face lies in a plane u.x = 3 with u = -t, t the vertex it faces",
      all(sum(-t[i] * 3 * w[i] for i in range(3)) == 3 for t in compA for w in compA if w != t))
normalsA = {tuple(-x for x in t) for t in compA}
cenA = {s for s in S if lam(s) == 1}
check("12d. closure: the centre tile's TetA corners sit on the composite TetA's faces and its TetB corners on the composite "
      "TetB's faces. Across the two levels TetA meets TetA and TetB meets TetB", cenA == normalsA)
compA_U = [s for s in S if xyz(s) == 1]
check("12e. uniform, by contrast: the composite carries the same orientation as the tile (no exchange), so the centre "
      "tile's TetA corners sit on the composite TetB's faces and the chambers cross between the levels",
      {s for s in S if xyz(s) == 1}.isdisjoint({tuple(-x for x in t) for t in compA_U}))

print(f"\n{sum(ok)}/{len(ok)} checks passed")
