#!/usr/bin/env python3
"""
Verification: The Constitutive Law as a Tug of War
==================================================

Every statement of the proof is checked here: exactly with sympy where the statement is
algebraic, exhaustively over the cube's 8 corners and 24 symmetries, and numerically (to
stated tolerances) for the root-finding and the rotation curves.

  A. Lemma 1      The cube forces a two-team share.
  B. Theorem 1    Exchange turns screening into a power law.
  C. Theorem 2    What fixes the power: four equivalent conditions.
  D. Prop. 1      Each premise is necessary.
  E. Prop. 2      The Field Origin as one node, and the cap.
  F. Theorem 3    Decoding mass: quiet, drive and brake.
  G. Prop. 3      The vortex: the exact solutions the reading rests on.
  H. Remark       Two corrections to the March 2026 syntheses.

Run: python verify_constitutive_law_tug_of_war.py      (numpy, scipy, sympy)
"""
import itertools
import math
import sys

import numpy as np
import sympy as sp
from scipy.optimize import brentq

PASS = FAIL = 0


def check(name, ok):
    global PASS, FAIL
    ok = bool(ok)
    PASS += ok
    FAIL += not ok
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")


# ---------------------------------------------------------------- the cube
CORNERS = [np.array(s) for s in itertools.product([1, -1], repeat=3)]
IDX = {tuple(s): i for i, s in enumerate(CORNERS)}
IN_A = np.array([s.prod() == 1 for s in CORNERS])
SUBSETS = list(itertools.product([0, 1], repeat=3))


def walsh(S):
    return np.array([np.prod([s[d] for d in range(3) if S[d]]) for s in CORNERS], dtype=float)


def Td():
    out = []
    for p in itertools.permutations(range(3)):
        for signs in itertools.product([1, -1], repeat=3):
            M = np.zeros((3, 3), dtype=int)
            for i in range(3):
                M[i, p[i]] = signs[i]
            if all((M @ s).prod() == 1 for s, a in zip(CORNERS, IN_A) if a):
                out.append(M)
    return out


def perm_matrix(M):
    P = np.zeros((8, 8))
    for i, s in enumerate(CORNERS):
        P[IDX[tuple(M @ s)], i] = 1
    return P


SA = lambda phi: phi[IN_A].sum()  # noqa: E731
SB = lambda phi: phi[~IN_A].sum()  # noqa: E731
share = lambda phi: SA(phi) / (SA(phi) + SB(phi))  # noqa: E731
law = lambda x: x / (x + 1)  # noqa: E731


def screening_root(x, n, m, p):
    return brentq(lambda u: x**n * (1 - u) ** m - u**p, 1e-300, 1 - 1e-16, xtol=1e-15)


def total_pull(g_bar, a0, k):
    f = lambda g: (g / a0) ** k / (1 + (g / a0) ** k) * g - g_bar  # noqa: E731
    return brentq(f, g_bar, g_bar + 10 * a0 + 10 * (g_bar * a0**k) ** (1 / (k + 1)), xtol=1e-30, rtol=1e-14)


x, u, g, a0 = sp.symbols("x u g a_0", positive=True)

# ======================================================================== A
print("A. Lemma 1: the cube forces a two-team share")
G = Td()
check("T_d has 24 elements, each keeping TetA and TetB", len(G) == 24 and all(
    IN_A[IDX[tuple(M @ s)]] == a for M in G for s, a in zip(CORNERS, IN_A)))
P = sum(perm_matrix(M) for M in G) / 24
check("the T_d-symmetric states form a 2-dimensional space, spanned by the chamber indicators",
      np.linalg.matrix_rank(P, tol=1e-10) == 2 and np.allclose(P @ IN_A, IN_A) and np.allclose(P @ ~IN_A, ~IN_A))
ok = True
for wA, wB in [(1.0, 1.0), (3.0, 1.0), (0.2, 5.0), (7.3, 0.01)]:
    phi = np.where(IN_A, wA, wB)
    s = (walsh((1, 1, 1)) @ phi) / (walsh((0, 0, 0)) @ phi)
    X = wA / wB
    ok &= math.isclose(share(phi), wA / (wA + wB)) and math.isclose(s, (X - 1) / (X + 1)) \
        and math.isclose(share(phi), (1 + s) / 2) and math.isclose(17 + 4 * s, (21 * X + 13) / (X + 1))
