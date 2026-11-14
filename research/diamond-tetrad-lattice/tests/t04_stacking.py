"""T04. Stacking sensitivity: diamond against lonsdaleite (same Gram matrix, result 6).
Linear part (as T02): unit source, Dirichlet zero, large boxes (diamond n = 80; lonsdaleite of
similar extent). Anisotropy = mean deviation from the fitted A/r + B in a 20-degree cone about
the stacking axis ([111] for diamond, c for lonsdaleite) minus that in a 20-degree band about the
plane normal to it, over 10d <= r <= 20d, relative to A/r.
Nonlinear part (as T03, one window a0 = 1e-2 at the transition): same anisotropy measure on |g|.
Pass (diamond singled out): lonsdaleite anisotropy above 1% where diamond's is below 0.1%."""
import sys
import numpy as np
import pyamg
import scipy.sparse as sps
from scipy.spatial import cKDTree
from lattice import diamond_grid, lonsdaleite_box, BOND


def graph_from_points(pts):
    pairs = cKDTree(pts).query_pairs(BOND * 1.01, output_type="ndarray")
    return pairs[:, 0], pairs[:, 1]


def solve_lin(N, I, J, src):
    Adj = sps.coo_matrix((np.ones(2*len(I)), (np.r_[I, J], np.r_[J, I])), shape=(N, N)).tocsr()
    Lap = (4.0 * sps.identity(N) - Adj).tocsr()
    rhs = np.zeros(N); rhs[src] = 1
    return pyamg.smoothed_aggregation_solver(Lap, symmetry="symmetric").solve(rhs, tol=1e-12, accel="cg")


def anis(pts, src, vals, axis, model):
    d = pts - pts[src]; r = np.linalg.norm(d, axis=1)
    win = (r >= 10*BOND) & (r <= 20*BOND)
    cosang = np.abs(d[win] @ axis) / r[win]
    dev = vals[win] / model(r[win]) - 1
    cone = cosang > np.cos(np.radians(20)); band = cosang < np.sin(np.radians(20))
    return dev[cone].mean() - dev[band].mean(), cone.sum(), band.sum()


def build(kind, size):
    if kind == "diamond":
        pts, lab, I, J, deg = diamond_grid(size)
        axis = np.ones(3) / np.sqrt(3)
    else:
        nx, nz = size
        pts, lab = lonsdaleite_box(nx, nx, nz)
        I, J = graph_from_points(pts)
        axis = np.array([0, 0, 1.0])
    c = pts.mean(0)
    src = np.argmin(np.sum((pts - c)**2, 1))
    return pts, I, J, src, axis


results = {}
for kind, size in [("diamond", 80), ("lonsdaleite", (113, 69))]:
    pts, I, J, src, axis = build(kind, size)
    N = len(pts)
    phi = solve_lin(N, I, J, src)
    r = np.linalg.norm(pts - pts[src], axis=1)
    win = (r >= 10*BOND) & (r <= 20*BOND)
    A, B = np.linalg.lstsq(np.vstack([1/r[win], np.ones(win.sum())]).T, phi[win], rcond=None)[0]
    a, nc, nb = anis(pts, src, phi - B, axis, lambda rr: A/rr)
    results[kind] = a
    print(f"{kind:12s} sites {N:8d}  A*pi = {A*np.pi:.5f}  linear anisotropy (axis - plane) = {a:+.5f}  [{nc} / {nb} sites]")
    sys.stdout.flush()

ok = abs(results["lonsdaleite"]) > 0.01 and abs(results["diamond"]) < 0.001
print("\nT04 (linear part)", "PASS" if ok else "FAIL",
      f"- lonsdaleite {results['lonsdaleite']:+.5f}, diamond {results['diamond']:+.5f} (criterion: lonsdaleite > 1%, diamond < 0.1%)")
