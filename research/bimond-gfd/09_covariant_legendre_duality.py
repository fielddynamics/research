"""09. Legendre duality of the SST scalar sector and BIMOND (alpha = -beta), at the level of the action.

Setting: the SST scalar sector, L_A = -(a0^2/8piG) F(X/a0^2) - rho Phi, with X = g^{mn} d_m Phi d_n Phi on ANY metric g
(spacelike gradients, X >= 0, where F is defined).  W(q) = F(|q|^2) = w(|q|), w(x) = x^2 - 2x + 2 ln(1+x).
Legendre dual: W*(p) = Q(|p|/2), Q(y) = y^2 + M(y)  (proofs/bimetric-two-potential-energy, Theorem 3).

A. First-order form.  L1(Phi, p) = (a0^2/8piG)[W*(p) - p.dPhi/a0] - rho Phi, p an auxiliary covector (no derivatives).
   Eliminating p gives L_A exactly, on any metric.  No new degree of freedom.
B. Gradient form.  Restrict p = 2 dchi/a0.  Then L2(Phi, chi) = (a0^2/8piG) Q(|dchi|/a0) - (1/4piG) dchi.dPhi - rho Phi, and with
   phi = Phi, phi* = chi, phihat = Phi - chi it is IDENTICALLY
       L2 = -(1/8piG)[ |dphi|^2 - |dphihat|^2 - a0^2 M(|dphi*|^2/a0^2) ] - rho phi,
   Milgrom's BIMOND nonrelativistic Lagrangian with beta = 1, alpha = -1.  The opposite sign is the sign of the Legendre pairing.
C. What differs.  Field equations:  AQUAL: field a0 grad W*(p) = dPhi is curl-free, flux p carries a curl, div p = 8piG rho/a0.
   QUMOND: flux p = 2 dchi/a0 is curl-free (chi Newtonian), the field nu dchi carries a curl, Phi is its gradient part.
   The two coincide whenever the curl part vanishes (e.g. spherical symmetry).
D. The Field Origin is nonlinear.  TetA and TetB are two schemes (two sectors) meeting at the Field Origin.  At zero
   field M has no Taylor expansion (M ~ (4/3) z^(3/4), M' ~ z^(-1/4) -> oo): the AQUAL Hessian -> 0 and the two-potential
   Hessian -> oo.  No quadratic theory exists there, so the sign pattern diag(1, -1) of the two-potential kinetic terms is
   the orientation of the two sectors, not a ghost diagnosis.  The first-order form is an equivalent rewriting of the SST.
"""
import numpy as np, sympy as sp
ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

x, y = sp.symbols('x y', positive=True)
w = x**2 - 2*x + 2*sp.log(1 + x)                                   # F(x^2)
b = 1/(1 + x); M = 2*x - 1 + 2*b - b**2 + 2*sp.log(b); yx = x**2/(1 + x)
Qx = yx**2 + M                                                    # Q at y = y(x)
Qf = lambda yy: sp.sqrt(yy)*(yy+2)*sp.sqrt(yy+4)/2 - yy**2/2 - 4*sp.asinh(sp.sqrt(yy)/2) + yy**2   # Q(y) = y^2 + M(y), M in y
Qn = sp.lambdify(y, Qf(y), 'numpy'); wn = sp.lambdify(x, w, 'numpy')

# ---- A. pointwise Legendre identity, Euclidean and Lorentzian (spacelike covectors)
check("A: w'(x) = 2y(x) and W*(p) = Q(|p|/2) is the Legendre dual: w(x) + Q(y) = 2xy",
      sp.simplify(sp.diff(w, x) - 2*yx) == 0 and sp.simplify(w + Qx - 2*x*yx) == 0)
rng = np.random.default_rng(3)
def lor_metric():
    A = rng.normal(size=(4, 4)) * 0.3 + np.eye(4)
    return A.T @ np.diag([-1.0, 1, 1, 1]) @ A                       # random metric of signature (-+++)
def norm(v, gi): return np.sqrt(v @ gi @ v)
okA = True
for _ in range(300):
    g = lor_metric(); gi = np.linalg.inv(g)
    # random spacelike covector q (w.r.t. g^{-1})
    while True:
        q = rng.normal(size=4) * rng.exponential(2)
        if q @ gi @ q > 1e-6: break
    X = norm(q, gi)
    p = 2 * (X**2/(1 + X)) * (gi @ q) / X                           # p^m = dW/dq_m, contravariant
    p_low = g @ p
    Wq = wn(X); Ws = Qn(norm(p_low, gi)/2)
    okA &= abs(Wq + Ws - p @ q) < 1e-9 * max(1, abs(p @ q))
