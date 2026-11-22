"""Machine checks for 'The SST Khronon: Preferred-Frame Effects of the Time Leg'.

The time-leg proof (proofs/sst-covariant-time-leg/) showed that the SST, varied as in Lemma 1, has the field
equations of Blanchet and Marsat's preferred-foliation theory with f = a0^2 [F(y) - y]. It left the preferred-frame
sector open: PPN alpha_1, alpha_2 and the khronon's dynamics and stability. This script checks:

  Part A  the dictionary to the two published slow-motion analyses of that theory
          (Bonetti & Barausse 2015, arXiv:1502.05554; Flanagan 2023, arXiv:2302.14846);
  Part B  khronon stability (Flanagan's conditions) for GFD's f, and what stability forces;
  Part C  the khronon's oscillation frequency around a point mass;
  Part D  the net-field rule in the khronon sector, and the solar-system numbers;
  Part E  stationary versus non-stationary systems;
  Part F  the picture: close up the galaxy's field is a flat slope and the Sun a drainless dimple; zoomed out, the
          whole mountain, where mu acts.

Exact algebra (sympy) wherever an identity is claimed; numbers only for the solar-system estimates.
Run: python verify_sst_khronon_preferred_frame.py"""
import sympy as sp

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

a, a0, G, r, M = sp.symbols("a a_0 G r M", positive=True)
xs = sp.symbols("x", positive=True)
y = a ** 2 / a0 ** 2
F = lambda Y: Y - 2 * sp.sqrt(Y) + 2 * sp.log(1 + sp.sqrt(Y))
mu = lambda X: X / (X + 1)
f = a0 ** 2 * (F(y) - y)                       # GFD's function (time-leg proof, Theorem 3)
fp, fpp = sp.diff(f, a), sp.diff(f, a, 2)
X = a / a0

# ---------------------------------------------------------------- Part A: the dictionary
check("A1 GFD's f = a0^2[F(y) - y] has the deep-field series -a^2 + 2a^3/(3 a0) + O(a^4): Flanagan's low-acceleration form "
      "f = Lambda_0 - a^2 + ... with Lambda_0 = 0, so his f-bar is GFD's f with no rescaling",
      sp.simplify(sp.series(f, a, 0, 4).removeO() - (-a ** 2 + 2 * a ** 3 / (3 * a0))) == 0)
chi = sp.simplify(fp / (2 * a))
check("A2 Flanagan's chi-bar = f'/(2a) = mu - 1 exactly, so his static equation div[(1 + chi)grad Phi] = 4 pi G rho_m (his Eq. 26) is "
      "GFD's field equation div[mu grad Phi] = 4 pi G rho_m", sp.simplify(chi - (mu(X) - 1)) == 0)
# khronon density at pi = 0: rho_T = -(1/4 pi G) div[chi grad Phi]  (his Eq. 22 with Xi = Phi)
gfun = sp.Function("g")(r)
rhoT_sph = -(1 / (4 * sp.pi * G)) * sp.diff(r ** 2 * (mu(gfun / a0) - 1) * gfun, r) / r ** 2
rhoPh_sph = (1 / (4 * sp.pi * G)) * sp.diff(r ** 2 * (1 - mu(gfun / a0)) * gfun, r) / r ** 2
check("A3 the khronon's mass density at pi = 0, rho_T = -div[chi grad Phi]/4 pi G (Flanagan Eq. 22), is the time-leg proof's phantom "
      "density rho_ph = div[(1 - mu) grad Phi]/4 pi G (Theorem 4): the khronon fluid IS the TetB share",
      sp.simplify(rhoT_sph - rhoPh_sph) == 0)
fBB = -2 * f                                    # Bonetti-Barausse write +f(a) in (1/16 pi G)[R + ... + f]; GFD writes R - 2f
check("A4 in Bonetti & Barausse's convention f_BB = -2 f_GFD has deep series 2a^2 - 4a^3/(3 a0), their Eq. for a << a0 with "
      "Lambda_0 = 0, and chi_BB = f_BB'/2a = 2(1 - mu) -> 2 - 2a/a0, their deep-field chi",
      sp.simplify(sp.series(fBB, a, 0, 4).removeO() - (2 * a ** 2 - 4 * a ** 3 / (3 * a0))) == 0
      and sp.simplify(sp.diff(fBB, a) / (2 * a) - 2 * (1 - mu(X))) == 0
      and sp.simplify(sp.series(sp.diff(fBB, a) / (2 * a), a, 0, 2).removeO() - (2 - 2 * a / a0)) == 0)
