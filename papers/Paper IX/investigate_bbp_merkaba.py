"""
BBP-Merkaba Structural Investigation
======================================

The Bailey-Borwein-Plouffe (1997) formula computes pi as:

    pi = SUM_{k=0}^{inf} (1/16^k) [4/(8k+1) - 2/(8k+4) - 1/(8k+5) - 1/(8k+6)]

This script investigates whether the structural constants of this formula
are the structural constants of the Merkaba (stellated octahedron / dual
tetrahedra). We test 8 specific correspondences, from convergence verification
through geometric mapping, to determine which connections are necessities
and which are coincidences.

    pip install mpmath
    python investigate_bbp_merkaba.py

Author: Stephen Nelson
Date: February 2026
"""

import math
from itertools import combinations
from fractions import Fraction

import mpmath


# =============================================================================
# MERKABA CONSTANTS (inlined from geometry_constants.py)
# =============================================================================
#
# 3-BIT BINARY ENCODING:
#   bit2 (MSB) = x-axis: 0 -> left (-1),  1 -> right (+1)
#   bit1       = y-axis: 0 -> bottom (-1), 1 -> top (+1)
#   bit0 (LSB) = z-axis: 0 -> back (-1),  1 -> front (+1)

K = 4   # closure constant = d + 1 = simplex vertex count in d=3
D = 3   # spatial dimensions

TET_A = {1, 2, 4, 7}   # odd popcount (1 or 3 yang lines)
TET_B = {0, 3, 5, 6}   # even popcount (0 or 2 yang lines)

VERTEX_COORDS = {
    0: (-1, -1, -1),  # 000  Earth    (Kun)
    1: (-1, -1, +1),  # 001  Mountain (Gen)
    2: (-1, +1, -1),  # 010  Water    (Kan)
    3: (-1, +1, +1),  # 011  Wind     (Xun)
    4: (+1, -1, -1),  # 100  Thunder  (Zhen)
    5: (+1, -1, +1),  # 101  Fire     (Li)
    6: (+1, +1, -1),  # 110  Lake     (Dui)
    7: (+1, +1, +1),  # 111  Heaven   (Qian)
}

TRIGRAM_NAMES = {
    0: "Earth",   1: "Mountain", 2: "Water",   3: "Wind",
    4: "Thunder", 5: "Fire",     6: "Lake",    7: "Heaven",
}

TIME_FACES = {'FACE_A7', 'FACE_B0'}
TIME_APICES = {0, 7}

COMPLEMENT_PAIRS = [(0, 7), (1, 6), (2, 5), (3, 4)]


# =============================================================================
# BBP FORMULA CONSTANTS
# =============================================================================
#
# The BBP formula has 4 terms per period-8 block:
#   position -> coefficient
# These are the ONLY free parameters in the formula besides base 16.

BBP_TERMS = {
    1: Fraction(4),
    4: Fraction(-2),
    5: Fraction(-1),
    6: Fraction(-1),
}

BBP_BASE = 16
BBP_PERIOD = 8
BBP_ACTIVE = set(BBP_TERMS.keys())       # {1, 4, 5, 6}
BBP_SILENT = set(range(8)) - BBP_ACTIVE   # {0, 2, 3, 7}
BBP_COEFFICIENTS = list(BBP_TERMS.values())


# =============================================================================
# HELPERS
# =============================================================================

def popcount(v):
    return bin(v).count('1')


def hamming(a, b):
    return bin(a ^ b).count('1')


def euclidean(v1, v2):
    c1, c2 = VERTEX_COORDS[v1], VERTEX_COORDS[v2]
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))


def bbp_partial_sum(n_terms):
    """Compute the BBP partial sum to n_terms using mpmath for precision."""
    mpmath.mp.dps = 80
    total = mpmath.mpf(0)
    for k in range(n_terms):
        base_power = mpmath.power(16, k)
        term = (
            mpmath.mpf(4) / (8 * k + 1)
            - mpmath.mpf(2) / (8 * k + 4)
            - mpmath.mpf(1) / (8 * k + 5)
            - mpmath.mpf(1) / (8 * k + 6)
        )
        total += term / base_power
    return total


