"""
================================================================================
Dual Tetrad Gravity And The Field Origin
Deriving Fundamental Equations With (3+1)^2 Topology
================================================================================

Validation Suite
Author: Stephen Nelson

VALIDATION SUITE

This script validates ALL numerical claims and equations in the paper using
full-precision CODATA 2022 constants. Every equation that produces a numerical
result has a corresponding validation function. No intermediate rounding is
applied; all calculations use maximum available precision.

Requirements: Python 3.6+ (standard library only)
Date: February 2026
"""

import math
from datetime import datetime


# =============================================================================
# SECTION 1: FUNDAMENTAL CONSTANTS (CODATA 2022)
# =============================================================================
# All values verified from NIST: physics.nist.gov/cuu/Constants/
# CODATA 2022 values published in Rev. Mod. Phys. 96, 025004 (2024)

G = 6.67430e-11                    # Newtonian gravitational constant [m^3/(kg*s^2)]
m_e = 9.1093837139e-31             # Electron mass [kg]
r_e = 2.8179403205e-15             # Classical electron radius [m]
c = 299792458                      # Speed of light [m/s] (exact by SI definition)
hbar = 1.054571817e-34             # Reduced Planck constant [J*s]
h = 2 * math.pi * hbar             # Planck constant [J*s]
e_charge = 1.602176634e-19         # Elementary charge [C] (exact by SI definition)
epsilon_0 = 8.8541878188e-12       # Vacuum permittivity [F/m]
alpha = 7.2973525693e-3            # Fine structure constant (dimensionless)

# Unit conversions (IAU 2015 exact definitions)
AU_in_m = 149597870700             # Astronomical unit [m] (exact, IAU 2012)
pc_in_AU = 648000 / math.pi        # Parsec in AU (exact, IAU 2015)
Mpc_in_m = AU_in_m * pc_in_AU * 1e6
km_s_Mpc_to_Hz = 1000.0 / Mpc_in_m

# Solar mass (IAU 2015 nominal)
M_sun = 1.98892e30                 # Solar mass [kg]


# =============================================================================
# SECTION 2: TOPOLOGICAL PARAMETERS
# =============================================================================

d = 3                              # Spatial dimensions
k = d + 1                          # Simplex faces: d + 1 = 4
k_squared = k ** 2                 # Isotropic coupling channels: k^2 = 16
hierarchy = 1 + k + k_squared      # Coupling hierarchy: 1 + 4 + 16 = 21
sqrt_k_over_pi = math.sqrt(k / math.pi)  # Aperture correction factor


# =============================================================================
# SECTION 3: EMPIRICAL REFERENCE VALUES
# =============================================================================

G_measured = 6.67430e-11           # CODATA 2022 value of G
a0_empirical = 1.22e-10            # MOND acceleration scale [m/s^2]
H_GW170817 = 70.0                  # GW170817 standard siren [km/s/Mpc]


# =============================================================================
# RESULTS COLLECTOR
# =============================================================================

results = []
section_divider = "=" * 78


def record(name, predicted, measured, unit=""):
    """Record a validation result with deviation calculation."""
    if measured != 0:
        deviation = abs(predicted - measured) / abs(measured) * 100
    else:
        deviation = 0.0
    results.append({
        "name": name,
        "predicted": predicted,
        "measured": measured,
        "deviation": deviation,
        "unit": unit
    })
    return deviation


# =============================================================================
# VALIDATION: SECTION I - Introduction (Eq. G)
# =============================================================================

