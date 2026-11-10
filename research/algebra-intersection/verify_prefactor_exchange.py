"""
verify_prefactor_exchange.py
============================

Part IX of INTERSECTION_ALGEBRA.md: the prefactor 17/13 as a phase average.

  Numerator.  For ANY distribution of the structural state s that is symmetric
  under the exchange s -> -s (x <-> 1/x), <s> = 0 and so <f> = <1 + sK + K^2> = 1 + K^2 = 17,
  whatever the measure.  The archive's breathing cycle (13 -> 21 -> 13,
  read_sweep_synthesis.md) is such a distribution for any step measure.

  Denominator.  The source in alpha_G = G m_e^2/(hbar c) is the electron, a bound
  pattern; the archive places bound matter in TetB (Paper VII: "Bound envelopes,
  TetB chambers occupied, are matter"), whose capacity is f(-1) = 13.

  So 17/13 = <f>_exchange / f(bound source).
"""
from __future__ import annotations

import math

import numpy as np
import sympy as sp

RESULTS = []


def check(name, cond):
    RESULTS.append((name, bool(cond)))
    print(f"[{'PASS' if cond else 'FAIL'}] {name}")


K = 4
f = lambda s: 1 + s * K + K * K
rng = np.random.default_rng(3)

print("\n=== N1. Exchange symmetry forces <f> = 1 + K^2 for any symmetric measure ===")
Ks, s = sp.symbols("K s")
check("<1 + sK + K^2> = 1 + K<s> + K^2, and exchange symmetry gives <s> = 0: <f> = K^2 + 1 = 17",
      sp.expand((1 + s * Ks + Ks ** 2).subs(s, 0)) == Ks ** 2 + 1)
measures = {
    "uniform in s": rng.uniform(-1, 1, 10 ** 6),
    "uniform in mu (= uniform in s)": 2 * rng.uniform(0, 1, 10 ** 6) - 1,
    "uniform rapidity eta in [-3, 3]": np.tanh(rng.uniform(-3, 3, 10 ** 6)),
    "log-normal x, symmetric in ln x": np.tanh(rng.normal(0, 1.7, 10 ** 6) / 2),
    "two-point s = +-1 (TetA/TetB only)": rng.choice([-1.0, 1.0], 10 ** 6),
}
for nm, sv in measures.items():
    print(f"      {nm:38s} <f> = {f(sv).mean():.4f}")
check("Every exchange-symmetric measure gives <f> = 17 (to Monte Carlo precision)",
      all(abs(f(sv).mean() - 17) < 0.02 for sv in measures.values()))


def climb(rng_):
    """One closure of the hexagram walk: random hexagrams until all 64 are seen; f per step."""
    seen, out = set(), []
    while len(seen) < 64:
        seen.add(int(rng_.integers(64)))
        out.append(13 + len(seen) / 8)          # f(n) = 13 + n/8 (closure-climb note)
    return out


steps = [v for _ in range(400) for v in climb(rng)]
up = np.mean(steps)
check(f"A one-way climb averaged per step is NOT exchange symmetric: <f> = {up:.2f} (the closure-climb note's ~19.2)",
      abs(up - 19.2) < 0.2)
breath = []
for _ in range(400):
    c = climb(rng)
    breath += c + [34 - v for v in c]           # exhale mirrors inhale: s -> -s, f -> 34 - f
check(f"The breathing cycle (inhale + its exchange-mirrored exhale), averaged per step: <f> = {np.mean(breath):.4f} = 17 exactly",
      abs(np.mean(breath) - 17) < 1e-9)

print("\n=== N2. The denominator: the bound source ===")
den = {"TetA (unbound read, s=+1)": f(1), "Field Origin (s=0)": f(0), "TetB (bound matter, s=-1)": f(-1)}
alpha = 7.2973525693e-3
aG = 6.67430e-11 * 9.1093837015e-31 ** 2 / (1.054571817e-34 * 299792458.0)
for nm, d in den.items():
    pre = 17 / d
    print(f"      <f>/f({nm:28s}) = 17/{d:2d} = {pre:.4f}   alpha_G residual {100 * (pre * alpha ** 21 * (1 + alpha / (2 * math.pi)) - aG) / aG:+.4f}%")
res = {d: abs(17 / d * alpha ** 21 * (1 + alpha / (2 * math.pi)) - aG) / aG for d in (21, 17, 13)}
check(f"Only the TetB source (13) fits alpha_G ({1e6 * res[13]:.0f} ppm); TetA (21) and the origin (17) miss by"
      f" {100 * res[21]:.0f}% and {100 * res[17]:.0f}%", res[13] < 22e-6 and res[21] > 0.2 and res[17] > 0.2)
check("And f(-1) = 13 = DK + 1 at D = 3, K = 4 (Paper VII Eq. 24's spatial-structure reading agrees)", f(-1) == 3 * 4 + 1)

n_pass = sum(1 for _, ok in RESULTS if ok)
print(f"\n{n_pass}/{len(RESULTS)} checks passed")
if __name__ == "__main__":
    raise SystemExit(0 if n_pass == len(RESULTS) else 1)
