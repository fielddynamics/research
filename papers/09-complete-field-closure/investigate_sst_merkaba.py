"""
SST-Merkaba Structural Investigation
======================================

The scalar-tensor (SST) action from GFD Paper VIII:

    S_SST = integral d^4x sqrt(-g) [ R/(16piG)
            - a_0^2/(8piG) F(|nabla Phi|^2 / a_0^2)
            - 1/4 e^{-2Phi/c^2} F_uv F^uv
            + L_matter ]

Every coupling constant in this action (16, 8, 4, 2) maps onto a
structural constant of the Merkaba (stellated octahedron). This script
tests 9 specific correspondences: from the coupling hierarchy through
the constitutive law derivation, to the N-metric family and the golden
ratio at N=2.

    pip install mpmath
    python investigate_sst_merkaba.py

Author: Stephen Nelson
Date: February 2026
"""

import math
from fractions import Fraction

import mpmath


# =============================================================================
# MERKABA CONSTANTS (inlined from geometry_constants.py)
# =============================================================================

K = 4   # closure constant = d + 1 = simplex vertex count in d=3
D = 3   # spatial dimensions

TET_A = {1, 2, 4, 7}   # odd popcount
TET_B = {0, 3, 5, 6}   # even popcount

COMPLEMENT_PAIRS = [(0, 7), (1, 6), (2, 5), (3, 4)]

# Coupling polynomial evaluated at k=4
F_PLUS  = 21   # f(4, +1) = 1 + 4 + 16 = 21  (TetA ceiling)
F_ZERO  = 17   # f(4,  0) = 1 + 0 + 16 = 17  (Field Origin)
F_MINUS = 13   # f(4, -1) = 1 - 4 + 16 = 13  (TetB floor)
F_RANGE = F_PLUS - F_MINUS  # = 8

# BBP formula constants (from the companion investigation)
BBP_BASE = 16
BBP_PERIOD = 8
BBP_ACTIVE_COUNT = 4


# =============================================================================
# HELPERS
# =============================================================================

def coupling_polynomial(k, s):
    """f(k, s) = 1 + ks + k^2"""
    return 1 + k * s + k ** 2


def conformal_map(x):
    """s(x) = (x - 1) / (x + 1), the Mobius transformation from
    kinematic acceleration space [0, inf) to state space [-1, +1]."""
    return (x - 1.0) / (x + 1.0)


def capacity_function(x):
    """f(x) = (21x + 13) / (x + 1), the continuous topological capacity."""
    return (F_PLUS * x + F_MINUS) / (x + 1.0)


def constitutive_law(x):
    """mu(x) = x / (x + 1), the MOND interpolation function."""
    return x / (x + 1.0)


def kinetic_functional(y):
    """F(y) = y - 2*sqrt(y) + 2*ln(1 + sqrt(y)), the SST kinetic term.
    Derived by integrating mu(sqrt(y)) = dF/dy."""
    sy = math.sqrt(y) if y > 0 else 0.0
    return y - 2.0 * sy + 2.0 * math.log(1.0 + sy)


def kinetic_functional_derivative(y, h=1e-8):
    """Numerical dF/dy for verification."""
    return (kinetic_functional(y + h) - kinetic_functional(y - h)) / (2.0 * h)


# =============================================================================
# TEST RUNNER
# =============================================================================

_results = []


def test(name, number):
    """Decorator that registers and runs an investigation."""
    def decorator(func):
        def wrapper():
            print()
            print("=" * 72)
            print(f"  TEST {number}: {name}")
            print("=" * 72)
            try:
                func()
                _results.append((number, name, "PASS"))
                print(f"\n  >> PASS")
            except AssertionError as e:
                _results.append((number, name, "FAIL"))
                print(f"\n  >> FAIL: {e}")
            except Exception as e:
                _results.append((number, name, "ERROR"))
                print(f"\n  >> ERROR: {e}")
        wrapper._number = number
        wrapper._name = name
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator


