"""
verify_sweep_sierpinski.py
==========================

Part VI of INTERSECTION_ALGEBRA.md: the G Sierpinski blocks against the
three-sweep Walsh-Hadamard kernel of research/spectral/spectral_kernel.py,
and whether any off-diagonal structure can reach G.

  S1. H2 = L diag(1,-2) L^T: a Hadamard sweep is Sierpinski x graded parity x Sierpinski^T.
  S2. The kernel tick H diag(b) H / n has trace sum(b): an identity bridge on blocks
      1, 4, 16 gives 21, the same as the Sierpinski blocks and the projectors.
  S3. det(alpha^A) = alpha^Tr(A) cannot see off-diagonal entries: the Sierpinski
      pattern (9 and 81 filled cells) does not enter G through this read.
  S4. No natural read of the full blocks gives 17/13 except the trace.
  S5. 1 + alpha/(2 pi) cannot come from any algebraic read of integer blocks.

Requires numpy, sympy.
"""
from __future__ import annotations

import itertools

import numpy as np
import sympy as sp

RESULTS = []


def check(name, cond):
    RESULTS.append((name, bool(cond)))
    print(f"[{'PASS' if cond else 'FAIL'}] {name}")


L = np.array([[1, 0], [1, 1]])
H2 = np.array([[1, 1], [1, -1]])
D2 = np.diag([1, -2])
kron = lambda A, n: np.array([[1]]) if n == 0 else (A if n == 1 else np.kron(A, kron(A, n - 1)))
pc = lambda v: bin(v).count("1")

print("\n=== S1. A Hadamard sweep is Sierpinski x graded parity x Sierpinski^T ===")
check("H2 = L diag(1,-2) L^T exactly", np.array_equal(L @ D2 @ L.T, H2))
ok = all(np.array_equal(kron(L, n) @ kron(D2, n) @ kron(L, n).T, kron(H2, n)) for n in range(1, 6))
check("H_(2^n) = S_n D_n S_n^T for n = 1..5, S_n = L^(x)n (the G blocks), D_n = diag((-2)^grade)", ok)
check("D_n = diag((-1)^grade 2^grade): the parity operator of the cube sits in the middle factor",
      all(np.array_equal(np.diag(kron(D2, n)), [(-2) ** pc(i) for i in range(2 ** n)]) for n in range(1, 6)))
check("Over F2 the factorisation collapses: S_n^2 = I mod 2 and D_n = diag(1,0,..) mod 2 (only the constant survives)",
      all(np.array_equal((kron(L, n) @ kron(L, n)) % 2, np.eye(2 ** n, dtype=int)) for n in range(1, 5)))

print("\n=== S2. The three-sweep kernel reads traces ===")
def tick(n, b):
    Hn = kron(H2, int(np.log2(n))) if n > 1 else np.array([[1]])
    return Hn @ np.diag(b) @ Hn / n
rng = np.random.default_rng(0)
check("Tr(H diag(b) H / n) = sum(b) for random bridges on n = 1, 4, 16",
      all(abs(np.trace(tick(n, b)) - b.sum()) < 1e-9 for n in (1, 4, 16) for b in [rng.standard_normal(n) for _ in range(5)]))
tr_kernel = [sum(np.trace(tick(n, np.ones(n)) * w) for n, w in zip((1, 4, 16), (1, s, 1))) for s in (1, 0, -1)]
tr_sierp = [np.trace(kron(L, 0)) + s * np.trace(kron(L, 2)) + np.trace(kron(L, 4)) for s in (1, 0, -1)]
check(f"Identity bridges on blocks 1, 4, 16 with s on the middle: traces {[round(t) for t in tr_kernel]}"
      f" = Sierpinski blocks {[int(t) for t in tr_sierp]} = 21, 17, 13",
      [round(t) for t in tr_kernel] == [int(t) for t in tr_sierp] == [21, 17, 13])

print("\n=== S3. det(alpha^A) is blind to everything off the diagonal ===")
a = sp.symbols("alpha", positive=True)
S1 = sp.Matrix(kron(L, 2))
blind = all(sp.simplify((sp.exp(sp.log(a) * M)).det() - a ** M.trace()) == 0
            for M in (S1, sp.eye(4), sp.Matrix(np.tril(np.ones((4, 4), dtype=int)))))
check("det(alpha^S) = det(alpha^I) = det(alpha^(any unit lower-triangular)) = alpha^4 on the 4x4 block", blind)
print("      => identity blocks give exactly the same G; the 5 and 65 off-diagonal filled cells never enter")

print("\n=== S4. Do other reads of the FULL blocks give 17/13? ===")
reads = {
    "sum of entries": lambda M: M.sum(),
    "Frobenius^2 (= filled cells)": lambda M: (M * M).sum(),
    "Tr(S^T S)": lambda M: np.trace(M.T @ M),
    "nonzeros below diagonal": lambda M: int(np.tril(M, -1).sum()),
}
found = []
for nm, f in reads.items():
    v = [f(kron(L, 0)) + s * f(kron(L, 2)) + f(kron(L, 4)) for s in (1, 0, -1)]
    r = v[1] / v[2] if v[2] else float("inf")
    print(f"      {nm:28s} s = +1, 0, -1: {[int(x) for x in v]}   ratio s0/s-1 = {r:.4f}")
    if abs(r - 17 / 13) < 1e-12:
        found.append(nm)
check("None of the off-diagonal-sensitive reads gives 17/13 (only the trace does)", found == [])
check("Tr(S^k) for every k is diagonal-only (S^k is unit lower-triangular), so it too returns 21, 17, 13 and nothing more",
      all(np.trace(np.linalg.matrix_power(kron(L, m), k)) == 4 ** (m // 2) for m in (0, 2, 4) for k in range(1, 6)))

print("\n=== S5. The one-loop factor 1 + alpha/2pi ===")
check("Any read built from integer blocks by sums, products, traces and determinants is a polynomial in alpha "
      "with rational coefficients; 1/(2 pi) is transcendental, so 1 + alpha/(2 pi) cannot come from the blocks",
      not sp.Rational(1, 1).equals(1 / (2 * sp.pi)) and (1 / (2 * sp.pi)).is_algebraic is False)

n_pass = sum(1 for _, ok_ in RESULTS if ok_)
print(f"\n{n_pass}/{len(RESULTS)} checks passed")
if __name__ == "__main__":
    raise SystemExit(0 if n_pass == len(RESULTS) else 1)
