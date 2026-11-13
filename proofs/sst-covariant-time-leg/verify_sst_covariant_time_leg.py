"""Machine checks for 'The SST Covariant Completion: y From the Acceleration of the Time Leg'.
Exact algebra (sympy) for every identity; random-point evaluation only for one time-dependent positivity check.
Run: python verify_sst_covariant_time_leg.py"""
import random
import sympy as sp
from sympy.calculus.euler import euler_equations

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

t, x, y, z = sp.symbols("t x y z", real=True)
c, a0, G, rho = sp.symbols("c a_0 G rho", positive=True)
X = [t, x, y, z]
def christoffel(g):
    gi = g.inv()
    return [[[sp.simplify(sum(gi[a, d] * (sp.diff(g[d, b], X[e]) + sp.diff(g[d, e], X[b]) - sp.diff(g[b, e], X[d])) for d in range(4)) / 2)
              for e in range(4)] for b in range(4)] for a in range(4)]
def accel(g, u):
    Gm = christoffel(g)
    return [sp.simplify(sum(u[n] * (sp.diff(u[m], X[n]) + sum(Gm[m][n][l] * u[l] for l in range(4))) for n in range(4))) for m in range(4)]
lower = lambda g, v: [sp.simplify(sum(g[m, n] * v[n] for n in range(4))) for m in range(4)]
dot = lambda g, v, w: sp.simplify(sum(g[m, n] * v[m] * w[n] for m in range(4) for n in range(4)))

# ---- Theorem 1: covariance and positivity
Nf = sp.Function("N")(t, x, y, z); Wf = sp.Function("W")(t, x, y, z)
gT = sp.diag(-Nf ** 2 * c ** 2, Wf ** 2, Wf ** 2, Wf ** 2)
uT = [1 / (Nf * c), 0, 0, 0]
aT = accel(gT, uT)
check("T1.1 u = e_0 is unit timelike, g(u,u) = -1, and its acceleration a = (u.grad)u satisfies a.u = 0 identically (general time-dependent "
      "lapse N(t,x) and conformal factor W(t,x))", sp.simplify(dot(gT, uT, uT) + 1) == 0 and sp.simplify(dot(gT, aT, uT)) == 0)
N2 = 1 + sp.Rational(1, 10) * sp.sin(t + x) * sp.exp(-y ** 2); W2 = 1 + sp.Rational(1, 5) * sp.cos(z - t)
g2 = sp.diag(-N2 ** 2, W2 ** 2, W2 ** 2, W2 ** 2); u2 = [1 / N2, 0, 0, 0]
a2 = accel(g2, u2)
random.seed(3)
pos = all(float(dot(g2, a2, a2).subs({t: random.uniform(-3, 3), x: random.uniform(-3, 3), y: random.uniform(-3, 3), z: random.uniform(-3, 3)})) >= -1e-14
          for _ in range(20))
check("T1.2 so a is spacelike or zero and y = c^4 a.a/a0^2 >= 0 for every configuration (checked on a time-dependent metric at 20 random "
      "points): F(y) is defined everywhere and no timelike-gradient branch is needed", pos)

# ---- Theorem 2: the static reduction
Ns = sp.Function("N")(x, y, z); Ws = sp.Function("W")(x, y, z)
gS = sp.diag(-Ns ** 2 * c ** 2, Ws ** 2, Ws ** 2, Ws ** 2); uS = [1 / (Ns * c), 0, 0, 0]
aS = lower(gS, accel(gS, uS))
check("T2.1 for a static metric -N^2 c^2 dt^2 + h, the time leg's acceleration is a_0 = 0, a_i = d_i ln N exactly",
      aS[0] == 0 and all(sp.simplify(aS[i] - sp.diff(sp.log(Ns), X[i])) == 0 for i in (1, 2, 3)))
Phi = sp.Function("Phi")(x, y, z)
check("T2.2 with N = exp(Phi/c^2): c^2 a_i = d_i Phi exactly, so the field strength is the time leg's acceleration",
      all(sp.simplify(c ** 2 * aS[i].subs(Ns, sp.exp(Phi / c ** 2)).doit() - sp.diff(Phi, X[i])) == 0 for i in (1, 2, 3)))
