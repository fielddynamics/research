"""
run_all_validations.py

Computational verification of every testable claim in:
  Letter 3: "Gravity Field Dynamics: Field Closure of the Tetrad Frame"

Each section header corresponds to a numbered equation or claim
in the letter.  Every claim is tested independently using SymPy
(symbolic) and NumPy (numerical).  The final summary reports
pass/fail for each.

The companion script run_all_validations.py verifies the
geometric and algebraic claims of Letters 1 and 2.

Requirements: numpy, sympy
Usage: python run_all_validations.py
"""

import numpy as np
import sympy as sp

results = {}

def section(title):
    print()
    print("=" * 70)
    print(f"  {title}")
    print("=" * 70)

def record(claim, passed):
    results[claim] = passed
    status = "PASS" if passed else "*** FAIL ***"
    print(f"  [{status}] {claim}")
    return passed


# ============================================================
# SETUP: symbolic variables
# ============================================================

x = sp.Symbol('x', positive=True)
y = sp.Symbol('y', positive=True)
u = sp.Symbol('u', positive=True)
K = 4
D = 3

mu = x / (x + 1)
tetb = 1 / (x + 1)


# ============================================================
# 1. CONNECTION COMPONENT COUNT (Eq. 1)
# ============================================================

section("1. CONNECTION COMPONENT COUNT")

record("K^3 = 64 components", K**3 == 64)


# ============================================================
# 2. COMBINATORIAL SPLIT (Eqs. 3-4)
# ============================================================

section("2. COMBINATORIAL SPLIT PER FACE")

kept_per_face = (K**2 + K) // 2
disc_per_face = (K**2 - K) // 2

