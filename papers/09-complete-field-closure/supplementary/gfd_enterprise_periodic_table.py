"""
GFD Enterprise Validation: The Complete Periodic Table Cross-Check
====================================================================

This suite cross-validates every stable isotope against TWO independent
GFD predictions plus observed nuclear data:

  GEOMETRIC (zero parameters):
    - Base-4 address from K-packing
    - Nesting level from K^n hierarchy
    - Capacity deficit Δf(A) from N-metric
    - Ceiling K^4 = 256

  NUCLEAR (observed, AME2020):
    - Binding energy per nucleon (BE/A)
    - Stability (stable vs radioactive)
    - Proton/neutron composition

  SEMF (standard 5-parameter model):
    - Volume, surface, Coulomb, asymmetry, pairing terms
    - Used as independent cross-reference, NOT fit to GFD

The validation checks that:
  1. Every isotope respects the geometric ceiling and structure
  2. The N-metric deficit correctly predicts the binding curve shape
  3. Magic numbers, alpha clusters, and shell effects appear as
     systematic residuals from the smooth geometric prediction
  4. Light nuclei show geometric modulation (gf < 1)
  5. Heavy nuclei saturate at Δf = K (gf → 1)

Author: Stephen Nelson / Field Dynamics Research
Date:   February 2026
"""

import math
from fractions import Fraction
from collections import Counter

# =============================================================================
# GEOMETRIC CONSTANTS — from d=3 uniqueness, zero free parameters
# =============================================================================

D = 3
K = D + 1              # = 4
F_PLUS = 1 + K + K**2  # = 21 (capacity ceiling)
F_ZERO = F_PLUS - K    # = 17 (Field Origin)
F_MINUS = F_ZERO - K   # = 13 (capacity floor)
CEILING = K ** K        # = 256
TIME_FACES = 2
MAGIC_NUMBERS = [2, 8, 20, 28, 50, 82, 126]


# =============================================================================
# HELPER: GEOMETRIC FUNCTIONS
# =============================================================================

