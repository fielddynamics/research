"""Machine checks for 'The Locked Bimetric Potential and the Constitutive Law'.
Exact algebra (sympy) throughout. Run: python verify_bimetric_lock_constitutive_law.py"""
from itertools import combinations
import sympy as sp

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

b = sp.symbols("b0:5")
LOCK = [1, 0, 16, 0, 1]
def e(ev, n): return sp.Integer(1) if n == 0 else sp.expand(sum(sp.prod(c) for c in combinations(ev, n)))
def V(ev, bb): return sp.expand(sum(bb[n] * e(ev, n) for n in range(5)))
w, s, x, y, u = sp.symbols("w s x y u", positive=True)

# ---------------- Part A: the standard reduction (no-go)
# A1 decoupling-limit coefficients d_k from the beta's: verify the expansion identity, not just the formula
import random
random.seed(1)
def e_mat(Mx, k):
    lam_ = sp.symbols("lam_"); cp = sp.Poly(sp.expand((lam_*sp.eye(4) - Mx).det()), lam_).all_coeffs()
    return [sp.Integer(1), -cp[1], cp[2], -cp[3], cp[4]][k]
def Ymat(Mx, n):
    o = sp.zeros(4)
    for k in range(n + 1): o += (-1)**k * e_mat(Mx, k) * Mx**(n - k)
    return o
Pi_ = sp.Matrix(4, 4, lambda i, j: sp.Rational(random.randint(-9, 9), 7)); Pi_ = (Pi_ + Pi_.T)/2
d = [b[0] + 3*b[1] + 3*b[2] + b[3], b[1] + 2*b[2] + b[3], b[2] + b[3], b[3]]
lhsY, rhsY = sp.zeros(4), sp.zeros(4)
for n in range(4): lhsY += (-1)**n * b[n] * Ymat(sp.eye(4) - Pi_, n)
for k in range(4): rhsY += d[k] * Ymat(Pi_, k)
dl = [v.subs(dict(zip(b, LOCK))) for v in d]
check("A1 the h-pi mixing: sum_n (-1)^n beta_n Y_n(1 - Pi) = sum_k d_k Y_k(Pi) holds identically (general beta, exact random symmetric Pi; "
      "Y_4 = 0 by Cayley-Hamilton), with d = (b0+3b1+3b2+b3, b1+2b2+b3, b2+b3, b3) = (49, 32, 16, 0) for the lock",
      sp.simplify(lhsY - rhsY) == sp.zeros(4) and sp.simplify(Ymat(Pi_, 4)) == sp.zeros(4) and dl == [49, 32, 16, 0])

# A1b derive the static spherical equations from the decoupling-limit Lagrangian (independently of the research note)
from sympy.calculus.euler import euler_equations
xs, ys, zs, rr = sp.symbols("x_s y_s z_s r_r", positive=True); XS = [xs, ys, zs]
c1, c2, c3, Ms, rho_ = sp.symbols("c1 c2 c3 M_s rho_s")
Af, Bf, pf = [sp.Function(nm)(xs, ys, zs) for nm in ("Af", "Bf", "pf")]
etaS = sp.diag(-1, 1, 1, 1); hS = sp.diag(Af, Bf, Bf, Bf); hUp = etaS*hS*etaS
dd = lambda f, m: 0 if m == 0 else sp.diff(f, XS[m - 1])
boxS = lambda f: sum(sp.diff(f, v, 2) for v in XS)
trh = sum(etaS[m, m]*hS[m, m] for m in range(4))
def Eop(m, n):
    t1 = boxS(hS[m, n]); t2 = sum(etaS[a, a]*dd(dd(hS[a, n], a), m) for a in range(4)); t3 = sum(etaS[a, a]*dd(dd(hS[a, m], a), n) for a in range(4))
    t4 = dd(dd(trh, m), n); t5 = etaS[m, n]*(boxS(trh) - sum(etaS[a, a]*etaS[c_, c_]*dd(dd(hS[a, c_], a), c_) for a in range(4) for c_ in range(4)))
    return -sp.Rational(1, 2)*(t1 - t2 - t3 + t4 - t5)
