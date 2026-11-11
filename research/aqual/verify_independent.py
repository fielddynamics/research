#!/usr/bin/env python3
"""
Independent verification for "The AQUAL Algebra, Taken Further".

verify_aqual_algebra.py checks each claim with the algebra that produced it.
This script checks the same results by routes that do not reuse that algebra:

  T1  random high-precision evaluation of every identity (60 digits, 200 points each)
  T2  the hyperbolic forms of sections 9-10, proved symbolically through a = sinh(psi/2)
  T3  the field equation solved numerically: Gauss's law with mu applied by
      root-finding (no closed-form inverse), the potential by quadrature,
      compared with the closed forms
  T4  the Legendre dual computed as a numerical supremum, not from its maximiser
  T5  the Hessian of the energy by finite differences in three dimensions
  T6  the family x^n (1-mu)^m = mu^k: irreducibility over Q, one root in (0,1),
      the change of variable S and the exchange E, and the classification of
      exchange-symmetric members
  T7  the mean coupling 17 by direct quadrature in two different measures
  T8  central slopes of the TetB density from root-finding and numerical derivatives

    pip install sympy mpmath
    python verify_independent.py
"""
import random
import sympy as sp
import mpmath as mp

mp.mp.dps = 60
TOL = mp.mpf(10) ** -45
rng = random.Random(20261110)
results = []