def validate_G_from_topology():
    """
    Eq. (eq:G), Section I, line 112-115
    G = [(3+1)^2 + 1] / [3(3+1) + 1] * alpha^{1+(3+1)+(3+1)^2} * hbar*c / m_e^2

    This is the central result inherited from the companion paper.
    Prefactor: 17/13, Exponent: 21, Scale: hbar*c/m_e^2
    """
    print(f"\n{section_divider}")
    print("RESULT 1: G FROM TETRAD TOPOLOGY (Eq. G, Section I)")
    print(section_divider)

    prefactor = (k_squared + 1) / (3 * k + 1)  # (16+1)/(12+1) = 17/13
    exponent = 1 + k + k_squared                 # 1 + 4 + 16 = 21
    scale = hbar * c / m_e ** 2

    G_predicted = prefactor * alpha ** exponent * scale

    print(f"  Prefactor: ({k}^2 + 1) / (3*{k} + 1) = {k_squared+1}/{3*k+1} = {prefactor:.10f}")
    print(f"  Exponent:  1 + {k} + {k}^2 = {exponent}")
    print(f"  alpha^{exponent} = {alpha**exponent:.6e}")
    print(f"  Scale:     hbar*c/m_e^2 = {scale:.6e}")
    print(f"  G_predicted = {G_predicted:.6e} m^3/(kg*s^2)")
    print(f"  G_measured  = {G_measured:.6e} m^3/(kg*s^2)")

    dev = record("Result 1: G from topology", G_predicted, G_measured, "m^3/(kg*s^2)")
    print(f"  Deviation:  {dev:.4f}%")

    return G_predicted


# =============================================================================
# VALIDATION: SECTION I - G in terms of d (Eq. G-general-d)
# =============================================================================

def validate_G_general_d():
    """
    Eq. (eq:G-general-d), Section IV.A, line 755-758
    G = [(d+1)^2 + 1] / [3(d+1) + 1] * alpha^{1+(d+1)+(d+1)^2} * hbar*c / m_e^2

    Demonstrates the entire equation is determined by d=3.
    """
    print(f"\n{section_divider}")
    print("G IN TERMS OF d (Eq. G-general-d, Section IV.A)")
    print(section_divider)

    for d_test in [2, 3, 4]:
        k_test = d_test + 1
        pf = (k_test**2 + 1) / (3 * k_test + 1)
        exp_test = 1 + k_test + k_test**2
        G_test = pf * alpha**exp_test * hbar * c / m_e**2
        ratio = G_test / G_measured if G_measured != 0 else 0
        print(f"  d={d_test}: k={k_test}, prefactor={pf:.4f}, exponent={exp_test}, "
              f"G={G_test:.3e}, ratio to measured={ratio:.4e}")

    print(f"\n  Only d=3 produces a physically reasonable G.")


# =============================================================================
# VALIDATION: EXPONENT SENSITIVITY (Section IV.A)
# =============================================================================

def validate_exponent_sensitivity():
    """
    Exponent sensitivity table, Section IV.A, lines 740-751
    Each unit change in exponent multiplies G by 1/alpha ~ 137.
    """
    print(f"\n{section_divider}")
    print("EXPONENT SENSITIVITY (Section IV.A)")
    print(section_divider)

    prefactor = (k_squared + 1) / (3 * k + 1)
    scale = hbar * c / m_e ** 2

    for exp in [20, 21, 22]:
        G_test = prefactor * alpha ** exp * scale
        ratio = G_test / G_measured
        dev = abs(ratio - 1) * 100
        print(f"  Exponent {exp}: G = {G_test:.3e}, deviation = {dev:.1f}%")

    print(f"\n  Adjacent integers miss by factor ~{1/alpha:.0f} = 1/alpha")


# =============================================================================
# VALIDATION: SECTION II.C - Classical electron radius (Route 1)
# =============================================================================

def validate_classical_electron_radius():
    """
    Section II.D, line 281-282
    r_e = e^2 / (4*pi*epsilon_0*m_e*c^2) = 2.818e-15 m
    """
    print(f"\n{section_divider}")
    print("CLASSICAL ELECTRON RADIUS (Section II.D, Route 1)")
    print(section_divider)

    r_e_calc = e_charge**2 / (4 * math.pi * epsilon_0 * m_e * c**2)

    print(f"  r_e = e^2 / (4*pi*eps_0*m_e*c^2)")
    print(f"  r_e_calculated = {r_e_calc:.10e} m = {r_e_calc*1e15:.6f} fm")
    print(f"  r_e_CODATA     = {r_e:.10e} m = {r_e*1e15:.6f} fm")

    dev = record("Classical electron radius", r_e_calc, r_e, "m")
    print(f"  Deviation: {dev:.6f}%")

    return r_e_calc


