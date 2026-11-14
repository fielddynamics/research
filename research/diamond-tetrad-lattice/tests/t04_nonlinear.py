"""T04, nonlinear part: one window at the transition (a0 = 1e-2, Q = pi, as T03), diamond
(n = 32) against lonsdaleite of similar extent. Anisotropy of |g| (axis cone minus plane band,
10d <= r <= 20d, relative to the analytic g). Pass as T04: lonsdaleite > 1%, diamond < 0.1%."""
import numpy as np, pyamg, scipy.sparse as sps
from scipy.spatial import cKDTree
from lattice import diamond_grid, lonsdaleite_box, BOND
mu = lambda x: x / (1 + x)
a0 = 1e-2; Q = np.pi
out = {}
for kind in ("diamond", "lonsdaleite"):
    if kind == "diamond":
        pts, lab, I, J, deg = diamond_grid(32); axis = np.ones(3)/np.sqrt(3)
    else:
        pts, lab = lonsdaleite_box(48, 48, 28)
        pr = cKDTree(pts).query_pairs(BOND*1.01, output_type="ndarray"); I, J = pr[:, 0], pr[:, 1]
        deg = np.bincount(np.r_[I, J], minlength=len(pts)); axis = np.array([0, 0, 1.0])
    N = len(pts); missing = 4 - deg; dv = pts[J] - pts[I]
    src = np.argmin(np.sum((pts - pts.mean(0))**2, 1)); r = np.linalg.norm(pts - pts[src], axis=1)
    def gm(phi):
        g = np.zeros((N, 3)); d = (phi[J]-phi[I])[:, None]*dv
        np.add.at(g, I, d); np.add.at(g, J, d); return np.linalg.norm(g/4, axis=1)
    def solve(wb, ws, x0=None):
        Adj = sps.coo_matrix((np.r_[wb, wb], (np.r_[I, J], np.r_[J, I])), shape=(N, N)).tocsr()
        Lap = (sps.diags(np.asarray(Adj.sum(1)).ravel() + missing*ws) - Adj).tocsr()
        rhs = np.zeros(N); rhs[src] = Q
        return pyamg.smoothed_aggregation_solver(Lap, symmetry="symmetric").solve(rhs, x0=x0, tol=1e-11, accel="cg")
    phi = solve(np.ones(len(I)), 1.0); wb = np.ones(len(I)); ws = np.ones(N)
    for it in range(200):
        g = gm(phi); g[src] = 1e300
        wb = 0.5*wb + 0.5*mu(0.5*(g[I]+g[J])/a0); ws = 0.5*ws + 0.5*mu(g/a0)
        new = solve(wb, ws, phi); ch = np.max(np.abs(new-phi))/np.max(np.abs(new)); phi = new
        if ch < 1e-8: break
    g = gm(phi); gN = 1/np.maximum(r, 1e-9)**2; ga = (gN + np.sqrt(gN**2 + 4*gN*a0))/2
    d = pts - pts[src]; win = (r >= 10*BOND) & (r <= 20*BOND)
    cosang = np.abs(d[win] @ axis)/r[win]; dev = g[win]/ga[win] - 1
    a = dev[cosang > np.cos(np.radians(20))].mean() - dev[cosang < np.sin(np.radians(20))].mean()
    out[kind] = a
    print(f"{kind:12s} sites {N:7d} iters {it+1:3d}  mean |g| error {dev.mean():+.4f}  anisotropy (axis - plane) {a:+.5f}")
ok = abs(out["lonsdaleite"]) > 0.01 and abs(out["diamond"]) < 0.001
print("\nT04 (nonlinear part)", "PASS" if ok else "FAIL",
      f"- lonsdaleite {out['lonsdaleite']:+.5f}, diamond {out['diamond']:+.5f}")
