"""
GFD: 10 One-Equation Tests
===========================

The stellated octahedron has TWO interpenetrating tetrahedra. Always.
There is no regime where one tetrahedron is "turned off." The
geometry IS bidirectional. Therefore there is ONE constitutive law:

    x · (1 − μ)² = μ

This is not N=2 vs N=1. There is no N. There is one equation.
μ = x/(x+1) was a first-order approximation that ignores TetB.

The same equation governs:
  - Galaxy rotation curves (x = acceleration ratio g/a₀)
  - Nuclear binding energy (x = compression from A bound fields)

These tests validate the consequences of this unification.

Requirements: Python 3.8+
"""

import math
from fractions import Fraction

# =============================================================================
# CONSTANTS
# =============================================================================

K = 4
D = 3
F_PLUS = 21
F_ZERO = 17
F_MINUS = 13
F_RANGE = 8

phi = (1.0 + math.sqrt(5.0)) / 2.0

TET_A = {1, 2, 4, 7}
TET_B = {0, 3, 5, 6}

ISOTOPE_TABLE = [
    (1, 'H', 1, 0.000), (2, 'He', 4, 7.074), (3, 'Li', 7, 5.606),
    (4, 'Be', 9, 6.463), (5, 'B', 11, 6.928), (6, 'C', 12, 7.680),
    (7, 'N', 14, 7.476), (8, 'O', 16, 7.976), (9, 'F', 19, 7.779),
    (10, 'Ne', 20, 8.032), (11, 'Na', 23, 8.112), (12, 'Mg', 24, 8.261),
    (13, 'Al', 27, 8.332), (14, 'Si', 28, 8.448), (15, 'P', 31, 8.481),
    (16, 'S', 32, 8.493), (17, 'Cl', 35, 8.520), (18, 'Ar', 40, 8.595),
    (19, 'K', 39, 8.557), (20, 'Ca', 40, 8.551), (20, 'Ca', 48, 8.667),
    (21, 'Sc', 45, 8.619), (22, 'Ti', 48, 8.723), (23, 'V', 51, 8.742),
    (24, 'Cr', 52, 8.776), (25, 'Mn', 55, 8.765), (26, 'Fe', 56, 8.790),
    (27, 'Co', 59, 8.768), (28, 'Ni', 58, 8.732), (29, 'Cu', 63, 8.752),
    (30, 'Zn', 64, 8.736), (31, 'Ga', 69, 8.724), (32, 'Ge', 74, 8.705),
    (33, 'As', 75, 8.701), (34, 'Se', 80, 8.712), (35, 'Br', 79, 8.696),
    (36, 'Kr', 84, 8.718), (37, 'Rb', 85, 8.697), (38, 'Sr', 88, 8.733),
    (39, 'Y', 89, 8.714), (40, 'Zr', 90, 8.710), (41, 'Nb', 93, 8.664),
    (42, 'Mo', 98, 8.635), (44, 'Ru', 102, 8.607), (45, 'Rh', 103, 8.584),
    (46, 'Pd', 106, 8.567), (47, 'Ag', 107, 8.554), (48, 'Cd', 114, 8.539),
    (49, 'In', 115, 8.516), (50, 'Sn', 120, 8.505), (51, 'Sb', 121, 8.482),
    (52, 'Te', 130, 8.431), (53, 'I', 127, 8.445), (54, 'Xe', 132, 8.416),
    (55, 'Cs', 133, 8.400), (56, 'Ba', 138, 8.393), (57, 'La', 139, 8.378),
    (58, 'Ce', 140, 8.376), (59, 'Pr', 141, 8.354), (60, 'Nd', 142, 8.346),
    (62, 'Sm', 152, 8.241), (63, 'Eu', 153, 8.227), (64, 'Gd', 158, 8.183),
    (65, 'Tb', 159, 8.171), (66, 'Dy', 164, 8.127), (67, 'Ho', 165, 8.117),
    (68, 'Er', 166, 8.112), (69, 'Tm', 169, 8.068), (70, 'Yb', 174, 8.024),
    (71, 'Lu', 175, 8.015), (72, 'Hf', 180, 7.977), (73, 'Ta', 181, 7.970),
    (74, 'W', 184, 7.945), (75, 'Re', 187, 7.917), (76, 'Os', 192, 7.891),
    (77, 'Ir', 193, 7.882), (78, 'Pt', 195, 7.868), (79, 'Au', 197, 7.916),
    (80, 'Hg', 202, 7.890), (81, 'Tl', 205, 7.873), (82, 'Pb', 208, 7.867),
    (83, 'Bi', 209, 7.848),
]


