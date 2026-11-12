"""Machine checks for every step of 'Chiral Holonomy of the Closed Tetrad Frame'.
Exact (sympy) wherever the claim is algebraic; exhaustive over the cube's Hamiltonian cycles.
Run: python verify_chiral_holonomy_closed_frame.py"""
import itertools
import numpy as np
import sympy as sp

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

# ---- Setting: the eight directions, the two classes, the cube graph
W = [sp.Matrix([(i >> 2) & 1, (i >> 1) & 1, i & 1]) * 2 - sp.Matrix([1, 1, 1]) for i in range(8)]   # (+-1,+-1,+-1)
v = [w / sp.sqrt(3) for w in W]
A = [i for i in range(8) if W[i][0] * W[i][1] * W[i][2] > 0]      # TetA: x y z > 0
B = [i for i in range(8) if i not in A]
inA = lambda i: i in A
adj = lambda i, j: bin(i ^ j).count('1') == 1
check("Setting: eight unit vectors, four with xyz > 0 (TetA) and four with xyz < 0 (TetB)",
      all(sp.simplify(u.dot(u)) == 1 for u in v) and len(A) == 4 and len(B) == 4)
check("Setting: parity v -> -v maps TetA onto TetB", sorted(7 - i for i in A) == sorted(B))
check("Setting: every cube edge joins TetA to TetB, with v_i . v_j = 1/3",
      all((inA(i) != inA(j)) and sp.simplify(v[i].dot(v[j])) == sp.Rational(1, 3) for i in range(8) for j in range(8) if adj(i, j)))
cyc = [(0,) + p for p in itertools.permutations(range(1, 8)) if all(adj(((0,) + p)[k], ((0,) + p)[(k + 1) % 8]) for k in range(8))]
und = {frozenset(frozenset((c[k], c[(k + 1) % 8])) for k in range(8)) for c in cyc}
check("Setting: the cube graph has 6 Hamiltonian cycles, 12 directed cycles from a given vertex", len(und) == 6 and len(cyc) == 12)
rev = lambda c: (c[0],) + tuple(reversed(c[1:]))

# ---- Lemma 1: the edge rotation
def Kmat(n): return sp.Matrix([[0, -n[2], n[1]], [n[2], 0, -n[0]], [-n[1], n[0], 0]])
cth, sth = sp.Rational(1, 3), 2 * sp.sqrt(2) / 3
def nvec(i, j):
    n = v[i].cross(v[j]); return n / sp.sqrt(n.dot(n))
def Rot(n, s):     # rotation about n with cos = 1/3, sin = s
    K = Kmat(n); return sp.eye(3) + s * K + (1 - cth) * K * K
Rij = {(i, j): sp.simplify(Rot(nvec(i, j), sth)) for i in range(8) for j in range(8) if adj(i, j)}
check("Lemma 1: R_ij is a rotation (R^T R = I, det 1) carrying v_i to v_j, on all 24 directed edges",
      all(sp.simplify(R.T * R - sp.eye(3)) == sp.zeros(3, 3) and sp.simplify(R.det()) == 1 and sp.simplify(R * v[i] - v[j]) == sp.zeros(3, 1)
          for (i, j), R in Rij.items()))
check("Lemma 1: R_ij^T = R(n_ij, -theta) = R_ji = R_ij^{-1}",
      all(sp.simplify(R.T - Rot(nvec(i, j), -sth)) == sp.zeros(3, 3) and sp.simplify(R.T - Rij[(j, i)]) == sp.zeros(3, 3) for (i, j), R in Rij.items()))
check("Lemma 1: transposition keeps the diagonal and exchanges the strict upper and lower triangles (and R_ij != R_ij^T)",
      all(all(sp.simplify(R[k, k] - R.T[k, k]) == 0 for k in range(3)) and
          all(sp.simplify(R[a, b] - R.T[b, a]) == 0 for a in range(3) for b in range(3) if a < b) and sp.simplify(R - R.T) != sp.zeros(3, 3)
          for R in Rij.values()))

