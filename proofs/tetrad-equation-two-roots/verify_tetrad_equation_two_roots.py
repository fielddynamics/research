"""Machine checks for every step of 'The Two Roots of the Tetrad Equation'.
Exact (sympy) wherever the statement is algebraic; random sampling over all
four components of the Lorentz group where it is a statement about every frame.
Run: python verify_tetrad_equation_two_roots.py"""
import itertools
import numpy as np
import sympy as sp

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

rng = np.random.default_rng(7)

def eta_(D): return sp.diag(-1, *([1] * D))
def P_(D):   return sp.diag(1, *([-1] * D))
def T_(D):   return sp.diag(-1, *([1] * D))
def R_(D):   return sp.diag(1, -1, *([1] * (D - 1)))
def s_(L):   return sp.sign(L.det()) * sp.sign(L[0, 0])
def s_num(L): return np.sign(np.linalg.det(L)) * np.sign(L[0, 0])

eta, P, T, R, I4 = eta_(3), P_(3), T_(3), R_(3), sp.eye(4)
etan = np.array(eta, dtype=float)

def boost(phi, axis):
    B = np.eye(4); c, s = np.cosh(phi), np.sinh(phi)
    B[0, 0] = B[axis, axis] = c; B[0, axis] = B[axis, 0] = s
    return B
def rot():
    Q, _ = np.linalg.qr(rng.normal(size=(3, 3)))
    if np.linalg.det(Q) < 0: Q[:, 0] *= -1
    L = np.eye(4); L[1:, 1:] = Q; return L
def so_plus():
    L = np.eye(4)
    for _ in range(3):
        L = L @ rot() @ boost(rng.normal(scale=1.2), int(rng.integers(1, 4)))
    return L
REPS = [np.array(X, dtype=float) for X in (I4, T, R, R * T)]
def lorentz():
    return REPS[int(rng.integers(0, 4))] @ so_plus()
def is_lorentz(L, tol=1e-8): return np.allclose(L.T @ etan @ L, etan, atol=tol)

# ---- Setting
check("Setting: P, T, R and -I are Lorentz transformations",
      all(X.T * eta * X == eta for X in (P, T, R, -I4)))
check("Setting: PT = -I",
      P * T == -I4)
check("Setting: s(I) = s(T) = 1 and s(R) = s(RT) = -1, so the four components fall into two classes",
      [s_(X) for X in (I4, T, R, R * T)] == [1, 1, -1, -1])

# ---- Lemma 1
samples = [lorentz() for _ in range(400)]
check("Lemma 1: sampled transformations from all four components satisfy L^T eta L = eta",
      all(is_lorentz(L) for L in samples) and {int(s_num(L)) * 10 + int(np.sign(L[0, 0])) for L in samples} == {11, -11, 9, -9})
check("Lemma 1: L eta L^T = eta, and |r|^2 = (L^0_0)^2 - 1 for the first row",
      all(np.allclose(L @ etan @ L.T, etan) and np.isclose(np.sum(L[0, 1:] ** 2), L[0, 0] ** 2 - 1) for L in samples))
good = True
for L in samples:
    u = np.concatenate([[rng.choice([-1, 1]) * (1 + rng.random())], rng.normal(size=3)])
    u[1:] *= abs(u[0]) * rng.random() / np.linalg.norm(u[1:])           # timelike: |u_vec| < |u0|
    good &= np.sign((L @ u)[0]) == np.sign(L[0, 0]) * np.sign(u[0])
check("Lemma 1: sgn (Lu)^0 = sgn L^0_0 * sgn u^0 for timelike u (400 frames, all components)", good)
pairs = [(lorentz(), lorentz()) for _ in range(400)]
check("Lemma 1: sgn L^0_0 and s are homomorphisms",
      all(np.sign((A @ B)[0, 0]) == np.sign(A[0, 0]) * np.sign(B[0, 0]) and s_num(A @ B) == s_num(A) * s_num(B) for A, B in pairs))

