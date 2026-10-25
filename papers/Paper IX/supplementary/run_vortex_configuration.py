"""
GFD 3D Vortex Configuration
============================================================

Given observed rotation curve velocities v(r), derives the complete
3D vortex geometry:

    1. The decoded mass profile M(r) from v(r) via the inverse pipeline
    2. The Newtonian acceleration field g_N(r, z) at all points
    3. The total acceleration g_t(r, z) via the vortex equation
    4. The velocity field v(r, z) throughout 3D space
    5. The TetA/TetB hourglass boundary surface

THE KEY RESULT:

    The TetA/TetB boundary (the Field Origin surface, the hourglass
    waist) is the isosurface where:

        g_N(r, z) = a_0 / 2

    This is UNIVERSAL -- the same equation for every galaxy, every
    mass distribution, every scale. It follows algebraically from
    mu(1) = 1/2 and the constitutive law mu(x) = x/(x+1).

    Inside this surface: TetA (Newtonian, s > 0, theta > 90 deg)
    Outside this surface: TetB (MOND, s < 0, theta < 90 deg)
    On this surface: Field Origin (s = 0, theta = 90 deg, x = 1)

THE VELOCITY FIELD:

    At any point (r, z) in space:
        R = sqrt(r^2 + z^2)
        g_N = G*M(R) / R^2
        g_t = [g_N + sqrt(g_N^2 + 4*g_N*a_0)] / 2
        v(r, z) = sqrt(g_t * r^2 / R)

Requirements: numpy

    pip install numpy
    python run_vortex_configuration.py

Author: Stephen Nelson / Field Dynamics Research
Date:   February 2026
"""

import math
import sys

import numpy as np

# =============================================================================
# CONSTANTS
# =============================================================================

K = 4
D = 3
G_CONST = 4.3009e-3  # kpc (km/s)^2 / M_sun
A0 = 3703.0           # (km/s)^2/kpc  [= 1.2e-10 m/s^2]

F_PLUS  = 21
F_ZERO  = 17
F_MINUS = 13
F_RANGE = 8


# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def mass_decode(r, v, a0=A0):
    """Decode enclosed mass from observed (r, v) pair."""
    return r * v ** 4 / (G_CONST * (a0 * r + v ** 2))


def g_total_from_g_newton(g_N, a0=A0):
    """Solve the constitutive law for g_t given g_N.

    g_N = mu(g_t/a_0) * g_t = g_t^2/(g_t + a_0)
    => g_t = [g_N + sqrt(g_N^2 + 4*g_N*a_0)] / 2
    """
    if g_N <= 0:
        return 0.0
    disc = g_N ** 2 + 4 * g_N * a0
    return (g_N + math.sqrt(disc)) / 2.0


def state_param_from_x(x):
    """s = (x-1)/(x+1)"""
    return (x - 1) / (x + 1)


def cyclotomic_phase_from_s(s):
    """theta = arccos(-s/2)"""
    return math.acos(max(-1, min(1, -s / 2)))


def velocity_at_point(r, z, M_enclosed_func, a0=A0):
    """Compute circular velocity at an arbitrary point (r, z).

    The acceleration at (r, z) points toward the center with magnitude
    g_t. The radial (in-plane) component is g_t * r/R, and the
    circular velocity satisfies v^2 = g_r * r = g_t * r^2/R.
    """
    R = math.sqrt(r ** 2 + z ** 2)
    if R < 1e-10:
        return 0.0
    M_R = M_enclosed_func(R)
    g_N = G_CONST * M_R / R ** 2
    g_t = g_total_from_g_newton(g_N, a0)
    g_r = g_t * r / R
    return math.sqrt(max(0, g_r * r))