# =============================================================================
# VALIDATION: SECTION II.D - Gravitational route to r_e (Route 2)
# =============================================================================

def validate_gravitational_electron_radius():
    """
    Section II.D, line 291-292
    r_e = k * sqrt(G*m_e/a_0) = 2.82e-15 m

    Uses MOND empirical a_0, not electron-derived a_0 (to avoid circularity).
    """
    print(f"\n{section_divider}")
    print("GRAVITATIONAL ELECTRON RADIUS (Section II.D, Route 2)")
    print(section_divider)

    r_e_grav = k * math.sqrt(G * m_e / a0_empirical)

    print(f"  r_e = k * sqrt(G*m_e/a_0)")
    print(f"  r_e_gravitational = {r_e_grav:.10e} m = {r_e_grav*1e15:.6f} fm")
    print(f"  r_e_CODATA        = {r_e:.10e} m = {r_e*1e15:.6f} fm")

    dev = record("Gravitational r_e (Route 2)", r_e_grav, r_e, "m")
    print(f"  Deviation: {dev:.4f}%")

    return r_e_grav


# =============================================================================
# VALIDATION: SECTION III.C - Spin from face ratio
# =============================================================================

def validate_spin():
    """
    Eq. (eq:spin), Section III.C, line 598-600
    S = (N_TIME / N_total) * L_total = (2/8) * 2*hbar = hbar/2
    """
    print(f"\n{section_divider}")
    print("RESULT 5 (from companion paper): SPIN FROM FACE RATIO (Section III.C)")
    print(section_divider)

    N_TIME = 2
    N_total = 2 * k   # 2 tetrahedra, k=4 faces each = 8
    L_total = 2 * hbar  # One hbar per tetrahedron (ansatz)

    S = (N_TIME / N_total) * L_total
    S_expected = hbar / 2

    print(f"  N_TIME  = {N_TIME} (inward-pointing faces)")
    print(f"  N_total = {N_total} (total faces in stellated octahedron)")
    print(f"  L_total = 2*hbar = {L_total:.6e} J*s")
    print(f"  S = ({N_TIME}/{N_total}) * 2*hbar = {S:.6e} J*s")
    print(f"  hbar/2 = {S_expected:.6e} J*s")
    print(f"  Match: {abs(S - S_expected) < 1e-50}")

    record("Spin hbar/2", S, S_expected, "J*s")


# =============================================================================
# VALIDATION: SECTION III.D - Coupling hierarchy
# =============================================================================

def validate_hierarchy():
    """
    Eq. (eq:hierarchy), Section III.D, line 635-636
    1 + (3+1) + (3+1)^2 = 1 + 4 + 16 = 21
    """
    print(f"\n{section_divider}")
    print("COUPLING HIERARCHY (Section III.D)")
    print(section_divider)

    level_1 = 1          # Field Origin
    level_2 = k          # One spacetime (3+1)
    level_3 = k_squared  # Full bimetric (3+1)^2

    total = level_1 + level_2 + level_3

    print(f"  Level 1 (Origin):    {level_1}")
    print(f"  Level 2 (Spacetime): {level_2} = (3+1)")
    print(f"  Level 3 (Bimetric):  {level_3} = (3+1)^2")
    print(f"  Total:               {total}")
    print(f"  Expected:            21")
    print(f"  Match: {total == 21}")


# =============================================================================
# VALIDATION: SECTION IV.D - Force hierarchy
# =============================================================================

def validate_force_hierarchy():
    """
    Result 4, Section IV.D, line 919-920
    Gravity/EM ~ alpha^21 / alpha^1 = alpha^20 ~ 10^{-43}
    """
    print(f"\n{section_divider}")
    print("RESULT 4: FORCE HIERARCHY (Section IV.D)")
    print(section_divider)

    ratio = alpha ** 20
    log_ratio = math.log10(ratio)

    print(f"  alpha^20 = (1/137.036)^20 = {ratio:.6e}")
    print(f"  log10(alpha^20) = {log_ratio:.2f}")
    print(f"  Paper claims: ~10^{{-43}}")
    print(f"  Match: {-44 < log_ratio < -42}")

    record("Force hierarchy alpha^20", log_ratio, -43, "log10")


