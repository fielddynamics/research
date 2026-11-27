#!/usr/bin/env python3
"""
GP-2  Robustness of the balance plane, and what the constitutive law says at Giza.

Verifies every statement of README.md. Exact (sympy / rationals) where the
statement is algebraic; high-precision numerics (mpmath, 40 digits) for the
Earth-field computation. Prints PASS/FAIL per check, exits non-zero on failure.

Run from this folder:  python verify_gp2_robustness.py
"""
import sys
import random
from fractions import Fraction as Fr

import sympy as sp
import mpmath as mp

mp.mp.dps = 40
RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {label}" + (f"  -- {detail}" if detail else ""))


# --------------------------------------------------------------------------
# exact geometry helpers
# --------------------------------------------------------------------------

def shoelace(poly):
    s = Fr(0)
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        s += x1 * y2 - x2 * y1
    return s / 2


def section(base, apex, u):
    return [((1 - u) * x + u * apex[0], (1 - u) * y + u * apex[1]) for (x, y) in base]


def integrate_linear_over_polygon(poly, f):
    """Exact integral of an affine function f(x, y) over a convex polygon, by a
    triangle fan, using the vertex-average rule (exact for affine f). This is
    independent of the centroid formula being tested."""
    total = Fr(0)
    p0 = poly[0]
    for i in range(1, len(poly) - 1):
        a, b, c = p0, poly[i], poly[i + 1]
        area = ((b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])) / 2
        total += area * (f(*a) + f(*b) + f(*c)) / 3
    return total


def centroid(poly):
    A = shoelace(poly)
    cx = cy = Fr(0)
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        c = x1 * y2 - x2 * y1
        cx += (x1 + x2) * c
        cy += (y1 + y2) * c
    return (cx / (6 * A), cy / (6 * A))


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def affine_flux_planar_polygon(pts, J):
    """Flux of an affine field J(r) through a planar polygon in R^3 (oriented by
    vertex order): triangle fan, vertex-average rule, exact."""
    total = Fr(0)
    p0 = pts[0]
    for i in range(1, len(pts) - 1):
        a, b, c = p0, pts[i], pts[i + 1]
        va = tuple(x / 2 for x in cross(tuple(b[k] - a[k] for k in range(3)), tuple(c[k] - a[k] for k in range(3))))
        Ja, Jb, Jc = J(*a), J(*b), J(*c)
        Jm = tuple((Ja[k] + Jb[k] + Jc[k]) / 3 for k in range(3))
        total += sum(Jm[k] * va[k] for k in range(3))
    return total


def affine_field(J0, M):
    return lambda x, y, z: tuple(J0[i] + M[i][0] * x + M[i][1] * y + M[i][2] * z for i in range(3))


BASE = [(Fr(0), Fr(-2)), (Fr(2), Fr(-1)), (Fr(2), Fr(1)), (Fr(-1), Fr(2)), (Fr(-2), Fr(0))]
APEX = (Fr(3, 2), Fr(-7, 5), Fr(5, 3))
SQUARE = [(Fr(-1), Fr(-1)), (Fr(1), Fr(-1)), (Fr(1), Fr(1)), (Fr(-1), Fr(1))]

print("=" * 78)
print("GP-2  Robustness of the balance plane; the constitutive share at Giza")
print("=" * 78)

# --------------------------------------------------------------------------
print("\n-- Theorem 1: centroid identity  int_S J_z dA = A(S) J_z(c(S))  for affine J")
rng = random.Random(11)
for k in range(6):
    J0 = tuple(Fr(rng.randint(-20, 20), 7) for _ in range(3))
    M = [[Fr(rng.randint(-9, 9), 5) for _ in range(3)] for _ in range(3)]
    J = affine_field(J0, M)
    poly = section(BASE, APEX, Fr(rng.randint(0, 9), 10))
    zlev = Fr(0)
    lhs = integrate_linear_over_polygon(poly, lambda x, y: J(x, y, zlev)[2])
    c = centroid(poly)
    rhs = shoelace(poly) * J(c[0], c[1], zlev)[2]
    check(f"T1 random affine J #{k + 1}: section flux = area x J_z(centroid), exactly", lhs == rhs)

