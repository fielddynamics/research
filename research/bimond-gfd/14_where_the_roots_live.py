"""14. Where the TetA/TetB distinction lives in the connection. A deduction from the frame.

A. Frame jets: the 64 first derivatives of a frame at a point are, one-to-one, the 40 first derivatives of
   the metric plus the 24 torsion components (Weitzenboeck). This is the covariant form of 64 = 40 + 24.
B. Levi-Civita uniqueness as algebra: on V(x)V(x)V, 'symmetric in the lower pair' and 'antisymmetric in the
   outer pair' (metric compatibility) intersect in 0 and together span all 64.
C. Two frames on the same metric, e' = L(x) e with L in O(1,3): their connections differ by
   e^-1 (L^-1 dL) e, which lies in the 24-dim contorsion space and depends only on L^-1 dL.
D. The second root: the 40 metric derivatives are the same for both roots, while the 24 torsion components in
   frame form, T^a = de^a, change with the root as the vielbein does (T^a -> P T^a). Expressed with coordinate
   indices (e_a^l T^a) the inverse frame applies P a second time and hides the sign, as forming g does.
E. Slow-motion force of the relative frame: -N^i_(00) = boost part of L^-1 d_0 L (the rate of relative
   rapidity). Rotations, and all spatial gradients, give no slow-motion force.
F. The torsion carried by four elementary relations (twist, spin, boost in time, boost in space), split
   into vector, axial and tensor parts.
"""
import itertools
import numpy as np
import sympy as sp

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

n = 4
etaN = np.diag([-1.0, 1, 1, 1])
rng = np.random.default_rng(7)
rank = lambda M: np.linalg.matrix_rank(M, tol=1e-9)
idx = lambda a, b, c: (a * n + b) * n + c

# ---------------------------------------------------------------- A: frame jets
def jet_map(e):
    """linear map  de[a, mu, nu] = d_mu e^a_nu  (64)  ->  (d_mu g_{nu rho} for nu<=rho (40), T^a_{mu nu} for mu<nu (24))"""
    rows = []
    basis = []
    for a, mu, nu in itertools.product(range(n), repeat=3):
        de = np.zeros((n, n, n)); de[a, mu, nu] = 1.0
        dg = np.einsum('amn,ab,br->mnr', de, etaN, e) + np.einsum('amr,ab,bn->mnr', de, etaN, e)  # d_m g_{n r}
        T = de - np.einsum('amn->anm', de)                                                        # T^a_{mn}
        v = [dg[m, a1, a2] for m in range(n) for a1 in range(n) for a2 in range(a1, n)] + \
            [T[b, m1, m2] for b in range(n) for m1 in range(n) for m2 in range(m1 + 1, n)]
        rows.append(v)
    return np.array(rows).T      # (40 + 24) x 64
for name, e in [("identity frame", np.eye(n)), ("random frame", rng.normal(size=(n, n)))]:
    J = jet_map(e)
    check(f"A. {name}: d(frame) (64) -> (d(metric) 40, torsion 24) is one-to-one (rank 64)", J.shape == (64, 64) and rank(J) == 64)
J0 = jet_map(np.eye(n))
check("A. its metric part alone has rank 40, kernel 24: the frame data the metric cannot see",
      rank(J0[:40]) == 40)
ker = np.linalg.svd(J0[:40])[2][40:].T          # kernel of d -> dg at e = I
so13 = []                                        # so(1,3): X with X^T eta + eta X = 0
for i, j in itertools.combinations(range(n), 2):
    X = np.zeros((n, n)); X[i, j] = 1; X[j, i] = -etaN[i, i] * etaN[j, j]; so13.append(X)
check("A. so(1,3) has dimension 6", all(np.allclose(X.T @ etaN + etaN @ X, 0) for X in so13) and len(so13) == 6)
lor_jets = np.array([np.einsum('ab,m->amb', X, np.eye(n)[m]).ravel() for X in so13 for m in range(n)]).T  # de = X dx^m
check("A. that kernel is exactly the local-Lorentz jets so(1,3) (x) V* = 6 x 4 = 24",
      lor_jets.shape[1] == 24 and rank(lor_jets) == 24 and rank(np.hstack([ker, lor_jets])) == 24)

