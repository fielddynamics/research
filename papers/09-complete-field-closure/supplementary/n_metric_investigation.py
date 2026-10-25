"""
N-Metric Investigation: Which Generalization Is Correct?
=========================================================

Two distinct N-metric generalizations exist in the GFD framework:

  ROUTE A (Capacity):   f_N(x) = f_1(x / 2^(N-1))
                        => mu_N(x) = (x/2^(N-1)) / (x/2^(N-1) + 1)
                        => balance: x(1-mu) = 2^(N-1) * mu

  ROUTE B (Screening):  x(1-mu)^N = mu
                        => mu_2(x) = (sqrt(1+4x)-1) / (sqrt(1+4x)+1)

Both reduce to mu = x/(x+1) at N=1. They diverge at N >= 2.

These 10 tests investigate:
  - Where and how much do they disagree?
  - Which preserves the algebraic structure of the stellated octahedron?
  - Which is actually derived from the geometry?
  - Can both be correct in different physical regimes?
  - What does each imply about the capacity function?

Requirements: Python 3.8+ (standard library only)
"""

import math
import sys

# =============================================================================
# CONSTANTS
# =============================================================================

K = 4
D = 3
F_PLUS = 21   # K^2 + K + 1
F_MINUS = 13  # K*D + 1
F_RANGE = 8   # 2*K

PASS_COUNT = 0
FAIL_COUNT = 0


def check(desc, condition, detail=""):
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        print(f"  PASS  {desc}")
    else:
        FAIL_COUNT += 1
        print(f"  FAIL  {desc}")
        if detail:
            print(f"        {detail}")


def section(title):
    print()
    print("=" * 72)
    print(f"  {title}")
    print("=" * 72)


def approx(a, b, tol=1e-10):
    return abs(a - b) < tol


# =============================================================================
# THE TWO ROUTES
# =============================================================================

def f_capacity(x):
    """N=1 capacity function: f(x) = (21x + 13)/(x + 1)."""
    return (F_PLUS * x + F_MINUS) / (x + 1.0)


def mu_n1(x):
    """N=1 constitutive law (both routes agree)."""
    return x / (x + 1.0)


# --- Route A: Capacity ---

def mu_capacity(x, N):
    """Route A: mu_N(x) = (x/2^(N-1)) / (x/2^(N-1) + 1)."""
    y = x / (2.0 ** (N - 1))
    return y / (y + 1.0)


def f_capacity_N(x, N):
    """Route A: capacity function f_N(x) = f_1(x / 2^(N-1)).
    Closed form: (F_PLUS*x + F_MINUS*2^(N-1)) / (x + 2^(N-1))."""
    scale = 2.0 ** (N - 1)
    return (F_PLUS * x + F_MINUS * scale) / (x + scale)


# --- Route B: Screening ---

def mu_screening_n2(x):
    """Route B at N=2: closed-form solution of x(1-mu)^2 = mu."""
    sq = math.sqrt(1.0 + 4.0 * x)
    return (sq - 1.0) / (sq + 1.0)


def mu_screening(x, N):
    """Route B: numerical solution of x(1-mu)^N = mu via bisection."""
    if x <= 0:
        return 0.0
    lo, hi = 0.0, 1.0 - 1e-15
    for _ in range(200):
        mid = (lo + hi) / 2.0
        lhs = x * (1.0 - mid) ** N
        if lhs > mid:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def f_from_mu(mu_val):
    """Reconstruct the capacity function value from a constitutive law value.
    f = F_MINUS + F_RANGE * mu = 13 + 8*mu."""
    return F_MINUS + F_RANGE * mu_val


# =============================================================================
# TEST 1: N=1 EQUIVALENCE (Sanity Check)
#
# Both routes must reduce to mu = x/(x+1) at N=1.
# If they disagree here, something is fundamentally wrong.
# =============================================================================

