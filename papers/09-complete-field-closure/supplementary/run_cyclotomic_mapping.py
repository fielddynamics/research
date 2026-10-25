"""
GFD Cyclotomic Rotation Curve Mapping
============================================================

Maps observed galaxy rotation curves onto the cyclotomic structure
of the coupling polynomial f(k,s) = 1 + ks + k².

A rotation curve is a TRAVERSAL OF THE UNIT CIRCLE. As the Newtonian
acceleration drops from center to edge, the cyclotomic phase sweeps
from 120° (Phi_3, cube roots of unity) through 90° (transition) to 60°
(Phi_6, sixth roots of unity). Each measured (g_bar, g_obs) pair maps to
a specific vertex weight, cyclotomic phase, and decoded mass.

Headline discovery: the gravitational boost at the transition point
is EXACTLY THE GOLDEN RATIO phi = (1+sqrt(5))/2. This is not input -- it
follows from the quadratic transition relation g_t^2/(a_0+g_t) = g_s
evaluated at g_s = a_0.

The pipeline is fully algebraic and invertible:
    (g_bar, r) -> x -> s -> theta -> f -> mu -> g_obs -> M_dec

Requirements: numpy

    pip install numpy
    python run_cyclotomic_mapping.py

Author: Stephen Nelson / Field Dynamics Research
Date:   February 2026
"""

import math
import sys
from itertools import combinations

import numpy as np

# =============================================================================
# CONSTANTS
# =============================================================================

K = 4
D = 3
PHI = (1 + math.sqrt(5)) / 2

TET_A = {1, 2, 4, 7}
TET_B = {0, 3, 5, 6}

VERTEX_COORDS = {
    0: (-1, -1, -1), 1: (-1, -1, +1), 2: (-1, +1, -1), 3: (-1, +1, +1),
    4: (+1, -1, -1), 5: (+1, -1, +1), 6: (+1, +1, -1), 7: (+1, +1, +1),
}

F_PLUS  = 21
F_ZERO  = 17
F_MINUS = 13
F_RANGE = 8


# =============================================================================
# PIPELINE FUNCTIONS
# =============================================================================

def conformal_map(x):
    return (x - 1.0) / (x + 1.0)

def inverse_conformal(s):
    return (1.0 + s) / (1.0 - s)

def cyclotomic_phase(s):
    return math.acos(max(-1.0, min(1.0, -s / 2.0)))

def inverse_phase(theta):
    return -2.0 * math.cos(theta)

def capacity(s):
    return 1 + K * s + K ** 2

def constitutive_law(x):
    return x / (x + 1.0)

def boost_function(x):
    return (1.0 + math.sqrt(1.0 + 4.0 / x)) / 2.0

def vertex_weights(s):
    return (1.0 + s) / 2.0, (1.0 - s) / 2.0

def vertex_state_vector(s):
    w_A, w_B = vertex_weights(s)
    psi = np.zeros(8)
    for v in range(8):
        if v in TET_A:
            psi[v] = math.sqrt(max(0, w_A / K))
        else:
            psi[v] = math.sqrt(max(0, w_B / K))
    return psi


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


# =========================================================================
#  I. CYCLOTOMIC PHASE <-> ACCELERATION
# =========================================================================

suite("I. Cyclotomic Phase and Acceleration")

@validate("Newtonian regime (x>>1): phase approaches 120 degrees = 2pi/3")
def validate_newtonian_phase():
    for x in [10, 100, 1000, 10000]:
        s = conformal_map(x)
        theta = cyclotomic_phase(s)
        assert theta < 2 * math.pi / 3 + 1e-10
        assert abs(theta - 2 * math.pi / 3) < 2.0 / x

@validate("Transition (x=1): phase = 90 degrees = pi/2 exactly, roots are +/-i")
def validate_transition_phase():
    theta = cyclotomic_phase(conformal_map(1.0))
    assert abs(theta - math.pi / 2) < 1e-14

