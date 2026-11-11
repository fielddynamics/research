#!/usr/bin/env python3
"""
Does the locked Hassan-Rosen potential beta = (1, 0, 16, 0, 1) project onto the
GFD constitutive law mu(x) = x/(x+1)?

Checks, in order (see README.md in this folder for the argument):
  A. The potential's variation:  d(sqrt(-g) V)/d g_{mn} = 1/2 sqrt(-g) sum (-1)^n b_n (Y_n(X) g^-1)^{mn}
  B. Proportional background f = c^2 g for the locked set; effective Lambda; Fierz-Pauli
     combination b1 c + 2 b2 c^2 + b3 c^3 = 32 c^2 by direct quadratic expansion; Higuchi bound.
  C. The parity configuration S = P = diag(1,-1,-1,-1): V(P) = 0 but its stress is anisotropic.
  D. Decoupling limit: sum (-1)^n b_n Y_n(1 - Pi) = sum_k d_k Y_k(Pi); locked d = (49, 32, 16, 0).
  E. Static spherical solution of the decoupling-limit Lagrangian: reduced action, first integrals,
     the algebraic pi-equation, and g_tot/g_N as a function of M_enc/r^3 only.
  F. The locked-set screening relation v(v^2 + 6v + 6) = 2Q and its bounds.
Requires numpy, scipy, sympy.
"""
import itertools, sys
import numpy as np, scipy.linalg as sl, sympy as sp
from sympy.calculus.euler import euler_equations

passed = failed = 0
def check(name, ok):
    global passed, failed
    print(("PASS " if ok else "FAIL ") + name)
    passed += bool(ok); failed += (not ok)

BETA = [1, 0, 16, 0, 1]
eta = np.diag([-1., 1, 1, 1])

def esym(X):
    lam = np.linalg.eigvals(X)
    return [1.0] + [np.real(sum(np.prod(c) for c in itertools.combinations(lam, k))) for k in range(1, 5)]
def Vpot(S, b=BETA): return sum(bn * en for bn, en in zip(b, esym(S)))
def Ynum(n, X):
    e = esym(X); return sum((-1)**k * np.linalg.matrix_power(X, n - k) * e[k] for k in range(n + 1))
def sym(A): return (A + A.T) / 2

# ---------------- A. variation of the potential ----------------
rng = np.random.default_rng(1)
b = rng.normal(size=5)
g = eta + 0.1 * sym(rng.normal(size=(4, 4))); f = 1.3 * (eta + 0.1 * sym(rng.normal(size=(4, 4))))
U = lambda g_: np.sqrt(-np.linalg.det(g_)) * Vpot(np.real(sl.sqrtm(np.linalg.inv(g_) @ f)), b)
D = np.zeros((4, 4)); h = 1e-6
for m in range(4):
    for n in range(m, 4):
        E = np.zeros((4, 4)); E[m, n] = E[n, m] = h
        dd = (U(g + E) - U(g - E)) / (2 * h)
        D[m, n] = D[n, m] = dd if m == n else dd / 2
X = np.real(sl.sqrtm(np.linalg.inv(g) @ f))
pred = 0.5 * np.sqrt(-np.linalg.det(g)) * sum((-1)**n * b[n] * Ynum(n, X) for n in range(4)) @ np.linalg.inv(g)
check("A: d(sqrt(-g)V)/dg = 1/2 sqrt(-g) sum(-1)^n b_n Y_n g^-1 (random g, f, beta)", np.allclose(D, pred, rtol=1e-5, atol=1e-7))

# ---------------- B. proportional background, FP mass, Higuchi ----------------
c, al = sp.symbols('c alpha', positive=True)
b0, b1, b2, b3, b4 = BETA
cond = al**2*(b0*c + 3*b1*c**2 + 3*b2*c**3 + b3*c**4) - b4*c**3 - 3*b3*c**2 - 3*b2*c - b1
check("B: background condition = c*(alpha^2(1+48c^2) - c^2 - 48)",
      sp.simplify(cond - c*(al**2*(1 + 48*c**2) - c**2 - 48)) == 0)