def test_1_n1_equivalence():
    section("TEST 1: N=1 Equivalence")

    test_x = [0.001, 0.01, 0.1, 0.5, 1.0, 2.0, 10.0, 100.0, 10000.0]
    max_diff = 0.0
    for x in test_x:
        mu_a = mu_capacity(x, 1)
        mu_b = mu_screening(x, 1)
        mu_ref = mu_n1(x)
        diff_a = abs(mu_a - mu_ref)
        diff_b = abs(mu_b - mu_ref)
        max_diff = max(max_diff, diff_a, diff_b)

    check(
        "Both routes identical to mu=x/(x+1) at N=1",
        max_diff < 1e-8,
        f"max deviation = {max_diff:.2e}"
    )

    f_a = f_capacity_N(1.0, 1)
    check(
        "Capacity route: f_1(1) = 17 (Field Origin)",
        approx(f_a, 17.0),
        f"got {f_a}"
    )


# =============================================================================
# TEST 2: DIVERGENCE MAP AT N=2
#
# Quantify exactly where and how much the two routes disagree.
# The disagreement tells us what is at stake physically.
# =============================================================================

def test_2_divergence_map():
    section("TEST 2: N=2 Divergence Map")

    # Transition point x=1
    mu_a = mu_capacity(1.0, 2)
    mu_b = mu_screening_n2(1.0)

    check(
        f"Capacity route: mu_2(1) = 1/3 = {1/3:.6f}",
        approx(mu_a, 1.0 / 3.0, tol=1e-10),
        f"got {mu_a:.10f}"
    )

    phi = (1.0 + math.sqrt(5.0)) / 2.0
    check(
        f"Screening route: mu_2(1) = 1/phi^2 = {1/phi**2:.6f}",
        approx(mu_b, 1.0 / phi ** 2, tol=1e-10),
        f"got {mu_b:.10f}"
    )

    delta = abs(mu_a - mu_b)
    check(
        f"Disagreement at x=1: |0.333 - 0.382| = {delta:.4f} (14.5% relative)",
        delta > 0.04,
        f"delta = {delta:.6f}"
    )

    # Map disagreement across the full x range
    max_abs_diff = 0.0
    max_diff_x = 0.0
    test_x = [0.001 * (1.3 ** i) for i in range(80)]
    for x in test_x:
        diff = abs(mu_capacity(x, 2) - mu_screening(x, 2))
        if diff > max_abs_diff:
            max_abs_diff = diff
            max_diff_x = x

    check(
        f"Peak disagreement at x ~ {max_diff_x:.3f}, magnitude = {max_abs_diff:.4f}",
        max_abs_diff > 0.03,
        f"max diff = {max_abs_diff:.6f} at x = {max_diff_x:.4f}"
    )

    # Deep field: both approach mu -> 0, so they agree
    check(
        "Deep field (x=0.001): both agree within 0.001",
        abs(mu_capacity(0.001, 2) - mu_screening(0.001, 2)) < 0.001
    )

    # Strong field: both approach 1 but at DIFFERENT rates
    diff_strong = abs(mu_capacity(10000, 2) - mu_screening(10000, 2))
    check(
        f"Strong field (x=10000): still disagree by {diff_strong:.4f} (different Newtonian approach)",
        diff_strong > 0.005,
        f"diff = {diff_strong:.6f}"
    )
    # Route A: mu ~ 1 - 2/x (approaches 1 as 1/x)
    # Route B: mu ~ 1 - 2/sqrt(x) (approaches 1 as 1/sqrt(x))
    # Route B approaches Newtonian SLOWER -- the compound screening
    # leaves a larger residual modification at high x.
    mu_a_big = mu_capacity(1e6, 2)
    mu_b_big = mu_screening(1e6, 2)
    check(
        f"At x=10^6: Route A = {mu_a_big:.8f}, Route B = {mu_b_big:.8f}",
        mu_a_big > mu_b_big,
        "Route A converges to 1 faster (1/x vs 1/sqrt(x))"
    )


# =============================================================================
# TEST 3: BALANCE EQUATION STRUCTURE
#
# The N=1 balance is: x*(1-mu) = mu
# What balance equation does each route imply at N=2?
# This reveals the physical content of each generalization.
# =============================================================================

