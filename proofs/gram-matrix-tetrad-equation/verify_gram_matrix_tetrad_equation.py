"""
Verification of "The Gram Matrix of the Tetrad Equation" (revised).

Every check is exact (sympy rationals) or exhaustive over a finite set.
Run:  python verify_gram_matrix_tetrad_equation.py   (exit code 0 if all pass)
"""

from __future__ import annotations

import itertools
import random
import sys

import sympy as sp

K, D = 4, 3
CHECKS: list[tuple[str, bool]] = []


def check(name: str, ok) -> None:
    CHECKS.append((name, bool(ok)))


I3, I4 = sp.eye(3), sp.eye(4)
J4 = sp.ones(4, 4)
ONE = sp.ones(4, 1)

M1 = sp.Matrix([[+1, +1, -1, -1],
                [+1, -1, +1, -1],
                [+1, -1, -1, +1]])
M2 = -M1
G = M1.T * M1


def rational_rotation(rng: random.Random, reflect: bool = False) -> sp.Matrix:
    """Exact rational orthogonal matrix by the Cayley transform."""
    a, b, c = (sp.Rational(rng.randint(-9, 9), rng.randint(1, 9)) for _ in range(3))
    A = sp.Matrix([[0, -a, -b], [a, 0, -c], [b, c, 0]])
    Q = (I3 - A) * (I3 + A).inv()
    if reflect:
        Q = Q * sp.diag(1, 1, -1)
    return sp.simplify(Q)


rng = random.Random(2026)

# ---------------------------------------------------------------- Part I
check("L1 root-blindness: M2^T M2 = M1^T M1", M2.T * M2 == G)
check("L2 cross-coupling: M1^T M2 = -G", M1.T * M2 == -G)
check("L2 cross-coupling is unchanged by exchanging the roots: M2^T M1 = M1^T M2",
      M2.T * M1 == M1.T * M2)
check("L2 the Gram products separate same-root from cross-root pairs (G != -G)",
      G != -G)

check("L3 rows of M are orthogonal with norm 4: M M^T = 4 I_3", M1 * M1.T == 4 * I3)
check("L3 closure: M 1 = 0", M1 * ONE == sp.zeros(3, 1))
H = ONE.T.col_join(M1)                       # bordered matrix [1; M]
check("L3 bordered matrix is Hadamard: H H^T = 4 I", H * H.T == 4 * I4)
check("L3 hence H^T H = 4 I", H.T * H == 4 * I4)
check("L3 G = M^T M = 4 I - J", G == 4 * I4 - J4)
check("L3 diagonal D = 3, off-diagonal -1",
      all(G[i, i] == 3 for i in range(4)) and all(G[i, j] == -1 for i in range(4) for j in range(4) if i != j))

P_frame, P_close = G / 4, J4 / 4
check("L5 I = G/4 + J/4", P_frame + P_close == I4)
check("L5 G/4 and J/4 are orthogonal idempotents",
      P_frame ** 2 == P_frame and P_close ** 2 == P_close and P_frame * P_close == sp.zeros(4, 4))
check("L5 G 1 = 0 (closure is the null vector)", G * ONE == sp.zeros(4, 1))
check("L5 the rows of M are eigenvectors: G M^T = 4 M^T", G * M1.T == 4 * M1.T)
check("L5 spectrum {0, 4, 4, 4}, rank 3",
      sorted(G.eigenvals(multiple=True)) == [0, 4, 4, 4] and G.rank() == 3)
check("L5 cross-coupling spectrum {0, -4, -4, -4}",
      sorted((M1.T * M2).eigenvals(multiple=True)) == [-4, -4, -4, 0])

# Lemma 4: invariance and rigidity
for k in range(4):
    Q = rational_rotation(rng, reflect=(k % 2 == 1))
    ok_orth = sp.simplify(Q.T * Q - I3) == sp.zeros(3, 3)
    U1, U2 = Q * M1, Q * M2
    check(f"L4 invariance of all three products under exact O(3) element #{k + 1}",
          ok_orth and sp.simplify(U1.T * U1 - G) == sp.zeros(4, 4)
          and sp.simplify(U2.T * U2 - G) == sp.zeros(4, 4)
          and sp.simplify(U1.T * U2 + G) == sp.zeros(4, 4))
    Qrec = sp.simplify(U1 * M1.T / 4)          # rigidity: Q = W M^T (M M^T)^-1
    check(f"L4 rigidity recovers the unique Q from the Gram data, #{k + 1}",
          sp.simplify(Qrec - Q) == sp.zeros(3, 3))