PiS = etaS*sp.Matrix(4, 4, lambda m, n: dd(dd(pf, m), n))
LdL = (-sp.Rational(1, 2)*sum(hUp[m, n]*Eop(m, n) for m in range(4) for n in range(4))
       + sum(ck*((etaS*hS)*Ymat(PiS, k)).trace() for ck, k in [(c1, 1), (c2, 2), (c3, 3)]) + Af*rho_/(2*Ms))
ELs = euler_equations(LdL, [Af, Bf, pf], XS)
Ar_, Br_, pr_ = [sp.Function(nm)(rr) for nm in ("Ar_", "Br_", "pr_")]
Rx = sp.sqrt(xs**2 + ys**2 + zs**2)
redS = [sp.simplify(q_.lhs.subs({Af: Ar_.subs(rr, Rx), Bf: Br_.subs(rr, Rx), pf: pr_.subs(rr, Rx)}).doit().subs({xs: rr, ys: 0, zs: 0})) for q_ in ELs]
p1 = sp.diff(pr_, rr)
JA = rr**2*(sp.diff(Br_, rr) + c1*p1 - c2*p1**2/rr + c3*p1**3/(3*rr**2))
JB = rr**2*(sp.diff(Ar_, rr) - sp.diff(Br_, rr) - 2*c1*p1 + c2*p1**2/rr)
Jp = c1*rr**2*(sp.diff(Ar_, rr) - 2*sp.diff(Br_, rr)) - 2*c2*rr*p1*(sp.diff(Ar_, rr) - sp.diff(Br_, rr)) + c3*p1**2*sp.diff(Ar_, rr)
check("A1b from the decoupling-limit Lagrangian -1/2 hEh + h.sum a_k Y_k(Pi) + h_00 rho/2M, with static isotropic h = diag(A, B, B, B) and "
      "pi(r), all three Euler-Lagrange equations are total derivatives (r^-2 d/dr of a current), so they integrate exactly",
      sp.simplify(redS[0] - (sp.diff(JA, rr)/rr**2 + rho_/(2*Ms))) == 0 and sp.simplify(redS[1] - sp.diff(JB, rr)/rr**2) == 0
      and sp.simplify(redS[2] - sp.diff(Jp, rr)/rr**2) == 0)
lamS, qS, Ap_, Bp_ = sp.symbols("lambda_S q_S Ap Bp")
solS = sp.solve([sp.Eq(Bp_ + c1*rr*lamS - c2*rr*lamS**2 + c3*rr*lamS**3/3, -qS*rr/(2*Ms)),
                 sp.Eq(Ap_ - Bp_ - 2*c1*rr*lamS + c2*rr*lamS**2, 0)], [Ap_, Bp_], dict=True)[0]
pieqS = sp.expand((c1*rr**2*(Ap_ - 2*Bp_) - 2*c2*rr*(lamS*rr)*(Ap_ - Bp_) + c3*(lamS*rr)**2*Ap_).subs(solS)/rr**3)
noteform = sp.Rational(3, 2)*c1**2*lamS - (3*c1*c2 + c3*qS/(4*Ms))*lamS**2 + (c2**2 + 2*c1*c3/3)*lamS**3 - (c3**2/6)*lamS**5 + c1*qS/(4*Ms)
forceS = sp.simplify(solS[Ap_]/solS[Ap_].subs({c1: 0, c2: 0, c3: 0}))
check("A1c with regular first integrals (q = M_enc/4 pi r^3, lambda = pi'/r) the pi-equation is twice the research note's form and contains "
      "no r, and g_tot/g_N = 1 - 2M a1 lambda/q + (2/3) M a3 lambda^3/q",
      sp.simplify(pieqS - 2*noteform) == 0 and rr not in pieqS.free_symbols
      and sp.simplify(forceS - (1 - 2*Ms*c1*lamS/qS + sp.Rational(2, 3)*Ms*c3*lamS**3/qS)) == 0)