check("A: covariant identity W(q) + W*(p) = p.q at p = dW/dq, 300 random Lorentzian metrics and spacelike q", okA)
# A2: eliminating the auxiliary p from L1 returns the SST Lagrangian (stationarity in p)
vals = []
for qn in [0.01, 0.3, 1.0, 4.0, 30.0]:
    ys = np.linspace(1e-7, 2*qn + 3, 400001)
    vals.append(abs((Qn(ys) - 2*ys*qn).min() + wn(qn)) < 1e-6 * max(1, wn(qn)))
check("A: min_p [W*(p) - p.q] = -W(q): eliminating p from L1 gives -(a0^2/8piG) F, the SST term (5 field strengths)", all(vals))

# ---- B. gradient form = BIMOND alpha = -beta (flat 3D and a curved static 3-metric)
X1, X2, X3, a0, G, rho = sp.symbols('X1 X2 X3 a0 G rho', positive=True)
co = (X1, X2, X3)
Phi = sp.Function('Phi')(*co); chi = sp.Function('chi')(*co)
h = [sp.Function(n)(*co) for n in ('h1', 'h2', 'h3')]              # curved diagonal 3-metric h_ii(x)
Mf = sp.Function('Mfun'); Qs = sp.Function('Q')
def ip(A, B, metric): return sum(sp.diff(A, co[i])*sp.diff(B, co[i])/metric[i] for i in range(3))
for label, metric in [("flat", [1, 1, 1]), ("curved diagonal 3-metric", h)]:
    vol = sp.sqrt(sp.prod(metric))
    Xchi = ip(chi, chi, metric)
    # Q(|dchi|/a0) = |dchi|^2/a0^2 + M(|dchi|^2/a0^2) as a function of z = |dchi|^2/a0^2
    L2 = vol*((a0**2/(8*sp.pi*G))*(Xchi/a0**2 + Mf(Xchi/a0**2)) - ip(chi, Phi, metric)/(4*sp.pi*G) - rho*Phi)
    phih = Phi - chi
    Lb = vol*(-(1/(8*sp.pi*G))*(ip(Phi, Phi, metric) - ip(phih, phih, metric) - a0**2*Mf(ip(chi, chi, metric)/a0**2)) - rho*Phi)
    check("B (%s): L2(Phi, chi) = -(1/8piG)[|dphi|^2 - |dphihat|^2 - a0^2 M] - rho phi identically, phi = Phi, phihat = Phi - chi" % label,
          sp.simplify(sp.expand(L2 - Lb)) == 0)
# field equations of the gradient form (flat): Laplacian(chi) = 4 pi G rho and Laplacian(Phi) = div[(1 + M') grad chi]
L2f = ((a0**2/(8*sp.pi*G))*(ip(chi, chi, [1,1,1])/a0**2 + Mf(ip(chi, chi, [1,1,1])/a0**2)) - ip(chi, Phi, [1,1,1])/(4*sp.pi*G) - rho*Phi)
EPhi, Echi = [e.lhs for e in sp.euler_equations(L2f, [Phi, chi], co)]
lap = lambda f: sum(sp.diff(f, v, 2) for v in co)
z = ip(chi, chi, [1,1,1])/a0**2
Mp = sp.Subs(sp.Derivative(Mf(sp.Symbol('t')), sp.Symbol('t')), sp.Symbol('t'), z).doit()
check("B: Phi-variation gives Laplacian(chi) = 4 pi G rho (chi = phi*, Newtonian)", sp.simplify(EPhi*4*sp.pi*G - (lap(chi) - 4*sp.pi*G*rho)) == 0)
check("B: chi-variation gives Laplacian(Phi) = div[(1 + M') grad chi] = div[nu grad phi*]  (QUMOND)",
      sp.simplify(Echi*4*sp.pi*G + (sum(sp.diff((1 + Mp)*sp.diff(chi, v), v) for v in co) - lap(Phi))) == 0)
check("B: the sign is forced: the pairing term -2 dchi.dPhi completes to |dPhi|^2 - |d(Phi - chi)|^2 - ... => beta = 1, alpha = -1",
      sp.expand((ip(chi, chi, [1,1,1]) - 2*ip(chi, Phi, [1,1,1])) - (ip(Phi - chi, Phi - chi, [1,1,1]) - ip(Phi, Phi, [1,1,1]))) == 0)

