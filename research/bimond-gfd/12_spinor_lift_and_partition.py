"""12. Taking the chiral holonomy further: the spinor lift, and the transport weighted by the constitutive law.

S. Spinor (SU(2)) lift of the transport around the cube's Hamiltonian cycles (step: cos(theta/2) - i sin(theta/2) n.sigma,
   cos theta = 1/3):
   - uniform (all-TetA, root-blind) transport: identity in SO(3) but exactly -1 in SU(2) on every cycle.  One circuit is
     a full 2pi turn: vectors come back, spinors come back with a minus sign; two circuits are needed (the 720 deg of
     the double cover, which Paper VII attributes to the two sheets).
   - chiral transport (TetB steps transposed): half-traces exactly 31/81 and -17/81 for the two senses
     (consistent with cos(Theta) = -4639/6561 and -5983/6561 in SO(3)).
M. Steps weighted by the shares, S = mu R + (1 - mu) R^T at a TetA source and mu R^T + (1 - mu) R at a TetB source
   (R^T is the TetB step; script 11):
   - exchange symmetry x -> 1/x (mu -> 1 - mu) maps the TetA step onto the TetB step exactly, so it acts as parity:
     it exchanges the two senses of circulation.
   - at the ring x = 1 (mu = 1/2) every step is symmetric (only the shared diagonal part survives), the two senses
     become equivalent, and the chirality vanishes; it has opposite signs inside and outside the ring.
   - mu = 1 and mu = 0 recover the two chiral classes.
"""
import itertools, numpy as np, sympy as sp
ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)
V = [(np.array([(i >> 2) & 1, (i >> 1) & 1, i & 1]) * 2 - 1) / np.sqrt(3) for i in range(8)]
tetA = lambda i: bin(i).count('1') % 2 == 1
adj = lambda i, j: bin(i ^ j).count('1') == 1
def R(n, a):
    K = np.array([[0, -n[2], n[1]], [n[2], 0, -n[0]], [-n[1], n[0], 0]])
    return np.eye(3) + np.sin(a) * K + (1 - np.cos(a)) * K @ K
cycles = [(0,) + p for p in itertools.permutations(range(1, 8)) if all(adj(((0,) + p)[k], ((0,) + p)[(k + 1) % 8]) for k in range(8))]
rev = lambda c: (c[0],) + tuple(reversed(c[1:]))
ang = lambda H: np.degrees(np.arccos(np.clip((np.trace(H) - 1) / 2, -1, 1)))
def geom(a, b):
    n = np.cross(V[a], V[b]); n /= np.linalg.norm(n); return n, np.arccos(np.clip(V[a] @ V[b], -1, 1))

# ---- S: spinor lift, exact
sx = sp.Matrix([[0, 1], [1, 0]]); sy = sp.Matrix([[0, -sp.I], [sp.I, 0]]); sz = sp.Matrix([[1, 0], [0, -1]])
Vs = [sp.Matrix([(i >> 2) & 1, (i >> 1) & 1, i & 1]) * 2 - sp.Matrix([1, 1, 1]) for i in range(8)]
def Ux(n, sgn):
    return sp.sqrt(sp.Rational(2, 3)) * sp.eye(2) - sp.I * sgn * sp.sqrt(sp.Rational(1, 3)) * (n[0] * sx + n[1] * sy + n[2] * sz)
def spin_hol(c, chiral):
    H = sp.eye(2)
    for k in range(8):
        a, b = c[k], c[(k + 1) % 8]; n = Vs[a].cross(Vs[b]); n = n / sp.sqrt(n.dot(n))
        H = sp.simplify(Ux(n, (1 if tetA(a) else -1) if chiral else 1) * H)
    return sp.simplify(H)
Hu = [spin_hol(c, False) for c in cycles]
check("S: uniform (root-blind) transport lifts to exactly -1 in SU(2) on all 12 cycles (identity in SO(3)): a full 2pi turn",
      all(sp.simplify(H + sp.eye(2)) == sp.zeros(2, 2) for H in Hu))
check("S: two circuits of uniform transport return spinors to +1 (720 deg)", all(sp.simplify(H * H - sp.eye(2)) == sp.zeros(2, 2) for H in Hu))
ht = sorted({sp.nsimplify(sp.simplify(spin_hol(c, True).trace() / 2)) for c in cycles})
check("S: chiral transport half-traces are exactly %s for the two senses" % ht, ht == [sp.Rational(-17, 81), sp.Rational(31, 81)])
check("S: consistent with SO(3): 2 (31/81)^2 - 1 = -4639/6561 and 2 (17/81)^2 - 1 = -5983/6561",
      2 * sp.Rational(31, 81)**2 - 1 == sp.Rational(-4639, 6561) and 2 * sp.Rational(17, 81)**2 - 1 == sp.Rational(-5983, 6561))

# ---- M: share-weighted steps
def step(a, b, mu):
    n, t = geom(a, b); Rm = R(n, t)
    return mu * Rm + (1 - mu) * Rm.T if tetA(a) else mu * Rm.T + (1 - mu) * Rm
def hol_mu(c, mu):
    H = np.eye(3)
    for k in range(8): H = step(c[k], c[(k + 1) % 8], mu) @ H
    return H
def rot_angle(H):
    U, s, Vt = np.linalg.svd(H); return ang(U @ Vt)
mu = lambda x: x / (1 + x)
xs = [100.0, 3.0, 1.5, 1 / 1.5, 1 / 3.0, 0.01]
okx = True
for x in (100.0, 3.0, 1.5):
    for c in cycles:
        okx &= np.isclose(rot_angle(hol_mu(c, mu(x))), rot_angle(hol_mu(rev(c), mu(1 / x))), atol=1e-6)
check("M: exchange x -> 1/x swaps the two senses exactly (it acts as parity), checked at x = 100, 3, 1.5 on all cycles", okx)
def tetA_form(Rm, m): return m * Rm + (1 - m) * Rm.T
def tetB_form(Rm, m): return m * Rm.T + (1 - m) * Rm
check("M: the TetA-source step at mu equals the TetB-source step at 1 - mu on every edge (exchange = relabelling)",
      all(np.allclose(tetA_form(R(*geom(i, j)), m), tetB_form(R(*geom(i, j)), 1 - m)) for i in range(8) for j in range(8) if adj(i, j) for m in (0.1, 0.3, 0.8)))
sym_ok = all(np.allclose(step(i, j, 0.5), step(i, j, 0.5).T) for i in range(8) for j in range(8) if adj(i, j))
eq_ok = all(np.isclose(rot_angle(hol_mu(c, 0.5)), rot_angle(hol_mu(rev(c), 0.5))) for c in cycles)
check("M: at the ring x = 1 every step is symmetric (shared part only) and the two senses are equivalent: chirality vanishes", sym_ok and eq_ok)
diffs = [rot_angle(hol_mu(cycles[0], mu(x))) - rot_angle(hol_mu(rev(cycles[0]), mu(x))) for x in xs]
check("M: the chirality (difference between the senses) is odd under x -> 1/x: %s deg" % np.round(diffs, 2),
      all(np.isclose(diffs[i], -diffs[-1 - i], atol=1e-6) for i in range(3)) and abs(diffs[0]) > 1)
check("M: mu = 1 and mu = 0 recover the two chiral classes (134.996 and 155.770 deg)",
      np.isclose(rot_angle(hol_mu(cycles[0], 1.0)), 134.996, atol=1e-3) and np.isclose(rot_angle(hol_mu(cycles[0], 0.0)), 155.770, atol=1e-3))
print(f"\n{sum(ok)}/{len(ok)} checks passed")
