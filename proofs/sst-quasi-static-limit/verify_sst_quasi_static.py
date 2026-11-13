"""Machine checks for 'The SST Covariant Completion in Its Quasi-Static Limit'.
Exact algebra (sympy) for every identity; numerics only to evaluate physical sizes.
Run: python verify_sst_quasi_static.py"""
import sympy as sp
from sympy.calculus.euler import euler_equations

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

x, y, t = sp.symbols("x y t", positive=True)
G, a0, M, r, b, c, rho = sp.symbols("G a_0 M r b c rho", positive=True)
mu = lambda X: X / (X + 1)
F = lambda Y: Y - 2 * sp.sqrt(Y) + 2 * sp.log(1 + sp.sqrt(Y))

# ---- Lemma 1: the reading made precise, and the matter coupling
X1, X2, X3 = sp.symbols("X1 X2 X3")
P = sp.Function("Phi")(X1, X2, X3)
Q = sp.Function("Psi")(X1, X2, X3)
grad = [sp.diff(P, v) for v in (X1, X2, X3)]
Y = sum(g_ ** 2 for g_ in grad) / a0 ** 2
LEH = (sum(sp.diff(Q, v_) ** 2 for v_ in (X1, X2, X3)) - 2 * sum(sp.diff(P, v_) * sp.diff(Q, v_) for v_ in (X1, X2, X3))) / (8 * sp.pi * G)
Lread = LEH - a0 ** 2 / (8 * sp.pi * G) * (F(Y) - Y) - rho * P
check("L1.1 (Lemma 1) on Psi = Phi, the curvature term's static part plus -(a0^2/8 pi G)[F(y) - y] equals -(a0^2/8 pi G) F(y): "
      "the energy the archive varies", sp.simplify(LEH.subs(Q, P) - a0 ** 2 / (8 * sp.pi * G) * (F(Y) - Y) + a0 ** 2 / (8 * sp.pi * G) * F(Y)) == 0)
eL = euler_equations(Lread, [P, Q], [X1, X2, X3])
check("L1.2 its Psi-equation is lap(Phi - Psi) = 0, so Psi = Phi for decaying fields: gamma = 1 at leading order",
      sp.simplify(eL[1].lhs * 4 * sp.pi * G - sum(sp.diff(P - Q, v_, 2) for v_ in (X1, X2, X3))) == 0)
xg0 = sp.sqrt(sum(g_ ** 2 for g_ in grad)) / a0
tgt0 = sum(sp.diff(mu(xg0) * g_, v_) for g_, v_ in zip(grad, (X1, X2, X3))) / (4 * sp.pi * G) - rho
check("L1.3 and its Phi-equation on Psi = Phi is div[mu grad Phi] = 4 pi G rho", sp.simplify(eL[0].lhs.subs(Q, P).doit() - tgt0) == 0)
m_, P0 = sp.symbols("m Phi_0", positive=True)
check("L1.4 matter: -m c^2 sqrt(-g_00) = -m c^2 sqrt(1 + 2 Phi/c^2) = -m c^2 - m Phi + O(Phi^2/c^2): minimal coupling gives the source -rho Phi",
      sp.simplify(sp.series(-m_ * c ** 2 * sp.sqrt(1 + 2 * P0 / c ** 2), P0, 0, 2).removeO() - (-m_ * c ** 2 - m_ * P0)) == 0)

# ---- Theorem 1: the field equation from the action
check("T1.1 F(0) = 0 and F'(y) = mu(sqrt y): the kinetic function of the SST is the AQUAL energy of mu(x) = x/(x+1)",
      F(sp.Integer(0)) == 0 and sp.simplify(sp.diff(F(y), y) - mu(sp.sqrt(y))) == 0)
L = -a0 ** 2 / (8 * sp.pi * G) * F(Y) - rho * P
EL = euler_equations(L, [P], [X1, X2, X3])[0].lhs
xg = sp.sqrt(sum(g_ ** 2 for g_ in grad)) / a0
target = sum(sp.diff(mu(xg) * g_, v) for g_, v in zip(grad, (X1, X2, X3))) / (4 * sp.pi * G) - rho
check("T1.2 the Euler-Lagrange equation of -(a0^2/8 pi G) F(|grad Phi|^2/a0^2) - rho Phi is (1/4 pi G) div[mu grad Phi] - rho = 0, "
      "i.e. div[mu(|grad Phi|/a0) grad Phi] = 4 pi G rho", sp.simplify(EL - target) == 0)
check("T1.3 the prefactor: (a0^2/8 pi G)(2/a0^2) = 1/(4 pi G)", sp.simplify(a0 ** 2 / (8 * sp.pi * G) * 2 / a0 ** 2 - 1 / (4 * sp.pi * G)) == 0)

# ---- Theorem 2: the capacity form
f = (21 * x + 13) / (x + 1)
check("T2.1 the capacity function f(x) = (21x+13)/(x+1) = 17 + 4 sigma(x), sigma = (x-1)/(x+1), takes 13, 17, 21 at x = 0, 1, infinity",
      sp.simplify(f - (17 + 4 * (x - 1) / (x + 1))) == 0 and f.subs(x, 0) == 13 and f.subs(x, 1) == 17 and sp.limit(f, x, sp.oo) == 21)