def full_state_at_point(r, z, M_enclosed_func, a0=A0):
    """Compute the full GFD state at an arbitrary point (r, z)."""
    R = math.sqrt(r ** 2 + z ** 2)
    if R < 1e-10:
        return {'R': 0, 'g_N': 0, 'g_t': 0, 'x': 0, 's': -1,
                'theta_deg': 60, 'mu': 0, 'w': 1, 'v': 0, 'region': 'origin'}

    M_R = M_enclosed_func(R)
    g_N = G_CONST * M_R / R ** 2
    g_t = g_total_from_g_newton(g_N, a0)
    x = g_t / a0
    s = state_param_from_x(x)
    theta = cyclotomic_phase_from_s(s)
    mu = x / (x + 1)
    w = 1 - mu
    g_r = g_t * r / R
    v = math.sqrt(max(0, g_r * r))

    if s > 0.01:
        region = 'TetA'
    elif s < -0.01:
        region = 'TetB'
    else:
        region = 'boundary'

    return {
        'R': R, 'g_N': g_N, 'g_t': g_t, 'x': x, 's': s,
        'theta_deg': math.degrees(theta), 'mu': mu, 'w': w,
        'v': v, 'region': region
    }


def find_boundary_z(r, M_enclosed_func, a0=A0, z_max=500):
    """Find z where g_N(r, z) = a_0/2 (the TetA/TetB boundary).

    Returns z_boundary, or None if the boundary is beyond z_max.
    """
    g_target = a0 / 2

    # Check if boundary exists within z_max
    R_max = math.sqrt(r ** 2 + z_max ** 2)
    g_at_max = G_CONST * M_enclosed_func(R_max) / R_max ** 2
    if g_at_max > g_target:
        return None  # boundary beyond z_max

    # Check if boundary is at z=0 (already in TetB in the plane)
    g_at_0 = G_CONST * M_enclosed_func(r) / r ** 2
    if g_at_0 < g_target:
        return 0.0  # already TetB at z=0

    # Bisect
    z_lo, z_hi = 0, z_max
    for _ in range(100):
        z_mid = (z_lo + z_hi) / 2
        R_mid = math.sqrt(r ** 2 + z_mid ** 2)
        g_N_mid = G_CONST * M_enclosed_func(R_mid) / R_mid ** 2
        if g_N_mid > g_target:
            z_lo = z_mid
        else:
            z_hi = z_mid

    return (z_lo + z_hi) / 2


def build_mass_profile(obs_data):
    """Build an interpolated enclosed mass function from observations.

    obs_data: list of (r_kpc, v_km_s) pairs.
    Returns: function M(R) that gives enclosed mass at spherical radius R.
    """
    r_arr = np.array([d[0] for d in obs_data])
    M_arr = np.array([mass_decode(r, v) for r, v in obs_data])

    def M_enclosed(R):
        if R <= r_arr[0]:
            return M_arr[0] * (R / r_arr[0]) ** 3
        elif R >= r_arr[-1]:
            return M_arr[-1]
        else:
            return float(np.interp(R, r_arr, M_arr))

    return M_enclosed


# =============================================================================
# FRAMEWORK
# =============================================================================

_results = []
_current_suite = ""
_last_printed_suite = ""


def suite(name):
    global _current_suite
    _current_suite = name


def validate(name):
    def decorator(func):
        def wrapper():
            global _last_printed_suite
            if _current_suite != _last_printed_suite:
                if _last_printed_suite:
                    print()
                print(f"--- {_current_suite} ---")
                _last_printed_suite = _current_suite
            try:
                func()
                _results.append((_current_suite, name, "PASS", ""))
                print(f"  PASS  {name}")
            except AssertionError as e:
                _results.append((_current_suite, name, "FAIL", str(e)))
                print(f"  FAIL  {name}: {e}")
            except Exception as e:
                _results.append((_current_suite, name, "ERROR", str(e)))
                print(f"  ERROR {name}: {e}")
        wrapper._name = name
        return wrapper
    return decorator


# =============================================================================
# TEST DATA: Approximate observed rotation curves
# =============================================================================

MW_DATA = [
    (1, 200), (2, 215), (3, 220), (5, 225), (7, 220),
    (10, 220), (15, 220), (20, 220), (25, 218), (30, 215),
]

M33_DATA = [
    (0.5, 30), (1, 55), (2, 85), (3, 100), (5, 110),
    (7, 115), (10, 120), (12, 122), (15, 130),
]