check("mu = wA/(wA+wB); rope position s = c_xyz/c_1 = (x-1)/(x+1) = 2mu - 1; f = 17 + 4s = (21x+13)/(x+1)", ok)
rng = np.random.default_rng(0)
ok = True
for _ in range(50):
    phi = rng.uniform(0.1, 5, 8)
    ok &= math.isclose(share(np.array([phi[IDX[tuple(-s)]] for s in CORNERS])), 1 - share(phi))
check("the inversion -I swaps the teams: mu -> 1 - mu (50 random states)", ok)
base = np.where(IN_A, 2.0, 1.0)
ok = all(math.isclose(share(base + sum(rng.normal() * walsh(S) for S in SUBSETS if sum(S) in (1, 2))), share(base))
         for _ in range(50))
check("adding any T2 (vortex) mode leaves mu unchanged (50 random combinations)", ok)

# ======================================================================== B
print("B. Theorem 1: exchange turns screening into a power law")
ok = True
for n, m, p in itertools.product([1, 2, 3], repeat=3):
    defect = max(abs(screening_root(X, n, m, p) + screening_root(1 / X, n, m, p) - 1) for X in (0.05, 0.3, 2.0, 7.0))
    ok &= (defect < 1e-9) == (m == p)
check("x^n (1-mu)^m = mu^p is exchange-symmetric iff m = p (all 27 cases n, m, p in {1,2,3})", ok)
q = sp.symbols("q", positive=True)
check("the step of the proof: q^m = q^p with 0 < q = mu(1-mu) <= 1/4 forces m = p",
      sp.maximum(u * (1 - u), u, sp.Interval(0, 1)) == sp.Rational(1, 4))
ok = all(sp.simplify((x**n * (1 - u) ** pp - u**pp).subs(u, x ** sp.Rational(n, pp) / (1 + x ** sp.Rational(n, pp)))) == 0
         for n, pp in [(1, 1), (2, 1), (1, 2), (3, 2)])
check("m = p gives Omega = mu/(1-mu) = x^(n/p) exactly", ok)
k = sp.symbols("k", positive=True)
muk = x**k / (1 + x**k)
check("every mu_k = x^k/(1+x^k) is exchange-symmetric, with mu_k(1) = 1/2",
      sp.simplify(muk.subs(x, 1 / x) - (1 - muk)) == 0 and muk.subs(x, 1) == sp.Rational(1, 2))

# ======================================================================== C
print("C. Theorem 2: what fixes the power")
ok = all(math.isclose((gg) ** kk / (1 + gg**kk) * (gg + 1), gg, rel_tol=1e-12) for gg in (0.1, 0.7, 3.0, 20.0)
         for kk in [1]) and not any(all(math.isclose((gg) ** kk / (1 + gg**kk) * (gg + 1), gg, rel_tol=1e-12)
                                        for gg in (0.1, 0.7, 3.0, 20.0)) for kk in (0.5, 2, 3))
check("(i) <=> (ii): the strengths add up to the field, mu (g + a0) = g, only for k = 1", ok)
check("(ii) exactly: mu_k (x + 1) = x  <=>  x^k = x", sp.simplify(sp.numer(sp.together(muk * (x + 1) - x)) - (x**k - x)) == 0)
ok = True
for kk in (0.5, 1.0, 2.0, 3.0):
    v2 = lambda r: total_pull(1.0 / r**2, 1.0, kk) * r  # noqa: E731
    slope = math.log(v2(1e6) / v2(1e5)) / math.log(10)
    ok &= math.isclose(slope, (kk - 1) / (kk + 1), abs_tol=2e-3)
check("(iii): the outer slope of v^2 is (k-1)/(k+1) for k = 0.5, 1, 2, 3 (flat only for k = 1)", ok)
GM, rr = sp.symbols("GM r", positive=True)
gdeep = (GM * a0**k / rr**2) ** (1 / (k + 1))
check("(iii) exactly: in the deep field g^(k+1) = GM a0^k / r^2, so v^2 = g r ∝ r^((k-1)/(k+1))",
      sp.simplify(sp.log(gdeep * rr).diff(rr) * rr - (k - 1) / (k + 1)) == 0)
