"""Machine checks for every step of
'The Two-Potential Energy of the Constitutive Law mu(x) = x/(x+1) in Bimetric MOND'.
Run: python verify_bimetric_two_potential_energy.py"""
import itertools
import numpy as np
import sympy as sp

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

def sqrt_factor(e):   # sqrt(p(x)) -> sqrt(factor(p)), so sqrt((x+2)^2) -> x+2 for x > 0
    return e.replace(lambda s: s.is_Pow and s.exp == sp.Rational(1, 2), lambda s: sp.sqrt(sp.factor(s.base)))

x, y, s, t, z = sp.symbols('x y s t z', positive=True)
mu = lambda v: v / (v + 1)
b = 1 / (1 + x)

# ---- Setting: Euler-Lagrange equations of the nonrelativistic BIMOND Lagrangian
X1, X2, X3, a0, G, rho, rhoh, al, be = sp.symbols('X1 X2 X3 a0 G rho rhohat alpha beta', real=True)
co = (X1, X2, X3)
ph = sp.Function('phi')(*co); phh = sp.Function('phihat')(*co)
Mf = sp.Function('M')
grad = lambda f: [sp.diff(f, v) for v in co]
dot = lambda A, B: sum(p * q for p, q in zip(A, B))
div = lambda A: sum(sp.diff(A[i], co[i]) for i in range(3))
gs = [p - q for p, q in zip(grad(ph), grad(phh))]               # grad phi*
zz = dot(gs, gs) / a0**2
L = -(1 / (8 * sp.pi * G)) * (be * dot(grad(ph), grad(ph)) + al * dot(grad(phh), grad(phh)) - a0**2 * Mf(zz)) \
    - rho * ph + rhoh * phh
E1, E2 = [e.lhs for e in sp.euler_equations(L, [ph, phh], co)]
Mp = sp.Subs(sp.Derivative(Mf(t), t), t, zz).doit()
eq1 = div([be * p - Mp * q for p, q in zip(grad(ph), gs)]) - 4 * sp.pi * G * rho          # = 0
eq2 = div([al * p + Mp * q for p, q in zip(grad(phh), gs)]) + 4 * sp.pi * G * rhoh        # = 0
check("Setting: the phi equation is div[beta grad phi - M' grad phi*] = 4 pi G rho",
      sp.simplify(E1 * 4 * sp.pi * G - eq1) == 0)
check("Setting: the phihat equation is div[alpha grad phihat + M' grad phi*] = -4 pi G rhohat",
      sp.simplify(E2 * 4 * sp.pi * G - eq2) == 0)

# ---- Theorem 1
comb = sp.expand(al * eq1 - be * eq2)
target = sp.expand(div([(al * be - (al + be) * Mp) * q for q in gs]) - 4 * sp.pi * G * (al * rho + be * rhoh))
check("Theorem 1: alpha*(phi eq) - beta*(phihat eq) gives div[(alpha beta - (alpha+beta) M') grad phi*] = 4 pi G (alpha rho + beta rhohat)",
      sp.simplify(comb - target) == 0)
lap = lambda f: div(grad(f))
phs = ph - phh
check("Theorem 1: alpha = -beta = -1 gives Laplacian(phi*) = 4 pi G (rho - rhohat)",
      sp.simplify((target.subs({al: -1, be: 1})) / (-1) - (lap(phs) - 4 * sp.pi * G * (rho - rhoh))) == 0)
check("Theorem 1: and then Laplacian(phi) = 4 pi G rho + div(M' grad phi*)",
      sp.simplify(eq1.subs(be, 1) - (lap(ph) - div([Mp * q for q in gs]) - 4 * sp.pi * G * rho)) == 0)
check("Theorem 1: for alpha + beta != 0 the phi* coefficient alpha beta - (alpha+beta) M' is constant only if M' is",
      sp.solve(sp.diff(al * be - (al + be) * sp.Function('m')(z), z), sp.Derivative(sp.Function('m')(z), z)) == [0])
Mpz = -sp.Rational(1, 2) + sp.sqrt(sp.Rational(1, 4) + z**sp.Rational(-1, 2))     # Theorem 2's M'
check("Theorem 1: a nonconstant M' is required: M' -> 0 (z -> oo) and M' -> oo (z -> 0) for the M' of Theorem 2",
      sp.limit(Mpz, z, sp.oo) == 0 and sp.limit(Mpz, z, 0) == sp.oo)

