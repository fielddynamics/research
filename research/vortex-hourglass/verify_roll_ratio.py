"""
Roll-ratio theorem: exact sympy checks.

Premise: the two chambers meet at one contact point (the Field Origin) and share its velocity
there (no slip). Their radii are the shares, R_A = mu (TetA) and R_B = 1 - mu (TetB), as in the
roulette (research/constitutive-law-u(x)). Then R_A omega_A = R_B omega_B.

Run: python verify_roll_ratio.py   (exit 0 if all pass)
"""
from __future__ import annotations

import sys

import sympy as sp

CHECKS = []


def check(name, ok):
    CHECKS.append((name, bool(ok)))


x = sp.symbols("x", positive=True)
wA = sp.symbols("omega_A", positive=True)
mu = x / (x + 1)
RA, RB = mu, 1 - mu

check("(0) the radii are the shares and fill the unit: R_A + R_B = 1", sp.simplify(RA + RB - 1) == 0)

# (i) no slip at the contact gives the rate ratio
wB = sp.solve(sp.Eq(RA * wA, RB * sp.Symbol("w")), sp.Symbol("w"))[0]
check("(i) no slip: omega_B / omega_A = R_A / R_B", sp.simplify(wB / wA - RA / RB) == 0)
check("(i) and R_A / R_B = mu / (1 - mu) = x, the odds ratio", sp.simplify(RA / RB - x) == 0)

# (ii) mean rate and half-difference; exchange of the chambers
wbar = (wA + wB) / 2
delta = (wA - wB) / 2
ratio = sp.simplify(delta / wbar)
check("(ii) half-difference over mean: delta / omega_bar = (1 - x)/(1 + x)", sp.simplify(ratio - (1 - x) / (1 + x)) == 0)
check("(ii) which is 1 - 2 mu", sp.simplify(ratio - (1 - 2 * mu)) == 0)
check("(ii) exchange of the chambers (x -> 1/x) flips delta / omega_bar",
      sp.simplify(ratio.subs(x, 1 / x) + ratio) == 0)
# Exchange swaps the two chambers: each takes the other's radius and rate.
RA2, RB2, wA2, wB2 = RB, RA, wB, wA
check("(ii) the exchanged pair still rolls without slip: R_A' omega_A' = R_B' omega_B'",
      sp.simplify(RA2 * wA2 - RB2 * wB2) == 0)
check("(ii) its rate ratio is 1/x, i.e. x -> 1/x", sp.simplify(wB2 / wA2 - 1 / x) == 0)
check("(ii) the mean rate is kept", sp.simplify((wA2 + wB2) / 2 - wbar) == 0)
check("(ii) the half-difference flips: the parity action of the hourglass lemma (f)",
      sp.simplify((wA2 - wB2) / 2 + delta) == 0)

# (iii) one rate only at the ring (the quiet partition itself)
check("(iii) delta = 0 exactly at x = 1", sp.solve(sp.Eq(ratio, 0), x) == [1])
check("(iii) where mu = 1/2 (the ring)", mu.subs(x, 1) == sp.Rational(1, 2))
check("(iii) TetB turns faster than TetA inside the ring (x > 1)", sp.simplify(wB.subs(x, 2) / wA) > 1)
check("(iii) and slower than TetA outside it (x < 1)", sp.simplify(wB.subs(x, sp.Rational(1, 2)) / wA) < 1)

# (iv) the shear's rate of change is the logistic core
t = sp.symbols("t", real=True)
r_t = ratio.subs(x, sp.exp(t))
check("(iv) d(delta/omega_bar)/d ln x = -2 mu (1 - mu)",
      sp.simplify(sp.diff(r_t, t) - (-2 * mu * (1 - mu)).subs(x, sp.exp(t))) == 0)
check("(iv) mu satisfies the logistic law x dmu/dx = mu (1 - mu)", sp.simplify(x * sp.diff(mu, x) - mu * (1 - mu)) == 0)
crit = sp.solve(sp.diff(-2 * mu * (1 - mu), x), x)
check("(iv) the shear changes fastest at the ring, x = 1, where mu (1 - mu) = 1/4",
      crit == [1] and (mu * (1 - mu)).subs(x, 1) == sp.Rational(1, 4))

# (v) the chiral-holonomy twist
sigma = (x - 1) / (x + 1)
check("(v) the chiral-holonomy share difference sigma = (x - 1)/(x + 1) = -delta/omega_bar = 2 mu - 1",
      sp.simplify(sigma + ratio) == 0 and sp.simplify(sigma - (2 * mu - 1)) == 0)

if __name__ == "__main__":
    for name, ok in CHECKS:
        print(f"{'PASS' if ok else 'FAIL'}  {name}")
    n = sum(ok for _, ok in CHECKS)
    print(f"\n{n}/{len(CHECKS)} checks passed")
    sys.exit(0 if n == len(CHECKS) else 1)