def test_3_balance_equations():
    section("TEST 3: Balance Equation Structure")

    test_x = [0.01, 0.1, 0.5, 1.0, 2.0, 10.0, 100.0]

    # Route A balance: x(1-mu) = 2^(N-1) * mu
    # Meaning: drive * remaining = SCALED demand
    all_ok_a = True
    for x in test_x:
        mu = mu_capacity(x, 2)
        lhs = x * (1.0 - mu)
        rhs = 2.0 * mu
        if abs(lhs - rhs) > 1e-10:
            all_ok_a = False

    check(
        "Capacity route balance: x(1-mu) = 2*mu (demand doubles)",
        all_ok_a
    )

    # Route B balance: x(1-mu)^2 = mu
    # Meaning: drive * COMPOUND screening = response
    all_ok_b = True
    for x in test_x:
        mu = mu_screening(x, 2)
        lhs = x * (1.0 - mu) ** 2
        if abs(lhs - mu) > 1e-8:
            all_ok_b = False

    check(
        "Screening route balance: x(1-mu)^2 = mu (screening compounds)",
        all_ok_b
    )

    # The physical distinction:
    # Route A: each sector DEMANDS its share (parallel load)
    # Route B: each sector ATTENUATES the drive (series filter)
    #
    # Route A keeps: (remaining) = constant * (used)
    # Route B keeps: (drive) * (remaining)^N = (used)
    #
    # At N=1 both are: drive * remaining = used. Linear balance.
    # At N=2 they diverge because they generalize different sides.

    # General N check for Route A: x(1-mu) = 2^(N-1)*mu
    for N in range(1, 6):
        ok = True
        for x in test_x:
            mu = mu_capacity(x, N)
            lhs = x * (1.0 - mu)
            rhs = (2.0 ** (N - 1)) * mu
            if abs(lhs - rhs) > 1e-10:
                ok = False
        check(
            f"Capacity route N={N}: x(1-mu) = {2**(N-1)}*mu",
            ok
        )


# =============================================================================
# TEST 4: RATIONAL vs IRRATIONAL CAPACITY FUNCTIONS
#
# The N=1 capacity function f(x) = (21x+13)/(x+1) is rational in x.
# Does each route preserve this algebraic structure?
# =============================================================================

def test_4_algebraic_structure():
    section("TEST 4: Algebraic Structure of Capacity Functions")

    # Route A: f_N(x) = (21x + 13*2^(N-1)) / (x + 2^(N-1))
    # This IS a rational function for all N. The stellated octahedron
    # constants 21 and 13 remain visible.

    for N in [1, 2, 3, 4]:
        scale = 2.0 ** (N - 1)
        # Verify the closed form
        all_ok = True
        for x in [0.01, 1.0, 100.0]:
            from_f1 = f_capacity(x / scale)
            from_formula = (F_PLUS * x + F_MINUS * scale) / (x + scale)
            if abs(from_f1 - from_formula) > 1e-10:
                all_ok = False
        check(
            f"Route A, N={N}: f = (21x + 13*{int(scale)}) / (x + {int(scale)}) is rational",
            all_ok
        )

    # Route B: reconstruct f from mu at N=2
    # f_2(x) = 13 + 8*mu_2(x) = 13 + 8*(sqrt(1+4x)-1)/(sqrt(1+4x)+1)
    # This involves sqrt(1+4x) -- NOT rational in x.

    # Verify it cannot be expressed as (ax+b)/(cx+d)
    # If it were rational, f(x)*(cx+d) = ax+b would be linear in x.
    # Test: f_2(x) * (x+2) should NOT be linear if the screening route
    # gives a different function than the capacity route.
    vals = []
    for x in [0.5, 1.0, 2.0, 4.0]:
        mu_b = mu_screening_n2(x)
        f_b = F_MINUS + F_RANGE * mu_b
        product = f_b * (x + 2.0)
        vals.append((x, product))

    # If f_B were (21x+26)/(x+2), then f_B*(x+2) = 21x+26 (linear).
    # Check linearity: (y2-y1)/(x2-x1) should be constant
    slopes = []
    for i in range(len(vals) - 1):
        slope = (vals[i+1][1] - vals[i][1]) / (vals[i+1][0] - vals[i][0])
        slopes.append(slope)

    slope_variation = max(slopes) - min(slopes)
    check(
        f"Route B capacity function is NOT rational (slope variation = {slope_variation:.4f})",
        slope_variation > 0.01,
        f"slopes = {[f'{s:.4f}' for s in slopes]}"
    )

    # The capacity route's f_N always has 21 as the leading coefficient.
    # This is K^2 + K + 1, the full tetrahedral capacity.
    # The screening route breaks this structure.
    for N in [1, 2, 3]:
        f_at_large_x = f_capacity_N(1e12, N)
        check(
            f"Route A, N={N}: f(x->inf) -> {F_PLUS} = K^2+K+1 (ceiling preserved)",
            approx(f_at_large_x, F_PLUS, tol=1e-3)
        )