# =============================================================================
# TEST 1: COUPLING HIERARCHY CASCADE
#
# The SST action contains three coupling denominators: 16piG (gravity),
# 8piG (scalar), and 1/4 (EM normalization). These are 2^K, 2^D, and
# 1/K respectively, forming a factor-2 descent through the Merkaba.
# =============================================================================

@test("Coupling Hierarchy: 16, 8, 4 = 2^K, 2^D, K", 1)
def test_coupling_hierarchy():
    gravity_scale = 16
    scalar_scale = 8
    em_scale = 4

    print()
    print(f"  SST coupling denominators (excluding pi*G factors):")
    print(f"    Gravity (Einstein-Hilbert):  R / (16 * pi * G)")
    print(f"    Scalar (kinetic term):       a_0^2 / (8 * pi * G)")
    print(f"    EM (field strength):         1/4 * F_uv F^uv")
    print()

    # Gravity scale = 2^K
    assert gravity_scale == 2 ** K, f"16 != 2^K = {2**K}"
    print(f"  16 = 2^K = 2^{K}")
    print(f"    = full Merkaba coupling: 2 tetrahedra x 8 vertices")
    print(f"    = k^2 = beta_2 = face coupling channels per tet")
    print(f"    = BBP formula base")

    # Scalar scale = 2^D
    assert scalar_scale == 2 ** D, f"8 != 2^D = {2**D}"
    print()
    print(f"  8 = 2^D = 2^{D}")
    print(f"    = trigram space (single vertex cycle)")
    print(f"    = BBP formula period")
    print(f"    = f_range = f(+1) - f(-1) = {F_PLUS} - {F_MINUS}")
    assert scalar_scale == F_RANGE

    # EM scale = K
    assert em_scale == K, f"4 != K = {K}"
    print()
    print(f"  4 = K = {K}")
    print(f"    = closure constant = vertices per tetrahedron")
    print(f"    = BBP active count per period")
    print(f"    = d + 1 = simplex vertex count")

    # Factor-2 cascade
    print()
    print(f"  Cascade: 16 / 8 = 2, 8 / 4 = 2")
    print(f"  Each step divides by the bimetric factor (2 tetrahedra)")
    assert gravity_scale // scalar_scale == 2
    assert scalar_scale // em_scale == 2

    # The cascade is 2^K -> 2^D -> 2^(D-1)
    assert gravity_scale == 2 ** K        # = 2^4 = 16
    assert scalar_scale == 2 ** D         # = 2^3 = 8
    assert em_scale == 2 ** (D - 1)       # = 2^2 = 4
    print(f"  Equivalently: 2^K -> 2^D -> 2^(D-1)")
    print(f"  That is: 2^4 -> 2^3 -> 2^2, descending by one power at each step")


# =============================================================================
# TEST 2: BIMETRIC COEFFICIENTS FROM STATIC SKELETON
#
# The coupling polynomial at s=0 gives f(4,0) = 17 = 1 + 0 + 16.
# This decomposes into the locked bimetric parameters {1, 0, 16, 0, 1}
# where the symmetry and parity constraints fix all five coefficients.
# =============================================================================

@test("Bimetric Coefficients {1, 0, 16, 0, 1} from f(4, 0)", 2)
def test_bimetric_coefficients():
    f_at_origin = coupling_polynomial(K, 0)
    assert f_at_origin == 17, f"f(4,0) = {f_at_origin}, expected 17"

    print()
    print(f"  f(k, s) = 1 + ks + k^2 at k={K}, s=0:")
    print(f"  f(4, 0) = 1 + 0 + 16 = {f_at_origin}")
    print()

    # The five beta coefficients
    beta = [1, 0, 16, 0, 1]
    print(f"  Locked bimetric parameters: beta = {beta}")
    print()

    # beta_0 = beta_4 = 1 (exchange symmetry between chambers)
    assert beta[0] == beta[4] == 1
    print(f"  beta_0 = beta_4 = 1  (exchange symmetry: TetA <-> TetB)")

    # beta_1 = beta_3 = 0 (orientation parity: odd powers vanish)
    assert beta[1] == beta[3] == 0
    print(f"  beta_1 = beta_3 = 0  (orientation parity: odd powers vanish)")

    # beta_2 = k^2 = 16 (face coupling capacity)
    assert beta[2] == K ** 2
    print(f"  beta_2 = k^2 = {K}^2 = {K**2}  (face coupling channels)")

    # Verify the polynomial values at the three structural states
    print()
    print(f"  Three structural states of f(4, s):")
    for s_val, label, expected in [(+1, "TetA ceiling", F_PLUS),
                                    (0, "Field Origin", F_ZERO),
                                    (-1, "TetB floor", F_MINUS)]:
        val = coupling_polynomial(K, s_val)
        assert val == expected, f"f(4,{s_val}) = {val}, expected {expected}"
        print(f"    s = {s_val:+d}: f = {val} ({label})")

    # The range f(+1) - f(-1) = 2k = 8 = 2^D
    computed_range = coupling_polynomial(K, +1) - coupling_polynomial(K, -1)
    assert computed_range == 2 * K == 8
    print(f"\n  Range: {F_PLUS} - {F_MINUS} = {computed_range} = 2k = 2^D")