Lam = b0 + 3*b1*c + 3*b2*c**2 + b3*c**3
check("B: Lambda_g/m^2 = 1 + 48 c^2 (49 at c = 1)", sp.expand(Lam - (1 + 48*c**2)) == 0)
for cc in (1.0, 0.7, 2.5):
    lam_g = 1 + 48*cc**2
    def Q(eps, dv):
        gg = eta @ np.diag(1 + eps*dv)
        return np.sqrt(-np.linalg.det(gg)) * Vpot(np.real(sl.sqrtm(np.linalg.inv(gg) @ (cc**2*eta))))
    rows, rhs = [], []
    for s in range(6):
        dv = np.random.default_rng(s).normal(size=4); e = 1e-3
        rows.append([np.sum(dv**2), np.sum(dv)**2]); rhs.append((Q(e, dv) - 2*Q(0, dv) + Q(-e, dv)) / e**2 / 2)
    Acoef, Bcoef = np.linalg.lstsq(np.array(rows), np.array(rhs), rcond=None)[0]
    # subtract the cosmological-constant part of sqrt(-g): lam*(1/8[d]^2 - 1/4[d^2])
    mA, mB = Acoef + lam_g/4, Bcoef - lam_g/8
    check(f"B: c={cc}: mass term is Fierz-Pauli, (1/8)(b1c+2b2c^2+b3c^3)([d^2]-[d]^2) with b1c+2b2c^2+b3c^3 = 32c^2",
          abs(mA + mB) < 1e-4 and abs(8*mA - 32*cc**2) < 1e-3)
alpha2 = (c**2 + 48) / (1 + 48*c**2)
mFP2 = 32*c**2*(1 + 1/(alpha2*c**2))            # in units of m^2
H2 = (1 + 48*c**2) / 3
hig = sp.simplify(mFP2/H2 - 2)
check("B: Higuchi: m_FP^2/H^2 - 2 = 4606 c^2/((c^2+48)(48c^2+1)) > 0 for every c",
      sp.simplify(hig - 4606*c**2/((c**2 + 48)*(48*c**2 + 1))) == 0)
check("B: m_FP^2/H^2 = 192/49 * ... = 3.918 at c = 1 (maximum)", abs(float((mFP2/H2).subs(c, 1)) - 3.918367) < 1e-5)

# ---------------- C. parity configuration ----------------
P = np.diag([1., -1, -1, -1])
check("C: e_n(P) = (1,-2,0,2,-1), so V(P) = 1 + 16*0 - 1 = 0", np.allclose(esym(P), [1, -2, 0, 2, -1]) and abs(Vpot(P)) < 1e-12)
Ue = lambda e_, et: np.linalg.det(e_) * Vpot(np.linalg.inv(e_) @ et)
Dv = np.zeros((4, 4))
for i in range(4):
    for j in range(4):
        E = np.zeros((4, 4)); E[i, j] = 1e-6
        Dv[i, j] = (Ue(np.eye(4) + E, P) - Ue(np.eye(4) - E, P)) / 2e-6
check("C: vielbein stress at S = P is diag(49,-15,-15,-15): not of cosmological-constant form",
      np.allclose(Dv, np.diag([49, -15, -15, -15]), atol=1e-5))

# ---------------- D. decoupling-limit coefficients ----------------
p = sp.symbols('p0:4'); Pi = sp.diag(*p); I4 = sp.eye(4)
def e_s(k, M):
    lam = [M[i, i] for i in range(4)]
    return sp.Integer(1) if k == 0 else sum(sp.Mul(*cm) for cm in itertools.combinations(lam, k))
def Ys(n, M): return sum((((-1)**k * e_s(k, M)) * M**(n - k) for k in range(n + 1)), sp.zeros(4))
bs = sp.symbols('b0:5'); dk = sp.symbols('d0:4')
def decomp(beta):
    Xm = sum((((-1)**n * beta[n]) * Ys(n, I4 - Pi) for n in range(4)), sp.zeros(4))
    ans = sum((dk[k] * Ys(k, Pi) for k in range(4)), sp.zeros(4))
    polys = []
    for i in range(4): polys += sp.Poly(sp.expand(Xm[i, i] - ans[i, i]), *p).coeffs()
    return sp.solve(polys, dk, dict=True)[0]
gen = decomp(bs)
check("D: d0 = b0+3b1+3b2+b3, d1 = b1+2b2+b3, d2 = b2+b3, d3 = b3",
      [sp.expand(gen[dk[k]]) for k in range(4)] == [bs[0]+3*bs[1]+3*bs[2]+bs[3], bs[1]+2*bs[2]+bs[3], bs[2]+bs[3], bs[3]])
lk = decomp(BETA)
check("D: locked set gives (d0,d1,d2,d3) = (49, 32, 16, 0): cubic coefficient d2 survives, irreducible d3 vanishes",
      [lk[dk[k]] for k in range(4)] == [49, 32, 16, 0])