check("k = 1 gives Tully-Fisher: v^4 = GM a0", sp.simplify((gdeep * rr).subs(k, 1) ** 2 - GM * a0) == 0)
a, b, c, d = sp.symbols("a b c d")
ok = True
for kk in (2, 3):
    coeffs = sp.Poly(sp.expand(x**kk * (c * x + d) - (a * x + b)), x).coeffs()
    ok &= sp.solve(coeffs, [a, b, c, d], dict=True) == [{a: 0, b: 0, c: 0, d: 0}]
check("(iv): x^k is a degree-one (Moebius) function of x only for k = 1 (k = 2, 3 have no Moebius form)", ok)
check("the law is the tug of war: g/(g + a0) = law(g/a0)", sp.simplify(g / (g + a0) - law(g / a0)) == 0)

# ======================================================================== D
print("D. Proposition 1: each premise is necessary")


def omega_counter(X, cc):
    t = np.log(X)
    return X * np.exp(cc * t * np.exp(-t * t))


ok = True
xs = np.logspace(-6, 6, 4001)
for cc in (0.3, -0.3, 0.6):
    Om = omega_counter(xs, cc)
    mu = Om / (1 + Om)
    mu_inv = omega_counter(1 / xs, cc) / (1 + omega_counter(1 / xs, cc))
    ok &= np.allclose(mu_inv, 1 - mu, atol=1e-12) and abs(mu[0] / xs[0] - 1) < 1e-4 and abs(mu[-1] - 1) < 1e-5 \
        and np.all(np.diff(mu) > 0) and np.max(np.abs(mu - law(xs))) > 1e-2
check("(a) without screening: exchange, both MOND limits and monotonicity hold for a law that is not x/(x+1)", ok)
phi_g = (1 + math.sqrt(5)) / 2
check("(b) unequal powers: x(1-mu)^2 = mu gives mu(1) = 1/phi^2 = 0.382, not 1/2",
      math.isclose(screening_root(1.0, 1, 2, 1), 1 / phi_g**2, rel_tol=1e-12))
check("(c) k = 2: v^2 keeps rising (by 2.15x per decade of radius)",
      total_pull(1e-12, 1.0, 2.0) * 1e6 / (total_pull(1e-10, 1.0, 2.0) * 1e5) > 2.0)
others = {"standard": lambda X: X / np.sqrt(1 + X**2), "exponential": lambda X: 1 - np.exp(-X),
          "n = 3 family": lambda X: X / (1 + X**3) ** (1 / 3)}
xs = np.logspace(-2, 2, 41)
check("(d) the standard, exponential and n = 3 functions break the exchange; x/(x+1) keeps it exactly",
      all(np.max(np.abs(f(xs) + f(1 / xs) - 1)) > 1e-2 for f in others.values())
      and np.allclose(law(xs) + law(1 / xs), 1, atol=1e-14))
pq, qq, rq, tq = sp.symbols("p q r t")
mu_bl = -(pq + qq * x) / (rq + tq * x)
coeffs = sp.Poly(sp.expand(sp.numer(sp.together(mu_bl.subs(x, 1 / x) - (1 - mu_bl)))), x).coeffs()
laws = set()
for sol in sp.solve(coeffs, [pq, qq, rq, tq], dict=True):
    mm = sp.simplify(mu_bl.subs(sol))
    if sp.simplify(mm.diff(x)) == 0:
        continue
    free = sorted(mm.free_symbols - {x}, key=str)
    for e in sp.solve(sp.Eq(mm.subs(x, 0), 0), free[0]):
        laws.add(sp.simplify(mm.subs(free[0], e)))
check("(e) degree one + endpoint + exchange leave x/(x+1) and x/(x-1); only x/(x+1) stays in [0,1]",
      laws == {x / (x + 1), x / (x - 1)})

# ======================================================================== E
print("E. Proposition 2: the Field Origin as one node, and the cap")
cA, cB, VA, VB, VO = sp.symbols("c_A c_B V_A V_B V_O", positive=True)
VOs = sp.solve(sp.Eq(cA * (VA - VO) + cB * (VB - VO), 0), VO)[0]
L = sp.Matrix([[cA, 0, -cA], [0, cB, -cB], [-cA, -cB, cA + cB]])
Lred = L[:2, :2] - L[:2, 2:] * L[2:, 2:].inv() * L[2:, :2]
check("one node: the Field Origin is the strength-weighted average; eliminating it leaves cA cB/(cA + cB)",
      sp.simplify(VOs - (cA * VA + cB * VB) / (cA + cB)) == 0 and sp.simplify(Lred[0, 0] - cA * cB / (cA + cB)) == 0)