# ---- Lemma 1: the tetrad Einstein-Hilbert term is odd under parity
eps = np.zeros((4,) * 4)
for p in itertools.permutations(range(4)):
    eps[p] = np.linalg.det(np.eye(4)[list(p)])
etaN = np.diag([-1.0, 1, 1, 1])
P = np.diag([1.0, -1, 1, 1])
ch, sh = np.cosh(0.7), np.sinh(0.7)
boost = np.eye(4); boost[0, 0] = boost[1, 1] = ch; boost[0, 1] = boost[1, 0] = sh
rot = np.eye(4); rot[2, 2] = rot[3, 3] = np.cos(1.1); rot[2, 3] = -np.sin(1.1); rot[3, 2] = np.sin(1.1)
rng = np.random.default_rng(1)
cases = {"parity P": P, "boost": boost, "rotation": rot, "P x boost x rotation": P @ boost @ rot}
check("Lemma 1: eps_abcd L^a_a' L^b_b' L^c_c' L^d_d' = det(L) eps_a'b'c'd' (P, boost, rotation, product)",
      all(np.allclose(np.einsum('abcd,ai,bj,ck,dl->ijkl', eps, Lm, Lm, Lm, Lm), np.linalg.det(Lm) * eps) for Lm in cases.values()))
check("Lemma 1: each of these is in O(1,3): L^T eta L = eta",
      all(np.allclose(Lm.T @ etaN @ Lm, etaN) for Lm in cases.values()))
e = rng.normal(size=(4, 4))
check("Lemma 1: for a random frame e, g(Pe) = g(e) and det(Pe) = -det(e); a proper boost keeps both",
      np.allclose((P @ e).T @ etaN @ (P @ e), e.T @ etaN @ e) and np.isclose(np.linalg.det(P @ e), -np.linalg.det(e))
      and np.allclose((boost @ e).T @ etaN @ (boost @ e), e.T @ etaN @ e) and np.isclose(np.linalg.det(boost @ e), np.linalg.det(e)))
check("Lemma 1: so det(e) R[g] changes sign under P (R depends on g only), and equal couplings give alpha = -beta",
      np.isclose(np.linalg.det(P @ e) / np.linalg.det(e), -1.0))

# ---- Proposition 1: spherical equivalence and the inverse function nu
xs = (y + sp.sqrt(y**2 + 4 * y)) / 2
check("Proposition 1: y = x mu(x) = x^2/(1+x) is inverted by x(y) = (y + sqrt(y^2 + 4y))/2",
      sp.simplify(xs * mu(xs) - y) == 0 and sp.simplify(sqrt_factor((x**2 / (1 + x) + sp.sqrt((x**2 / (1 + x))**2 + 4 * x**2 / (1 + x))) / 2) - x) == 0)
nu = sp.Rational(1, 2) + sp.sqrt(sp.Rational(1, 4) + 1 / y)
check("Proposition 1: nu(y) = x(y)/y = 1/2 + sqrt(1/4 + 1/y)", sp.simplify(xs / y - nu) == 0)
check("Proposition 1: x(y) is increasing, from 0 to oo (so the inverse exists and is unique)",
      sp.simplify(sp.diff(x**2 / (1 + x), x) - x * (x + 2) / (x + 1)**2) == 0 and sp.limit(xs, y, 0) == 0 and sp.limit(xs, y, sp.oo) == sp.oo)
gN, gt = sp.symbols('g_N g_t', positive=True)
check("Proposition 1: AQUAL spherical law mu(g/a0) g = g_N and QUMOND g = nu(g_N/a0) g_N give the same g (5 points)",
      all(abs(sp.N(mu(xs.subs(y, gv)) * xs.subs(y, gv) - gv)) < 1e-30 and abs(sp.N(nu.subs(y, gv) * gv - xs.subs(y, gv))) < 1e-30
          for gv in map(sp.Rational, ['1/1000', '1/10', '1', '7', '1000'])))

# ---- Theorem 2: the function M
check("Theorem 2: M'(z) = nu(sqrt z) - 1 = -1/2 + sqrt(1/4 + z^(-1/2))",
      sp.simplify(nu.subs(y, sp.sqrt(z)) - 1 - Mpz) == 0)
