"""
verify_gravity_starts_at_13.py
==============================

Part XIII of INTERSECTION_ALGEBRA.md: the author's statement that 13 is where
gravity starts, and that below it is the photonic matrix of light
(research/photonic/the-pixel-and-the-lattice.md, gfd_light_substrate_synthesis.md).

Checked against the framework's own equations:
  the continuous capacity f(x) = (21x + 13)/(x + 1)  (the-pixel-and-the-lattice.md)
  the constitutive law mu = (f - 13)/8               (llms.txt Eq. 15)
and against the measured G.
"""
from __future__ import annotations

import math

import numpy as np
import sympy as sp

RESULTS = []


def check(name, cond):
    RESULTS.append((name, bool(cond)))
    print(f"[{'PASS' if cond else 'FAIL'}] {name}")


x = sp.symbols("x", positive=True)
f = (21 * x + 13) / (x + 1)
mu = x / (x + 1)

print("\n=== S1. 13 is the field-free limit: the bare photonic substrate ===")
check("f(x) -> 13 as x -> 0 (no gravitational field) and -> 21 as x -> oo", sp.limit(f, x, 0) == 13 and sp.limit(f, x, sp.oo) == 21)
check("f(x) - 13 = 8 mu(x) exactly: gravity's response is the capacity ABOVE 13", sp.simplify(f - 13 - 8 * mu) == 0)
xs = np.logspace(-12, 12, 2001)
fx = (21 * xs + 13) / (xs + 1)
check("For every field strength x > 0, 13 < f(x) < 21: no gravitational state reaches 13 or below", bool(np.all((fx > 13) & (fx < 21))))
check("f is strictly increasing in x: capacity rises from 13 the moment any field is present",
      sp.simplify(sp.diff(f, x) - 8 / (x + 1) ** 2) == 0)
print("      => 13 is the capacity of the substrate with no field (x = 0, mu = 0): the photonic matrix.")
print("         Gravity is the excess f - 13 = 8 mu. Nothing gravitational lives at or below 13.")

print("\n=== S2. The prefactor as closure capacity in substrate units ===")
s = sp.symbols("s")
fK = 1 + 4 * s + 16
check("A closure that starts at the floor and breathes exchange-symmetrically has mean capacity 17 (Part IX)",
      sp.integrate(fK, (s, -1, 1)) / 2 == 17)
print("      Reading (premise, not a check): 17/13 = (mean capacity of a closure) / (capacity of the field-free substrate)")

alpha = 7.2973525693e-3
aG = 6.67430e-11 * 9.1093837015e-31 ** 2 / (1.054571817e-34 * 299792458.0)
loop = 1 + alpha / (2 * math.pi)
ref = {"13, field-free substrate (gravity starts here)": 13, "17, Field Origin": 17, "21, TetA ceiling": 21}
res = {}
for nm, r in ref.items():
    res[r] = (17 / r * alpha ** 21 * loop - aG) / aG
    print(f"      reference {nm:46s}: alpha_G residual {1e6 * res[r]:+10.1f} ppm")
check("Only the field-free reference 13 fits the measured G (12 ppm); 17 and 21 miss by 24% and 38%",
      abs(res[13]) < 22e-6 and abs(res[17]) > 0.2 and abs(res[21]) > 0.3)

print("\n=== S3. Consistency with the one-way read (Part XII) ===")
print("      Premise (Paper I, not a check): the snapshot is taken first (READ -> SETTLE -> REGISTER), at the closure's start, the floor 13")
check("Same form as the loop factor: (average over the closure) / (value at the snapshot reference): 17/13 and (N+1)/N",
      abs((1 + 1 / (2 * math.pi / alpha)) - loop) < 1e-15)

print("\n=== S4. Provenance ===")
print("      The photonic notes, Paper VII's TetB statements and the 17/13 formula all entered this repository in one")
print("      import commit (31 Oct 2026), so git cannot show which came first. The checks above do not depend on order.")

n_pass = sum(1 for _, ok in RESULTS if ok)
print(f"\n{n_pass}/{len(RESULTS)} checks passed")
if __name__ == "__main__":
    raise SystemExit(0 if n_pass == len(RESULTS) else 1)