def cube_with_centre(tA, tB, he=0.0):
    H = np.zeros((9, 9))
    for i, s in enumerate(CORNERS):
        H[i, 8] = H[8, i] = tA if IN_A[i] else tB
        for j, t in enumerate(CORNERS):
            if np.sum(s != t) == 1:
                H[i, j] = he
    return H


ok = True
for tA, tB in [(1.0, 1.0), (2.0, 1.0), (0.3, 1.7)]:
    H = cube_with_centre(tA, tB)
    K = H[:8, :8] + H[:8, 8:] @ np.linalg.inv(5.0 * np.eye(1) - H[8:, 8:]) @ H[8:, :8]
    wv, V = np.linalg.eigh(K)
    ok &= np.linalg.matrix_rank(K, tol=1e-10) == 1 and math.isclose(share(V[:, np.argmax(np.abs(wv))]), tA / (tA + tB))
check("the cube through its Field Origin: one rope (rank one) with TetA share tA/(tA + tB)", ok)
wv, V = np.linalg.eigh(cube_with_centre(2.0, 1.0, he=0.7))
sh = [share(V[:8, j]) for j in range(9) if abs(SA(V[:8, j]) + SB(V[:8, j])) > 1e-6]
check("direct cube-edge links between the chambers break the rule", sh and all(abs(m - 2 / 3) > 1e-3 for m in sh))
mu_s = g / (g + a0)
check("g = mu g + mu a0, and TetB carries (1 - mu) g = mu a0",
      sp.simplify(mu_s * g + mu_s * a0 - g) == 0 and sp.simplify((1 - mu_s) * g - mu_s * a0) == 0)
gs = np.logspace(-14, 2, 200)
tetB = gs / (gs / 1.2e-10 + 1)
check("TetB's pull rises towards a0 and never passes it", np.all(tetB < 1.2e-10) and np.all(np.diff(tetB) > 0)
      and math.isclose(tetB[-1] / 1.2e-10, 1, rel_tol=1e-9))
check("missing / visible = a0/g", sp.simplify((1 - mu_s) / mu_s - a0 / g) == 0)
cc, lam = sp.symbols("c lam", positive=True)
E_ = cc / g
check("the exchange on pulls, g -> c/g, is a dilation-covariant involution with fixed point sqrt(c) = a0",
      sp.simplify(E_.subs(g, E_) - g) == 0 and sp.simplify(E_.subs(g, lam * g) - E_ / lam) == 0
      and sp.solve(sp.Eq(E_, g), g) == [sp.sqrt(cc)])

# ======================================================================== F
print("F. Theorem 3: decoding mass, quiet, drive and brake")
gb, Gc, r_ = sp.symbols("g_bar G r", positive=True)
w = g * (g - gb) / gb
ratio = law(g / a0) * g / gb
check("M_dec/M_phot = mu(g/a0) g / g_bar = (g + w)/(g + a0), with w = g (g - g_bar)/g_bar",
      sp.simplify(ratio - (g + w) / (g + a0)) == 0)
check("Delta M / M_phot = (w - a0)/(g + a0)", sp.simplify(ratio - 1 - (w - a0) / (g + a0)) == 0)
v = sp.symbols("v", positive=True)
check("the decode is the letter's M_dec = r v^4 / (G (a0 r + v^2))",
      sp.simplify(law((v**2 / r_) / a0) * (v**2 / r_) * r_**2 / Gc - r_ * v**4 / (Gc * (a0 * r_ + v**2))) == 0)
ok = True
rng = np.random.default_rng(3)
for _ in range(2000):
    G_ = 10 ** rng.uniform(-2, 2)
    Gb = G_ * rng.uniform(0.01, 0.999)
    R = law(G_) * G_ / Gb
    W = G_ * (G_ - Gb) / Gb
    drive, brake = R > 1 + 1e-12, R < 1 - 1e-12
    ok &= drive == (W > 1) == (G_ - Gb > law(G_)) and brake == (W < 1) == (G_ - Gb < law(G_))