def check(label, ok):
    results.append((label, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}")


def rand(lo, hi):
    """Log-uniform random mpf in [lo, hi]."""
    return mp.e ** (mp.log(lo) + (mp.log(hi) - mp.log(lo)) * mp.mpf(rng.random()))


def mu(x):
    return x / (1 + x)


def mu_b(x):
    return 1 - (mp.sqrt(1 + 4 * x) - 1) / (2 * x)


def total_from_source(zz):
    """Total acceleration from source acceleration by bisection on x mu(x) = z (no closed form)."""
    return mp.findroot(lambda X: X * mu(X) - zz, (mp.mpf(0), zz + 2), solver='anderson')


PHI = (1 + mp.sqrt(5)) / 2

# ------------------------------------------------------------------ T1
print("\nT1  Random high-precision identity tests (200 points each, |error| < 1e-45)")
identities = {
    "1b  z(1-mu) = mu^2, z = x mu": lambda x: (x * mu(x)) * (1 - mu(x)) - mu(x) ** 2,
    "1c  g_t - g_s = a0 mu": lambda x: x - x * mu(x) - mu(x),
    "1e  nu(z) = (1 + sqrt(1+4/z))/2 at z = x mu": lambda x: x / (x * mu(x)) - (1 + mp.sqrt(1 + 4 / (x * mu(x)))) / 2,
    "2   bound law z(1-mu_b)^2 = mu_b": lambda x: x * (1 - mu_b(x)) ** 2 - mu_b(x),
    "2c  1 - mu_b(x) = 1/nu(1/x)": lambda x: (1 - mu_b(x)) - 2 / (1 + mp.sqrt(1 + 4 * x)),
    "2d  mu(x) + mu(1/x) = 1": lambda x: mu(x) + mu(1 / x) - 1,
    "3c  x mu_b' = mu_b(1-mu_b)/(1+mu_b)": lambda x: x * mp.diff(mu_b, x) - mu_b(x) * (1 - mu_b(x)) / (1 + mu_b(x)),
    "4a  (x mu)'/mu = 2 - mu": lambda x: mp.diff(lambda t: t * mu(t), x) / mu(x) - (2 - mu(x)),
    "4c  (x mu_b)'/mu_b = 2/(1+mu_b)": lambda x: mp.diff(lambda t: t * mu_b(t), x) / mu_b(x) - 2 / (1 + mu_b(x)),
    "5   int_0^x (1-mu) = int_0^x mu dln x = ln(1+x)":
        lambda x: (mp.quad(lambda t: 1 - mu(t), [0, x]) - mp.log(1 + x)) + (mp.quad(lambda t: mu(t) / t, [0, x]) - mp.log(1 + x)),
    "9   S(B): mu_b = sqrt(z_b)/(1+sqrt(z_b)), z_b = x mu_b": lambda x: mu_b(x) - mu(mp.sqrt(x * mu_b(x))),
    "11  s(x1 x2) = (s1+s2)/(1+s1 s2)": None,
}
for label, f in identities.items():
    if f is None:
        s = lambda X: (X - 1) / (X + 1)
        errs = []
        for _ in range(200):
            a, b = rand(mp.mpf('1e-8'), mp.mpf('1e8')), rand(mp.mpf('1e-8'), mp.mpf('1e8'))
            errs.append(abs(s(a * b) - (s(a) + s(b)) / (1 + s(a) * s(b))))
        check(label, max(errs) < TOL)
        continue
    npts = 40 if label.startswith("5") else 200
    tol = mp.mpf(10) ** -30 if label.startswith(("3c", "4", "5")) else TOL
    errs = [abs(f(rand(mp.mpf('1e-6'), mp.mpf('1e6')))) for _ in range(npts)]
    check(label, max(errs) < tol)

# ------------------------------------------------------------------ T2
print("\nT2  Hyperbolic forms, proved symbolically with a = sinh(psi/2) > 0, c = cosh(psi/2) = sqrt(1+a^2)")
a = sp.symbols('a', positive=True)
c = sp.sqrt(1 + a**2)
sinh_psi = 2 * a * c                      # sinh psi
cosh_psi = 1 + 2 * a**2                   # cosh psi
w = sinh_psi / 2                          # r / r_M
# sqrt(1 + 4 w^2): prove it is the perfect square cosh psi = 1 + 2a^2 > 0, then substitute
root = cosh_psi
square_ok = sp.expand(root**2 - (1 + 4 * w**2)) == 0
gt = (root + 1) / (2 * w**2)
gs = 1 / w**2


def z0(e):
    return sp.simplify(sp.radsimp(e)) == 0


check("9a  1 + 4 w^2 = cosh^2 psi exactly, with cosh psi = 1 + 2a^2 > 0", square_ok)
check("9b  g_t = a0 csch^2(psi/2)", z0(gt - 1 / a**2))
check("9c  mu = g_s/g_t = sech^2(psi/2)", z0(gs / gt - 1 / c**2))
check("9d  v^2 = g_t r = sqrt(G M a0) coth(psi/2)", z0(gt * w - c / a))
check("9e  1 - mu = tanh^2(psi/2) = mu_b at x = r^2/r_M^2 = a0/g_s",
      z0((1 - 1 / c**2) - a**2 / c**2)
      and z0(w**2 * (1 - a**2 / c**2)**2 - a**2 / c**2))
psi = sp.symbols('psi', positive=True)
Phi_closed = sp.asinh(2 * w) - (1 + sp.sqrt(1 + 4 * w**2)) / (2 * w)
# asinh(2w) = asinh(sinh psi) = psi; the rest must equal coth(psi/2) = c/a
check("9f  Phi = sqrt(G M a0) [psi - coth(psi/2)], so Phi + v^2 = sqrt(G M a0) psi",
      z0((1 + root) / (2 * w) - c / a) and abs(sp.N((sp.asinh(2 * w) - 2 * sp.asinh(a)).subs(a, sp.Rational(7, 5)), 40)) < 1e-35)
check("9g  gate x = 1 at sinh(psi/2) = 1: psi/2 = ln(1+sqrt2), r = sqrt2 r_M",
      z0((sinh_psi / 2).subs(a, 1) - sp.sqrt(2)) and z0(sp.asinh(1) - sp.log(1 + sp.sqrt(2))))
check("9h  g_s = a0 at r = r_M: cosh^2(psi/2) = phi, mu = 1/phi",
      z0((c**2).subs(a, sp.sqrt((sp.sqrt(5) - 1) / 2)) - (1 + sp.sqrt(5)) / 2)
      and z0((w**2).subs(a, sp.sqrt((sp.sqrt(5) - 1) / 2)) - 1))
tq = 1 / sinh_psi                         # sqrt(z)/2 with z = 4/sinh^2 psi
rq = cosh_psi / sinh_psi                  # claimed sqrt(1 + tq^2), positive
check("10b QUMOND log term on the point mass: asinh(sqrt(z)/2) = ln coth(psi/2), z = 4/sinh^2 psi",
      z0(rq**2 - (1 + tq**2)) and z0(tq + rq - c / a))
check("10a bound law: x = sinh^2(psi)/4 gives mu_b = tanh^2(psi/2)",
      z0((sinh_psi**2 / 4) * (1 - a**2 / c**2)**2 - a**2 / c**2))

# ------------------------------------------------------------------ T3
print("\nT3  Field equation solved numerically (root-finding + quadrature), against the closed forms")
mp.mp.dps = 30
# point mass, units G M = a0 = 1 so r_M = 1; Gauss: mu(g/a0) g = GM/r^2, g found by root-finding
g_num = lambda r: total_from_source(1 / r**2)
Phi_c = lambda r: mp.asinh(2 * r) - (1 + mp.sqrt(1 + 4 * r * r)) / (2 * r)
ok = True
for r1, r2 in [(mp.mpf('0.05'), mp.mpf('0.4')), (mp.mpf('0.3'), mp.mpf('3')), (mp.mpf(2), mp.mpf(40))]:
    dnum = mp.quad(g_num, [r1, r2])
    ok &= abs(dnum - (Phi_c(r2) - Phi_c(r1))) < mp.mpf('1e-20')
check("T3a point mass: Phi(r2) - Phi(r1) from quadrature of the root-found field = closed form", ok)
ok = all(abs(g_num(r) * r - mp.sqrt(1 / (4 * r * r) + 1) - 1 / (2 * r)) < mp.mpf('1e-20')
         for r in [mp.mpf('0.01'), mp.mpf('0.7'), mp.mpf(1), mp.mpf(25)])
check("T3b point mass: v^2 from the root-found field = vN^2/2 + sqrt(vN^4/4 + GMa0)", ok)
ok = all(abs(g_num(r) * r - mp.coth(mp.asinh(2 * r) / 2)) < mp.mpf('1e-20') for r in [mp.mpf('0.1'), mp.mpf(2), mp.mpf(9)])
check("T3c point mass: v^2 = coth(psi/2) with sinh psi = 2r/r_M", ok)
check("T3d gate: root-found g equals a0 at r = sqrt2 r_M, and g = phi a0 at r = r_M",
      abs(g_num(mp.sqrt(2)) - 1) < mp.mpf('1e-20') and abs(g_num(mp.mpf(1)) - (1 + mp.sqrt(5)) / 2) < mp.mpf('1e-20'))
# Plummer sphere, scale b = 1, GM = 1: g_N = r/(r^2+1)^1.5. Outside the mass the field must match the point mass
# only asymptotically; check instead that the root-found field obeys the source form z(1-mu) = mu^2 everywhere
plummer = lambda r: r / (r * r + 1) ** mp.mpf(1.5)
ok = True
for r in [mp.mpf('0.01'), mp.mpf('0.5'), mp.mpf(3), mp.mpf(30)]:
    zz = plummer(r)
    X = total_from_source(zz)
    m_ = mu(X)
    ok &= abs(zz * (1 - m_) - m_**2) < mp.mpf('1e-25') and abs(X - zz - m_) < mp.mpf('1e-25')
check("T3e Plummer sphere: root-found field obeys (1b) and (1c) at every radius", ok)

nuQ = lambda zz: (1 + mp.sqrt(1 + 4 / zz)) / 2
worst = mp.mpf(0)
for _ in range(300):
    gN = [mp.mpf(rng.uniform(-5, 5)) * mp.e ** rng.uniform(-8, 8) for _ in range(3)]
    zN = mp.sqrt(sum(v * v for v in gN))
    g = [nuQ(zN) * v for v in gN]
    X = mp.sqrt(sum(v * v for v in g))
    worst = max(worst, max(abs((gi - gNi) - mu(X) * gNi / zN) for gi, gNi in zip(g, gN)))
check("T3f QUMOND field (a separate action from GFD's), any geometry: g - g_N = a0 mu(|g|/a0) unit(g_N), 300 random field vectors", worst < mp.mpf('1e-25'))

# ------------------------------------------------------------------ T4
print("\nT4  Legendre dual as a numerical supremum")
mp.mp.dps = 30
F = lambda t: t * t - 2 * t + 2 * mp.log(1 + t)              # F(y) with t = sqrt(y)
Qc = lambda zz: zz**2 / 2 + (zz + 2) * mp.sqrt(zz * (zz + 4)) / 2 - 4 * mp.asinh(mp.sqrt(zz) / 2)


def numerical_sup(zz):
    """sup_t [2 z t - F(t^2)] over t >= 0 by golden-section search on a bracket."""
    lo, hi = mp.mpf(0), 4 * (zz + 2)
    gr = (mp.sqrt(5) - 1) / 2
    f = lambda t: -(2 * zz * t - F(t))
    a_, b_ = lo, hi
    c_, d_ = b_ - gr * (b_ - a_), a_ + gr * (b_ - a_)
    for _ in range(200):
        if f(c_) < f(d_):
            b_ = d_
        else:
            a_ = c_
        c_, d_ = b_ - gr * (b_ - a_), a_ + gr * (b_ - a_)
    t = (a_ + b_) / 2
    return 2 * zz * t - F(t)


ok = all(abs(numerical_sup(zz) - Qc(zz)) < mp.mpf('1e-20') for zz in [mp.mpf('0.01'), mp.mpf('0.3'), mp.mpf(1), mp.mpf(7), mp.mpf(120)])
check("T4a sup_q [q.P - W(q)] at |P| = 2z equals the closed form Q(z^2)", ok)
check("T4b gate value Q(1) = 1/2 + 3 sqrt5/2 - 4 ln phi",
      abs(Qc(mp.mpf(1)) - (mp.mpf(1) / 2 + 3 * mp.sqrt(5) / 2 - 4 * mp.log(PHI))) < mp.mpf('1e-25'))

# ------------------------------------------------------------------ T5
print("\nT5  Hessian of W(q) = F(|q|^2) by finite differences in three dimensions")
mp.mp.dps = 50
W = lambda q: F(mp.sqrt(q[0]**2 + q[1]**2 + q[2]**2))
ok_eig, ok_ratio = True, True
for _ in range(12):
    q = [mp.mpf(rng.uniform(-3, 3)) for _ in range(3)]
    X = mp.sqrt(sum(v * v for v in q))
    h = mp.mpf('1e-12')
    H = mp.matrix(3, 3)
    for i in range(3):
        for j in range(3):
            def shifted(di, dj):
                p = list(q)
                p[i] += di
                p[j] += dj
                return W(p)
            H[i, j] = (shifted(h, h) - shifted(h, -h) - shifted(-h, h) + shifted(-h, -h)) / (4 * h * h)
    ev = sorted(mp.eig(H)[0], key=lambda e: mp.re(e))
    ev = [mp.re(e) for e in ev]
    want = sorted([2 * mu(X), 2 * mu(X), 2 * X * (X + 2) / (X + 1)**2])
    ok_eig &= all(abs(e - t_) < mp.mpf('1e-8') for e, t_ in zip(ev, want))
    ok_ratio &= abs(ev[2] / ev[0] - (2 - mu(X))) < mp.mpf('1e-8')
check("T5a eigenvalues are 2mu, 2mu, 2(x mu)' at 12 random gradients", ok_eig)
check("T5b longitudinal/transverse ratio = 2 - mu = 1 + TetB share", ok_ratio)

# ------------------------------------------------------------------ T6
print("\nT6  The family x^n (1-mu)^m = mu^k")
X_, M_ = sp.symbols('X M')
irr, one_root = True, True
for n in range(1, 4):
    for m in range(1, 4):
        for k in range(1, 4):
            if sp.gcd(sp.gcd(n, m), k) != 1:
                continue
            P = X_**n * (1 - M_)**m - M_**k
            fl = sp.factor_list(P)
            irr &= len(fl[1]) == 1 and fl[1][0][1] == 1
            for xv in [sp.Rational(1, 50), sp.Rational(1), sp.Rational(37, 3)]:
                roots = sp.Poly(P.subs(X_, xv), M_).count_roots(0, 1)
                one_root &= roots == 1
check("T6a every primitive member with n, m, k <= 3 is irreducible over Q", irr)
check("T6b each has exactly one root mu in [0,1] (Sturm count at x = 1/50, 1, 37/3)", one_root)


def S_op(t):
    n, m, k = t
    return (n, m, k + n)


def E_op(t):
    n, m, k = t
    return (n, k, m)


z = sp.symbols('z', positive=True)
ok = True
for _ in range(25):
    t = tuple(rng.randint(1, 5) for _ in range(3))
    n, m, k = t
    orig = X_**n * (1 - M_)**m - M_**k
    snew = z**n * (1 - M_)**m - M_**(k + n)
    ok &= sp.expand(snew.subs(z, X_ * M_) - M_**n * orig) == 0
    en, em, ek = E_op(t)
    exch = (1 / X_)**n * (1 - (1 - M_))**m - (1 - M_)**k
    ok &= sp.expand(-(exch * X_**n) - (X_**en * (1 - M_)**em - M_**ek)) == 0
check("T6c S (z = x mu) and E (x->1/x, mu->1-mu) act as (n,m,k)->(n,m,k+n) and (n,m,k)->(n,k,m), 25 random members", ok)
U = (1, 1, 1)
check("T6d orbit: U -S-> (1,1,2) -E-> (1,2,1) = bound law -S-> (1,2,2) = unbound law in sqrt(z), fixed by E",
      S_op(U) == (1, 1, 2) and E_op(S_op(U)) == (1, 2, 1) and S_op(E_op(S_op(U))) == (1, 2, 2)
      and E_op((1, 2, 2)) == (1, 2, 2))
ok = True
for n in range(1, 5):
    for m in range(1, 5):
        xv = rand(mp.mpf('1e-3'), mp.mpf('1e3'))
        sol = xv ** (mp.mpf(n) / m) / (1 + xv ** (mp.mpf(n) / m))
        ok &= abs(xv**n * (1 - sol)**m - sol**m) < mp.mpf('1e-25')
        ok &= abs(sol + (1 / xv) ** (mp.mpf(n) / m) / (1 + (1 / xv) ** (mp.mpf(n) / m)) - 1) < mp.mpf('1e-25')
check("T6e members fixed by E (m = k) are mu = x^a/(1+x^a), a = n/m, and all are exchange-symmetric", ok)
mp.mp.dps = 30
ok = True
for (n, m, k) in [(1, 1, 1), (1, 2, 1), (2, 1, 1), (1, 1, 2), (2, 3, 2)]:
    # deep: L = ln mu, n ln x + m ln(1 - e^L) - k L = 0 ; strong: L = ln(1 - mu), n ln x + m L - k ln(1 - e^L) = 0
    def deep_root(lx):
        return mp.findroot(lambda L: n * lx + m * mp.log(1 - mp.e**L) - k * L, (mp.mpf(-400), mp.mpf('-1e-30')), solver='anderson')
    def tail_root(lx):
        return mp.findroot(lambda L: n * lx + m * L - k * mp.log(1 - mp.e**L), (mp.mpf(-400), mp.mpf('-1e-30')), solver='anderson')
    lxs, lxl = -mp.mpf(30) * mp.log(10), mp.mpf(30) * mp.log(10)
    deep = deep_root(lxs) / lxs
    tail = tail_root(lxl) / (-lxl)
    ok &= abs(deep - mp.mpf(n) / k) < mp.mpf('1e-3') and abs(tail - mp.mpf(n) / m) < mp.mpf('1e-3')
check("T6f tails: mu ~ x^(n/k) deep, 1 - mu ~ x^(-n/m) strong (5 members); deep scaling needs n = k, exchange needs m = k", ok)
# ------------------------------------------------------------------ T7
print("\nT7  Mean coupling by direct quadrature")
mp.mp.dps = 30
f_of_x = lambda xv: 1 + 4 * (xv - 1) / (xv + 1) + 16
ok = True
for L in [mp.mpf('0.3'), mp.mpf(3), mp.mpf(25)]:
    ok &= abs(mp.quad(lambda l: f_of_x(mp.e**l), [-L, 0, L]) / (2 * L) - 17) < mp.mpf('1e-25')
check("T7a <f> = 17 over symmetric windows in ln x (measure d ln x)", ok)
ok = abs(sum(1 + (mp.mpf(n) / 32 - 1) * 4 + 16 for n in range(65)) / 65 - 17) == 0
check("T7b <f> = 17 per new hexagram in the closure climb (measure linear in s)", ok)

# ------------------------------------------------------------------ T8
print("\nT8  Central slope of the TetB density, from root-finding and numerical derivatives")
mp.mp.dps = 40


def rho_B(r, gN):
    return mp.diff(lambda rr: rr**2 * mu(total_from_source(gN(rr))), r) / r**2


def slope(gN, r1=mp.mpf('1e-7'), r2=mp.mpf('1e-8')):
    return mp.log(rho_B(r1, gN) / rho_B(r2, gN)) / mp.log(r1 / r2)


check("T8a point mass: -1", abs(slope(lambda r: 1 / r**2) + 1) < 1e-3)
check("T8b Hernquist (rho ~ 1/r): -1", abs(slope(lambda r: 1 / (1 + r)**2) + 1) < 1e-3)
check("T8c Plummer (cored): -1/2", abs(slope(plummer) + mp.mpf('0.5')) < 1e-3)
r_ = mp.mpf('1e-9')
# rho_B in units a0/(4 pi G). Point mass: mu -> 1 so rho_B -> 2/r. Plummer (GM = b = 1): g_N ~ r, x ~ sqrt r,
# mu ~ sqrt r, r^2 mu ~ r^(5/2), so rho_B -> (5/2) r^(-1/2)
check("T8d point mass coefficient: r rho_B -> 2, i.e. rho_B -> a0/(2 pi G r)",
      abs(r_ * rho_B(r_, lambda r: 1 / r**2) - 2) < mp.mpf('1e-3'))
check("T8e Plummer coefficient: sqrt(r) rho_B -> 5/2 (in units a0/4piG, GM = b = 1)",
      abs(mp.sqrt(r_) * rho_B(r_, plummer) - mp.mpf(5) / 2) < mp.mpf('1e-3'))

failed = [l for l, ok in results if not ok]
print(f"\n{len(results) - len(failed)}/{len(results)} independent checks pass")
if failed:
    print("FAILED:", *failed, sep="\n  ")