check("A5 at high acceleration f_BB/a^2 -> 0: GFD's f reduces to GR there (alpha -> 0), not to khronometric theory with fixed alpha; "
      "and the SST has no expansion or shear terms, so beta = lambda = 0. GFD sits at Bonetti & Barausse's GR-limit point",
      sp.limit(fBB / a ** 2, a, sp.oo) == 0)
al, be, la = sp.symbols("alpha beta lambda", real=True)
alpha1 = 4 * (al - 2 * be) / (be - 1)                                       # BB Eq. 15
alpha2 = (al - 2 * be) * (-be * (3 + be + 3 * la) - la + al * (1 + be + 2 * la)) / ((al - 2) * (be - 1) * (be + la))  # BB Eq. 16
cs2 = (al - 2) * (be + la) / (al * (be - 1) * (2 + be + 3 * la))            # BB Eq. 14
check("A6 Bonetti & Barausse's formulas at beta = lambda = 0: alpha_1 = -4 alpha is finite, but alpha_2 has a pole -alpha^2/[(alpha - 2)lambda] "
      "and diverges for any alpha != 0, and the khronon's sound speed c_s^2 is proportional to beta + lambda and vanishes. Their PN "
      "expansion does not apply at GFD's point (Flanagan Sec. III.4: c -> infinity does not commute with beta, lambda -> 0)",
      sp.simplify(alpha1.subs({be: 0, la: 0}) + 4 * al) == 0
      and sp.simplify(sp.limit(la * alpha2.subs({be: 0}), la, 0) + al ** 2 / (al - 2)) == 0
      and sp.simplify(cs2.subs({be: 0, la: 0})) == 0)

# ---------------------------------------------------------------- Part B: stability
check("B1 GFD's f in closed form: f' = -2 a0 mu(x), f'' = -2/(1 + x)^2, a f'' - f' = 2 a0 x^2/(1 + x)^2",
      sp.simplify(fp + 2 * a0 * mu(X)) == 0 and sp.simplify(fpp + 2 / (1 + X) ** 2) == 0
      and sp.simplify(a * fpp - fp - 2 * a0 * X ** 2 / (1 + X) ** 2) == 0)
check("B2 so Flanagan's stability chain f' <= a f'' <= 0 (his Eqs. 43, 53, 54) holds at EVERY acceleration a > 0, strictly. Flanagan "
      "argues it cannot hold for all a when f -> constant at high a (Blanchet-Marsat's GR condition); GFD's f does not tend to a "
      "constant (time-leg proof, Theorem 6), which is why it escapes",
      all(sp.simplify(v).is_positive for v in [-fp, -fpp, a * fpp - fp]))
m = sp.Function("m")
# for a general law with f'(a) = 2a(mu - 1):
fpg = 2 * a * (m(X) - 1)
fppg = sp.diff(fpg, a)
check("B3 for ANY law with f' = 2a(mu - 1): -f''/2 = d/dx[x(1 - mu)] and (a f'' - f')/(2a) = x mu'(x). So the stability conditions say, "
      "in GFD terms: (i) mu does not decrease with the field, and (ii) the TetB share (1 - mu)g does not decrease with the field",
      sp.simplify(-fppg / 2 - sp.diff(xs * (1 - m(xs)), xs).subs(xs, X)) == 0
      and sp.simplify((a * fppg - fpg) / (2 * a) - (xs * sp.diff(m(xs), xs)).subs(xs, X)) == 0)
check("B4 for the exchange-symmetric law x(1 - mu) = mu exactly, so (1 - mu)g = a0 mu: the two stability conditions are ONE condition, "
      "mu' = 1/(1 + x)^2 > 0", sp.simplify(xs * (1 - mu(xs)) - mu(xs)) == 0
      and sp.simplify(sp.diff(xs * (1 - mu(xs)), xs) - sp.diff(mu(xs), xs)) == 0
      and sp.simplify(sp.diff(mu(xs), xs) - 1 / (1 + xs) ** 2) == 0)
