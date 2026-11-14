"""T03. Nonlinear lattice field with the bond share on every bond.

Solve sum_j w_ij (phi_i - phi_j) = Q delta_{i,0} on the diamond net, with each bond's
weight w_ij = mu(x), mu(x) = x/(1+x), x = |grad phi|/a0 at the bond (mean of the two
end-site gradients, each reconstructed from its 4 bonds by the tight frame).
Picard iteration with damping. Dirichlet zero outside the box.

Continuum target (T02's normalisation, site volume 8): mu(g/a0) g = g_N = Q/(pi r^2),
so g = (g_N + sqrt(g_N^2 + 4 g_N a0))/2. Windows of a0 cover g/a0 from 1e-2 to 1e2.

Pass (fixed in TEST_PLAN.md): the radial profile g(r) (shell means) within 1% of the
analytic g for r > 5d, over g/a0 from 1e-2 to 1e2; and in the deep field v^4/(G M a0)
equal to the law's 1 + x within 1% (the exact deep limit is 1 as x -> 0).
"""
import numpy as np
import pyamg
import scipy.sparse as sps

from lattice import diamond_grid, BOND

import sys
n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 32
L = 4 * n
pts, lab, I, J, deg = diamond_grid(n)
N = len(pts)
c = np.full(3, 2.0 * n)
src = np.argmin(np.where(lab == 1, np.sum((pts - c) ** 2, 1), np.inf))
r = np.linalg.norm(pts - pts[src], axis=1)
missing = 4 - deg                                   # bonds to the Dirichlet boundary
Q = np.pi                                           # so g_N = 1 / r^2
dv = pts[J] - pts[I]
mu = lambda x: x / (1 + x)


def grad_mag(phi):
    g = np.zeros((N, 3))
    dphi = (phi[J] - phi[I])[:, None] * dv
    np.add.at(g, I, dphi); np.add.at(g, J, dphi)
    return np.linalg.norm(g / 4.0, axis=1), g / 4.0


def solve(w_b, w_site, phi0=None):
    Adj = sps.coo_matrix((np.r_[w_b, w_b], (np.r_[I, J], np.r_[J, I])), shape=(N, N)).tocsr()
    diag = np.asarray(Adj.sum(1)).ravel() + missing * w_site
    Lap = (sps.diags(diag) - Adj).tocsr()
    rhs = np.zeros(N); rhs[src] = Q
    ml = pyamg.smoothed_aggregation_solver(Lap, symmetry="symmetric")
    return ml.solve(rhs, x0=phi0, tol=1e-11, accel="cg")


def analytic(rr, a0):
    gN = 1 / np.maximum(rr, 1e-9) ** 2
    return (gN + np.sqrt(gN ** 2 + 4 * gN * a0)) / 2


rmin = next((float(v.split("=")[1]) for v in sys.argv if v.startswith("--rmin=")), 5.0)
lo, hi = rmin * BOND, 0.3 * L
win = (r >= lo) & (r <= hi)
edges = np.geomspace(lo, hi, 15)
worst = 0.0
deep_worst = 0.0
covered = []
import sys
print(f"sites {N}, window {lo:.2f} <= r <= {hi:.1f}")
print(" a0        x range        iters  worst shell |rel err|   deep v^4/(GMa0(1+x)) - 1")
A0S = [float(v) for v in sys.argv[2].split(',')] if len(sys.argv) > 2 and not sys.argv[2].startswith("-") else [1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1.0, 10.0]
for a0 in A0S:
    phi = solve(np.ones(len(I)), 1.0)                # Newtonian start
    wb = np.ones(len(I)); ws = np.ones(N)
    for it in range(200):
        gm, _ = grad_mag(phi)
        gm[src] = 1e300                              # the source site: mu -> 1
        wb_new = mu(0.5 * (gm[I] + gm[J]) / a0)
        ws_new = mu(gm / a0)
        wb = 0.5 * wb + 0.5 * wb_new; ws = 0.5 * ws + 0.5 * ws_new
        phi_new = solve(wb, ws, phi)
        change = np.max(np.abs(phi_new - phi)) / np.max(np.abs(phi_new))
        phi = phi_new
        if change < 1e-8:
            break
    gm, gvec = grad_mag(phi)
    ga = analytic(r, a0)
    x = ga / a0
    errs = []
    for a, b in zip(edges[:-1], edges[1:]):
        m = (r >= a) & (r < b) & win
        if m.sum() < 20:
            continue
        xs = x[m].mean()
        if not (1e-2 <= xs <= 1e2):
            continue
        e = gm[m].mean() / ga[m].mean() - 1
        errs.append((0.5 * (a + b), xs, e))
        covered.append(xs)
    w = max(abs(e) for _, _, e in errs) if errs else np.nan
    worst = max(worst, w) if errs else worst
    deep = []
    for rc, xs, _ in errs:
        if xs < 0.1:
            k = np.searchsorted(edges, rc) - 1
            m = (r >= edges[k]) & (r < edges[k + 1]) & win
            deep.append(abs(np.mean((gm[m] * r[m]) ** 2 / (a0 * (1 + ga[m] / a0))) - 1))
    dw = max(deep) if deep else np.nan
    if deep:
        deep_worst = max(deep_worst, dw)
    xr = (min(e[1] for e in errs), max(e[1] for e in errs)) if errs else (np.nan, np.nan)
    if "-v" in sys.argv:
        print("    " + "  ".join(f"r={rc:.1f} x={xs:.3g} err={e:+.4f}" for rc, xs, e in errs))
    print(f" {a0:7.0e}  {xr[0]:8.3g}-{xr[1]:<8.3g}  {it+1:4d}   {w:.4f}" + (f"                {dw:.4f}" if deep else ""))

cov = (min(covered), max(covered))
ok = worst < 0.01 and deep_worst < 0.01 and cov[0] <= 0.02 and cov[1] >= 50
print(f"\ncovered x from {cov[0]:.3g} to {cov[1]:.3g}")
print("T03" + ("" if rmin == 5.0 else f" DIAGNOSTIC (r >= {rmin:g} d, not the criterion)"), "PASS" if ok else "FAIL",
      f"- worst shell-mean error {worst:.4f}, worst deep-field error {deep_worst:.4f} (criterion 0.01)")