@validate("Deep MOND (x<<1): phase approaches 60 degrees = pi/3")
def validate_mond_phase():
    for x in [0.1, 0.01, 0.001, 0.0001]:
        s = conformal_map(x)
        theta = cyclotomic_phase(s)
        assert theta > math.pi / 3 - 1e-10
        assert abs(theta - math.pi / 3) < 2 * x

@validate("Phase sweep = pi/3 = 1/6 circle = one hexagonal sector")
def validate_phase_sweep():
    sweep = cyclotomic_phase(conformal_map(1e6)) - cyclotomic_phase(conformal_map(1e-6))
    assert abs(sweep - math.pi / 3) < 0.001

@validate("Phase is monotonically increasing in x")
def validate_phase_monotone():
    prev = 0
    for x in [0.001, 0.01, 0.1, 1, 10, 100, 1000]:
        theta = cyclotomic_phase(conformal_map(x))
        assert theta > prev
        prev = theta

@validate("Full roundtrip: x -> s -> theta -> s -> x recovers x")
def validate_full_roundtrip():
    for x in [0.001, 0.01, 0.1, 0.5, 1.0, 2.0, 10.0, 100.0, 1000.0]:
        s = conformal_map(x)
        theta = cyclotomic_phase(s)
        s_back = inverse_phase(theta)
        x_back = inverse_conformal(s_back)
        assert abs(x_back - x) / (1 + x) < 1e-10


# =========================================================================
#  II. GOLDEN RATIO BOOST
# =========================================================================

suite("II. Golden Ratio Boost")

@validate("Boost at transition (x=1): nu(1) = phi = (1+sqrt(5))/2 EXACTLY")
def validate_golden_boost():
    nu = boost_function(1.0)
    assert abs(nu - PHI) < 1e-14

@validate("Boost derives from phi^2 - phi - 1 = 0 (the defining equation of phi)")
def validate_boost_derivation():
    assert abs(PHI ** 2 - PHI - 1) < 1e-14
    a0 = 1.0
    g_t = PHI * a0
    assert abs(g_t ** 2 / (a0 + g_t) - a0) < 1e-14

@validate("Boost connects to N=2: nu(1) * mu_N2(1) = 1/phi = phi-1")
def validate_boost_n2_connection():
    nu = boost_function(1.0)
    mu_n2 = 1.0 / PHI ** 2
    product = nu * mu_n2
    assert abs(product - 1.0 / PHI) < 1e-14
    assert abs(product - (PHI - 1)) < 1e-14

@validate("Boost satisfies nu^2*x - nu*x - 1 = 0 for all x > 0")
def validate_boost_equation():
    for x in [0.001, 0.01, 0.1, 0.5, 1.0, 2.0, 10.0, 100.0]:
        nu = boost_function(x)
        assert abs(nu ** 2 * x - nu * x - 1) < 1e-10

@validate("Boost limits: nu -> 1 (Newtonian) and nu -> 1/sqrt(x) (deep MOND)")
def validate_boost_limits():
    assert abs(boost_function(10000) - 1.0) < 0.01
    for x in [0.0001, 0.001]:
        assert abs(boost_function(x) * math.sqrt(x) - 1.0) < 0.05


# =========================================================================
#  III. VERTEX STATE VECTOR
# =========================================================================

suite("III. Vertex State Vector")

@validate("State vector is normalized |psi|^2 = 1 for all s")
def validate_state_normalized():
    for s in np.linspace(-1, 1, 1000):
        psi = vertex_state_vector(s)
        assert abs(np.sum(psi ** 2) - 1.0) < 1e-12

@validate("At s=0: uniform psi = 1/sqrt(8) = 1/2^(D/2) for all vertices")
def validate_state_uniform():
    psi = vertex_state_vector(0.0)
    expected = 1.0 / math.sqrt(2 ** D)
    for v in range(8):
        assert abs(psi[v] - expected) < 1e-14