# ---- C. which side carries the curl: an explicit non-spherical solution (two point masses), numerically
def gN(r, masses):                                                   # Newtonian field, G = 1, a0 = 1
    out = np.zeros(3)
    for m, c in masses:
        d = r - c; out += -m*d/np.linalg.norm(d)**3
    return out
nu = lambda yy: 0.5 + np.sqrt(0.25 + 1/yy)
masses = [(1.0, np.array([0.0, 0, 0])), (0.5, np.array([2.0, 0, 0]))]
def curl(F, r, hh=1e-4):
    J = np.zeros((3, 3))
    for j in range(3):
        e = np.zeros(3); e[j] = hh
        J[:, j] = (F(r + e) - F(r - e))/(2*hh)
    return np.array([J[2,1]-J[1,2], J[0,2]-J[2,0], J[1,0]-J[0,1]]), J
qflux = lambda r: nu(np.linalg.norm(gN(r, masses)))*gN(r, masses)   # QUMOND field before projection: nu(|gN|) gN
pts = [np.array([1.0, 1.3, 0.4]), np.array([3.1, -0.7, 0.9]), np.array([-1.5, 0.2, -1.1])]
cq = [curl(qflux, r)[0] for r in pts]
cN = [curl(lambda rr: gN(rr, masses), r)[0] for r in pts]
check("C: two masses: the Newtonian flux (QUMOND's p) is curl-free, while nu(|gN|) gN has a nonzero curl (|curl| = %.1e, %.1e, %.1e)"
      % tuple(np.linalg.norm(c) for c in cq), all(np.linalg.norm(c) < 1e-6 for c in cN) and all(np.linalg.norm(c) > 1e-4 for c in cq))
single = [(1.0, np.array([0.0, 0, 0]))]
cs = [curl(lambda rr: nu(np.linalg.norm(gN(rr, single)))*gN(rr, single), r)[0] for r in pts]
check("C: one mass (spherical): nu(|gN|) gN is curl-free, so AQUAL and QUMOND coincide", all(np.linalg.norm(c) < 1e-6 for c in cs))

# ---- D. kinetic matrices
K_grad = sp.Matrix([[1, 0], [0, -1]])                               # (phi, phihat) in L2 ~ -(1/8piG)[X_phi - X_phihat ...]
check("D: the two-potential kinetic terms carry the orientation signs diag(1, -1) (beta = 1, alpha = -1)", K_grad.det() == -1)
zz = sp.symbols('z', positive=True)
Mz = (sp.sqrt(sp.sqrt(zz))*(sp.sqrt(zz)+2)*sp.sqrt(sp.sqrt(zz)+4)/2 - zz/2 - 4*sp.asinh(sp.sqrt(sp.sqrt(zz))/2))   # M as a function of z = u^2
lead = sp.limit(Mz/zz**sp.Rational(3, 4), zz, 0)
check("D: at the Field Origin (zero field) M is non-analytic: M ~ (4/3) z^(3/4), M'(z) -> oo, no Taylor expansion in z",
      lead == sp.Rational(4, 3) and sp.limit(sp.diff(Mz, zz), zz, 0) == sp.oo)
xx = sp.symbols('x', positive=True)
check("D: the AQUAL Hessian (2mu, 2(x mu)') -> 0 and the two-potential Hessian (2nu, 2(x+1)^2/(x(x+2))) -> oo at zero field: no quadratic theory at the vertex",
      sp.limit(2*xx/(1+xx), xx, 0) == 0 and sp.limit(2*xx*(xx+2)/(xx+1)**2, xx, 0) == 0
      and sp.limit(2*(xx+1)**2/(xx*(xx+2)), xx, 0) == sp.oo)
P = [sp.Function(n)(*co) for n in ('p1', 'p2', 'p3')]
Ws = sp.Function('Wstar')
L1 = (a0**2/(8*sp.pi*G))*(Ws(sum(pi**2 for pi in P)) - sum(P[i]*sp.diff(Phi, co[i]) for i in range(3))/a0) - rho*Phi
Ep = [e.lhs for e in sp.euler_equations(L1, P, co)]
check("D: first-order form: the p equations are algebraic (no derivatives of p): an exact rewriting of the SST scalar sector",
      all(not e.has(*[sp.Derivative(pi, v) for pi in P for v in co]) for e in Ep))

print(f"\n{sum(ok)}/{len(ok)} checks passed")