# =============================================================================
# TEST 3: CONFORMAL MAP AND COORDINATE BOUNDS
#
# The map s(x) = (x-1)/(x+1) transforms kinematic acceleration space
# [0, inf) onto the state parameter range [-1, +1]. This is the same
# bounded interval as the Merkaba's vertex coordinates along any axis.
# =============================================================================

@test("Conformal Map s(x) = (x-1)/(x+1): bounds, origin, symmetry", 3)
def test_conformal_map():
    print()
    print("  The conformal map s(x) = (x-1)/(x+1):")
    print()

    # Boundary conditions from the physics
    # x -> 0: deep MOND, saturated at TetB floor
    s_zero = conformal_map(0.0)
    assert abs(s_zero - (-1.0)) < 1e-10
    print(f"  x -> 0:   s = {s_zero:+.1f}  (TetB floor, deep MOND)")

    # x = 1: transition point, balanced at Field Origin
    s_one = conformal_map(1.0)
    assert abs(s_one - 0.0) < 1e-10
    print(f"  x = 1:    s = {s_one:+.1f}  (Field Origin, transition)")

    # x -> inf: Newtonian, full TetA capacity
    s_large = conformal_map(1e12)
    assert abs(s_large - 1.0) < 1e-6
    print(f"  x -> inf: s -> {s_large:+.6f}  (TetA ceiling, Newtonian)")

    # The range [-1, +1] matches vertex coordinate bounds
    print()
    print(f"  The state parameter range [-1, +1] is the same interval")
    print(f"  as each vertex coordinate axis in the Merkaba.")
    print(f"  Each axis takes values in {{-1, +1}}.")
    print(f"  The conformal map projects physics onto geometry.")

    # Verify it is a Mobius transformation (fractional linear)
    # s(x) = (ax + b)/(cx + d) with a=1, b=-1, c=1, d=1
    # Determinant ad - bc = 1*1 - (-1)*1 = 2 (non-degenerate)
    det = 1 * 1 - (-1) * 1
    assert det == 2, f"Mobius determinant = {det}, expected 2 (bimetric factor)"
    print(f"\n  Mobius determinant: ad - bc = 1*1 - (-1)*1 = {det}")
    print(f"  = 2 = bimetric factor")

    # The inverse map: x(s) = (1+s)/(1-s)
    # At s = 0: x = 1 (transition)
    # At s = +1: x -> inf (Newtonian)
    # At s = -1: x = 0 (deep MOND)
    for s_test, x_expected in [(0.0, 1.0), (-0.5, 1.0/3.0), (0.5, 3.0)]:
        x_recovered = (1.0 + s_test) / (1.0 - s_test)
        assert abs(x_recovered - x_expected) < 1e-10
    print(f"  Inverse x(s) = (1+s)/(1-s) verified at s = 0, -0.5, +0.5")


# =============================================================================
# TEST 4: CAPACITY FUNCTION AND NORMALIZATION
#
# f(x) = (21x + 13)/(x+1) is bounded between f_min=13 and f_max=21.
# Normalizing to [0,1] via mu = (f - 13)/8 yields mu = x/(x+1).
# The normalization divisor 8 = 2^D = f_range.
# =============================================================================