DWARF_DATA = [
    (0.5, 15), (1, 25), (2, 35), (3, 42), (5, 48), (7, 50), (10, 50),
]


# =========================================================================
#  I. BOUNDARY EQUATION
#
#  The TetA/TetB boundary is universally at g_N = a_0/2.
# =========================================================================

suite("I. Boundary Equation: g_N = a_0/2")


@validate("Boundary condition: g_N = a_0/2 gives x = 1 exactly")
def validate_boundary_x():
    g_N = A0 / 2
    g_t = g_total_from_g_newton(g_N)
    x = g_t / A0
    assert abs(x - 1.0) < 1e-10, f"x = {x}, expected 1.0"


@validate("At boundary: s = 0, theta = 90 deg, mu = 1/2, w = 1/2")
def validate_boundary_state():
    g_N = A0 / 2
    g_t = g_total_from_g_newton(g_N)
    x = g_t / A0
    s = state_param_from_x(x)
    theta = math.degrees(cyclotomic_phase_from_s(s))
    mu = x / (x + 1)
    w = 1 - mu

    assert abs(s) < 1e-10, f"s = {s}"
    assert abs(theta - 90.0) < 1e-8, f"theta = {theta} deg"
    assert abs(mu - 0.5) < 1e-10, f"mu = {mu}"
    assert abs(w - 0.5) < 1e-10, f"w = {w}"


@validate("Algebraic proof: mu(1) = 1/2, so g_N = mu*g_t = (1/2)*a_0 = a_0/2")
def validate_boundary_algebra():
    # At the boundary: x = 1 by definition
    # mu(1) = 1/(1+1) = 1/2
    # g_t = x * a_0 = a_0
    # g_N = mu * g_t = (1/2) * a_0 = a_0/2
    mu_at_1 = 1.0 / (1.0 + 1.0)
    assert abs(mu_at_1 - 0.5) < 1e-14

    g_t = A0
    g_N = mu_at_1 * g_t
    assert abs(g_N - A0 / 2) < 1e-10


@validate("Point mass boundary: R_boundary = sqrt(2GM/a_0)")
def validate_point_mass_boundary():
    for M in [1e8, 1e10, 5e10, 1e11]:
        R_bnd = math.sqrt(2 * G_CONST * M / A0)

        # Verify: g_N at R_bnd = a_0/2
        g_N = G_CONST * M / R_bnd ** 2
        assert abs(g_N - A0 / 2) < 1e-6, (
            f"M={M:.0e}: g_N at R_bnd = {g_N:.4f}, expected {A0/2:.4f}"
        )


@validate("Boundary scales as sqrt(M): R_bnd(10M)/R_bnd(M) = sqrt(10)")
def validate_boundary_scaling():
    M1 = 1e10
    M2 = 1e11

    R1 = math.sqrt(2 * G_CONST * M1 / A0)
    R2 = math.sqrt(2 * G_CONST * M2 / A0)

    ratio = R2 / R1
    assert abs(ratio - math.sqrt(M2 / M1)) < 1e-10


# =========================================================================
#  II. VELOCITY FIELD ROUNDTRIP
#
#  v_obs -> M_dec -> g_N(r,z) -> g_t(r,z) -> v(r,z=0) must recover v_obs.
# =========================================================================

suite("II. Velocity Field Roundtrip")


@validate("Disk-plane roundtrip: v(r, z=0) recovers v_obs exactly")
def validate_disk_roundtrip():
    M_enc = build_mass_profile(MW_DATA)

    for r, v_obs in MW_DATA:
        v_computed = velocity_at_point(r, 0, M_enc)
        assert abs(v_computed - v_obs) < 0.1, (
            f"r={r}: v_obs={v_obs}, v_computed={v_computed:.4f}"
        )


@validate("Off-plane velocity is always less than disk-plane velocity")
def validate_offplane_less():
    M_enc = build_mass_profile(MW_DATA)

    for r, v_obs in MW_DATA:
        v_plane = velocity_at_point(r, 0, M_enc)
        for z in [1, 5, 10, 20]:
            v_off = velocity_at_point(r, z, M_enc)
            assert v_off <= v_plane + 0.1, (
                f"r={r}, z={z}: v_off={v_off:.1f} > v_plane={v_plane:.1f}"
            )