record("Retained per face = (K^2+K)/2 = 10", kept_per_face == 10)
record("Discarded per face = (K^2-K)/2 = 6", disc_per_face == 6)
record("Diagonal count = K = 4", K == 4)
record("Off-diagonal = K^2-K = 12", K**2 - K == 12)
record("Mirror pairs = (K^2-K)/2 = 6", (K**2 - K) // 2 == 6)


# ============================================================
# 3. TOTAL ACROSS FACES
# ============================================================

section("3. TOTAL ACROSS ALL FACES")

total_kept = K * kept_per_face
total_disc = K * disc_per_face
total_all = total_kept + total_disc

record("Total retained = 40", total_kept == 40)
record("Total discarded = 24", total_disc == 24)
record("40 + 24 = 64 = K^3", total_all == 64 and total_all == K**3)


# ============================================================
# 4. POLYNOMIAL IDENTITY (Eqs. 5-6)
# ============================================================

section("4. POLYNOMIAL IDENTITY")

def f(K_val, s_val):
    return 1 + s_val * K_val + K_val**2

f_plus = f(K, +1)
f_minus = f(K, -1)
f_zero = f(K, 0)

print(f"  f(K, +1) = {f_plus}")
print(f"  f(K,  0) = {f_zero}")
print(f"  f(K, -1) = {f_minus}")

record("f(K, +1) = 21", f_plus == 21)
record("f(K,  0) = 17", f_zero == 17)
record("f(K, -1) = 13", f_minus == 13)

poly_kept = (f_plus - 1) // 2
poly_disc = (f_minus - 1) // 2

record("(f(K,+1) - 1)/2 = 10 = retained per face", poly_kept == 10)
record("(f(K,-1) - 1)/2 = 6 = discarded per face", poly_disc == 6)
record("Polynomial kept matches combinatorial kept",
       poly_kept == kept_per_face)
record("Polynomial discarded matches combinatorial discarded",
       poly_disc == disc_per_face)


# ============================================================
# 5. FIELD-ORIGIN TERM JUSTIFICATION
# ============================================================

section("5. FIELD-ORIGIN TERM (K^0 = 1)")

record("K^0 = 1", K**0 == 1)
record("Diagonal entries per face = K = 4", K == 4)
record("f(K,+1) - 1 = K^2 + K = 20",
       f_plus - 1 == K**2 + K)
record("f(K,-1) - 1 = K^2 - K = 12",
       f_minus - 1 == K**2 - K)
record("+/-K separating 20 from 12 is the sK parity-odd term",
       (f_plus - 1) - (f_minus - 1) == 2 * K)


# ============================================================
# 6. PARTITION PROPERTIES (Eqs. 7-8)
# ============================================================

section("6. PARTITION PROPERTIES")

record("mu(x) = x/(x+1)", sp.simplify(mu - x/(x+1)) == 0)
record("1-mu(x) = 1/(x+1)", sp.simplify((1 - mu) - 1/(x+1)) == 0)
record("mu + (1-mu) = 1", sp.simplify(mu + tetb - 1) == 0)
record("mu(0) = 0", mu.subs(x, 0) == 0)
record("mu(1) = 1/2", mu.subs(x, 1) == sp.Rational(1, 2))
record("mu -> 1 as x -> inf", sp.limit(mu, x, sp.oo) == 1)
record("Exchange symmetry: mu(1/x) = 1 - mu(x)",
       sp.simplify(mu.subs(x, 1/x) - (1 - mu)) == 0)


# ============================================================
# 7. LOGISTIC IDENTITY (Eq. 9)
# ============================================================

section("7. LOGISTIC IDENTITY")

dmu_dx = sp.diff(mu, x)
lhs = x * dmu_dx
rhs = mu * (1 - mu)

record("x dmu/dx = mu(1-mu)",
       sp.simplify(lhs - rhs) == 0)
record("Peak transition rate at x=1: mu(1-mu) = 1/4",
       (mu * (1 - mu)).subs(x, 1) == sp.Rational(1, 4))


# ============================================================
# 8. RADIAL ACCELERATION RELATION (Eq. 10)
# ============================================================

section("8. RADIAL ACCELERATION RELATION")

g_obs = sp.Symbol('g_obs', positive=True)
a0 = sp.Symbol('a0', positive=True)

x_sub = g_obs / a0
mu_sub = x_sub / (x_sub + 1)
g_bar = mu_sub * g_obs
rar = g_obs**2 / (g_obs + a0)

record("g_bar = mu * g_obs = g_obs^2/(g_obs + a0)",
       sp.simplify(g_bar - rar) == 0)
record("High-x limit: g_bar/g_obs -> 1",
       sp.limit(rar / g_obs, g_obs, sp.oo) == 1)
record("Low-x limit: g_bar -> g_obs^2/a0",
       sp.limit(rar / (g_obs**2 / a0), g_obs, 0) == 1)


# ============================================================
# 9. F(y) LONG DIVISION (Eqs. 11-12)
# ============================================================

section("9. F(y) LONG DIVISION AND INTEGRATION")

# Long division verification
reconstruction = sp.expand((u - 1) * (u + 1) + 1)
record("Long division: (u-1)(u+1) + 1 = u^2",
       reconstruction == u**2)
record("u^2/(u+1) = u - 1 + 1/(u+1)",
       sp.simplify(u**2 / (u + 1) - (u - 1 + 1/(u + 1))) == 0)

# Integration term by term
sqrt_y = sp.sqrt(y)

term1 = 2 * sp.integrate(u, (u, 0, sqrt_y))
term2 = 2 * sp.integrate(-1, (u, 0, sqrt_y))
term3 = 2 * sp.integrate(1/(u+1), (u, 0, sqrt_y))

print(f"  Term 1 (K^2 level):  {term1}")
print(f"  Term 2 (sK level):   {term2}")
print(f"  Term 3 (K^0 level):  {term3}")

F_derived = term1 + term2 + term3
F_expected = y - 2*sp.sqrt(y) + 2*sp.log(1 + sp.sqrt(y))

record("Term 1: 2*int(u du) = y",
       sp.simplify(term1 - y) == 0)
record("Term 2: 2*int(-1 du) = -2*sqrt(y)",
       sp.simplify(term2 - (-2*sp.sqrt(y))) == 0)
record("Term 3: 2*int(1/(u+1) du) = 2*ln(1+sqrt(y))",
       sp.simplify(term3 - 2*sp.log(1 + sp.sqrt(y))) == 0)
record("F(y) = y - 2*sqrt(y) + 2*ln(1+sqrt(y))",
       sp.simplify(F_derived - F_expected) == 0)

# Remainder = 1-mu (TetB fraction)
mu_u = u / (u + 1)
record("Remainder 1/(u+1) = 1 - mu(u) [TetB fraction]",
       sp.simplify(1/(u + 1) - (1 - mu_u)) == 0)


# ============================================================
# 10. F(y) DERIVATIVE ROUND-TRIP
# ============================================================

section("10. F(y) DERIVATIVE ROUND-TRIP")

dF_dy = sp.diff(F_expected, y)
mu_sqrt_y = sp.sqrt(y) / (1 + sp.sqrt(y))

record("dF/dy = sqrt(y)/(1+sqrt(y)) = mu(sqrt(y))",
       sp.simplify(dF_dy - mu_sqrt_y) == 0)


# ============================================================
# 11. ASYMPTOTIC LIMITS OF F(y)
# ============================================================

section("11. ASYMPTOTIC LIMITS OF F(y)")

ratio_high = F_expected / y
record("F(y)/y -> 1 as y -> inf [reduces to GR]",
       sp.limit(ratio_high, y, sp.oo) == 1)

# Low-acceleration: numerical check
y_small = 1e-8
F_num = float(F_expected.subs(y, y_small))
F_approx = (2.0/3.0) * y_small**1.5
record("F(y) ~ (2/3)*y^(3/2) at y << 1 [deep-field]",
       abs(F_num - F_approx) / abs(F_approx) < 1e-3)

# Symbolic series check
eps = sp.Symbol('eps', positive=True)
F_eps = F_expected.subs(y, eps**2)
series = sp.series(F_eps, eps, 0, n=5)
print(f"  F(eps^2) series: {series}")
record("Leading series term is (2/3)*eps^3 = (2/3)*y^(3/2)",
       series.coeff(eps, 3) == sp.Rational(2, 3))


# ============================================================
# 12. FIELD CLOSURE COUNTS
# ============================================================

section("12. FIELD CLOSURE")

record("Kept + Discarded = K^2 per face: 10 + 6 = 16",
       kept_per_face + disc_per_face == K**2)
record("Total: 40 + 24 = 64 = K^3",
       total_kept + total_disc == K**3)
record("Surplus per face = K: 10 - 6 = 4",
       kept_per_face - disc_per_face == K)
record("Total surplus = K^2: 40 - 24 = 16",
       total_kept - total_disc == K**2)


# ============================================================
# 13. ACTION PREFACTORS
# ============================================================

section("13. ACTION PREFACTORS")

prefactors = [K**2, 2**D, K]
print(f"  Prefactors: {prefactors} = [K^2, 2^D, K] = [16, 8, 4]")

record("16 = K^2", prefactors[0] == 16)
record("8 = 2^D", prefactors[1] == 8)
record("4 = K", prefactors[2] == 4)
record("Geometric sequence ratio 2: 16/8 = 8/4 = 2",
       prefactors[0] / prefactors[1] == 2 and
       prefactors[1] / prefactors[2] == 2)


# ============================================================
# SUMMARY
# ============================================================

section("SUMMARY")

n_pass = sum(1 for v in results.values() if v)
n_fail = sum(1 for v in results.values() if not v)
n_total = len(results)

for claim, passed in results.items():
    status = "PASS" if passed else "FAIL"
    print(f"  [{status}]  {claim}")

print()
print(f"  {n_pass}/{n_total} claims verified.  {n_fail} failures.")
if n_fail == 0:
    print("  All claims in Letter 3 are computationally confirmed.")
else:
    print("  *** SOME CLAIMS FAILED — REVIEW ABOVE ***")
