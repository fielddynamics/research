"""Exact checks for research/diamond-tetrad-lattice/README.md.

The tetrad's two roots, TetA = M (cube corners with xyz = +1) and
TetB = -M (xyz = -1), used as bond stars of a lattice.

Run:  python verify_diamond_tetrad_lattice.py
"""
import itertools
from collections import deque

import sympy as sp

passed = failed = 0


def check(label, ok):
    global passed, failed
    if ok:
        passed += 1
    else:
        failed += 1
    print(("PASS " if ok else "FAIL ") + label)


def add(p, v, s=1):
    return tuple(a + s * b for a, b in zip(p, v))


TETA = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
TETB = [tuple(-c for c in v) for v in TETA]
M = sp.Matrix(TETA).T

# 1. The bond star --------------------------------------------------------
G = M.T * M
check("1.1 Gram of TetA's legs is 4I - J (each leg length^2 3, each pair -1)",
      G == 4 * sp.eye(4) - sp.ones(4, 4))
check("1.2 so the bond angle is the tetrahedral angle, cos = -1/3",
      all(sp.Rational(G[i, j], G[i, i]) == sp.Rational(-1, 3) for i in range(4) for j in range(4) if i != j))
check("1.3 TetA = cube corners with xyz = +1, TetB = those with xyz = -1",
      all(v[0] * v[1] * v[2] == 1 for v in TETA) and all(v[0] * v[1] * v[2] == -1 for v in TETB))
check("1.4 together they are the 8 cube corners: the stellated octahedron",
      sorted(TETA + TETB) == sorted(itertools.product((1, -1), repeat=3)))
check("1.5 TetB = -TetA: spatial inversion (the parity root) maps one star onto the other",
      sorted(TETB) == sorted(tuple(-c for c in v) for v in TETA))

# 2. Reciprocity: one root cannot close ------------------------------------
check("2.1 no reversed TetA leg is a TetA leg (TetA and -TetA are disjoint)",
      not set(TETA) & set(TETB))
check("2.2 so a net whose sites all carry TetA has no bond that runs both ways",
      all(tuple(-c for c in v) not in TETA for v in TETA))
check("2.3 a site that bonds back along every leg must carry -TetA = TetB",
      all(tuple(-c for c in v) in TETB for v in TETA))

# 3. Alternating the roots builds the diamond lattice ----------------------
R, r = 11, 6
seen = {((0, 0, 0), +1)}
queue = deque(seen)
while queue:
    p, s = queue.popleft()
    for v in TETA:
        q = add(p, v, s)               # s = +1 carries TetA, s = -1 carries TetB
        if max(map(abs, q)) <= R and (q, -s) not in seen:
            seen.add((q, -s))
            queue.append((q, -s))
A = {p for p, s in seen if s == +1}
B = {p for p, s in seen if s == -1}
box = list(itertools.product(range(-r, r + 1), repeat=3))
fcc_a = {p for p in box if all(c % 2 == 0 for c in p) and sum(p) % 4 == 0}
fcc_b = {p for p in box if all(c % 2 for c in p) and sum(p) % 4 == 3}
inner = lambda S: {p for p in S if max(map(abs, p)) <= r}
check("3.1 no site is reached carrying both roots (the alternation is consistent)", not A & B)
check("3.2 TetA sites are exactly an fcc lattice", inner(A) == fcc_a)
check("3.3 TetB sites are exactly that fcc lattice shifted by (1,1,1)", inner(B) == fcc_b)
check("3.4 so the net is the diamond lattice (two fcc lattices offset along a body diagonal)",
      inner(B) == {add(p, (1, 1, 1)) for p in fcc_a if max(map(abs, add(p, (1, 1, 1)))) <= r})
far = lambda p: max(map(abs, p)) > R - 2
check("3.5 every site has exactly 4 neighbours, all carrying the other root",
      all(sum(add(p, v) in B for v in TETA) == 4 for p in A if not far(p))
      and all(sum(add(p, v) in A for v in TETB) == 4 for p in B if not far(p)))