check("L4 the two roots lie in one O(3) orbit: M2 = (-I) M1", (-I3) * M1 == M2)
R_needed = M2 * M1.T / 4
check("L4 the only Q with Q M1 = M2 is -I, which has det -1 (not in SO(3))",
      R_needed == -I3 and R_needed.det() == -1)

triples = list(itertools.combinations(range(4), 3))
dets1 = [M1[:, list(t)].det() for t in triples]
dets2 = [M2[:, list(t)].det() for t in triples]
check("P1 every triple of legs has nonzero orientation", all(d != 0 for d in dets1))
check("P1 the orientation of every triple flips between the roots (D = 3 odd)",
      all(d2 == -d1 for d1, d2 in zip(dets1, dets2)))
Rp = rational_rotation(rng)
check("P1 orientation is SO(3)-invariant",
      sp.simplify(Rp.det() - 1) == 0 and
      all(sp.simplify((Rp * M1)[:, list(t)].det() - d) == 0 for t, d in zip(triples, dets1)))

# ---------------------------------------------------------------- Part II
cols1 = {tuple(M1[:, j]) for j in range(4)}
cols2 = {tuple(M2[:, j]) for j in range(4)}
cube = set(itertools.product([-1, 1], repeat=3))
check("T2 columns of M1 have xyz = +1, columns of M2 have xyz = -1",
      all(x * y * z == 1 for x, y, z in cols1) and all(x * y * z == -1 for x, y, z in cols2))
check("T2 the two column sets are disjoint", not cols1 & cols2)
check("T2 together they are the eight corners of the cube", cols1 | cols2 == cube)
edges = [((M1[:, i] - M1[:, j]).T * (M1[:, i] - M1[:, j]))[0] for i, j in itertools.combinations(range(4), 2)]
check("T2 all six edges have squared length 2(3+1) = 8 (regular tetrahedron)",
      all(e == 8 for e in edges))
check("T2 centroid at the origin (closure)", sum((M1[:, j] for j in range(4)), sp.zeros(3, 1)) == sp.zeros(3, 1))


def symmetry_group(V: sp.Matrix) -> list[sp.Matrix]:
    """All orthogonal maps of R^3 that permute the columns of V (V spans R^3)."""
    VVt_inv = (V * V.T).inv()
    n, out = V.shape[1], []
    for p in itertools.permutations(range(n)):
        Vp = V[:, list(p)]
        L = Vp * V.T * VVt_inv
        if L * V == Vp and L.T * L == I3:
            out.append(L)
    return out


S = M1.row_join(M2)
symA = symmetry_group(M1)
symS = symmetry_group(S)
keyA = {tuple(L) for L in symA}
keyS = {tuple(L) for L in symS}
check("T3 the tetrahedron has 24 symmetries, acting as all of S4 on the legs",
      len(symA) == 24 and len(keyA) == 24)
check("T3 the stellated octahedron has 48 symmetries (exhaustive over 8! relabellings)",
      len(symS) == 48)
check("T3 Sym(TetA) is a subgroup of Sym(S) of index 2", keyA <= keyS and len(keyS) == 2 * len(keyA))
check("T3 -I is a symmetry of S but not of TetA", tuple(-I3) in keyS and tuple(-I3) not in keyA)
check("T3 Sym(S) = Sym(TetA) x {I, -I}", keyS == keyA | {tuple(-L) for L in symA})
outside = [L for L in symS if tuple(L) not in keyA]
check("T3 every symmetry of S outside Sym(TetA) carries TetA onto TetB",
      all({tuple((L * M1)[:, j]) for j in range(4)} == cols2 for L in outside))
check("T3 TetA is not congruent to S (4 versus 8 points; 24 versus 48 symmetries)",
      len(cols1) != len(cols1 | cols2) and len(symA) != len(symS))

# ---------------------------------------------------------------- Part III


def vec_index(l, m, n):
    return (l * K + m) * K + n


tau = sp.zeros(K ** 3, K ** 3)
for l, m, n in itertools.product(range(K), repeat=3):
    tau[vec_index(l, n, m), vec_index(l, m, n)] = 1
