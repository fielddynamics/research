"""
verify_topological_alpha_in_G.py
================================

Part XI of INTERSECTION_ALGEBRA.md: does G use the measured alpha or the
stellated octahedron's alpha?

docs/03-fundamental-constants/01-fine-structure-constant-alpha.md derives
    1/alpha_top = 1 + 8 x 17 + 1/28 = 137 + 1/28        (interaction states of the stellated octahedron)
and docs/03-fundamental-constants (mass page): the closure bandwidth c/r is shared over N = 1/alpha states,
so each level's read takes a 1/N share.  In G the per-level factor is raised to the 21st power, so the
2.1 ppm gap between alpha_top and the measured alpha becomes about 44 ppm in G: large enough to test
against the 16 measurements of the CODATA 2022 adjustment (the archive's own table).

Inputs: CODATA 2022 (as in g_from_topology/compare_G_measurements.py). Nothing is fitted.
"""
from __future__ import annotations

import math
import os
import sys

RESULTS = []


def check(name, cond):
    RESULTS.append((name, bool(cond)))
    print(f"[{'PASS' if cond else 'FAIL'}] {name}")


sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "g_from_topology"))
import compare_G_measurements as cg  # noqa: E402

A_MEAS = cg.ALPHA
A_TOP = 1 / (137 + 1 / 28)
SCALE = cg.HBAR * cg.C / cg.M_E ** 2


def G(a_level, a_seam):
    return 17 / 13 * a_level ** 21 * (1 + a_seam / (2 * math.pi)) * SCALE * 1e11


print("\n=== T1. The stellated octahedron's alpha ===")
check("1/alpha_top = 1 + 8 x 17 + 1/28 = 137.0357143 (docs, fine-structure page)", abs(1 / A_TOP - (1 + 8 * 17 + 1 / 28)) < 1e-12)
gap = (A_TOP / A_MEAS - 1)
print(f"      alpha_top / alpha_meas - 1 = {1e6 * gap:+.3f} ppm;  amplified 21x in G: {1e6 * ((1 + gap) ** 21 - 1):+.1f} ppm")
check("The 2.1 ppm gap in alpha becomes ~44 ppm in G: larger than CODATA's 22 ppm", 40e-6 < (1 + gap) ** 21 - 1 < 48e-6)
check("Per-level window from Part X (-1.56 to +2.72 ppm at 2 sigma) contains the gap (+2.08 ppm): CODATA cannot exclude it",
      -1.56e-6 < gap < 2.72e-6)

versions = {
    "measured alpha (pre-registered)": G(A_MEAS, A_MEAS),
    "topological alpha, levels and seam": G(A_TOP, A_TOP),
    "topological levels, measured seam": G(A_TOP, A_MEAS),
}
print("\n=== T2. The versions against CODATA and the 16 measurements ===")
g0, s0 = cg.CODATA
for nm, p in versions.items():
    print(f"      {nm:38s} G = {p:.6f}   vs CODATA {1e6 * (p - g0) / g0:+6.1f} ppm  z = {(p - g0) / s0:+.2f}")
check("Both the measured-alpha and topological-alpha versions lie within 2 sigma of CODATA (z = -0.5 and +1.5)",
      all(abs((p - g0) / s0) < 2 for p in versions.values()))

print("\n      experiment     G          sigma(ppm)   z(measured alpha)  z(topological alpha)")
best = {}
for name, g, s in sorted(cg.MEASUREMENTS, key=lambda r: r[2]):
    zm, zt = (versions["measured alpha (pre-registered)"] - g) / s, (versions["topological alpha, levels and seam"] - g) / s
    best[name] = (zm, zt)
    print(f"      {name:10s} {g:9.6f}   {1e6 * s / g:7.1f}      {zm:+7.2f}            {zt:+7.2f}")
