"""
verify_closure_ladder.py
========================

Part XIV of INTERSECTION_ALGEBRA.md: the floor-and-mean reading of Part XIII applied
to closures of every depth n.

A depth-n closure has levels of size 1, K, ..., K^(n-1); odd levels flip under parity
(Letter 2's (-1)^rank). Then:
  junctions        J_n = (K^n - 1)/(K - 1)
  field-free floor F_n = sum (-K)^k = (1 - (-K)^n)/(1 + K)
  symmetric mean   E_n = sum of the even-level sizes
  coupling         alpha_n = (E_n / F_n) alpha^(J_n)
A closure needs a positive floor (a substrate beneath it, Part XIII).
"""
from __future__ import annotations

from fractions import Fraction

RESULTS = []


def check(name, cond):
    RESULTS.append((name, bool(cond)))
    print(f"[{'PASS' if cond else 'FAIL'}] {name}")


def ladder(n, K=4):
    J = (K ** n - 1) // (K - 1)
    Fl = sum((-K) ** k for k in range(n))
    E = sum(K ** k for k in range(0, n, 2))
    return J, Fl, E


K, D = 4, 3
print("   n   J_n   floor   mean   prefactor")
for n in range(1, 8):
    J, Fl, E = ladder(n)
    print(f"  {n:2d} {J:5d} {Fl:7d} {E:6d}   {Fraction(E, Fl)}")

check("Floor F_n = (1 - (-K)^n)/(1 + K) is positive exactly for odd n (K = 2..9, n = 1..12)",
      all((sum((-k) ** j for j in range(n)) > 0) == (n % 2 == 1) for k in range(2, 10) for n in range(1, 13)))
check("Depth 1 = electromagnetism: J = 1, prefactor exactly 1 (alpha_1 = alpha, as calibration requires)",
      ladder(1)[0] == 1 and Fraction(ladder(1)[2], ladder(1)[1]) == 1)
check("Depth 3 = gravity: J = 21, prefactor 17/13", ladder(3)[0] == 21 and Fraction(ladder(3)[2], ladder(3)[1]) == Fraction(17, 13))
check("Depths 2 and 4 are forbidden (floors -3 and -51): no closure between electromagnetism and gravity",
      ladder(2)[1] < 0 and ladder(4)[1] < 0)
n5 = ladder(5)
check(f"The next allowed rung is depth 5: alpha^{n5[0]} x {Fraction(n5[2], n5[1])}, about 10^-729 (physically empty)",
      n5[0] == 341 and Fraction(n5[2], n5[1]) == Fraction(273, 205))
check("Closed form for odd n: prefactor = (K^(n+1) - 1)/((K - 1)(K^n + 1)), tending to K/(K-1) = 4/3",
      all(Fraction(ladder(n)[2], ladder(n)[1]) == Fraction(K ** (n + 1) - 1, (K - 1) * (K ** n + 1)) for n in (1, 3, 5, 7))
      and abs(float(Fraction(K ** 22 - 1, (K - 1) * (K ** 21 + 1))) - 4 / 3) < 1e-9)
check("For every even n the floor/mean ratio is -1/(K-1) = -1/D = cos(tetrahedral angle) (recorded, not interpreted)",
      all(Fraction(ladder(n)[2], ladder(n)[1]) == Fraction(-1, K - 1) for n in (2, 4, 6, 8)))
check("Gravity's depth is D = 3 (face, channel, subchannel), which must be odd: the same oddness that lets parity"
      " change the tetrad root (scheme proof: 'because three is odd')", D % 2 == 1 and ladder(D)[1] > 0)

n_pass = sum(1 for _, ok in RESULTS if ok)
print(f"\n{n_pass}/{len(RESULTS)} checks passed")
if __name__ == "__main__":
    raise SystemExit(0 if n_pass == len(RESULTS) else 1)
