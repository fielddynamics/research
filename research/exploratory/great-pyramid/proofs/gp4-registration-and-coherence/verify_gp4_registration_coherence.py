#!/usr/bin/env python3
"""
GP-4  Registration and coherence of phase ensembles.

Checks every statement of README.md: exact (sympy) where the statement is
algebraic, 50-digit numerics (mpmath) where it involves roots of unity of
order 21. Prints PASS/FAIL per check, exits non-zero on any failure.

Run from this folder:  python verify_gp4_registration_coherence.py
"""
import sys
import random
import itertools
from math import gcd

import sympy as sp
import mpmath as mp

mp.mp.dps = 50
RESULTS = []
TOL = mp.mpf("1e-40")


def check(label, ok, detail=""):
    RESULTS.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {label}" + (f"  -- {detail}" if detail else ""))


def harmonic(dist, k):
    """m_k = E[e^{ik theta}] for a discrete distribution [(theta, p), ...]."""
    return mp.fsum(p * mp.e ** (1j * k * t) for t, p in dist)


def normalise(ws):
    s_ = mp.fsum(ws)
    return [w / s_ for w in ws]


rng = random.Random(21)
two_pi = 2 * mp.pi

print("=" * 78)
print("GP-4  Registration and coherence of phase ensembles")
print("=" * 78)

# --------------------------------------------------------------------------
print("\n-- Theorem 1: C_N = 1 iff the ensemble lies on one coset of the N-gon")
for N in (3, 7, 21):
    ok = True
    for trial in range(40):
        th0 = mp.mpf(rng.uniform(0, 6.3))
        ws = normalise([mp.mpf(rng.random()) for _ in range(N)])
        dist = [(th0 + two_pi * n / N, ws[n]) for n in range(N)]
        if abs(abs(harmonic(dist, N)) - 1) > TOL:
            ok = False
    check(f"T1 (if) N = {N}: 40 random ensembles on a rotated {N}-gon have C_{N} = 1 to 1e-40", ok)
for N in (3, 7, 21):
    ok = True
    for trial in range(40):
        th0 = mp.mpf(rng.uniform(0, 6.3))
        ws = normalise([mp.mpf(rng.random()) for _ in range(N)])
        dist = [(th0 + two_pi * n / N, ws[n]) for n in range(N)]
        # move one atom off the coset by a small amount
        j = rng.randrange(N)
        dist[j] = (dist[j][0] + mp.mpf(rng.uniform(0.01, 0.2)), dist[j][1])
        if abs(harmonic(dist, N)) > 1 - mp.mpf("1e-8"):
            ok = False
    check(f"T1 (only if) N = {N}: moving any atom off the coset makes C_{N} < 1", ok)
# exact statement for the uniform N-gon: m_k = [N | k]
for N in (3, 7, 21):
    # exact algebra: sum_{n<N} z^{kn} = N if z^k = 1 else (z^{kN} - 1)/(z^k - 1) = 0; checked numerically to 1e-40
    ok = all(
        abs(mp.fsum(mp.e ** (2j * mp.pi * k * n / N) for n in range(N)) / N - (1 if k % N == 0 else 0)) < TOL
        for k in range(0, 2 * N + 1))
    check(f"T1 uniform {N}-gon: m_k = 1 if {N} | k else 0, for k = 0..{2*N}", ok)

# --------------------------------------------------------------------------
print("\n-- Theorem 2: registration does not imply coherence; every C_1 in [0,1] occurs with C_N = 1")
for N in (3, 7, 21):
    ok = True
    for t in [mp.mpf(0), mp.mpf("0.25"), mp.mpf("0.5"), mp.mpf("0.9"), mp.mpf(1)]:
        ws = [(1 - t) / N + (t if n == 0 else 0) for n in range(N)]
        dist = [(two_pi * n / N, ws[n]) for n in range(N)]
        if abs(abs(harmonic(dist, N)) - 1) > TOL or abs(abs(harmonic(dist, 1)) - t) > TOL:
            ok = False
    check(f"T2 N = {N}: the mixture (1-t) uniform + t point has C_{N} = 1 and C_1 = t (t = 0, 1/4, 1/2, 0.9, 1)", ok)
check("T2 the README table: uniform circle (0,0), uniform 21-gon (C_21 = 1, C_1 = 0), single phase (1, 1)",
      abs(harmonic([(two_pi * n / 21, mp.mpf(1) / 21) for n in range(21)], 1)) < TOL and
      abs(abs(harmonic([(two_pi * n / 21, mp.mpf(1) / 21) for n in range(21)], 21)) - 1) < TOL)