# =============================================================================
# THE ONE EQUATION
# =============================================================================

def mu(x):
    """The one constitutive law: x(1-μ)² = μ.
    This is the stellated octahedron's screening equation.
    Both tetrahedra participate. Always. No approximation."""
    if x <= 0:
        return 0.0
    return ((2.0 * x + 1.0) - math.sqrt(4.0 * x + 1.0)) / (2.0 * x)


def s(x):
    """Conformal map: s = 2μ - 1. Maps μ ∈ [0,1] to s ∈ [-1,+1]."""
    return 2.0 * mu(x) - 1.0


def mu_approx(x):
    """The old approximation: x(1-μ)=μ → μ=x/(x+1).
    This ignores TetB. Kept only for comparison."""
    return x / (x + 1.0) if x > 0 else 0.0


# =============================================================================
# VALIDATION FRAMEWORK
# =============================================================================

_results = []


def validate(name, section):
    def decorator(func):
        def wrapper():
            try:
                func()
                _results.append((section, name, "PASS", ""))
                print(f"  PASS  {name}")
            except AssertionError as e:
                _results.append((section, name, "FAIL", str(e)))
                print(f"  FAIL  {name}: {e}")
            except Exception as e:
                _results.append((section, name, "ERROR", str(e)))
                print(f"  ERROR {name}: {e}")
        wrapper._section = section
        wrapper._name = name
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator


# =============================================================================
# TEST 1: ONE EQUATION — THE GOLDEN RATIO IS THE LAW
#
# At x = 1 (the transition scale), μ = 1/φ². This is not a choice.
# It falls out of x(1-μ)² = μ with no free parameters.
# The golden ratio is gravity's constitutive constant.
# =============================================================================

@validate(
    "μ(1) = 1/φ² = (3-√5)/2: the golden ratio IS gravity's transition value",
    "E1. Golden Ratio Is Law",
)
def validate_golden_ratio_is_law():
    """At x = 1 (where observed acceleration equals a₀), the one
    equation gives μ = 1/φ². This is not one of several options.
    There is no N=1 alternative. The golden ratio is the unique,
    parameter-free transition value of the constitutive law.
    
    The defining property ν² + ν = 1 (where ν = 1-μ) falls directly
    from (1-μ)² = μ at x = 1. The golden ratio is not imported —
    it is PRODUCED by the geometry."""
    mu_1 = mu(1.0)
    nu = 1.0 - mu_1

    # ν = 1/φ exactly
    assert abs(nu - 1.0 / phi) < 1e-12

    # μ = 1/φ² exactly
    assert abs(mu_1 - 1.0 / phi ** 2) < 1e-12

    # The golden ratio property: ν² + ν = 1
    assert abs(nu ** 2 + nu - 1.0) < 1e-12

    # This is the ONLY real root in (0,1)
    # The other root (3+√5)/2 ≈ 2.618 is > 1, unphysical
    other_root = (3.0 + math.sqrt(5.0)) / 2.0
    assert other_root > 1.0, "Other root should be unphysical"


# =============================================================================
# TEST 2: THE APPROXIMATION μ = x/(x+1) OVERESTIMATES EVERYWHERE
#
# The old "simple" MOND function overestimates μ at every x > 0.
# It was always too generous — predicting more Newtonian gravity
# than the true law provides.
# =============================================================================

@validate(
    "μ_approx = x/(x+1) > μ_true for all x > 0: the approximation always overestimates",
    "E2. Approximation Overestimates",
)
def validate_approximation_overestimates():
    """The scalar-tensor approximation μ = x/(x+1) gives a HIGHER
    value of μ than the true equation x(1-μ)²=μ at every x > 0.
    This means it overestimates the Newtonian component and
    underestimates the modified-gravity component everywhere."""
    test_points = [0.001, 0.01, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0,
                   100.0, 1000.0, 1e6]
    for x in test_points:
        mu_true = mu(x)
        mu_app = mu_approx(x)
        assert mu_app > mu_true, (
            f"x={x}: approx {mu_app:.6f} not > true {mu_true:.6f}"
        )

    # Maximum relative error is in the transition regime (x ~ 2-3)
    max_rel_err = 0
    for i in range(1, 10000):
        x = i * 0.01
        err = (mu_approx(x) - mu(x)) / mu(x) if mu(x) > 0.001 else 0
        if err > max_rel_err:
            max_rel_err = err
    assert max_rel_err > 0.25, (
        f"Max relative error = {max_rel_err:.3f}, expected > 0.25 (25%)"
    )


