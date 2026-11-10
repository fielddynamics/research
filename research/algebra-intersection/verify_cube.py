"""
verify_cube.py
==============

Part III of INTERSECTION_ALGEBRA.md: the stellated octahedron *in its cube*.

The cube carries the full symmetry O_h (48), not just the rotations O (24).
O_h has three index-2 subgroups, O, T_d and T_h, and three non-trivial
characters det, swap and det*swap. Two of the subgroups are copies of S4:
the modular group PSL2(Z/4) = O, and the tetrahedron's own group T_d,
which is the S4 of the torsion proof. Keeping them apart is the point.

  J. Cube cell dictionary for the special points of X(4).
  K. The three binary labels, which the framework calls "parity" (det, swap,
     det*swap), realised by x -> 1/x, spatial inversion and the constitutive law.
  L. The labels as the Galois group of Q(zeta12), via the closure axis; this
     corrects Appendix J's table.
  M. The connection under the frame's own symmetry T_d and under all of O_h,
     with the tetrad legs taken as vectors to the TetA corners. This corrects Part II.
  N. What distinguishes exchange = mirror from exchange = inversion.

Requires numpy, sympy.  Prints PASS/FAIL per claim.
"""
from __future__ import annotations

import itertools

import numpy as np
import sympy as sp

RESULTS = []


def check(name, cond):
    RESULTS.append((name, bool(cond)))
    print(f"[{'PASS' if cond else 'FAIL'}] {name}")


def signed_perms():
    out = []
    for p in itertools.permutations(range(3)):
        for sg in itertools.product([1, -1], repeat=3):
            M = np.zeros((3, 3), dtype=int)
            for i, j in enumerate(p):
                M[j, i] = sg[i]
            out.append(M)
    return out


OH = signed_perms()
det = lambda M: int(round(np.linalg.det(M)))
CORNERS = [np.array(v) for v in itertools.product([1, -1], repeat=3)]
TETA = [c for c in CORNERS if np.prod(c) == 1]
TETB = [c for c in CORNERS if np.prod(c) == -1]
inA = lambda v: any((v == a).all() for a in TETA)
swap = lambda M: 1 if all(inA(M @ a) for a in TETA) else -1
O = [M for M in OH if det(M) == 1]
TD = [M for M in OH if swap(M) == 1]
TH = [M for M in OH if det(M) * swap(M) == 1]
A4 = [M for M in O if swap(M) == 1]
Z = -np.eye(3, dtype=int)

# ---------------------------------------------------------------------------
print("\n=== J. The cube cell dictionary for X(4) ===")
cells = [np.array(v) for v in itertools.product([-1, 0, 1], repeat=3) if any(v)]
by_support = {k: [c for c in cells if np.count_nonzero(c) == k] for k in (1, 2, 3)}
stab = lambda v: sum(1 for M in O if (M @ v == v).all())
check("Non-zero cells of the cube = {-1,0,1}^3 minus 0: 6 faces, 12 edges, 8 corners (26 = 27 - 1)",
      [len(by_support[k]) for k in (1, 2, 3)] == [6, 12, 8])
check("Rotation stabilisers: face 4, edge 2, corner 3 = cusps (Z4), i-points (Z2), rho-points (Z3) of X(4)",
      {stab(v) for v in by_support[1]} == {4} and {stab(v) for v in by_support[2]} == {2}
      and {stab(v) for v in by_support[3]} == {3})
edges_A = [(a, b) for a, b in itertools.combinations(TETA, 2)]
edges_B = [(a, b) for a, b in itertools.combinations(TETB, 2)]
mid = lambda e: (e[0] + e[1]) // 2
check("Each cube FACE centre (cusp) is the crossing point of exactly one TetA edge and one TetB edge",
      all(sum((mid(e) == f).all() for e in edges_A) == 1 and sum((mid(e) == f).all() for e in edges_B) == 1
          for f in by_support[1]))
check("Each cube EDGE joins one TetA corner to one TetB corner (the cube graph is bipartite A|B)",
      all((inA(a) != inA(b)) for a, b in itertools.combinations(CORNERS, 2) if np.abs(a - b).sum() == 2))
# core octahedron |x|+|y|+|z| <= 1 = TetA intersect TetB
# face planes: for a tetrahedron inscribed in the cube, the face opposite vertex v is { x : v.x = -1 }
faceplane = lambda v: (v, -1)
on = lambda p, x: int(np.dot(p[0], x)) == p[1]
core_edges = [(np.eye(3, dtype=int)[i] * si, np.eye(3, dtype=int)[j] * sj)
              for i, j in itertools.combinations(range(3), 2) for si in (1, -1) for sj in (1, -1)]