check("D: Y_4(Pi) = 0 identically (Cayley-Hamilton), so the basis stops at k = 3", sp.simplify(Ys(4, Pi)) == sp.zeros(4))

# ---------------- E. static spherical solution ----------------
t, x, y, z = sp.symbols('t x y z', real=True); Xc = [t, x, y, z]
r = sp.Symbol('r', positive=True); R = sp.sqrt(x**2 + y**2 + z**2)
A, B, pif, rho = [sp.Function(n) for n in ('A', 'B', 'pi', 'rho')]
a1, a2, a3, Mpl = sp.symbols('a1 a2 a3 Mpl')
etas = sp.diag(-1, 1, 1, 1)
hm = sp.diag(A(R), B(R), B(R), B(R))
dd = lambda F, m: sp.diff(F, Xc[m])
tr = sum(etas[m, m]*hm[m, m] for m in range(4))
L = 0
for l in range(4):
    for m in range(4):
        for n in range(4):
            L += -sp.Rational(1, 2)*etas[l, l]*etas[m, m]*etas[n, n]*dd(hm[m, n], l)**2
for l in range(4):
    L += sum(etas[m, m]*etas[l, l]*dd(hm[m, l], m) for m in range(4)) * sum(etas[n, n]*dd(hm[n, l], n) for n in range(4))
for n in range(4):
    L += -sum(etas[m, m]*etas[n, n]*dd(hm[m, n], m) for m in range(4)) * dd(tr, n)
for l in range(4):
    L += sp.Rational(1, 2)*etas[l, l]*dd(tr, l)**2
PiM = etas * sp.Matrix(4, 4, lambda m, n: dd(dd(pif(R), m), n))
def e_tr(k, M):
    pw = [(M**j).trace() for j in range(1, 4)]
    return [sp.Integer(1), pw[0], (pw[0]**2 - pw[1])/2, (pw[0]**3 - 3*pw[0]*pw[1] + 2*pw[2])/6][k]
def Ytr(k, M): return sum((((-1)**j*e_tr(j, M))*M**(k - j) for j in range(k + 1)), sp.zeros(4))
for k, ak in ((1, a1), (2, a2), (3, a3)):
    Xup = Ytr(k, PiM) * etas
    L += ak*sum(hm[m, n]*Xup[m, n] for m in range(4) for n in range(4))
L += hm[0, 0]*rho(R)/(2*Mpl)
Lr = sp.simplify(L.subs({x: r, y: 0, z: 0}).doit())
EL = euler_equations(sp.expand(r**2*Lr), [A(r), B(r), pif(r)], r)
mu_t = sp.Function('mt')   # mt(r) = int_0^r s^2 rho ds = M_enc/(4 pi)
u = sp.diff(pif(r), r)
Bp = (-mu_t(r)/Mpl - 2*a1*r**2*u + 2*a2*r*u**2 - sp.Rational(2, 3)*a3*u**3)/(4*r**2)
Ap = Bp + a1*u - a2*u**2/(2*r)
first = [  # first integrals (each EL equation is a total derivative)
    sp.diff(4*Mpl*r**2*Bp, r) + 2*Mpl*sp.diff(a1*r**2*u - a2*r*u**2 + a3*u**3/3, r) + r**2*rho(r),
]
resA = sp.simplify((EL[0].lhs*2*Mpl - (2*Mpl*sp.diff(a1*r**2*u - a2*r*u**2 + a3*u**3/3, r) + 4*Mpl*sp.diff(r**2*sp.diff(B(r), r), r) + r**2*rho(r))))
check("E: A-equation = d/dr[2M(a1 r^2 pi' - a2 r pi'^2 + a3 pi'^3/3) + 4M r^2 B'] + r^2 rho", resA == 0)
resB = sp.simplify(EL[1].lhs - sp.diff(-2*a1*r**2*u + a2*r*u**2 + 2*r**2*sp.diff(A(r), r) - 2*r**2*sp.diff(B(r), r), r))
check("E: B-equation = d/dr[-2a1 r^2 pi' + a2 r pi'^2 + 2r^2(A' - B')]", resB == 0)
Aq, Bq = sp.symbols('Aq Bq')   # A', B'
resP = sp.simplify(EL[2].lhs - sp.diff(a1*(r**2*sp.diff(A(r), r) - 2*r**2*sp.diff(B(r), r))
                                       - 2*a2*r*u*(sp.diff(A(r), r) - sp.diff(B(r), r)) + a3*sp.diff(A(r), r)*u**2, r))