check("3.6 every bond runs both ways",
      all(add(add(p, v), tuple(-c for c in v)) == p and tuple(-c for c in v) in TETB for p in A for v in TETA))
span = {tuple(i * a + j * b + k * c for a, b, c in zip((2, 2, 0), (2, 0, 2), (0, 2, 2)))
        for i, j, k in itertools.product(range(-8, 9), repeat=3)}
check("3.7 the TetA sites are the lattice spanned by (2,2,0), (2,0,2), (0,2,2): fcc",
      fcc_a == {p for p in span if max(map(abs, p)) <= r})

# 4. Parity is the lattice's own inversion ---------------------------------
mid = (sp.Rational(1, 2),) * 3
inv = lambda p: tuple(2 * m - c for m, c in zip(mid, p))
check("4.1 inversion through a bond midpoint maps TetA sites onto TetB sites",
      all(inv(p) in B for p in A if max(map(abs, p)) <= r - 1))
check("4.2 and maps each TetA site's bonds onto its image's TetB bonds",
      all(inv(add(p, v)) == add(inv(p), v, -1) and add(inv(p), v, -1) in A
          for p in A if max(map(abs, p)) <= r - 2 for v in TETA))

# 5. Second neighbours and rings -------------------------------------------
second = {tuple(a - b for a, b in zip(v, w)) for v in TETA for w in TETA if v != w}
fcc12 = {q for p in set(itertools.permutations((2, 2, 0)))
         for q in itertools.product(*[(c, -c) if c else (0,) for c in p])}
check("5.1 same-root (second) neighbours are the 12 fcc vectors: the tetrahedron's edges",
      second == fcc12 and len(second) == 12)


def nbrs(p):
    return [add(p, v) for v in (TETA if p in A else TETB)]


def girth_through(p):
    """Shortest cycle through site p, by BFS from p tracking the first branch."""
    best = None
    dist, branch = {p: 0}, {p: None}
    dq = deque()
    for q in nbrs(p):
        dist[q], branch[q] = 1, q
        dq.append(q)
    while dq:
        u = dq.popleft()
        for w in nbrs(u):
            if w == p:
                continue
            if w not in dist:
                dist[w], branch[w] = dist[u] + 1, branch[u]
                dq.append(w)
            elif branch[w] != branch[u]:
                L = dist[u] + dist[w] + 1
                best = L if best is None else min(best, L)
        if best is not None and dist[u] * 2 > best:
            break
    return best


def count_rings(p, L=6):
    """Number of simple cycles of length L through p."""
    n = 0

    def walk(path):
        nonlocal n
        u = path[-1]
        for w in nbrs(u):
            if len(path) == L and w == p:
                n += 1
            elif len(path) < L and w not in path:
                walk(path + [w])

    walk([p])
    return n // 2


check("5.2 the smallest rings are hexagons (girth 6), at a TetA and a TetB site",
      girth_through((0, 0, 0)) == 6 and girth_through((1, 1, 1)) == 6)
check("5.3 12 hexagons pass through every site", count_rings((0, 0, 0)) == 12 and count_rings((1, 1, 1)) == 12)