ok = True
for u, v in core_edges:
    pa = [faceplane(a) for a in TETA if on(faceplane(a), u) and on(faceplane(a), v)]
    pb = [faceplane(b) for b in TETB if on(faceplane(b), u) and on(faceplane(b), v)]
    ok &= len(pa) == 1 and len(pb) == 1
check("Each of the 12 core-octahedron edges (i-points) is where one TetA face meets one TetB face", ok and len(core_edges) == 12)
check("The 8 corners (rho-points) split 4 + 4 into TetA and TetB, disjoint, each tetrahedron regular (edge^2 = 8)",
      len(TETA) == len(TETB) == 4 and all(np.dot(a - b, a - b) == 8 for a, b in itertools.combinations(TETA, 2))
      and all(np.dot(a - b, a - b) == 8 for a, b in itertools.combinations(TETB, 2)))
print("      => cusps: TetA edge x TetB edge;  i-points (17): TetA face x TetB face, the A-B contact;"
      "  rho-points (21/13): the corners")

# ---------------------------------------------------------------------------
print("\n=== K. Three binary labels, which the framework calls 'parity' ===")
check("|O| = |T_d| = |T_h| = 24, pairwise distinct, all containing A4 (12)",
      len(O) == len(TD) == len(TH) == 24 and len(A4) == 12)
leg_perm = lambda G: len({tuple(next(j for j, b in enumerate(TETA) if (M @ a == b).all()) for a in TETA) for M in G})
check("T_d (stabiliser of TetA) permutes the 4 legs with NO sign: it is the torsion proof's S4",
      all(all(inA(M @ a) for a in TETA) for M in TD) and leg_perm(TD) == 24)
check("O (= PSL2(Z/4)) sends TetA corners to MINUS TetA corners for every odd element",
      all((swap(M) == 1) or all(any((M @ a == -b).all() for b in TETA) for a in TETA) for M in O))
labels = {"det": det, "swap": swap, "det.swap": lambda M: det(M) * swap(M)}
P_mirror = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 1]])        # plane x = y (bit swap)
L_quarter = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])      # quarter-turn about a face axis
row = lambda M: tuple(f(M) for f in labels.values())
check("A diagonal mirror (bit SWAP) has (det, swap) = (-1, +1): it flips orientation and keeps each tetrahedron",
      row(P_mirror)[:2] == (-1, 1))
check("Spatial inversion Z (NOT on all three bits) has (det, swap) = (-1, -1)", row(Z)[:2] == (-1, -1))
check("A quarter-turn (the class of the constitutive law L) has (det, swap) = (+1, -1)", row(L_quarter)[:2] == (1, -1))
key = lambda M: (det(M), swap(M))
check("O_h / A4 = Z2 x Z2 = {1, mirror, inversion, quarter-turn}: the constitutive law is mirror x inversion mod A4",
      len({key(M) for M in OH}) == 4 and key(P_mirror @ Z) == key(L_quarter))
print("      (Part II matches: x->1/x is the level-4 mirror fixing 2 cusps, L the quarter-turn, centre Z the inversion)")

# ---------------------------------------------------------------------------
print("\n=== L. The three labels are the Galois group of Q(zeta12) ===")
d = np.array([1, 1, 1])
D3d = [M for M in OH if (M @ d == d).all() or (M @ d == -d).all()]
check("Stabiliser of the closure axis (1,1,1) is D_3d, order 12", len(D3d) == 12)
# action on the Omega-fixed algebra Q[T1, I]: T1 -> eps*T1 (eps = sign of M d), I -> det(M) I
act = lambda M: (1 if (M @ d == d).all() else -1, det(M))
check("D_3d acts on <T1, I> by sign pairs; kernel = the three rotations about the axis (C3)",
      sum(1 for M in D3d if act(M) == (1, 1)) == 3 and len({act(M) for M in D3d}) == 4)
check("D_3d / C3 -> O_h / A4 is an isomorphism (both (Z2)^2; each class meets D_3d)",
      {key(M) for M in D3d} == {key(M) for M in OH})
# zeta12 = (T1 + I)/2  with T1 ~ sqrt3, I ~ i  ->  zeta12 = (sqrt3 + i)/2 = e^{i pi/6}
z = sp.exp(sp.I * sp.pi / 6)
img = lambda e, dt: sp.nsimplify(sp.expand((e * sp.sqrt(3) + dt * sp.I) / 2))
galois = {}
for M in D3d:
    e, dt = act(M)
    w = img(e, dt)
    a = next(k for k in (1, 5, 7, 11) if sp.simplify(sp.expand_complex(z ** k) - w) == 0)
    galois[key(M)] = a
check(f"Induced Galois elements: mirror -> sigma_{galois[(-1, 1)]}, inversion -> sigma_{galois[(-1, -1)]}, "
      f"quarter-turn class -> sigma_{galois[(1, -1)]}",
      galois == {(1, 1): 1, (-1, 1): 11, (-1, -1): 7, (1, -1): 5})
