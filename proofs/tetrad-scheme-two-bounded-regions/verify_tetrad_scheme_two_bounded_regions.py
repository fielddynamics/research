"""Machine checks for every claim of 'The Tetrad Scheme and the Two Bounded Regions'
(revised), labelled by the section of the note each one supports.
Exact (sympy) wherever the statement is algebraic; random sampling over all
four components of the Lorentz group where it is a statement about every frame.
One step is cited rather than computed: that SO(1+D, C) is connected (Borel).
Run: python verify_tetrad_scheme_two_bounded_regions.py"""
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

eta, P, T, R, I4 = eta_(3), P_(3), T_(3), R_(3), sp.eye(4)
etan = np.array(eta, dtype=float)

def boost(phi, axis):
    B = np.eye(4); c, s = np.cosh(phi), np.sinh(phi)
    B[0, 0] = B[axis, axis] = c; B[0, axis] = B[axis, 0] = s
    return B
def rot3(proper=True):
    Q, _ = np.linalg.qr(rng.normal(size=(3, 3)))
    if (np.linalg.det(Q) > 0) != proper: Q[:, 0] *= -1
    return Q
def spatial(Q):
    L = np.eye(4); L[1:, 1:] = Q; return L
def so_plus():
    L = np.eye(4)
    for _ in range(3):
        L = L @ spatial(rot3()) @ boost(rng.normal(scale=1.2), int(rng.integers(1, 4)))
    return L
REPS = [np.array(X, dtype=float) for X in (I4, T, R, R * T)]
def lorentz(k=None):
    return REPS[int(rng.integers(0, 4)) if k is None else k] @ so_plus()
def is_lorentz(L, tol=1e-8): return np.allclose(L.T @ etan @ L, etan, atol=tol)
root = lambda e: int(np.sign(np.linalg.det(e)))
t_ref = np.array([1.0, 0, 0, 0])                     # future-directed timelike reference
tau = lambda e: int(np.sign((e @ t_ref)[0]))

# ---- Setting
check("Quadratic: P, T, R and -I are Lorentz transformations, and PT = -I",
      all(X.T * eta * X == eta for X in (P, T, R, -I4)) and P * T == -I4)
E = sp.Matrix(4, 4, lambda i, j: sp.Symbol(f'e{i}{j}', real=True))
g_s = sp.Matrix(4, 4, lambda i, j: sp.Symbol(f'g{min(i, j)}{max(i, j)}', real=True))
check("Two components: same signature, so c = det g / det eta > 0 (200 random Lorentzian metrics)",
      all((np.linalg.det((e0 := rng.normal(size=(4, 4))).T @ etan @ e0) / np.linalg.det(etan)) > 0 for _ in range(200)))

# ---- Lemma 1
samples = [lorentz() for _ in range(400)]
check("Two components (time leg): samples from all four components are Lorentz, with |r|^2 = (L^0_0)^2 - 1",
      all(is_lorentz(L) and np.isclose(np.sum(L[0, 1:] ** 2), L[0, 0] ** 2 - 1) for L in samples)
      and {(root(L), int(np.sign(L[0, 0]))) for L in samples} == {(1, 1), (1, -1), (-1, 1), (-1, -1)})
good = True
for L in samples:
    u = np.concatenate([[rng.choice([-1, 1]) * (1 + rng.random())], rng.normal(size=3)])
    u[1:] *= abs(u[0]) * rng.random() / np.linalg.norm(u[1:])
    good &= np.sign((L @ u)[0]) == np.sign(L[0, 0]) * np.sign(u[0])
check("Two components (time leg): sgn (Lu)^0 = sgn L^0_0 * sgn u^0 for timelike u", good)
check("Two components (time leg): sgn L^0_0 is a homomorphism",
      all(np.sign((A @ B)[0, 0]) == np.sign(A[0, 0]) * np.sign(B[0, 0]) for A, B in ((lorentz(), lorentz()) for _ in range(400))))

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
check("Two components (canonical P): the centre of O(1,D) is +-I (D = 1..4, exact)",
      all((r := centre_solutions(D, True)) is not None and r[0] == r[1] * sp.eye(D + 1) and r[2] == [-1, 1] for D in (1, 2, 3, 4)))
check("Two components (canonical P): the centre of O(D) is +-I_D (D = 1..4, exact)",
      all((r := centre_solutions(D, False)) is not None and r[0] == r[1] * sp.eye(D) and r[2] == [-1, 1] for D in (1, 2, 3, 4)))

# ---- Theorem 1 (the scheme)
check("Quadratic: (det e)^2 det eta = det(e^T eta e) identically, so e is invertible on X_g (exact, symbolic e)",
      sp.expand(E.det() ** 2 * eta.det() - (E.T * eta * E).det()) == 0)
