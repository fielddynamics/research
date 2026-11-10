"""
verify_level_factor.py
======================

Part X of INTERSECTION_ALGEBRA.md: what the measured G already says about the
per-level factor, using the 21-fold amplification of any correction to it.

Geometry (archive definitions): the read circle has circumference lambda_C
(one rotation = one Compton period), so radius lambda_bar_C; a tile has length
r_e and subtends the angle theta = r_e / lambda_bar_C = alpha radians.
Tiles per turn N = 2 pi / theta.

The G formula then reads
    alpha_G = [per-level factor]^21 x 17/13 x [seam factor].
This script tests candidate per-level factors (arc, chord, sine, tangent,
per-turn probability) and seam factors against CODATA G, and derives the
range of second-order corrections the data allow.
"""
from __future__ import annotations

import math

RESULTS = []


def check(name, cond):
    RESULTS.append((name, bool(cond)))
    print(f"[{'PASS' if cond else 'FAIL'}] {name}")


ALPHA = 7.2973525693e-3          # CODATA 2018 (archive convention)
HBAR, C, M_E = 1.054571817e-34, 299792458.0, 9.1093837015e-31
G_MEAS, G_SIG = 6.67430e-11, 0.00015e-11
th = ALPHA
N = 2 * math.pi / th
scale = HBAR * C / M_E ** 2


def G(level, seam):
    return level ** 21 * 17 / 13 * seam * scale


def z(g):
    return (g - G_MEAS) / G_SIG


print("\n=== X1. The tile angle on the read circle is alpha ===")
lam_bar = HBAR / (M_E * C)
r_e = ALPHA * lam_bar
check("Read circle circumference lambda_C = 2 pi lambda_bar_C, so its radius is lambda_bar_C",
      abs(2 * math.pi * lam_bar - 2 * math.pi * HBAR / (M_E * C)) < 1e-25)
check("A tile r_e on that circle subtends theta = r_e / lambda_bar_C = alpha radians exactly", abs(r_e / lam_bar - ALPHA) < 1e-18)

print("\n=== X2. Which per-level factor survives the measured G? (seam fixed at (N+1)/N) ===")
seam = (N + 1) / N
cands = {
    "arc, theta": th,
    "chord, 2 sin(theta/2)": 2 * math.sin(th / 2),
    "sine, sin(theta)": math.sin(th),
    "tangent, tan(theta)": math.tan(th),
    "per-turn probability, theta/2pi": th / (2 * math.pi),
    "theta (1 + theta/2pi)": th * (1 + th / (2 * math.pi)),
}
zs = {}
for nm, v in cands.items():
    zs[nm] = z(G(v, seam))
    print(f"      {nm:34s} G = {G(v, seam):.6e}   z = {zs[nm]:+.3g}")
check("The arc theta fits (|z| < 1)", abs(zs["arc, theta"]) < 1)
check("The chord is excluded at > 2 sigma: its -theta^2/24 per level costs 21 theta^2/24 = 47 ppm", abs(zs["chord, 2 sin(theta/2)"]) > 2)
check("The sine (-theta^2/6), tangent (+theta^2/3), per-turn probability and theta(1+theta/2pi) are excluded far beyond 2 sigma",
      all(abs(zs[k]) > 5 for k in ("sine, sin(theta)", "tangent, tan(theta)", "per-turn probability, theta/2pi", "theta (1 + theta/2pi)")))

print("\n=== X3. Which seam factor, with the arc per level? ===")
seams = {"(N+1)/N = 1 + theta/2pi (per turn)": seam, "1 + theta (per radian)": 1 + th, "none": 1.0}
for nm, v in seams.items():
    print(f"      {nm:36s} z = {z(G(th, v)):+.3g}")
check("Only the per-turn seam fits: per radian (1 + theta) is excluded and no seam at all is excluded",
      abs(z(G(th, seam))) < 1 and abs(z(G(th, 1 + th))) > 5 and abs(z(G(th, 1.0))) > 5)
print("      => the data fix the mechanism's two measures: levels count the arc in RADIANS, the seam counts tiles per full TURN")

print("\n=== X4. The allowed second-order correction per level ===")
# per-level factor theta (1 + c theta^2): G scales by (1 + c theta^2)^21 ~ 1 + 21 c theta^2
base = G(th, seam)
lo = (G_MEAS - 2 * G_SIG - base) / base / (21 * th ** 2)
hi = (G_MEAS + 2 * G_SIG - base) / base / (21 * th ** 2)
print(f"      per-level factor theta (1 + c theta^2):  2-sigma range  {lo:+.4f} < c < {hi:+.4f}")
check("At 2 sigma the data allow -0.03 < c < +0.06 roughly: the arc (c = 0) is inside, chord (-1/24), sine (-1/6) and tangent (+1/3) are outside",
      lo < 0 < hi and not lo < -1 / 24 < hi and not lo < -1 / 6 < hi and not lo < 1 / 3 < hi)
eps_lo, eps_hi = (G_MEAS - 2 * G_SIG - base) / base / 21, (G_MEAS + 2 * G_SIG - base) / base / 21
print(f"      any relative change eps per level:        {1e6 * eps_lo:+.2f} ppm < eps < {1e6 * eps_hi:+.2f} ppm")
check("Each level's factor must equal theta = alpha to within about 2 ppm: the 21-fold amplification makes G a per-level precision test",
      abs(eps_lo) < 3e-6 and abs(eps_hi) < 3e-6)

n_pass = sum(1 for _, ok in RESULTS if ok)
print(f"\n{n_pass}/{len(RESULTS)} checks passed")
if __name__ == "__main__":
    raise SystemExit(0 if n_pass == len(RESULTS) else 1)