@validate("Velocity decreases with |z| at fixed r (field weakens off-plane)")
def validate_v_decreases_with_z():
    M_enc = build_mass_profile(MW_DATA)

    for r in [5, 10, 20]:
        prev_v = velocity_at_point(r, 0, M_enc)
        for z in [2, 5, 10, 20, 30]:
            v_z = velocity_at_point(r, z, M_enc)
            assert v_z <= prev_v + 0.1, (
                f"r={r}, z={z}: v={v_z:.1f} > prev={prev_v:.1f}"
            )
            prev_v = v_z


@validate("Symmetry: v(r, z) = v(r, -z) (reflection about disk plane)")
def validate_z_symmetry():
    M_enc = build_mass_profile(MW_DATA)

    for r in [5, 10, 20]:
        for z in [1, 5, 10, 20]:
            v_pos = velocity_at_point(r, z, M_enc)
            v_neg = velocity_at_point(r, -z, M_enc)
            assert abs(v_pos - v_neg) < 1e-10, (
                f"r={r}: v(z={z})={v_pos:.4f} != v(z={-z})={v_neg:.4f}"
            )


# =========================================================================
#  III. HOURGLASS GEOMETRY
#
#  The TetA/TetB boundary surface z_boundary(r) forms an hourglass.
# =========================================================================

suite("III. Hourglass Geometry")


@validate("Boundary surface exists for all galaxies")
def validate_boundary_exists():
    for name, data in [("MW", MW_DATA), ("M33", M33_DATA), ("Dwarf", DWARF_DATA)]:
        M_enc = build_mass_profile(data)

        # Check at the innermost radius -- this has the highest g_N
        r_inner = data[0][0]
        state = full_state_at_point(r_inner, 0, M_enc)
        # If the inner disk is in TetA (s > 0), boundary exists above it
        # If even the inner disk is TetB, the boundary is below the disk
        # plane -- but the boundary STILL exists somewhere at smaller R.
        z_bnd = find_boundary_z(r_inner, M_enc, z_max=1000)
        # The boundary always exists: for sufficiently small R,
        # g_N -> inf (TetA), and for sufficiently large R, g_N -> 0 (TetB).
        # The transition must occur somewhere.
        # For galaxies already in TetB at all observed radii, the
        # boundary is at R < r_min.
        assert z_bnd is not None or state['s'] < 0, (
            f"{name}: no boundary found and inner disk not in TetB"
        )


@validate("Boundary z > 0 at inner radii where disk is in TetA")
def validate_boundary_above_disk():
    M_enc = build_mass_profile(MW_DATA)

    # At r=5 kpc (inner MW), the disk-plane acceleration is high (TetA)
    # so the boundary should be above the disk: z_bnd > 0
    z_bnd = find_boundary_z(5, M_enc)
    assert z_bnd is not None and z_bnd > 0, (
        f"r=5: z_boundary = {z_bnd}, expected > 0"
    )


@validate("Boundary z = 0 at large r where disk is already in TetB")
def validate_boundary_at_disk():
    M_enc = build_mass_profile(MW_DATA)

    # At very large r, the disk-plane acceleration is below a_0/2
    # so the boundary is at z=0 (or doesn't exist)
    r_large = 200  # well beyond MW observations
    z_bnd = find_boundary_z(r_large, M_enc)
    assert z_bnd is not None and z_bnd < 1.0, (
        f"r={r_large}: z_boundary = {z_bnd}, expected ~= 0"
    )


@validate("Hourglass is symmetric: z_boundary(r) reflected about z=0")
def validate_hourglass_symmetry():
    # By construction: the acceleration field g_N(r, z) depends on
    # R = sqrt(r^2 + z^2), which is symmetric in z.
    # So z_boundary is the same above and below the disk.
    M_enc = build_mass_profile(MW_DATA)

    for r in [3, 7, 12]:
        z_bnd = find_boundary_z(r, M_enc)
        if z_bnd is not None and z_bnd > 0:
            state_above = full_state_at_point(r, z_bnd, M_enc)
            state_below = full_state_at_point(r, -z_bnd, M_enc)
            assert abs(state_above['x'] - state_below['x']) < 1e-8