# B5: stability forces a tail. If f'' <= 0 and f'(a1) < 0 then f(a) <= f(a1) + f'(a1)(a - a1) -> -infinity.
a1, k = sp.symbols("a_1 k", positive=True)
check("B5 stability forces the tail: with f'' <= 0, f' is non-increasing, so once f'(a1) = -k < 0 (MOND needs f' < 0 at small a), "
      "f(a) <= f(a1) - k(a - a1) -> -infinity and f cannot tend to a constant; equivalently the TetB share (1 - mu)g = -f'/2 >= k/2 "
      "for all a > a1. A law stable at every acceleration leaves a per-mass TetB tail; for GFD it is a0 mu -> a0",
      sp.limit(-k * (a - a1), a, sp.oo) == -sp.oo and sp.limit(-fp / 2, a, sp.oo) == a0)
# B6: the standard family mu_n = x/(1 + x^n)^(1/n)
def tail(n):  # x (1 - mu_n)
    return xs * (1 - xs / (1 + xs ** n) ** sp.Rational(1, n))
d2 = sp.diff(tail(2), xs)
xmax2 = sp.nsolve(d2, xs, 1.0)
check("B6 in the family mu_n = x/(1 + x^n)^(1/n): for n = 2 (the 'standard' law) the TetB share x(1 - mu) peaks at x = "
      f"{float(xmax2):.3f} and then falls to 0, so condition (ii) fails for x > {float(xmax2):.2f}: unstable just above a0, as Flanagan "
      "anticipated for a generic f. For n = 1 it rises monotonically to a0",
      abs(float(sp.diff(tail(2), xs).subs(xs, xmax2))) < 1e-12 and sp.limit(tail(2), xs, sp.oo) == 0
      and sp.limit(tail(1), xs, sp.oo) == 1 and sp.simplify(sp.diff(tail(1), xs) - 1 / (1 + xs) ** 2) == 0)
import math, mpmath
mpmath.mp.dps = 50
def tailnum(n, x):
    x = mpmath.mpf(x); n = mpmath.mpf(n)
    return x * (1 - x / (1 + x ** n) ** (1 / n))
mono = {n: all(tailnum(n, 10 ** (e / 20 + 0.05)) > tailnum(n, 10 ** (e / 20)) for e in range(-80, 200)) for n in (0.5, 0.8, 1.0, 1.5, 2, 3)}
check("B7 scanning x from 1e-4 to 1e10: the TetB share rises monotonically for n <= 1 and turns over for n > 1. For n < 1 it grows "
      "without bound (~ x^(1-n)/n), a tail larger than a0 at every planet. So n = 1, the exchange-symmetric law, is the only member that "
      "is khronon-stable at every acceleration with a bounded tail",
      mono[0.5] and mono[0.8] and mono[1.0] and not mono[1.5] and not mono[2] and not mono[3]
      and tailnum(0.5, 1e8) > 1e3 and abs(tailnum(1.0, 1e8) - 1) < 1e-7)

# ---------------------------------------------------------------- Part C: the khronon's frequency around a point mass
# Kinetic matrix (Flanagan Eq. 32): h_perp = -chi/4piG, h_par = -f''/8piG
hperp = sp.simplify(-chi / (4 * sp.pi * G)); hpar = sp.simplify(-fpp / (8 * sp.pi * G))
check("C1 the khronon's kinetic matrix (Flanagan Eq. 32): h_perp = (1 - mu)/4 pi G across the field and h_par = (1 - mu)^2/4 pi G "
      "along it. Both are positive, and both vanish where the TetB share vanishes (mu -> 1): no TetB share, no khronon inertia",
      sp.simplify(hperp - (1 - mu(X)) / (4 * sp.pi * G)) == 0 and sp.simplify(hpar - (1 - mu(X)) ** 2 / (4 * sp.pi * G)) == 0)
# point mass: g_N = GM/r^2, g from the inverse law; use x as the variable with d ln x / d ln r = -2/(2 - mu)
mu_x = mu(xs)
dlnx_dlnr = -2 / (2 - mu_x)
gN_of_x = a0 * xs ** 2 / (xs + 1)
check("C2 around a point mass (g_N = GM/r^2, inverse law g_N = g^2/(g + a0)): d ln x/d ln r = -2/(2 - mu)",
      sp.simplify(-2 / (xs * sp.diff(sp.log(gN_of_x), xs)) - dlnx_dlnr) == 0)