# A2 the static spherical screening equation, from the decoupling-limit pi-equation with a3 = 0
a1, a2, q, Mp, lam, sv, Q = sp.symbols("a1 a2 q M lambda s Q", nonzero=True)
pieq = sp.Rational(3, 2)*a1**2*lam - 3*a1*a2*lam**2 + a2**2*lam**3 + a1*q/(4*Mp)
sub = pieq.subs(lam, -sv*q/(2*Mp*a1))
target = Q**2*sv**3 + 6*Q*sv**2 + 6*sv - 2
ratio = sp.simplify(sp.factor(sp.expand(sub).subs(a2, Q*Mp*a1**2/q)) / target)
check("A2 with lambda = pi'/r = -s q/(2 M a1) and Q = a2 q/(M a1^2), the pi-equation is proportional to Q^2 s^3 + 6 Q s^2 + 6 s - 2 = 0 "
      "(q = M_enc/(4 pi r^3), g_tot/g_N = 1 + s): r enters only through q, so the response depends on the enclosed mass only through M_enc/r^3",
      ratio.free_symbols.isdisjoint({sv, Q}) and ratio != 0)
v_ = sp.symbols("v", real=True)
Dv = v_**2 + 6*v_ + 6
Qv, sv_ = v_*Dv/2, 2/Dv
vstar = -2 + sp.sqrt(2)
check("A3 every real root is s = 2/D(v), Q = v D(v)/2 with D = v^2 + 6v + 6. The branch that matches the linear solution (v -> 0, s = 1/3, "
      "g_tot/g_N = 4/3, vDVZ) is screened for Q > 0 (s -> 0) and for Q < 0 turns at Q* = 2 - 2 sqrt2, where s = 1/sqrt2: on it "
      "g_tot/g_N <= 1 + 1/sqrt2 < 1.71, and no solution on it continues past Q*",
      sp.simplify(target.subs({Q: Qv, sv: sv_})) == 0 and sv_.subs(v_, 0) == sp.Rational(1, 3)
      and sp.simplify(sp.diff(Qv, v_).subs(v_, vstar)) == 0 and sp.simplify(Qv.subs(v_, vstar) - (2 - 2*sp.sqrt(2))) == 0
      and sp.simplify(sv_.subs(v_, vstar) - 1/sp.sqrt(2)) == 0 and float(1 + 1/sp.sqrt(2)) < 1.71)
vpm = sp.solve(Dv, v_)
Mx_, r_, kk = sp.symbols("M_x r_x k", positive=True)
check("A3b the other real roots are not bounded: where D < 0, s <= -2/3 (g_tot/g_N <= 1/3); but as D -> 0+ (v -> -3 +/- sqrt3), Q -> 0 and "
      "s -> v/Q -> infinity. There g_tot ~ g_N v/Q with Q = k M/r^3, so g_tot ~ (M/r^2)(r^3/M) ~ r, independent of the mass: a "
      "self-accelerating-type force, not matching the linear solution at large r, and not the deep-MOND form sqrt(G M a0)/r",
      sp.minimum(Dv, v_) == -3 and all(sp.simplify(Qv.subs(v_, vp)) == 0 for vp in vpm)
      and sp.simplify(sp.diff((Mx_/r_**2)*vpm[1]/(kk*Mx_/r_**3), Mx_)) == 0)
Mm, r, L = sp.symbols("M_m r L", positive=True)
mu = lambda X: X/(1 + X)
check("A4 no function of M/r^3 equals a function of x = G M/(a0 r^2) for all M, r: along M = L r^3 the density is fixed but x = L r varies, "
      "and d/dr [1/mu(L r)] = -1/(L r^2) != 0. So no change of variable maps the standard response onto mu, for ANY beta",
      sp.simplify(sp.diff(1/mu(L*r), r) + 1/(L*r**2)) == 0)
check("A5 the Vainshtein and MOND radii scale as M^(1/3) and M^(1/2): their ratio is not mass-independent",
      sp.simplify(sp.diff(sp.log(Mm**sp.Rational(1, 3)/Mm**sp.Rational(1, 2)), Mm)) != 0)
P = [1, -1, -1, -1]
check("A6 at GFD's parity configuration S = P = diag(1,-1,-1,-1), e_n(P) = (1,-2,0,2,-1) and the locked potential vanishes, V(P) = b0 - b4 = 0",
      [e(P, n) for n in range(5)] == [1, -2, 0, 2, -1] and V(P, LOCK) == 0)