# ---- Lemma 2: turning and enclosed area (Gauss-Bonnet)
V = [np.array([float(c) for c in u]) for u in v]
def tang(p, q):
    t = q - (p @ q) * p; return t / np.linalg.norm(t)
def turns(c):
    out = []
    for k in range(8):
        p, q, r = V[c[k - 1]], V[c[k]], V[c[(k + 1) % 8]]
        tin, tout = -tang(q, p), tang(q, r)
        out.append(np.arctan2(q @ np.cross(tin, tout), tin @ tout))
    return out
check("Lemma 2: at each vertex the three edges leave at 120 deg to one another, so every turn is +-pi/3",
      all(np.allclose(np.abs(turns(c)), np.pi / 3) for c in cyc))
check("Lemma 2: every Hamiltonian cycle makes four left and four right turns, so it encloses area exactly 2 pi (a hemisphere's worth)",
      all(sum(1 for t in turns(c) if t > 0) == 4 and np.isclose(2 * np.pi - sum(turns(c)), 2 * np.pi) for c in cyc))

# ---- Transports
def H_uniform(c):
    H = sp.eye(3)
    for k in range(8): H = Rij[(c[k], c[(k + 1) % 8])] * H
    return sp.simplify(H)
def step_chiral(i, j, relabel=False):
    R = Rij[(i, j)]
    return (R if inA(i) else R.T) if not relabel else (R.T if inA(i) else R)
def H_chiral(c, relabel=False):
    H = sp.eye(3)
    for k in range(8): H = step_chiral(c[k], c[(k + 1) % 8], relabel) * H
    return sp.simplify(H)
cosang = lambda H: sp.nsimplify(sp.simplify((H.trace() - 1) / 2))

# ---- Theorem 1: uniform transport
Hu = {c: H_uniform(c) for c in cyc}
check("Theorem 1: uniform transport returns the identity in SO(3) on all 12 cycles", all(H == sp.eye(3) for H in Hu.values()))
sx = sp.Matrix([[0, 1], [1, 0]]); sy = sp.Matrix([[0, -sp.I], [sp.I, 0]]); sz = sp.Matrix([[1, 0], [0, -1]])
def Ulift(n, sgn):   # SU(2) lift of the edge rotation: cos(theta/2) = sqrt(2/3), sin(theta/2) = sqrt(1/3)
    return sp.sqrt(sp.Rational(2, 3)) * sp.eye(2) - sp.I * sgn * sp.sqrt(sp.Rational(1, 3)) * (n[0] * sx + n[1] * sy + n[2] * sz)
sig_ = [sx, sy, sz]
def cover(U):
    return sp.Matrix(3, 3, lambda a, b: sp.simplify((sig_[a] * U * sig_[b] * U.H).trace() / 2))
check("Theorem 1: the SU(2) element of each edge covers R_ij (its SO(3) image is R_ij), on all 24 directed edges",
      all(sp.simplify(cover(Ulift(nvec(i, j), 1)) - Rij[(i, j)]) == sp.zeros(3, 3) for (i, j) in Rij))
def spin(c, chiral):
    H = sp.eye(2)
    for k in range(8):
        i, j = c[k], c[(k + 1) % 8]
        H = sp.simplify(Ulift(nvec(i, j), (1 if inA(i) else -1) if chiral else 1) * H)
    return sp.simplify(H)
Su = {c: spin(c, False) for c in cyc}
check("Theorem 1: its SU(2) lift is exactly -1 on all 12 cycles", all(sp.simplify(S + sp.eye(2)) == sp.zeros(2, 2) for S in Su.values()))
check("Theorem 1: two circuits give +1", all(sp.simplify(S * S - sp.eye(2)) == sp.zeros(2, 2) for S in Su.values()))
check("Theorem 1: uniform transport of the reversed cycle is the transpose: H_u(reverse C) = H_u(C)^T",
      all(sp.simplify(H_uniform(rev(c)) - Hu[c].T) == sp.zeros(3, 3) for c in cyc))