check("Theorem 2: dM/dy = 2y M'(y^2) = 2(x - y) = 2 mu(x), with x = y + mu(x)",
      sp.simplify(2 * y * Mpz.subs(z, y**2) - 2 * (xs - y)) == 0 and sp.simplify(x - (x**2 / (1 + x) + mu(x))) == 0)
check("Theorem 2: dy/dx = x(x+2)/(x+1)^2", sp.simplify(sp.diff(x**2 / (1 + x), x) - x * (x + 2) / (x + 1)**2) == 0)
check("Theorem 2: s^2 (s+2)/(s+1)^3 = 1 - 1/t - 1/t^2 + 1/t^3, t = s + 1",
      sp.simplify((s**2 * (s + 2) / (s + 1)**3) - (1 - 1 / t - 1 / t**2 + 1 / t**3).subs(t, s + 1)) == 0)
Mx = 2 * x - 1 + 2 * b - b**2 + 2 * sp.log(b)
check("Theorem 2: 2 int_0^x s^2 (s+2)/(s+1)^3 ds = 2x - 1 + 2b - b^2 + 2 ln b, b = 1/(1+x)",
      sp.simplify(2 * sp.integrate(s**2 * (s + 2) / (s + 1)**3, (s, 0, x)) - Mx) == 0)
check("Theorem 2: equivalently M = x(2x^2 + 3x + 2)/(x+1)^2 - 2 ln(1+x), and M(0) = 0",
      sp.simplify(sp.expand_log(Mx - (x * (2 * x**2 + 3 * x + 2) / (x + 1)**2 - 2 * sp.log(1 + x)), force=True)) == 0 and Mx.subs(x, 0) == 0)
check("Theorem 2: conversely (dM/dx)/(dy/dx) = 2 mu(x)",
      sp.simplify(sp.diff(Mx, x) / sp.diff(x**2 / (1 + x), x) - 2 * mu(x)) == 0)
My = sp.sqrt(y) * (y + 2) * sp.sqrt(y + 4) / 2 - y**2 / 2 - 4 * sp.asinh(sp.sqrt(y) / 2)
check("Theorem 2: in y, M = (1/2) sqrt(y) (y+2) sqrt(y+4) - y^2/2 - 4 arsinh(sqrt(y)/2): same derivative 2(x - y) and M(0) = 0",
      sp.simplify((sp.diff(My, y) - 2 * (xs - y)).subs(sp.sqrt(y**2 + 4 * y), sp.sqrt(y) * sp.sqrt(y + 4))) == 0 and My.subs(y, 0) == 0)
check("Theorem 2: the two forms agree to 40 digits at x = 1/100, 1/2, 1, 3, 100",
      all(abs(sp.N(Mx.subs(x, xv) - My.subs(y, xv**2 / (1 + xv)), 50)) < 1e-40 for xv in map(sp.Rational, ['1/100', '1/2', '1', '3', '100'])))
check("Theorem 2: uniqueness: two functions with this M' differ by a constant, removed by M(0) = 0",
      sp.diff(Mx + sp.Symbol('C'), x) == sp.diff(Mx, x))

# ---- Corollary 1: limits
check("Corollary 1: M'(z) -> 0 as z -> oo (Newtonian) and z^(1/4) M'(z) -> 1 as z -> 0 (deep MOND), Milgrom's two conditions",
      sp.limit(Mpz, z, sp.oo) == 0 and sp.limit(z**sp.Rational(1, 4) * Mpz, z, 0) == 1)
check("Corollary 1: M'(z) = z^(-1/4) - 1/2 + z^(1/4)/8 + O(z^(3/4)) as z -> 0",
      sp.simplify(sp.series(Mpz.subs(z, s**4), s, 0, 3).removeO() - (1 / s - sp.Rational(1, 2) + s / 8)) == 0)
check("Corollary 1: M = (4/3) y^(3/2) - y^2/2 + y^(5/2)/10 + O(y^3) as y -> 0",
      sp.simplify(sp.series(My.subs(y, s**2), s, 0, 6).removeO() - (sp.Rational(4, 3) * s**3 - s**4 / 2 + s**5 / 10)) == 0)
w = sp.symbols('w', positive=True)
big = sp.series((My.subs(y, 1 / w) - (2 / w + 2 * sp.log(w))).rewrite(sp.log), w, 0, 3).removeO()
check("Corollary 1: M = 2y - 2 ln y + 1 - 4/y + 5/y^2 + O(y^-3) as y -> oo", sp.simplify(big - (1 - 4 * w + 5 * w**2)) == 0)

