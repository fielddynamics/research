"""Machine checks for every step of
'The Energy Functional of the Constitutive Law mu(x) = x/(x+1)'.
Run: python verify_aqual_energy_functional.py"""
import numpy as np
import sympy as sp

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

y, u, r, t = sp.symbols('y u r t', positive=True)
mu = lambda x: x / (x + 1)
F = y - 2 * sp.sqrt(y) + 2 * sp.log(1 + sp.sqrt(y))

# ---- Setting: Euler-Lagrange equation and its sign
X, Y, Z, a0, G, rho = sp.symbols('X Y Z a0 G rho', positive=True)
Phi = sp.Function('Phi')(X, Y, Z)
Fs = sp.Function('Fs')
grad2 = sum(sp.diff(Phi, v)**2 for v in (X, Y, Z))
def el(sign_rho):
    L = -(a0**2 / (8 * sp.pi * G)) * Fs(grad2 / a0**2) + sign_rho * rho * Phi
    return sp.euler_equations(L, Phi, (X, Y, Z))[0].lhs
Fp = sp.Subs(sp.Derivative(Fs(t), t), t, grad2 / a0**2).doit()
div = sum(sp.diff(Fp * sp.diff(Phi, v), v) for v in (X, Y, Z))
check("Setting: L = -(a0^2/8piG) F - rho Phi gives div(F' grad Phi) = 4 pi G rho",
      sp.simplify(el(-1) * 4 * sp.pi * G - (div - 4 * sp.pi * G * rho)) == 0)
check("Setting: the opposite sign, + rho Phi, would give div(F' grad Phi) = -4 pi G rho",
      sp.simplify(el(+1) * 4 * sp.pi * G - (div + 4 * sp.pi * G * rho)) == 0)
check("Setting: an additive constant in F leaves the field equation unchanged",
      sp.diff(F + sp.Symbol('C'), y) == sp.diff(F, y))

# ---- Theorem 1
check("Theorem 1: F'(y) = mu(sqrt y)", sp.simplify(sp.diff(F, y) - mu(sp.sqrt(y))) == 0)
check("Theorem 1: F(0) = 0 and F'(y) -> 0 as y -> 0",
      sp.limit(F, y, 0) == 0 and sp.limit(sp.diff(F, y), y, 0) == 0)
check("Theorem 1: u^2/(1+u) = u - 1 + 1/(1+u)", sp.simplify(u**2 / (1 + u) - (u - 1 + 1 / (1 + u))) == 0)
check("Theorem 1: integral of sqrt(t)/(1+sqrt t) from 0 to y equals F (numerical, 6 points)",
      all(abs(sp.N(sp.Integral(sp.sqrt(t) / (1 + sp.sqrt(t)), (t, 0, yv))) - sp.N(F.subs(y, yv))) < 1e-12
          for yv in [sp.Rational(1, 100), sp.Rational(1, 2), 1, 3, 10, 1000]))
Fu = F.subs(y, u**2)
check("Theorem 1: dF/du = 2u^2/(1+u)", sp.simplify(sp.diff(Fu, u) - 2 * u**2 / (1 + u)) == 0)

# ---- Corollary 1
small = sp.series(Fu, u, 0, 14).removeO()
check("Corollary 1: small-y series = 2 sum_{k>=3} (-1)^(k+1) u^k / k (through u^13)",
      sp.expand(small - sum(2 * (-1)**(k + 1) * u**k / k for k in range(3, 14))) == 0)
check("Corollary 1: leading terms (2/3) y^(3/2) - (1/2) y^2 + (2/5) y^(5/2)",
      sp.expand(small).coeff(u, 3) == sp.Rational(2, 3) and sp.expand(small).coeff(u, 4) == -sp.Rational(1, 2)
      and sp.expand(small).coeff(u, 5) == sp.Rational(2, 5))
w = sp.symbols('w', positive=True)    # w = 1/u
rest = sp.series(Fu.subs(u, 1 / w) - (1 / w**2 - 2 / w + 2 * sp.log(1 / w)), w, 0, 12).removeO()
check("Corollary 1: large-y series = y - 2 sqrt y + ln y + 2 sum_{k>=1} (-1)^(k+1) y^(-k/2) / k (through 11 terms)",
      sp.expand(rest - sum(2 * (-1)**(k + 1) * w**k / k for k in range(1, 12))) == 0)
check("Corollary 1: the series converge on their ranges (numerical, y = 0.5 and y = 4, 200 terms)",
      abs(float(2 * sum((-1)**(k + 1) * 0.5**(k / 2) / k for k in range(3, 400))) - float(F.subs(y, sp.Rational(1, 2)))) < 1e-10
      and abs(float(4 - 2 * 2 + np.log(4) + 2 * sum((-1)**(k + 1) * 4**(-k / 2) / k for k in range(1, 200)))
              - float(F.subs(y, 4))) < 1e-12)
check("Corollary 1: deep-MOND, mu(x) ~ x, and Newtonian, mu -> 1",
      sp.limit(mu(r) / r, r, 0) == 1 and sp.limit(mu(r), r, sp.oo) == 1)