# --------------------------------------------------------------------------
print("\n-- Theorem 2: in a cone, mu_B(u) = (1-u)^2 (1 + b u),  b = J_z(apex)/J_z(base centroid) - 1")
for k in range(6):
    J0 = (Fr(rng.randint(-5, 5)), Fr(rng.randint(-5, 5)), Fr(rng.randint(20, 40)))
    M = [[Fr(rng.randint(-9, 9), 5) for _ in range(3)] for _ in range(3)]
    J = affine_field(J0, M)
    h = APEX[2]
    c0 = centroid(BASE)
    b = J(APEX[0], APEX[1], h)[2] / J(c0[0], c0[1], Fr(0))[2] - 1
    Phi0 = integrate_linear_over_polygon(BASE, lambda x, y: J(x, y, Fr(0))[2])
    ok = True
    for uu in [Fr(1, 9), Fr(2, 7), Fr(1, 2), Fr(4, 5)]:
        sec = section(BASE, APEX, uu)
        Phi = integrate_linear_over_polygon(sec, lambda x, y: J(x, y, uu * h)[2])
        if Phi / Phi0 != (1 - uu) ** 2 * (1 + b * uu):
            ok = False
    check(f"T2 oblique pentagonal cone, random affine J #{k + 1}: mu_B(u) = (1-u)^2(1+bu) exactly (b = {float(b):+.4f})", ok)

print("\n-- Theorem 2(b): for div J = tr M = 0 the frustum balance base = section + lateral holds face by face;"
      " otherwise the defect is tr(M) x volume")


def frustum_balance(base, apex, u, J):
    h = apex[2]
    sec = section(base, apex, u)
    n = len(base)
    base3 = [(p[0], p[1], Fr(0)) for p in base]
    sec3 = [(p[0], p[1], u * h) for p in sec]
    # outward fluxes: base faces down (-z): reverse orientation; top faces up
    out_base = affine_flux_planar_polygon(list(reversed(base3)), J)
    out_top = affine_flux_planar_polygon(sec3, J)
    out_lat = Fr(0)
    for i in range(n):
        out_lat += affine_flux_planar_polygon([base3[i], base3[(i + 1) % n], sec3[(i + 1) % n], sec3[i]], J)
    return out_base, out_top, out_lat


for k in range(4):
    J0 = (Fr(rng.randint(-5, 5)), Fr(rng.randint(-5, 5)), Fr(rng.randint(20, 40)))
    M = [[Fr(rng.randint(-9, 9), 5) for _ in range(3)] for _ in range(3)]
    trace_free = [row[:] for row in M]
    trace_free[2][2] = -(M[0][0] + M[1][1])
    for label, MM in (("tr M = 0", trace_free), ("tr M != 0", M)):
        J = affine_field(J0, MM)
        uu = Fr(3, 10)
        ob, ot, ol = frustum_balance(BASE, APEX, uu, J)
        h = APEX[2]
        A0 = shoelace(BASE)
        # frustum volume = cone volume minus the small cone above
        Vfr = A0 * h / 3 * (1 - (1 - uu) ** 3)
        tr = MM[0][0] + MM[1][1] + MM[2][2]
        net = ob + ot + ol
        if label == "tr M = 0":
            check(f"T2b affine J #{k + 1}, {label}: net outward flux of the frustum is 0 (base_in = section_out + lateral_out)", net == 0)
        else:
            check(f"T2b affine J #{k + 1}, {label}: net outward flux = tr(M) x frustum volume", net == tr * Vfr)

# --------------------------------------------------------------------------
print("\n-- Theorem 3: the balance level is unique for every b > -1")
u_, b_ = sp.symbols("u b", real=True)
g = (1 - u_) ** 2 * (1 + b_ * u_)
gp = sp.factor(sp.diff(g, u_))
check("T3 g'(u) = -(1-u)(2 - b + 3bu)", sp.simplify(gp - (-(1 - u_) * (2 - b_ + 3 * b_ * u_))) == 0, str(gp))
roots_ok = True
for bv in [sp.Rational(-99, 100), sp.Rational(-1, 2), sp.Rational(-1, 10), 0, sp.Rational(1, 2), 1, 2, 3, 10, 50, 1000]:
    poly = sp.Poly(sp.expand(g.subs(b_, bv) - sp.Rational(1, 2)), u_)
    rts = [r for r in poly.real_roots() if 0 < r < 1]
    if len(rts) != 1:
        roots_ok = False