# ---------------------------------------------------------------- B: Levi-Civita uniqueness
def T3(f):
    M = np.zeros((64, 64))
    for a, b, c in itertools.product(range(n), repeat=3):
        for (a2, b2, c2), w in f(a, b, c): M[idx(a2, b2, c2), idx(a, b, c)] += w
    return M
I64 = np.eye(64)
sw_low = T3(lambda a, b, c: [((a, c, b), 1.0)])     # N_abc -> N_acb (lower pair)
sw_out = T3(lambda a, b, c: [((c, b, a), 1.0)])     # N_abc -> N_cba (outer pair, metric compatibility)
SymLow, AltOut = (I64 + sw_low) / 2, (I64 - sw_out) / 2
check("B. 'symmetric in the lower pair' (40) and 'antisymmetric in the outer pair' (24) meet only in 0 and span all 64",
      rank(SymLow) == 40 and rank(AltOut) == 24 and rank(np.hstack([SymLow, AltOut])) == 64)
print("     (this is the fundamental theorem of Riemannian geometry: a torsion-free, metric-compatible connection difference is 0)")
for K in range(2, 7):
    s_low, a_out = K * K * (K + 1) // 2, K * K * (K - 1) // 2
    assert s_low + a_out == K ** 3
check("B. for every K: K^2(K+1)/2 + K^2(K-1)/2 = K^3, i.e. 40 + 24 at K = 4", True)

# ---------------------------------------------------------------- C, D, E: two frames on one metric
t, x, y, z = sp.symbols('t x y z', real=True); X4 = [t, x, y, z]
eta = sp.diag(-1, 1, 1, 1)
def weitz(E):        # Gamma^l_{m n} = E_a^l d_m E^a_n   (derivative index m first)
    Ei = E.inv()
    return sp.Array([[[sp.simplify(sum(Ei[l, a] * sp.diff(E[a, nn], X4[m]) for a in range(4))) for nn in range(4)]
                      for m in range(4)] for l in range(4)])
def rot(th, i=1, j=2):
    R = sp.eye(4); R[i, i] = R[j, j] = sp.cos(th); R[i, j] = -sp.sin(th); R[j, i] = sp.sin(th); return R
def boost(z_, i=1):
    B = sp.eye(4); B[0, 0] = B[i, i] = sp.cosh(z_); B[0, i] = B[i, 0] = sp.sinh(z_); return B
P = sp.diag(1, -1, 1, 1)   # an improper Lorentz transformation (spatial reflection, det -1)
f1, f2 = sp.Function('f1')(t, x, y, z), sp.Function('f2')(t, x, y, z)
L = rot(f1) * boost(f2)                                   # a general-enough local Lorentz field
check("C. L = R(f1) B(f2) is Lorentz at every point: L^T eta L = eta", sp.simplify(L.T * eta * L - eta) == sp.zeros(4, 4))
GW_I = weitz(sp.eye(4)); GW_L = weitz(L); GW_PL = weitz(P * L); GW_P = weitz(P)
N = sp.Array([[[sp.simplify(GW_L[l, m, nn] - GW_I[l, m, nn]) for nn in range(4)] for m in range(4)] for l in range(4)])
A = [sp.simplify(L.inv() * sp.diff(L, X4[m])) for m in range(4)]
check("C. the connection difference is N^l_{m n} = (L^-1 d_m L)^l_n", all(sp.simplify(N[l, m, nn] - A[m][l, nn]) == 0
      for l, m, nn in itertools.product(range(4), repeat=3)))
check("C. each L^-1 d_m L lies in so(1,3), so N lowered with eta is antisymmetric in its outer pair (metric compatible: the 24)",
      all(sp.simplify(A[m].T * eta + eta * A[m]) == sp.zeros(4, 4) for m in range(4)))
# D: the second root. Gram parity e^i -> -e^i, i.e. Pg = diag(1,-1,-1,-1) acting on the frame index.
Pg = sp.diag(1, -1, -1, -1)
e0 = rot(sp.Symbol('k') * z) * sp.diag(1, 1, 1, 1 + x**2)        # a nontrivial frame (twisted and curved)
def frameT(E):       # T^a_{mu nu} = d_mu e^a_nu - d_nu e^a_mu, frame index a (torsion of the frame's own connection)
    return [[[sp.simplify(sp.diff(E[a, nn], X4[m]) - sp.diff(E[a, m], X4[nn])) for nn in range(4)] for m in range(4)] for a in range(4)]