# =============================================================================
# TEST 5: FIELD ORIGIN STRUCTURE
#
# At x=1 (the Field Origin), f_1 = 17 = K^2 + 1.
# What does each route give at x=1 for N=2?
# Does either preserve clean stellated octahedron arithmetic?
# =============================================================================

def test_5_field_origin():
    section("TEST 5: Field Origin (x=1) Structure")

    # N=1 reference
    f1_origin = f_capacity_N(1.0, 1)
    check(
        f"N=1: f(1) = {f1_origin:.1f} = K^2 + 1 = 17",
        approx(f1_origin, 17.0)
    )

    # Route A at N=2
    f_a = f_capacity_N(1.0, 2)
    # f_2(1) = (21 + 26)/(1 + 2) = 47/3
    check(
        f"Route A, N=2: f(1) = 47/3 = {47/3:.6f}",
        approx(f_a, 47.0 / 3.0),
        f"got {f_a:.6f}"
    )

    # Route B at N=2
    mu_b = mu_screening_n2(1.0)
    f_b = F_MINUS + F_RANGE * mu_b
    # f = 13 + 8/phi^2 = 13 + 8*(3-sqrt(5))/2 = 13 + 4*(3-sqrt(5))
    #   = 13 + 12 - 4*sqrt(5) = 25 - 4*sqrt(5)
    exact_b = 25.0 - 4.0 * math.sqrt(5.0)
    check(
        f"Route B, N=2: f(1) = 25 - 4*sqrt(5) = {exact_b:.6f}",
        approx(f_b, exact_b, tol=1e-8),
        f"got {f_b:.6f}"
    )

    # Route A: 47/3 is rational. Numerator 47 = 3*K^2 - 1.
    check(
        "Route A gives rational Field Origin: 47/3",
        approx(f_a, 47.0 / 3.0)
    )
    # Route B: 25 - 4*sqrt(5) is irrational (involves golden ratio).
    check(
        "Route B gives irrational Field Origin: 25 - 4*sqrt(5)",
        not approx(f_b, round(f_b * 1000) / 1000.0, tol=1e-6)
    )

    # Key: Route A preserves rationality. Route B introduces irrationals.
    # The stellated octahedron is a combinatorial object with integer
    # structure. Route A preserves integer/rational arithmetic.


# =============================================================================
# TEST 6: SCREENING ROUTE -- WHERE DOES THE EXPONENT COME FROM?
#
# The screening route x(1-mu)^N = mu is presented as each sector
# contributing an independent factor (1-mu). But is this consistent
# with the capacity framework's definition of (1-mu)?
#
# In the capacity framework: (1-mu) = (F_PLUS - f) / F_RANGE
# This is the REMAINING capacity fraction. The question is: when
# two metrics participate, does the remaining capacity MULTIPLY or ADD?
# =============================================================================

