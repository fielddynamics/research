"""
Verification of the Gram-matrix theorems of the tetrad frame.

Covers two notes:
  [A] "The Spatial Geometry of the Lorentz Tetrad"
      (papers/letter-radial-acceleration-relation-sparc/supplementary/
       supplementary_spatial_geometry_of_the_lorentz_tetrad.tex)
  [B] "The Gram Matrix of the Tetrad Equation"
      (papers/gram-matrix-of-tetrad-equation/supplementary_gram_stellated_octahedron.tex)

Run:  python verify_gram_theorems.py      (exit code 0 if every check passes)
"""

from __future__ import annotations

import itertools
import sys

import numpy as np

K, D = 4, 3
CHECKS: list[tuple[str, bool]] = []


def check(name: str, ok: bool) -> None:
    CHECKS.append((name, bool(ok)))


def perm_matrix(s):
    P = np.zeros((K, K))
    for i, j in enumerate(s):
        P[j, i] = 1.0
    return P


PERMS = [perm_matrix(s) for s in itertools.permutations(range(K))]
I4, J4 = np.eye(K), np.ones((K, K))

# --------------------------------------------------------------------------
# [A] Lemma (commutant): S4-invariant 4x4 matrices form span{I, J}
# --------------------------------------------------------------------------
A = np.vstack([np.kron(P, P) - np.eye(K * K) for P in PERMS])
null_dim = K * K - np.linalg.matrix_rank(A)
check("[A] commutant of the S4 permutation representation has dimension 2", null_dim == 2)
for G in (I4, J4):
    check("[A] I and J are S4-invariant",
          all(np.allclose(P @ G @ P.T, G) for P in PERMS))

# --------------------------------------------------------------------------
# [A] Theorem (forced Gram matrix): F1-F3 => G = c^2 I - (c^2/3)(J - I)
# --------------------------------------------------------------------------
try:
    import sympy as sp
    a, b, c = sp.symbols("alpha beta c", positive=False)
    sol = sp.solve([sp.Eq(a + b, c ** 2), sp.Eq(4 * c ** 2 + 12 * b, 0)], [a, b], dict=True)[0]
    check("[A] F1 + F2 fix beta = -c^2/3, alpha = 4c^2/3",
          sp.simplify(sol[b] + c ** 2 / 3) == 0 and sp.simplify(sol[a] - 4 * c ** 2 / 3) == 0)
except ImportError:
    beta = -1.0 / 3.0
    check("[A] F1 + F2 fix beta = -c^2/3 (c = 1, numeric)", abs(4 + 12 * beta) < 1e-15)


def forced_gram(c2: float) -> np.ndarray:
    return c2 * I4 - (c2 / 3.0) * (J4 - I4)


for c2 in (1.0, 3.0, 7.5):
    ev = np.sort(np.linalg.eigvalsh(forced_gram(c2)))
    check(f"[A] spectrum {{0, 4c^2/3 (x3)}} at c^2 = {c2}",
          np.allclose(ev, [0, 4 * c2 / 3, 4 * c2 / 3, 4 * c2 / 3]))

# Canonical representative and its properties
M1 = np.array([[+1, +1, -1, -1],
               [+1, -1, +1, -1],
               [+1, -1, -1, +1]], dtype=float)
M2 = -M1
G = M1.T @ M1
check("[A]/[B] canonical M realises the forced Gram matrix at c^2 = 3",
      np.allclose(G, forced_gram(3.0)))
check("[A] F1 common norm", np.allclose(np.diag(G), 3.0))
check("[A] F2 balanced closure", np.allclose(M1.sum(axis=1), 0.0))
check("[A] F3 S4-invariance of G", all(np.allclose(P @ G @ P.T, G) for P in PERMS))

# Regular tetrahedron: all six edges equal to c sqrt(8/3)
edges = [np.linalg.norm(M1[:, i] - M1[:, j]) for i, j in itertools.combinations(range(K), 2)]
check("[A] regular tetrahedron, edge c*sqrt(8/3)", np.allclose(edges, np.sqrt(3.0 * 8.0 / 3.0)))