# ---- Theorem 2: chiral transport
Hc = {c: H_chiral(c) for c in cyc}
vals = {c: cosang(H) for c, H in Hc.items()}
check("Theorem 2: chiral transport is never the identity; cos(Theta) takes exactly the values -4639/6561 and -5983/6561",
      all(H != sp.eye(3) for H in Hc.values()) and set(vals.values()) == {sp.Rational(-4639, 6561), sp.Rational(-5983, 6561)})
check("Theorem 2: on every undirected cycle the two senses give the two different values",
      all({vals[c], vals[rev(c)]} == {sp.Rational(-4639, 6561), sp.Rational(-5983, 6561)} for c in cyc))
check("Theorem 2: 6561 = 3^8, and Theta = %.4f and %.4f deg (134.996 is not 3pi/4)" % (
      float(sp.acos(sp.Rational(-4639, 6561)) * 180 / sp.pi), float(sp.acos(sp.Rational(-5983, 6561)) * 180 / sp.pi)),
      6561 == 3**8 and sp.Rational(-4639, 6561) != -sp.sqrt(2) / 2)
ht = {sp.nsimplify(sp.simplify(spin(c, True).trace() / 2)) for c in cyc}
check("Theorem 2: SU(2) half-traces are exactly 31/81 and -17/81, with 2(31/81)^2 - 1 = -4639/6561 and 2(17/81)^2 - 1 = -5983/6561",
      ht == {sp.Rational(31, 81), sp.Rational(-17, 81)} and 2 * sp.Rational(31, 81)**2 - 1 == sp.Rational(-4639, 6561)
      and 2 * sp.Rational(17, 81)**2 - 1 == sp.Rational(-5983, 6561))
def shift(c, m): return tuple(c[(k + m) % 8] for k in range(8))
def H_chiral_seq(seq):
    H = sp.eye(3)
    for k in range(8): H = step_chiral(seq[k], seq[(k + 1) % 8]) * H
    return sp.simplify(H)
check("Theorem 2: the angle does not depend on the starting vertex (a shifted start conjugates the holonomy)",
      all(cosang(H_chiral_seq(shift(c, m))) == vals[c] for c in cyc[:4] for m in range(1, 8)))

# ---- Theorem 3: relabelling (parity) = reversal
check("Theorem 3: relabelling TetA <-> TetB gives H'(C) = H_chi(reverse C)^T exactly, on all 12 cycles",
      all(sp.simplify(H_chiral(c, relabel=True) - Hc[rev(c)].T) == sp.zeros(3, 3) for c in cyc))
check("Theorem 3: so relabelling exchanges the two values, as reversing the sense does",
      all(cosang(H_chiral(c, relabel=True)) == vals[rev(c)] for c in cyc))
check("Theorem 3: reversal uses the same eight step matrices in the opposite order",
      all(all(sp.simplify(step_chiral(c[(k + 1) % 8], c[k]) - step_chiral(c[k], c[(k + 1) % 8])) == sp.zeros(3, 3) for k in range(8)) for c in cyc[:4]))

# ---- Proposition 4: share-weighted steps
sig, th = sp.symbols('sigma theta', real=True)
n0 = sp.Matrix([0, 0, 1]); K0 = Kmat(n0)
S = sp.eye(3) + sig * sp.sin(th) * K0 + (1 - sp.cos(th)) * K0 * K0
mu = sp.symbols('mu', real=True)
Rg = sp.eye(3) + sp.sin(th) * K0 + (1 - sp.cos(th)) * K0 * K0
check("Prop 4: mu R + (1 - mu) R^T = I + sigma sin(theta) K + (1 - cos(theta)) K^2 with sigma = 2 mu - 1",
      sp.simplify(mu * Rg + (1 - mu) * Rg.T - S.subs(sig, 2 * mu - 1)) == sp.zeros(3, 3))
