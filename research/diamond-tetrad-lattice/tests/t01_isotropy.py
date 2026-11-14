"""T01. Isotropy from the tight frame.

Exact: sum_a v_a v_a^T = 4 I for the TetA legs, so the O(k^2) term of the
diamond graph Laplacian is isotropic. Numerical: the O(k^4) anisotropy of the
acoustic (lowest) Laplacian branch for diamond, simple cubic and lonsdaleite,
all with bond length 1.
Pass: O(k^2) term exactly isotropic; k^4 coefficients reported for all three.
"""
import itertools

import numpy as np
import sympy as sp

from lattice import TETA, lonsdaleite_box, bonds, BOND

ok = True
M = sp.Matrix(TETA.astype(int)).T
frame = M * M.T
print("tight frame  sum v v^T =", frame.tolist())
ok &= frame == 4 * sp.eye(3)

# exact O(k^2) term of the acoustic branch: lambda = 4 - |f|, f = sum exp(i k.v)
kx, ky, kz, e = sp.symbols("kx ky kz e", real=True)
k = sp.Matrix([kx, ky, kz])
f = sum(sp.exp(sp.I * e * (k.T * sp.Matrix(v))[0]) for v in TETA.astype(int))
f2 = sp.expand(sp.series(sp.simplify(f * sp.conjugate(f)), e, 0, 5).removeO())
lam = sp.series(4 - sp.sqrt(f2), e, 0, 5).removeO()
c2 = sp.simplify(lam.coeff(e, 2))
print("diamond acoustic branch, O(k^2):", c2, " (bond^2 = 3, so per bond length:", sp.simplify(c2 / 3), ")")
ok &= sp.simplify(c2 - sp.Rational(2) * (kx**2 + ky**2 + kz**2) / 1) == 0 or sp.simplify(c2 - 2 * (kx**2 + ky**2 + kz**2)) == 0
c4 = sp.factor(sp.simplify(lam.coeff(e, 4)))
print("diamond acoustic branch, O(k^4):", c4)


def bloch_lowest(cell_pos, disp, kvec):
    """Lowest eigenvalue of the Bloch graph Laplacian; disp = list of (i, j, d_ij)."""
    n = len(cell_pos)
    H = np.zeros((n, n), complex)
    for i, j, d in disp:
        H[i, i] += 1
        H[i, j] -= np.exp(1j * kvec @ d)
    return np.linalg.eigvalsh(H)[0]


# unit cells, bond length 1
s = 1 / BOND
diamond = ([0, 1], [(0, 1, v * s) for v in TETA] + [(1, 0, -v * s) for v in TETA])
sc = ([0], [(0, 0, np.array(e)) for e in itertools.chain(np.eye(3), -np.eye(3))])
# lonsdaleite cell from a periodic patch
pts, lab = lonsdaleite_box(3, 3, 3)
a = BOND * np.sqrt(8 / 3); c = 8 * BOND / 3
a1 = np.array([a, 0, 0]); a2 = np.array([a / 2, a * np.sqrt(3) / 2, 0]); a3 = np.array([0, 0, c])
cell = pts[:4]
disp = []
for i, ri in enumerate(cell):
    for t in itertools.product((-1, 0, 1), repeat=3):
        T = t[0] * a1 + t[1] * a2 + t[2] * a3
        for j, rj in enumerate(cell):
            d = rj + T - ri
            if abs(np.linalg.norm(d) - BOND) < 1e-6:
                disp.append((i, j, d * s))
assert all(sum(1 for q in disp if q[0] == i) == 4 for i in range(4))
lons = (list(range(4)), disp)

rng = np.random.default_rng(1)
dirs = rng.normal(size=(400, 3)); dirs /= np.linalg.norm(dirs, axis=1)[:, None]
dirs = np.vstack([dirs, np.eye(3), np.ones((1, 3)) / np.sqrt(3)])
ks = np.array([0.01, 0.02, 0.03, 0.04])
print("\nper lattice, lambda(k n) = A(n) k^2 + B(n) k^4 fitted at small k (bond length 1)")
report = {}
for name, (cp, dl) in [("diamond", diamond), ("simple cubic", sc), ("lonsdaleite", lons)]:
    A, B = [], []
    for n in dirs:
        y = np.array([bloch_lowest(cp, dl, kk * n) for kk in ks])
        X = np.vstack([ks**2, ks**4]).T
        a_, b_ = np.linalg.lstsq(X, y, rcond=None)[0]
        A.append(a_); B.append(b_)
    A, B = np.array(A), np.array(B)
    report[name] = (A, B)
    print(f"  {name:13s} A mean {A.mean():.6f}, spread {(A.max()-A.min())/A.mean():.1e} | "
          f"B mean {B.mean():.5f}, spread (max-min)/|mean| {(B.max()-B.min())/abs(B.mean()):.3f}")

ok &= all((A.max() - A.min()) / A.mean() < 1e-4 for A, _ in report.values())
print("\nT01", "PASS" if ok else "FAIL", "- O(k^2) isotropic (exact for diamond, numerically for all three); k^4 anisotropy reported")