good = True
for _ in range(200):
    e0 = rng.normal(size=(4, 4)); g = e0.T @ etan @ e0
    L = lorentz(); e1 = L @ e0
    good &= np.allclose(e1.T @ etan @ e1, g) and is_lorentz(e1 @ np.linalg.inv(e0)) and np.allclose(e1 @ np.linalg.inv(e0), L)
check("Quadratic: L -> L e0 and e -> e e0^{-1} are inverse maps between O(1,3) and the real tetrads (200 metrics)", good)
good = True; roots_seen = set()
for _ in range(200):
    e0 = rng.normal(size=(4, 4)); g = e0.T @ etan @ e0; c = np.linalg.det(g) / np.linalg.det(etan)
    for _ in range(4):
        e1 = lorentz() @ e0; good &= np.isclose(np.linalg.det(e1) ** 2, c); roots_seen.add(int(np.sign(np.linalg.det(e1)) * np.sign(np.linalg.det(e0))))
check("Two components: every tetrad has (det e)^2 = c, and both roots det e = +-sqrt(c) occur", good and roots_seen == {1, -1})
check("Two components: under the isomorphism, the root of L e0 is det L * root(e0), so the fibres are SO and R*SO",
      all(root(L @ (e0 := rng.normal(size=(4, 4)))) == root(L) * root(e0) for L in samples))
print("     (cited: SO(1+D, C) is connected [Borel], so each fibre is geometrically connected)")
good = all(T_(D).det() == -1 and R_(D).det() == -1 and P_(D).det() == (-1) ** D and (-sp.eye(D + 1)).det() == (-1) ** (D + 1)
           for D in range(1, 9))
check("Two components: det T = det R = -1, det P = (-1)^D, det(-I) = (-1)^(D+1), for D = 1..8", good)
check("Two components: for D = 3, P and T exchange the roots and -I does not (exact, symbolic e)",
      sp.simplify((P * E).det() + E.det()) == 0 and sp.simplify((T * E).det() + E.det()) == 0 and sp.simplify((-E).det() - E.det()) == 0)

# ---- Theorem 2 (real points)
good = True; pieces = set()
for k in range(4):
    for _ in range(100):
        e0 = so_plus(); L = lorentz(k); e1 = L @ e0
        good &= tau(e1) == int(np.sign(L[0, 0])) * tau(e0); pieces.add((root(e1), tau(e1)))
check("Two components: tau(Le) = sgn L^0_0 * tau(e), and the real tetrads fall into four pieces (root, tau)",
      good and pieces == {(1, 1), (1, -1), (-1, 1), (-1, -1)})
good = True
for _ in range(200):
    e0 = so_plus(); Q = rot3(proper=bool(rng.integers(0, 2))); e1 = spatial(Q) @ e0
    good &= tau(e1) == tau(e0) == 1 and (root(e1) != root(e0)) == (np.linalg.det(Q) < 0)
check("Two components (one observer): a frame change diag(1,Q) keeps the observer and tau, and exchanges the roots iff det Q = -1", good)
good = True
for _ in range(200):
    e0 = so_plus(); L = lorentz(int(rng.choice([0, 2]))); e1 = L @ e0          # future-pointing frames only
    Ev = np.linalg.inv(e1)[:, 1:]                                              # spatial frame vectors, in coordinates
    adapted = np.linalg.inv(e0)                                                # basis of the reference frame
    spatial_coords = np.linalg.solve(adapted, Ev)                              # components of E_i in that basis
    hand = np.sign(np.linalg.det(spatial_coords[1:, :]))                       # handedness of the spatial legs
    good &= tau(e1) == 1 and hand == root(e1) * root(e0)
check("Two components (one observer): for future-pointing frames, the root is the handedness of the spatial legs", good)
Y = centre_solutions(3, False)
check("Two components (canonical P): in O(3) the only elements commuting with every rotation and reflection are +-I_3, and only -I_3 is improper",
      Y[2] == [-1, 1] and (-sp.eye(3)).det() == -1 and sp.eye(3).det() == 1)
check("Two components (cautions): for D = 3, -e keeps the root and reverses tau, and -e = T(Pe)",
      all(root(-e0) == root(e0) and tau(-e0) == -tau(e0) for e0 in (so_plus() @ rng.normal(size=(4, 4)) for _ in range(100)))
      and T * P == -I4)