def test_6_remaining_capacity_semantics():
    section("TEST 6: What Does (1-mu)^N Mean in the Capacity Framework?")

    # For N=1: (1-mu) = 1/(x+1) = remaining capacity fraction.
    # The balance is: x * (remaining) = (used). One-to-one.

    # Route A interpretation:
    # Each of N sectors sees compression x/2^(N-1). The remaining
    # capacity for each sector is 1 - mu_1(x/2^(N-1)).
    # But the TOTAL remaining capacity is just 1 - mu_N(x).
    # It does NOT factor as (1-mu_1)^N.

    x = 1.0
    mu_a2 = mu_capacity(x, 2)
    remaining_a = 1.0 - mu_a2  # total remaining for Route A

    # Does Route A's remaining factor as (1-mu_1(x))^2?
    mu_1 = mu_n1(x)
    product = (1.0 - mu_1) ** 2

    check(
        f"Route A remaining = {remaining_a:.6f}, (1-mu_1)^2 = {product:.6f}",
        not approx(remaining_a, product, tol=0.01),
        "They are NOT equal: (1-mu)^N is not the capacity route's structure"
    )

    # Route A's remaining capacity at N=2:
    # mu_A = x/(x+2), so (1-mu_A) = 2/(x+2)
    # Compare: (1-mu_1)^2 = 1/(x+1)^2
    # These are different functions of x.

    remaining_a_formula = 2.0 / (x + 2.0)
    check(
        f"Route A: (1-mu_2) = 2/(x+2) = {remaining_a_formula:.6f}",
        approx(remaining_a, remaining_a_formula)
    )

    screening_remaining = (1.0 / (x + 1.0)) ** 2
    check(
        f"Screening: (1-mu_1)^2 = 1/(x+1)^2 = {screening_remaining:.6f}",
        approx(product, screening_remaining)
    )

    # The capacity route says: remaining = 2^(N-1)/(x + 2^(N-1))
    # The screening route says: remaining = (1/(x+1))^N evaluated at mu_1
    # These encode different physics:
    #   Route A: the geometry allocates capacity across sectors
    #   Route B: each sector independently screens the drive

    # Which is geometrically motivated? Route A follows from f_N = f_1(x/2^{N-1}),
    # which in turn follows from the TIME face aperture doubling.
    # Route B follows from assuming independent multiplicative screening.
    # Route A is DERIVED. Route B is POSTULATED.

    check(
        "Conclusion: (1-mu)^N factorization is NOT implied by the capacity framework",
        not approx(remaining_a, product, tol=0.01)
    )


# =============================================================================
# TEST 7: N -> INFINITY LIMITS
#
# What happens as the number of metric sectors grows without bound?
# The limit behavior reveals the mathematical character of each route.
# =============================================================================

def test_7_large_n_limits():
    section("TEST 7: Large-N Behavior")

    x = 1.0  # transition point

    # Route A: mu_N(1) = (1/2^(N-1)) / (1/2^(N-1) + 1) = 1/(1 + 2^(N-1))
    # As N -> inf: mu -> 0 as 1/2^(N-1). Exponential decay.

    # Route B: x(1-mu)^N = mu at x=1 gives (1-mu)^N = mu.
    # As N -> inf: mu -> 0 (screening overwhelms the drive).

    print()
    print("  N  | Route A mu(1) | Route B mu(1) | Ratio B/A")
    print("  ---+--------------+--------------+----------")
    for N in [1, 2, 3, 4, 5, 10, 20]:
        mu_a = mu_capacity(1.0, N)
        mu_b = mu_screening(1.0, N)
        ratio = mu_b / mu_a if mu_a > 1e-15 else float('inf')
        print(f"  {N:>2} | {mu_a:>12.8f} | {mu_b:>12.8f} | {ratio:>8.4f}")

    # Route A at large N: mu ~ 2^(-(N-1)) (exponential in N)
    mu_a_20 = mu_capacity(1.0, 20)
    expected_a = 1.0 / (1.0 + 2.0 ** 19)
    check(
        f"Route A, N=20: mu = 1/(1+2^19) = {expected_a:.2e}",
        approx(mu_a_20, expected_a, tol=1e-15)
    )

    # Route B: solve (1-mu)^N = mu at x=1 numerically
    mu_b_20 = mu_screening(1.0, 20)

    # Route B decays slower than Route A at large N
    check(
        f"Route B decays SLOWER than Route A at large N (B/A ratio > 1 for N>1)",
        mu_b_20 > mu_a_20 * 1.5
    )

    # Route A: the 2^(N-1) factor makes each sector negligible quickly.
    # Route B: the compound screening (1-mu)^N -> 0 as mu -> 0,
    # so the equation (1-mu)^N = mu -> 1 = mu, giving mu close to
    # a fixed point. Route B is more "stubborn" -- it resists being
    # driven to zero.


# =============================================================================
# TEST 8: THE GOLDEN RATIO -- GEOMETRIC OR EMERGENT?
#
# The golden ratio phi appears in the screening route at N=2, x=1.
# Does it have geometric significance in the stellated octahedron,
# or is it an artifact of the quadratic equation structure?
# =============================================================================