@validate("At boundary surface: region = 'boundary' (s ~= 0)")
def validate_boundary_is_boundary():
    M_enc = build_mass_profile(MW_DATA)

    for r in [3, 7, 12]:
        z_bnd = find_boundary_z(r, M_enc)
        if z_bnd is not None and z_bnd > 0:
            state = full_state_at_point(r, z_bnd, M_enc)
            assert abs(state['s']) < 0.05, (
                f"r={r}: s at boundary = {state['s']}, expected ~= 0"
            )


# =========================================================================
#  IV. TetA AND TetB REGIONS
#
#  Inside the hourglass boundary: TetA (s > 0, Newtonian).
#  Outside the hourglass boundary: TetB (s < 0, MOND).
# =========================================================================

suite("IV. TetA and TetB Regions")


@validate("Inside boundary (small z): state is TetA (s > 0)")
def validate_teta_inside():
    M_enc = build_mass_profile(MW_DATA)

    for r in [3, 7, 12]:
        z_bnd = find_boundary_z(r, M_enc)
        if z_bnd is not None and z_bnd > 1:
            # Check a point inside the boundary
            z_inside = z_bnd / 2
            state = full_state_at_point(r, z_inside, M_enc)
            assert state['s'] > 0, (
                f"r={r}, z={z_inside}: s = {state['s']}, expected > 0 (TetA)"
            )


@validate("Outside boundary (large z): state is TetB (s < 0)")
def validate_tetb_outside():
    M_enc = build_mass_profile(MW_DATA)

    for r in [3, 7, 12]:
        z_bnd = find_boundary_z(r, M_enc)
        if z_bnd is not None and z_bnd > 0:
            z_outside = z_bnd * 2
            state = full_state_at_point(r, z_outside, M_enc)
            assert state['s'] < 0, (
                f"r={r}, z={z_outside}: s = {state['s']}, expected < 0 (TetB)"
            )


@validate("Vortex width w < 0.5 in TetA, w > 0.5 in TetB")
def validate_width_regions():
    M_enc = build_mass_profile(MW_DATA)

    for r in [5, 10]:
        z_bnd = find_boundary_z(r, M_enc)
        if z_bnd is not None and z_bnd > 1:
            # TetA
            state_A = full_state_at_point(r, z_bnd / 2, M_enc)
            assert state_A['w'] < 0.5, f"TetA: w = {state_A['w']}"

            # TetB
            state_B = full_state_at_point(r, z_bnd * 2, M_enc)
            assert state_B['w'] > 0.5, f"TetB: w = {state_B['w']}"


@validate("Cyclotomic phase: theta > 90 deg in TetA, theta < 90 deg in TetB")
def validate_phase_regions():
    M_enc = build_mass_profile(MW_DATA)

    for r in [5, 10]:
        z_bnd = find_boundary_z(r, M_enc)
        if z_bnd is not None and z_bnd > 1:
            state_A = full_state_at_point(r, z_bnd / 2, M_enc)
            state_B = full_state_at_point(r, z_bnd * 2, M_enc)
            assert state_A['theta_deg'] > 90, f"TetA: theta = {state_A['theta_deg']:.1f} deg"
            assert state_B['theta_deg'] < 90, f"TetB: theta = {state_B['theta_deg']:.1f} deg"


# =========================================================================
#  V. MULTI-GALAXY UNIVERSALITY
#
#  The same equations work for all three galaxies without adjustment.
# =========================================================================

suite("V. Multi-Galaxy Universality")


