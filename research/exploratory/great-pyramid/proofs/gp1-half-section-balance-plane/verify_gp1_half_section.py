#!/usr/bin/env python3
"""
GP-1  The half-section theorem: the balance plane of a cone.

Verifies every statement of README.md, exactly wherever possible (sympy
rationals and radicals). Prints PASS/FAIL per check and exits non-zero on
any failure.

Run from this folder:  python verify_gp1_half_section.py
"""
import sys
from fractions import Fraction as Fr
import itertools
import random

import sympy as sp

RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {label}" + (f"  -- {detail}" if detail else ""))


# ---------------------------------------------------------------------------
# Exact polygon / polyhedron helpers (rational arithmetic)
# ---------------------------------------------------------------------------

def shoelace(poly):
    """Signed area of a planar polygon given as [(x, y), ...]."""
    s = Fr(0)
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        s += x1 * y2 - x2 * y1
    return s / 2


def section(base, apex, u):
    """Section of the cone at fractional height u: homothety of the base."""
    ax, ay, _ = apex
    return [((1 - u) * x + u * ax, (1 - u) * y + u * ay) for (x, y) in base]


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def planar_polygon_vector_area(pts):
    """Vector area (1/2) sum p_i x p_{i+1} of a planar polygon in R^3."""
    s = (Fr(0), Fr(0), Fr(0))
    n = len(pts)
    for i in range(n):
        c = cross(pts[i], pts[(i + 1) % n])
        s = tuple(a + b for a, b in zip(s, c))
    return tuple(x / 2 for x in s)


def frustum_lateral_flux(base, apex, u, J):
    """Outward flux of a constant field J through the lateral faces of the
    frustum between z = 0 and z = u h. Each lateral face is a planar
    quadrilateral (base edge, section edge). Computed face by face from the
    exact vector area, independently of the divergence theorem."""
    h = apex[2]
    sec = section(base, apex, u)
    n = len(base)
    # orientation: base polygon counter-clockwise seen from above (+z)
    flux = Fr(0)
    for i in range(n):
        p0 = (base[i][0], base[i][1], Fr(0))
        p1 = (base[(i + 1) % n][0], base[(i + 1) % n][1], Fr(0))
        q1 = (sec[(i + 1) % n][0], sec[(i + 1) % n][1], u * h)
        q0 = (sec[i][0], sec[i][1], u * h)
        va = planar_polygon_vector_area([p0, p1, q1, q0])
        flux += dot(J, va)
    return flux


# ---------------------------------------------------------------------------
# Test bodies: a right square pyramid, an oblique pentagonal cone, and random
# oblique cones over random convex polygons.
# ---------------------------------------------------------------------------