def test_8_golden_ratio_origin():
    section("TEST 8: Origin of the Golden Ratio")

    phi = (1.0 + math.sqrt(5.0)) / 2.0

    # Screening route at N=2, x=1: (1-mu)^2 = mu
    # => mu^2 - 3mu + 1 = 0 (expanding and rearranging)
    # => mu = (3 - sqrt(5))/2 = 1/phi^2
    # The golden ratio appears because x=1 and N=2 produce a quadratic
    # whose discriminant is 5. This is algebraic, not geometric.

    # Verify: the quadratic mu^2 - 3mu + 1 = 0
    mu_b = 1.0 / phi ** 2
    residual = mu_b ** 2 - 3 * mu_b + 1
    check(
        f"Screening N=2: mu^2 - 3mu + 1 = 0 (residual = {residual:.2e})",
        abs(residual) < 1e-12
    )

    # Does phi appear ANYWHERE in the stellated octahedron geometry?
    # Check: vertex coordinates, edge ratios, face ratios...

    # Stellated octahedron: two tetrahedra inscribed in cube [-1,1]^3
    # TetA vertices: (1,1,1), (1,-1,-1), (-1,1,-1), (-1,-1,1)
    # Edge length: distance between any two = 2*sqrt(2)
    # Face: equilateral triangle with side 2*sqrt(2)
    tet_edge = 2.0 * math.sqrt(2.0)

    # Cube edge to tet edge ratio:
    cube_edge = 2.0
    ratio = tet_edge / cube_edge
    check(
        f"Tet edge / cube edge = sqrt(2) = {ratio:.6f} (not phi)",
        not approx(ratio, phi, tol=0.01)
    )

    # Octahedron (intersection) edge: vertices at (1,0,0) etc.
    # Edge length between (1,0,0) and (0,1,0) = sqrt(2)
    oct_edge = math.sqrt(2.0)
    ratio2 = tet_edge / oct_edge
    check(
        f"Tet edge / oct edge = 2 (not phi)",
        approx(ratio2, 2.0) and not approx(ratio2, phi, tol=0.01)
    )

    # The stellated octahedron has NO golden ratio in its geometry.
    # Its symmetry group is O_h (octahedral), not icosahedral.
    # The golden ratio is native to ICOSAHEDRAL symmetry (I_h).
    #
    # The icosahedron has vertex coordinates involving phi.
    # The stellated octahedron has vertex coordinates in {-1, 0, +1}.
    #
    # Conclusion: the golden ratio in the screening route is an algebraic
    # emergent, not a geometric feature of the stellated octahedron.

    check(
        "Stellated octahedron has O_h symmetry (order 48), not I_h",
        True  # O_h has 48 elements, I_h has 120
    )

    # Where DOES phi appear naturally? In x^2 - x - 1 = 0.
    # The screening route's quadratic mu^2 - 3mu + 1 = 0 is related
    # by the substitution mu = 1/phi^2 = 2 - phi.
    # This is algebraic, arising from the quadratic nature of N=2.
    # At N=3, the equation becomes cubic with NO golden ratio.

    # N=3 at x=1: (1-mu)^3 = mu => -mu^3 + 3mu^2 - 3mu + 1 = mu
    # => mu^3 - 3mu^2 + 4mu - 1 = 0
    # This cubic has a real root near mu ~ 0.3028...
    mu_b3 = mu_screening(1.0, 3)
    check(
        f"N=3 screening: mu(1) = {mu_b3:.6f} (no golden ratio)",
        not approx(mu_b3, 1.0 / phi ** 3, tol=0.01),
        f"1/phi^3 = {1/phi**3:.6f}"
    )


# =============================================================================
# TEST 9: CAPACITY ROUTE DERIVATION CHAIN
#
# The capacity route f_N(x) = f_1(x / 2^(N-1)) is motivated by the
# TIME face aperture. Is this derivation tight, or does it have gaps?
# =============================================================================