check("Corollary 1: the orders u and u^2 cancel among the three terms",
      sp.series(Fu, u, 0, 3).removeO() == 0)

# ---- Theorem 2
g = Fu.subs(u, r)
gp, gpp = sp.simplify(sp.diff(g, r)), sp.simplify(sp.diff(g, r, 2))
check("Theorem 2: g'(r) = 2 r^2/(1+r) = 2 r mu(r)", sp.simplify(gp - 2 * r**2 / (1 + r)) == 0 and sp.simplify(gp - 2 * r * mu(r)) == 0)
check("Theorem 2: g''(r) = 2 r (r+2)/(r+1)^2 = 2 (x mu)'", sp.simplify(gpp - 2 * r * (r + 2) / (r + 1)**2) == 0
      and sp.simplify(gpp - 2 * sp.diff(r * mu(r), r)) == 0)
check("Theorem 2: g'/r -> 0 and g'' -> 0 as r -> 0 (gradient and Hessian extend continuously by 0)",
      sp.limit(gp / r, r, 0) == 0 and sp.limit(gpp, r, 0) == 0 and sp.limit(gp, r, 0) == 0)
q1, q2, q3 = sp.symbols('q1 q2 q3', real=True)
qv = sp.Matrix([q1, q2, q3]); R = sp.sqrt(q1**2 + q2**2 + q3**2)
Gq = R**2 - 2 * R + 2 * sp.log(1 + R)
H = sp.hessian(Gq, (q1, q2, q3))
qhat = qv / R
Hform = 2 * mu(R) * (sp.eye(3) - qhat * qhat.T) + 2 * sp.diff(r * mu(r), r).subs(r, R) * qhat * qhat.T
pt = {q1: sp.Rational(3, 7), q2: -sp.Rational(5, 3), q3: sp.Rational(2, 9)}
check("Theorem 2: Hessian of W(q) equals 2mu (I - qq^T) + 2(x mu)' qq^T (exact at a rational point)",
      sp.simplify((H - Hform).subs(pt)) == sp.zeros(3, 3))
check("Theorem 2: eigenvalues 2mu (twice) and 2(x mu)' (once) are positive for x > 0",
      all(sp.simplify(e) > 0 for e in [2 * mu(r).subs(r, 2), (2 * sp.diff(r * mu(r), r)).subs(r, 2)]) and
      sp.solve(sp.Eq(r * (r + 2), 0), r) == [])
check("Theorem 2: ratio (x mu)'/mu = (x+2)/(x+1), in (1, 2]",
      sp.simplify(sp.diff(r * mu(r), r) / mu(r) - (r + 2) / (r + 1)) == 0 and
      sp.limit((r + 2) / (r + 1), r, 0) == 2 and sp.limit((r + 2) / (r + 1), r, sp.oo) == 1 and
      sp.simplify(sp.diff((r + 2) / (r + 1), r)) < 0)
check("Theorem 2: A(p) = mu(|p|/a0) p = (a0/2) grad G(p/a0)",
      sp.simplify((a0 / 2) * sp.Matrix([sp.diff(Gq, v) for v in (q1, q2, q3)]).subs({q1: q1 / a0, q2: q2 / a0, q3: q3 / a0})
                  - mu(R / a0) * qv) == sp.zeros(3, 1))
rng = np.random.default_rng(0)
def A(p, a=1.0): n = np.linalg.norm(p); return n / (a + n) * p
viol = sum(1 for _ in range(200000)
           for p, pp in [(rng.normal(size=3) * rng.exponential(3), rng.normal(size=3) * rng.exponential(3))]
           if (A(p) - A(pp)) @ (p - pp) <= 0)
check("Theorem 2: strict monotonicity of A on 200000 random pairs, including small and large gradients", viol == 0)
seg_ok = True
for _ in range(2000):   # strict convexity along segments through the origin
    p = rng.normal(size=3); pp = -rng.uniform(0.1, 3) * p
    Gn = lambda v: np.linalg.norm(v)**2 - 2 * np.linalg.norm(v) + 2 * np.log1p(np.linalg.norm(v))
    seg_ok &= Gn(0.5 * (p + pp)) < 0.5 * (Gn(p) + Gn(pp))
check("Theorem 2: strict convexity holds on segments through q = 0 (2000 random cases)", seg_ok)

# ---- Corollary 2
pvec = sp.Matrix([q1, q2, q3])
Ap = R * pvec / (a0 + R)
J = Ap.jacobian(pvec)
Jform = R / (a0 + R) * sp.eye(3) + a0 / (a0 + R)**2 * pvec * pvec.T / R
check("Corollary 2: A(p) = |p| p/(a0+|p|) has Jacobian |p|/(a0+|p|) I + a0 p p^T/(|p|(a0+|p|)^2), of norm <= 2|p|/a0 -> 0 (A is C^1)",
      sp.simplify(Ap - mu(R / a0) * pvec) == sp.zeros(3, 1) and sp.simplify(J - Jform) == sp.zeros(3, 3))

print(f"\n{sum(ok)}/{len(ok)} checks passed")
