"""T02 diagnostic (not a re-run of the criterion): where does the shell spread come from?
Same solve at n = 80 (box twice as large). If the inner spread is lattice discreteness it
should be unchanged at fixed r; if the outer spread is the box it should fall at fixed r."""
import numpy as np, pyamg, scipy.sparse as sps
from lattice import diamond_grid, BOND
out = {}
for n in (40, 80):
    pts, lab, I, J, deg = diamond_grid(n); N = len(pts)
    Adj = sps.coo_matrix((np.ones(2*len(I)), (np.r_[I, J], np.r_[J, I])), shape=(N, N)).tocsr()
    Lap = (4.0*sps.identity(N) - Adj).tocsr()
    c = np.full(3, 2.0*n); src = np.argmin(np.where(lab == 1, np.sum((pts-c)**2, 1), np.inf))
    rhs = np.zeros(N); rhs[src] = 1
    phi = pyamg.smoothed_aggregation_solver(Lap, symmetry="symmetric").solve(rhs, tol=1e-12, accel="cg")
    r = np.linalg.norm(pts-pts[src], axis=1)
    win = (r >= 5*BOND) & (r <= 48)
    A, B = np.linalg.lstsq(np.vstack([1/r[win], np.ones(win.sum())]).T, phi[win], rcond=None)[0]
    dev = (phi - (A/r + B))/(A/r)
    rows = []
    for lo in (5, 10, 15, 20, 25):
        m = (r >= lo*BOND) & (r < (lo+2)*BOND)
        rows.append((lo, dev[m].max()-dev[m].min()))
    m = (r >= 44.7) & (r < 48); rows.append(("44.7-48", dev[m].max()-dev[m].min()))
    out[n] = rows
    print(f"n={n}: A*pi={A*np.pi:.5f}; shell spread at r/d = " + ", ".join(f"{a}:{b:.4f}" for a, b in rows))