# ---- Lemma 2 (exact)
def centre_solutions(D, lorentzian):
    n = D + 1 if lorentzian else D
    Z = sp.Matrix(n, n, lambda i, j: sp.Symbol(f'z{i}{j}'))
    gens = []
    for signs in itertools.product([1, -1], repeat=D):
        S = sp.diag(*signs); gens.append(sp.diag(1, S) if lorentzian else S)
    for p in itertools.permutations(range(D)):
        S = sp.Matrix(D, D, lambda i, j: 1 if p[i] == j else 0); gens.append(sp.diag(1, S) if lorentzian else S)
    if lorentzian:
        B = sp.eye(n); B[0, 0] = B[1, 1] = sp.Rational(5, 3); B[0, 1] = B[1, 0] = sp.Rational(4, 3)
        gens.append(B)
    eqs = [x for G in gens for x in (Z * G - G * Z) if x != 0]
    sol = sp.solve(eqs, list(Z), dict=True)[0] if eqs else {}
    Zs = Z.subs(sol); free = sorted(Zs.free_symbols, key=str)
    if len(free) != 1: return None
    lam = free[0]
    met = eta_(D) if lorentzian else sp.eye(D)
    lams = sp.solve([x for x in (Zs.T * met * Zs - met) if x != 0], lam, dict=True)
    return Zs, lam, sorted(d[lam] for d in lams)
res = all((r := centre_solutions(D, True)) is not None and r[0] == r[1] * sp.eye(D + 1) and r[2] == [-1, 1] for D in (1, 2, 3, 4))
check("Lemma 2: matrices commuting with the generators of O(1,D) are lambda*I, and lambda = +-1 (D = 1..4, exact)", res)
res = all((r := centre_solutions(D, False)) is not None and r[0] == r[1] * sp.eye(D) and r[2] == [-1, 1] for D in (1, 2, 3, 4))
check("Lemma 2: the centre of O(D) is +-I (D = 1..4, exact)", res)
Bx = sp.eye(4); Bx[0, 0] = Bx[1, 1] = sp.Rational(5, 3); Bx[0, 1] = Bx[1, 0] = sp.Rational(4, 3)
check("Lemma 2 / Theorem 2: P B P = B^{-1} != B for a boost, so parity is not central",
      P * Bx * P == Bx.inv() and P * Bx * P != Bx)

# ---- Theorem 1
E = sp.Matrix(4, 4, lambda i, j: sp.Symbol(f'e{i}{j}', real=True))
check("Theorem 1(a): (-e)^T eta (-e) = e^T eta e identically (exact, symbolic e)",
      sp.expand((-E).T * eta * (-E) - E.T * eta * E) == sp.zeros(4, 4))
check("Theorem 1(a): det(e^T eta e) = (det e)^2 det eta identically, so every solution is invertible",
      sp.expand((E.T * eta * E).det() - E.det() ** 2 * eta.det()) == 0)
good = True
for _ in range(200):
    e0 = rng.normal(size=(4, 4)); g = e0.T @ etan @ e0
    L = lorentz(); e1 = L @ e0
    good &= np.allclose(e1.T @ etan @ e1, g)
    good &= is_lorentz(e1 @ np.linalg.inv(e0)) and np.allclose(e1 @ np.linalg.inv(e0), L)
check("Theorem 1(a): every Le solves, and every solution e' gives L = e' e^{-1} in O(1,3) (200 random metrics)", good)
t_future = np.array([1.0, 0, 0, 0])          # future-directed timelike reference in coordinates
def o_(e, t=t_future): return np.sign(np.linalg.det(e)) * np.sign((e @ t)[0])
good = True; seen = set()
for _ in range(300):
    e0 = so_plus() @ np.diag([1, 1, 1, 1.0])  # a solution for eta; then a generic metric
    C = rng.normal(size=(4, 4)); e0 = e0 @ C
    t = np.linalg.solve(C, t_future) if np.linalg.det(C) != 0 else t_future
    g = e0.T @ etan @ e0
    if t @ g @ t >= 0: continue
    L = lorentz(); good &= o_(L @ e0, t) == s_num(L) * o_(e0, t); seen.add(int(o_(L @ e0, t)))
check("Theorem 1(b): o(Le) = s(L) o(e), and both signs occur (exactly two classes)", good and seen == {1, -1})
check("Theorem 1(b): T preserves the class, R exchanges it",
      s_(T) == 1 and s_(R) == -1)