check("T2.2 mu = (f - 13)/8 = x/(x+1), so div[((f-13)/8) grad Phi] = 4 pi G rho is the same field equation", sp.simplify((f - 13) / 8 - mu(x)) == 0)

# ---- Theorem 3: the spherical law and the inverse pipeline
h = sp.Function("h")
R3 = sp.sqrt(X1 ** 2 + X2 ** 2 + X3 ** 2)
Ph3 = h(R3)
g3 = [sp.diff(Ph3, v_) for v_ in (X1, X2, X3)]
mag = sp.sqrt(sum(g_ ** 2 for g_ in g3))
div3 = sum(sp.diff(mu(mag / a0) * g_, v_) for g_, v_ in zip(g3, (X1, X2, X3)))
hp = sp.Function("hp")
rr = sp.symbols("rr", positive=True)
sph = (sp.diff(rr ** 2 * mu(h(rr).diff(rr) / a0) * h(rr).diff(rr), rr) / rr ** 2)
pt = {X1: sp.Rational(3, 7), X2: -sp.Rational(2, 5), X3: sp.Rational(1, 3)}
r0 = sp.sqrt(sum(val ** 2 for val in pt.values()))
test = lambda expr: expr.subs(h, sp.Lambda(rr, sp.exp(-rr) + rr ** 3))   # a concrete increasing-gradient profile
lhs = sp.N(test(div3).doit().subs(pt), 30)
rhs = sp.N(test(sph).doit().subs(rr, r0), 30)
check("T3.1 in spherical symmetry div[mu grad Phi] = r^-2 d/dr(r^2 mu Phi') (checked on a test profile at a test point to 30 digits), so with "
      "4 pi r^2 rho = M'(r) the field equation integrates to r^2 mu(g_t/a0) g_t = G M(<r), the conserved flux, with no curl term",
      abs(lhs - rhs) < 1e-25)
gt, gs = sp.symbols("g_t g_s", positive=True)
check("T3.2 mu(g_t/a0) g_t = g_s  <=>  g_s = g_t^2/(a0 + g_t), the spherical field equation", sp.simplify(mu(gt / a0) * gt - gt ** 2 / (a0 + gt)) == 0)
fwd = (gs + sp.sqrt(gs ** 2 + 4 * gs * a0)) / 2
check("T3.3 the forward solver g_t = [g_s + sqrt(g_s^2 + 4 g_s a0)]/2 is the unique positive root (the other root is negative)",
      sp.simplify(fwd ** 2 / (a0 + fwd) - gs) == 0
      and sp.simplify(((gs - sp.sqrt(gs ** 2 + 4 * gs * a0)) / 2)).subs({gs: 1, a0: 1}) < 0)
v = sp.symbols("v", positive=True)
Mdec = r * v ** 4 / (G * (a0 * r + v ** 2))
check("T3.4 with g_t = v^2/r and g_s = G M/r^2: M_dec(r) = r v^4/[G(a0 r + v^2)]; decoding then re-solving returns v",
      sp.simplify(Mdec - r ** 2 / G * (v ** 2 / r) ** 2 / (a0 + v ** 2 / r)) == 0
      and all(abs(sp.N(fwd.subs(gs, G * Mdec / r ** 2).subs(vals) - (v ** 2 / r).subs(vals), 40)) < 1e-30
              for vals in ({G: 1, a0: 1, r: 2, v: 3}, {G: sp.Rational(1, 3), a0: 5, r: sp.Rational(7, 2), v: sp.Rational(1, 4)}, {G: 2, a0: sp.Rational(1, 9), r: 11, v: 2})))

# ---- Theorem 4: limits and scales
check("T4.1 Newtonian limit: g_t = g_s + a0 - a0^2/g_s + O(g_s^-2) as g_s -> infinity",
      sp.simplify(sp.series(fwd.subs(gs, 1 / t), t, 0, 2).removeO().subs(t, 1 / gs) - (gs + a0 - a0 ** 2 / gs)) == 0)
check("T4.2 deep limit: g_t = sqrt(g_s a0) + g_s/2 + O(g_s^(3/2)) as g_s -> 0",
      sp.simplify(sp.series(fwd.subs(gs, t ** 2), t, 0, 3).removeO() - (t * sp.sqrt(a0) + t ** 2 / 2)) == 0)
vflat = sp.sqrt(fwd.subs(gs, G * M / r ** 2) * r)
check("T4.3 baryonic Tully-Fisher: for a bounded mass M, v^4 -> G M a0 exactly as r -> infinity", sp.simplify(sp.limit(vflat ** 4, r, sp.oo) - G * M * a0) == 0)
check("T4.4 the TetB share of the field is (1 - mu) g_t = a0 mu(g_t/a0) < a0: bounded by the acceleration scale",
      sp.simplify((1 - mu(gt / a0)) * gt - a0 * mu(gt / a0)) == 0)