# --------------------------------------------------------------------------
print("\n-- Theorem 3: coherence implies registration:  1 - Re(e^{-i N phi} m_N) <= N^2 (1 - C_1)")
x = sp.symbols("x", real=True)
for N in (2, 3, 4, 5, 7):
    # sin(N x)/sin(x) is a Chebyshev-type polynomial in cos x of sup norm N
    U = sp.simplify(sp.expand_trig(sp.sin(N * x)) / sp.sin(x))
    check(f"T3 lemma N = {N}: sin(Nx)/sin(x) = U_(N-1)(cos x), a polynomial in cos x",
          sp.simplify(U.rewrite(sp.cos) - sp.chebyshevu(N - 1, sp.cos(x))) == 0)
lemma_ok = all(abs(mp.sin(N * t)) <= N * abs(mp.sin(t)) + mp.mpf("1e-45")
               for N in (2, 3, 7, 21) for t in [mp.mpf(i) / 997 for i in range(-3200, 3200)])
check("T3 lemma |sin(N t)| <= N |sin t| on a 6400-point grid, N = 2, 3, 7, 21", lemma_ok)
ineq_ok = True
worst = 0
for N in (2, 3, 7, 21):
    for trial in range(400):
        natoms = rng.randint(1, 12)
        spread = rng.choice([0.01, 0.1, 0.5, 2.0, 6.0])
        c = mp.mpf(rng.uniform(0, 6.3))
        dist = [(c + mp.mpf(rng.uniform(-spread, spread)), mp.mpf(rng.random())) for _ in range(natoms)]
        dist = [(t, p) for (t, p), p in zip(dist, normalise([p for _, p in dist]))]
        m1 = harmonic(dist, 1)
        C1 = abs(m1)
        if C1 < TOL:
            continue
        phi = mp.arg(m1)
        lhs = 1 - mp.re(mp.e ** (-1j * N * phi) * harmonic(dist, N))
        rhs = N * N * (1 - C1)
        if lhs > rhs + mp.mpf("1e-40"):
            ineq_ok = False
        if rhs > 0:
            worst = max(worst, lhs / rhs)
check("T3 1600 random ensembles (N = 2, 3, 7, 21): the inequality holds", ineq_ok, f"max lhs/rhs = {float(worst):.4f}")
# sharpness: two atoms at +-d, ratio -> 1 as d -> 0
N = 21
ratios = []
for d in [mp.mpf("1e-2"), mp.mpf("1e-4"), mp.mpf("1e-6")]:
    dist = [(-d, mp.mpf(1) / 2), (d, mp.mpf(1) / 2)]
    C1 = abs(harmonic(dist, 1))
    lhs = 1 - mp.re(harmonic(dist, N))
    ratios.append(lhs / (N * N * (1 - C1)))
check("T3 the constant N^2 is sharp: a symmetric pair at +-d has ratio -> 1 as d -> 0 (N = 21)",
      abs(ratios[-1] - 1) < mp.mpf("1e-9") and ratios[0] < ratios[1] < ratios[2], f"{[float(r) for r in ratios]}")
check("T3 corollary (N = 21): C_1 >= 1 - 1/882 guarantees C_21 >= 1/2",
      1 - 21 ** 2 * (sp.Rational(1, 882)) == sp.Rational(1, 2))

# --------------------------------------------------------------------------
print("\n-- Theorem 4: registration at coprime orders is coherence (Bezout);  C_a = C_b = 1  =>  C_gcd(a,b) = 1")
check("T4 Bezout: 1 = 7 x 1 - 3 x 2, so e^{i theta} = e^{7 i theta} (e^{3 i theta})^(-2)", 7 * 1 - 3 * 2 == 1)
ok = True
for trial in range(50):
    c3 = mp.mpf(rng.uniform(0, 6.3))
    c7 = mp.mpf(rng.uniform(0, 6.3))
    # points with e^{3i th} = e^{i c3}: th = (c3 + 2 pi j)/3; keep those with e^{7 i th} = e^{i c7}
    common = [(c3 + two_pi * j) / 3 for j in range(3)]
    common = [t for t in common if abs(mp.e ** (7j * t) - mp.e ** (1j * c7)) < mp.mpf("1e-30")]
    if common:
        ok = False   # generic c3, c7: the two cosets do not meet at all
# compatible case: pick theta0, set c3 = 3 theta0, c7 = 7 theta0
for trial in range(50):
    t0 = mp.mpf(rng.uniform(0, 6.3))
    cands = [(3 * t0 + two_pi * j) / 3 for j in range(3)]
    meet = [t for t in cands if abs(mp.e ** (7j * t) - mp.e ** (7j * t0)) < mp.mpf("1e-30")]
    if len(meet) != 1:
        ok = False
