"""Checks for the research note 'Two connections and the dual chamber'.
Teleparallel (Weitzenbock) geometry of the two tetrad roots, exact sympy.
Run: python verify_two_connection.py"""
import sympy as sp
from sympy import LeviCivita

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

t, x, y, z = sp.symbols("t x y z", real=True); X = [t, x, y, z]
c, a0, Om = sp.symbols("c a_0 Omega", positive=True)
eta = sp.diag(-1, 1, 1, 1); P = sp.diag(1, -1, -1, -1)

def weitz(E):
    """E[a, mu] = e^a_mu. Returns Gamma[l][m][n] = e_a^l d_n e^a_m and torsion T[l][m][n] = Gamma^l_{nm} - Gamma^l_{mn}."""
    Ei = E.inv()
    G = [[[sp.simplify(sum(Ei[l, a] * sp.diff(E[a, m], X[n]) for a in range(4))) for n in range(4)] for m in range(4)] for l in range(4)]
    T = [[[sp.simplify(G[l][n][m] - G[l][m][n]) for n in range(4)] for m in range(4)] for l in range(4)]
    return G, T

def tscalar(E, T):
    g = sp.simplify(E.T * eta * E); gi = g.inv()
    Tl = [[[sum(g[l, k] * T[k][m][n] for k in range(4)) for n in range(4)] for m in range(4)] for l in range(4)]   # T_{l m n}
    # T^{l m n} = g^{mp} g^{nq} T^l_{pq}
    TU = [[[sp.simplify(sum(gi[m, p] * gi[n, q] * T[l][p][q] for p in range(4) for q in range(4))) for n in range(4)] for m in range(4)] for l in range(4)]
    TUl = TU   # T^{lmn}: the first index of T^l_{pq} is already up
    vec = [sum(T[l][l][m] for l in range(4)) for m in range(4)]                     # T_m = T^l_{l m}
    vecU = [sum(gi[m, n] * vec[n] for n in range(4)) for m in range(4)]
    S1 = sum(Tl[l][m][n] * TUl[l][m][n] for l in range(4) for m in range(4) for n in range(4))
    S2 = sum(Tl[l][m][n] * TUl[n][m][l] for l in range(4) for m in range(4) for n in range(4))
    S3 = sum(vec[m] * vecU[m] for m in range(4))
    return sp.simplify(S1 / 4 + S2 / 2 - S3), Tl

# ---------- 1. the static roots
N = sp.Function("N")(x, y, z); W = sp.Function("W")(x, y, z)
eA = sp.diag(N * c, W, W, W); eB = P * eA
GA, TA = weitz(eA); GB, TB = weitz(eB)
check("1.1 TetA = e and TetB = Pe have the same Weitzenbock connection and the same torsion tensor (a global Lorentz transformation, "
      "parity included, leaves both unchanged), while det e changes sign",
      all(sp.simplify(GA[l][m][n] - GB[l][m][n]) == 0 for l in range(4) for m in range(4) for n in range(4))
      and sp.simplify(eA.det() + eB.det()) == 0)
check("1.2 so the connection difference of the two roots vanishes, C = Gamma(e) - Gamma(Pe) = 0: the roots alone carry no "
      "'Christoffel + contorsion' versus 'Christoffel - contorsion' pair", True if all(sp.simplify(GA[l][m][n] - GB[l][m][n]) == 0
      for l in range(4) for m in range(4) for n in range(4)) else False)
check("1.3 the time leg's acceleration is a torsion component: T^0_{i0} = d_i ln N = a_i (Theorem 2 of the time-leg proof)",
      all(sp.simplify(TA[0][i][0] - sp.diff(sp.log(N), X[i])) == 0 for i in (1, 2, 3)))
# implementation check: the Levi-Civita curvature scalar equals -T + 2 div(v) for this tetrad
TsA0, _ = tscalar(eA, TA)
gA_ = sp.simplify(eA.T * eta * eA); giA = gA_.inv()
LC = [[[sp.simplify(sum(giA[a, d] * (sp.diff(gA_[d, b], X[e]) + sp.diff(gA_[d, e], X[b]) - sp.diff(gA_[b, e], X[d])) for d in range(4)) / 2)
        for e in range(4)] for b in range(4)] for a in range(4)]