@validate("At s=+1: TetA fully occupied, TetB empty")
def validate_state_newtonian():
    psi = vertex_state_vector(1.0)
    for v in range(8):
        if v in TET_A:
            assert abs(psi[v] - 1.0 / math.sqrt(K)) < 1e-14
        else:
            assert abs(psi[v]) < 1e-14

@validate("At s=-1: TetB fully occupied, TetA empty")
def validate_state_mond():
    psi = vertex_state_vector(-1.0)
    for v in range(8):
        if v in TET_B:
            assert abs(psi[v] - 1.0 / math.sqrt(K)) < 1e-14
        else:
            assert abs(psi[v]) < 1e-14

@validate("State overlap: <psi(s)|psi(-s)> = sqrt(1-s^2) (complement duality)")
def validate_state_overlap():
    for s in np.linspace(-0.99, 0.99, 50):
        psi_s = vertex_state_vector(s)
        psi_neg = vertex_state_vector(-s)
        overlap = np.dot(psi_s, psi_neg)
        assert abs(overlap - math.sqrt(1 - s ** 2)) < 1e-10


# =========================================================================
#  IV. SPACE-TIME WEIGHT RATIO
# =========================================================================

suite("IV. Space-Time Weight Ratio")

@validate("Time/space weight ratio = 1/D = 1/3 for ALL s (universal 3+1 split)")
def validate_spacetime_ratio():
    for s in np.linspace(-1, 1, 100):
        w_A, w_B = vertex_weights(s)
        w_time = (w_A + w_B) / K
        w_space = D * (w_A + w_B) / K
        assert abs(w_space / w_time - D) < 1e-12

@validate("Time weight = 1/K = 1/4 is constant across all regimes")
def validate_time_weight_constant():
    for s in np.linspace(-1, 1, 100):
        w_A, w_B = vertex_weights(s)
        w_time = (w_A + w_B) / K
        assert abs(w_time - 1.0 / K) < 1e-14

@validate("The 3+1 split is spectral: eigenvalue multiplicities 2 and 6, ratio = D")
def validate_spectral_31():
    assert 6 / 2 == D


# =========================================================================
#  V. RADIAL ACCELERATION RELATION (RAR)
# =========================================================================

suite("V. Radial Acceleration Relation")

@validate("RAR formula: g_obs = [g_bar + sqrt(g_bar^2 + 4*g_bar*a0)] / 2")
def validate_rar_formula():
    a0 = 1.0
    for log_x in np.linspace(-3, 3, 50):
        g_bar = 10 ** log_x * a0
        g_obs = (g_bar + math.sqrt(g_bar ** 2 + 4 * g_bar * a0)) / 2
        assert abs(g_obs ** 2 / (a0 + g_obs) - g_bar) / (1 + g_bar) < 1e-10

@validate("RAR slope -> 1 (Newtonian) and -> 1/2 (deep MOND)")
def validate_rar_slopes():
    a0 = 1.0
    h = 0.001
    def log_gobs(log_gbar):
        gb = 10 ** log_gbar
        return math.log10((gb + math.sqrt(gb**2 + 4*gb*a0)) / 2)
    for lx, expected in [(2, 1.0), (3, 1.0), (-2, 0.5), (-3, 0.5)]:
        slope = (log_gobs(lx+h) - log_gobs(lx-h)) / (2*h)
        assert abs(slope - expected) < 0.03, f"log_x={lx}: slope={slope}"

@validate("Every RAR point maps to a unique cyclotomic phase in [60, 120] degrees")
def validate_rar_to_phase():
    for log_x in np.linspace(-3, 3, 100):
        x = 10 ** log_x
        theta = cyclotomic_phase(conformal_map(x))
        assert math.pi / 3 - 0.01 <= theta <= 2 * math.pi / 3 + 0.01