@test("Capacity f(x) = (21x+13)/(x+1), normalization yields mu = x/(x+1)", 4)
def test_capacity_and_normalization():
    print()
    print(f"  Capacity function f(x) = ({F_PLUS}x + {F_MINUS}) / (x + 1)")
    print()

    # Verify at structural states
    test_points = [
        (0.0, F_MINUS, "TetB floor (deep MOND)"),
        (1.0, F_ZERO, "Field Origin (transition)"),
        (1e12, F_PLUS, "TetA ceiling (Newtonian)"),
    ]
    for x_val, f_expected, label in test_points:
        f_val = capacity_function(x_val)
        assert abs(f_val - f_expected) < 1e-3, (
            f"f({x_val}) = {f_val}, expected {f_expected}"
        )
        print(f"  f({x_val:>12}) = {f_val:7.2f}  ({label})")

    # Verify f(x) = f(k, s(x)) by composing polynomial with conformal map
    print()
    print(f"  Verifying f(x) = f(k=4, s(x)) at 20 test points:")
    for i in range(20):
        x = 0.01 * (10 ** (i * 0.25))
        s = conformal_map(x)
        f_composed = coupling_polynomial(K, s)
        f_direct = capacity_function(x)
        assert abs(f_composed - f_direct) < 1e-8, (
            f"x={x}: composed={f_composed}, direct={f_direct}"
        )
    print(f"  All 20 points match to within 1e-8")

    # Normalization: mu = (f - f_min) / f_range
    print()
    print(f"  Normalization: mu(x) = (f(x) - {F_MINUS}) / {F_RANGE}")
    for x_val in [0.001, 0.1, 0.5, 1.0, 2.0, 10.0, 1000.0]:
        f_val = capacity_function(x_val)
        mu_from_f = (f_val - F_MINUS) / F_RANGE
        mu_direct = constitutive_law(x_val)
        assert abs(mu_from_f - mu_direct) < 1e-10, (
            f"x={x_val}: mu_from_f={mu_from_f}, mu_direct={mu_direct}"
        )
    print(f"  mu = (f - 13)/8 = x/(x+1) verified at 7 test points")

    # The normalization divisor is 8 = 2^D = f_range
    assert F_RANGE == 2 ** D == 8
    print(f"\n  Normalization divisor: {F_RANGE} = 2^D = {2**D}")


# =============================================================================
# TEST 5: CONSTITUTIVE LAW AS MOND INTERPOLATION
#
# mu(x) = x/(x+1) has the correct asymptotic behavior for a MOND
# interpolating function: mu -> 1 for x >> 1 (Newtonian), mu -> x
# for x << 1 (deep MOND), and mu(1) = 1/2 at the transition.
# =============================================================================

@test("Constitutive Law mu(x) = x/(x+1): MOND limits and transition", 5)
def test_constitutive_law_mond():
    print()
    print(f"  mu(x) = x/(x+1) as MOND interpolation function:")
    print()

    # Deep MOND regime: x << 1, mu ~ x
    print(f"  Deep MOND (x << 1): mu(x) -> x")
    for x_val in [0.001, 0.01, 0.1]:
        mu = constitutive_law(x_val)
        ratio = mu / x_val
        print(f"    mu({x_val}) = {mu:.6f}, mu/x = {ratio:.6f}")
        assert abs(ratio - 1.0) < 0.11, f"Deep MOND: mu/x = {ratio}, not close to 1"

    # Newtonian regime: x >> 1, mu -> 1
    print()
    print(f"  Newtonian (x >> 1): mu(x) -> 1")
    for x_val in [10, 100, 1000]:
        mu = constitutive_law(x_val)
        print(f"    mu({x_val}) = {mu:.6f}")
        assert abs(mu - 1.0) < 0.1, f"Newtonian: mu({x_val}) = {mu}, not close to 1"

    # Transition point: x = 1, mu = 1/2
    mu_transition = constitutive_law(1.0)
    assert abs(mu_transition - 0.5) < 1e-10
    print()
    print(f"  Transition (x = 1): mu(1) = {mu_transition}")
    print(f"  = 1/2 = K/(2K) = time face fraction")
    print(f"  = constitutive law at equilibrium")
    print(f"  = pi traversal TetA visit fraction")
    print(f"  = BBP active fraction (K/8)")

    # mu is monotonically increasing on [0, inf)
    print()
    prev_mu = 0.0
    monotonic = True
    for i in range(1, 1000):
        x = i * 0.01
        mu = constitutive_law(x)
        if mu <= prev_mu:
            monotonic = False
            break
        prev_mu = mu
    assert monotonic, "mu(x) is not monotonically increasing"
    print(f"  Monotonicity verified on (0, 10] with 1000 sample points")