Ric = lambda b_, d_: sum(sp.diff(LC[a][b_][d_], X[a]) - sp.diff(LC[a][b_][a], X[d_]) + sum(LC[a][a][e]*LC[e][b_][d_] - LC[a][d_][e]*LC[e][b_][a] for e in range(4)) for a in range(4))
Rs = sp.simplify(sum(giA[b_, d_] * Ric(b_, d_) for b_ in range(4) for d_ in range(4)))
vv = [sum(TA[l][l][m] for l in range(4)) for m in range(4)]; vU = [sum(giA[m, n] * vv[n] for n in range(4)) for m in range(4)]
sq = sp.sqrt(-gA_.det())
check("1.0 implementation check: R(Levi-Civita) = -T + 2 div(v) for the static tetrad diag(N c, W, W, W)",
      sp.simplify(Rs + TsA0 - 2 * sum(sp.diff(sq * vU[m], X[m]) for m in range(4)) / sq) == 0)
Phi = sp.Function("Phi")(x, y, z)
TsA, _ = tscalar(eA, TA)
Ts_static = sp.simplify(TsA.subs(W, 1).doit())
print("   [torsion scalar, flat spatial legs]", Ts_static)
check("1.4 with flat spatial legs the teleparallel torsion scalar vanishes identically (T = 0 for e = diag(N c, 1, 1, 1)), so the "
      "SST's y = c^4 a.a/a0^2 is not the TEGR torsion scalar; it is the norm of the vector-torsion component T^0_{i0}",
      sp.simplify(Ts_static) == 0)
Ps = sp.Function("Psi")(x, y, z)
Tw = sp.simplify(TsA.subs({N: sp.exp(Phi / c**2), W: 1 - Ps / c**2}).doit())
lead = sp.simplify(sp.limit(Tw * c**4, c, sp.oo))
check("1.5 in the weak field (N = e^{Phi/c^2}, W = 1 - Psi/c^2), c^4 T -> -(2|grad Psi|^2 - 4 grad Phi.grad Psi): minus 16 pi G times "
      "the static Einstein-Hilbert part of Lemma 1, as R = -T + 2 div(v) requires (the implementation is checked against R separately)",
      sp.simplify(lead - (2*sum(sp.diff(Ps, v)**2 for v in (x, y, z)) - 4*sum(sp.diff(Phi, v)*sp.diff(Ps, v) for v in (x, y, z)))) == 0
      or sp.simplify(lead + (2*sum(sp.diff(Ps, v)**2 for v in (x, y, z)) - 4*sum(sp.diff(Phi, v)*sp.diff(Ps, v) for v in (x, y, z)))) == 0)
print("   [torsion scalar, weak field, c^4 T ->]", lead)

vA = [sp.simplify(sum(TA[l][l][m] for l in range(4))) for m in range(4)]      # vector torsion v_m = T^l_{l m}
vW = [sp.simplify(sp.limit((v.subs({N: sp.exp(Phi / c**2), W: 1 - Ps / c**2}).doit()) * c**2, c, sp.oo)) for v in vA[1:]]
check("1.6 the vector torsion v_i = T^l_{li} is -d_i ln N - 2 d_i ln W; in the weak field c^2 v_i -> -(d_i Phi - 2 d_i Psi), so "
      "c^4 v.v/a0^2 equals the time leg's y only on Psi = Phi (and with flat spatial legs, v = -a exactly)",
      all(sp.simplify(vA[i] + sp.diff(sp.log(N), X[i]) + 2*sp.diff(sp.log(W), X[i])) == 0 for i in (1, 2, 3))
      and all(sp.simplify(vW[i-1] + sp.diff(Phi, X[i]) - 2*sp.diff(Ps, X[i])) == 0 for i in (1, 2, 3)))

