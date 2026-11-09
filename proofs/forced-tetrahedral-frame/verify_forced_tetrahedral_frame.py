"""Machine checks for every step of 'The Spatial Geometry of the Lorentz Tetrad'.
Run: python verify_forced_tetrahedral_frame.py"""
import itertools
import numpy as np
import sympy as sp

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

I4, J4, one = sp.eye(4), sp.ones(4, 4), sp.ones(4, 1)
perms = [sp.Matrix(4, 4, lambda i, j: 1 if p[i] == j else 0) for p in itertools.permutations(range(4))]
a, b, c, q, t = sp.symbols('alpha beta c q t', real=True)

# ---- Setting
eta = sp.diag(-1, 1, 1, 1)
check("Setting: |eta| = identity, invariant under all 24 permutations of the legs",
      eta.applyfunc(abs) == I4 and all(P * I4 * P.T == I4 for P in perms))
check("Setting: eta itself is invariant under exactly the 6 permutations fixing the time leg",
      sum(P * eta * P.T == eta for P in perms) == 6)

# ---- Lemma 1 (commutant)
g = sp.Matrix(4, 4, lambda i, j: sp.Symbol(f'g{i}{j}'))
eqs = [e for P in perms for e in (P * g * P.T - g)]
sol = sp.solve(eqs, list(g), dict=True)[0]
gs = g.subs(sol); free = sorted(gs.free_symbols, key=str)
check("Remark: S4-invariant 4x4 matrices form a 2-dimensional space",
      len(free) == 2)
check("Remark: that space is spanned by I and J, i.e. (M)+(R) <=> S4-invariance",
      all(sp.simplify(gs.subs({free[0]: x, free[1]: y}) - (gs.subs({free[0]: x, free[1]: y})[0, 1] * J4 + (gs.subs({free[0]: x, free[1]: y})[0, 0] - gs.subs({free[0]: x, free[1]: y})[0, 1]) * I4)) == sp.zeros(4, 4)
          for x, y in [(1, 0), (0, 1), (2, 5)]))
check("Remark converse: I and J commute with every permutation matrix",
      all(P * I4 * P.T == I4 and P * J4 * P.T == J4 for P in perms))

# ---- Lemma 2 (rigidity), numerical with random data
rng = np.random.default_rng(1)
good = True
for _ in range(200):
    U = rng.normal(size=(3, 4))
    Q, _r = np.linalg.qr(rng.normal(size=(3, 3)))
    W = Q @ U
    Qrec = W @ np.linalg.pinv(U)              # the map U lambda -> W lambda on the column space
    good &= np.allclose(U.T @ U, W.T @ W) and np.allclose(Qrec, Q) and np.allclose(Qrec.T @ Qrec, np.eye(3))
check("Lemma (rigidity): equal Gram matrices of rank 3 differ by a unique orthogonal Q (200 random cases)", good)

# ---- Theorem
G = a * I4 + b * J4
check("Theorem: (M),(R) give G = c^2 I + beta(J-I) = alpha I + beta J; eigenvalues are alpha (x3) and alpha+4beta (x1)",
      G.eigenvals() == {a: 3, a + 4 * b: 1})
check("Theorem: every pair at the same distance |v_a - v_b|^2 = 2 alpha",
      all(sp.expand(G[i, i] + G[j, j] - 2 * G[i, j]) == 2 * a for i in range(4) for j in range(4) if i != j))
check("Theorem: alpha>0 and alpha+4beta != 0 gives rank 4 (impossible in R^3)",
      (G.subs({a: 1, b: 1})).rank() == 4 and (G.subs({a: 1, b: -sp.Rational(1, 3)})).rank() == 4)
check("Theorem: alpha+4beta = 0 gives rank 3 and G*1 = 0 (closure)",
      G.subs(b, -a / 4).subs(a, 1).rank() == 3 and sp.simplify(G.subs(b, -a / 4) * one) == sp.zeros(4, 1))
forced = c**2 * I4 - c**2 / 3 * (J4 - I4)
check("Theorem: c^2 = alpha+beta = 3alpha/4 and beta = -c^2/3 give the forced Gram matrix",
      sp.simplify(G.subs(b, -a / 4).subs(a, sp.Rational(4, 3) * c**2) - forced) == sp.zeros(4, 4))

# ---- Corollary 1
M = sp.Matrix([[1, 1, -1, -1], [1, -1, 1, -1], [1, -1, -1, 1]])
check("Corollary 1: M^T M = 3I - (J - I)", M.T * M == 3 * I4 - (J4 - I4))
check("Corollary 1: (c/sqrt3) M realises the forced Gram matrix",
      sp.simplify((c / sp.sqrt(3) * M).T * (c / sp.sqrt(3) * M) - forced) == sp.zeros(4, 4))