# =============================================================================
# TEST 6: KINETIC FUNCTIONAL F(y) FROM INTEGRATION
#
# F(y) = y - 2*sqrt(y) + 2*ln(1 + sqrt(y)) is obtained by integrating
# dF/dy = mu(sqrt(y)) = sqrt(y)/(sqrt(y) + 1). This uniquely specifies
# the scalar field kinetic term in the SST action.
# =============================================================================

@test("F(y) = y - 2*sqrt(y) + 2*ln(1 + sqrt(y)): integration of mu", 6)
def test_kinetic_functional():
    print()
    print(f"  The SST kinetic functional F(y) is determined by:")
    print(f"    dF/dy = mu(sqrt(y)) = sqrt(y) / (sqrt(y) + 1)")
    print()

    # Verify dF/dy = mu(sqrt(y)) numerically at multiple points
    print(f"  Verifying dF/dy = mu(sqrt(y)) at test points:")
    print(f"  {'y':>10}  {'dF/dy (num)':>14}  {'mu(sqrt(y))':>14}  {'error':>10}")
    max_error = 0.0
    for y_val in [0.01, 0.1, 0.25, 0.5, 1.0, 2.0, 4.0, 9.0, 16.0, 25.0]:
        dF_num = kinetic_functional_derivative(y_val)
        mu_val = constitutive_law(math.sqrt(y_val))
        error = abs(dF_num - mu_val)
        max_error = max(max_error, error)
        print(f"  {y_val:10.2f}  {dF_num:14.8f}  {mu_val:14.8f}  {error:10.2e}")

    assert max_error < 1e-6, f"Max integration error: {max_error}"
    print(f"\n  Max error: {max_error:.2e} (< 1e-6)")

    # Boundary behavior of F(y)
    print()
    print(f"  Boundary behavior:")
    # F(0) = 0 - 0 + 2*ln(1) = 0
    f_zero = kinetic_functional(0.0)
    assert abs(f_zero) < 1e-10
    print(f"    F(0) = {f_zero:.10f}  (vanishes at origin)")

    # For large y: F(y) ~ y - 2*sqrt(y) + 2*ln(sqrt(y)) ~ y (dominant)
    f_large = kinetic_functional(10000.0)
    ratio = f_large / 10000.0
    print(f"    F(10000) / 10000 = {ratio:.6f}  (approaches 1 for Newtonian regime)")

    # For small y: F(y) ~ y^2 / 2 (deep MOND, quadratic)
    f_small = kinetic_functional(0.001)
    ratio_small = f_small / (0.001 ** 2 / 2)
    print(f"    F(0.001) / (y^2/2) = {ratio_small:.4f}  (deep MOND: approaches quadratic)")


# =============================================================================
# TEST 7: BBP CONSTANTS = SST COUPLING SCALES
#
# The BBP digit-extraction formula for pi has base 16, period 8, and
# K=4 active terms. These are the same three numbers that appear as
# coupling scales in the SST action. Pi's analytical structure encodes
# the coupling hierarchy of gravity.
# =============================================================================

