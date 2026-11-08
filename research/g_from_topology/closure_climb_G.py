#!/usr/bin/env python3
"""
G from the closure climb
========================

Companion to g_from_the_closure_climb.md. Checks, in order:

1. The climb: over one closure the coupling f = 1 + sK + K^2 rises from 13
   (TetB, no hexagrams seen) through 17 (Field Origin, 32 seen) to 21 (TetA,
   all 64 seen), linearly, one unit per 8 new hexagrams.
2. The average coupling over the closure, measured per new hexagram, is exactly
   17, the Field Origin value. Measured per step of an actual walk it is not
   (about 19.2), and neither are the geometric or harmonic means.
3. The closure-stage rules alpha^E * (A/B), with E, A, B drawn from
   {start, mean, end} = {13, 17, 21}: 21 rules. Which of them match
   alpha_G = G m_e^2 / (hbar c)?
4. How often the same 21 rules fit a fake value of alpha_G (look-elsewhere).

Python 3.8+, standard library; mpmath (optional) for pi's walk in step 2.

    python closure_climb_G.py
"""
import math
import random
from fractions import Fraction

ALPHA = 7.2973525643e-3          # CODATA 2018
HBAR = 1.054571817e-34
C = 299792458.0
M_E = 9.1093837015e-31
G = 6.67430e-11                  # relative uncertainty 2.2e-5
A_G = G * M_E ** 2 / (HBAR * C)
LOOP = 1 + ALPHA / (2 * math.pi)
K, D = 4, 3


def f_of_s(s):
    return 1 + s * K + K * K


def f_of_n(n):
    """Coupling after n distinct hexagrams: s runs from -1 (n = 0) to +1 (n = 64)."""
    return f_of_s(Fraction(n, 32) - 1)


def walk_time_mean(digits):
    s, prev, seen, vals = 3, None, set(), []
    for d in digits:
        s = (s + d) % 8
        if prev is not None:
            seen.add((prev, s))
            vals.append(float(f_of_n(len(seen))))
            if len(seen) == 64:
                break
        prev = s
    return sum(vals) / len(vals), len(vals)


def pi_octal(n=1200):
    try:
        from mpmath import mp
    except ImportError:
        return None
    with mp.workdps(int(n * 0.904) + 20):
        x = mp.pi - 3
        out = []
        for _ in range(n):
            x *= 8
            d = int(x)
            out.append(d)
            x -= d
    return [3] + out


def main():
    print("=" * 72)
    print("  G FROM THE CLOSURE CLIMB")
    print("=" * 72)

    # 1. the climb
    start, mid, end = f_of_n(0), f_of_n(32), f_of_n(64)
    steps = {f_of_n(n + 1) - f_of_n(n) for n in range(64)}
    print(f"\n1. Climb: f(0 hexagrams) = {start}, f(32) = {mid}, f(64) = {end}; "
          f"rise per new hexagram = {steps.pop()} (one unit per 8)")

    # 2. averages
    mean_progress = sum(f_of_n(n) for n in range(65)) / 65
    gm = math.exp(sum(math.log(f_of_n(n)) for n in range(65)) / 65)
    hm = 65 / sum(1 / float(f_of_n(n)) for n in range(65))
    print(f"\n2. Mean coupling over the closure, per new hexagram: {mean_progress} (exact)")
    print(f"   geometric mean {gm:.3f}, harmonic mean {hm:.3f}")
    rng = random.Random(0)
    tm = [walk_time_mean([3] + [rng.randrange(8) for _ in range(3000)])[0] for _ in range(1000)]
    print(f"   mean per step of the walk: random digits {sum(tm) / len(tm):.2f}", end="")
    pd = pi_octal()
    if pd:
        m, n = walk_time_mean(pd)
        print(f", pi {m:.2f} (closure at step {n})")
    else:
        print(" (install mpmath for pi's walk)")

    # 3. the rule menu
    stage = {"start": 13, "mean": 17, "end": 21}
    rules = []
    for e in stage:
        rules.append((f"alpha^{e}", stage[e], 1.0))
        for a in stage:
            for b in stage:
                if a != b:
                    rules.append((f"alpha^{e} * {a}/{b}", stage[e], stage[a] / stage[b]))
    tree = abs(17 / 13 * ALPHA ** 21 - A_G) / A_G
    print(f"\n3. {len(rules)} closure-stage rules; those within 1% of alpha_G:")
    for name, e, p in rules:
        r = (p * ALPHA ** e - A_G) / A_G
        if abs(r) < 0.01:
            r1 = (p * ALPHA ** e * LOOP - A_G) / A_G
            print(f"   {name:24s}  tree {100 * r:+.4f}%   with (1 + alpha/2pi) {1e6 * r1:+.1f} ppm")

    # 4. look-elsewhere with fake targets
    vals = [p * ALPHA ** e for _, e, p in rules]
    rng = random.Random(2)
    n_fake = 100_000
    half = math.log(1 / ALPHA) / 2
    fakes = [A_G * math.exp(rng.uniform(-half, half)) for _ in range(n_fake)]
    t = sum(min(abs(v - x) / x for v in vals) <= tree for x in fakes) / n_fake
    lp = sum(min(abs(v * LOOP - x) / x for v in vals) < 22e-6 for x in fakes) / n_fake
    print(f"\n4. Fake values of alpha_G (log-uniform over one factor of alpha) fitted by some rule:")
    print(f"   at tree level, within {100 * tree:.3f}%: {t:.4f}")
    print(f"   with (1 + alpha/2pi), within 22 ppm:  {lp:.5f}")
    print("\n   These rates apply only if the rule is fixed before comparison; see the note.")


if __name__ == "__main__":
    main()