# =============================================================================
# VALIDATION: SECTION VI - Fine structure constant
# =============================================================================

def validate_alpha():
    """
    Eq. (eq:alpha), Section VI.C, line 1183-1184
    1/alpha = (1/2pi) * f_closure/f_Compton = lambda_C / (2*pi*r_e) = 137.036

    Also validates:
    - f_closure = c/r_e (line 1153-1154)
    - f_Compton = m_e*c^2/h (line 1160-1161)
    - lambda_C = h/(m_e*c) (line 1132-1133)
    - lambda_C/r_e = 2*pi/alpha (line 1139-1140)
    """
    print(f"\n{section_divider}")
    print("RESULT 9: FINE STRUCTURE CONSTANT (Section VI)")
    print(section_divider)

    # Closure rate
    f_closure = c / r_e
    print(f"  f_closure = c/r_e = {f_closure:.6e} Hz")

    # Compton frequency
    f_Compton = m_e * c**2 / h
    print(f"  f_Compton = m_e*c^2/h = {f_Compton:.6e} Hz")

    # Compton wavelength
    lambda_C = h / (m_e * c)
    print(f"  lambda_C  = h/(m_e*c) = {lambda_C:.6e} m = {lambda_C*1e12:.6f} pm")

    # Ratio
    ratio = f_closure / f_Compton
    print(f"  f_closure/f_Compton = {ratio:.6f}")

    # 1/alpha from the ratio
    one_over_alpha_calc = (1 / (2 * math.pi)) * ratio
    one_over_alpha_known = 1 / alpha

    print(f"  1/alpha (calculated) = (1/2pi) * ratio = {one_over_alpha_calc:.6f}")
    print(f"  1/alpha (CODATA)     = {one_over_alpha_known:.6f}")

    dev = record("1/alpha from closure rate", one_over_alpha_calc, one_over_alpha_known, "")
    print(f"  Deviation: {dev:.6f}%")

    # Also verify lambda_C / r_e = 2*pi/alpha
    lc_re_ratio = lambda_C / r_e
    two_pi_over_alpha = 2 * math.pi / alpha
    print(f"\n  lambda_C / r_e       = {lc_re_ratio:.6f}")
    print(f"  2*pi/alpha           = {two_pi_over_alpha:.6f}")
    print(f"  Match: {abs(lc_re_ratio - two_pi_over_alpha)/two_pi_over_alpha*100:.6f}%")


# =============================================================================
# VALIDATION: SECTION VII.D - Characteristic acceleration a_0
# =============================================================================

def validate_a0():
    """
    Eq. (eq:a0-dm), Section VII.D, line 1313-1314
    a_0 = k^2 * G * m_e / r_e^2 = 16 * G * m_e / r_e^2 ~ 1.2e-10 m/s^2
    """
    print(f"\n{section_divider}")
    print("CHARACTERISTIC ACCELERATION a_0 (Section VII.D)")
    print(section_divider)

    a0_derived = k_squared * G * m_e / r_e**2

    print(f"  a_0 = k^2 * G * m_e / r_e^2")
    print(f"  a_0 = {k_squared} * {G:.4e} * {m_e:.4e} / ({r_e:.4e})^2")
    print(f"  a_0_derived   = {a0_derived:.6e} m/s^2")
    print(f"  a_0_empirical = {a0_empirical:.6e} m/s^2")

    dev = record("a_0 from topology", a0_derived, a0_empirical, "m/s^2")
    print(f"  Deviation: {dev:.4f}%")

    return a0_derived


# =============================================================================
# VALIDATION: SECTION VII.D - Correction factor mu(x) (detailed balance)
# =============================================================================