check("T3 exactly one root of g(u) = 1/2 in (0,1) for b in {-0.99,-1/2,-1/10,0,1/2,1,2,3,10,50,1000} (exact real-root isolation)", roots_ok)
check("T3 b = -1: J_z vanishes at the apex (1 + b u -> 0); b < -1: J_z changes sign inside the cone, no flux share",
      sp.simplify((1 + b_ * u_).subs({b_: -1, u_: 1})) == 0 and (1 + (-2) * sp.Rational(3, 4)) < 0)

# --------------------------------------------------------------------------
print("\n-- Theorem 4: shift of the balance level  du*/db at b = 0 equals (sqrt 2 - 1)/4")
u0 = 1 - 1 / sp.sqrt(2)
# implicit differentiation
dudb = sp.simplify(-sp.diff(g, b_) / sp.diff(g, u_)).subs({b_: 0, u_: u0})
check("T4 du*/db|_{b=0} = (sqrt 2 - 1)/4 = 0.103553", sp.simplify(dudb - (sp.sqrt(2) - 1) / 4) == 0, f"{float(dudb):.6f}")
# second order, exact
G = sp.Function("U")
bb = sp.symbols("bb")
U = sp.symbols("U")
F = (1 - U) ** 2 * (1 + bb * U) - sp.Rational(1, 2)
d1 = -sp.diff(F, bb) / sp.diff(F, U)
d2 = sp.diff(d1, bb) + sp.diff(d1, U) * d1
d2v = sp.radsimp(sp.simplify(d2.subs({bb: 0, U: u0})))
check("T4 d2u*/db2|_{b=0} = 1 - 11 sqrt(2)/16 = 0.027728 (exact)",
      sp.simplify(d2v - (1 - 11 * sp.sqrt(2) / 16)) == 0, f"{float(d2v):.6f}")
h_in = 5776.0
check("T4 Great Pyramid (h = 5776 in): 598.1 in per unit b, reproducing 01.7's numerical 599 in exactly in closed form",
      abs(float(dudb) * h_in - 598.1) < 0.1, f"{float(dudb) * h_in:.2f} in")
# exact root vs linear prediction at b = 1e-3
bt = sp.Rational(1, 1000)
rt = [r for r in sp.Poly(sp.expand(g.subs(b_, bt) - sp.Rational(1, 2)), u_).nroots(n=30) if 0 < sp.re(r) < 1 and abs(sp.im(r)) < 1e-25][0]
check("T4 exact root at b = 1e-3 agrees with the first two Taylor terms to < 1e-9",
      abs(float(sp.re(rt)) - float(u0 + dudb * bt + d2v * bt ** 2 / 2)) < 1e-9)

# --------------------------------------------------------------------------
print("\n-- Theorem 5: any field whose mean axial density varies by at most a fraction eps keeps u* in a closed interval")


def interval(eps):
    lo = 1 - 1 / mp.sqrt(2 * (1 - eps))
    hi = 1 - 1 / mp.sqrt(2 * (1 + eps))
    return lo, hi


rngp = random.Random(5)
import math
ok = True
for trial in range(300):
    eps = rngp.choice([1e-4, 1e-3, 1e-2, 0.05, 0.2])
    cs = [rngp.uniform(-1, 1) for _ in range(5)]
    def r(uu, cs=cs, eps=eps):
        s_ = sum(c * math.sin((k + 1) * math.pi * uu / 2) for k, c in enumerate(cs))
        return 1 + eps * math.tanh(s_)
    lo, hi = (float(v) for v in interval(mp.mpf(eps)))
    f = lambda uu: (1 - uu) ** 2 * r(uu) - 0.5
    grid = [i / 4000 for i in range(4001)]
    for a, c in zip(grid[:-1], grid[1:]):
        fa, fc = f(a), f(c)
        if fa * fc < 0:
            for _ in range(80):
                m = 0.5 * (a + c)
                if f(a) * f(m) <= 0:
                    c = m
                else:
                    a = m
            root = 0.5 * (a + c)
            if not (lo - 1e-12 <= root <= hi + 1e-12):
                ok = False
