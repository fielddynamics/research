#!/usr/bin/env python3
"""
Verification for "The AQUAL Algebra, Taken Further" (aqual_algebra_further.md).

Every numbered claim in the note is checked here, symbolically with sympy
where an identity is claimed, and numerically with mpmath where an integral,
a limit or a slope is claimed.

    pip install sympy mpmath
    python verify_aqual_algebra.py

Notation: x = g_t/a0 (total), z = g_s/a0 (source), mu = TetA share,
1 - mu = TetB share, phi = (1 + sqrt 5)/2. Units a0 = 1 unless stated.
"""
import sympy as sp
import mpmath as mp

mp.mp.dps = 40
x, z, m, u, s, w, n, M = sp.symbols('x z m u s w n M', positive=True)
mm = sp.symbols('mm', positive=True)
phi = (1 + sp.sqrt(5)) / 2
results = []


def check(label, ok):
    results.append((label, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}")


def zero(e):
    return sp.simplify(e) == 0


mu = x / (1 + x)                                   # unbound law
nu_b = (sp.sqrt(1 + 4 * x) - 1) / (2 * x)          # bound law TetB share
mu_b = 1 - nu_b                                    # bound law TetA share
x_of_z = (z + sp.sqrt(z**2 + 4 * z)) / 2           # total from source (spherical field equation, inverted)
nuQ = (1 + sp.sqrt(1 + 4 / z)) / 2                 # g_t/g_s

print("\n1. One algebra, three forms")
check("1a  x(1-mu) = mu", zero(x * (1 - mu) - mu))
check("1b  source form z(1-mu) = mu^2 with z = x mu", zero((x * mu) * (1 - mu) - mu**2))
check("1c  g_t - g_s = a0 mu (TetB acceleration = a0 x TetA share)", zero(x - x * mu - mu))
check("1d  g_t = (g_s + sqrt(g_s^2 + 4 a0 g_s))/2 solves the spherical field equation g_s = g_t^2/(a0 + g_t)", zero(x_of_z**2 / (1 + x_of_z) - z))
check("1e  nu = g_t/g_s = (1 + sqrt(1 + 4 a0/g_s))/2", zero(x_of_z / z - nuQ))
check("1f  nu(1) = phi, i.e. g_t = phi a0 at g_s = a0", zero(nuQ.subs(z, 1) - phi))
check("1g  mu at g_s = a0 is 1/phi (root of mu^2 + mu - 1)", zero((1 / phi)**2 + 1 / phi - 1))
v2 = x_of_z.subs(z, 1 / w**2) * w                  # a0 = 1, r_M = 1: g_s = 1/w^2, v^2 = g_t r
check("1h  v^2 = vN^2/2 + sqrt(vN^4/4 + GM a0) for a point mass",
      zero(v2 - (1 / (2 * w) + sp.sqrt(1 / (4 * w**2) + 1))))

print("\n2. The bound law is the exchange image of the source form")
src = z * (1 - mm) - mm**2                          # 1b
exch = src.subs({z: 1 / z, mm: 1 - mm}, simultaneous=True) * z
check("2a  (z, mu) -> (1/z, 1-mu) sends z(1-mu) = mu^2 to z(1-mu)^2 = mu",
      zero(sp.expand(exch) - sp.expand(-(z * (1 - mm)**2 - mm))))
check("2b  nu_b solves x nu^2 + nu - 1 = 0 (Paper XIII law)", zero(x * nu_b**2 + nu_b - 1))
check("2c  1 - mu_b(x) = 1/nu(1/x)", zero(nu_b - 1 / nuQ.subs(z, 1 / x)))
check("2d  in total variable the unbound law is self-conjugate: mu(x) + mu(1/x) = 1",
      zero(mu + mu.subs(x, 1 / x) - 1))
check("2e  bound gate: mu_b(1) = 1/phi^2, TetB share 1/phi", zero(mu_b.subs(x, 1) - 1 / phi**2))
ok = True
for A in [4, 56, 208]:
    X = mp.mpf(A)**2
    nb = (mp.sqrt(1 + 4 * X) - 1) / (2 * X)
    ok &= abs(nb - (1 / mp.mpf(A) - 1 / (2 * mp.mpf(A)**2))) < 1 / mp.mpf(A)**3
check("2f  large x: 1 - mu_b(A^2) = 1/A - 1/(2A^2) + O(A^-3), against 1/(1+A^2) unbound", ok)

print("\n3. The logistic family")
P = n * sp.log(x) + m * sp.log(1 - M) - sp.log(M)   # x^n (1-mu)^m = mu
xdm = -sp.diff(P, x) * x / sp.diff(P, M)
check("3a  x mu' = n mu(1-mu)/(1 + (m-1) mu) on x^n(1-mu)^m = mu",
      zero(xdm - n * M * (1 - M) / (1 + (m - 1) * M)))
check("3b  unbound: x mu' = mu(1-mu)", zero(x * sp.diff(mu, x) - mu * (1 - mu)))
check("3c  bound: x mu_b' = mu_b(1-mu_b)/(1+mu_b)", zero(x * sp.diff(mu_b, x) - mu_b * (1 - mu_b) / (1 + mu_b)))
gate = (mu_b * (1 - mu_b) / (1 + mu_b)).subs(x, 1)
check("3d  bound gate slope = 1/(sqrt5 phi^2) = (3 sqrt5 - 5)/10", zero(gate - 1 / (sp.sqrt(5) * phi**2))
      and zero(gate - (3 * sp.sqrt(5) - 5) / 10))

rate = mm * (1 - mm) / (1 + mm)
crit = sp.solve(sp.diff(rate, mm), mm)
check("3e  bound rate peaks at mu = sqrt2 - 1, x = (1+sqrt2)/2, value (sqrt2-1)^2",
      len(crit) == 1 and zero(crit[0] - (sp.sqrt(2) - 1))
      and zero((mm / (1 - mm)**2).subs(mm, crit[0]) - (1 + sp.sqrt(2)) / 2)
      and zero(rate.subs(mm, crit[0]) - (sp.sqrt(2) - 1)**2))

print("\n4. Field-equation anisotropy")
check("4a  unbound (x mu)'/mu = 2 - mu = 1 + TetB share", zero(sp.diff(x * mu, x) / mu - (2 - mu)))
check("4b  matches Theorem 2: (x+2)/(x+1)", zero(sp.diff(x * mu, x) / mu - (x + 2) / (x + 1)))
check("4c  bound (x mu_b)'/mu_b = 2/(1 + mu_b)", zero(sp.diff(x * mu_b, x) / mu_b - 2 / (1 + mu_b)))
fam = 1 + n * M * (1 - M) / (1 + (m - 1) * M) / M
ok = all(fam.subs({n: nn, m: mmv, M: q}) > 1 for nn in [1, 2, 3] for mmv in [1, 2, 3]
         for q in [sp.Rational(1, 100), sp.Rational(1, 2), sp.Rational(99, 100)])
check("4d  family ratio 1 + n(1-mu)/(1+(m-1)mu) > 1: both Hessian eigenvalues positive", ok)

print("\n5. The logarithm is the screening identity integrated")
check("5a  mu/x = 1 - mu", zero(mu / x - (1 - mu)))
check("5b  int_0^u (1-mu) dx = ln(1+u)", zero(sp.integrate(1 / (1 + s), (s, 0, u)) - sp.log(1 + u)))
check("5c  int_0^u mu dln x = ln(1+u)", zero(sp.integrate((s / (1 + s)) / s, (s, 0, u)) - sp.log(1 + u)))
F = u**2 - 2 * u + 2 * sp.log(1 + u)                # F(y) with u = sqrt(y)
check("5d  dF/du = 2u mu(u), so F' (y) = mu(sqrt y)", zero(sp.diff(F, u) - 2 * u * u / (1 + u)))
FB = u**2 - F
check("5e  TetB complement y - F = 2(sqrt y - ln(1 + sqrt y)) = int (1-mu) dy",
      zero(FB - 2 * (u - sp.log(1 + u))) and zero(sp.diff(FB, u) - 2 * u * (1 - u / (1 + u))))
Om = mm / (1 - mm)                                  # odds = x
d5f = F.subs(u, Om) - (Om**2 - 2 * Om - 2 * sp.log(1 - mm))
check("5f  in partition variables F = Om^2 - 2 Om - 2 ln(1 - mu)  (since 1 + Om = 1/(1-mu))",
      zero(1 + Om - 1 / (1 - mm))
      and all(abs(sp.N(d5f.subs(mm, v), 40)) < 1e-35 for v in [sp.Rational(1, 10), sp.Rational(1, 2), sp.Rational(9, 10)]))

print("\n6. Exchange mean of the coupling")
check("6a  f(x) = 1 + s(x) K + K^2 = 13 + 8 mu = (21x + 13)/(x + 1), s = (x-1)/(x+1)",
      zero(1 + (x - 1) / (x + 1) * 4 + 16 - (13 + 8 * mu)) and zero(13 + 8 * mu - (21 * x + 13) / (x + 1)))
ok = True
for L in [mp.mpf('0.5'), 2, 10]:
    a = mp.quad(lambda l: 13 + 8 * mp.e**l / (1 + mp.e**l), [-L, 0, L]) / (2 * L)
    ok &= abs(a - 17) < mp.mpf('1e-30')
check("6b  <f> = 17 over |ln x| <= 0.5, 2, 10 (unbound)", ok)
bvals = []
for L in [mp.mpf('0.5'), 2, 10]:
    nbf = lambda l: (mp.sqrt(1 + 4 * mp.e**l) - 1) / (2 * mp.e**l)
    bvals.append(mp.quad(lambda l: 13 + 8 * (1 - nbf(l)), [-L, 0, L]) / (2 * L))
check("6c  bound law <f> = 16.058, 16.104, 16.605 over the same windows (< 17)",
      all(abs(b - t) < 1e-3 for b, t in zip(bvals, [16.0584, 16.1039, 16.6054])))

print("\n7. Closed forms")
Xs = x_of_z.subs(z, s)
Q = sp.integrate(2 * Xs, (s, 0, z))
Qc = z**2 / 2 + (z + 2) * sp.sqrt(z * (z + 4)) / 2 - 4 * sp.asinh(sp.sqrt(z) / 2)
check("7a  QUMOND kinetic fn: Q(z^2) = z^2/2 + (z+2)sqrt(z(z+4))/2 - 4 asinh(sqrt z/2)",
      zero(sp.diff(Qc, z) - 2 * x_of_z) and Qc.subs(z, 0) == 0)
FF = lambda U: U**2 - 2 * U + 2 * sp.log(1 + U)
Wstar = 2 * z * x_of_z - FF(x_of_z)
check("7b  Q is the Legendre dual of the GFD energy: W*(2z) = Q(z^2)",
      all(abs(sp.N((Wstar - Qc).subs(z, v), 30)) < 1e-25 for v in [sp.Rational(1, 7), 1, 3, 50]))
check("7c  asinh(1/2) = ln phi (the gate value of Q)", abs(mp.asinh(mp.mpf(1) / 2) - mp.log(mp.phi)) < 1e-35)
Fb = u**2 + u - (2 * u / 3 + sp.Rational(1, 6)) * sp.sqrt(1 + 4 * u) + sp.Rational(1, 6)
mub_u = 1 - (sp.sqrt(1 + 4 * u) - 1) / (2 * u)
check("7d  bound kinetic fn F_b(y) = y + sqrt y - (2 sqrt y/3 + 1/6) sqrt(1 + 4 sqrt y) + 1/6",
      zero(sp.diff(Fb, u) - 2 * u * mub_u) and zero(Fb.subs(u, 0)))
check("7e  F_b = (2/3) y^(3/2) - y^2 + ... at small y (same deep limit as F)",
      zero(sp.series(Fb, u, 0, 5).removeO() - (sp.Rational(2, 3) * u**3 - u**4)))
Phi = sp.asinh(2 * w) - (1 + sp.sqrt(1 + 4 * w**2)) / (2 * w)   # units sqrt(G M a0), w = r/r_M
check("7f  point-mass potential: dPhi/dw = g_t", zero(sp.diff(Phi, w) - x_of_z.subs(z, 1 / w**2)))
check("7g  inner limit Phi = -GM/r + a0 r + ...", zero(sp.series(Phi, w, 0, 2).removeO() - (-1 / w + w)))
check("7h  outer limit Phi - sqrt(GM a0)[ln(4 r/r_M) - 1] -> 0",
      sp.limit(Phi.rewrite(sp.log) - sp.log(4 * w) + 1, w, sp.oo) == 0)

print("\n8. Central slope of the TetB density, rho_B = (a0/4piG) r^-2 d(r^2 mu)/dr")
def xt(zz):
    return (zz + mp.sqrt(zz * zz + 4 * zz)) / 2
def rho_B(r, gN):
    return mp.diff(lambda rr: rr**2 * (xt(gN(rr)) / (1 + xt(gN(rr)))), r) / r**2
def slope(gN):
    r1, r2 = mp.mpf('1e-8'), mp.mpf('1e-9')
    return mp.log(rho_B(r1, gN) / rho_B(r2, gN)) / mp.log(r1 / r2)
check("8b  point mass: slope -1", abs(slope(lambda r: 1 / r**2) + 1) < 1e-3)
check("8c  Hernquist baryons (rho ~ 1/r): slope -1", abs(slope(lambda r: 1 / (1 + r)**2) + 1) < 1e-3)
check("8d  cored baryons (g_N ~ r): slope -1/2", abs(slope(lambda r: r) + mp.mpf('0.5')) < 1e-3)

failed = [l for l, ok in results if not ok]
print(f"\n{len(results) - len(failed)}/{len(results)} checks pass")
if failed:
    print("FAILED:", *failed, sep="\n  ")