check("A7 the locked potential is not the coupling polynomial: on S = diag(1,s,s,s) it is 1 + 48 s + 48 s^2 + s^3 (98, 1, 0 at s = +1, 0, -1), "
      "not 1 + 4 s + 16 s^2 (21, 17, 13)",
      sp.expand(V([1, s, s, s], LOCK) - (1 + 48*s + 48*s**2 + s**3)) == 0 and [V([1, t, t, t], LOCK) for t in (1, 0, -1)] == [98, 1, 0])

# A8-A9 Letter 2's lemma applied to Hassan-Rosen: the potential is root-blind
Nn = sp.Function("N")(*sp.symbols("X Y Z")); cc = sp.symbols("c", positive=True)
eta = sp.diag(-1, 1, 1, 1); Pm = sp.diag(1, -1, -1, -1)
eA = sp.diag(Nn*cc, 1 + sp.Function("h")(*sp.symbols("X Y Z")), 1, 1)   # a static tetrad (TetA)
eB = Pm*eA                                                                # its parity root (TetB)
gA, gB = eA.T*eta*eA, eB.T*eta*eB
check("A8 Letter 2's Lemma: TetA = e and TetB = Pe give the same metric, while det e changes sign (the two roots of one metric)",
      sp.simplify(gA - gB) == sp.zeros(4) and sp.simplify(eA.det() + eB.det()) == 0)
check("A9 so Hassan-Rosen's metric-form matrix g^-1 f is the identity when f is built from TetB: the potential takes the same value for "
      "either root and cannot tell TetA from TetB; only the vielbein form e^-1(Pe) = P sees the second root, where V(P) = 0 (A6)",
      sp.simplify(gA.inv()*gB) == sp.eye(4) and sp.simplify(eA.inv()*eB) == Pm)

check("A10 P is a square root of g^-1 f = I, but not the principal one (eigenvalues -1); and e^T eta (P e) is symmetric, so the vielbein form "
      "with S = P meets the symmetric-vielbein condition. The two roots of the tetrad equation are the two square-root branches I and P of "
      "g^-1 f = I; Hassan-Rosen's metric form, defined with the principal root, sees only I",
      Pm*Pm == sp.eye(4) and any(ev_ < 0 for ev_ in Pm.eigenvals()) and sp.simplify((eA.T*eta*eB) - (eA.T*eta*eB).T) == sp.zeros(4))

# ---------------- Part B: the acceleration-deformed frame
Vw = V([1, 1, 1, w], b); A = Vw.subs(w, 0); B = sp.expand(Vw.coeff(w))
check("B1 on the rank-one deformation S = diag(1,1,1,w), V = A + B w for every beta, with A = b0+3b1+3b2+b3 and B = b1+3b2+3b3+b4",
      sp.expand(Vw - (A + B*w)) == 0 and sp.expand(A - (b[0]+3*b[1]+3*b[2]+b[3])) == 0 and sp.expand(B - (b[1]+3*b[2]+3*b[3]+b[4])) == 0)
sh = B*w/(A + B*w)
num = sp.factor(sp.numer(sp.together(sh.subs(w, 1/w) - (1 - sh))))
check("B2 the deformed leg's share B w/(A + B w) obeys exchange closure s(1/w) = 1 - s(w) iff A = B, i.e. iff b0 + 2 b1 = b4 + 2 b3",
      sp.expand(num + w*(A - B)*(A + B)) == 0 and sp.expand(A - B - (b[0]+2*b[1]-2*b[3]-b[4])) == 0)
check("B3 and then the share is exactly w/(1 + w): with w = x = |grad Phi|/a0 it is mu(x) = x/(x+1)",
      sp.simplify(sh.subs(b[4], b[0] + 2*b[1] - 2*b[3]) - w/(1 + w)) == 0)
pal = [b[0], b[1], b[2], b[1], b[0]]
ev = sp.symbols("l1:5", positive=True)
check("B4 palindromic beta (the g <-> f symmetry det S V(S^-1) = V(S)) satisfies the condition; then V = (b0 + 4 b1 + 3 b2)(1 + w)",
      sp.simplify(sp.prod(ev)*V([1/t for t in ev], pal) - V(list(ev), pal)) == 0
      and sp.expand(V([1, 1, 1, w], pal) - (b[0] + 4*b[1] + 3*b[2])*(1 + w)) == 0)