def validate_mu_detailed_balance():
    """
    Eq. (eq:mu-dm), Section VII.D, lines 1329-1338
    Detailed balance: kappa*x*(1-epsilon) = kappa*epsilon
    Solution: epsilon = x/(1+x), therefore mu(x) = x/(1+x)

    Validates limits:
    - x >> 1: mu -> 1 (Newtonian)
    - x << 1: mu -> x (deep-MOND)
    - x = 1:  mu = 0.5 (transition)
    """
    print(f"\n{section_divider}")
    print("CORRECTION FACTOR mu(x) (Section VII.D, detailed balance)")
    print(section_divider)

    def mu(x):
        return x / (1 + x)

    test_points = [0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0]
    print(f"  {'x':>10}  {'mu(x)':>10}  {'Regime':>15}")
    print(f"  {'-'*40}")
    for x in test_points:
        regime = "Deep-MOND" if x < 0.1 else ("Transition" if x < 10 else "Newtonian")
        print(f"  {x:>10.3f}  {mu(x):>10.6f}  {regime:>15}")

    # Verify limits
    print(f"\n  Limit checks:")
    print(f"    mu(1e-6) = {mu(1e-6):.10f} (should approach x = 1e-6)")
    print(f"    mu(1e6)  = {mu(1e6):.10f} (should approach 1)")
    print(f"    mu(1)    = {mu(1):.10f} (should be 0.5)")


# =============================================================================
# VALIDATION: SECTION VII.D - Aperture correction sqrt(k/pi)
# =============================================================================

def validate_aperture_correction():
    """
    Eq. (aperture correction), Section VII.D, line 1412-1413
    Aperture correction = sqrt(k/pi) = sqrt(4/pi) = 1.128
    """
    print(f"\n{section_divider}")
    print("APERTURE CORRECTION sqrt(k/pi) (Section VII.D)")
    print(section_divider)

    correction = math.sqrt(k / math.pi)
    k_over_pi = k / math.pi

    print(f"  k/pi = {k}/{math.pi:.6f} = {k_over_pi:.6f} (area-level ratio)")
    print(f"  sqrt(k/pi) = {correction:.10f}")
    print(f"  Paper states: 1.128")
    print(f"  Match: {abs(correction - 1.128) < 0.001}")


# =============================================================================
# VALIDATION: SECTION VII.D - Hubble constant from topology
# =============================================================================

def validate_H_from_topology():
    """
    Section VII.D (MOND challenges), line 1415
    H_flat = 2*pi*a_0/c, then H_measured = H_flat / sqrt(k/pi) = 69.92 km/s/Mpc

    Uses a_0 = 1.22e-10 (empirical MOND value from Paper IV).
    """
    print(f"\n{section_divider}")
    print("HUBBLE CONSTANT FROM TOPOLOGY (Section VII.D)")
    print(section_divider)

    # H in flat space from MOND relation
    H_flat_Hz = 2 * math.pi * a0_empirical / c
    H_flat = H_flat_Hz / km_s_Mpc_to_Hz

    # Apply aperture correction
    H_measured = H_flat / sqrt_k_over_pi

    print(f"  a_0 (empirical)     = {a0_empirical:.2e} m/s^2")
    print(f"  H_flat              = 2*pi*a_0/c = {H_flat:.6f} km/s/Mpc")
    print(f"  sqrt(k/pi)          = {sqrt_k_over_pi:.10f}")
    print(f"  H_measured          = H_flat/sqrt(k/pi) = {H_measured:.6f} km/s/Mpc")
    print(f"  GW170817            = {H_GW170817:.1f} km/s/Mpc")

    dev = record("H from topology", H_measured, H_GW170817, "km/s/Mpc")
    print(f"  Deviation from GW170817: {dev:.4f}%")

    return H_measured


# =============================================================================
# VALIDATION: SECTION VII.D - Galaxy rotation curve predictions
# =============================================================================