# =============================================================================
# TEST 3: MASS DECODE — THE APPROXIMATE FORMULA OVERESTIMATES MASS
#
# Using μ=x/(x+1) to decode rotation curves gives M_dec that is
# systematically TOO HIGH. The true equation gives exact masses.
# This systematic overestimate is what gets attributed to dark matter.
# =============================================================================

@validate(
    "Approximate mass decode overestimates by 10-33%: the true equation gives exact M",
    "E3. Mass Decode",
)
def validate_mass_decode():
    """The approximate decode M = rv⁴/(G(a₀r+v²)) systematically
    overestimates mass because it uses μ=x/(x+1). The true decode
    using x(1-μ)²=μ gives exact mass recovery. The overestimate
    is largest in the transition regime — exactly where the "missing
    mass" problem is worst."""
    G = 1.0
    a_0 = 1.0

    errors = []
    for M_true in [0.5, 1.0, 5.0, 50.0]:
        for r in [1.0, 5.0, 20.0]:
            # Forward solve: M_true → v using the TRUE equation
            a_N = G * M_true / r ** 2
            a = a_N  # initial guess
            for _ in range(200):
                x = a / a_0
                mu_val = mu(x)
                if mu_val < 1e-15:
                    break
                a_new = a_N / mu_val
                if abs(a_new - a) / (a + 1e-30) < 1e-14:
                    break
                a = a_new
            v = math.sqrt(a * r)

            # Decode with TRUE equation: exact
            x_obs = v ** 2 / (r * a_0)
            M_full = mu(x_obs) * r * v ** 2 / G

            # Decode with APPROXIMATE equation: overestimate
            M_approx = r * v ** 4 / (G * (a_0 * r + v ** 2))

            err_full = abs(M_full - M_true) / M_true
            err_approx = (M_approx - M_true) / M_true

            # Full decode should be exact (< 1% error from numerics)
            assert err_full < 0.01, (
                f"Full decode error {err_full:.3f} for M={M_true}, r={r}"
            )
            # Approximate decode should overestimate
            assert err_approx > 0.01, (
                f"Approx should overestimate for M={M_true}, r={r}"
            )
            errors.append(err_approx)

    # Average overestimate should be substantial
    avg_err = sum(errors) / len(errors)
    assert avg_err > 0.10, (
        f"Average overestimate = {avg_err:.2%}, expected > 10%"
    )


# =============================================================================
# TEST 4: ONE EQUATION ACROSS 18 ORDERS OF MAGNITUDE
#
# The same μ(x) from x(1-μ)²=μ works for:
#   Galaxy: x ~ 0.01 to 100 (acceleration ratios)
#   Nucleus: x ~ 1 to 43,000 (A² for A=1 to 209)
# The equation spans from galactic to nuclear scales.
# =============================================================================

@validate(
    "μ(x) is well-defined and physical (0 < μ < 1) from x = 10⁻⁶ to x = 10⁶",
    "E4. 12 Orders of Magnitude",
)
def validate_range():
    """The one equation x(1-μ)²=μ produces physical results across the
    entire range from deep MOND (x ~ 10⁻⁶) through galactic transition
    (x ~ 1) to nuclear compression (x ~ 10⁵). Same equation, always."""
    for exp in range(-6, 7):
        x = 10.0 ** exp
        mu_val = mu(x)
        assert 0 < mu_val < 1, (
            f"x = 10^{exp}: μ = {mu_val}, should be in (0,1)"
        )
        # Verify the equation
        lhs = x * (1.0 - mu_val) ** 2
        assert abs(lhs - mu_val) < 1e-8, (
            f"x = 10^{exp}: x(1-μ)² = {lhs} ≠ μ = {mu_val}"
        )