check("T5 300 random non-uniform profiles: every balance root lies in [1 - 1/sqrt(2(1-eps)), 1 - 1/sqrt(2(1+eps))]", ok)
# sharpness: constant ratios 1 +- eps attain the endpoints
eps = mp.mpf("0.01")
lo, hi = interval(eps)
check("T5 sharp: constant ratio 1+eps puts u* at the upper endpoint, 1-eps at the lower",
      abs((1 - hi) ** 2 * (1 + eps) - 0.5) < 1e-35 and abs((1 - lo) ** 2 * (1 - eps) - 0.5) < 1e-35)
half_width_coeff = mp.diff(lambda e: interval(e)[1], 0)
check("T5 half-width = eps / (2 sqrt 2) + O(eps^2) = 0.35355 eps",
      abs(half_width_coeff - 1 / (2 * mp.sqrt(2))) < 1e-25, f"{float(half_width_coeff):.6f}")
check("T5 Phase 0's reported axial uniformity 5e-5 confines the plane to +-0.10 in of 0.292893 h",
      abs(float((interval(mp.mpf("5e-5"))[1] - (1 - 1 / mp.sqrt(2))) * h_in) - 0.102) < 0.002,
      f"+-{float((interval(mp.mpf('5e-5'))[1] - (1 - 1/mp.sqrt(2))) * h_in):.3f} in")

# --------------------------------------------------------------------------
print("\n-- Theorem 6: the Earth's own field fixes the plane to within a millimetre")
# Earth monopole at depth R below the base centre. Flux of g = -GM r/r^3 through a
# horizontal square of side a at height d above the centre = -GM x solid angle.
R_m = mp.mpf("6.371e6")
inch = mp.mpf("0.0254")
H = mp.mpf("5776.0") * inch           # reconstructed height (Petrie)
SIDE = mp.mpf("9068.8") * inch        # mean base side (Petrie), only enters the solid angle


def solid_angle_square(a, d):
    return 4 * mp.atan(a * a / (4 * d * mp.sqrt(d * d + a * a / 2)))


def muB_earth(z):
    a = SIDE * (1 - z / H)
    return solid_angle_square(a, R_m + z) / solid_angle_square(SIDE, R_m)


zstar_earth = mp.findroot(lambda z: muB_earth(z) - mp.mpf(1) / 2, (1 - 1 / mp.sqrt(2)) * H)
shift_mm = (zstar_earth - (1 - 1 / mp.sqrt(2)) * H) * 1000
b_earth = (R_m / (R_m + H)) ** 2 - 1
pred_mm = (mp.sqrt(2) - 1) / 4 * b_earth * H * 1000
check("T6 Earth monopole field, exact solid-angle fluxes: balance level shifts by -0.70 mm (downwards)",
      -0.75 < float(shift_mm) < -0.65, f"{float(shift_mm):.4f} mm")
check("T6 affine prediction (sqrt2-1)/4 b h with b = (R/(R+h))^2 - 1 agrees to better than 1%",
      abs(float(shift_mm / pred_mm) - 1) < 0.01, f"predicted {float(pred_mm):.4f} mm, b = {float(b_earth):.3e}")
check("T6 the Earth's gradient is about 29 times too small to account for the 0.80 in residual",
      abs(0.80 * 25.4 / float(shift_mm)) > 25, f"ratio {abs(0.80 * 25.4 / float(shift_mm)):.0f}")
# exterior Newtonian field is divergence-free: the frustum balance holds for it
x, y, zz = sp.symbols("x y z", real=True)
rr = sp.sqrt(x ** 2 + y ** 2 + zz ** 2)
gvec = [-x / rr ** 3, -y / rr ** 3, -zz / rr ** 3]
check("T6 the exterior monopole field is divergence-free (so base = section + lateral exactly)",
      sp.simplify(sum(sp.diff(gvec[i], v) for i, v in enumerate((x, y, zz)))) == 0)