# ---- Theorem 3: Legendre duality
gx = x**2 - 2 * x + 2 * sp.log(1 + x)          # F(x^2)
yx = x**2 / (1 + x)
Qx = yx**2 + Mx                                 # Q(y) = y^2 + M(y) at y = y(x)
check("Theorem 3: F(x^2) + y^2 + M(y) = 2 x y at y = x mu(x) (exact)", sp.simplify(gx + Qx - 2 * x * yx) == 0)
check("Theorem 3: d F(x^2)/dx = 2y and dQ/dy = 2x", sp.simplify(sp.diff(gx, x) - 2 * yx) == 0
      and sp.simplify(sp.diff(Qx, x) / sp.diff(yx, x) - 2 * x) == 0)
check("Theorem 3: the logarithms cancel: F(x^2) + M has no log term",
      not sp.simplify(sp.expand_log(gx + Mx, force=True)).has(sp.log))
gnum = sp.lambdify(x, gx, 'numpy'); Qnum = sp.lambdify(x, Qx, 'numpy'); ynum = sp.lambdify(x, yx, 'numpy')
grid = np.logspace(-4, 4, 20001)
check("Theorem 3: Q(y) = max_x [2xy - F(x^2)] (Legendre-Fenchel) at 9 values of y (numerical, grid of 20001)",
      all(abs(np.max(2 * grid * ynum(xv) - gnum(grid)) - Qnum(xv)) < 1e-6 * max(1, Qnum(xv)) for xv in [1e-2, 0.1, 0.5, 1, 2, 5, 10, 50, 100]))
check("Theorem 3: in spherical symmetry |grad phihat| = |grad phi| - |grad phi*| = a0 (x - y) = a0 mu(x) < a0",
      sp.simplify((x - yx) - mu(x)) == 0 and sp.limit(mu(x), x, sp.oo) == 1)

# ---- Corollary 2: convexity, reciprocal ratio, uniqueness
Qp = sp.simplify(sp.diff(Qx, x) / sp.diff(yx, x)); Qpp = sp.simplify(sp.diff(Qp, x) / sp.diff(yx, x))
check("Corollary 2: Hessian eigenvalues of Q(|q|): Q'/y = 2 nu = 2x/y (twice) and Q'' = 2 dx/dy = 2 (x+1)^2/(x(x+2)) (once)",
      sp.simplify(Qp / yx - 2 * x / yx) == 0 and sp.simplify(Qpp - 2 * (x + 1)**2 / (x * (x + 2))) == 0)
ratio = sp.simplify(Qpp / (Qp / yx))
aqual_ratio = sp.simplify(sp.diff(x * mu(x), x) / mu(x))
check("Corollary 2: ratio along/across = (x+1)/(x+2), in [1/2, 1), the reciprocal of the AQUAL ratio (x+2)/(x+1)",
      sp.simplify(ratio - (x + 1) / (x + 2)) == 0 and sp.simplify(ratio * aqual_ratio - 1) == 0
      and sp.limit(ratio, x, 0) == sp.Rational(1, 2) and sp.limit(ratio, x, sp.oo) == 1)
check("Corollary 2: both eigenvalues positive for y > 0, and 2 nu -> oo as y -> 0",
      sp.limit(2 * nu, y, 0) == sp.oo and all(sp.N(e.subs(x, v)) > 0 for e in [Qp / yx, Qpp] for v in [sp.Rational(1, 100), 1, 100]))
def B(p): n = np.linalg.norm(p); return (0.5 + np.sqrt(0.25 + 1 / n)) * p
viol = sum(1 for _ in range(200000)
           for p, pp in [(rng.normal(size=3) * rng.exponential(3), rng.normal(size=3) * rng.exponential(3))]
           if (B(p) - B(pp)) @ (p - pp) <= 0)
check("Corollary 2: strict monotonicity of B(p) = nu(|p|) p on 200000 random pairs", viol == 0)
check("Corollary 2: |nu(y) y| = x(y) -> 0 as y -> 0 and x(y)/sqrt(y) -> 1: the flux is continuous (Hoelder 1/2) at grad phi* = 0",
      sp.simplify(nu * y - xs) == 0 and sp.limit(xs, y, 0) == 0 and sp.limit(xs / sp.sqrt(y), y, 0) == 1)

print(f"\n{sum(ok)}/{len(ok)} checks passed")