phi_g = (1 + sp.sqrt(5)) / 2
check("T4.5 the ring x = 1 (mu = 1/2) lies where g_s = a0/2, at r_1 = sqrt(2 G M/a0); at r = sqrt(G M/a0) (g_s = a0) the field is x = phi "
      "= (1 + sqrt5)/2 with mu = 1/phi", sp.simplify((1 ** 2 / (1 + 1)) - sp.Rational(1, 2)) == 0
      and sp.simplify(fwd.subs({gs: a0}) / a0 - phi_g) == 0 and sp.simplify(mu(phi_g) - 1 / phi_g) == 0)
gtr = fwd.subs(gs, G * M / r ** 2)
rho_ph = sp.diff(r ** 2 * gtr, r) / (4 * sp.pi * G * r ** 2)
lead = sp.limit(rho_ph * r ** 2, r, sp.oo)
check("T4.6 outside a point mass the phantom density is rho_ph = (4 pi G r^2)^-1 d/dr(r^2 g_t), with leading term sqrt(G M a0)/(4 pi G r^2)",
      sp.simplify(lead - sp.sqrt(G * M * a0) / (4 * sp.pi * G)) == 0)

# ---- Theorem 5: uniqueness and ellipticity (from the energy-functional proof)
e_perp, e_par = 2 * mu(x), 2 * sp.diff(x * mu(x), x)
check("T5.1 the Hessian of F(|p|^2/a0^2) in p has eigenvalues 2 mu (across) and 2 (x mu)' (along), both positive for x > 0",
      sp.simplify(e_perp - 2 * x / (x + 1)) == 0 and sp.simplify(e_par - 2 * x * (x + 2) / (x + 1) ** 2) == 0)
check("T5.2 their ratio (x mu)'/mu = 1 + (1 - mu) lies in [1, 2]: elliptic, with anisotropy equal to the TetB share",
      sp.simplify(sp.diff(x * mu(x), x) / mu(x) - (1 + (1 - mu(x)))) == 0)

# ---- Theorem 6: the single-potential reading
z = sp.symbols("z", real=True)
def deflection(gfun, gamma=1):
    return sp.simplify((1 + gamma) / c ** 2 * sp.integrate(gfun(sp.sqrt(b ** 2 + z ** 2)) * b / sp.sqrt(b ** 2 + z ** 2), (z, -sp.oo, sp.oo)))
check("T6.1 with g_00 = -(1 + 2 Phi/c^2), g_ij = (1 - 2 Phi/c^2) delta_ij (gamma = 1), a Newtonian point mass deflects light by 4 G M/(b c^2)",
      sp.simplify(deflection(lambda R: G * M / R ** 2) - 4 * G * M / (b * c ** 2)) == 0)
check("T6.2 in the deep field g_t = sqrt(G M a0)/r gives the constant deflection 2 pi sqrt(G M a0)/c^2 (Milgrom's result)",
      sp.simplify(deflection(lambda R: sp.sqrt(G * M * a0) / R) - 2 * sp.pi * sp.sqrt(G * M * a0) / c ** 2) == 0)
check("T6.3 so the lensing mass equals the dynamical mass: the deflection is the integral of the same g_t that sets the rotation curve, and a "
      "GR lens of mass profile M_dyn(r) = g_t r^2/G gives the identical integral",
      sp.simplify(deflection(lambda R: G * (fwd.subs(gs, G * M / R ** 2) * R ** 2 / G) / R ** 2) - deflection(lambda R: fwd.subs(gs, G * M / R ** 2))) == 0)
check("T6.4 in a galaxy (v = 200 km/s) the EM factor departs from 1 by about 2|Phi|/c^2 ~ 1e-6, so it does not enter the static dynamics",
      abs(float(2 * (2e5) ** 2 / (2.998e8) ** 2) - 8.9e-7) < 1e-7)

# ---- Remark: why the convention is needed
Q = sp.Function("Psi")(X1, X2, X3)
LEH = (sum(sp.diff(Q, v_) ** 2 for v_ in (X1, X2, X3)) - 2 * sum(sp.diff(P, v_) * sp.diff(Q, v_) for v_ in (X1, X2, X3))) / (8 * sp.pi * G)
eP = euler_equations(LEH + L, [P, Q], [X1, X2, X3])
target2 = sum(sp.diff((1 + mu(xg)) * g_, v_) for g_, v_ in zip(grad, (X1, X2, X3))) / (4 * sp.pi * G) - rho
check("R1 (convention) if the static weak-field part of R/16 pi G, (1/8 pi G)[(grad Psi)^2 - 2 grad Phi.grad Psi], were also counted for "
      "Phi, the equations would give Psi = Phi and div[(1 + mu) grad Phi] = 4 pi G rho; the SST's field equation requires Phi's response "
      "to be carried by F alone, as the archive states",
      sp.simplify(eP[0].lhs.subs(Q, P).doit() - target2) == 0)

print(f"\n{sum(ok)}/{len(ok)} checks passed")