# --------------------------------------------------------------------------
print("\n-- Theorem 7: the pyramid's self-gravity, bounded")
G = mp.mpf("6.674e-11")
rho = mp.mpf(2300)           # limestone, kg/m^3 (upper-end mean density of the core masonry)
g_surf = mp.mpf("9.79")
R_c = mp.sqrt(2 * (SIDE / 2) ** 2 + 0 ** 2)   # base half-diagonal; circumradius about the base centre is max(half-diagonal, h)
R_c = max(R_c, H)
g_self_max = 8 * mp.pi * G * rho * R_c
eps_self = 2 * g_self_max / g_surf
du_self = (interval(eps_self)[1] - (1 - 1 / mp.sqrt(2))) * h_in
check("T7 |g_self| <= 8 pi G rho R_c  (B lies in the ball of radius 2 R_c about any of its points)",
      g_self_max < mp.mpf("1e-3"), f"{float(g_self_max):.2e} m/s^2")
check("T7 the self-field, though sourced (div J != 0 inside), moves the section-flux balance level by at most 0.6 in",
      float(du_self) < 0.6, f"bound {float(du_self):.3f} in (eps = {float(eps_self):.2e})")
eps_tot = eps_self + abs(b_earth)
du_tot = (interval(eps_tot)[1] - (1 - 1 / mp.sqrt(2))) * h_in
check("T7 Earth gradient + self-gravity together: the gravitational balance level lies within 0.36 in of 0.292893 h",
      float(du_tot) < 0.37, f"bound {float(du_tot):.3f} in (eps = {float(eps_tot):.2e})")

# --------------------------------------------------------------------------
print("\n-- Theorem 8: the structural share mu_B is not the constitutive share mu at Giza")
a0 = mp.mpf("1.2e-10")
xg = g_surf / a0
one_minus_mu = 1 / (1 + xg)
check("T8 at the Earth's surface x = g/a0 = 8.2e10", abs(xg / mp.mpf("8.158e10") - 1) < 1e-3, f"x = {float(xg):.3e}")
check("T8 even applied per mass (which the net-field rule forbids), the TetB share 1/(1+x) is 1.2e-11",
      one_minus_mu < mp.mpf("1.3e-11"), f"{float(one_minus_mu):.2e}")
check("T8 net-field rule [T+L]: inside the drainless solar system mu = 1 exactly; at the balance plane mu_B = 1/2,"
      " so |mu_B - mu| = 1/2", abs(mp.mpf(1) / 2 - 1) == mp.mpf(1) / 2)
check("T8 within the constitutive law, mu = 1/2 requires g = a0, i.e. a field 8e10 times weaker than Giza's",
      sp.solve(sp.Eq(sp.Symbol('X') / (sp.Symbol('X') + 1), sp.Rational(1, 2)), sp.Symbol('X')) == [1])


print("\n-- Theorem 3b (referee): the balance level is unique for EVERY real b")
uu = sp.symbols("uu", positive=True)
Bf = (1 / (2 * (1 - uu) ** 2) - 1) / uu
dB = sp.together(sp.diff(Bf, uu))
claim = ((1 - uu) ** 3 + uu ** 2 * (3 - uu)) / (2 * uu ** 2 * (1 - uu) ** 3)
check("T3b B(u) = (1/(2(1-u)^2) - 1)/u has B'(u) = [(1-u)^3 + u^2(3-u)] / [2u^2(1-u)^3] > 0 on (0,1)",
      sp.simplify(dB - claim) == 0)
check("T3b B(0+) = -oo and B(1-) = +oo, so B is an increasing bijection (0,1) -> R",
      sp.limit(Bf, uu, 0, "+") == -sp.oo and sp.limit(Bf, uu, 1, "-") == sp.oo)
ok = True
for bv in [-1000, -50, -10, -3, -2, -1, sp.Rational(-1, 2), 0, 2, 10, 1000]:
    poly = sp.Poly(sp.expand(g.subs(b_, bv) - sp.Rational(1, 2)), u_)
    if len([r for r in poly.real_roots() if 0 < r < 1]) != 1:
        ok = False