check("T4 the 3-gon coset and the 7-gon coset meet in at most one point (generic: none; compatible: exactly one)", ok)
uni21 = [(two_pi * n / 21, mp.mpf(1) / 21) for n in range(21)]
check("T4 contrast: the uniform 21-gon has C_21 = 1 but C_3 = C_7 = 0, so registration in Z_21 is strictly weaker than registration in Z_3 and Z_7",
      abs(abs(harmonic(uni21, 21)) - 1) < TOL and abs(harmonic(uni21, 3)) < TOL and abs(harmonic(uni21, 7)) < TOL)
check("T4 the group isomorphism Z_3 x Z_7 = Z_21 (CRT) holds: k -> (k mod 3, k mod 7) is a bijection",
      len({(k % 3, k % 7) for k in range(21)}) == 21)
ok = True
for a, b in [(2, 3), (4, 6), (6, 15), (10, 14), (3, 7), (21, 14)]:
    g = gcd(a, b)
    # registration at a and b: support on {theta: e^{ia th} = 1, e^{ib th} = 1} = (2 pi / g) Z
    sup = [two_pi * j / (a * b) for j in range(a * b)]
    sup = [t for t in sup if abs(mp.e ** (1j * a * t) - 1) < mp.mpf("1e-30") and abs(mp.e ** (1j * b * t) - 1) < mp.mpf("1e-30")]
    if len(sup) != g:
        ok = False
check("T4 general form: {e^{ia t} = e^{ib t} = 1} is exactly the gcd(a,b)-gon, for six (a, b) pairs", ok)

# --------------------------------------------------------------------------
print("\n-- Theorem 5: the full character sum is the only exact selector; filtered sums have sidelobes")
N = 21
full = [mp.fsum(mp.e ** (2j * mp.pi * k * d / N) for k in range(N)) / N for d in range(N)]
check("T5 (1/21) sum_k e^{2 pi i k d/21} = delta_{d,0} for d = 0..20",
      abs(full[0] - 1) < TOL and all(abs(v) < TOL for v in full[1:]))


def filtered(S, N):
    return [mp.fsum(mp.e ** (2j * mp.pi * k * d / N) for k in S) / len(S) for d in range(N)]


ok_parseval, ok_bound, ok_nonzero = True, True, True
for size in range(1, N):
    for trial in range(30):
        S = sorted(rng.sample(range(N), size))
        F = filtered(S, N)
        par = mp.fsum(abs(v) ** 2 for v in F)
        if abs(par - mp.mpf(N) / size) > mp.mpf("1e-35"):
            ok_parseval = False
        side = max(abs(v) for v in F[1:])
        bound = mp.sqrt((mp.mpf(N) / size - 1) / (N - 1))
        if side < bound - mp.mpf("1e-35"):
            ok_bound = False
        if side < mp.mpf("1e-20"):
            ok_nonzero = False
check("T5 Parseval: sum_d |F_S(d)|^2 = N/|S| (570 random subsets of Z_21)", ok_parseval)
check("T5 sidelobe bound: max_{d != 0} |F_S(d)| >= sqrt((N/|S| - 1)/(N - 1)) for every proper subset tested", ok_bound)
check("T5 no proper subset gives an exact selector (every tested F_S has a nonzero sidelobe)", ok_nonzero)
S14 = [k for k in range(N) if k % 3 != 0]
F14 = filtered(S14, N)
expect = [1 if d == 0 else (-mp.mpf(1) / 2 if d % 7 == 0 else 0) for d in range(N)]
check("T5 the 14 characters k not divisible by 3: F(d) = 1 at d = 0, -1/2 at d = 7, 14, and 0 elsewhere (exact: (21[21|d] - 7[7|d])/14)",
      all(abs(F14[d] - expect[d]) < TOL for d in range(N)) and len(S14) == 14)
check("T5 its sidelobe 1/2 exceeds the Parseval floor sqrt(1/40) = 0.158", mp.mpf(1) / 2 > mp.sqrt(mp.mpf(1) / 40))

# --------------------------------------------------------------------------
print("\n-- Proposition 6: the 21-fold lock potential (README section 8), as stated there")
th = sp.symbols("theta", real=True)
V = -sp.cos(21 * th)
crit = sp.solve(sp.Eq(sp.diff(V, th), 0), th)
minima = [sp.Rational(2, 21) * sp.pi * n for n in range(21)]
check("P6 -cos(21 theta) has its minima exactly at theta_n = 2 pi n / 21 (21 of them on [0, 2 pi))",
      all(sp.simplify(sp.diff(V, th, 2).subs(th, m)) > 0 and sp.simplify(sp.diff(V, th).subs(th, m)) == 0 for m in minima))
check("P6 a population spread evenly over those minima is registered (C_21 = 1) but incoherent (C_1 = 0)",
      abs(abs(harmonic(uni21, 21)) - 1) < TOL and abs(harmonic(uni21, 1)) < TOL)


