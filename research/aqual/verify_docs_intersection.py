#!/usr/bin/env python3
"""
Verification for docs_and_the_energy_functional.md.

Checks every statement the note makes about what the documentation derives
from the AQUAL energy functional F(y) = y - 2 sqrt y + 2 ln(1 + sqrt y):
where the docs agree with the research/aqual work, where they do not, and
the identities that connect the two.

    pip install sympy mpmath
    python verify_docs_intersection.py
"""
import sympy as sp
import mpmath as mp

mp.mp.dps = 40
results = []


def check(label, ok):
    results.append((label, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}")


def zero(e):
    return sp.simplify(e) == 0


x, y, z, g, a0, G, M, r, v = sp.symbols('x y z g a0 G M r v', positive=True)
u = sp.sqrt(y)
F = y - 2 * u + 2 * sp.log(1 + u)
mu = x / (1 + x)

print("\nA. Where the docs and the AQUAL work agree")
check("A1 dF/dy = mu(sqrt y): the round trip (docs 06, site test)", zero(sp.diff(F, y) - u / (1 + u)))
check("A2 F(0) = 0 and F >= 0 (F = int_0^y mu, mu >= 0)", F.subs(y, 0) == 0
      and all(sp.N(F.subs(y, t)) > 0 for t in [sp.Rational(1, 10**6), 1, 10**4]))
check("A3 F'' = 1/(2 sqrt y (1 + sqrt y)^2) (site test formula)", zero(sp.diff(F, y, 2) - 1 / (2 * u * (1 + u)**2)))
# docs 03: mu(g/a0) g = GM/r^2 with g = v^2/r  <=>  v^4 = GM (g + a0)
lhs = (g / a0) / (1 + g / a0) * g - G * M / r**2
check("A4 docs 03: v^4 = GM(g + a0) is the spherical field equation, with v^2 = g r",
      zero(sp.numer(sp.together(lhs.subs(G * M, (g * r)**2 / (r**2 * (g + a0)) * r**2)))))
psi = sp.symbols('psi', positive=True)
check("A5 in the hyperbolic variable of the note (9): g + a0 = a0 coth^2(psi/2), so v^4 = GMa0 coth^2(psi/2)",
      zero((1 / sp.sinh(psi / 2)**2 + 1) - sp.cosh(psi / 2)**2 / sp.sinh(psi / 2)**2))
Mdec = r * v**4 / (G * (a0 * r + v**2))
gt = v**2 / r
check("A6 decode M_dec = r v^4/[G(a0 r + v^2)] = (r^2/G)(g_t - a0 mu): total field minus its TetB share",
      zero(Mdec - r**2 / G * (gt - a0 * (gt / a0) / (1 + gt / a0))))
check("A7 deep field: M_dec -> v^4/(G a0), slope 4 in log M vs log v (BTFR)",
      zero(sp.limit(Mdec * G * a0 / v**4, r, sp.oo) - 1))

print("\nB. Docs statements the algebra does not support")
mp.mp.dps = 50
yv = mp.mpf('1e-6')
t1, t2, t3 = yv, -2 * mp.sqrt(yv), 2 * mp.log(1 + mp.sqrt(yv))
Fv = t1 + t2 + t3
check("B1 docs 06 'the log term dominates in the deep field': at y = 1e-6 the log term is 3000x F;"
      " F = (2/3) y^1.5 arises from cancellation of all three",
      abs(t3) / Fv > 2900 and abs(Fv - mp.mpf(2) / 3 * yv**mp.mpf(1.5)) / Fv < 1e-2)
# decode is explicit for any mu: M = r^2 g mu(g/a0)/G. Standard mu:
std = lambda X: X / mp.sqrt(1 + X**2)
gv, a0v, rv = mp.mpf(3), mp.mpf(1), mp.mpf(2)
check("B2 docs 03 'no other interpolating function gives an exact decode': M = r^2 g mu(g/a0)/G is explicit for every mu",
      abs(rv**2 * gv * std(gv / a0v) - rv**2 * gv**2 / mp.sqrt(a0v**2 + gv**2)) < 1e-40)
xs = sp.sqrt(z * (z + sp.sqrt(z**2 + 4)) / 2)
check("B3 the standard mu = x/sqrt(1+x^2) has an algebraic forward inverse x = sqrt(z(z + sqrt(z^2+4))/2)",
      all(abs(sp.N((xs * xs / sp.sqrt(1 + xs**2) - z).subs(z, zz), 40)) < 1e-35 for zz in [sp.Rational(1, 9), 1, 17]))
check("B4 docs 03 'n family' x/(1+x)^(1/n) exceeds 1 (x = 3, n = 2 gives 1.5); the family is x/(1+x^n)^(1/n)",
      mp.mpf(3) / mp.sqrt(4) > 1 and mp.mpf(3) / mp.sqrt(1 + 9) < 1)
# midpoint mu(1) = 1/2 is a choice of unit: standard mu with a0 -> a0*sqrt(3) passes
std_rescaled = lambda X: std(X / mp.sqrt(3))
check("B5 site uniqueness test: mu(1) = 1/2 is fixed by the unit of a0; the standard mu passes after a0 -> sqrt3 a0",
      abs(std_rescaled(mp.mpf(1)) - mp.mpf(1) / 2) < 1e-40)

print("\nC. Stability and propagation of a covariant F")
pt, px, py, pz = sp.symbols('p_t p_x p_y p_z', real=True)
Xc = -pt**2 + px**2 + py**2 + pz**2          # g^{mu nu} d phi d phi / a0^2, signature (-,+,+,+), c = 1
Fc = lambda Y: Y - 2 * sp.sqrt(Y) + 2 * sp.log(1 + sp.sqrt(Y))
L = -Fc(Xc)
P = [pt, px, py, pz]
g0 = sp.symbols('g0', positive=True)
H = sp.Matrix(4, 4, lambda i, j: sp.diff(L, P[i], P[j])).subs({pt: 0, px: 0, py: 0, pz: g0})
H = sp.simplify(H)
mu0 = g0 / (1 + g0)
check("C1 kinetic coefficient H_tt = 2 mu > 0: no ghost", zero(H[0, 0] - 2 * mu0))
check("C2 gradient coefficients are -2 mu (across) and -2 (x mu)' (along): the note's section 4 eigenvalues",
      zero(H[1, 1] + 2 * mu0) and zero(H[3, 3] + 2 * sp.diff(g0 * mu0, g0)))
c_perp2 = sp.simplify(-H[1, 1] / H[0, 0])
c_par2 = sp.simplify(-H[3, 3] / H[0, 0])
check("C3 waves cross a static field at c and travel along it at c sqrt(2 - mu)",
      zero(c_perp2 - 1) and zero(c_par2 - (2 - mu0)))
check("C4 along-gradient speed lies in [c, sqrt2 c): above c wherever mu < 1 (any x), approaching sqrt2 c as x -> 0",
      all(1 < sp.N(c_par2.subs(g0, t)) < 2 for t in [sp.Rational(1, 1000), 1, 1000]))
check("C5 stability conditions F' > 0 and F' + 2yF'' > 0 are the Hessian eigenvalues mu and (x mu)'",
      zero((sp.diff(F, y) + 2 * y * sp.diff(F, y, 2)).subs(y, x**2) - sp.diff(x * mu, x)))
check("C6 F is undefined for timelike gradients (y < 0): sqrt(y) is not real",
      sp.sqrt(sp.Integer(-1)).is_real is False)

print("\nD. The source of the scalar equation")
Phi = sp.Function('Phi')
R_ = sp.symbols('R', positive=True)
rho = sp.Function('rho')
# radial reduction of the scalar Lagrangian density, with and without -rho Phi
Lfield = -(a0**2 / (8 * sp.pi * G)) * Fc(sp.diff(Phi(R_), R_)**2 / a0**2) * R_**2
for with_source in (True, False):
    Lr = Lfield - (rho(R_) * Phi(R_) * R_**2 if with_source else 0)
    eq = sp.euler_equations(Lr, Phi(R_), R_)[0].lhs
    gp = sp.diff(Phi(R_), R_)
    target = (1 / (4 * sp.pi * G)) * sp.diff(R_**2 * (gp / a0) / (1 + gp / a0) * gp, R_) - (rho(R_) * R_**2 if with_source else 0)
    # compare after substituting a positive test profile
    test = {Phi(R_): R_**2 / 3 + R_}
    e1 = sp.simplify(eq.subs(test).doit())
    e2 = sp.simplify(target.subs(test).doit())
    if with_source:
        okA = zero(e1 - e2)
    else:
        okB = zero(e1 - e2) and not e1.has(rho(R_))
check("D1 with -rho Phi: Euler-Lagrange is (1/4piG)(r^2 mu Phi')' - rho r^2 = 0, i.e. div[mu grad Phi] = 4 pi G rho", okA)
check("D2 without any matter-Phi coupling: div[mu grad Phi] = 0, no source", okB)

print("\nE. The acceleration scale")
c = mp.mpf(299792458)
Hs = mp.mpf('70.21') * 1000 / mp.mpf('3.0856775814913673e22')
a_plain = c * Hs / (2 * mp.pi)
a_corr = a_plain * mp.sqrt(4 / mp.pi)
a_tile = 16 * mp.mpf('6.67430e-11') * mp.mpf('9.1093837139e-31') / mp.mpf('2.8179403205e-15')**2
check("E1 a0 = cH/2pi gives 1.086e-10 at H = 70.21 (what_is_gravity.md, read_sweep_synthesis.md)",
      abs(a_plain - mp.mpf('1.0856e-10')) < mp.mpf('1e-13'))
check("E2 a0 = (cH/2pi) sqrt(4/pi) gives 1.225e-10 (docs H0 page), matching 16 G m_e/r_e^2 (Paper VII) to 1 part in 1e4",
      abs(a_corr / a_tile - 1) < mp.mpf('1e-4'))
check("E3 the two relations differ by sqrt(4/pi) = 1.128", abs(a_corr / a_plain - mp.sqrt(4 / mp.pi)) < 1e-30)

failed = [l for l, ok in results if not ok]
print(f"\n{len(results) - len(failed)}/{len(results)} checks pass")
if failed:
    print("FAILED:", *failed, sep="\n  ")