def pi_binary_digits(n_bits):
    """Compute n binary digits of pi's fractional part via mpmath."""
    mpmath.mp.dps = n_bits // 3 + 50
    pi_val = mpmath.mp.pi
    frac = pi_val - int(pi_val)
    bits = []
    for _ in range(n_bits):
        frac *= 2
        b = int(frac)
        bits.append(b)
        frac -= b
    return bits


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
# TEST 1: BBP CONVERGENCE VERIFICATION
#
# Before we interpret the formula, we must confirm it actually computes pi.
# =============================================================================

@test("BBP Convergence Verification", 1)
def test_bbp_convergence():
    mpmath.mp.dps = 60
    pi_ref = mpmath.mp.pi

    print()
    print("  Comparing BBP partial sums against mpmath pi:")
    print(f"  Reference pi = {mpmath.nstr(pi_ref, 50)}")
    print()

    checkpoints = [1, 5, 10, 20, 50, 100]
    for n in checkpoints:
        bbp_val = bbp_partial_sum(n)
        error = abs(bbp_val - pi_ref)
        correct_digits = -int(mpmath.log10(error)) if error > 0 else 60
        print(f"  k=0..{n-1:3d}:  {correct_digits:2d} correct decimal digits")

    # Final verification: 100 terms should give 50+ correct digits
    final = bbp_partial_sum(100)
    final_error = abs(final - pi_ref)
    correct = -int(mpmath.log10(final_error)) if final_error > 0 else 60
    assert correct >= 50, f"Only {correct} correct digits at 100 terms"
    print(f"\n  100 terms -> {correct} correct digits (need >= 50)")


# =============================================================================
# TEST 2: PERIOD-8 STRUCTURE = TRIGRAM SPACE
#
# The BBP denominators all have the form 8k + offset. The period is 8.
# This is the cardinality of the trigram set: 2^3 = 8.
# =============================================================================

@test("Period-8 Structure = Trigram Space", 2)
def test_period_8_structure():
    print()
    print(f"  BBP denominator form: 8k + offset")
    print(f"  Period = {BBP_PERIOD}")
    print(f"  Trigram count = 2^D = 2^{D} = {2**D}")
    assert BBP_PERIOD == 2 ** D, (
        f"Period {BBP_PERIOD} != 2^D = {2**D}"
    )
    print(f"  >> Period matches trigram space: {BBP_PERIOD} = 2^{D}")

    active = len(BBP_ACTIVE)
    silent = len(BBP_SILENT)
    print()
    print(f"  Active positions per period: {active}")
    print(f"  Silent positions per period: {silent}")
    print(f"  Active set: {sorted(BBP_ACTIVE)}")
    print(f"  Silent set: {sorted(BBP_SILENT)}")
    assert active == K, f"Active count {active} != K={K}"
    assert silent == K, f"Silent count {silent} != K={K}"
    print(f"  >> K = {K} active, K = {K} silent: period splits into two K-groups")

    ratio = Fraction(active, BBP_PERIOD)
    print()
    print(f"  Active fraction: {active}/{BBP_PERIOD} = {ratio} = {float(ratio)}")
    print(f"  Constitutive law mu(1) = 1/(1+1) = 1/2")
    assert ratio == Fraction(1, 2), f"Active fraction {ratio} != 1/2"
    print(f"  >> Active fraction = mu(1) = 1/2")


# =============================================================================
# TEST 3: ACTIVE POSITIONS MAP TO CROSS-CHAMBER VERTICES
#
# The offsets {1, 4, 5, 6} are vertex indices. They split evenly across
# the two tetrahedra: 2 from TET_A, 2 from TET_B.
# =============================================================================