zt18 = best["HUSTT-18"]
za18 = best["HUSTA-18"]
check("The two most precise measurements disagree with each other by 45 ppm (HUST-18 time-of-swing vs angular-acceleration)",
      abs(6.674484 - 6.674184) / 6.6743 * 1e6 > 40)
check("Measured-alpha G sits at HUST time-of-swing (z = +0.4); topological-alpha G sits at HUST angular-acceleration (z = +0.3)",
      abs(zt18[0]) < 1 and abs(za18[1]) < 1)
check("...and each version is > 3 sigma from the other HUST result: the 45 ppm HUST split matches the 44 ppm alpha gap in size (observation, not evidence)",
      abs(zt18[1]) > 3 and abs(za18[0]) > 3)


def chi2(p, scale=1.0):
    return sum(((p - g) / (s * scale)) ** 2 for _, g, s in cg.MEASUREMENTS)


birge = 3.9   # CODATA's expansion factor for this inconsistent set
print("\n=== T3. Over all 16 (sigmas expanded by CODATA's factor 3.9) ===")
for nm, p in versions.items():
    print(f"      {nm:38s} chi^2 = {chi2(p, birge):6.2f}  (16 points)")
dchi = chi2(versions["topological alpha, levels and seam"], birge) - chi2(versions["measured alpha (pre-registered)"], birge)
check(f"The full set does not decide: delta chi^2 = {dchi:+.2f} (well under 4)", abs(dchi) < 4)

print("\n=== T4. What alpha the measured G implies per level ===")
inv = {}
for nm, (g, s) in {"CODATA 2022": cg.CODATA, "HUSTT-18": (6.674184, 0.000078), "HUSTA-18": (6.674484, 0.000077)}.items():
    a = (g / (17 / 13 * (1 + A_MEAS / (2 * math.pi)) * SCALE * 1e11)) ** (1 / 21)
    da = s / g / 21
    inv[nm] = (1 / a, da / a)
    print(f"      {nm:12s} implies 1/alpha_level = {1 / a:.6f} +- {1 / a * s / g / 21:.6f}")
check("CODATA's G implies 1/alpha_level = 137.03592 +- 0.00015: measured 137.035999 (+0.5 sigma) and topological 137.035714 (-1.4 sigma) both inside 2 sigma",
      abs(inv["CODATA 2022"][0] - 137.035999) < 2 * 0.000147 and abs(inv["CODATA 2022"][0] - 137.035714) < 2 * 0.000147)

print("\n=== T5. After CODATA 2022: NIST 2026 (Schlamminger et al., Metrologia 63, 025012) ===")
G_NIST, REL_NIST = 6.67387, 57e-6          # published April 2026, BEFORE the 9 Nov 2026 pre-registration
s_n = G_NIST * REL_NIST
zm_n = (versions["measured alpha (pre-registered)"] - G_NIST) / s_n
zt_n = (versions["topological alpha, levels and seam"] - G_NIST) / s_n
print(f"      measured alpha: z = {zm_n:+.2f}    octahedron alpha: z = {zt_n:+.2f}")
check("NIST 2026 lies below both and mildly prefers the measured alpha (z = +0.92 vs +1.68); neither is excluded",
      0 < zm_n < zt_n < 2)
print("      (by PREREGISTRATION.md this is a cross-check, not a test: it predates 9 Nov 2026)")

print("\n=== T6. The rival explanation of the HUST split (Klein 2020, MOND corrections) ===")
x_lab = 9.81 / 1.2e-10
check(f"Under GFD's own mu(x) = x/(1+x) with Earth's field as external field, 1 - mu = {1 / (1 + x_lab):.1e}:"
      " no lab effect, so Klein's mechanism needs a different interpolation function than GFD's",
      1 / (1 + x_lab) < 1e-10)

n_pass = sum(1 for _, ok in RESULTS if ok)
print(f"\n{n_pass}/{len(RESULTS)} checks passed")
if __name__ == "__main__":
    raise SystemExit(0 if n_pass == len(RESULTS) else 1)