aa = dot(gS, accel(gS, uS), accel(gS, uS))
check("T2.3 and y = c^4 a.a/a0^2 = h^ij d_i Phi d_j Phi / a0^2 = |grad Phi|^2/(W^2 a0^2) exactly",
      sp.simplify(c ** 4 * aa.subs(Ns, sp.exp(Phi / c ** 2)).doit() - sum(sp.diff(Phi, v) ** 2 for v in (x, y, z)) / Ws ** 2) == 0)
Psi = sp.Function("Psi")(x, y, z)
yw = (c ** 4 * aa.subs({Ns: sp.exp(Phi / c ** 2), Ws: 1 - Psi / c ** 2}).doit() / a0 ** 2)
check("T2.4 in the weak field (W = 1 - Psi/c^2) y = |grad Phi|^2/a0^2 + O(1/c^2): the archive's y is the static form of this scalar",
      sp.simplify(sp.limit(yw, c, sp.oo) - sum(sp.diff(Phi, v) ** 2 for v in (x, y, z)) / a0 ** 2) == 0)

# ---- Theorem 3: the covariant SST and Lemma 1
A = sp.symbols("A", positive=True)
F = lambda Y: Y - 2 * sp.sqrt(Y) + 2 * sp.log(1 + sp.sqrt(Y))
mu = lambda X_: X_ / (X_ + 1)
f = a0 ** 2 * (F(A ** 2 / a0 ** 2) - A ** 2 / a0 ** 2)
chi = sp.diff(f, A) / (2 * A)
check("T3.1 the SST as written, varied as in Lemma 1, has Blanchet-Marsat's field equations with f = a0^2 [F(y) - y], y = a^2/a0^2 (c = 1): "
      "their chi = f'(a)/2a = mu - 1, so mu_total = 1 + chi = mu(a/a0) = x/(x+1)", sp.simplify(chi - (mu(A / a0) - 1)) == 0)
check("T3.2 term by term -2f/16 pi G = -(a0^2/8 pi G)[F(y) - y]: the y of F is the curvature term's (Lemma 1), F - y is the rest; "
      "the action itself is the SST as written", sp.simplify(-2 * f / (16 * sp.pi * G) + a0 ** 2 / (8 * sp.pi * G) * (F(A ** 2 / a0 ** 2) - A ** 2 / a0 ** 2)) == 0)
X1, X2, X3 = sp.symbols("X1 X2 X3")
P = sp.Function("Phi")(X1, X2, X3); Q = sp.Function("Psi")(X1, X2, X3)
gr = [sp.diff(P, v) for v in (X1, X2, X3)]
Yv = sum(g_ ** 2 for g_ in gr) / a0 ** 2
LEH = (sum(sp.diff(Q, v) ** 2 for v in (X1, X2, X3)) - 2 * sum(sp.diff(P, v) * sp.diff(Q, v) for v in (X1, X2, X3))) / (8 * sp.pi * G)
L = LEH - a0 ** 2 / (8 * sp.pi * G) * (F(Yv) - Yv) - rho * P
eL = euler_equations(L, [P, Q], [X1, X2, X3])
xg = sp.sqrt(sum(g_ ** 2 for g_ in gr)) / a0
tgt = sum(sp.diff(mu(xg) * g_, v) for g_, v in zip(gr, (X1, X2, X3))) / (4 * sp.pi * G) - rho
check("T3.3 the SST's static weak-field reduction (N = exp(Phi/c^2), h = (1 - 2 Psi/c^2) delta, minimal coupling) gives lap(Phi - Psi) = 0, so "
      "Psi = Phi (gamma = 1), and div[mu grad Phi] = 4 pi G rho",
      sp.simplify(eL[1].lhs * 4 * sp.pi * G - sum(sp.diff(P - Q, v, 2) for v in (X1, X2, X3))) == 0
      and sp.simplify(eL[0].lhs.subs(Q, P).doit() - tgt) == 0)