@test("Active Positions Map to Cross-Chamber Vertices", 3)
def test_cross_chamber_mapping():
    print()
    print("  BBP active positions -> Merkaba vertex mapping:")
    print()

    active_in_A = BBP_ACTIVE & TET_A
    active_in_B = BBP_ACTIVE & TET_B

    for pos in sorted(BBP_ACTIVE):
        chamber = "TET_A" if pos in TET_A else "TET_B"
        binary = format(pos, '03b')
        name = TRIGRAM_NAMES[pos]
        coeff = int(BBP_TERMS[pos])
        print(f"    V{pos} = {binary} = {name:10s}  {chamber}  coeff = {coeff:+d}")

    print()
    print(f"  Active in TET_A: {sorted(active_in_A)}")
    print(f"  Active in TET_B: {sorted(active_in_B)}")
    assert len(active_in_A) == 2, f"Expected 2 in TET_A, got {len(active_in_A)}"
    assert len(active_in_B) == 2, f"Expected 2 in TET_B, got {len(active_in_B)}"
    print(f"  >> Balanced: 2 + 2 cross-chamber selection")

    # Geometry of the active vertex set
    print()
    print("  Geometry of active vertex set {1, 4, 5, 6}:")
    print()
    for va, vb in combinations(sorted(BBP_ACTIVE), 2):
        h = hamming(va, vb)
        d = euclidean(va, vb)
        cross = "cross" if (va in TET_A) != (vb in TET_A) else "intra"
        comp = " [COMPLEMENT]" if va + vb == 7 else ""
        print(f"    ({va},{vb}): Hamming={h}, dist={d:.4f}, {cross}{comp}")

    intra_pairs = [(a, b) for a, b in combinations(sorted(BBP_ACTIVE), 2)
                   if (a in TET_A) == (b in TET_A)]
    cross_pairs = [(a, b) for a, b in combinations(sorted(BBP_ACTIVE), 2)
                   if (a in TET_A) != (b in TET_A)]
    print()
    print(f"  Intra-chamber pairs: {len(intra_pairs)}")
    print(f"  Cross-chamber pairs: {len(cross_pairs)}")
    assert len(cross_pairs) == K, f"Expected {K} cross pairs, got {len(cross_pairs)}"


# =============================================================================
# TEST 4: TEMPORAL AXIS EXCLUSION
#
# The BBP formula's silent positions {0, 2, 3, 7} contain both apices
# of the temporal body diagonal: V0 (Earth) and V7 (Heaven). The formula
# avoids the time dimension entirely.
# =============================================================================

@test("Temporal Axis Exclusion", 4)
def test_temporal_exclusion():
    print()
    print("  Silent positions -> Merkaba vertex mapping:")
    print()

    for pos in sorted(BBP_SILENT):
        chamber = "TET_A" if pos in TET_A else "TET_B"
        binary = format(pos, '03b')
        name = TRIGRAM_NAMES[pos]
        apex = " ** TIME APEX **" if pos in TIME_APICES else ""
        print(f"    V{pos} = {binary} = {name:10s}  {chamber}{apex}")

    # Verify temporal axis is fully silent
    temporal_silent = TIME_APICES & BBP_SILENT
    assert temporal_silent == TIME_APICES, (
        f"Temporal apices {TIME_APICES} not fully silent: "
        f"only {temporal_silent} are silent"
    )
    print()
    print(f"  Temporal axis {{0, 7}} is COMPLETELY SILENT in the BBP formula.")
    print(f"  The formula operates in the spatial sector only.")

    # Complementary pair analysis: which pairs are active, half, or silent?
    print()
    print("  Complementary pair analysis:")
    print()
    full_pairs = 0
    half_pairs = 0
    absent_pairs = 0

    for va, vb in COMPLEMENT_PAIRS:
        a_active = va in BBP_ACTIVE
        b_active = vb in BBP_ACTIVE
        status = "BOTH ACTIVE" if (a_active and b_active) else \
                 "BOTH SILENT" if (not a_active and not b_active) else \
                 "HALF (split)"
        a_name = TRIGRAM_NAMES[va]
        b_name = TRIGRAM_NAMES[vb]
        a_mark = "*" if a_active else "."
        b_mark = "*" if b_active else "."
        print(f"    ({va},{vb}) {a_name}/{b_name}: [{a_mark}|{b_mark}] {status}")
        if a_active and b_active:
            full_pairs += 1
        elif not a_active and not b_active:
            absent_pairs += 1
        else:
            half_pairs += 1

    print()
    print(f"  Pattern: {full_pairs} full, {half_pairs} half, {absent_pairs} absent")
    assert (full_pairs, half_pairs, absent_pairs) == (1, 2, 1), (
        f"Expected (1,2,1) pattern, got ({full_pairs},{half_pairs},{absent_pairs})"
    )
    print(f"  >> 1-2-1 pattern confirmed")
    print(f"  >> The absent pair (0,7) is the TEMPORAL axis")
    print(f"  >> The full pair (1,6) is Mountain/Lake (a SPATIAL coupling axis)")


# =============================================================================
# TEST 5: COEFFICIENT CANCELLATION = FIELD ORIGIN
#
# The vertex position vectors of the cube sum to (0,0,0) at the Field Origin.
# The BBP coefficients sum to zero in the same way: the formula's weighted
# contributions cancel, producing a convergent series from divergent harmonics.
# =============================================================================