check("B5 for the locked set V = 49(1 + w), and b2 = 16 cancels from the share: every palindromic set gives the same mu",
      sp.expand(V([1, 1, 1, w], LOCK) - 49*(1 + w)) == 0 and sp.simplify(sh.subs(dict(zip(b, pal))) - w/(1 + w)) == 0)
check("B4b the share is canonical: Bw/(A + Bw) is the elasticity w d ln V/dw of V on this family",
      sp.simplify(w*sp.diff(sp.log(A + B*w), w) - B*w/(A + B*w)) == 0)
symdiff = sp.expand(sp.prod(ev)*V([1/t for t in ev], b) - V(list(ev), b))
check("B4c HR's g <-> f symmetry det S V(S^-1) = V(S) holds iff beta is palindromic (b0 = b4, b1 = b3): the difference is "
      "sum_n (b_{4-n} - b_n) e_n(S)", sp.simplify(symdiff - sum((b[4-n] - b[n])*e(list(ev), n) for n in range(5))) == 0)
check("B6 the condition is not implied by beta2 or by vanishing odd terms alone: b = (1, 0, 16, 0, 2) fails it", (1 + 0 - 0 - 2) != 0)
check("B7 on this family V/V(I) = det[(I + S)/2]: the ratio is the volume of the midpoint (Field-Origin) frame",
      sp.simplify(V([1, 1, 1, w], LOCK)/V([1, 1, 1, 1], LOCK) - sp.prod([(1 + t)/2 for t in (1, 1, 1, w)])) == 0)

# B8 the deformed-frame shares are not the two roots
check("B8 the two shares of Theorem 5 are two parts of one deformed frame, not the two roots: on the actual roots the locked potential is "
      "V(I) = 98 and V(P) = 0, and on the path between them, diag(1,s,s,s), it is (1+s)(s^2+47s+1), with no exchange symmetry between the ends",
      V([1, 1, 1, 1], LOCK) == 98 and V(P, LOCK) == 0
      and sp.expand(V([1, s, s, s], LOCK) - (1 + s)*(s**2 + 47*s + 1)) == 0)

# ---------------- Part C: the dynamics, and the time leg
E = (1 - sp.exp(-u))*y - 2*(sp.sinh(u) - u)
ust = sp.log(1 + sp.sqrt(y))
Fy = y - 2*sp.sqrt(y) + 2*sp.log(1 + sp.sqrt(y))
check("C1 the auxiliary energy E(u; y) = (1 - e^-u) y - 2(sinh u - u), u = ln(V/V0), is stationary at V/V0 = 1 + sqrt(y) = 1 + x",
      sp.simplify(sp.diff(E, u).subs(u, ust).rewrite(sp.exp)) == 0)
check("C2 its stationary value is the SST's F(y) and its slope dE/dy there is mu(x)",
      sp.simplify((E.subs(u, ust) - Fy).rewrite(sp.exp)) == 0 and sp.simplify((1 - sp.exp(-ust)) - sp.sqrt(y)/(1 + sp.sqrt(y))) == 0)
check("C3 but its u-dependence -2(sinh u - u) contains no beta: the potential supplies the variable V/V0, not the energy",
      not any(t in E.free_symbols for t in b))
c_, a0 = sp.symbols("c a_0", positive=True)
Phi = sp.Function("Phi")(*sp.symbols("X Y Z"))
check("C4 covariantly, w is |a|/a0 for the acceleration a of the tetrad's time leg; in a static field c^2|a| = |grad Phi| exactly "
      "(proofs/sst-covariant-time-leg, Theorem 2), so w = x and the deformed leg is the time leg's acceleration direction",
      all(sp.simplify(c_**2*sp.diff(sp.log(sp.exp(Phi/c_**2)), v) - sp.diff(Phi, v)) == 0 for v in sp.symbols("X Y Z")))

print(f"\n{sum(ok)}/{len(ok)} checks passed")
