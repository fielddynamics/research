"""T02. Newtonian limit of the lattice Green's function.

Discrete Poisson equation sum_j (phi_i - phi_j) = delta_{i,0} on a diamond net of
40^3 conventional cells (512,000 sites), Dirichlet zero outside, unit source at the
central TetA site. Fit phi = A/r + B over 5d <= r <= 0.3 L.
Pass: deviation from A/r + B below 1% of A/r over that range, and no direction
dependence above 1% on any shell. Continuum expectation: A = V_site / (2 * 4 pi) = 1/pi
(site volume 8, lattice Laplacian -> -2 nabla^2 by the tight frame).
"""
import numpy as np
import pyamg
import scipy.sparse as sps

from lattice import diamond_grid, BOND

n = 40
pts, lab, I, J, deg = diamond_grid(n)
N = len(pts)
Adj = sps.coo_matrix((np.ones(2 * len(I)), (np.r_[I, J], np.r_[J, I])), shape=(N, N)).tocsr()
Lap = (4.0 * sps.identity(N) - Adj).tocsr()           # missing neighbours are at phi = 0

c = np.full(3, 2.0 * n)
src = np.argmin(np.where(lab == 1, np.sum((pts - c) ** 2, 1), np.inf))
rhs = np.zeros(N); rhs[src] = 1.0
ml = pyamg.smoothed_aggregation_solver(Lap, symmetry="symmetric")
res = []
phi = ml.solve(rhs, tol=1e-12, accel="cg", residuals=res)
print(f"sites {N}, solve residual {res[-1]/res[0]:.1e} in {len(res)} iterations")

d = pts - pts[src]
r = np.linalg.norm(d, axis=1)
L = 4 * n
win = (r >= 5 * BOND) & (r <= 0.3 * L)
X = np.vstack([1 / r[win], np.ones(win.sum())]).T
Afit, Bfit = np.linalg.lstsq(X, phi[win], rcond=None)[0]
print(f"fit: A = {Afit:.6f} (continuum 1/pi = {1/np.pi:.6f}, ratio {Afit*np.pi:.5f}), B = {Bfit:.6f}")

dev = (phi[win] - (Afit / r[win] + Bfit)) / (Afit / r[win])
print(f"max |deviation| / (A/r) over the window: {np.abs(dev).max():.4f}")

# direction dependence on shells
edges = np.linspace(5 * BOND, 0.3 * L, 13)
worst = 0.0
print("shell r     n_sites  mean dev   spread (max-min)/(A/r)")
for lo, hi in zip(edges[:-1], edges[1:]):
    m = (r[win] >= lo) & (r[win] < hi)
    if m.sum() < 10:
        continue
    sp_ = dev[m].max() - dev[m].min()
    worst = max(worst, sp_)
    print(f"{lo:5.1f}-{hi:5.1f}  {m.sum():7d}  {dev[m].mean():+.4f}   {sp_:.4f}")

ok = np.abs(dev).max() < 0.01 and worst < 0.01
print("\nT02", "PASS" if ok else "FAIL",
      f"- max deviation {np.abs(dev).max():.4f}, worst shell spread {worst:.4f} (criterion 0.01); A*pi = {Afit*np.pi:.4f}")