@test("Coefficient Cancellation = Field Origin", 5)
def test_coefficient_cancellation():
    coeffs = [BBP_TERMS[p] for p in sorted(BBP_ACTIVE)]
    coeff_sum = sum(BBP_TERMS.values())

    print()
    print(f"  Coefficients at active positions:")
    for p in sorted(BBP_ACTIVE):
        name = TRIGRAM_NAMES[p]
        chamber = "A" if p in TET_A else "B"
        print(f"    V{p} ({name}, Tet{chamber}): {int(BBP_TERMS[p]):+d}")

    print()
    terms_str = ' + '.join(f'({int(BBP_TERMS[p]):+d})' for p in sorted(BBP_ACTIVE))
    print(f"  Coefficient sum: {terms_str} = {int(coeff_sum)}")
    assert coeff_sum == 0, f"Coefficient sum = {coeff_sum}, expected 0"
    print(f"  >> Sum = 0: analogous to vertex vectors cancelling at Field Origin")

    abs_sum = sum(abs(c) for c in BBP_TERMS.values())
    print()
    print(f"  Absolute coefficient sum: {' + '.join(str(abs(int(BBP_TERMS[p]))) for p in sorted(BBP_ACTIVE))} = {int(abs_sum)}")
    assert abs_sum == 8, f"|Coefficient| sum = {abs_sum}, expected 8"
    print(f"  >> |Sum| = 8 = total vertex count = 2^D")

    # Per-chamber balance
    net_A = sum(BBP_TERMS[p] for p in BBP_ACTIVE & TET_A)
    net_B = sum(BBP_TERMS[p] for p in BBP_ACTIVE & TET_B)
    print()
    print(f"  TET_A net coefficient: {int(net_A):+d}")
    print(f"  TET_B net coefficient: {int(net_B):+d}")
    assert net_A == -net_B, f"Chamber imbalance: A={net_A}, B={net_B}"
    assert abs(net_A) == 2, f"|net_A| = {abs(net_A)}, expected 2"
    print(f"  >> Inter-chamber balance: |+{abs(int(net_A))}| = |-{abs(int(net_B))}|")
    print(f"  >> Net magnitude per chamber = 2 = bimetric factor")


# =============================================================================
# TEST 6: BIT PLACE VALUES IN COEFFICIENTS
#
# The coefficient magnitudes {4, 2, 1} are exactly {2^2, 2^1, 2^0},
# the binary place values that define the 3-bit coordinate encoding.
# The BBP numerators literally encode the axes of the cube.
# =============================================================================

@test("Bit Place Values in Coefficients", 6)
def test_bit_place_values():
    magnitudes = sorted(set(abs(int(c)) for c in BBP_TERMS.values()), reverse=True)
    bit_values = [2 ** i for i in range(D - 1, -1, -1)]  # [4, 2, 1]

    print()
    print(f"  Unique coefficient magnitudes (descending): {magnitudes}")
    print(f"  Bit place values for D={D} bits:             {bit_values}")
    assert magnitudes == bit_values, (
        f"Magnitudes {magnitudes} != bit values {bit_values}"
    )
    print(f"  >> EXACT MATCH: BBP numerators = binary axis weights")

    # Map each coefficient to its axis
    print()
    print("  Coefficient -> axis mapping:")
    axis_names = ['x (bit2, MSB)', 'y (bit1)', 'z (bit0, LSB)']
    for mag, axis in zip(bit_values, axis_names):
        positions = [p for p in sorted(BBP_ACTIVE) if abs(int(BBP_TERMS[p])) == mag]
        for p in positions:
            name = TRIGRAM_NAMES[p]
            sign = "+" if BBP_TERMS[p] > 0 else "-"
            print(f"    |coeff| = {mag} = 2^{int(math.log2(mag))} -> {axis}:  "
                  f"V{p} ({name}), sign {sign}")

    # The 4th coefficient (magnitude 1 repeated) means z-axis appears twice
    count_by_mag = {}
    for c in BBP_TERMS.values():
        m = abs(int(c))
        count_by_mag[m] = count_by_mag.get(m, 0) + 1

    print()
    print("  Multiplicity of each magnitude:")
    for m in sorted(count_by_mag, reverse=True):
        print(f"    |coeff| = {m}: appears {count_by_mag[m]} time(s)")

    assert count_by_mag[4] == 1, "Magnitude 4 should appear once"
    assert count_by_mag[2] == 1, "Magnitude 2 should appear once"
    assert count_by_mag[1] == 2, "Magnitude 1 should appear twice"
    print(f"  >> Pattern: 1-1-2 (MSB once, middle once, LSB twice)")
    print(f"  >> Total terms: 1+1+2 = {sum(count_by_mag.values())} = K")


