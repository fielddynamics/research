"""Validation of gfd_field_solver.py against two exact results.
Run: python validate_solver.py      (about 1 minute)"""
import numpy as np
from gfd_field_solver import Solver, g_isolated, mu

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

# 1. Isolated mass: exact spherical solution of mu(g) g = g_N.
S = Solver(g_e=0.0, NR=160, NZ=321); S.iterate()
err = {r: S.internal_radial(r)[0] / g_isolated(r) - 1 for r in (0.1, 0.3, 1, 3, 10, 30)}
for r, e in err.items():
    print(f"     r = {r:5.1f} r_M   solver / exact - 1 = {100 * e:+.3f}%")
check("isolated mass: within 0.3% of the exact solution at every radius", max(abs(e) for e in err.values()) < 3e-3)
check("isolated mass: within 0.05% at r >= 3 r_M (the wide-binary regime)", max(abs(err[r]) for r in (3, 10, 30)) < 5e-4)

# 2. Mass in an external field: analytic far field where g_N << g_e (linearised field equation).
ge = 1.744
me, Le = mu(ge), 1 / (1 + ge)
def far_field_gamma(s, n=200):
    c, w = np.polynomial.legendre.leggauss(n); th = np.arccos(c)
    R, z = s * np.sin(th), s * np.cos(th)
    q = np.sqrt(R ** 2 + z ** 2 / (1 + Le)); k = 1 / (me * np.sqrt(1 + Le))
    gr = np.sin(th) * k * R / q ** 3 + np.cos(th) * k * z / (1 + Le) / q ** 3
    return 0.5 * np.sum(w * gr) * s * s
coarse, fine = Solver(g_e=ge, NR=160, NZ=321), Solver(g_e=ge, NR=240, NZ=481)
coarse.iterate(); fine.iterate()
for s in (5, 10, 20):
    gc, gf = coarse.internal_radial(s)[0] * s * s, fine.internal_radial(s)[0] * s * s
    print(f"     s = {s:2d} r_M   gamma coarse {gc:.4f}  fine {gf:.4f}  analytic far field {far_field_gamma(s):.4f}")
check("external field: within 0.3% of the analytic far field at s = 10 and 20 r_M",
      all(abs(fine.internal_radial(s)[0] * s * s / far_field_gamma(s) - 1) < 3e-3 for s in (10, 20)))
check("grid convergence: coarse and fine grids agree within 0.3% for s >= 0.2 r_M",
      all(abs(coarse.internal_radial(s)[0] / fine.internal_radial(s)[0] - 1) < 3e-3 for s in (0.2, 0.5, 1, 2, 5, 10, 20)))
check("Newtonian close in: gamma within 5% of 1 at s = 0.2 r_M", abs(fine.internal_radial(0.2)[0] * 0.04 - 1) < 0.05)

print(f"\n{sum(ok)}/{len(ok)} checks passed")