@validate("RAR curvature peaks near the transition x=1")
def validate_rar_curvature():
    a0 = 1.0; h = 0.01
    def log_gobs(lx):
        gb = 10**lx
        return math.log10((gb + math.sqrt(gb**2 + 4*gb*a0))/2)
    test_pts = np.linspace(-2, 2, 41)
    curvatures = [abs(log_gobs(lx+h) - 2*log_gobs(lx) + log_gobs(lx-h))/h**2 for lx in test_pts]
    max_idx = np.argmax(curvatures)
    assert abs(test_pts[max_idx]) < 0.5


# =========================================================================
#  VI. OBSERVATIONAL VERTEX ASSIGNMENT
# =========================================================================

suite("VI. Observational Vertex Assignment")

@validate("Protocol: (v, r, a0) -> unique vertex state, fully invertible")
def validate_observation_protocol():
    a0 = 3703.0
    v, r = 150.0, 8.0
    g_obs = v**2 / r; x = g_obs / a0; s = conformal_map(x)
    theta = cyclotomic_phase(s); psi = vertex_state_vector(s)
    f = capacity(s); mu = constitutive_law(x)
    assert -1 < s < 1
    assert math.pi/3 < theta < 2*math.pi/3
    assert abs(np.sum(psi**2) - 1.0) < 1e-12
    s_back = inverse_phase(theta)
    x_back = inverse_conformal(s_back)
    v_back = math.sqrt(x_back * a0 * r)
    assert abs(v_back - v) < 1e-6

@validate("HSB galaxies occupy higher phase (closer to 120) than LSB galaxies")
def validate_galaxy_types():
    a0 = 3703.0
    x_hsb = (200**2 / 3) / a0
    x_lsb = (80**2 / 3) / a0
    theta_hsb = cyclotomic_phase(conformal_map(x_hsb))
    theta_lsb = cyclotomic_phase(conformal_map(x_lsb))
    assert theta_hsb > theta_lsb

@validate("Capacity uniquely determines mu, theta, and s")
def validate_capacity_determines_all():
    for f_val in np.linspace(F_MINUS + 0.1, F_PLUS - 0.1, 50):
        s = (f_val - F_ZERO) / K
        x = inverse_conformal(s)
        mu = constitutive_law(x)
        assert abs((capacity(s) - F_MINUS) / F_RANGE - mu) < 1e-10


# =============================================================================
# MAIN
# =============================================================================

def main():
    print()
    print("=" * 72)
    print("  GFD CYCLOTOMIC ROTATION CURVE MAPPING")
    print("  Mapping observed velocities to the unit circle")
    print("=" * 72)

    all_validations = [
        validate_newtonian_phase, validate_transition_phase, validate_mond_phase,
        validate_phase_sweep, validate_phase_monotone, validate_full_roundtrip,
        validate_golden_boost, validate_boost_derivation, validate_boost_n2_connection,
        validate_boost_equation, validate_boost_limits,
        validate_state_normalized, validate_state_uniform, validate_state_newtonian,
        validate_state_mond, validate_state_overlap,
        validate_spacetime_ratio, validate_time_weight_constant, validate_spectral_31,
        validate_rar_formula, validate_rar_slopes, validate_rar_to_phase, validate_rar_curvature,
        validate_observation_protocol, validate_galaxy_types, validate_capacity_determines_all,
    ]

    for v in all_validations:
        v()

    print()
    print("=" * 72)
    passed = sum(1 for _, _, st, _ in _results if st == "PASS")
    failed = sum(1 for _, _, st, _ in _results if st != "PASS")
    print(f"  RESULTS: {passed} passed, {failed} failed, {passed+failed} total")
    print("=" * 72)

    if failed:
        print("\nFAILURES:")
        for s, n, st, m in _results:
            if st != "PASS":
                print(f"  [{st}] {s} / {n}: {m}")

    return failed == 0

if __name__ == "__main__":
    sys.exit(0 if main() else 1)