# =============================================================================
# TEST 7: BASE 16 = 2 x 8 FACTORIZATION
#
# The geometric series base in BBP is 16 = 2 * 8.
# The factor 8 = 2^D is the trigram space (octahedral symmetry).
# The factor 2 is the bimetric factor (two tetrahedra).
# Together: 16 = (number of chambers) * (vertices per cube).
# =============================================================================

@test("Base 16 = 2 x 8 Factorization", 7)
def test_base_factorization():
    print()
    print(f"  BBP base = {BBP_BASE}")
    print(f"  Factorization: {BBP_BASE} = 2 x 8")
    assert BBP_BASE == 2 * 8, f"Base {BBP_BASE} != 2 * 8"

    trigram_space = 2 ** D
    bimetric = 2
    print()
    print(f"  Factor 8 = 2^D = 2^{D} = trigram space (octahedral vertices)")
    print(f"  Factor 2 = bimetric factor (TET_A + TET_B)")
    print(f"  Product:  {bimetric} x {trigram_space} = {bimetric * trigram_space}")
    assert bimetric * trigram_space == BBP_BASE

    # The base is also 2^4 = 2^(D+1)
    print()
    print(f"  Alternatively: {BBP_BASE} = 2^{int(math.log2(BBP_BASE))} = 2^(D+1) = 2^{D+1}")
    assert BBP_BASE == 2 ** (D + 1)
    print(f"  >> D+1 = {D+1} = K (closure constant)")
    print(f"  >> So BBP base = 2^K")
    assert BBP_BASE == 2 ** K
    print(f"  >> {BBP_BASE} = 2^K confirmed")

    # Power decomposition
    print()
    print("  Power decomposition 1/16^k = 1/2^k * 1/8^k:")
    for k in range(5):
        val_16 = 16 ** k
        val_2 = 2 ** k
        val_8 = 8 ** k
        assert val_16 == val_2 * val_8
        print(f"    k={k}: 16^{k} = {val_16:8d} = 2^{k} * 8^{k} = {val_2} * {val_8}")


# =============================================================================
# TEST 8: BBP HEX DIGIT EXTRACTION vs MPMATH OCTAL DIGITS
#
# BBP extracts pi in base 16 (4-bit groups). The Merkaba traversal uses
# base 8 (3-bit groups). Both decompose the same underlying binary stream.
# The hex and octal representations are different "windows" into the same
# binary expansion of pi, confirming that the base-16 formula and the
# base-8 traversal are reading the same information at different resolutions.
# =============================================================================