good = all(s_(-sp.eye(D + 1)) == (-1) ** D and s_(P_(D)) == (-1) ** D for D in range(1, 9))
check("Theorem 1(c): s(-I) = s(P) = (-1)^D for D = 1..8, so -e and Pe change class iff D is odd", good)
check("Theorem 1(c): for D = 3 both are -1",
      s_(-I4) == -1 and s_(P) == -1)

# ---- Theorem 2
good = True
for _ in range(100):
    L, e0 = lorentz(), rng.normal(size=(4, 4))
    good &= np.allclose(L @ (-e0), -(L @ e0))
check("Theorem 2: e -> -e commutes with every change of frame (100 random frames)", good)
fails = {name: any(not np.allclose(L @ (np.array(Z, dtype=float) @ e0), np.array(Z, dtype=float) @ (L @ e0))
                   for L, e0 in ((lorentz(), rng.normal(size=(4, 4))) for _ in range(50)))
         for name, Z in (("P", P), ("T", T), ("R", R))}
check("Theorem 2: e -> Pe, Te, Re each fail to commute with some change of frame",
      all(fails.values()))
check("Theorem 2: Pe = T(-e)",
      T * (-I4) == P)

# ---- Theorem 3
x = sp.symbols('x0:4', real=True)
A, Bf, Cf = sp.Function('A')(x[0], x[1]), sp.Function('B')(x[0], x[1]), sp.Function('C')(x[0], x[1])
ef = sp.Matrix([[A, Cf, 0, 0], [0, Bf, 0, 0], [0, 0, A * Bf, 0], [0, 0, 0, 1 + x[1] ** 2]])
def christoffel(g):
    gi = g.inv()
    return [[[sp.simplify(sum(gi[l, m] * (sp.diff(g[m, i], x[j]) + sp.diff(g[m, j], x[i]) - sp.diff(g[i, j], x[m])) for m in range(4)) / 2)
              for j in range(4)] for i in range(4)] for l in range(4)]
g1 = sp.simplify(ef.T * eta * ef)
Lc = (P * Bx)                      # a constant transformation in the parity class
others = [(-ef), (P * ef), (Lc * ef)]
check("Theorem 3: a tetrad field e(x), -e(x), Pe(x) and (PB)e(x) give the identical metric field (exact)",
      all(sp.simplify((o.T * eta * o) - g1) == sp.zeros(4, 4) for o in others))
G1 = christoffel(g1); G2 = christoffel(sp.simplify((-ef).T * eta * (-ef)))
check("Theorem 3: and therefore identical Christoffel symbols (computed, not assumed)",
      G1 == G2)
check("Theorem 3: -I is not in SO+(1,3), since (-I)^0_0 = -1",
      (-I4)[0, 0] == -1)

# ---- Theorem 4
M = sp.Matrix([[1, 1, -1, -1], [1, -1, 1, -1], [1, -1, -1, 1]])
check("Theorem 4: M^T M = 4I - J, the forced regular tetrahedron",
      M.T * M == 4 * sp.eye(4) - sp.ones(4, 4))
def n_coords(e, e_ref):
    """Coordinates, in the spatial frame vectors of e_ref, of the four directions built from e."""
    Ev, Er = np.linalg.inv(e), np.linalg.inv(e_ref)          # columns are frame vectors E_a
    n = Ev[:, 1:] @ np.array(M, dtype=float)                 # n_a = sum_i M_ia E_i
    return np.linalg.lstsq(Er[:, 1:], n, rcond=None)[0], np.allclose(Er[:, 1:] @ np.linalg.lstsq(Er[:, 1:], n, rcond=None)[0], n)
good = True; Mn = np.array(M, dtype=float)
for _ in range(100):
    e0 = rng.normal(size=(4, 4))
    for Z, target in ((-np.eye(4), -Mn), (np.array(P, dtype=float), -Mn), (np.array(T, dtype=float), Mn)):
        c, inW = n_coords(Z @ e0, e0); good &= inW and np.allclose(c, target)
    Q = np.array(rot()[1:, 1:]) @ np.diag([1, 1, rng.choice([-1, 1])]); eps = rng.choice([-1, 1])
    L = np.eye(4); L[0, 0] = eps; L[1:, 1:] = Q
    c, inW = n_coords(L @ e0, e0)
    good &= inW and np.allclose(c, Q.T @ Mn) and np.isclose(np.linalg.det(Q.T), s_num(L))