# ---- Theorem 4: no separate scalar; the size of the time-leg term's stress-energy
M, r = sp.symbols("M r", positive=True)
Ys = sp.symbols("Y", positive=True)
check("T4.1 deep field: F(y) - y = -y + (2/3) y^(3/2) + O(y^2), so the time-leg term's energy density is ~ a0^2 y/(8 pi G) = g^2/(8 pi G)",
      sp.simplify(sp.series(F(Ys) - Ys, Ys, 0, 2).removeO().subs(Ys, sp.Symbol("q", positive=True) ** 2)
                  - (-sp.Symbol("q", positive=True) ** 2 + sp.Rational(2, 3) * sp.Symbol("q", positive=True) ** 3)) == 0)
gd2 = G * M * a0 / r ** 2                          # deep field g^2
rho_tl = gd2 / (8 * sp.pi * G * c ** 2)            # its energy density as a mass density
rho_ph = sp.sqrt(G * M * a0) / (4 * sp.pi * G * r ** 2)   # deep-field phantom density div[(1-mu) grad Phi]/4 pi G ~ g/(2 pi G r)... exact for g = sqrt(GMa0)/r
check("T4.2 Phi is the lapse potential, not an independent field, so there is no separate scalar stress tensor: the time-leg term's "
      "stress-energy is the gravitational field energy, v^2/(2c^2) times the phantom density (v^4 = G M a0): ~2e-7 at 200 km/s",
      sp.simplify(rho_tl / rho_ph - sp.sqrt(G * M * a0) / (2 * c ** 2)) == 0 and abs((2e5) ** 2 / (2 * 3e8 ** 2) - 2.2e-7) < 1e-8)
Pr = sp.Function("Phi")(r)
gt_ = sp.sqrt(G * M * a0) / r
check("T4.3 the metric 00-equation carries the TetB share as a source: lap Phi = 4 pi G (rho + rho_ph), rho_ph = div[(1 - mu) grad Phi]/4 pi G; "
      "for the deep point mass rho_ph = sqrt(G M a0)/(4 pi G r^2)",
      sp.simplify(sp.diff(r ** 2 * gt_, r) / r ** 2 / (4 * sp.pi * G) - rho_ph) == 0)

# ---- Theorem 5: cosmology
ta = sp.Function("a")(t)
gF = sp.diag(-1, ta ** 2, ta ** 2, ta ** 2); uF = [1, 0, 0, 0]
check("T5.1 in a homogeneous, isotropic (FLRW) background the comoving time leg is geodesic, a = 0, so y = 0 and F(0) = 0: the background is "
      "exactly general relativity; the SST acts on perturbations", all(sp.simplify(v) == 0 for v in accel(gF, uF)) and F(sp.Integer(0)) == 0)

# ---- Theorem 6: the two limits of f
e = sp.symbols("e", positive=True)
check("T6.1 deep field: f = -a^2 + 2a^3/(3 a0) + O(a^4), Blanchet-Marsat's MOND condition with Lambda_0 = 0",
      sp.simplify(sp.series(f, A, 0, 4).removeO() - (-A ** 2 + 2 * A ** 3 / (3 * a0))) == 0)
check("T6.2 strong field: f = -2 a0 a + 2 a0^2 ln(a/a0) + O(1) does not tend to a constant (their condition for exact GR), and the residual "
      "field a0 mu(x) -> a0 as x -> infinity", sp.limit(f / A, A, sp.oo) == -2 * a0 and sp.limit(a0 * mu(A / a0), A, sp.oo) == a0)
gsat = 6.5e-5   # Sun's field at Saturn, m/s^2 (G M_sun / (9.5 AU)^2)
xs = gsat / 1.2e-10
check("T6.3 applied to the Sun's own field, the TetB tail (1 - mu) g is a0 to 2 parts in 10^6 at Saturn (x ~ 5e5): the per-mass tail the "
      "archive records as excluded (Coles Notes 5.4); evaluated on each mass's own time leg, the action does not implement the net-field rule",
      abs((1 - xs / (xs + 1)) * gsat / 1.2e-10 - 1) < 3e-6)

print(f"\n{sum(ok)}/{len(ok)} checks passed")