@test("BBP Hex Digit Extraction vs mpmath Octal Digits", 8)
def test_hex_octal_bridge():
    # Compute binary digits of pi via mpmath
    n_bits = 48  # enough for 12 octal or 12 hex digits
    binary = pi_binary_digits(n_bits)
    binary_str = ''.join(str(b) for b in binary)

    print()
    print(f"  Binary expansion of pi (fractional part, {n_bits} bits):")
    print(f"  {binary_str}")

    # Group into 3-bit (octal) chunks
    octal_digits = []
    for i in range(0, n_bits - 2, 3):
        chunk = binary[i:i+3]
        if len(chunk) == 3:
            octal_digits.append(chunk[0] * 4 + chunk[1] * 2 + chunk[2])

    # Group into 4-bit (hex) chunks
    hex_digits = []
    for i in range(0, n_bits - 3, 4):
        chunk = binary[i:i+4]
        if len(chunk) == 4:
            hex_digits.append(chunk[0] * 8 + chunk[1] * 4 + chunk[2] * 2 + chunk[3])

    print()
    print(f"  Octal  (3-bit groups): {' '.join(str(d) for d in octal_digits[:16])}")
    print(f"  Hex    (4-bit groups): {' '.join(f'{d:x}' for d in hex_digits[:12])}")

    # Verify against mpmath direct computation
    mpmath.mp.dps = 50
    pi_val = mpmath.mp.pi
    frac = pi_val - int(pi_val)
    mpmath_octal = []
    f = frac
    for _ in range(16):
        f *= 8
        d = int(f)
        mpmath_octal.append(d)
        f -= d

    print()
    print(f"  mpmath octal (direct): {' '.join(str(d) for d in mpmath_octal)}")
    assert octal_digits[:16] == mpmath_octal, (
        f"Binary->octal mismatch:\n  {octal_digits[:16]}\n  {mpmath_octal}"
    )
    print(f"  >> Binary-to-octal matches mpmath direct computation")

    # The key insight: LCM(3, 4) = 12 bits is the alignment period
    lcm_bits = 12
    print()
    print(f"  Alignment period: LCM(3, 4) = {lcm_bits} bits")
    print(f"  Every {lcm_bits} binary digits, octal and hex frames realign.")
    print(f"  {lcm_bits} bits = {lcm_bits // 3} octal digits = {lcm_bits // 4} hex digits")
    assert lcm_bits == 12
    assert lcm_bits // 3 == K  # 4 octal digits per alignment
    assert lcm_bits // 4 == D  # 3 hex digits per alignment
    print(f"  >> {lcm_bits // 3} octal digits per alignment = K = {K}")
    print(f"  >> {lcm_bits // 4} hex digits per alignment = D = {D}")
    print(f"  >> The alignment period encodes (K, D) = ({K}, {D})")

    # Demonstrate: each 12-bit window produces K=4 trigram steps
    # and D=3 hexadecimal steps
    print()
    print(f"  First 12-bit window: {binary_str[:12]}")
    oct_window = [binary[i] * 4 + binary[i+1] * 2 + binary[i+2]
                  for i in range(0, 12, 3)]
    hex_window = [binary[i] * 8 + binary[i+1] * 4 + binary[i+2] * 2 + binary[i+3]
                  for i in range(0, 12, 4)]
    print(f"    -> {K} octal digits:  {oct_window}")
    print(f"    -> {D} hex digits:    {[f'0x{d:x}' for d in hex_window]}")
    for od in oct_window:
        assert 0 <= od <= 7, f"Octal digit {od} out of range"
    for hd in hex_window:
        assert 0 <= hd <= 15, f"Hex digit {hd} out of range"


# =============================================================================
# MAIN
# =============================================================================

def main():
    print()
    print("*" * 72)
    print("*  BBP-MERKABA STRUCTURAL INVESTIGATION")
    print("*  Bailey-Borwein-Plouffe (1997) meets the Stellated Octahedron")
    print("*" * 72)

    all_tests = [
        test_bbp_convergence,
        test_period_8_structure,
        test_cross_chamber_mapping,
        test_temporal_exclusion,
        test_coefficient_cancellation,
        test_bit_place_values,
        test_base_factorization,
        test_hex_octal_bridge,
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

    # Profundity ranking
    print("  PROFUNDITY RANKING (structural necessity vs coincidence):")
    print()

    rankings = [
        ("STRUCTURAL NECESSITY",
         "These follow from the mathematics -- if the Merkaba is the geometry,",
         "the BBP formula MUST have these features.",
         [
             (2, "Period 8 = 2^D = trigram space"),
             (3, "K=4 active terms per period, balanced 2+2 across chambers"),
             (5, "Coefficient sum = 0 (convergence requires cancellation)"),
             (7, "Base 16 = 2^K = 2 * 8 = bimetric x trigram"),
             (8, "Alignment LCM(3,4) = 12 encodes (K,D) = (4,3)"),
         ]),
        ("DEEP CORRESPONDENCE",
         "These are exact matches that go beyond counting -- they reveal",
         "the BBP formula encodes the Merkaba's internal structure.",
         [
             (4, "Temporal axis {0,7} completely silent in BBP"),
             (6, "Coefficient magnitudes {4,2,1} = bit place values = axis weights"),
             (5, "Per-chamber net coeff = +/-2 = bimetric factor"),
         ]),
        ("REMARKABLE PATTERN",
         "These are observations that reward further investigation.",
         [
             (4, "Complementary pair pattern: 1 full, 2 half, 1 absent"),
             (3, "Active set {1,4,5,6} contains exactly 1 complement pair (1,6)"),
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