FA, FB = frameT(e0), frameT(Pg * e0)
check("D. the metric and its 40 derivatives are the same for both roots (root-blind: the Gram product)",
      all(sp.simplify(sp.diff((Pg * e0).T * eta * (Pg * e0) - e0.T * eta * e0, v)) == sp.zeros(4, 4) for v in X4))
check("D. the 24 torsion components, in frame form T^a = de^a, change with the root: T^a(Pe) = P T^a(e)",
      all(sp.simplify(FB[a][m][nn] - Pg[a, a] * FA[a][m][nn]) == 0 for a, m, nn in itertools.product(range(4), repeat=3)))
check("D. and the change is real: the spatial frame torsion of this frame is nonzero",
      any(FA[a][m][nn] != 0 for a in (1, 2, 3) for m in range(4) for nn in range(4)))
GA, GB = weitz(e0), weitz(Pg * e0)
check("D. converting the frame index back with the inverse frame (e_a^l T^a, or Gamma = e^-1 de) applies P twice and hides the "
      "sign, exactly as forming g = e^T eta e does",
      all(sp.simplify(GA[l, m, nn] - GB[l, m, nn]) == 0 for l, m, nn in itertools.product(range(4), repeat=3)))
check("D. likewise the relative-frame difference L^-1 dL is the same for L and P L (both factors carry P)",
      all(sp.simplify(GW_PL[l, m, nn] - GW_L[l, m, nn]) == 0 for l, m, nn in itertools.product(range(4), repeat=3)))
check("D. the orientation also distinguishes the roots: det(P L) = -det(L)", sp.simplify((P * L).det() + L.det()) == 0)

def torsion(G):      # T^l_{m n} = Gamma^l_{m n} - Gamma^l_{n m}
    return sp.Array([[[sp.simplify(G[l, m, nn] - G[l, nn, m]) for nn in range(4)] for m in range(4)] for l in range(4)])
def axial(E, G):     # a^mu = (1/6) eps^{mu nu rho sigma} T_{nu rho sigma}, with eps built from the frame: det(E)
    T = torsion(G); g = E.T * eta * E; gi = g.inv(); dt = E.det()
    Tl = [[[sum(g[l, q] * T[q, m, nn] for q in range(4)) for nn in range(4)] for m in range(4)] for l in range(4)]
    a_low = [sp.simplify(sum(dt * sp.LeviCivita(mu, a, b, c) * Tl[a][b][c] for a in range(4) for b in range(4) for c in range(4)) / 6)
             for mu in range(4)]
    return a_low
twist = rot(sp.Symbol('k') * z)
a1 = axial(twist, weitz(twist)); a2 = axial(P * twist, weitz(P * twist))
check("D. in coordinate form the root still shows through the orientation: the axial torsion vector (built with eps = det e) "
      "flips sign, while the coordinate-index connection does not", all(sp.simplify(u + v) == 0 for u, v in zip(a1, a2)) and any(u != 0 for u in a1)
      and all(sp.simplify(weitz(P * twist)[l, m, nn] - weitz(twist)[l, m, nn]) == 0 for l, m, nn in itertools.product(range(4), repeat=3)))

# E: the slow-motion force of the relative frame: autoparallel d2x^i/dt2 = -N^i_(00)
force = [sp.simplify(-(N[i, 0, 0] + N[i, 0, 0]) / 2) for i in range(1, 4)]
boost_rate = [sp.simplify(-A[0][i, 0]) for i in range(1, 4)]
check("E. slow force -N^i_(00) = -(L^-1 d_t L)^i_0: the time-rate of the relative boost, nothing else",
      all(sp.simplify(u - v) == 0 for u, v in zip(force, boost_rate)))
check("E. pure rotation, any profile theta(t,x,y,z): no slow-motion force",
      all(sp.simplify(weitz(rot(f1))[i, 0, 0]) == 0 for i in range(1, 4)))
check("E. pure boost with a static rapidity profile zeta(x,y,z): no slow-motion force",
      all(sp.simplify(weitz(boost(sp.Function('h')(x, y, z)))[i, 0, 0]) == 0 for i in range(1, 4)))
zt = sp.Function('zeta')(t)
check("E. boost with rapidity zeta(t) along x: slow force on x is d zeta/dt (the relative acceleration of the two time legs)",
      sp.simplify(weitz(boost(zt))[1, 0, 0] - sp.diff(zt, t)) == 0)