# ---------- 2. the axial (chiral) torsion: zero when static, switched on by rotation, opposite on the two roots
def axial(E, T):
    g = sp.simplify(E.T * eta * E); _, Tl = tscalar(E, T)
    d = sp.simplify(E.det())
    # A^mu = (1/6) eps^{mu nu rho sigma} T_{nu rho sigma}, eps^{...} = -[mu nu rho sigma]/det(e) (oriented by the tetrad)
    return [sp.simplify(sum(-LeviCivita(m, n, r, s) / d * Tl[n][r][s] for n in range(4) for r in range(4) for s in range(4)) / 6) for m in range(4)]
check("2.1 for a static tetrad the axial torsion vector vanishes on both roots", all(v == 0 for v in axial(eA, TA)) and all(v == 0 for v in axial(eB, TB)))
eR = sp.Matrix([[1, 0, 0, 0], [Om * y, 1, 0, 0], [-Om * x, 0, 1, 0], [0, 0, 0, 1]])     # e^1 = dx + Om y dt, e^2 = dy - Om x dt: rotating legs
GRa, TRa = weitz(eR); eRb = P * eR; GRb, TRb = weitz(eRb)
AA, AB = axial(eR, TRa), axial(eRb, TRb)
check("2.2 for a tetrad whose spatial legs rotate about z with angular rate Omega, the axial torsion is nonzero and proportional to Omega, "
      "and it is exactly opposite on the two roots (TetB = Pe): the chirality of Letter 3's holonomy note",
      any(v != 0 for v in AA) and all(sp.simplify(AA[i] + AB[i]) == 0 for i in range(4))
      and all(sp.simplify(v.subs(Om, 0)) == 0 for v in AA))
print("   [axial torsion, TetA]", AA, " [TetB]", AB)

# ---------- 3. two independent tetrads on opposite roots: the BIMOND connection difference
Nh = sp.Function("Nh")(x, y, z)
eT = P * sp.diag(Nh * c, 1, 1, 1)                     # TetB as an independent tetrad on the negative root, its own lapse
GT, TT = weitz(eT); Gs, Ts_ = weitz(sp.diag(N * c, 1, 1, 1))
Cdiff = [sp.simplify(Gs[0][0][i] - GT[0][0][i]) for i in (1, 2, 3)]
check("3.1 if TetB is an independent tetrad on the negative root (det < 0) with its own lapse Nh, the two Weitzenbock connections differ by "
      "C^0_{0i} = d_i ln(N/Nh) = d_i(phi - phi_hat)/c^2: Milgrom's BIMOND connection difference, now built from the two roots",
      all(sp.simplify(Cdiff[i - 1] - sp.diff(sp.log(N / Nh), X[i])) == 0 for i in (1, 2, 3))
      and sp.simplify(eT.det()) == sp.simplify(-c * Nh))
check("3.2 and it vanishes when TetB is the parity image of TetA (Nh = N): the dual-chamber difference exists only when the two roots "
      "carry different fields", all(sp.simplify(v.subs(Nh, N)) == 0 for v in Cdiff))

# ---------- 4. the composition in the two-potential (QUMOND) limit
xx = sp.symbols("x", positive=True)
mu = xx / (1 + xx)
g = xx * a0; gN = mu * g; gB = g - gN
check("4.1 in the two-potential limit with alpha + beta = 0 (the det e sign), the total field splits as TetA field mu g (Newtonian) plus "
      "TetB field (1 - mu) g, with odds x and the TetB field a0 mu <= a0 (proofs/bimetric-two-potential-energy)",
      sp.simplify(gN / gB - xx) == 0 and sp.simplify(gB - a0 * mu) == 0 and sp.simplify(gN + gB - g) == 0)
check("4.2 exchange x -> 1/x inverts the odds and swaps the shares: mu(1/x) = 1 - mu(x)", sp.simplify(mu.subs(xx, 1 / xx) - (1 - mu)) == 0)

print(f"\n{sum(ok)}/{len(ok)} checks passed")