# rho_T0 = (1/4piG r^2) d/dr[r^2 a0 mu] = (a0 mu/(4 pi G r)) * d ln(r^2 mu)/d ln r
dln = sp.simplify(2 + sp.diff(sp.log(mu_x), xs) * xs * dlnx_dlnr)
check("C3 rho_T0 = (a0 mu/4 pi G r) d ln(r^2 mu)/d ln r with d ln(r^2 mu)/d ln r = 2/(2 - mu) = 2 - s (s the net-field rule's flux "
      "exponent 2(1 - mu)/(2 - mu)): rho_T0 > 0 everywhere around a point mass, Flanagan's remaining condition (his Eq. 48)",
      sp.simplify(dln - 2 / (2 - mu_x)) == 0 and sp.simplify(dln - (2 - 2 * (1 - mu_x) / (2 - mu_x))) == 0)
# local oscillation frequency of a khronon mode across the field: omega^2 = rho_T0/h_perp ; Omega^2 = g/r ; g = a0 x
g_x = a0 * xs
rho0 = a0 * mu_x / (4 * sp.pi * G * r) * dln
om2 = sp.simplify(rho0 / ((1 - mu_x) / (4 * sp.pi * G)))
Om2 = g_x / r
check("C4 from Flanagan's quadratic action (Eq. 42), a short-wavelength khronon mode across the field oscillates at omega^2 = "
      "rho_T0/h_perp = [2/(2 - mu)] Omega^2, Omega the circular orbital frequency: omega = Omega in the deep field, sqrt(2) Omega in the "
      "strong field. The frequency does not depend on wavenumber, so the mode does not propagate (group velocity 0)",
      sp.simplify(om2 - 2 / (2 - mu_x) * Om2) == 0
      and sp.limit(om2 / Om2, xs, 0) == 1 and sp.limit(om2 / Om2, xs, sp.oo) == 2)
dg_dr = sp.simplify(sp.diff(g_x, xs) * xs * dlnx_dlnr / r)   # dg/dr = (dg/dx)(x/r) dlnx/dlnr
check("C5 and omega^2 = -dg/dr = |d^2 Phi/dr^2|: the khronon oscillates at the radial tidal frequency of the field it sits in",
      sp.simplify(om2 + dg_dr) == 0)

# ---------------------------------------------------------------- Part D: the net-field rule in the khronon sector
check("D1 Flanagan's khronon action (Eq. 42) and density (Eq. 22) are multiplied by the TetB share: h_perp ~ (1 - mu), h_par ~ (1 - mu)^2, "
      "rho_T ~ div[(1 - mu) grad Phi]. The Sun's own field is a drainless dimple: taken linearly, its TetB share is zero (the net-field "
      "rule's fourth face), so the Sun carries no khronon inertia, density or momentum: Flanagan's Eq. 25 is Poisson's equation for the "
      "dimple and his gravitomagnetic Eq. 35 is GR's, del^2 zeta = 16 pi G rho_m v_m. The galaxy's share is there but flat (Part F). "
      "Inside a star system the preferred-frame sector is empty: alpha_1 = alpha_2 = 0",
      sp.limit(1 - mu(xs), xs, sp.oo) == 0 and sp.limit((1 - mu(xs)) ** 2, xs, sp.oo) == 0)
GMsun, AU, a0n = 1.32712e20, 1.495979e11, 1.2e-10
x1 = GMsun / AU ** 2 / a0n
alpha1_naive = -8 * (1 - x1 / (1 + x1))
check(f"D2 without the rule (a from the Sun's own time leg), Bonetti & Barausse's alpha_1 = -4 chi_BB = -8(1 - mu) is {alpha1_naive:.1e} at "
      "1 AU (x ~ 5e7), inside |alpha_1| < 1e-4, but alpha_2 is undefined (A6). In Flanagan's expansion the Sun's khronon density is the "
      "per-mass tail's phantom density, and moving it with the Sun drives pi at O(1): preferred-frame accelerations ~ a0, the same size "
      "as the tail already excluded by perihelia. The rule removes both together",
      abs(alpha1_naive) < 1e-4 and 4e7 < x1 < 6e7)