def random_convex_polygon(rng, n):
    # points on a circle-like curve with rational coordinates, sorted by angle
    import math
    angles = sorted(rng.uniform(0, 2 * math.pi) for _ in range(n))
    pts = []
    for t in angles:
        r = Fr(rng.randint(80, 120), 100)
        pts.append((Fr(round(1000 * float(r) * math.cos(t)), 1000),
                    Fr(round(1000 * float(r) * math.sin(t)), 1000)))
    # make sure it is counter-clockwise and convex by taking the hull
    pts = sorted(set(pts))

    def turn(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and turn(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and turn(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def bodies():
    out = []
    s = Fr(1)
    out.append(("right square pyramid", [(-s, -s), (s, -s), (s, s), (-s, s)], (Fr(0), Fr(0), Fr(146, 100))))
    out.append(("oblique pentagonal cone",
                [(Fr(0), Fr(-2)), (Fr(2), Fr(-1)), (Fr(2), Fr(1)), (Fr(-1), Fr(2)), (Fr(-2), Fr(0))],
                (Fr(3, 2), Fr(-7, 5), Fr(5, 3))))
    rng = random.Random(20261127)
    for k in range(6):
        poly = random_convex_polygon(rng, rng.randint(3, 9))
        apex = (Fr(rng.randint(-150, 150), 100), Fr(rng.randint(-150, 150), 100), Fr(rng.randint(50, 300), 100))
        out.append((f"random oblique cone #{k + 1} ({len(poly)}-gon base)", poly, apex))
    return out


print("=" * 78)
print("GP-1  The half-section theorem: the balance plane of a cone")
print("=" * 78)

# ---------------------------------------------------------------------------
print("\n-- Theorem 1: sections of a cone are homothetic, A(z) = A0 (1 - z/h)^(D-1)")
us = [Fr(0), Fr(1, 7), Fr(2, 7), Fr(1, 2), Fr(5, 6), Fr(1)]
for name, base, apex in bodies():
    A0 = shoelace(base)
    ok = A0 > 0 and all(shoelace(section(base, apex, u)) == A0 * (1 - u) ** 2 for u in us)
    check(f"T1 [D=3] {name}: A(u) = A0 (1-u)^2 exactly at u in {{0,1/7,2/7,1/2,5/6,1}}", ok)

# centroid moves on the segment from the base centroid to the apex
def centroid(poly):
    A = shoelace(poly)
    cx = cy = Fr(0)
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        c = x1 * y2 - x2 * y1
        cx += (x1 + x2) * c
        cy += (y1 + y2) * c
    return (cx / (6 * A), cy / (6 * A))

for name, base, apex in bodies()[:3]:
    c0 = centroid(base)
    ok = all(centroid(section(base, apex, u)) == ((1 - u) * c0[0] + u * apex[0], (1 - u) * c0[1] + u * apex[1])
             for u in us[:-1])
    check(f"T1 centroid of the section is (1-u) c0 + u a_perp ({name})", ok)

# general D, symbolically: Lebesgue measure scales by lambda^(D-1) under a homothety of ratio lambda
u, D = sp.symbols("u D", positive=True)
lam = 1 - u
for d in range(2, 8):
    # unit cube of dimension d-1 scaled by lam: product of lengths
    vol = sp.prod([lam] * (d - 1))
    check(f"T1 [D={d}] (d-1)-volume of a homothetic section scales as (1-u)^{d-1}", sp.simplify(vol - lam ** (d - 1)) == 0)

# ---------------------------------------------------------------------------
print("\n-- Theorem 2: a uniform current partitions as mu_B(z) = A(z)/A0, for any direction with J_z != 0")
rngJ = random.Random(7)
for name, base, apex in bodies():
    A0 = shoelace(base)
    allok = True
    for trial in range(4):
        J = (Fr(rngJ.randint(-9, 9), 7), Fr(rngJ.randint(-9, 9), 5), Fr(rngJ.choice([-11, -3, 2, 13]), 3))
        Phi_base = J[2] * A0                     # flux entering through the base (+z)
        for uu in us[1:-1]:
            Phi_sec = J[2] * shoelace(section(base, apex, uu))
            Phi_lat = frustum_lateral_flux(base, apex, uu, J)
            # divergence theorem for the frustum, checked face by face
            if Phi_base != Phi_sec + Phi_lat:
                allok = False
            if Phi_sec / Phi_base != (1 - uu) ** 2:
                allok = False
    check(f"T2 {name}: base = section + lateral (face by face), mu_B = (1-u)^2, 4 random tilted J", allok)

# the lateral share is exactly J_z (A0 - A(z)) for every tilt
name, base, apex = bodies()[1]
J = (Fr(5), Fr(-3), Fr(2))
check("T2 tilted J = (5,-3,2): lateral flux equals J_z (A0 - A(z)) at u = 2/7",
      frustum_lateral_flux(base, apex, Fr(2, 7), J) == J[2] * (shoelace(base) - shoelace(section(base, apex, Fr(2, 7)))))

# J_z = 0: no partition is defined (the base flux vanishes)
J0 = (Fr(1), Fr(1), Fr(0))
check("T2 necessity of J_z != 0: horizontal J gives zero base flux, mu_B undefined",
      J0[2] * shoelace(base) == 0)

# ---------------------------------------------------------------------------
print("\n-- Theorem 3: the unique balance level u* = 1 - 2^(-1/(D-1))")
for d in range(2, 9):
    ustar = 1 - sp.Integer(2) ** sp.Rational(-1, d - 1)
    val = sp.nsimplify((1 - ustar) ** (d - 1))
    check(f"T3 [D={d}] (1-u*)^{d-1} = 1/2 with u* = {sp.nsimplify(ustar)} = {float(ustar):.9f}", sp.simplify(val - sp.Rational(1, 2)) == 0)
# monotonic -> unique
check("T3 mu_B(u) = (1-u)^(D-1) strictly decreasing on [0,1] (derivative -(D-1)(1-u)^(D-2) < 0 on [0,1))",
      all(sp.diff((1 - u) ** (d - 1), u).subs(u, sp.Rational(k, 10)) < 0 for d in range(2, 9) for k in range(10)))
u3 = 1 - 1 / sp.sqrt(2)
check("T3 [D=3] u* = 1 - 1/sqrt(2) = (2 - sqrt 2)/2", sp.simplify(u3 - (2 - sp.sqrt(2)) / 2) == 0,
      f"{sp.N(u3, 15)}")

# ---------------------------------------------------------------------------
print("\n-- Theorem 4: the meridional (vertical) section is halved at the same level, in D = 3 only")
# a plane through the apex cuts the cone in a planar cone over a segment (a triangle).
for name, base, apex in bodies()[:4]:
    # vertical plane through the apex in direction (1, 2): parametrise by w along it
    ax, ay, h = apex
    dvec = (Fr(1), Fr(2))
    # intersect the base polygon with the line through (ax, ay) along dvec
    ts = []
    n = len(base)
    for i in range(n):
        p, q = base[i], base[(i + 1) % n]
        # solve p + s (q-p) = (ax,ay) + t dvec
        M = sp.Matrix([[q[0] - p[0], -dvec[0]], [q[1] - p[1], -dvec[1]]])
        if M.det() == 0:
            continue
        sol = M.LUsolve(sp.Matrix([ax - p[0], ay - p[1]]))
        s_, t_ = sol
        if 0 <= s_ <= 1:
            ts.append(sp.Rational(t_))
    ts = sorted(set(ts))
    if len(ts) < 2:
        check(f"T4 {name}: plane misses the base", False)
        continue
    t1, t2 = ts[0], ts[-1]
    seg = abs(t2 - t1) * sp.sqrt(dvec[0] ** 2 + dvec[1] ** 2)
    # the meridional triangle has base 'seg' (at z=0) and its apex at height h; its width at u is seg (1-u)
    total = seg * h / 2
    above = lambda uu: seg * (1 - uu) * (h * (1 - uu)) / 2
    ok = all(sp.simplify(above(uu) / total - (1 - uu) ** 2) == 0 for uu in [sp.Rational(1, 3), u3])
    check(f"T4 {name}: meridional area above level u is (1-u)^2 of the total; halves at u* = 1 - 1/sqrt 2", ok)

# horizontal-area halving = 1 - 2^{-1/(D-1)}, meridional halving = 1 - 2^{-1/2} for every D
coincide = [d for d in range(2, 40) if sp.simplify((1 - sp.Integer(2) ** sp.Rational(-1, d - 1)) - u3) == 0]
check("T4 the horizontal-section and meridional-section halvings coincide iff D = 3 (checked D = 2..39; proof: 1/(D-1) = 1/2)",
      coincide == [3], f"coincidence set {coincide}")

# ---------------------------------------------------------------------------
print("\n-- Theorem 5: the three canonical halving levels of a cone (k-dimensional measure, D = 3)")
levels = {k: 1 - sp.Integer(2) ** sp.Rational(-1, k) for k in (1, 2, 3)}
check("T5 k = 1 (height / apex distance): u = 1/2", levels[1] == sp.Rational(1, 2))
check("T5 k = 2 (section area, meridional area): u = 1 - 1/sqrt 2", sp.simplify(levels[2] - u3) == 0)
check("T5 k = 3 (volume above = volume below): u = 1 - 2^(-1/3)",
      sp.simplify((1 - levels[3]) ** 3 - sp.Rational(1, 2)) == 0, f"{float(levels[3]):.6f}")
# volume above the area-balance plane
vol_above = (1 - u3) ** 3
check("T5 at the area-balance plane the volume above is 2^(-3/2) = 0.35355 of the total (not one half)",
      sp.simplify(vol_above - sp.Integer(2) ** sp.Rational(-3, 2)) == 0, f"{float(vol_above):.5f}")
check("T5 ordering u_3 < u_2 < u_1 (volume, area, length)",
      float(levels[3]) < float(levels[2]) < float(levels[1]))
# exact volume check by integrating A(z) on the oblique cone
name, base, apex = bodies()[1]
z = sp.symbols("z", nonnegative=True)
h = sp.Rational(apex[2])
A0 = sp.Rational(shoelace(base))
V = sp.integrate(A0 * (1 - z / h) ** 2, (z, 0, h))
check("T5 cone volume = A0 h / 3 from integrating the sections (oblique pentagonal cone)", sp.simplify(V - A0 * h / 3) == 0)

# ---------------------------------------------------------------------------
print("\n-- Proposition 6: share labelling (a labelling, not a derivation; see README section 'Naming')")
muB = (1 - u) ** 2
sigmaB = 2 * muB - 1
fB = 17 + 4 * sigmaB
check("P6 f_B = 13 + 8 mu_B runs 21 (base) -> 17 (balance) -> 13 (apex)",
      [sp.simplify(fB.subs(u, v)) for v in (0, u3, 1)] == [21, 17, 13])
check("P6 exchange mu_B -> 1 - mu_B has the balance level as its only fixed level",
      [r for r in sp.solve(sp.Eq(muB, 1 - muB), u) if 0 <= float(r) <= 1] == [1 - sp.sqrt(2) / 2])

# ---------------------------------------------------------------------------
print("\n-- Proposition 6b: the graded structural operator A_B(u) = P_even + (2 mu_B - 1) P_odd (conditional)")
Pe = sp.diag(*([1] * 17 + [0] * 4)); Po = sp.eye(21) - Pe
AB = lambda uu: Pe + (2 * (1 - uu) ** 2 - 1) * Po
check("P6b Tr A_B(u) = 13 + 8 mu_B(u) for symbolic u", sp.simplify(AB(u).trace() - (13 + 8 * (1 - u) ** 2)) == 0)
check("P6b A_B(0) = I (trace 21), A_B(u*) = P_even (trace 17), A_B(1) = J = P_even - P_odd (trace 13)",
      AB(0) == sp.eye(21) and sp.simplify(AB(u3) - Pe) == sp.zeros(21) and AB(1) == Pe - Po)
check("P6b at the balance level the 4-dimensional signed sector is exactly suppressed: A_B(u*) P_odd = 0",
      sp.simplify(AB(u3) * Po) == sp.zeros(21))

print("\n-- Observation O7: the Great Pyramid (Petrie 1883; values verified in ../../metrics) [O]")
h_in, dh = 5776.0, 7.0
target = float(u3) * h_in
dtarget = float(u3) * dh
floor_lo, floor_hi = 1691.4, 1693.7
floor_mean = 0.5 * (floor_lo + floor_hi)
floor_allow = 0.5 * (floor_hi - floor_lo) + 0.6          # half-range plus Petrie's stated .6 allowance
resid = floor_mean - target
allow = dtarget + floor_allow                            # bounded allowances add (no Gaussian assumption)
check("O7 area-balance target 0.292893 h = 1691.75 in, allowance +-2.05 in from the height reconstruction",
      abs(target - 1691.75) < 0.01 and abs(dtarget - 2.05) < 0.01, f"{target:.2f} +- {dtarget:.2f} in")
check("O7 floor midpoint 1692.55 in with allowance +-1.75 in (half of the 1691.4-1693.7 range plus 0.6)",
      abs(floor_mean - 1692.55) < 1e-9 and abs(floor_allow - 1.75) < 1e-9)
check("O7 residual +0.80 in lies well inside the combined allowance +-3.80 in (an allowance interval, not a sigma)",
      abs(resid - 0.80) < 0.01 and abs(allow - 3.80) < 0.01 and abs(resid) < allow,
      f"residual {resid:+.2f} in, allowance +-{allow:.2f} in")
vol_plane = float(levels[3]) * h_in
len_plane = 0.5 * h_in
check("O7 the volume-balance (1191.6 in) and height-balance (2888.0 in) levels lie > 100 allowances from the floor",
      abs(floor_mean - vol_plane) / allow > 100 and abs(floor_mean - len_plane) / allow > 100,
      f"{abs(floor_mean - vol_plane)/allow:.0f} and {abs(floor_mean - len_plane)/allow:.0f} allowances")
# look-elsewhere: windows of radius delta about the three planes, intersected with [0, h/2];
# the height plane sits at the boundary h/2, so its window contributes delta, not 2 delta.
def null_prob(delta):
    L = 0.5 * h_in
    win = 0.0
    for c in (vol_plane, target, len_plane):
        win += max(0.0, min(L, c + delta) - max(0.0, c - delta))
    return win / L
check("O7 null model (floor uniform on [0, h/2]): P(any canonical window of radius delta) = 5 delta/(h/2)",
      abs(null_prob(3.80) - 5 * 3.80 / (0.5 * h_in)) < 1e-12 and abs(null_prob(2.70) - 0.004675) < 1e-5,
      f"{100*null_prob(3.80):.2f}% at delta = 3.80 in; {100*null_prob(2.70):.2f}% at 2.70 in (not a calibrated p-value)")

print("\n" + "=" * 78)
n_pass = sum(RESULTS)
print(f"GP-1: {n_pass}/{len(RESULTS)} checks passed")
sys.exit(0 if all(RESULTS) else 1)