check("Corollary 1: edges all c*sqrt(8/3); centroid of M at the origin",
      all(sp.simplify(forced[i, i] + forced[j, j] - 2 * forced[i, j] - sp.Rational(8, 3) * c**2) == 0
          for i in range(4) for j in range(4) if i != j) and M * one == sp.zeros(3, 1))
check("Corollary 1: each pair of columns of M agrees in exactly one coordinate",
      all(sum(M[k, i] == M[k, j] for k in range(3)) == 1 for i in range(4) for j in range(i + 1, 4)))

# ---- Corollary 2 (dimension), K = 2..8
good = True
for K in range(2, 9):
    GK = a * sp.eye(K) + b * sp.ones(K, K)
    ev = GK.eigenvals()
    good &= ev == {a: K - 1, a + K * b: 1}
    good &= GK.subs({a: 1, b: -sp.Rational(1, K)}).rank() == K - 1        # simplex: rank K-1
    good &= GK.subs({a: 1, b: 0}).rank() == K                              # orthogonal legs need D >= K
    # explicit regular simplex in R^(K-1): centred standard basis, then orthonormal coordinates
    E = np.eye(K) - np.ones((K, K)) / K
    w, Vv = np.linalg.eigh(E); X = (Vv[:, w > 1e-9] * np.sqrt(w[w > 1e-9])).T   # (K-1) x K
    Gx = X.T @ X
    good &= X.shape[0] == K - 1 and np.allclose(np.diag(Gx), Gx[0, 0]) and np.allclose(Gx.sum(axis=1), 0)
check("Corollary 2: for K = 2..8, rank >= K-1; simplex realised in R^(K-1) with closure; beta=0 needs D >= K", good)

# ---- Corollary 3 (parity completion)
cols = {tuple(M[:, j]) for j in range(4)}; ncols = {tuple(-M[:, j]) for j in range(4)}
check("Corollary 3: -M has the same Gram matrix", (-M).T * (-M) == M.T * M)
check("Corollary 3: M and -M share no point; together they are the 8 vertices of {-1,+1}^3",
      cols.isdisjoint(ncols) and cols | ncols == set(itertools.product([-1, 1], repeat=3)))
check("Corollary 3: no shared point in general, since G_ab never equals -c^2",
      all(sp.simplify(forced[i, j] + c**2) != 0 for i in range(4) for j in range(4)))

# ---- Necessity table
v, w = sp.Matrix([1, 0, 0]), sp.Matrix([0, 1, 0])
Sq = sp.Matrix.hstack(v, w, -v, -w); GS = Sq.T * Sq
check("Necessity (R): square (v,w,-v,-w) is distinct, equal-norm, closed, in R^3, but not S4-invariant",
      len({tuple(Sq[:, j]) for j in range(4)}) == 4 and Sq * one == sp.zeros(3, 1)
      and all(GS[i, i] == 1 for i in range(4)) and not all(P * GS * P.T == GS for P in perms))
check("Necessity (N): all legs equal gives G = c^2 J, S4-invariant, rank 1",
      all(P * J4 * P.T == J4 for P in perms) and J4.rank() == 1)
check("Necessity (D): in R^4 the orthonormal legs give G = c^2 I: S4-invariant, distinct, not closed",
      I4 * one != sp.zeros(4, 1) and I4.rank() == 4)
check("Necessity (D): in R^2 no realisation (rank >= 3 whenever alpha > 0)",
      all(G.subs({a: 1, b: bv}).rank() >= 3 for bv in [-1, -sp.Rational(1, 4), 0, 2]))
Xo = sp.Matrix.hstack(sp.zeros(3, 1), sp.eye(3)); Go = Xo.T * Xo
check("Necessity (M): observer projection v0 = 0, v_i orthonormal: equal relation (all 0), distinct, in R^3, not a tetrahedron",
      all(Go[i, j] == 0 for i in range(4) for j in range(4) if i != j) and Go[0, 0] == 0 and Go[1, 1] == 1)
Gn = -sp.ones(4, 4) + sp.diag(2, 4, 8, 8)            # diagonal (1,3,7,7), off-diagonal -1
ev = Gn.eigenvals()
check("Necessity (M): non-zero legs with G_aa = (1,3,7,7), G_ab = -1: PSD of rank 3, so realisable in R^3, unequal norms",
      Gn.rank() == 3 and all(sp.re(k) >= 0 for k in ev) and [Gn[i, i] for i in range(4)] == [1, 3, 7, 7])
Xn = np.linalg.eigh(np.array(Gn, dtype=float)); wv, Vv = Xn
Xr = (Vv[:, wv > 1e-9] * np.sqrt(wv[wv > 1e-9])).T
check("Necessity (M): explicit realisation of that Gram matrix in R^3",
      Xr.shape == (3, 4) and np.allclose(Xr.T @ Xr, np.array(Gn, dtype=float)))
check("Premise (R): four mutually orthogonal non-zero vectors need rank 4, impossible in R^3",
      (I4).rank() == 4)

print(f"\n{sum(ok)}/{len(ok)} checks passed")