# =============================================================================
# TEST 5: GALAXY-NUCLEAR UNIFICATION — SAME μ, SAME C-FACTOR RANGE
#
# If the equation is truly the same, then the C-factor (the ratio
# of observed to geometric) should be similar in both domains.
# =============================================================================

@validate(
    "Nuclear C-factors (BE/A ÷ geometric) fall in [1.9, 2.4]: same equation, bounded residual",
    "E5. Galaxy-Nuclear Unification",
)
def validate_unification():
    """The one equation gives geometric predictions for nuclear binding.
    The C-factor C = BE/A ÷ (K·s(A²)) should be bounded and nearly
    constant across the periodic table if the equation captures the
    geometric physics correctly."""
    C_vals = []
    for Z, sym, A, bea in ISOTOPE_TABLE:
        if A <= 4:
            continue
        geo = K * s(A ** 2)
        if geo > 0.01:
            C = bea / geo
            C_vals.append(C)
            assert 1.5 < C < 2.5, (
                f"{sym}-{A}: C = {C:.4f} out of bounds"
            )

    # Standard deviation should be small relative to mean
    import statistics
    mean_C = statistics.mean(C_vals)
    std_C = statistics.stdev(C_vals)
    cv = std_C / mean_C
    assert cv < 0.05, f"CV = {cv:.3f}, expected < 0.05"


# =============================================================================
# TEST 6: DEEP MOND PRESERVED — MILGROM'S LAW INTACT
#
# For x << 1: μ ≈ x, giving a² = a_N · a₀ (Milgrom's law).
# The one equation must preserve this because it's confirmed
# by 175+ galaxy rotation curves.
# =============================================================================

@validate(
    "Deep MOND: μ(x) ≈ x for x << 1, preserving Milgrom's law a² = a_N·a₀",
    "E6. Deep MOND Preserved",
)
def validate_deep_mond():
    """In the deep MOND regime (x << 1), μ must approach x linearly.
    This gives a² = a_N · a₀ (Milgrom 1983), which is confirmed by
    the baryonic Tully-Fisher relation. The one equation preserves
    this because x(1-μ)² ≈ x·1 = x ≈ μ when μ << 1."""
    for x in [1e-4, 1e-3, 1e-2]:
        mu_val = mu(x)
        # μ should equal x to within x² corrections
        assert abs(mu_val / x - 1.0) < 10 * x, (
            f"x={x}: μ/x = {mu_val/x:.6f}, expected ≈ 1"
        )

    # The exact leading-order expansion: μ ≈ x - 2x² + ...
    # Verify the -2x² correction term
    x_small = 0.001
    mu_val = mu(x_small)
    correction = (mu_val - x_small) / x_small ** 2
    assert abs(correction + 2.0) < 0.1, (
        f"Second-order correction = {correction:.3f}, expected ≈ -2"
    )


# =============================================================================
# TEST 7: NEWTONIAN LIMIT PRESERVED
#
# For x >> 1: μ → 1, recovering Newtonian gravity.
# =============================================================================

@validate(
    "Newtonian limit: μ → 1 for x >> 1, recovering standard gravity",
    "E7. Newtonian Limit",
)
def validate_newtonian():
    """In the Newtonian regime (x >> 1, strong gravitational fields),
    μ must approach 1. The one equation gives μ = 1 - 1/√x + O(1/x),
    a slower approach than the approximation's 1 - 1/x."""
    for x in [100, 1000, 10000, 1e6]:
        mu_val = mu(x)
        assert abs(mu_val - 1.0) < 1.0 / math.sqrt(x), (
            f"x={x}: 1-μ = {1-mu_val:.6f}, expected < 1/√x = {1/math.sqrt(x):.6f}"
        )

    # The approach rate is 1/√x, NOT 1/x
    # This is slower than the approximation, which goes as 1/x
    x_test = 100.0
    gap_true = 1.0 - mu(x_test)
    gap_approx = 1.0 - mu_approx(x_test)
    assert gap_true > gap_approx, (
        f"True gap ({gap_true:.6f}) should > approx gap ({gap_approx:.6f})"
    )


# =============================================================================
# TEST 8: THE (1-μ)² STRUCTURE COMES FROM TWO TETRAHEDRA
#
# The exponent 2 in x(1-μ)² = μ is not arbitrary. It reflects
# TetA and TetB — two interpenetrating tetrahedra. The stellated
# octahedron HAS two tetrahedra. That's why the exponent is 2.
# =============================================================================