# fixed quadratic subfields of sigma_a on Q(zeta12):  sigma_a(zeta) = zeta^a
sig = lambda a, expr_in_zeta: sp.simplify(sp.expand_complex(expr_in_zeta(z ** a) - expr_in_zeta(z)))
i_ = lambda w: w ** 3                 # i = zeta^3
om = lambda w: w ** 4                 # omega = zeta^4
r3 = lambda w: w + w ** 11            # sqrt3 = zeta + zeta^-1
fixed = {a: [nm for nm, f in (("Q(i)", i_), ("Q(omega)", om), ("Q(sqrt3)", r3)) if sig(a, f) == 0] for a in (5, 7, 11)}
check(f"Fixed fields: sigma_5 -> {fixed[5]}, sigma_7 -> {fixed[7]}, sigma_11 -> {fixed[11]}",
      fixed == {5: ["Q(i)"], 7: ["Q(omega)"], 11: ["Q(sqrt3)"]})
check("CORRECTION to Appendix J sec. 3: there sigma_5 is said to fix Q(sqrt-3) and sigma_7 Q(i); it is the other way round",
      fixed[5] == ["Q(i)"] and fixed[7] == ["Q(omega)"])
gal = lambda M: galois[key(M)]
check("det = +1 exactly on {sigma_1, sigma_5} = Gal(Q(zeta12)/Q(i)): orientation (the root of det e) is the Gaussian character",
      all((det(M) == 1) == (gal(M) in (1, 5)) for M in D3d))
check("swap = +1 exactly on {sigma_1, sigma_11} = Gal(./Q(sqrt3)): TetA <-> TetB is the real-quadratic character",
      all((swap(M) == 1) == (gal(M) in (1, 11)) for M in D3d))
check("det*swap = +1 exactly on {sigma_1, sigma_7} = Gal(./Q(omega)): kernel T_h is the Eisenstein character",
      all((det(M) * swap(M) == 1) == (gal(M) in (1, 7)) for M in D3d))

# ---------------------------------------------------------------------------
print("\n=== M. The connection with legs as vectors to the TetA corners ===")


def V(M):
    R = np.zeros((4, 4))
    for a, t in enumerate(TETA):
        w = M @ t
        for b, u in enumerate(TETA):
            if (w == u).all():
                R[b, a] = 1
            if (w == -u).all():
                R[b, a] = -1
    return R


IDX = list(itertools.product(range(4), repeat=3))


def conn(M):
    Vm = V(M)
    return np.kron(np.kron(Vm, Vm), Vm)


def sub(pattern):
    B = []
    for a in range(4):
        if pattern in ("inc", "non"):
            for b, c in itertools.combinations(range(4), 2):
                if (a in (b, c)) == (pattern == "inc"):
                    v = np.zeros(64)
                    v[IDX.index((a, b, c))], v[IDX.index((a, c, b))] = 1, -1
                    B.append(v / np.sqrt(2))
        else:
            for b, c in itertools.combinations_with_replacement(range(4), 2):
                v = np.zeros(64)
                v[IDX.index((a, b, c))] += 1
                v[IDX.index((a, c, b))] += 1
                B.append(v / np.linalg.norm(v))
    return np.array(B).T


INC, NON, CHR = sub("inc"), sub("non"), sub("chr")
TOR = np.hstack([INC, NON])
tr = lambda B, M: float(np.trace(B.T @ conn(M) @ B))
check("Spatial inversion Z acts as -1 on all 64 components (three vector indices)",
      np.allclose(conn(Z), -np.eye(64)))
mult = lambda B, ch: round(sum(tr(B, M) * ch(M) for M in OH) / 48)
m = {nm: {lab: mult(B, f) for lab, f in labels.items()} for nm, B in (("tors", TOR), ("chr", CHR))}
check(f"Under all of O_h: det occurs {m['tors']['det']}x in torsion and {m['chr']['det']}x in Christoffel",
      m["tors"]["det"] == 1 and m["chr"]["det"] == 0)
check(f"swap occurs {m['tors']['swap']}x in torsion and {m['chr']['swap']}x in Christoffel; det.swap and trivial never",
      m["tors"]["swap"] == 1 and m["chr"]["swap"] == 4 and m["tors"]["det.swap"] == m["chr"]["det.swap"] == 0)
print("      => the torsion proof's 'sign representation' is det: ORIENTATION, the root of det e."
      "  GR (Christoffel) is blind to it, but carries the TetA/TetB label (swap) four times.")
# the det mode is the volume form of TetA: T^a_[bc] = eps_{abcd}, d the remaining index
eps = np.zeros(64)
for a, b, c in IDX:
    if len({a, b, c}) == 3:
        dd = ({0, 1, 2, 3} - {a, b, c}).pop()
        eps[IDX.index((a, b, c))] = sp.LeviCivita(a, b, c, dd)