check("Prop 4: the weighted step is normal (commutes with its transpose)", sp.simplify(S * S.T - S.T * S) == sp.zeros(3, 3))
ev = sp.simplify(S[0:2, 0:2])
lam = sp.symbols('lam')
cp = sp.expand(sp.simplify((ev - lam * sp.eye(2)).det()))
check("Prop 4: eigenvalues 1 (along n) and cos(theta) +- i sigma sin(theta): a rotation by phi, tan phi = sigma tan theta, times a contraction rho = sqrt(cos^2 + sigma^2 sin^2) in the plane",
      sp.simplify(cp - sp.expand((lam - sp.cos(th))**2 + sig**2 * sp.sin(th)**2)) == 0 and sp.simplify(S[2, 2] - 1) == 0)
x = sp.symbols('x', positive=True)
check("Prop 4: with mu = x/(x+1), sigma = (x-1)/(x+1), the share difference; exchange x -> 1/x sends sigma -> -sigma",
      sp.simplify(2 * x / (x + 1) - 1 - (x - 1) / (x + 1)) == 0 and sp.simplify(((1 / x - 1) / (1 / x + 1)) + (x - 1) / (x + 1)) == 0)
check("Prop 4: sigma = +1, 0, -1 give rotation by +theta, 0 (pure contraction to 1/3), -theta",
      sp.simplify(S.subs(sig, 1) - Rg) == sp.zeros(3, 3) and sp.simplify(S.subs(sig, -1) - Rg.T) == sp.zeros(3, 3)
      and sp.simplify(S.subs({sig: 0, th: sp.acos(sp.Rational(1, 3))}) - S.subs({sig: 0, th: sp.acos(sp.Rational(1, 3))}).T) == sp.zeros(3, 3)
      and sp.simplify(S.subs({sig: 0, th: sp.acos(sp.Rational(1, 3))})[0, 0]) == sp.Rational(1, 3))
check("Prop 4: det = cos^2 + sigma^2 sin^2 >= 1/9 at cos(theta) = 1/3: every weighted step is invertible",
      sp.simplify(S.det() - (sp.cos(th)**2 + sig**2 * sp.sin(th)**2)) == 0)
Rn = {k: np.array(val.evalf(), dtype=float) for k, val in Rij.items()}
def Sw(i, j, s):
    R = Rn[(i, j)]; m = (1 + s) / 2
    return m * R + (1 - m) * R.T if inA(i) else m * R.T + (1 - m) * R
def Hw(c, s):
    H = np.eye(3)
    for k in range(8): H = Sw(c[k], c[(k + 1) % 8], s) @ H
    return H
def rot_deg(H):
    U, _, Vt = np.linalg.svd(H); Q = U @ Vt
    return np.degrees(np.arccos(np.clip((np.trace(Q) - 1) / 2, -1, 1)))
check("Prop 4: H_{-sigma}(C) = H_sigma(reverse C)^T on all 12 cycles (sigma = 0.9, 0.5, 0.2)",
      all(np.allclose(Hw(c, -s), Hw(rev(c), s).T) for c in cyc for s in (0.9, 0.5, 0.2)))
check("Prop 4: at sigma = 0 every step is symmetric and both senses have the same rotational part: no chirality",
      all(np.allclose(Sw(i, j, 0), Sw(i, j, 0).T) for (i, j) in Rn) and all(np.isclose(rot_deg(Hw(c, 0)), rot_deg(Hw(rev(c), 0))) for c in cyc))
chi = lambda c, s: rot_deg(Hw(c, s)) - rot_deg(Hw(rev(c), s))
check("Prop 4: the chirality (difference between the senses) is odd in sigma and nonzero away from 0",
      all(np.isclose(chi(c, s), -chi(c, -s), atol=1e-8) and abs(chi(c, s)) > 1e-3 for c in cyc for s in (0.3, 0.8)))
check("Prop 4: sigma = +-1 recover the two values of Theorem 2",
      all(np.isclose(np.cos(np.radians(rot_deg(Hw(c, 1.0)))), float(vals[c])) for c in cyc))

print(f"\n{sum(ok)}/{len(ok)} checks passed")