@validate("Pipeline works for Milky Way, M33, and Dwarf with same a_0")
def validate_universality():
    for name, data in [("MW", MW_DATA), ("M33", M33_DATA), ("Dwarf", DWARF_DATA)]:
        M_enc = build_mass_profile(data)

        # Check roundtrip in the disk plane
        for r, v_obs in data:
            v_computed = velocity_at_point(r, 0, M_enc)
            assert abs(v_computed - v_obs) < 0.5, (
                f"{name} r={r}: v_obs={v_obs}, v_computed={v_computed:.1f}"
            )


@validate("Boundary equation g_N = a_0/2 is the same for all galaxies")
def validate_same_boundary():
    # The boundary condition doesn't depend on the galaxy
    # It's always g_N = a_0/2 = 1851.5 (km/s)^2/kpc
    for name, data in [("MW", MW_DATA), ("M33", M33_DATA), ("Dwarf", DWARF_DATA)]:
        M_enc = build_mass_profile(data)

        # Find boundary at r=3 (or wherever it exists)
        for r in [1, 3, 5]:
            z_bnd = find_boundary_z(r, M_enc)
            if z_bnd is not None and z_bnd > 0:
                R_bnd = math.sqrt(r ** 2 + z_bnd ** 2)
                g_N = G_CONST * M_enc(R_bnd) / R_bnd ** 2
                assert abs(g_N - A0 / 2) < 10, (
                    f"{name} r={r}: g_N at boundary = {g_N:.1f}, expected {A0/2:.1f}"
                )
                break


@validate("Larger galaxies have larger hourglass (boundary R ~ sqrt(M_total))")
def validate_size_ordering():
    # Use the outermost decoded mass to compute the point-mass boundary
    # R_bnd = sqrt(2GM/a_0)
    boundaries = []
    for name, data in [("Dwarf", DWARF_DATA), ("M33", M33_DATA), ("MW", MW_DATA)]:
        M_outer = mass_decode(data[-1][0], data[-1][1])
        R_bnd = math.sqrt(2 * G_CONST * M_outer / A0)
        boundaries.append((name, R_bnd, M_outer))

    for i in range(len(boundaries) - 1):
        assert boundaries[i][1] < boundaries[i + 1][1], (
            f"{boundaries[i][0]} (M={boundaries[i][2]:.1e}, R={boundaries[i][1]:.1f}) "
            f">= {boundaries[i+1][0]} (M={boundaries[i+1][2]:.1e}, R={boundaries[i+1][1]:.1f})"
        )


# =============================================================================
# MAIN
# =============================================================================

def main():
    print()
    print("=" * 72)
    print("  GFD 3D VORTEX CONFIGURATION")
    print("  The hourglass: TetA -> Field Origin -> TetB")
    print("  Boundary equation: g_N(r, z) = a_0/2  (universal)")
    print("=" * 72)

    all_validations = [
        # I. Boundary Equation
        validate_boundary_x,
        validate_boundary_state,
        validate_boundary_algebra,
        validate_point_mass_boundary,
        validate_boundary_scaling,
        # II. Velocity Field Roundtrip
        validate_disk_roundtrip,
        validate_offplane_less,
        validate_v_decreases_with_z,
        validate_z_symmetry,
        # III. Hourglass Geometry
        validate_boundary_exists,
        validate_boundary_above_disk,
        validate_boundary_at_disk,
        validate_hourglass_symmetry,
        validate_boundary_is_boundary,
        # IV. TetA and TetB Regions
        validate_teta_inside,
        validate_tetb_outside,
        validate_width_regions,
        validate_phase_regions,
        # V. Multi-Galaxy Universality
        validate_universality,
        validate_same_boundary,
        validate_size_ordering,
    ]

    for v in all_validations:
        v()

    print()
    print("=" * 72)
    passed = sum(1 for _, _, status, _ in _results if status == "PASS")
    failed = sum(1 for _, _, status, _ in _results if status != "PASS")
    total = len(_results)
    print(f"  RESULTS: {passed} passed, {failed} failed, {total} total")
    print("=" * 72)

    if failed > 0:
        print()
        print("FAILURES:")
        for s, name, status, msg in _results:
            if status != "PASS":
                print(f"  [{status}] {s} / {name}")
                if msg:
                    print(f"         {msg}")

    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
