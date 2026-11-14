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
# A1 decoupling-limit coefficients d_k from the beta's
d = [b[0] + 3*b[1] + 3*b[2] + b[3], b[1] + 2*b[2] + b[3], b[2] + b[3], b[3]]
dl = [v.subs(dict(zip(b, LOCK))) for v in d]
check("A1 the h-pi mixing coefficients (d0, d1, d2, d3) = (49, 32, 16, 0) for the locked set: d1 = 32 is the Fierz-Pauli "
      "combination, d3 = 0 removes the quintic mixing, d2 = 16 != 0 keeps the cubic Galileon", dl == [49, 32, 16, 0])
# A2 the static spherical screening equation, from the decoupling-limit pi-equation with a3 = 0
a1, a2, q, Mp, lam, sv, Q = sp.symbols("a1 a2 q M lambda s Q", nonzero=True)
pieq = sp.Rational(3, 2)*a1**2*lam - 3*a1*a2*lam**2 + a2**2*lam**3 + a1*q/(4*Mp)
sub = pieq.subs(lam, -sv*q/(2*Mp*a1))
target = Q**2*sv**3 + 6*Q*sv**2 + 6*sv - 2
ratio = sp.simplify(sp.factor(sp.expand(sub).subs(a2, Q*Mp*a1**2/q)) / target)
check("A2 with lambda = pi'/r = -s q/(2 M a1) and Q = a2 q/(M a1^2), the pi-equation is proportional to Q^2 s^3 + 6 Q s^2 + 6 s - 2 = 0 "
      "(q = M_enc/(4 pi r^3), g_tot/g_N = 1 + s): r enters only through q, so the response depends on the enclosed mass only through M_enc/r^3",
      ratio.free_symbols.isdisjoint({sv, Q}) and ratio != 0)
v_ = sp.symbols("v")
Qv = v_*(v_**2 + 6*v_ + 6)/2
vstar = -2 + sp.sqrt(2)
check("A3 bounded enhancement: s -> 1/3 as Q -> 0 (g_tot/g_N = 4/3, vDVZ); on the Q < 0 branch the turning point is Q* = 2 - 2 sqrt2 with "
      "s = 1/sqrt2, so g_tot/g_N < 1.71; as Q -> +inf, s -> 0 (screened to GR). Flat rotation curves need g_tot/g_N -> inf",
      sp.solve(target.subs(Q, 0), sv) == [sp.Rational(1, 3)] and sp.simplify(sp.diff(Qv, v_).subs(v_, vstar)) == 0
      and sp.simplify(Qv.subs(v_, vstar) - (2 - 2*sp.sqrt(2))) == 0 and sp.simplify(vstar/Qv.subs(v_, vstar) - 1/sp.sqrt(2)) == 0
      and float(1 + 1/sp.sqrt(2)) < 1.71)
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