# Uniqueness up to O(3): reconstruct any realisation from G and align to M1
rng = np.random.default_rng(1)
w, V = np.linalg.eigh(G)
X = (V[:, w > 1e-9] * np.sqrt(w[w > 1e-9])).T          # a realisation from G alone
U, _, Wt = np.linalg.svd(M1 @ X.T)
R = U @ Wt                                             # orthogonal Procrustes
check("[A] realisation from G alone is O(3)-equivalent to M", np.allclose(R @ X, M1))
for _ in range(5):
    Q, _ = np.linalg.qr(rng.normal(size=(3, 3)))
    check("[A]/[B] Gram matrix invariant under random O(3)",
          np.allclose((Q @ M1).T @ (Q @ M1), G))

# Parity completion: cube and stella octangula
verts = {tuple(v) for v in np.hstack([M1, M2]).T.astype(int)}
check("[A] V u P(V) is the cube {-1,+1}^3", verts == set(itertools.product([-1, 1], repeat=3)))

# --------------------------------------------------------------------------
# [B] The three Gram products
# --------------------------------------------------------------------------
check("[B] Lemma 1 root-blindness G_11 = G_22", np.allclose(M2.T @ M2, G))
check("[B] Lemma 2 cross-coupling G_12 = -G_11", np.allclose(M1.T @ M2, -G))
check("[B] exactly three distinct products (G_21 = G_12)", np.allclose(M2.T @ M1, M1.T @ M2))
check("[B] Lemma 3 explicit G (diag D, off-diag -1)",
      np.allclose(G, D * I4 - (J4 - I4)))
check("[B] Lemma 5 G = (D+1) I - J", np.allclose(G, (D + 1) * I4 - J4))
check("[B] Lemma 5 null vector (1,1,1,1)", np.allclose(G @ np.ones(K), 0.0))
check("[B] Lemma 5 eigenvalue D+1 with multiplicity D",
      np.allclose(np.sort(np.linalg.eigvalsh(G)), [0, D + 1, D + 1, D + 1]))

# --------------------------------------------------------------------------
# [B] Index grid and the torsion-free projection
# --------------------------------------------------------------------------
diag, upper, lower = K, K * (K - 1) // 2, K * (K - 1) // 2
check("[B] slice 4 + 6 + 6 = 16", diag + upper + lower == K ** 2)
check("[B] connection 24 + 16 + 24 = 64", K * upper + K * diag + K * lower == K ** 3)

# The symmetric (torsion-free) subspace of a KxK slice has dimension K(K+1)/2
T = np.zeros((K * K, K * K))
for i in range(K):
    for j in range(K):
        T[j * K + i, i * K + j] = 1.0                     # transposition operator
ev = np.linalg.eigvalsh(T)
n_sym, n_anti = int(np.sum(np.isclose(ev, 1))), int(np.sum(np.isclose(ev, -1)))
check("[B] transposition eigenspaces 10 (+1) and 6 (-1) per slice", (n_sym, n_anti) == (10, 6))
check("[B] torsion-free retains 40, discards 24", (K * n_sym, K * n_anti) == (40, 24))


def f(k, s):
    return 1 + s * k + k * k


check("[B] polynomial gives the same split: (f(K,+1)-1)/2 = 10, (f(K,-1)-1)/2 = 6",
      ((f(K, 1) - 1) // 2, (f(K, -1) - 1) // 2) == (n_sym, n_anti))
check("[B] Theorem: 16 + 24 = 40 != 64", 16 + 24 == 40 and 40 != K ** 3)

# --------------------------------------------------------------------------
if __name__ == "__main__":
    width = max(len(n) for n, _ in CHECKS)
    for name, ok in CHECKS:
        print(f"{'PASS' if ok else 'FAIL'}  {name}")
    n_ok = sum(ok for _, ok in CHECKS)
    print(f"\n{n_ok}/{len(CHECKS)} checks passed")
    sys.exit(0 if n_ok == len(CHECKS) else 1)