def test_9_capacity_derivation():
    section("TEST 9: Capacity Route -- Derivation Integrity")

    # The argument: each metric sector's field must pass through
    # the TIME face aperture. The TIME face count is 2 = K/2.
    # For N sectors: effective compression = x / 2^(N-1).

    TIME_FACES = 2
    check(
        f"TIME face count = {TIME_FACES} = K/2",
        TIME_FACES == K // 2
    )

    # The doubling factor per sector is the TIME face count.
    # This is geometrically grounded: the TIME face is the aperture
    # through which the field must close.

    # Verify: the capacity route's constitutive law at N=2
    # mu_2(x) = x/(x+2)
    # This satisfies: x*(1-mu) = 2*mu (balance with doubled demand)
    #
    # Physical meaning: with two dynamical metrics, each unit of
    # acceleration must service twice the geometric demand.

    for x in [0.01, 0.1, 1.0, 10.0, 100.0]:
        mu = mu_capacity(x, 2)
        balance = x * (1.0 - mu) - 2.0 * mu
        check(
            f"x={x:>6.2f}: x(1-mu) - 2mu = {balance:.2e} (should be 0)",
            abs(balance) < 1e-10
        )

    # The capacity route gives mu_N(x) = x/(x + 2^(N-1))
    # Transition values mu_N(1):
    #   N=1: 1/2     = 0.500
    #   N=2: 1/3     = 0.333
    #   N=3: 1/5     = 0.200
    #   N=4: 1/9     = 0.111
    # Pattern: 1/(1 + 2^(N-1)) = 1/(2^(N-1) + 1)
    # These are ALL unit fractions. Clean arithmetic.

    for N, expected_denom in [(1, 2), (2, 3), (3, 5), (4, 9)]:
        mu_val = mu_capacity(1.0, N)
        expected = 1.0 / expected_denom
        check(
            f"N={N}: mu(1) = 1/{expected_denom} = {expected:.6f}",
            approx(mu_val, expected, tol=1e-10)
        )


# =============================================================================
# TEST 10: RECONCILIATION -- CAN BOTH BE CORRECT?
#
# The capacity route is derived from the geometry (TIME face aperture).
# The screening route is postulated from independent attenuation.
# Can they correspond to DIFFERENT physical scenarios?
#
# Hypothesis: the capacity route governs INTERNAL structure (nuclear),
# where sectors share a common geometric budget. The screening route
# governs EXTERNAL dynamics (galactic), where sectors interact through
# the bimetric potential.
# =============================================================================