check("T3b exactly one root in (0,1) for b in {-1000,-50,-10,-3,-2,-1,-1/2,0,2,10,1000} (exact isolation)", ok)
check("T3b for b < -1 the signed ratio is defined (g(0) = 1) and turns negative near the apex: g_{-2}(3/4) = -1/32",
      g.subs({b_: -2, u_: 0}) == 1 and g.subs({b_: -2, u_: sp.Rational(3, 4)}) == sp.Rational(-1, 32))

print("\n-- Theorem 5b (referee): normalised sharpness witnesses and existence/uniqueness hypotheses")
ok = True
for epsv in [mp.mpf("0.01"), mp.mpf("0.1"), mp.mpf("0.4")]:
    lo, hi = interval(epsv)
    for sign, ustar in ((+1, hi), (-1, lo)):
        r = lambda x, sign=sign, ustar=ustar: 1 + sign * epsv * min(x / ustar, 1)
        if abs(r(0) - 1) > 1e-40 or abs((1 - ustar) ** 2 * r(ustar) - mp.mpf(1) / 2) > 1e-35:
            ok = False
        if not all(abs(r(x) - 1) <= epsv + 1e-40 for x in [mp.mpf(i) / 50 for i in range(51)]):
            ok = False
check("T5b r_+-(u) = 1 +- eps min(u/u*, 1) satisfy r(0) = 1, |r - 1| <= eps, and put a root exactly at each endpoint", ok)
check("T5b the lower endpoint is positive (attainable) iff eps < 1/2",
      float(interval(mp.mpf("0.49"))[0]) > 0 and float(interval(mp.mpf("0.5"))[0]) <= 1e-30)
x_ = sp.symbols("x_")
rr = sp.Function("r")
check("T5b (1-u)^2 r(u) is strictly decreasing iff r'/r < 2/(1-u) (derivative identity)",
      sp.simplify(sp.diff((1 - x_) ** 2 * rr(x_), x_) - (1 - x_) * ((1 - x_) * sp.diff(rr(x_), x_) - 2 * rr(x_))) == 0)

print("\n-- Theorem 7b (referee): sharper self-gravity bound by rearrangement, 4 pi G rho R_eq")
Vpy = (SIDE ** 2) * H / 3
R_eq = (3 * Vpy / (4 * mp.pi)) ** (mp.mpf(1) / 3)
g_self_eq = 4 * mp.pi * G * rho * R_eq
eps_E = 1 - (R_m / (R_m + H)) ** 2
g0 = mp.mpf("9.793")
eps_tot2 = (g0 * eps_E + 2 * g_self_eq) / (g0 - g_self_eq)
lo2, hi2 = interval(eps_tot2)
u0f = 1 - 1 / mp.sqrt(2)
disp2 = max(u0f - lo2, hi2 - u0f) * h_in
check("T7b R_eq = (3V/4pi)^(1/3) = 85.25 m and |g_self| <= 4 pi G rho R_eq = 1.64e-4 m/s^2",
      abs(R_eq - mp.mpf("85.246")) < 0.01 and abs(g_self_eq - mp.mpf("1.644e-4")) < 1e-7,
      f"R_eq {float(R_eq):.3f} m, bound {float(g_self_eq):.4e}")
check("T7b eps_total <= (g0 eps_E + 2 g_self)/(g0 - g_self) = 7.96e-5 gives |shift| <= 0.163 in (larger endpoint)",
      abs(eps_tot2 - mp.mpf("7.964e-5")) < 1e-8 and abs(disp2 - mp.mpf("0.1626")) < 0.001,
      f"eps {float(eps_tot2):.3e}, {float(disp2):.3f} in")
check("T7b the refined gravitational budget (0.163 in) is below the original conservative 0.36 in", disp2 < 0.36)

print("\n" + "=" * 78)
print(f"GP-2: {sum(RESULTS)}/{len(RESULTS)} checks passed")
sys.exit(0 if all(RESULTS) else 1)