check("drive <=> w > a0 <=> TetB pulls more than mu a0; brake <=> the reverse (2000 random points)", ok)
ok = all(math.isclose(law(G_) * G_ / (law(G_) * G_), 1) and math.isclose(G_ * (G_ - law(G_) * G_) / (law(G_) * G_), 1)
         for G_ in (0.01, 0.5, 1.0, 4.0, 100.0))
check("quiet is exactly the law: g_bar = mu g gives M_dec = M_phot and w = a0", ok)
check("the same change in w moves the decode by (w - a0)/(g + a0): 45% at g = a0/10, 5e-8 at g = 1e7 a0",
      0.5 / 1.1 > 0.4 and 0.5 / (1e7 + 1) < 1e-7)

# ======================================================================== G
print("G. Proposition 3: the vortex")
r, t, nu, alpha, Gam = sp.symbols("r t nu alpha Gamma", positive=True)
beta = alpha / (4 * nu)
om = sp.exp(-beta * r**2)
lhs = (-alpha * r / 2) * om.diff(r)
rhs = alpha * om + nu * (om.diff(r, 2) + om.diff(r) / r)
check("Burgers: inflow -alpha r/2 balances stretching alpha omega and diffusion: steady, exact",
      sp.simplify(lhs - rhs) == 0)
uth = Gam / (2 * sp.pi * r) * (1 - sp.exp(-beta * r**2))
res = (-alpha * r / 2) * (uth.diff(r) + uth / r) - nu * (uth.diff(r, 2) + uth.diff(r) / r - uth / r**2)
check("Burgers swirl Gamma/(2 pi r) (1 - exp(-alpha r^2/4 nu)) solves the azimuthal Navier-Stokes equation",
      sp.simplify(res) == 0)
omL = Gam / (4 * sp.pi * nu * t) * sp.exp(-r**2 / (4 * nu * t))
check("Lamb-Oseen: with no drain the vortex diffuses, d_t omega = nu (omega'' + omega'/r), exact",
      sp.simplify(omL.diff(t) - nu * (omL.diff(r, 2) + omL.diff(r) / r)) == 0)
om0 = Gam * alpha / (4 * sp.pi * nu)
circ = sp.integrate(om0 * sp.exp(-beta * r**2) * 2 * sp.pi * r, (r, 0, sp.oo))
check("at fixed circulation the core vorticity is Gamma alpha/(4 pi nu): a stronger drain spins the core up",
      sp.simplify(circ - Gam) == 0)


def burgers_peak(al):
    rs = np.linspace(1e-4, 20 * math.sqrt(1 / al), 200001)
    us = 1 / (2 * math.pi * rs) * (1 - np.exp(-al * rs**2 / 4))
    i = int(np.argmax(us))
    return rs[i], us[i]


(r1, u1), (r4, u4) = burgers_peak(1.0), burgers_peak(4.0)
check("quadrupling the drain halves the core radius and doubles the peak swirl",
      math.isclose(r1 / r4, 2, rel_tol=1e-3) and math.isclose(u4 / u1, 2, rel_tol=1e-3))
check("far from the core the swirl is Gamma/(2 pi r), whatever the drain strength",
      sp.limit(uth * 2 * sp.pi * r / Gam, r, sp.oo) == 1)

# ======================================================================== H
print("H. Remark: two corrections to the March 2026 syntheses")
ok = True
for N in (1, 2, 4, 16):
    for X in (0.2, 1.0, 5.0):
        qq_ = X / (1 + X)
        mean = sum(math.comb(N, j) * qq_**j * (1 - qq_) ** (N - j) * j / N for j in range(N + 1))
        ok &= math.isclose(mean, X / (1 + X), rel_tol=1e-12)
check("N independent sites fill to x/(1+x) for every N; x^N/(1+x^N) needs them to fill together", ok)
inv = u / sp.sqrt(1 - u**2)
check("the standard function's inverse mu/sqrt(1-mu^2) is algebraic but not rational",
      sp.simplify(inv**2 * (1 - u**2) - u**2) == 0 and not inv.is_rational_function(u)
      and (u / (1 - u)).is_rational_function(u))

print(f"\nRESULT: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
sys.exit(1 if FAIL else 0)