# ---------------------------------------------------------------- F: which torsion each relation carries
def pieces(G):
    """|vector|, |axial|, |tensor| parts of T_{l m n} (lowered with eta) at the origin, numeric"""
    T = torsion(G)
    Tn = np.array([[[float(sp.N(T[l, m, nn].subs({t: 0, x: 0, y: 0, z: 0}))) for nn in range(4)] for m in range(4)] for l in range(4)])
    Tl = np.einsum('lq,qmn->lmn', etaN, Tn)
    ax = sum(np.sign(np.linalg.det(np.eye(3)[list(p)])) * np.transpose(Tl, p) for p in itertools.permutations(range(3))) / 6
    vec_c = np.einsum('ml,lmn->n', np.linalg.inv(etaN), Tn)                     # T^l_{l n}
    vec = np.zeros((4, 4, 4))
    for l, m, nn in itertools.product(range(4), repeat=3):
        vec[l, m, nn] = (etaN[l, m] * vec_c[nn] - etaN[l, nn] * vec_c[m]) / 3
    ten = Tl - ax - vec
    return [round(float(np.abs(p).max()), 6) for p in (vec, ax, ten)]
kk, ww = 1.0, 1.0
cases = {
    "twist: rotation about z by theta = k z": rot(kk * z),
    "spin: rotation about z by theta = w t": rot(ww * t),
    "boost along x with rapidity zeta = w t": boost(ww * t),
    "boost along x with rapidity zeta = k z": boost(kk * z, 1),
}
table = {}
for name, E in cases.items():
    G = weitz(E); vxa = pieces(G)
    fx = [float(sp.N(-G[i, 0, 0].subs({t: 0, x: 0, y: 0, z: 0}))) for i in range(1, 4)]
    table[name] = (vxa, fx)
    print(f"     {name:42s} |vector| {vxa[0]:.3f} |axial| {vxa[1]:.3f} |tensor| {vxa[2]:.3f}   slow force {np.round(fx, 3)}")
check("F. twist and spin carry axial torsion and exert no slow force",
      all(table[k][0][1] > 0 and np.allclose(table[k][1], 0) for k in list(cases)[:2]))
check("F. twist and spin carry no vector torsion", all(table[k][0][0] == 0 for k in list(cases)[:2]))
check("F. a time-dependent boost carries vector torsion, no axial torsion, and pushes slow matter",
      table[list(cases)[2]][0][0] > 0 and table[list(cases)[2]][0][1] == 0 and not np.allclose(table[list(cases)[2]][1], 0))
check("F. a spatial boost gradient carries torsion but exerts no slow force",
      sum(table[list(cases)[3]][0]) > 0 and np.allclose(table[list(cases)[3]][1], 0))

# ---------------------------------------------------------------- G: which action terms see the root
# First-order tetrad 4-forms are contractions of e^a, T^a, R^ab with eta_ab and eps_abcd. Under a constant
# frame transformation L in O(1,3), eta-contractions are invariant and each eps contributes det(L).
Pn = np.diag([1.0, -1, 1, 1])
eps = np.zeros((4,) * 4)
for p in itertools.permutations(range(4)):
    eps[p] = np.linalg.det(np.eye(4)[list(p)])
check("G. eta_ab is invariant under parity (P^T eta P = eta) and eps_abcd picks up det P = -1",
      np.allclose(Pn.T @ etaN @ Pn, etaN) and np.allclose(np.einsum('abcd,ai,bj,ck,dl->ijkl', eps, Pn, Pn, Pn, Pn), -eps))
terms = {"Palatini / Einstein-Hilbert  eps_abcd e^a e^b R^cd": 1, "cosmological  eps_abcd e^a e^b e^c e^d": 1,
         "Euler  eps_abcd R^ab R^cd": 1, "Holst  e_a e_b R^ab": 0, "Nieh-Yan  T^a T_a - e_a e_b R^ab": 0,
         "Pontryagin  R_ab R^ab": 0}
for k, ne in terms.items():
    print(f"     {k:52s} {'odd: sees the root' if ne % 2 else 'even: root-blind'}")
check("G. so the root-resolving terms are exactly those with an odd number of eps: Einstein-Hilbert, cosmological, Euler",
      [k for k, ne in terms.items() if ne % 2] == list(terms)[:3])
print(f"\n{sum(ok)}/{len(ok)} checks passed")