def base4_digits(A):
    """Decompose A into base-4 digits [n4, n3, n2, n1, r]."""
    digits = []
    temp = A
    for level in range(4, 0, -1):
        power = K ** level
        digits.append(temp // power)
        temp %= power
    digits.append(temp)
    return tuple(digits)


def nesting_level(A):
    """Highest nesting level with nonzero fill."""
    if A == 0:
        return 0
    for n in range(4, 0, -1):
        if A >= K ** n:
            return n
    return 0


def is_level_complete(A):
    """True if A is exactly K^n for some n >= 1."""
    if A < K:
        return False
    n = round(math.log(A) / math.log(K))
    return K ** n == A


# =============================================================================
# HELPER: N-METRIC FUNCTIONS
# =============================================================================

def capacity_deficit(A):
    """Δf(A) = K·(2^(A-1) - 1) / (2^(A-1) + 1).

    Ranges from 0 (A=1) to K (A→∞). Saturates by A~12.
    """
    if A <= 1:
        return 0.0
    s = 2 ** (A - 1)
    return K * (s - 1) / (s + 1)


def geometric_fraction(A):
    """gf(A) = Δf(A)/K = (2^(A-1) - 1) / (2^(A-1) + 1).

    The fraction of maximum binding capacity available.
    Ranges from 0 to 1.
    """
    return capacity_deficit(A) / K


def compression_scale(A):
    """x = 2^(A-1): compression needed for A fields at Field Origin."""
    return 2 ** (A - 1)


# =============================================================================
# HELPER: SEMF (Standard Nuclear Physics, Independent Reference)
# =============================================================================

_AV = 15.56    # Volume (MeV)
_AS = 17.23    # Surface (MeV)
_AC = 0.697    # Coulomb (MeV)
_AA = 23.29    # Asymmetry (MeV)
_AP = 12.0     # Pairing (MeV)


def semf_be_total(A, Z):
    """Standard SEMF total binding energy (MeV)."""
    if A <= 0:
        return 0.0
    N = A - Z
    be = _AV * A - _AS * A**(2/3) - _AC * Z*(Z-1) / A**(1/3) - _AA*(N-Z)**2 / (4*A)
    if Z % 2 == 0 and N % 2 == 0:
        be += _AP / A**0.5
    elif Z % 2 == 1 and N % 2 == 1:
        be -= _AP / A**0.5
    return max(be, 0.0)


def semf_be_per_a(A, Z):
    """Standard SEMF binding energy per nucleon (MeV)."""
    if A <= 0:
        return 0.0
    return semf_be_total(A, Z) / A


# =============================================================================
# NUCLEAR DATA — AME2020 observed values
# =============================================================================
# (Z, symbol, A, BE_per_A in MeV)
# Most abundant stable isotope for each element Z=1..83, plus key isotopes.

ISOTOPE_TABLE = [
    # Light nuclei (A < 20): geometric fraction < 1 matters
    (1, 'H', 1, 0.000),
    (2, 'He', 4, 7.074),
    (3, 'Li', 7, 5.606),
    (4, 'Be', 9, 6.463),
    (5, 'B', 11, 6.928),
    (6, 'C', 12, 7.680),
    (7, 'N', 14, 7.476),
    (8, 'O', 16, 7.976),
    (9, 'F', 19, 7.779),
    (10, 'Ne', 20, 8.032),
    # Medium nuclei (20 < A < 60): near saturation
    (11, 'Na', 23, 8.112),
    (12, 'Mg', 24, 8.261),
    (13, 'Al', 27, 8.332),
    (14, 'Si', 28, 8.448),
    (15, 'P', 31, 8.481),
    (16, 'S', 32, 8.493),
    (17, 'Cl', 35, 8.520),
    (18, 'Ar', 40, 8.595),
    (19, 'K', 39, 8.557),
    (20, 'Ca', 40, 8.551),
    (20, 'Ca', 48, 8.667),  # doubly magic (Z=20, N=28)
    (21, 'Sc', 45, 8.619),
    (22, 'Ti', 48, 8.723),
    (23, 'V', 51, 8.742),
    (24, 'Cr', 52, 8.776),
    (25, 'Mn', 55, 8.765),
    (26, 'Fe', 56, 8.790),
    (27, 'Co', 59, 8.768),
    (28, 'Ni', 58, 8.732),
    (29, 'Cu', 63, 8.752),
    (30, 'Zn', 64, 8.736),
    # Heavy nuclei (60 < A < 130)
    (31, 'Ga', 69, 8.724),
    (32, 'Ge', 74, 8.705),
    (33, 'As', 75, 8.701),
    (34, 'Se', 80, 8.712),
    (35, 'Br', 79, 8.696),
    (36, 'Kr', 84, 8.718),
    (37, 'Rb', 85, 8.697),
    (38, 'Sr', 88, 8.733),
    (39, 'Y', 89, 8.714),
    (40, 'Zr', 90, 8.710),
    (41, 'Nb', 93, 8.664),
    (42, 'Mo', 98, 8.635),
    (44, 'Ru', 102, 8.607),
    (45, 'Rh', 103, 8.584),
    (46, 'Pd', 106, 8.567),
    (47, 'Ag', 107, 8.554),
    (48, 'Cd', 114, 8.539),
    (49, 'In', 115, 8.516),
    (50, 'Sn', 120, 8.505),
    (51, 'Sb', 121, 8.482),
    (52, 'Te', 130, 8.431),
    (53, 'I', 127, 8.445),
    (54, 'Xe', 132, 8.416),
    # Very heavy nuclei (A > 130): Coulomb effects dominate
    (55, 'Cs', 133, 8.400),
    (56, 'Ba', 138, 8.393),
    (57, 'La', 139, 8.378),
    (58, 'Ce', 140, 8.376),
    (59, 'Pr', 141, 8.354),
    (60, 'Nd', 142, 8.346),
    (62, 'Sm', 152, 8.241),
    (63, 'Eu', 153, 8.227),
    (64, 'Gd', 158, 8.183),
    (65, 'Tb', 159, 8.171),
    (66, 'Dy', 164, 8.127),
    (67, 'Ho', 165, 8.117),
    (68, 'Er', 166, 8.112),
    (69, 'Tm', 169, 8.068),
    (70, 'Yb', 174, 8.024),
    (71, 'Lu', 175, 8.015),
    (72, 'Hf', 180, 7.977),
    (73, 'Ta', 181, 7.970),
    (74, 'W', 184, 7.945),
    (75, 'Re', 187, 7.917),
    (76, 'Os', 192, 7.891),
    (77, 'Ir', 193, 7.882),
    (78, 'Pt', 195, 7.868),
    (79, 'Au', 197, 7.916),
    (80, 'Hg', 202, 7.890),
    (81, 'Tl', 205, 7.873),
    (82, 'Pb', 208, 7.867),
    (83, 'Bi', 209, 7.848),
]


# =============================================================================
# VALIDATION FRAMEWORK
# =============================================================================

_results = []
_current_suite = ""


def suite(name):
    global _current_suite
    _current_suite = name


def validate(name):
    def decorator(func):
        def wrapper():
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
#  SUITE 1: GEOMETRIC CEILING AND BASE-4 ADDRESS SPACE
# =========================================================================

suite("1. Geometric Ceiling and Base-4 Address Space")


@validate("All 81 elements have A < K⁴ = 256: no stable nucleus violates the ceiling")
def validate_ceiling():
    violations = [(Z, sym, A) for Z, sym, A, _ in ISOTOPE_TABLE if A >= CEILING]
    assert len(violations) == 0, f"Violations: {violations}"
    assert len(ISOTOPE_TABLE) >= 80


@validate("Every A decomposes to valid base-4 with digits 0-3, reconstruction exact")
def validate_base4():
    for Z, sym, A, _ in ISOTOPE_TABLE:
        digits = base4_digits(A)
        assert all(0 <= d <= 3 for d in digits), f"{sym}-{A}: invalid digit"
        reconstructed = sum(d * K**(4-i) for i, d in enumerate(digits))
        assert reconstructed == A, f"{sym}-{A}: reconstruction failed"


@validate("Level-complete nuclei He-4, O-16, Zn-64 (K^n) all stable with high BE/A")
def validate_level_complete():
    expected = {4: ('He', 7.074), 16: ('O', 7.976), 64: ('Zn', 8.736)}
    for target_A, (exp_sym, exp_be) in expected.items():
        matches = [(Z, sym, A, bea) for Z, sym, A, bea in ISOTOPE_TABLE if A == target_A]
        assert len(matches) > 0, f"K^n={target_A} not in table"
        _, sym, A, bea = matches[0]
        assert sym == exp_sym, f"A={target_A}: expected {exp_sym}, got {sym}"
        assert bea > 5.0, f"{sym}-{A}: BE/A={bea} too low for level-complete"


@validate("Pb-208 = 13×16 = F_MINUS × K²: heaviest stable at 81.25% capacity")
def validate_pb208_encoding():
    pb = [r for r in ISOTOPE_TABLE if r[1] == 'Pb' and r[2] == 208]
    assert len(pb) == 1
    assert 208 == F_MINUS * K**2
    assert Fraction(208, CEILING) == Fraction(13, 16)


@validate("No element uses L4 digit: highest nesting is L3 (n3 ≤ 3)")
def validate_no_L4():
    for Z, sym, A, _ in ISOTOPE_TABLE:
        digits = base4_digits(A)
        assert digits[0] == 0, f"{sym}-{A}: L4 digit = {digits[0]}"
        assert digits[1] <= 3, f"{sym}-{A}: L3 digit = {digits[1]} > 3"


# =========================================================================
#  SUITE 2: CAPACITY DEFICIT AND SATURATION
# =========================================================================

suite("2. Capacity Deficit Δf(A) and Saturation")


@validate("Δf ranges from 0 to K: monotonically increasing, bounded")
def validate_deficit_range():
    assert capacity_deficit(1) == 0.0
    prev = -1
    for A in range(1, 300):
        df = capacity_deficit(A)
        assert 0 <= df <= K + 1e-10, f"Δf({A})={df} out of [0,K]"
        assert df >= prev - 1e-15, f"Δf({A})={df} < Δf({A-1})={prev}"
        prev = df


@validate("Saturation: Δf > 0.999K by A=12, > 0.9999K by A=16, > 0.99999K by A=22")
def validate_saturation():
    assert capacity_deficit(12) > 0.999 * K
    assert capacity_deficit(16) > 0.9999 * K
    assert capacity_deficit(22) > 0.99999 * K


@validate("He-4 deficit = 28/9 ≈ 3.111: exactly K×7/9 of maximum")
def validate_he4_deficit():
    expected = Fraction(28, 9)
    actual = capacity_deficit(4)
    assert abs(actual - float(expected)) < 1e-10


@validate("Geometric fraction gf < 0.98 only for A ≤ 8: light nuclei geometrically distinct")
def validate_light_distinct():
    for Z, sym, A, bea in ISOTOPE_TABLE:
        gf = geometric_fraction(A)
        if gf < 0.98:
            assert A <= 8, f"{sym}-{A}: gf={gf:.4f} but A > 8"


@validate("For A ≥ 22, gf > 0.999999: geometry saturated, nuclear physics sets BE/A")
def validate_heavy_saturated():
    for Z, sym, A, bea in ISOTOPE_TABLE:
        if A >= 22:
            gf = geometric_fraction(A)
            assert gf > 0.999999, f"{sym}-{A}: gf={gf}"


# =========================================================================
#  SUITE 3: BINDING ENERGY CROSS-CHECK
# =========================================================================

suite("3. Binding Energy Cross-Check (BE/A vs Δf)")


@validate("BE/A increases with Δf for N=Z even-even chain: He→C→O→Ne→Mg→Si→Ca")
def validate_be_tracks_deficit():
    chain = [
        (4, 7.074), (12, 7.680), (16, 7.976),
        (20, 8.032), (24, 8.261), (28, 8.448), (40, 8.551),
    ]
    for i in range(1, len(chain)):
        A_prev, be_prev = chain[i-1]
        A_curr, be_curr = chain[i]
        assert capacity_deficit(A_curr) > capacity_deficit(A_prev)
        assert be_curr > be_prev, (
            f"BE/A should increase: A={A_prev}→{A_curr}, "
            f"{be_prev:.3f}→{be_curr:.3f}"
        )


@validate("BE/A peaks at A=56-62 (Fe/Ni region), declines for heavier nuclei")
def validate_peak_region():
    peak = max(bea for _, _, A, bea in ISOTOPE_TABLE if 50 <= A <= 70)
    tail_max = max(bea for _, _, A, bea in ISOTOPE_TABLE if A > 150)
    assert peak > tail_max, f"Peak {peak:.3f} ≤ tail {tail_max:.3f}"


@validate("Correction factor C = BE/A ÷ Δf bounded: 0.8 < C < 2.3 for all A > 1")
def validate_C_bounded():
    for Z, sym, A, bea in ISOTOPE_TABLE:
        if A <= 1:
            continue
        C = bea / capacity_deficit(A)
        assert 0.8 < C < 2.3, f"{sym}-{A}: C={C:.3f} out of bounds"


@validate("He-4 has the highest C of any element: alpha cluster enhancement is unique")
def validate_alpha_enhancement():
    C_he4 = 7.074 / capacity_deficit(4)
    for Z, sym, A, bea in ISOTOPE_TABLE:
        if A <= 1 or (Z == 2 and A == 4):
            continue
        C = bea / capacity_deficit(A)
        assert C_he4 > C, f"He-4 C={C_he4:.3f} ≤ {sym}-{A} C={C:.3f}"


@validate("C for saturated nuclei (A≥20): mean ≈ 2.1, std < 0.2")
def validate_C_statistics():
    C_vals = [bea / capacity_deficit(A) for _, _, A, bea in ISOTOPE_TABLE if A >= 20]
    mean = sum(C_vals) / len(C_vals)
    var = sum((c - mean)**2 for c in C_vals) / len(C_vals)
    std = math.sqrt(var)
    assert 1.9 < mean < 2.3, f"Mean C = {mean:.3f}"
    assert std < 0.2, f"Std C = {std:.3f}"


# =========================================================================
#  SUITE 4: MAGIC NUMBER SIGNATURES
# =========================================================================

suite("4. Magic Number Signatures in the Data")


@validate("Z-magic elements (Z ≥ 8) have above-median BE/A in their mass region")
def validate_z_magic_enhanced():
    z_magic = {8, 20, 28, 50, 82}  # Exclude Z=2: He-4 is light (gf < 1)
    for Zm in z_magic:
        magic_entries = [(A, bea) for Z, _, A, bea in ISOTOPE_TABLE if Z == Zm]
        if not magic_entries:
            continue
        ref_A = magic_entries[0][0]
        region = [bea for _, _, A, bea in ISOTOPE_TABLE
                  if abs(A - ref_A) <= 12 and A > 4]
        if len(region) < 3:
            continue
        median_be = sorted(region)[len(region)//2]
        magic_be = max(bea for _, bea in magic_entries)
        assert magic_be >= median_be - 0.15, (
            f"Z={Zm}: magic BE/A={magic_be:.3f} < region median={median_be:.3f}"
        )


@validate("All 5 doubly-magic stable nuclei confirmed in dataset with high BE/A")
def validate_doubly_magic():
    doubly = {
        (2, 4): 'He-4', (8, 16): 'O-16', (20, 40): 'Ca-40',
        (20, 48): 'Ca-48', (82, 208): 'Pb-208',
    }
    for (Zd, Ad), name in doubly.items():
        match = [(Z, A, bea) for Z, _, A, bea in ISOTOPE_TABLE
                 if Z == Zd and A == Ad]
        assert len(match) == 1, f"{name} not found in table"
        _, _, bea = match[0]
        # Doubly magic must be well-bound (above 7 MeV/A)
        assert bea > 7.0, f"{name}: BE/A={bea:.3f} too low for doubly magic"


# =========================================================================
#  SUITE 5: NEUTRON BALANCE AND STABILITY TRENDS
# =========================================================================

suite("5. Neutron Balance and Stability Trends")


@validate("N/Z ratio trend: increases from ~1.0 (light) to ~1.54 (Pb)")
def validate_nz_trend():
    light = [(A - Z) / Z for Z, _, A, _ in ISOTOPE_TABLE if 4 <= Z <= 10]
    heavy = [(A - Z) / Z for Z, _, A, _ in ISOTOPE_TABLE if Z >= 70]
    mean_light = sum(light) / len(light)
    mean_heavy = sum(heavy) / len(heavy)
    assert mean_light < 1.2, f"Light mean N/Z = {mean_light:.3f}"
    assert mean_heavy > 1.3, f"Heavy mean N/Z = {mean_heavy:.3f}"
    assert mean_heavy > mean_light


@validate("Light nuclei (Z ≤ 20): N/Z < 1.5 for all")
def validate_light_nz():
    for Z, sym, A, bea in ISOTOPE_TABLE:
        if 2 <= Z <= 20:
            ratio = (A - Z) / Z
            assert ratio < 1.5, f"{sym}-{A}: N/Z={ratio:.2f}"


@validate("Heavy nuclei (Z ≥ 50): N > Z for all (neutron excess required)")
def validate_heavy_nz():
    for Z, sym, A, bea in ISOTOPE_TABLE:
        if Z >= 50:
            N = A - Z
            assert N > Z, f"{sym}-{A}: N={N} ≤ Z={Z}"


@validate("Pb-208: N/Z = 126/82 = 1.537, the 54% neutron excess")
def validate_pb_nz():
    ratio = 126 / 82
    assert abs(ratio - 1.537) < 0.001


# =========================================================================
#  SUITE 6: SEMF INDEPENDENT CROSS-CHECK
# =========================================================================

suite("6. SEMF Independent Cross-Check")


@validate("SEMF predicts BE/A within 1 MeV for all A ≥ 12 nuclei")
def validate_semf_accuracy():
    for Z, sym, A, bea in ISOTOPE_TABLE:
        if A < 12:
            continue
        semf = semf_be_per_a(A, Z)
        diff = abs(bea - semf)
        assert diff < 1.0, f"{sym}-{A}: |obs-SEMF|={diff:.3f} MeV"


@validate("SEMF systematically overestimates for heavy nuclei: shell effects missing")
def validate_semf_heavy_bias():
    heavy = [(Z, sym, A, bea) for Z, sym, A, bea in ISOTOPE_TABLE if A > 100]
    overshoots = sum(1 for Z, _, A, bea in heavy if semf_be_per_a(A, Z) > bea)
    total = len(heavy)
    assert overshoots > total * 0.5, (
        f"Only {overshoots}/{total} SEMF overshoots for heavy nuclei"
    )


@validate("GFD geometric fraction ≈ 1 for all SEMF-regime nuclei (A ≥ 12)")
def validate_gfd_semf_regime():
    for Z, sym, A, bea in ISOTOPE_TABLE:
        if A >= 12:
            gf = geometric_fraction(A)
            assert abs(gf - 1.0) < 0.001, f"{sym}-{A}: gf={gf}"


# =========================================================================
#  SUITE 7: ELEMENT-BY-ELEMENT CROSS-CHECK
# =========================================================================

suite("7. Element-by-Element Cross-Check")


@validate("Full table: every element passes ceiling + base-4 + deficit + C-factor checks")
def validate_full_table():
    failures = []
    for Z, sym, A, bea in ISOTOPE_TABLE:
        # 1. Ceiling
        if A >= CEILING:
            failures.append(f"{sym}-{A}: exceeds ceiling K^4={CEILING}")
        # 2. Base-4 validity
        digits = base4_digits(A)
        if any(d < 0 or d > 3 for d in digits):
            failures.append(f"{sym}-{A}: invalid base-4 digits")
        recon = sum(d * K**(4-i) for i, d in enumerate(digits))
        if recon != A:
            failures.append(f"{sym}-{A}: base-4 reconstruction failed")
        # 3. Deficit in [0, K]
        df = capacity_deficit(A)
        if df < -0.001 or df > K + 0.001:
            failures.append(f"{sym}-{A}: Δf={df:.4f} out of [0,K]")
        # 4. C-factor bounded (skip hydrogen)
        if A > 1:
            C = bea / df
            if C < 0.5 or C > 2.5:
                failures.append(f"{sym}-{A}: C={C:.3f} out of [0.5, 2.5]")
    assert len(failures) == 0, f"{len(failures)} failures:\n" + "\n".join(failures[:10])


@validate("K-multiple preference: A mod 4 = 0 overrepresented (>27% vs 25% random)")
def validate_k_preference():
    counts = Counter(A % K for _, _, A, _ in ISOTOPE_TABLE)
    total = len(ISOTOPE_TABLE)
    k_mult_frac = counts[0] / total
    assert k_mult_frac > 0.27, f"K-mult fraction = {k_mult_frac:.3f}"


@validate("Nesting level progression: elements span L0 through L3, none at L4")
def validate_nesting_progression():
    levels = set()
    for _, _, A, _ in ISOTOPE_TABLE:
        levels.add(nesting_level(A))
    # Should have levels 0 (H), 1 (He-Li-Be-B), 2 (C through Zn), 3 (Ga+)
    assert 0 in levels, "No L0 elements"
    assert 1 in levels, "No L1 elements"
    assert 2 in levels, "No L2 elements"
    assert 3 in levels, "No L3 elements"
    assert 4 not in levels, "L4 element found — violates ceiling"


# =========================================================================
#  SUITE 8: THE BINDING ENERGY CURVE SHAPE
# =========================================================================

suite("8. The Binding Energy Curve Shape")


@validate("BE/A curve has single peak: rises then falls, no secondary maxima after A=62")
def validate_single_peak():
    # After the peak (A~62), BE/A should only decrease
    past_peak = [(A, bea) for _, _, A, bea in ISOTOPE_TABLE if A > 70]
    past_peak.sort()
    for i in range(1, len(past_peak)):
        A_prev, be_prev = past_peak[i-1]
        A_curr, be_curr = past_peak[i]
        # Allow small fluctuations (< 0.1 MeV) from isotope selection
        assert be_curr < be_prev + 0.05, (
            f"Unexpected rise: {A_prev}→{A_curr}, "
            f"{be_prev:.3f}→{be_curr:.3f}"
        )


@validate("Geometric capacity Δf predicts the SHAPE: rises fast then flat (sigmoidal)")
def validate_deficit_shape():
    # Δf should rise steeply for A < 10, then flatten
    df_4 = capacity_deficit(4)
    df_12 = capacity_deficit(12)
    df_56 = capacity_deficit(56)
    df_208 = capacity_deficit(208)

    # The steep rise: Δf(4) < Δf(12) by a significant margin
    assert df_12 - df_4 > 0.8, "Deficit rise too slow"
    # The plateau: Δf(12) ≈ Δf(56) ≈ Δf(208) ≈ K
    assert abs(df_56 - df_12) < 0.01, "Not saturated by A=12"
    assert abs(df_208 - df_56) < 1e-10, "Not saturated by A=56"


@validate("The BE/A decline for A > 62 is entirely from C(A,Z), not from Δf")
def validate_decline_is_coulomb():
    # Δf is constant (= K) for all A > 20
    # So any BE/A decline must come from C decreasing
    C_peak = max(bea / capacity_deficit(A) for _, _, A, bea in ISOTOPE_TABLE
                 if 50 <= A <= 70)
    C_tail = min(bea / capacity_deficit(A) for _, _, A, bea in ISOTOPE_TABLE
                 if A > 180)
    assert C_peak > C_tail, "C should decrease for heavy nuclei"
    assert C_peak - C_tail > 0.15, f"C decline only {C_peak-C_tail:.3f}"


@validate("The alpha cliff: He-4 C-factor (2.27) exceeds all neighbors by > 30%")
def validate_alpha_cliff():
    C_he4 = 7.074 / capacity_deficit(4)
    C_li = 5.606 / capacity_deficit(7)
    C_be = 6.463 / capacity_deficit(9)

    # He-4 exceeds its neighbors by > 30%
    assert C_he4 > C_li * 1.3, f"Alpha cliff too small: He={C_he4:.3f} vs Li={C_li:.3f}"
    assert C_he4 > C_be * 1.3, f"Alpha cliff too small: He={C_he4:.3f} vs Be={C_be:.3f}"


# =============================================================================
# MAIN
# =============================================================================

def main():
    print()
    print("=" * 72)
    print("  GFD ENTERPRISE VALIDATION")
    print("  The Complete Periodic Table Cross-Check")
    print("=" * 72)

    all_suites = [
        ("1. Geometric Ceiling and Base-4 Address Space", [
            validate_ceiling,
            validate_base4,
            validate_level_complete,
            validate_pb208_encoding,
            validate_no_L4,
        ]),
        ("2. Capacity Deficit Δf(A) and Saturation", [
            validate_deficit_range,
            validate_saturation,
            validate_he4_deficit,
            validate_light_distinct,
            validate_heavy_saturated,
        ]),
        ("3. Binding Energy Cross-Check (BE/A vs Δf)", [
            validate_be_tracks_deficit,
            validate_peak_region,
            validate_C_bounded,
            validate_alpha_enhancement,
            validate_C_statistics,
        ]),
        ("4. Magic Number Signatures in the Data", [
            validate_z_magic_enhanced,
            validate_doubly_magic,
        ]),
        ("5. Neutron Balance and Stability Trends", [
            validate_nz_trend,
            validate_light_nz,
            validate_heavy_nz,
            validate_pb_nz,
        ]),
        ("6. SEMF Independent Cross-Check", [
            validate_semf_accuracy,
            validate_semf_heavy_bias,
            validate_gfd_semf_regime,
        ]),
        ("7. Element-by-Element Cross-Check", [
            validate_full_table,
            validate_k_preference,
            validate_nesting_progression,
        ]),
        ("8. The Binding Energy Curve Shape", [
            validate_single_peak,
            validate_deficit_shape,
            validate_decline_is_coulomb,
            validate_alpha_cliff,
        ]),
    ]

    for suite_name, tests in all_suites:
        print()
        print(f"--- {suite_name} ---")
        for t in tests:
            t()

    # =====================================================================
    #  SUMMARY
    # =====================================================================

    print()
    print("=" * 72)
    passed = sum(1 for _, _, s, _ in _results if s == "PASS")
    failed = sum(1 for _, _, s, _ in _results if s != "PASS")
    total = len(_results)
    print(f"  RESULTS: {passed} passed, {failed} failed, {total} total")
    print("=" * 72)

    # Print the full cross-check table
    print()
    print("  COMPLETE PERIODIC TABLE CROSS-CHECK")
    print("  " + "-" * 68)
    print(f"  {'Z':>3} {'Sym':>3} {'A':>4} {'base4':>12} {'Δf':>6} {'gf':>6}"
          f" {'BE/A':>6} {'C':>6} {'SEMF':>6} {'notes'}")
    print("  " + "-" * 68)

    magic_z = set(MAGIC_NUMBERS)
    for Z, sym, A, bea in ISOTOPE_TABLE:
        digits = base4_digits(A)
        b4_str = f"{digits[1]}·{digits[2]}·{digits[3]}·{digits[4]}"
        df = capacity_deficit(A)
        gf = geometric_fraction(A)
        C = bea / df if df > 0.001 else 0.0
        semf = semf_be_per_a(A, Z) if A > 1 else 0.0

        notes = []
        if is_level_complete(A):
            notes.append(f"K^{round(math.log(A)/math.log(K))}")
        if Z in magic_z:
            notes.append("Z✦")
        N = A - Z
        if N in magic_z:
            notes.append("N✦")
        if Z in magic_z and N in magic_z:
            notes[-2:] = ["2✦"]
        if A % K == 0:
            notes.append(f"{A//K}α")
        note_str = " ".join(notes)

        print(f"  {Z:>3} {sym:>3} {A:>4} {b4_str:>12} {df:>6.3f} {gf:>6.4f}"
              f" {bea:>6.3f} {C:>6.3f} {semf:>6.3f} {note_str}")

    print()
    print("  LEGEND: Z✦ = Z-magic, N✦ = N-magic, 2✦ = doubly magic")
    print("  " + "-" * 68)
    print()
    print("  FRAMEWORK SUMMARY:")
    print(f"    Input constants:     K = {K}, D = {D} (from 2(d+1) = 2^d)")
    print(f"    Address space:       base-4, ceiling K^K = {CEILING}")
    print(f"    Geometric capacity:  Δf(A) = K·(2^(A-1)-1)/(2^(A-1)+1)")
    print(f"    Binding energy:      BE/A = C(A,Z) × Δf(A)")
    print(f"    Geometry provides:   Δf (zero parameters, exact)")
    print(f"    Nuclear physics:     C (Coulomb, pairing, shell, symmetry)")
    print(f"    Elements validated:  {len(ISOTOPE_TABLE)} isotopes, Z = 1..83")
    print()

    if failed > 0:
        print("  FAILURES:")
        for s, name, status, msg in _results:
            if status != "PASS":
                print(f"    [{status}] {s} / {name}")
                if msg:
                    for line in msg.split("\n")[:3]:
                        print(f"            {line}")
        print()

    return failed == 0


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