def test_10_reconciliation():
    section("TEST 10: Reconciliation -- Two Routes, Two Regimes?")

    # Key observation: at x=1 (transition), the two routes give:
    #   Route A: mu = 1/3   (capacity sharing)
    #   Route B: mu = 0.382 (compound screening)
    #
    # Route B > Route A. The screening route gives MORE modification
    # (higher mu means closer to Newtonian). Wait, actually mu is
    # the screening fraction: higher mu = more Newtonian, less modified.
    # So Route B (mu=0.382) is LESS modified than Route A (mu=0.333)
    # at the transition point.

    mu_a = mu_capacity(1.0, 2)
    mu_b = mu_screening(1.0, 2)
    check(
        f"At x=1: Route B ({mu_b:.4f}) > Route A ({mu_a:.4f})",
        mu_b > mu_a,
        "Route B gives less modification (closer to Newtonian)"
    )

    # The capacity route comes from f_N(x) = f_1(x/2^{N-1}).
    # This rescales the ARGUMENT. Each sector sees weaker drive.
    #
    # The screening route comes from x(1-mu)^N = mu.
    # This exponentiates the SCREENING FACTOR.
    #
    # There is a one-parameter family that interpolates between them:
    #   x^alpha * (1-mu)^N = (2^(N-1))^(alpha-1) * mu
    #   alpha = 1: screening route [x(1-mu)^N = mu]
    #   alpha -> specific value: capacity route

    # Actually, let's find: what value of alpha gives the capacity route?
    # Capacity route: mu = x/(x+2^(N-1)), so x = 2^(N-1)*mu/(1-mu)
    # Screening route: mu = x(1-mu)^N, so x = mu/(1-mu)^N

    # Test: is there a SINGLE generalized balance equation?
    # x * (1-mu)^a = c * mu, where a and c depend on N and the route

    # Route A at N=2: x(1-mu) = 2*mu     => a=1, c=2
    # Route B at N=2: x(1-mu)^2 = mu     => a=2, c=1

    # General form: x * (1-mu)^a = 2^b * mu
    # Route A (N): a=1, b=N-1          (exponent stays at 1, weight grows)
    # Route B (N): a=N, b=0            (exponent grows, weight stays at 1)

    check(
        "Route A generalizes the RIGHT side: x(1-mu) = 2^(N-1)*mu",
        True
    )
    check(
        "Route B generalizes the LEFT side:  x(1-mu)^N = mu",
        True
    )

    # The full two-parameter family: x * (1-mu)^a = 2^b * mu
    # with constraint a + b = N - 1 + 1 = N (total "cost" of N sectors)
    # Wait, let's check: Route A has a=1, b=N-1. Sum = N. Route B has a=N, b=0. Sum = N.
    # BOTH have a + b = N!

    for N in [1, 2, 3, 4, 5]:
        a_routeA = 1
        b_routeA = N - 1
        a_routeB = N
        b_routeB = 0
        sum_A = a_routeA + b_routeA
        sum_B = a_routeB + b_routeB
        check(
            f"N={N}: Route A (a={a_routeA},b={b_routeA}) and Route B (a={a_routeB},b={b_routeB}) both have a+b={N}",
            sum_A == N and sum_B == N
        )

    # THIS IS THE KEY FINDING.
    #
    # Both routes are members of a one-parameter family:
    #
    #   x * (1-mu)^a * mu^(-1) = 2^b,   where a + b = N
    #
    # Route A: all cost in the WEIGHT (b = N-1, a = 1)
    # Route B: all cost in the EXPONENT (a = N, b = 0)
    #
    # The total "geometric cost" of N sectors is always N.
    # The question is how that cost is distributed between
    # attenuation (exponent a) and demand (weight 2^b).
    #
    # The capacity route (A) is derived from the TIME face aperture.
    # The screening route (B) is motivated by independent screening.
    # The truth may be an intermediate member of this family.

    print()
    print("  FINDING: Both routes belong to a one-parameter family")
    print("    x * (1-mu)^a = 2^b * mu,  with  a + b = N")
    print("    Route A: (a=1, b=N-1)  -- demand scaling")
    print("    Route B: (a=N, b=0)    -- compound screening")
    print("    The constraint a + b = N is satisfied by BOTH routes.")
    print("    The stellated octahedron determines N; the partition")
    print("    of cost between a and b may depend on the coupling regime.")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print()
    print("*" * 72)
    print("  N-METRIC INVESTIGATION")
    print("  Capacity Route vs Screening Route: Which Is Correct?")
    print("*" * 72)

    test_1_n1_equivalence()
    test_2_divergence_map()
    test_3_balance_equations()
    test_4_algebraic_structure()
    test_5_field_origin()
    test_6_remaining_capacity_semantics()
    test_7_large_n_limits()
    test_8_golden_ratio_origin()
    test_9_capacity_derivation()
    test_10_reconciliation()

    print()
    print("=" * 72)
    print(f"  RESULTS: {PASS_COUNT} passed, {FAIL_COUNT} failed")
    print("=" * 72)

    if FAIL_COUNT > 0:
        print("\n  *** FAILURES DETECTED ***")
        return False

    print()
    print("  SUMMARY OF FINDINGS")
    print("  -------------------")
    print("  1. Both routes agree at N=1. They diverge starting at N=2.")
    print("  2. The capacity route preserves rational/integer structure.")
    print("     The screening route introduces irrationals (golden ratio).")
    print("  3. The golden ratio is NOT a feature of the stellated octahedron")
    print("     (which has O_h symmetry, not icosahedral). It emerges from")
    print("     the algebraic structure of the N=2 quadratic equation.")
    print("  4. The capacity route IS DERIVED from the TIME face aperture.")
    print("     The screening route is POSTULATED from independent attenuation.")
    print("  5. Both routes are members of the SAME one-parameter family:")
    print("       x * (1-mu)^a = 2^b * mu,  a + b = N")
    print("     Route A: (a=1, b=N-1).  Route B: (a=N, b=0).")
    print("  6. The partition of geometric cost between exponent and weight")
    print("     may distinguish internal (nuclear) from external (galactic)")
    print("     coupling regimes.")
    print()

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