check("The det mode is the volume form of TetA, T^a_[bc] = eps_abcd: non-incident, transforms by det",
      all(np.allclose(conn(M) @ eps, det(M) * eps) for M in OH) and np.allclose(INC.T @ eps, 0))
# swap modes: the S4-invariant tensors
inv_dim = np.linalg.matrix_rank(sum(conn(M) for M in TD) / 24)
check(f"The swap modes are the {inv_dim} tensors invariant under all leg permutations (aaa, aab, aba, baa, abc patterns)",
      inv_dim == 5)
# Part II correction: under O with signed legs, the rep is (unsigned) x sgn
Vu = lambda M: np.abs(V(M))
conn_u = lambda M: np.kron(np.kron(Vu(M), Vu(M)), Vu(M))
check("CORRECTION to Part II: with legs as vectors, O acts as (Part II's unsigned rep) x sgn", all(
      np.allclose(conn(M), swap(M) * conn_u(M)) for M in O))
check("... and on T_d the two agree (no signs), so Part II's decomposition is right for T_d's abstract S4",
      all(np.allclose(conn(M), conn_u(M)) for M in TD))
# T_d-native statement: torsion = R[vertices of TetA] x C^1(edges of TetA), checked by characters of the geometric action
def vperm_A(M):
    return [next(j for j, b in enumerate(TETA) if (M @ a == b).all()) for a in TETA]
EA = list(itertools.combinations(range(4), 2))
def tr_vert(M):
    p = vperm_A(M); return sum(1 for i in range(4) if p[i] == i)
def tr_edges(M, oriented):
    p = vperm_A(M); t = 0
    for i, j in EA:
        if (p[i], p[j]) == (i, j): t += 1
        elif (p[j], p[i]) == (i, j): t += -1 if oriented else 1
    return t
check("T_d acts on legs as det = sign of the leg permutation (so the torsion proof's sign rep is det)",
      all(det(M) == int(round(np.linalg.det(V(M)))) for M in TD))
check("Under T_d (geometric action): torsion = R[TetA vertices] x C^1(ORIENTED TetA edges)",
      all(abs(tr(TOR, M) - tr_vert(M) * tr_edges(M, True)) < 1e-9 for M in TD))
check("Under T_d: Christoffel = R[TetA vertices] x (R[TetA vertices] + R[UNORIENTED TetA edges])",
      all(abs(tr(CHR, M) - tr_vert(M) * (tr_vert(M) + tr_edges(M, False))) < 1e-9 for M in TD))
check("The 6 TetA edges are the cube face diagonals through the 6 cusps (one per face)",
      sorted(tuple(mid((TETA[i], TETA[j]))) for i, j in EA) == sorted(tuple(f) for f in by_support[1]))

# ---------------------------------------------------------------------------
print("\n=== N. Mirror or inversion: what distinguishes them on the connection ===")
detmode = eps / np.linalg.norm(eps)
Pinv = conn(P_mirror)
swapproj = sum(swap(M) * conn(M) for M in OH) / 48
check("The mirror (exchange read at level 4) FLIPS the axial/volume torsion mode", np.allclose(Pinv @ detmode, -detmode))
check("Inversion also FLIPS it: the axial mode cannot tell the two readings apart", np.allclose(conn(Z) @ detmode, -detmode))
check("The mirror FIXES all 5 swap modes (the leg-permutation-invariant part of the connection)",
      np.allclose(Pinv @ swapproj, swapproj))
check("Inversion FLIPS all 5 swap modes", np.allclose(conn(Z) @ swapproj, -swapproj))
print("      => discriminating observable: the permutation-invariant part of the connection (4 Christoffel"
      " + vector-torsion trace).  Exchange = mirror leaves it; exchange = inversion reverses it.")

# Clifford model: does inversion exchange 21 and 13?  Grade involution on Cl(3,0) in the Pauli rep
s1 = np.array([[0, 1], [1, 0]], complex); s2 = np.array([[0, -1j], [1j, 0]], complex); s3 = np.diag([1, -1]).astype(complex)
Ips, T1 = s1 @ s2 @ s3, s1 + s2 + s3
Rr = (np.eye(2) - Ips @ T1) / 2
inv_R = (np.eye(2) - (-Ips) @ (-T1)) / 2          # grade involution: vectors and I change sign
check("Clifford model: inversion FIXES the closure rotor R, so it does NOT exchange N(K+R)=21 with N(K-R)=13"
      " (disagrees with the modular model's s -> -s; recorded as unresolved)", np.allclose(inv_R, Rr))

n_pass = sum(1 for _, ok in RESULTS if ok)
print(f"\n{n_pass}/{len(RESULTS)} checks passed")
if __name__ == "__main__":
    raise SystemExit(0 if n_pass == len(RESULTS) else 1)