Bx = sp.eye(4); Bx[0, 0] = Bx[1, 1] = sp.Rational(5, 3); Bx[0, 1] = Bx[1, 0] = sp.Rational(4, 3)
check("Two components (canonical P): P is not central in O(1,3): P B P = B^{-1} != B for a boost",
      P * Bx * P == Bx.inv() and P * Bx * P != Bx)

# ---- Theorem 3 (root-blindness)
check("Both present: det(Pe)^2 = det(e)^2: the metric sees (det e)^2 only (exact)",
      sp.expand((P * E).det() ** 2 - E.det() ** 2) == 0)
x = sp.symbols('x0:4', real=True)
A, Bf, Cf = sp.Function('A')(x[0], x[1]), sp.Function('B')(x[0], x[1]), sp.Function('C')(x[0], x[1])
ef = sp.Matrix([[A, Cf, 0, 0], [0, Bf, 0, 0], [0, 0, A * Bf, 0], [0, 0, 0, 1 + x[1] ** 2]])
def christoffel(g):
    gi = g.inv()
    return [[[sp.simplify(sum(gi[l, m] * (sp.diff(g[m, i], x[j]) + sp.diff(g[m, j], x[i]) - sp.diff(g[i, j], x[m])) for m in range(4)) / 2)
              for j in range(4)] for i in range(4)] for l in range(4)]
g1 = sp.simplify(ef.T * eta * ef)
check("Both present: a tetrad field e(x), Pe(x), Te(x), -e(x) and (PB)e(x) give the identical metric field (exact)",
      all(sp.simplify((o.T * eta * o) - g1) == sp.zeros(4, 4) for o in (P * ef, T * ef, -ef, P * Bx * ef)))
check("Both present: and identical Christoffel symbols for e(x) and Pe(x) (computed, not assumed)",
      christoffel(g1) == christoffel(sp.simplify((P * ef).T * eta * (P * ef))))
check("Both present: SO+(1,3) lies in one root: every sampled proper orthochronous L has det L = 1",
      all(np.isclose(np.linalg.det(so_plus()), 1) for _ in range(200)))

# ---- Theorem 4 (the two tetrahedra)
M = sp.Matrix([[1, 1, -1, -1], [1, -1, 1, -1], [1, -1, -1, 1]]); Mn = np.array(M, dtype=float)
check("Two components: M^T M = 4I - J, the forced regular tetrahedron",
      M.T * M == 4 * sp.eye(4) - sp.ones(4, 4))
def n_coords(e, e_ref):
    Ev, Er = np.linalg.inv(e), np.linalg.inv(e_ref)
    n = Ev[:, 1:] @ Mn
    c = np.linalg.lstsq(Er[:, 1:], n, rcond=None)[0]
    return c, np.allclose(Er[:, 1:] @ c, n)
good = True
for _ in range(100):
    e0 = so_plus() @ rng.normal(size=(4, 4))
    for Z, target in ((np.array(P, dtype=float), -Mn), (-np.eye(4), -Mn), (np.array(T, dtype=float), Mn)):
        c, inW = n_coords(Z @ e0, e0); good &= inW and np.allclose(c, target)
check("Two components: n(Pe) = n(-e) = -M and n(Te) = M (100 random frames)", good)
good = True
for _ in range(200):
    e0 = so_plus(); proper = bool(rng.integers(0, 2)); Q = rot3(proper); e1 = spatial(Q) @ e0
    c, inW = n_coords(e1, e0)
    same_root = root(e1) == root(e0)
    Rc = c @ np.linalg.pinv(Mn) if same_root else c @ np.linalg.pinv(-Mn)      # c = Rc M or Rc (-M)
    good &= inW and np.allclose(c, Q.T @ Mn) and same_root == proper and np.allclose(Rc.T @ Rc, np.eye(3)) and np.isclose(np.linalg.det(Rc), 1)
check("Two components (one observer): diag(1,Q)e gives Q^T M: a rotation of M in the root of e, a rotation of -M in the other", good)
Qsol = (-M) * M.T * (M * M.T).inv()
check("Two components (not a rotation): rank M = 3 and QM = -M forces Q = -I, of determinant -1 (exact)",
      M.rank() == 3 and Qsol == -sp.eye(3) and Qsol.det() == -1)
def simplex(D):
    X = sp.eye(D + 1) - sp.ones(D + 1, D + 1) / (D + 1)
    basis = sp.GramSchmidt([X[:, i] for i in range(D)], True)
    return sp.Matrix.hstack(*basis).T * X
good = True
for D in range(1, 6):
    S = simplex(D); G = sp.simplify(S.T * S)
    regular = len({sp.nsimplify(G[i, i]) for i in range(D + 1)}) == 1 and len({sp.nsimplify(G[i, j]) for i in range(D + 1) for j in range(D + 1) if i != j}) == 1
    Q = sp.simplify((-S) * S.T * (S * S.T).inv())
    good &= regular and S.rank() == D and Q == -sp.eye(D) and Q.det() == (-1) ** D