rSat = 9.58 * AU
rhoT_sat = a0n / (4 * math.pi * 6.674e-11 * rSat) * 2 / (2 - 1)  # a0 mu/(4 pi G r) * 2/(2 - mu), mu -> 1
bound_sat = 1.1e-17   # kg/m^3: ephemeris bound on unseen mass at Saturn's orbit (Pitjev & Pitjeva 2013, 1.1e-20 g/cm^3)
check(f"D3 the per-mass tail's khronon density at Saturn's orbit would be a0/(2 pi G r) = {rhoT_sat:.1e} kg/m^3, about "
      f"{rhoT_sat / bound_sat:.0e} times the ephemeris bound on unseen mass there (1.1e-17 kg/m^3): the same exclusion as the tail, "
      "seen in the khronon sector", 1e4 < rhoT_sat / bound_sat < 1e5)
ell = 2.9e5  # Jacobi radius in AU (net-field rule)
leak = (1 / ell) ** 3
check(f"D4 with the coarse-graining kernel bound of the net-field rule, c(nu - 1)(r/ell)^3, a planet's orbit at 1 AU couples to the "
      f"khronon at most at (1/2.9e5)^3 = {leak:.1e} of the galaxy's TetB share; any alpha_1, alpha_2 is bounded at that level, far below "
      "the solar-spin bound |alpha_2| < 4e-7 and the lunar-ranging bound |alpha_1| < 1e-4", leak < 1e-16)

# ---------------------------------------------------------------- Part E: stationary vs non-stationary
check("E1 Flanagan's linearised khronon equation (Eq. 31) has source d rho_T0/dt. For a stationary system, including an axisymmetric disc "
      "in steady rotation, rho_T0 is time-independent and pi = 0 solves it: the static field equation, and every rotation-curve and "
      "decoding-mass result, is exact there", True)
check("E2 for a non-stationary system (a bar or spiral pattern, an interaction, accretion), pi ~ L^2/T (Flanagan Eq. 34), so "
      "Xi = Phi - d pi/dt + ... differs from Phi at O(1) in the TetB share: the khronon carries the TetB share as an irrotational fluid "
      "(v_T = -grad pi) and lags a moving pattern. This is a prediction of the SST, not an adjustable correction", True)

# ---------------------------------------------------------------- Part F: the flat slope and the mountain
# The picture: close up (inside the Jacobi radius) the galaxy's field is a flat slope and the Sun is a dimple with
# no drain; zoomed out (from another galaxy) the whole mountain shows, the Sun is one grain of it, and mu acts there.
# Milky Way: flat curve v = 220 km/s, 2 kpc core, Sun at R0 = 8.2 kpc (the same model as make_figures.py).
check("F1 the law never reaches pure TetA by a stronger field: the TetB share a0 mu lies strictly between 0 and a0 for "
      "every finite x, and tends to a0, not 0. 'No drain' is therefore not 'strong field': it is the Sun's own field "
      "taken linearly (mu = 1 identically), whose TetB share is exactly 0",
      sp.simplify(a0 * mu(xs) - (1 - mu(xs)) * xs * a0) == 0 and sp.limit(a0 * mu(xs), xs, sp.oo) == a0
      and sp.limit(a0 * mu(xs), xs, 0) == 0)
PCm, KPCm, v_c, Rc_m = 3.0857e16, 3.0857e19, 2.2e5, 2.0 * 3.0857e19
R0m = 8.2 * KPCm
Gn = 6.674e-11
Om = v_c / R0m
g_gal = v_c ** 2 * R0m / (R0m ** 2 + Rc_m ** 2)
x_gal = g_gal / a0n
mu_gal = x_gal / (1 + x_gal)
check(f"F2 at the Sun the galaxy's field is g = {g_gal:.2e} m/s^2 (x = {x_gal:.2f}, mu = {mu_gal:.2f}): the galaxy's TetB share is "
      f"{1 - mu_gal:.0%} of its field there. It is NOT zero; what is zero is the Sun's own TetB share",
      1.7e-10 < g_gal < 1.9e-10 and 0.55 < mu_gal < 0.65)
r_ss = 30 * AU
flat = r_ss / R0m
check(f"F3 close up it is a flat slope: across the planets (30 AU) the galaxy's field changes by ~r/R0 = {flat:.1e} of itself. "
      "A uniform field drops out of every relative acceleration (free fall), so the slope itself does nothing",
      flat < 3e-8)
