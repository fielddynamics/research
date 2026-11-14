"""S4. The Lambda mechanism on the lattice, with mu computed, not inserted.
As T03 (diamond net n = 32, Picard, Dirichlet box, Q = pi so g_N = 1/r^2), but each bond's
conductance is the TetA share of the lowest eigenvector of its own 3x3 Lambda Hamiltonian
[[0, 0, -tA], [0, 0, -tB], [-tA, -tB, Delta]], tA^2 = g_b (the bond's local field), tB^2 = a0,
found numerically (numpy eigh), not from a formula.
Pass (fixed in PLAN.md): every run within 0.5% of the analytic g(r) for r >= 8d, and the field the
same for every Delta to within 1e-6."""
import sys
sys.path.insert(0, "../tests")
import numpy as np
import pyamg
import scipy.sparse as sps
from lattice import diamond_grid, BOND

n = 32; L = 4 * n
pts, lab, I, J, deg = diamond_grid(n); N = len(pts)
src = np.argmin(np.where(lab == 1, np.sum((pts - 2.0 * n) ** 2, 1), np.inf))
r = np.linalg.norm(pts - pts[src], axis=1)
missing = 4 - deg; dv = pts[J] - pts[I]; Q = np.pi


def lambda_share(gb, a0, Delta):
    """TetA share of the lowest eigenvector of the 3x3 Lambda Hamiltonian, per entry of gb."""
    gb = np.minimum(gb, 1e8 * a0)
    m = len(gb)
    H = np.zeros((m, 3, 3))
    tA, tB = np.sqrt(gb), np.sqrt(a0)
    H[:, 0, 2] = H[:, 2, 0] = -tA
    H[:, 1, 2] = H[:, 2, 1] = -tB
    H[:, 2, 2] = Delta
    w, U = np.linalg.eigh(H)
    v = U[:, :, 0]
    return v[:, 0] ** 2 / (v[:, 0] ** 2 + v[:, 1] ** 2)


def grad_mag(phi):
    g = np.zeros((N, 3)); d = (phi[J] - phi[I])[:, None] * dv
    np.add.at(g, I, d); np.add.at(g, J, d)
    return np.linalg.norm(g / 4, axis=1)


def solve(wb, ws, x0=None):
    Adj = sps.coo_matrix((np.r_[wb, wb], (np.r_[I, J], np.r_[J, I])), shape=(N, N)).tocsr()
    Lap = (sps.diags(np.asarray(Adj.sum(1)).ravel() + missing * ws) - Adj).tocsr()
    rhs = np.zeros(N); rhs[src] = Q
    return pyamg.smoothed_aggregation_solver(Lap, symmetry="symmetric").solve(rhs, x0=x0, tol=1e-11, accel="cg")


def run(a0, Delta):
    phi = solve(np.ones(len(I)), 1.0); wb = np.ones(len(I)); ws = np.ones(N)
    for it in range(300):
        gm = grad_mag(phi); gm[src] = 1e8 * a0
        wb = 0.5 * wb + 0.5 * lambda_share(0.5 * (gm[I] + gm[J]), a0, Delta)
        ws = 0.5 * ws + 0.5 * lambda_share(gm, a0, Delta)
        new = solve(wb, ws, phi)
        ch = np.max(np.abs(new - phi)) / np.max(np.abs(new)); phi = new
        if ch < 1e-9:
            break
    return grad_mag(phi), it + 1


lo, hi = 8 * BOND, 0.3 * L
win = (r >= lo) & (r <= hi)
edges = np.geomspace(lo, hi, 13)
def compare(gm, a0):
    gN = 1 / np.maximum(r, 1e-9) ** 2; ga = (gN + np.sqrt(gN ** 2 + 4 * gN * a0)) / 2
    errs = []
    for a, b in zip(edges[:-1], edges[1:]):
        m = (r >= a) & (r < b) & win
        errs.append((ga[m].mean() / a0, gm[m].mean() / ga[m].mean() - 1))
    return errs

def main():
  global worst
  worst = 0.0; fields = {}
  print(" a0      Delta/a0   iters   x range         worst shell |rel err| (r >= 8d)")
  for a0, dr in [(1e-2, 0.01), (1e-2, 1.0), (1e-2, 100.0), (1e-4, 1.0), (1.0, 1.0)]:
      gm, its = run(a0, dr * a0)
      e = compare(gm, a0)
      w = max(abs(v) for _, v in e); worst = max(worst, w)
      fields[(a0, dr)] = gm[win]
      print(f" {a0:6.0e}  {dr:7.2f}   {its:4d}   {min(x for x, _ in e):.3g}-{max(x for x, _ in e):<8.3g}   {w:.4f}")
      sys.stdout.flush()
  base = fields[(1e-2, 1.0)]
  dmax = max(np.max(np.abs(fields[(1e-2, d)] / base - 1)) for d in (0.01, 100.0))
  print(f"\nlargest relative difference between Delta runs (a0 = 1e-2): {dmax:.1e}")
  ok = worst < 0.005 and dmax < 1e-6
  print("S4", "PASS" if ok else "FAIL", f"- mu computed from each bond's Lambda spectrum reproduces the field law within "
        f"{100*worst:.2f}% beyond 8 bond lengths; independent of Delta to {dmax:.0e}")


if __name__ == "__main__":
  main()