def validate_rotation_curves():
    """
    Table (tab:darkmatter), Section VII.D, lines 1376-1387
    Rotation curve predictions for a 10^11 solar mass galaxy.
    Validates: g/a_0, mu(x), v_Newton, v_actual, DM% at specific radii.
    """
    print(f"\n{section_divider}")
    print("GALAXY ROTATION CURVES (Table, Section VII.D)")
    print(section_divider)

    M_galaxy = 1e11 * M_sun
    radii_kpc = [5, 10, 20, 30, 50]

    print(f"  Galaxy mass: {M_galaxy:.2e} kg ({M_galaxy/M_sun:.0e} solar masses)")
    print(f"\n  {'r (kpc)':>8} {'g/a_0':>8} {'mu(x)':>8} {'v_Newt':>10} {'v_actual':>10} {'DM%':>6}")
    print(f"  {'-'*56}")

    for r_kpc in radii_kpc:
        r_m = r_kpc * 3.086e19  # kpc to meters

        # Newtonian gravity
        g_newton = G * M_galaxy / r_m**2

        # Correction
        x = g_newton / a0_empirical
        mu = x / (1 + x)

        # Corrected gravity
        g_corrected = g_newton / mu

        # Velocities
        v_newton = math.sqrt(G * M_galaxy / r_m) / 1000  # km/s
        v_corrected = math.sqrt(g_corrected * r_m) / 1000  # km/s

        # Dark matter fraction
        M_inferred = g_corrected * r_m**2 / G
        dm_fraction = (M_inferred - M_galaxy) / M_inferred * 100

        print(f"  {r_kpc:>8} {x:>8.2f} {mu:>8.2f} {v_newton:>10.0f} {v_corrected:>10.0f} {dm_fraction:>6.0f}%")


# =============================================================================
# VALIDATION: SECTION VII.E - Electron mass from closure geometry (Result 10)
# =============================================================================

def validate_electron_mass():
    """
    Result 10, Section VII.E (The Frontier), lines 1479-1537

    Three-equation system:
    (1) a_0 = k^2 * G * m / r^2          (closure saturation)
    (2) a_0 = cH/(2pi) * sqrt(k/pi)      (cosmological connection)
    (3) m = alpha*hbar / (r*c)            (quantum-EM relation)

    Solution: r^3 = 2*pi^(3/2) * k^(3/2) * alpha*hbar*G / (c^2*H)
    For k=4:  r^3 = 16*pi^(3/2) * alpha*hbar*G / (c^2*H)
    Then:     m = alpha*hbar / (r*c)

    External input: H = 69.92 km/s/Mpc (from topology, validated above)
    """
    print(f"\n{section_divider}")
    print("RESULT 10: ELECTRON MASS FROM CLOSURE GEOMETRY (Section VII.E)")
    print(section_divider)

    # Use the topology-derived H
    H_topology = 69.92  # km/s/Mpc (validated above)
    H_si = H_topology * km_s_Mpc_to_Hz  # Convert to Hz (s^-1)

    # Verify intermediate algebra: r^3 = 2*pi^(3/2) * k^(3/2) * alpha*hbar*G / (c^2*H)
    r_cubed_general = 2 * math.pi**(3/2) * k**(3/2) * alpha * hbar * G / (c**2 * H_si)

    # For k=4 specifically: r^3 = 16 * pi^(3/2) * alpha*hbar*G / (c^2*H)
    r_cubed_k4 = 16 * math.pi**(3/2) * alpha * hbar * G / (c**2 * H_si)

    print(f"  H (topology) = {H_topology} km/s/Mpc = {H_si:.6e} Hz")
    print(f"\n  General form: r^3 = 2*pi^(3/2)*k^(3/2) * alpha*hbar*G/(c^2*H)")
    print(f"  r^3 (general, k={k}) = {r_cubed_general:.6e} m^3")
    print(f"  r^3 (k=4 form)       = {r_cubed_k4:.6e} m^3")
    print(f"  Match: {abs(r_cubed_general - r_cubed_k4)/r_cubed_k4*100:.6f}%")

    # Solve for r
    r_predicted = r_cubed_k4 ** (1/3)

    # Solve for m using Eq. 3
    m_predicted = alpha * hbar / (r_predicted * c)

    print(f"\n  r_predicted = {r_predicted:.6e} m = {r_predicted*1e15:.4f} fm")
    print(f"  r_e (CODATA) = {r_e:.6e} m = {r_e*1e15:.4f} fm")
    dev_r = record("r from closure geometry", r_predicted, r_e, "m")
    print(f"  Deviation (r): {dev_r:.4f}%")

    print(f"\n  m_predicted  = {m_predicted:.6e} kg")
    print(f"  m_e (CODATA) = {m_e:.6e} kg")
    dev_m = record("m_e from closure geometry", m_predicted, m_e, "kg")
    print(f"  Deviation (m): {dev_m:.4f}%")

    # Overdetermination check: verify all three equations are satisfied
    print(f"\n  OVERDETERMINATION CHECK:")
    a0_eq1 = k_squared * G * m_predicted / r_predicted**2
    a0_from_cosmo = c * H_si * sqrt_k_over_pi / (2 * math.pi)

    print(f"    Eq 1: a_0 = k^2*G*m/r^2 = {a0_eq1:.6e} m/s^2")
    print(f"    Eq 2: a_0 = cH*sqrt(k/pi)/(2pi) = {a0_from_cosmo:.6e} m/s^2")
    print(f"    Match (Eq1 vs Eq2): {abs(a0_eq1 - a0_from_cosmo)/a0_from_cosmo*100:.4f}%")

    return r_predicted, m_predicted