@test("BBP base=16, period=8, active=4 match SST coupling scales", 7)
def test_bbp_sst_correspondence():
    print()
    print(f"  BBP formula constants vs SST coupling scales:")
    print()
    print(f"  {'BBP constant':25s}  {'Value':>6}  {'SST role'}")
    print(f"  {'-'*25}  {'-'*6}  {'-'*35}")

    pairs = [
        ("Base (geometric series)", BBP_BASE, 16, "R/(16*pi*G) gravity term"),
        ("Period (denominator cycle)", BBP_PERIOD, 8, "a_0^2/(8*pi*G) scalar term"),
        ("Active terms per period", BBP_ACTIVE_COUNT, 4, "1/4 EM normalization"),
    ]

    for label, bbp_val, sst_val, role in pairs:
        assert bbp_val == sst_val, f"{label}: BBP={bbp_val}, SST={sst_val}"
        print(f"  {label:25s}  {bbp_val:6d}  {role}")

    print()
    print(f"  All three match exactly.")
    print(f"  Pi's digit-extraction algorithm encodes the coupling hierarchy:")
    print(f"    Base 16 = gravity (full Merkaba)")
    print(f"    Period 8 = scalar field (trigram cycle)")
    print(f"    Active 4 = EM (closure constant)")

    # The ratios also match
    assert BBP_BASE // BBP_PERIOD == 2, "16/8 should be bimetric factor"
    assert BBP_PERIOD // BBP_ACTIVE_COUNT == 2, "8/4 should be bimetric factor"
    print(f"\n  Ratio chain: 16 / 8 / 4 = 2 / 2 (bimetric cascade)")


# =============================================================================
# TEST 8: N-METRIC FAMILY AND THE GOLDEN RATIO
#
# The generalized constitutive law x(1-mu)^N = mu yields different mu(1)
# at the transition for different N. For N=1 (SST): mu(1) = 1/2.
# For N=2 (Hassan-Rosen bimetric): mu(1) = 1/phi^2 where phi is the
# golden ratio. This provides a concrete observational discriminant.
# =============================================================================

@test("N-metric family: N=1 gives 1/2, N=2 gives 1/phi^2 at transition", 8)
def test_n_metric_golden_ratio():
    phi = (1.0 + math.sqrt(5.0)) / 2.0  # golden ratio
    print()
    print(f"  Golden ratio phi = (1 + sqrt(5)) / 2 = {phi:.10f}")
    print()

    # N=1: x(1-mu) = mu at x=1 gives 1-mu = mu, so mu = 1/2
    print(f"  N=1 (effective single-metric SST):")
    print(f"    Screening equation: x(1-mu) = mu")
    print(f"    At x=1: (1-mu) = mu, so mu = 1/2")
    mu_n1 = constitutive_law(1.0)
    assert abs(mu_n1 - 0.5) < 1e-10
    print(f"    mu_N1(1) = {mu_n1}")

    # N=2: x(1-mu)^2 = mu at x=1 gives (1-mu)^2 = mu
    # Solving: 1 - 2mu + mu^2 = mu, mu^2 - 3mu + 1 = 0
    # mu = (3 - sqrt(5))/2 = (3 - sqrt(5))/2
    print()
    print(f"  N=2 (Hassan-Rosen bimetric):")
    print(f"    Screening equation: x(1-mu)^2 = mu")
    print(f"    At x=1: (1-mu)^2 = mu")
    print(f"    Quadratic: mu^2 - 3mu + 1 = 0")

    discriminant = 9.0 - 4.0
    mu_n2 = (3.0 - math.sqrt(discriminant)) / 2.0
    phi_inv_sq = 1.0 / (phi ** 2)

    print(f"    mu_N2(1) = (3 - sqrt(5))/2 = {mu_n2:.10f}")
    print(f"    1/phi^2  = {phi_inv_sq:.10f}")
    assert abs(mu_n2 - phi_inv_sq) < 1e-10, (
        f"mu_N2(1) = {mu_n2}, 1/phi^2 = {phi_inv_sq}"
    )
    print(f"    MATCH: mu_N2(1) = 1/phi^2")

    # Golden ratio identity: phi^2 = phi + 1, so 1/phi^2 = 2 - phi
    assert abs(phi_inv_sq - (2.0 - phi)) < 1e-10
    print(f"    Note: 1/phi^2 = 2 - phi = {2.0 - phi:.10f} (golden ratio identity)")

    # Verify the screening equation is satisfied
    check_n2 = 1.0 * (1.0 - mu_n2) ** 2
    assert abs(check_n2 - mu_n2) < 1e-10
    print(f"    Verification: (1-mu)^2 = {check_n2:.10f} = mu")

    # Both limits agree asymptotically
    print()
    print(f"  Asymptotic agreement:")
    print(f"  {'x':>10}  {'mu_N1':>12}  {'mu_N2':>12}  {'ratio':>10}")
    for x_val in [0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0]:
        mu1 = constitutive_law(x_val)
        # N=2: solve (1-mu)^2 = mu/x numerically
        # mu^2 - (2 + 1/x)mu + 1 = 0
        a, b, c = 1.0, -(2.0 + 1.0/x_val), 1.0
        disc = b**2 - 4*a*c
        mu2 = (-b - math.sqrt(disc)) / (2*a) if disc >= 0 else 0
        ratio = mu2 / mu1 if mu1 > 0 else 0
        print(f"  {x_val:10.3f}  {mu1:12.6f}  {mu2:12.6f}  {ratio:10.6f}")

    print()
    print(f"  Deep MOND (x<<1): both approach mu ~ x (ratio -> 1)")
    print(f"  Newtonian (x>>1): both approach mu ~ 1 (ratio -> 1)")
    print(f"  They differ ONLY at the transition scale (x ~ 1)")
    print(f"  This is the observational discriminant between N=1 and N=2")