check("Theorem 4(a): n(-e) = n(Pe) = -M, n(Te) = M, n(diag(eps,Q)e) = Q^T M with det Q^T = s (100 random frames)", good)
Qsol = (-M) * M.T * (M * M.T).inv()
check("Theorem 4(b): rank M = 3 and QM = -M forces Q = -I, of determinant -1 (exact)",
      M.rank() == 3 and Qsol == -sp.eye(3) and Qsol.det() == -1)
def simplex(D):
    X = sp.eye(D + 1) - sp.ones(D + 1, D + 1) / (D + 1)       # D+1 points spanning a D-dim space
    basis = sp.GramSchmidt([X[:, i] for i in range(D)], True)
    return sp.Matrix.hstack(*basis).T * X                     # D x (D+1), regular simplex
good = True
for D in range(1, 6):
    S = simplex(D); G = sp.simplify(S.T * S)
    regular = len({sp.nsimplify(G[i, i]) for i in range(D + 1)}) == 1 and len({sp.nsimplify(G[i, j]) for i in range(D + 1) for j in range(D + 1) if i != j}) == 1
    Q = sp.simplify((-S) * S.T * (S * S.T).inv())
    good &= regular and S.rank() == D and Q == -sp.eye(D) and Q.det() == (-1) ** D
check("Theorem 4(b): for the regular simplex in R^D (D = 1..5), the only map with QM = -M is -I, of det (-1)^D", good)
Rpi = sp.Matrix([[-1, 0], [0, -1]])
check("Theorem 4(b) / Scope: for D = 2 that map is the rotation by pi, in SO(2)",
      Rpi.det() == 1 and Rpi * simplex(2) == -simplex(2))
def vertices(N):
    """Vertices of {x : N[:,a].x <= 1 for all a} (exact)."""
    out = set()
    for tri in itertools.combinations(range(4), 3):
        A = sp.Matrix.hstack(*[N[:, a] for a in tri]).T
        if A.det() == 0: continue
        v = A.inv() * sp.ones(3, 1)
        if all((N[:, a].T * v)[0] <= 1 for a in range(4)): out.add(tuple(v))
    return out
VA, VB = vertices(M), vertices(-M)
check("Theorem 4(c): TetA = {max n.x <= 1} and the region of -e = {max(-n.x) <= 1} have vertex sets V and -V",
      len(VA) == 4 and VB == {tuple(-sp.Matrix(v)) for v in VA})
good = True
for _ in range(2000):
    p = rng.uniform(-3, 3, size=3)
    inA = np.max(np.array(M, dtype=float).T @ (-p)) <= 1; inB = np.max(-np.array(M, dtype=float).T @ p) <= 1
    good &= inA == inB
check("Theorem 4(c): x is in the region of -e iff -x is in TetA (2000 random points)", good)
check("Theorem 4(c): the eight vertices are the cube {-1,+1}^3, the stellated octahedron",
      VA | VB == set(itertools.product([-1, 1], repeat=3)) and not (VA & VB))

# ---- Remark
Rz = sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
check("Remark: the 90-degree rotation about the third axis (det +1) maps the vertex set of TetA onto that of TetB",
      Rz.det() == 1 and {tuple(Rz * sp.Matrix(v)) for v in VA} == VB)
check("Remark: but it reorders the legs: Rz M != -M",
      Rz * M != -M)

# ---- Scope
e_a = sp.Matrix([[1, 0], [1, 0]]); eta2 = eta_(1)
check("Scope: for g = 0, D = 1, both e = 0 and e = [[1,0],[1,0]] solve, and L*e_a is never 0, so S(g) is not one orbit",
      e_a.T * eta2 * e_a == sp.zeros(2, 2) and sp.zeros(2, 2).T * eta2 * sp.zeros(2, 2) == sp.zeros(2, 2) and e_a.rank() == 1)
check("Scope: for D = 2, s(-I) = +1, so -e stays in the class of e",
      s_(-sp.eye(3)) == 1)

print(f"\n{sum(ok)}/{len(ok)} checks passed")
