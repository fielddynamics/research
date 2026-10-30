#!/usr/bin/env python3
"""
Look-elsewhere test for G = (17/13) alpha^21 hbar c / m_e^2
===========================================================

The GFD expression for Newton's constant has a rational prefactor (17/13) and
an integer exponent (21). How special is that combination? This script
searches every simple alternative of the same form,

    alpha_G = (p/q) * alpha^n,   p, q = 1..21 coprime,   n = 18..24,

and counts how many land as close to the measured
alpha_G = G m_e^2 / (hbar c) as 17/13 * alpha^21 does:

  - within the tree-level residual of 0.12%
  - within 22 ppm (the CODATA uncertainty of G) after the one-loop factor
    (1 + alpha/2pi)

Python 3.8+, standard library only.

    python look_elsewhere_G.py
"""
import math

ALPHA = 7.2973525643e-3          # CODATA 2018
HBAR = 1.054571817e-34
C = 299792458.0
M_E = 9.1093837015e-31
G = 6.67430e-11                  # relative uncertainty 2.2e-5

A_G = G * M_E ** 2 / (HBAR * C)
LOOP = 1 + ALPHA / (2 * math.pi)


def main():
    tree_target = abs(17 / 13 * ALPHA ** 21 - A_G) / A_G
    candidates, tree_hits, loop_hits = 0, [], []
    for n in range(18, 25):
        for p in range(1, 22):
            for q in range(1, 22):
                if math.gcd(p, q) != 1:
                    continue
                candidates += 1
                v = p / q * ALPHA ** n
                if abs(v - A_G) / A_G <= tree_target * 1.0001:
                    tree_hits.append((p, q, n, (v - A_G) / A_G))
                if abs(v * LOOP - A_G) / A_G < 22e-6:
                    loop_hits.append((p, q, n, (v * LOOP - A_G) / A_G))

    print("=" * 70)
    print("  LOOK-ELSEWHERE TEST: alpha_G = (p/q) alpha^n")
    print("=" * 70)
    print(f"  measured alpha_G = {A_G:.6e}")
    print(f"  candidates: p, q = 1..21 coprime, n = 18..24  ->  {candidates}")
    print(f"\n  within the tree-level residual ({100 * tree_target:.3f}%):")
    for p, q, n, r in tree_hits:
        print(f"    {p}/{q} * alpha^{n}   residual {100 * r:+.4f}%")
    print("\n  with the one-loop factor (1 + alpha/2pi), within 22 ppm:")
    for p, q, n, r in loop_hits:
        print(f"    {p}/{q} * alpha^{n}   residual {1e6 * r:+.1f} ppm")
    unique = tree_hits == [h for h in tree_hits if (h[0], h[1], h[2]) == (17, 13, 21)] and \
        [(h[0], h[1], h[2]) for h in loop_hits] == [(17, 13, 21)]
    print(f"\n  17/13 * alpha^21 is the only candidate in both windows: {unique}")
    return dict(candidates=candidates, tree_hits=tree_hits, loop_hits=loop_hits, unique=unique)


if __name__ == "__main__":
    main()