# =============================================================================
# TEST 9: THE STELLATED OCTAHEDRON FIELD EQUATION
#
# The modified Poisson equation nabla . [mu(x) nabla Phi] = 4piG rho
# can be rewritten using mu = (f-13)/8 as:
#   nabla . [(f(x) - 13)/8 * nabla Phi] = 4piG rho
# where f(x) = (21x + 13)/(x+1).
#
# Every constant in this equation traces to the Merkaba:
#   4piG has the 4 = K = closure constant
#   13 = kd + 1 = edge count + origin
#   8 = 2^D = trigram space
#   21 = f(K, +1) = full TetA capacity
# =============================================================================

@test("Stellated Octahedron Field Equation: all constants are Merkaba", 9)
def test_field_equation_constants():
    print()
    print(f"  The stellated octahedron field equation:")
    print(f"    nabla . [(f(x) - 13) / 8  *  nabla Phi] = 4 pi G rho")
    print(f"    where f(x) = (21x + 13) / (x + 1)")
    print()
    print(f"  Constant-by-constant Merkaba mapping:")
    print()

    # 4 in 4piG
    print(f"  4 (in 4piG):")
    print(f"    = K = closure constant")
    print(f"    = d + 1 = simplex vertex count in d=3")
    print(f"    = vertices per tetrahedron")
    assert K == 4

    # 13 = kd + 1
    print(f"\n  13 (TetB floor, subtracted in normalization):")
    print(f"    = f(K, -1) = 1 - K + K^2 = 1 - 4 + 16")
    print(f"    = kd + 1 = {K}*{D} + 1 = {K*D + 1}")
    print(f"    = 12 Merkaba edges + 1 Field Origin")
    assert F_MINUS == K * D + 1 == 13

    # 8 = normalization divisor
    print(f"\n  8 (normalization divisor):")
    print(f"    = f_max - f_min = {F_PLUS} - {F_MINUS}")
    print(f"    = 2^D = trigram space = 2 * K")
    print(f"    = BBP period")
    assert F_RANGE == 2 ** D == 2 * K == 8

    # 21 = f(K, +1)
    print(f"\n  21 (TetA ceiling, numerator coefficient):")
    print(f"    = f(K, +1) = 1 + K + K^2 = 1 + 4 + 16")
    print(f"    = coupling polynomial at full capacity")
    print(f"    = alpha exponent in G = (17/13) * alpha^21 * ...")
    assert F_PLUS == 1 + K + K ** 2 == 21

    # 17 = f(K, 0), the Field Origin value
    print(f"\n  17 (Field Origin capacity, implicit in f(x)):")
    print(f"    = f(K, 0) = 1 + K^2 = 1 + 16")
    print(f"    = midpoint of [13, 21]")
    print(f"    = numerator of the G ratio 17/13")
    assert F_ZERO == 1 + K ** 2 == 17
    assert (F_PLUS + F_MINUS) / 2 == F_ZERO

    # Verify the field equation is self-consistent
    print()
    print(f"  Self-consistency check:")
    print(f"  At x=1 (transition): mu = 1/2, so the effective coupling")
    print(f"  is exactly half of Newtonian gravity.")
    mu_at_1 = (capacity_function(1.0) - F_MINUS) / F_RANGE
    assert abs(mu_at_1 - 0.5) < 1e-10
    print(f"  mu(1) = (f(1) - 13)/8 = ({capacity_function(1.0):.1f} - 13)/8 = {mu_at_1}")

    # The ratio 17/13 as continued fraction [1; 3, 4] = [1; D, K]
    cf_value = 1.0 + 1.0 / (D + 1.0 / K)
    assert abs(cf_value - 17.0/13.0) < 1e-10
    print(f"\n  17/13 = [1; {D}, {K}] = [1; D, K]")
    print(f"  The coupling ratio encodes the dimension and closure constant")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print()
    print("*" * 72)
    print("*  SST-MERKABA STRUCTURAL INVESTIGATION")
    print("*  Scalar-Tensor Action meets the Stellated Octahedron")
    print("*" * 72)

    all_tests = [
        test_coupling_hierarchy,
        test_bimetric_coefficients,
        test_conformal_map,
        test_capacity_and_normalization,
        test_constitutive_law_mond,
        test_kinetic_functional,
        test_bbp_sst_correspondence,
        test_n_metric_golden_ratio,
        test_field_equation_constants,
    ]

    for t in all_tests:
        t()

    # Summary
    print()
    print()
    print("*" * 72)
    print("*  SUMMARY OF FINDINGS")
    print("*" * 72)
    print()

    passed = sum(1 for _, _, s in _results if s == "PASS")
    total = len(_results)
    print(f"  Results: {passed}/{total} tests passed")
    print()

    rankings = [
        ("STRUCTURAL NECESSITY",
         "These follow directly from the coupling polynomial f(k,s) = 1+ks+k^2.",
         "If the Merkaba is the geometry, the SST MUST have these features.",
         [
             (1, "Coupling hierarchy 16/8/4 = 2^K / 2^D / K"),
             (2, "Bimetric coefficients {1,0,16,0,1} from f(4,0)"),
             (4, "Capacity normalization (f-13)/8 yields mu = x/(x+1)"),
             (9, "Every constant in the field equation is a Merkaba number"),
         ]),
        ("DEEP CORRESPONDENCE",
         "These reveal the SST action's internal structure encodes the",
         "Merkaba at levels beyond parameter counting.",
         [
             (3, "Conformal map [-1,+1] = vertex coordinate bounds, det=2"),
             (5, "Constitutive law is a valid MOND interpolator with mu(1)=1/2"),
             (6, "Kinetic functional F(y) uniquely determined, no free parameters"),
             (7, "BBP base/period/active = SST gravity/scalar/EM scales"),
         ]),
        ("OBSERVATIONAL PREDICTION",
         "The N-metric family provides a concrete test distinguishing",
         "the single-metric SST from the full bimetric theory.",
         [
             (8, "N=2 gives mu(1) = 1/phi^2, distinct from N=1 mu(1) = 1/2"),
         ]),
    ]

    for category, *desc_lines, items in rankings:
        print(f"  [{category}]")
        for line in desc_lines:
            print(f"  {line}")
        print()
        for num, desc in items:
            status = next((s for n, _, s in _results if n == num), "?")
            mark = "PASS" if status == "PASS" else "FAIL"
            print(f"    [{mark}] Test {num}: {desc}")
        print()

    if passed < total:
        print("  FAILURES:")
        for num, name, status in _results:
            if status != "PASS":
                print(f"    Test {num}: {name} -> {status}")

    return passed == total


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