check("Two components (D odd): for the regular simplex in R^D (D = 1..5), QM = -M forces Q = -I_D, of det (-1)^D", good)
def vertices(N):
    out = set()
    for tri in itertools.combinations(range(4), 3):
        A_ = sp.Matrix.hstack(*[N[:, a] for a in tri]).T
        if A_.det() == 0: continue
        v = A_.inv() * sp.ones(3, 1)
        if all((N[:, a].T * v)[0] <= 1 for a in range(4)): out.add(tuple(v))
    return out
VA, VB = vertices(M), vertices(-M)
check("Two components (Route 1): the regions {max n.x <= 1} and {max(-n.x) <= 1} have vertex sets V and -V",
      len(VA) == 4 and VB == {tuple(-sp.Matrix(v)) for v in VA})
good = all((np.max(Mn.T @ (-p)) <= 1) == (np.max(-Mn.T @ p) <= 1) for p in rng.uniform(-3, 3, size=(2000, 3)))
check("Two components (Route 1): x is in TetB iff -x is in TetA (2000 random points)", good)
check("Summary: the eight vertices are the cube {-1,+1}^3, the stellated octahedron",
      VA | VB == set(itertools.product([-1, 1], repeat=3)) and not (VA & VB))

# ---- Remark
Rz = sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
check("Two components (cautions): the 90-degree rotation about the third axis maps the vertex set of TetA onto that of TetB, but Rz M != -M",
      Rz.det() == 1 and {tuple(Rz * sp.Matrix(v)) for v in VA} == VB and Rz * M != -M)
check("Two components (cautions): -e carries TetB (n = -M) in the root of e (det(-e) = det e), because it reverses tau",
      all(np.allclose(n_coords(-e0, e0)[0], -Mn) and root(-e0) == root(e0) and tau(-e0) == -tau(e0)
          for e0 in (so_plus() for _ in range(50))))

# ---- Scope
e_a = sp.Matrix([[1, 0], [1, 0]]); eta2 = eta_(1); y = sp.Symbol('y')
check("Quadratic: det g = 0 gives c = 0 and y^2 = 0 a double root; for g = 0, D = 1, both 0 and [[1,0],[1,0]] solve",
      sp.roots(y ** 2 - 0, y) == {0: 2} and e_a.T * eta2 * e_a == sp.zeros(2, 2) and e_a.rank() == 1)
check("Two components (D odd): for D = 2, det P = +1, so parity keeps the root, and -M_2 is M_2 turned by pi",
      P_(2).det() == 1 and sp.Matrix([[-1, 0], [0, -1]]) * simplex(2) == -simplex(2) and sp.Matrix([[-1, 0], [0, -1]]).det() == 1)

# ---- Both present: the signature convention selects nothing
etam = -eta
check("Both present: flipping the signature convention (eta -> -eta) leaves the Lorentz group unchanged",
      all(np.allclose(L.T @ np.array(etam, dtype=float) @ L, np.array(etam, dtype=float)) for L in samples))

# ---- 3+1 decomposition
patterns_A = [tuple(int(v) for v in M[:, a]) for a in range(4)]
patterns_B = [tuple(-v for v in p) for p in patterns_A]
uni = lambda ps: [p for p in ps if len(set(p)) == 1]
check("3+1: TetA's normals have one uniform-sign pattern (+,+,+) and three mixed; TetB's have (-,-,-) and three mixed",
      uni(patterns_A) == [(1, 1, 1)] and uni(patterns_B) == [(-1, -1, -1)] and sum(len(set(p)) > 1 for p in patterns_A + patterns_B) == 6)
check("3+1: parity exchanges the uniform-sign normals (+,+,+) and (-,-,-)",
      tuple(-v for v in uni(patterns_A)[0]) == uni(patterns_B)[0])
cols = [sp.Matrix(p) for p in patterns_A]
transitive = all(any(sp.Matrix(Q) * cols[0] == cols[k] and {tuple(sp.Matrix(Q) * c) for c in cols} == set(patterns_A)
                     for Q in (sp.diag(1, -1, -1), sp.diag(-1, 1, -1), sp.diag(-1, -1, 1)))
                 for k in (1, 2, 3))
check("3+1: the tetrahedron's own rotations (by pi about each axis) carry the uniform normal to each mixed one, so the split is fixed by the frame's legs",
      transitive)

print(f"\n{sum(ok)}/{len(ok)} checks passed")