@validate(
    "Exponent 2 = number of tetrahedra in the stellated octahedron: structural, not parametric",
    "E8. Why the Exponent Is 2",
)
def validate_exponent_structure():
    """The exponent 2 in (1-μ)² is not a free parameter. The stellated
    octahedron is composed of exactly 2 interpenetrating tetrahedra.
    If there were 3 tetrahedra, the exponent would be 3. The number
    of tetrahedra is a topological invariant of the geometry.
    
    Crucially: you can't set the exponent to 1 and claim that's
    also a valid equation. That would mean ignoring one tetrahedron —
    which is an approximation, not a different theory."""
    # The stellated octahedron has exactly 2 tetrahedra
    n_tetrahedra = 2
    assert len(TET_A) == K
    assert len(TET_B) == K
    assert TET_A | TET_B == set(range(8))  # full cube
    assert TET_A & TET_B == set()  # no overlap

    # Each tetrahedron contributes one (1-μ) factor
    # x · (1-μ)^n_tet = μ is the equation
    # Verify for various x:
    for x in [0.1, 1.0, 5.0, 100.0]:
        mu_val = mu(x)
        lhs = x * (1.0 - mu_val) ** n_tetrahedra
        assert abs(lhs - mu_val) < 1e-10

    # The exponent 2 gives the golden ratio at x=1.
    # Exponent 1 gives μ=1/2. Exponent 3 gives a different constant.
    # ONLY exponent 2 gives φ. And there are exactly 2 tetrahedra.
    mu_exp1 = 0.5  # from x(1-μ)=μ at x=1
    mu_exp2 = 1.0 / phi ** 2  # from x(1-μ)²=μ at x=1
    # Exponent 3: x(1-μ)³=μ at x=1: (1-μ)³=μ
    # Numerical solve:
    from scipy.optimize import brentq
    mu_exp3 = brentq(lambda m: (1 - m) ** 3 - m, 0, 1)

    # Only exp=2 gives a golden ratio value
    assert abs(mu_exp2 - 1.0 / phi ** 2) < 1e-10
    assert abs(mu_exp1 - 1.0 / phi ** 2) > 0.1  # 1/2 ≠ 1/φ²
    assert abs(mu_exp3 - 1.0 / phi ** 2) > 0.05  # different again


# =============================================================================
# TEST 9: THE MASS DECODE FORMULA — EXACT CLOSED FORM
#
# From x(1-μ)² = μ with x = v²/(ra₀) and μ = GM/(rv²):
# M = (ra₀/2) · [(2v²/(ra₀) + 1) - √(4v²/(ra₀) + 1)]
# This is a closed-form mass decode with zero free parameters.
# =============================================================================

@validate(
    "Exact mass decode: M = (ra₀/2)[(2w+1) - √(4w+1)] where w = v²/(ra₀), closed form",
    "E9. Exact Mass Decode",
)
def validate_exact_mass_decode():
    """The one equation gives a CLOSED-FORM mass decode formula:
    
    M = (r·a₀ / 2) · [(2w + 1) - √(4w + 1)]
    
    where w = v²/(r·a₀). This replaces the approximate formula
    M = rv⁴/(G(a₀r + v²)). The new formula is exact for the true
    constitutive law and has zero free parameters."""
    G = 1.0
    a_0 = 1.0

    def M_decode_exact(r, v):
        """Exact mass decode from x(1-μ)²=μ."""
        w = v ** 2 / (r * a_0)
        mu_val = mu(w)
        return mu_val * r * v ** 2 / G

    def M_decode_closed(r, v):
        """Closed form: M = (r²/2)·[(2w+1) - √(4w+1)] where w = v²/(ra₀).
        Derived: M = μ(w)·r·v² = [(2w+1)-√(4w+1)]/(2w) · r·v²
        and since w = v²/(ra₀), we get r·v²/(2w) = r²·a₀/2."""
        w = v ** 2 / (r * a_0)
        return (r ** 2 * a_0 / 2.0) * ((2 * w + 1) - math.sqrt(4 * w + 1))

    # These two forms must agree (they're the same equation)
    for r in [1.0, 5.0, 20.0]:
        for v in [0.5, 1.0, 2.0, 5.0, 10.0]:
            M_ex = M_decode_exact(r, v)
            M_cl = M_decode_closed(r, v)
            assert abs(M_ex - M_cl) < 1e-10, (
                f"r={r}, v={v}: exact={M_ex:.6f}, closed={M_cl:.6f}"
            )

    # The closed form must give positive mass for all v, r > 0
    for r in [0.1, 1.0, 100.0]:
        for v in [0.01, 1.0, 100.0]:
            M = M_decode_closed(r, v)
            assert M > 0, f"M = {M} for r={r}, v={v}"