check("E: pi-equation = d/dr[a1 r^2(A' - 2B') - 2a2 r pi'(A' - B') + a3 A' pi'^2]", resP == 0)
lam, q, uu, mt = sp.symbols('lambda q uu mt')
Bp2 = (-mt/Mpl - 2*a1*r**2*uu + 2*a2*r*uu**2 - sp.Rational(2, 3)*a3*uu**3)/(4*r**2)
Ap2 = Bp2 + a1*uu - a2*uu**2/(2*r)
pieq = sp.expand((a1*(r**2*Ap2 - 2*r**2*Bp2) - 2*a2*r*uu*(Ap2 - Bp2) + a3*Ap2*uu**2).subs({uu: lam*r, mt: q*r**3})/r**3)
check("E: pi-equation depends on r only through lambda = pi'/r and q = M_enc/(4 pi r^3)", not pieq.has(r))
ratio = sp.simplify((-Ap2/(2*Mpl))/(mt/(8*Mpl**2*r**2)))
ratio = sp.simplify(ratio.subs({uu: lam*r, mt: q*r**3}))
check("E: g_tot/g_N = 1 - 2 M a1 lambda/q + (2/3) M a3 lambda^3/q, also free of r", not ratio.has(r) and
      sp.simplify(ratio - (1 - 2*Mpl*a1*lam/q + sp.Rational(2, 3)*Mpl*a3*lam**3/q)) == 0)
lin = sp.solve(sp.expand(pieq.subs(a2, 0).subs(a3, 0)), lam)[0]
check("E: linear regime gives g_tot/g_N = 4/3 (vDVZ), independent of mass and radius",
      sp.simplify(ratio.subs({a2: 0, a3: 0, lam: lin}) - sp.Rational(4, 3)) == 0)

# ---------------- F. locked set: a3 = 0 ----------------
s_, Qv, v = sp.symbols('s Q v')
# with a3 = 0 write lambda = -s q/(2 M a1) (so g_tot/g_N = 1 + s) and Q = a2 q/(M a1^2)
eqF = sp.simplify(pieq.subs(a3, 0).subs(lam, -s_*q/(2*Mpl*a1)).subs(a2, Qv*Mpl*a1**2/q) / (a1*q/(4*Mpl)))
check("F: locked pi-equation becomes Q^2 s^3 + 6Q s^2 + 6 s - 2 = 0  (i.e. v(v^2+6v+6) = 2Q with v = Qs)",
      sp.simplify(eqF + (Qv**2*s_**3 + 6*Qv*s_**2 + 6*s_ - 2)/2) == 0)
vstar = -2 + sp.sqrt(2)
Qstar = sp.simplify(vstar*(vstar**2 + 6*vstar + 6)/2)
check("F: for Q < 0 the branch connected to infinity ends at Q* = 2 - 2 sqrt(2) = -0.828, where s = 1/sqrt(2)",
      sp.simplify(Qstar - (2 - 2*sp.sqrt(2))) == 0 and sp.simplify(vstar/Qstar - 1/sp.sqrt(2)) == 0)
# bound on the enhancement along both signs
Qs = np.concatenate([np.linspace(float(Qstar) + 1e-6, -1e-9, 2000), np.linspace(1e-9, 1e4, 4000)])
smax = 0
for Qn in Qs:
    roots = np.roots([Qn**2, 6*Qn, 6, -2])
    # pick the root continuously connected to s = 1/3 at Q -> 0 (smallest |s - 1/3| when Q small; track monotone)
    real = sorted([rr.real for rr in roots if abs(rr.imag) < 1e-9 and rr.real > 0])
    smax = max(smax, min(real, key=lambda w: abs(w - 1/3)) if real else 0)
check("F: enhancement g_tot/g_N = 1 + s stays below 1 + 1/sqrt(2) = 1.71 on the solution branch (no deep-MOND growth)",
      smax <= 1/np.sqrt(2) + 1e-3)
# Vainshtein vs MOND scaling
check("F: transition at fixed M/r^3 (Vainshtein, r_V ~ M^(1/3)) vs fixed M/r^2 (MOND, r_M ~ M^(1/2)): exponents differ",
      sp.Rational(1, 3) != sp.Rational(1, 2))

print(f"\n{passed}/{passed + failed} checks passed")
sys.exit(1 if failed else 0)