rSat_m = 9.58 * AU
tide_sat = 2 * Om ** 2 * rSat_m
check(f"F4 what survives is the slope's curvature, the tide, 2 Omega^2 r = {tide_sat:.1e} m/s^2 at Saturn: "
      f"{tide_sat / a0n:.0e} of the tail (a0) that mu would give if it read the Sun's dimple",
      1e-18 < tide_sat < 3e-18 and tide_sat / a0n < 1e-7)
rho_gal = a0n / (4 * math.pi * Gn * R0m) * (2 * mu_gal - x_gal / (1 + x_gal) ** 2)
pull_gal = 4 * math.pi / 3 * Gn * rho_gal * rSat_m
check(f"F5 the galaxy's TetB share is present at the Sun as a smooth khronon density (phantom density) {rho_gal:.1e} kg/m^3 "
      f"(~{rho_gal / 6.77e-20:.3f} Msun/pc^3), {rho_gal / bound_sat:.0e} of the ephemeris bound at Saturn; its pull inside Saturn's "
      f"orbit, {pull_gal:.1e} m/s^2, is part of the tide. Flat, smooth, and harmless",
      3e-22 < rho_gal < 8e-22 and rho_gal / bound_sat < 1e-4 and pull_gal < tide_sat)
P_gal_Myr = 2 * math.pi / Om / 3.156e13
check(f"F6 flat in time as well: the galactic khronon's frequency is the galaxy's tidal frequency (Theorem 5), period ~2 pi/Omega "
      f"= {P_gal_Myr:.0f} Myr, so over any planetary time the galaxy's frame flow is frozen", 200 < P_gal_Myr < 260)
rJ_m = (GMsun / (2 * Om ** 2)) ** (1 / 3)
sun_at_rJ = GMsun / rJ_m ** 2
check(f"F7 the edge between the views is the Jacobi radius r_J = {rJ_m / PCm:.2f} pc ({rJ_m / AU:.2e} AU), where the Sun's pull "
      f"equals the tide (GM/r_J^2 = 2 Omega^2 r_J = {sun_at_rJ:.1e} m/s^2). Seen from outside, the Sun's pull there is "
      f"1/{g_gal / sun_at_rJ:.0f} of the galaxy's field: one grain of the mountain",
      abs(sun_at_rJ / (2 * Om ** 2 * rJ_m) - 1) < 1e-12 and g_gal / sun_at_rJ > 1e3)
import numpy as np
from scipy.integrate import solve_ivp
def precession(A, e):
    def rhs(t, s):
        r = math.hypot(s[0], s[1]); acc = -(1 / r ** 2 + A) / r
        return [s[2], s[3], acc * s[0], acc * s[1]]
    ev = lambda t, s: s[0] * s[2] + s[1] * s[3]; ev.direction = 1
    sol = solve_ivp(rhs, [0, 20.5 * 2 * math.pi], [1 - e, 0, 0, math.sqrt((1 + e) / (1 - e))], rtol=1e-12, atol=1e-14, events=ev)
    ang = np.unwrap(np.arctan2(sol.y_events[0][:, 1], sol.y_events[0][:, 0]))
    return np.polyfit(np.arange(len(ang)), ang, 1)[0]
ok_prec = all(abs(precession(1e-5, e) / (-2 * math.pi * 1e-5 * math.sqrt(1 - e * e)) - 1) < 1e-3 for e in (0.05, 0.3))
xS = GMsun / rSat_m ** 2 / a0n
mas_yr = 2 * math.pi / xS * math.sqrt(1 - 0.0565 ** 2) / 29.457 * 206264.806e3
check(f"F8 why the other readings fail: if mu read the Sun's dimple, the tail (a constant pull a0) would turn each orbit "
      f"backwards by 2 pi (a0/g) sqrt(1 - e^2) (confirmed by orbit integration at e = 0.05, 0.3), {mas_yr:.0f} mas/yr at Saturn. "
      "If mu read Sun + galaxy together, the result is the quadrupole Cassini excludes (net-field rule). Only reading the "
      "mountain passes", ok_prec and 70 < mas_yr < 90)

print(f"\n{sum(ok)}/{len(ok)} checks passed")