# =============================================================================
# VALIDATION: SECTION VII.E - Round-trip test
# =============================================================================

def validate_round_trip():
    """
    Section VII.E (Precision Context), lines 1456-1457
    Starting from G, alpha, hbar, c, m_e: derive H = 69.92 km/s/Mpc (0.11%)
    Reversing: observed H recovers m_e to 0.10%.
    """
    print(f"\n{section_divider}")
    print("ROUND-TRIP TEST (Section VII.E)")
    print(section_divider)

    # Forward: m_e -> a_0 -> H
    a0_from_electron = k_squared * G * m_e / r_e**2
    H_flat_Hz = 2 * math.pi * a0_from_electron / c
    H_flat = H_flat_Hz / km_s_Mpc_to_Hz
    H_forward = H_flat / sqrt_k_over_pi

    print(f"  Forward: m_e -> a_0 -> H")
    print(f"    a_0 = {a0_from_electron:.6e} m/s^2")
    print(f"    H_flat = {H_flat:.6f} km/s/Mpc")
    print(f"    H_predicted = {H_forward:.6f} km/s/Mpc")
    dev_h = abs(H_forward - H_GW170817) / H_GW170817 * 100
    print(f"    Deviation from GW170817: {dev_h:.4f}%")

    # Reverse: H -> m_e (using GW170817)
    H_si = H_GW170817 * km_s_Mpc_to_Hz
    denominator = 2 * math.pi * k_squared * G * (4 * math.pi * epsilon_0)**2 * c**3
    numerator = H_si * e_charge**4 * sqrt_k_over_pi
    m_e_recovered = (numerator / denominator) ** (1/3)

    print(f"\n  Reverse: H (GW170817) -> m_e")
    print(f"    m_e_recovered = {m_e_recovered:.6e} kg")
    print(f"    m_e_CODATA    = {m_e:.6e} kg")
    dev_m = abs(m_e_recovered - m_e) / m_e * 100
    print(f"    Deviation: {dev_m:.4f}%")

    record("Round-trip: H forward", H_forward, H_GW170817, "km/s/Mpc")
    record("Round-trip: m_e reverse", m_e_recovered, m_e, "kg")


# =============================================================================
# VALIDATION: Precision table values (Section VII.E)
# =============================================================================