# 6. What reciprocity alone does not fix -----------------------------------
v = sp.Matrix(TETA[0]) / sp.sqrt(3)
K = sp.Matrix([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
Rot = sp.simplify(sp.eye(3) + sp.sin(sp.pi / 3) * K + (1 - sp.cos(sp.pi / 3)) * K * K)  # 60 deg about leg 1
star_B = [sp.Matrix(w) for w in TETB]
rot_star = [sp.simplify(Rot * w) for w in star_B]
check("6.1 TetB turned 60 deg about the bond still bonds back (-v is kept)",
      any(sp.simplify(w + sp.Matrix(TETA[0])) == sp.zeros(3, 1) for w in rot_star))
check("6.2 but it is no longer the parity root -TetA (a turn of this kind gives the eclipsed bond of hexagonal stacking)",
      sorted(tuple(w) for w in rot_star) != sorted(TETB))
check("6.3 and its Gram matrix is unchanged, so the metric cannot tell the two stackings apart",
      sp.simplify(sp.Matrix.hstack(*rot_star).T * sp.Matrix.hstack(*rot_star)) == G)

# 7. The cubic tiling of pixels --------------------------------------------
# Cubes of side 2 centred on the odd points. Each cube holds one whole
# stellated octahedron: its centre is the pixel's Field Origin, its 8 legs
# run to its own 8 corners (the even points), which neighbouring cubes share.
Rc = 9
centres = {p for p in itertools.product(range(-Rc, Rc + 1), repeat=3) if all(c % 2 for c in p)}
corners = {p for p in itertools.product(range(-Rc, Rc + 1), repeat=3) if all(c % 2 == 0 for c in p)}
c0 = (1, 1, 1)
check("7.1 each stellated octahedron lies in one cube: its 8 vertices are that cube's corners",
      sorted(add(c0, v) for v in TETA + TETB) == sorted(itertools.product((0, 2), repeat=3)))
o = (0, 0, 0)
around = [c for c in centres if max(map(abs, c)) == 1]
roles = [add(o, c, -1) in TETA for c in around]
check("7.2 each corner is shared by 8 cubes: a TetA vertex in 4 and a TetB vertex in the other 4",
      len(around) == 8 and roles.count(True) == 4)
face = [(0, 0, 0), (2, 0, 0), (0, 2, 0), (2, 2, 0)]
c1, c2 = (1, 1, 1), (1, 1, -1)
check("7.3 across every face the cubes swap: a shared corner is TetA in one, TetB in the other",
      all((add(k, c1, -1) in TETA) != (add(k, c2, -1) in TETA) for k in face))
check("7.4 so on a shared face one cube's TetA edge is the next cube's TetB edge",
      {k for k in face if add(k, c1, -1) in TETA} == {k for k in face if add(k, c2, -1) in TETB})


def leg_graph(legs):
    adj = {}
    for c in centres:
        for v in legs:
            k = add(c, v)
            if k in corners:
                adj.setdefault(c, set()).add(k)
                adj.setdefault(k, set()).add(c)
    comps, seen = [], set()
    for st in adj:
        if st in seen:
            continue
        comp, dq = {st}, deque([st])
        seen.add(st)
        while dq:
            u = dq.popleft()
            for w in adj[u]:
                if w not in seen:
                    seen.add(w); comp.add(w); dq.append(w)
        comps.append(comp)
    return adj, comps


adjA, compA = leg_graph(TETA)
check("7.5 at each corner the TetA legs of its 4 cubes arrive as a TetB-shaped star",
      sorted(add(c, o, -1) for c in adjA[o]) == sorted(TETB))
check("7.6 the TetA legs of all cubes, joined at the corners, form two separate nets",
      len(compA) == 2)
shift = {add(p, (1, 1, 1)) for p in fcc_a | fcc_b}
inbox = lambda S, m: {p for p in S if max(map(abs, p)) <= m}
check("7.7 one of them is exactly the diamond lattice of results 3-4, moved by (1,1,1)",
      any(inbox(comp, r - 1) == inbox(shift, r - 1) for comp in compA))
check("7.7 and the other is the same diamond moved by one cube, (2,0,0)",
      inbox(compA[0], r - 3) == inbox({add(p, (2, 0, 0)) for p in compA[1]}, r - 3)
      or inbox(compA[1], r - 3) == inbox({add(p, (2, 0, 0)) for p in compA[0]}, r - 3))
check("7.8 and its nodes alternate cube centre (Field Origin, TetA star) and shared corner (TetB star)",
      all(all(c in centres for c in adjA[k]) for k in corners if k in adjA)
      and all(all(k in corners for k in adjA[c]) for c in centres if c in adjA))
adjB, compB = leg_graph(TETB)
check("7.9 the TetB legs form two more diamond nets the same way",
      len(compB) == 2 and sorted(add(c, o, -1) for c in adjB[o]) == sorted(TETA))

print(f"\n{passed}/{passed + failed} checks passed")
raise SystemExit(failed)