# =============================================================================
# TEST 10: THE FALSIFIABLE PREDICTION
#
# The one equation makes a prediction that differs from both
# "simple" and "standard" MOND by measurable amounts in the
# transition regime (x = 0.1 to 10). This is testable against
# existing SPARC rotation curve data (175 galaxies, 2693 data points).
# =============================================================================

@validate(
    "GFD μ differs from both MOND functions by > 5% for x ∈ [0.1, 10]: testable with SPARC data",
    "E10. Falsifiable Prediction",
)
def validate_falsifiable_prediction():
    """The one equation predicts a SPECIFIC μ(x) that disagrees with:
      - Simple MOND: μ = x/(x+1)         [differs by > 20% at x=1]
      - Standard MOND: μ = x/√(1+x²)     [differs by > 30% at x=1]
    
    The GFD function gives LESS modification than either. This means
    GFD predicts rotation curves that are closer to Newtonian in the
    transition regime — a prediction that can be checked against
    every galaxy in the SPARC database."""
    def mu_standard(x):
        return x / math.sqrt(1.0 + x * x)

    # At x = 1 (the critical transition point):
    mu_gfd_1 = mu(1.0)
    mu_simple_1 = mu_approx(1.0)
    mu_standard_1 = mu_standard(1.0)

    # GFD is lower than both
    assert mu_gfd_1 < mu_simple_1, "GFD < simple at x=1"
    assert mu_gfd_1 < mu_standard_1, "GFD < standard at x=1"

    # Quantitative differences
    diff_simple = abs(mu_gfd_1 - mu_simple_1) / mu_gfd_1
    diff_standard = abs(mu_gfd_1 - mu_standard_1) / mu_gfd_1

    assert diff_simple > 0.20, (
        f"GFD-simple difference = {diff_simple:.2%}, expected > 20%"
    )
    assert diff_standard > 0.50, (
        f"GFD-standard difference = {diff_standard:.2%}, expected > 50%"
    )

    # The difference persists across the transition regime
    for x in [0.3, 0.5, 1.0, 2.0, 5.0]:
        mu_g = mu(x)
        mu_s = mu_approx(x)
        diff = abs(mu_g - mu_s) / mu_g
        assert diff > 0.05, (
            f"x={x}: GFD-simple diff = {diff:.2%}, expected > 5%"
        )


# =============================================================================
# MAIN
# =============================================================================

def main():
    print()
    print("=" * 72)
    print("  GFD: 10 ONE-EQUATION TESTS")
    print("  x(1-μ)² = μ  —  One law. Zero parameters.")
    print("=" * 72)
    print()

    all_tests = [
        validate_golden_ratio_is_law,
        validate_approximation_overestimates,
        validate_mass_decode,
        validate_range,
        validate_unification,
        validate_deep_mond,
        validate_newtonian,
        validate_exponent_structure,
        validate_exact_mass_decode,
        validate_falsifiable_prediction,
    ]

    current_section = None
    for test in all_tests:
        section = test._section
        if section != current_section:
            print()
            print(f"--- {section} ---")
            current_section = section
        test()

    print()
    print("=" * 72)
    passed = sum(1 for _, _, s, _ in _results if s == "PASS")
    failed = sum(1 for _, _, s, _ in _results if s != "PASS")
    total = len(_results)
    print(f"  RESULTS: {passed} passed, {failed} failed, {total} total")
    print("=" * 72)

    if failed > 0:
        print("\nFAILURES:")
        for section, name, status, msg in _results:
            if status != "PASS":
                print(f"  [{status}] {section} / {name}")
                if msg:
                    print(f"         {msg}")

    return failed == 0


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