P_sym = (sp.eye(K ** 3) + tau) / 2
check("G1 per slice: 4 diagonal + 6 upper + 6 lower = 16", K + 2 * (K * (K - 1) // 2) == K ** 2)
check("G1 whole connection: 24 + 16 + 24 = 64", K * 6 + K * 4 + K * 6 == K ** 3)
check("G2 tau is an involution", tau * tau == sp.eye(K ** 3))
check("G2 P = (1 + tau)/2 is a projection", P_sym * P_sym == P_sym)
check("G2 rank P = 40, kernel = 24 (antisymmetric = torsion)",
      P_sym.rank() == 40 and K ** 3 - P_sym.rank() == 24)
up = [(m, n) for m in range(K) for n in range(K) if m < n]
swaps_triangles = all(tau[vec_index(l, n, m), vec_index(l, m, n)] == 1 for l in range(K) for m, n in up)
check("G3 tau exchanges the upper and lower triangles and fixes the diagonal",
      swaps_triangles and all(tau[vec_index(l, m, m), vec_index(l, m, m)] == 1 for l in range(K) for m in range(K)))
# In (d, u, l) coordinates the symmetric part is (d, (u + l)/2) and the torsion is u - l
uu, ll = sp.symbols("u l")
check("G3 symmetric part of a mirror pair is (u + l)/2, invariant under u <-> l; torsion u - l changes sign",
      sp.simplify(((uu + ll) / 2).subs({uu: ll, ll: uu}, simultaneous=True) - (uu + ll) / 2) == 0
      and sp.simplify((uu - ll).subs({uu: ll, ll: uu}, simultaneous=True) + (uu - ll)) == 0)

# ---------------------------------------------------------------- Part IV


def metric_compatible_torsion_map(g: sp.Matrix) -> tuple[int, int, int]:
    """Dimension of metric-compatible differences D, of torsions, and rank of D -> T restricted."""
    syms = sp.symbols(f"d0:{K ** 3}")
    Dup = {(l, m, n): syms[vec_index(l, m, n)] for l, m, n in itertools.product(range(K), repeat=3)}
    Dlow = {(l, m, n): sum(g[l, s] * Dup[(s, m, n)] for s in range(K))
            for l, m, n in itertools.product(range(K), repeat=3)}
    eqs = [Dlow[(l, m, n)] + Dlow[(n, m, l)] for l, m, n in itertools.product(range(K), repeat=3)]
    A = sp.Matrix([[sp.diff(e, s) for s in syms] for e in eqs])
    basis = A.nullspace()
    Tmap = sp.Matrix([[sp.diff(Dup[(l, m, n)] - Dup[(l, n, m)], s) for s in syms]
                      for l in range(K) for m in range(K) for n in range(K) if m < n])
    image = Tmap * sp.Matrix.hstack(*basis)
    return len(basis), Tmap.rows, image.rank()


eta = sp.diag(-1, 1, 1, 1)
dimC, dimT, rk = metric_compatible_torsion_map(eta)
check("T4 metric-compatible differences form a 24-dimensional space (eta)", dimC == 24)
check("T4 torsions form a 24-dimensional space", dimT == 24)
check("T4 the map difference -> torsion is bijective (eta): T = 0 forces Gamma = Levi-Civita",
      rk == 24)
E = sp.Matrix(4, 4, lambda i, j: sp.Rational(rng.randint(-5, 5), rng.randint(1, 4)) + (3 if i == j else 0))
g_gen = E.T * eta * E
dimC2, _, rk2 = metric_compatible_torsion_map(g_gen)
check("T4 the same holds for a generic Lorentzian metric g = E^T eta E",
      g_gen.det() != 0 and dimC2 == 24 and rk2 == 24)
Pspace = sp.diag(1, -1, -1, -1)
check("T4 the metric is root-blind: (P e)^T eta (P e) = e^T eta e",
      (Pspace * E).T * eta * (Pspace * E) == g_gen)
check("T4 the roots differ in orientation: det(P e) = -det e", (Pspace * E).det() == -E.det())

# ----------------------------------------------------------------
if __name__ == "__main__":
    for name, ok in CHECKS:
        print(f"{'PASS' if ok else 'FAIL'}  {name}")
    n_ok = sum(ok for _, ok in CHECKS)
    print(f"\n{n_ok}/{len(CHECKS)} checks passed")
    sys.exit(0 if n_ok == len(CHECKS) else 1)