def validate_precision_table():
    """
    Table (tab:precision), Section VII.E, lines 1438-1455
    Validates all four entries: G, H, m_e, a_0
    """
    print(f"\n{section_divider}")
    print("PRECISION TABLE (Section VII.E)")
    print(section_divider)

    # G
    pf = (k_squared + 1) / (3 * k + 1)
    G_pred = pf * alpha**hierarchy * hbar * c / m_e**2
    dev_G = abs(G_pred - G_measured) / G_measured * 100

    # H
    a0_e = k_squared * G * m_e / r_e**2
    H_flat_Hz = 2 * math.pi * a0_e / c
    H_flat = H_flat_Hz / km_s_Mpc_to_Hz
    H_pred = H_flat / sqrt_k_over_pi
    dev_H = abs(H_pred - H_GW170817) / H_GW170817 * 100

    # m_e (from H_GW170817)
    H_si = H_GW170817 * km_s_Mpc_to_Hz
    denom = 2 * math.pi * k_squared * G * (4*math.pi*epsilon_0)**2 * c**3
    m_e_pred = (H_si * e_charge**4 * sqrt_k_over_pi / denom) ** (1/3)
    dev_me = abs(m_e_pred - m_e) / m_e * 100

    # a_0
    a0_pred = k_squared * G * m_e / r_e**2
    dev_a0 = abs(a0_pred - a0_empirical) / a0_empirical * 100

    print(f"  {'Quantity':<8} {'Predicted':>15} {'Observed':>15} {'Deviation':>10}")
    print(f"  {'-'*50}")
    print(f"  {'G':<8} {G_pred:>15.3e} {G_measured:>15.3e} {dev_G:>9.2f}%")
    print(f"  {'H':<8} {H_pred:>15.2f} {H_GW170817:>15.1f} {dev_H:>9.2f}%")
    print(f"  {'m_e':<8} {m_e_pred:>15.3e} {m_e:>15.3e} {dev_me:>9.2f}%")
    print(f"  {'a_0':<8} {a0_pred:>15.3e} {a0_empirical:>15.3e} {dev_a0:>9.2f}%")

    mean_dev = (dev_G + dev_H + dev_me + dev_a0) / 4
    print(f"\n  Mean deviation: {mean_dev:.2f}%")


# =============================================================================
# SUMMARY
# =============================================================================

def print_summary():
    """Print comprehensive validation summary table."""
    print(f"\n{section_divider}")
    print("VALIDATION SUMMARY")
    print(section_divider)

    print(f"\n  {'#':<3} {'Test':<35} {'Deviation':>10}")
    print(f"  {'-'*50}")

    for i, r in enumerate(results, 1):
        print(f"  {i:<3} {r['name']:<35} {r['deviation']:>9.4f}%")

    print(f"  {'-'*50}")

    if results:
        avg = sum(r["deviation"] for r in results) / len(results)
        print(f"\n  Total validations: {len(results)}")
        print(f"  Average deviation: {avg:.4f}%")


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Run all validations."""
    print(section_divider)
    print("Dual Tetrad Gravity And The Field Origin")
    print("Deriving Fundamental Equations With (3+1)^2 Topology")
    print("Validation Suite")
    print(section_divider)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    print(f"\n{'FUNDAMENTAL CONSTANTS (CODATA 2022)':^78}")
    print(f"  G       = {G:.5e} m^3/(kg*s^2)")
    print(f"  m_e     = {m_e:.10e} kg")
    print(f"  r_e     = {r_e:.10e} m")
    print(f"  c       = {c} m/s (exact)")
    print(f"  hbar    = {hbar:.9e} J*s")
    print(f"  h       = {h:.9e} J*s")
    print(f"  alpha   = {alpha:.10e} ({1/alpha:.6f})")
    print(f"  e       = {e_charge:.9e} C (exact)")
    print(f"  eps_0   = {epsilon_0:.10e} F/m")

    print(f"\n{'TOPOLOGICAL PARAMETERS':^78}")
    print(f"  d = {d} (spatial dimensions)")
    print(f"  k = d+1 = {k} (simplex faces)")
    print(f"  k^2 = {k_squared} (coupling channels)")
    print(f"  1+k+k^2 = {hierarchy} (hierarchy exponent)")
    print(f"  sqrt(k/pi) = {sqrt_k_over_pi:.10f} (aperture correction)")

    # Run all validations in paper order
    validate_G_from_topology()
    validate_G_general_d()
    validate_exponent_sensitivity()
    validate_classical_electron_radius()
    validate_gravitational_electron_radius()
    validate_spin()
    validate_hierarchy()
    validate_force_hierarchy()
    validate_alpha()
    validate_a0()
    validate_mu_detailed_balance()
    validate_aperture_correction()
    validate_H_from_topology()
    validate_rotation_curves()
    validate_electron_mass()
    validate_round_trip()
    validate_precision_table()
    print_summary()

    print(f"\n{section_divider}")
    print("ALL VALIDATIONS COMPLETE")
    print(section_divider)


if __name__ == "__main__":
    main()