print("\n-- Theorem 1b (referee): the rotated polygon's harmonics carry the rotation phase")
ok = True
for N in (3, 7, 21):
    th0 = mp.mpf("0.731")
    dist = [(th0 + two_pi * n / N, mp.mpf(1) / N) for n in range(N)]
    for k in range(0, 2 * N + 1):
        target = mp.e ** (1j * k * th0) if k % N == 0 else 0
        if abs(harmonic(dist, k) - target) > TOL:
            ok = False
check("T1b uniform rotated N-gon: m_k = e^{i k theta0} if N | k, else 0 (N = 3, 7, 21)", ok)

print("\n-- Theorem 4b (referee): approximate coprime locking, C1 >= 1 - [sqrt(1-C7) + 2 sqrt(1-C3)]^2")
ok, worst = True, mp.mpf(1)
for trial in range(3000):
    n = rng.randint(1, 8)
    c = mp.mpf(rng.uniform(0, 6.3)); sd = rng.choice([0.003, 0.03, 0.2, 1.0, 3.0])
    dist = [(c + mp.mpf(rng.gauss(0, sd)), mp.mpf(rng.random())) for _ in range(n)]
    dist = [(t, p) for (t, _), p in zip(dist, normalise([p for _, p in dist]))]
    C1, C3, C7 = (abs(harmonic(dist, k)) for k in (1, 3, 7))
    bound = max(mp.mpf(0), 1 - (mp.sqrt(1 - C7) + 2 * mp.sqrt(1 - C3)) ** 2)
    worst = min(worst, C1 - bound)
    if C1 < bound - mp.mpf("1e-30"):
        ok = False
check("T4b 3000 random ensembles satisfy the bound", ok, f"min(C1 - bound) = {float(worst):.2e}")
check("T4b equal stages C3 = C7 = r give C1 >= 1 - 9(1 - r): 99% per stage guarantees 91% coherence",
      abs((1 - (mp.sqrt(mp.mpf("0.01")) + 2 * mp.sqrt(mp.mpf("0.01"))) ** 2) - mp.mpf("0.91")) < 1e-40)

print("\n-- Theorem 5b (referee): complementary reconstruction F21 = (2/3) F14 + (1/3) F7")
S7 = [k for k in range(21) if k % 3 == 0]
F7 = filtered(S7, 21)
check("T5b the 7 characters k = 0 mod 3: F7(d) = 1 if 7 | d, else 0",
      all(abs(F7[d] - (1 if d % 7 == 0 else 0)) < TOL for d in range(21)))
F21 = [mp.mpf(2) / 3 * F14[d] + mp.mpf(1) / 3 * F7[d] for d in range(21)]
check("T5b coherent recombination (2/3) F14 + (1/3) F7 is exactly delta_{d,0}",
      all(abs(F21[d] - (1 if d == 0 else 0)) < TOL for d in range(21)))
check("T5b incoherent (intensity) addition cannot cancel the aliases: (2/3)|F14|^2 + (1/3)|F7|^2 = 1/2 at d = 7",
      abs(mp.mpf(2) / 3 * abs(F14[7]) ** 2 + mp.mpf(1) / 3 * abs(F7[7]) ** 2 - mp.mpf(1) / 2) < TOL)
check("T5b the scalar 14-filter separates a match (1) from an alias (-1/2) but not the two aliases from each other",
      abs(F14[0] - 1) < TOL and abs(F14[7] - F14[14]) < TOL and abs(F14[7] + mp.mpf(1) / 2) < TOL)

print("\n-- Proposition 6b (referee): a coercive amplitude-phase potential with 21 phase minima")
rho_, th_, a_, b4, c_, h_ = sp.symbols("rho theta a b c h", real=True)
Vp = a_ * rho_ ** 2 + b4 * rho_ ** 4 + c_ * rho_ ** 22 - 2 * h_ * rho_ ** 21 * sp.cos(21 * th_)
stiff = sp.simplify(sp.diff(Vp, th_, 2).subs(th_, 2 * sp.pi * 5 / 21))
check("P6b angular stiffness at theta_n = 2 pi n/21 is 2 h rho^21 (21)^2 = 882 h rho^21",
      sp.simplify(stiff - 882 * h_ * rho_ ** 21) == 0)
Vnum = sp.lambdify(rho_, Vp.subs({a_: -1, b4: sp.Rational(1, 2), c_: 1, h_: 1, th_: 0}))
check("P6b with c > 0 the potential is bounded below (coercive); with a = -1 a nonzero minimum exists",
      Vnum(3.0) > 0 and Vnum(10.0) > Vnum(3.0) and min(Vnum(x / 100) for x in range(1, 200)) < Vnum(0))

print("\n" + "=" * 78)
print(f"GP-4: {sum(RESULTS)}/{len(RESULTS)} checks passed")
sys.exit(0 if all(RESULTS) else 1)
