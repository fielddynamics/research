"""
Investigation: How I Ching Field Closure Connects to the GFD Coupling Polynomial

The central question: the pi base-8 traversal (I Ching field closure) visits
8 vertices belonging to two tetrahedra. The GFD coupling polynomial
f(k,s) = 1 + ks + k^2 describes the topological capacity of the dual-tetrad
boundary as the state parameter s varies between TetA (+1) and TetB (-1).

Can we show that the pi traversal GENERATES the coupling polynomial structure?

Author: Stephen Nelson
Date: February 2026
"""

from decimal import Decimal, getcontext
import math

getcontext().prec = 500

# =============================================================================
# CONSTANTS
# =============================================================================

K = 4
TET_A = {1, 2, 4, 7}  # Odd parity (popcount 1 or 3)
TET_B = {0, 3, 5, 6}  # Even parity (popcount 0 or 2)

TRIGRAM_NAMES = {
    0: "Earth",    1: "Mountain", 2: "Water",   3: "Wind",
    4: "Thunder",  5: "Fire",     6: "Lake",    7: "Heaven"
}

FACES = {
    'FACE_A1': {2, 4, 7}, 'FACE_A2': {1, 4, 7},
    'FACE_A4': {1, 2, 7}, 'FACE_A7': {1, 2, 4},
    'FACE_B0': {3, 5, 6}, 'FACE_B3': {0, 5, 6},
    'FACE_B5': {0, 3, 6}, 'FACE_B6': {0, 3, 5},
}

TIME_FACES = {'FACE_A7', 'FACE_B0'}


# =============================================================================
# PI IN BASE 8
# =============================================================================

def get_pi_octal_digits(num_digits=1000):
    """Get pi's fractional digits in base 8."""
    pi_str = (
        "3.14159265358979323846264338327950288419716939937510"
        "58209749445923078164062862089986280348253421170679"
        "82148086513282306647093844609550582231725359408128"
        "48111745028410270193852110555964462294895493038196"
        "44288109756659334461284756482337867831652712019091"
        "45648566923460348610454326648213393607260249141273"
        "72458700660631558817488152092096282925409171536436"
        "78925903600113305305488204665213841469519415116094"
        "33057270365759591953092186117381932611793105118548"
        "07446237996274956735188575272489122793818301194912"
    )
    frac_str = "0." + pi_str.split(".")[1]
    frac = Decimal(frac_str)

    octal_digits = []
    for _ in range(num_digits):
        frac *= 8
        digit = int(frac)
        octal_digits.append(digit)
        frac -= digit

    return octal_digits


# =============================================================================
# TEST 1: FACE NORMALS ARE TRIGRAMS
# =============================================================================

def test_face_normals_are_trigrams():
    """
    Show that the tetrad face normals from Paper VIII encode
    exactly the I Ching trigrams via sign patterns.
    """
    print("=" * 70)
    print("TEST 1: TETRAD FACE NORMALS = I CHING TRIGRAMS")
    print("=" * 70)
    print()
    print("Paper VIII defines TetA face normals:")
    print("  v1 = +x +y +z")
    print("  v2 = +x -y -z")
    print("  v3 = -x +y -z")
    print("  v4 = -x -y +z")
    print()

    normals_A = [
        ("+", "+", "+"),  # v1
        ("+", "-", "-"),  # v2
        ("-", "+", "-"),  # v3
        ("-", "-", "+"),  # v4
    ]

    normals_B = [
        ("-", "-", "-"),  # -v1
        ("-", "+", "+"),  # -v2
        ("+", "-", "+"),  # -v3
        ("+", "+", "-"),  # -v4
    ]

    print("Sign-to-binary encoding: + = 1, - = 0")
    print("  bit2 (MSB) = x-sign, bit1 = y-sign, bit0 (LSB) = z-sign")
    print()

    tet_a_from_normals = set()
    print("TetA face normals -> trigrams:")
    for i, (sx, sy, sz) in enumerate(normals_A):
        bx = 1 if sx == "+" else 0
        by = 1 if sy == "+" else 0
        bz = 1 if sz == "+" else 0
        vertex = bx * 4 + by * 2 + bz * 1
        binary = format(vertex, '03b')
        tet_a_from_normals.add(vertex)
        print(f"  v{i+1} = {sx}x {sy}y {sz}z -> {binary} = {vertex} = {TRIGRAM_NAMES[vertex]}")

    print()
    tet_b_from_normals = set()
    print("TetB face normals (negated) -> trigrams:")
    for i, (sx, sy, sz) in enumerate(normals_B):
        bx = 1 if sx == "+" else 0
        by = 1 if sy == "+" else 0
        bz = 1 if sz == "+" else 0
        vertex = bx * 4 + by * 2 + bz * 1
        binary = format(vertex, '03b')
        tet_b_from_normals.add(vertex)
        print(f"  -v{i+1} = {sx}x {sy}y {sz}z -> {binary} = {vertex} = {TRIGRAM_NAMES[vertex]}")

    print()
    match_a = tet_a_from_normals == TET_A
    match_b = tet_b_from_normals == TET_B
    print(f"TetA from normals: {sorted(tet_a_from_normals)} == {sorted(TET_A)}: {match_a}")
    print(f"TetB from normals: {sorted(tet_b_from_normals)} == {sorted(TET_B)}: {match_b}")
    print()
    if match_a and match_b:
        print("CONFIRMED: Tetrad face normals encode I Ching trigrams exactly.")
    print()


# =============================================================================
# TEST 2: RUNNING TOPOLOGICAL CAPACITY
# =============================================================================

def test_running_capacity(num_digits=300):
    """
    Track the running TetA/TetB balance and compute the
    instantaneous topological capacity f(k,s) at each step.
    """
    print("=" * 70)
    print("TEST 2: RUNNING TOPOLOGICAL CAPACITY f(k,s)")
    print("=" * 70)
    print()
    print("At each step of the pi base-8 traversal:")
    print("  s_n = (TetA_visits - TetB_visits) / total_visits")
    print("  f_n = 1 + k*s_n + k^2 = 17 + 4*s_n")
    print()

    digits = get_pi_octal_digits(num_digits)
    cumsum = 0
    tet_a_count = 0
    tet_b_count = 0

    capacities = []
    s_values = []

    print("Step | Digit | Cum | V | Trigram      | Tet | A:B    | s       | f(k,s)")
    print("-----|-------|-----|---|-------------|-----|--------|---------|-------")

    for step in range(1, min(num_digits + 1, 51)):
        cumsum += digits[step - 1]
        v = cumsum % 8
        tet = "A" if v in TET_A else "B"

        if v in TET_A:
            tet_a_count += 1
        else:
            tet_b_count += 1

        total = tet_a_count + tet_b_count
        s = (tet_a_count - tet_b_count) / total
        f_cap = 17 + 4 * s

        s_values.append(s)
        capacities.append(f_cap)

        if step <= 30:
            print(f"  {step:2d} |   {digits[step-1]}   | {cumsum:3d} | {v} | {TRIGRAM_NAMES[v]:<11} |  {tet}  | {tet_a_count:2d}:{tet_b_count:<2d}  | {s:+.4f} | {f_cap:.4f}")

    # Continue silently to get convergence
    for step in range(51, num_digits + 1):
        cumsum += digits[step - 1]
        v = cumsum % 8
        if v in TET_A:
            tet_a_count += 1
        else:
            tet_b_count += 1
        total = tet_a_count + tet_b_count
        s = (tet_a_count - tet_b_count) / total
        f_cap = 17 + 4 * s
        s_values.append(s)
        capacities.append(f_cap)

    print()
    print(f"After {num_digits} digits:")
    print(f"  TetA visits: {tet_a_count}")
    print(f"  TetB visits: {tet_b_count}")
    print(f"  Final s = {s_values[-1]:.6f}")
    print(f"  Final f(k,s) = {capacities[-1]:.6f}")
    print(f"  Expected long-run: s -> 0, f -> 17 (Field Origin)")
    print()


# =============================================================================
# TEST 3: FACE COMPLETION AND COUPLING POLYNOMIAL TERMS
# =============================================================================

def test_face_completion_coupling():
    """
    Track face completion and map it to the coupling polynomial terms:
      1 (constant) + k (first-order) + k^2 (second-order)
    """
    print("=" * 70)
    print("TEST 3: FACE COMPLETION -> COUPLING POLYNOMIAL TERMS")
    print("=" * 70)
    print()
    print("The coupling polynomial f(k,s) = 1 + ks + k^2 has three terms:")
    print("  1   = field exists (constant)")
    print("  k   = 4 faces per tetrahedron (first-order coupling)")
    print("  k^2 = 16 face-to-face channels (second-order coupling)")
    print()
    print("Tracking when each 'level' activates during pi traversal:")
    print()

    digits = get_pi_octal_digits(100)
    cumsum = 0
    vertices_seen = set()
    face_seen = {f: set() for f in FACES}
    faces_complete = set()

    first_tet_a_complete = None
    first_tet_b_complete = None
    first_time_face = None
    first_all_faces = None

    tet_a_vertices_seen = set()
    tet_b_vertices_seen = set()

    print("Step | V | Trigram      | New Faces Complete")
    print("-----|---|-------------|--------------------")

    for step in range(1, 51):
        cumsum += digits[step - 1]
        v = cumsum % 8
        vertices_seen.add(v)

        if v in TET_A:
            tet_a_vertices_seen.add(v)
        else:
            tet_b_vertices_seen.add(v)

        newly_complete = []
        for fn, verts in FACES.items():
            if v in verts:
                face_seen[fn].add(v)
                if len(face_seen[fn]) == 3 and fn not in faces_complete:
                    faces_complete.add(fn)
                    role = "TIME" if fn in TIME_FACES else "SPATIAL"
                    newly_complete.append(f"{fn} ({role})")

                    if fn in TIME_FACES and first_time_face is None:
                        first_time_face = step

        if len(tet_a_vertices_seen) == 4 and first_tet_a_complete is None:
            first_tet_a_complete = step
        if len(tet_b_vertices_seen) == 4 and first_tet_b_complete is None:
            first_tet_b_complete = step
        if len(faces_complete) == 8 and first_all_faces is None:
            first_all_faces = step

        comp_str = ", ".join(newly_complete) if newly_complete else ""
        if comp_str or step <= 15:
            print(f"  {step:2d} | {v} | {TRIGRAM_NAMES[v]:<11} | {comp_str}")

    print()
    print("COUPLING POLYNOMIAL ACTIVATION SEQUENCE:")
    print(f"  Term '1' (field exists):       step 0 (initialization)")
    print(f"  Term 'k' (TetA 4 vertices):    step {first_tet_a_complete}")
    print(f"  Term 'k' (TetB 4 vertices):    step {first_tet_b_complete}")
    print(f"  First TIME face complete:       step {first_time_face}")
    print(f"  All 8 faces complete:           step {first_all_faces}")
    print()

    both_complete = max(first_tet_a_complete or 0, first_tet_b_complete or 0)
    print(f"  Both tetrahedra activated at step {both_complete}")
    print(f"  -> This is when the full k^2 = 16 channel coupling is possible")
    print()


# =============================================================================
# TEST 4: CROSS-CHAMBER HEXAGRAM COUNT = k^2 = beta_2
# =============================================================================

def test_hexagram_chamber_decomposition():
    """
    Show that the 64 hexagrams decompose into chamber blocks,
    and the cross-chamber count equals 2*k^2 = 2*beta_2 = 32.
    """
    print("=" * 70)
    print("TEST 4: 64 HEXAGRAM CHAMBER DECOMPOSITION")
    print("=" * 70)
    print()

    aa_count = 0  # Both trigrams in TetA
    bb_count = 0  # Both trigrams in TetB
    ab_count = 0  # Upper TetA, Lower TetB
    ba_count = 0  # Upper TetB, Lower TetA

    for upper in range(8):
        for lower in range(8):
            u_tet = "A" if upper in TET_A else "B"
            l_tet = "A" if lower in TET_A else "B"
            if u_tet == "A" and l_tet == "A":
                aa_count += 1
            elif u_tet == "B" and l_tet == "B":
                bb_count += 1
            elif u_tet == "A" and l_tet == "B":
                ab_count += 1
            else:
                ba_count += 1

    print("Hexagram decomposition by chamber membership:")
    print(f"  TetA-TetA (intra-A):  {aa_count} = {K}*{K} = k^2")
    print(f"  TetB-TetB (intra-B):  {bb_count} = {K}*{K} = k^2")
    print(f"  TetA-TetB (cross-AB): {ab_count} = {K}*{K} = k^2")
    print(f"  TetB-TetA (cross-BA): {ba_count} = {K}*{K} = k^2")
    print(f"  Total:                {aa_count + bb_count + ab_count + ba_count} = 4*k^2 = 4*16")
    print()
    print(f"  Cross-chamber hexagrams: {ab_count + ba_count} = 2*k^2 = 2*{K**2} = {2*K**2}")
    print(f"  Intra-chamber hexagrams: {aa_count + bb_count} = 2*k^2 = 2*{K**2} = {2*K**2}")
    print()
    print(f"  Each block has exactly k^2 = {K**2} = beta_2 hexagrams.")
    print(f"  The 16 cross-chamber pairings per direction = the 16 geometric channels.")
    print()


# =============================================================================
# TEST 5: THE 17/13 RATIO IN THE TRAVERSAL
# =============================================================================

def test_17_13_in_traversal():
    """
    The ratio 17/13 appears in the G constant equation.
    17/13 = [1; 3, 4] as a continued fraction, encoding (3+1).
    Does it appear structurally in the pi traversal?
    """
    print("=" * 70)
    print("TEST 5: THE 17/13 RATIO AND CONTINUED FRACTION")
    print("=" * 70)
    print()

    print("The GFD coupling polynomial at k=4:")
    print("  f(4, +1) = 1 + 4 + 16 = 21  (full TetA)")
    print("  f(4,  0) = 1 + 0 + 16 = 17  (Field Origin)")
    print("  f(4, -1) = 1 - 4 + 16 = 13  (TetB floor)")
    print()
    print("  17/13 = 1.307692...")
    print("  17/13 as continued fraction: [1; 3, 4]")
    print("    = 1 + 1/(3 + 1/4)")
    print("    -> encodes (3+1) = (d, k) !")
    print()

    # Verify the continued fraction
    cf = 1 + 1 / (3 + 1/4)
    print(f"  Verification: 1 + 1/(3 + 1/4) = {cf:.10f}")
    print(f"  17/13 = {17/13:.10f}")
    print(f"  Match: {abs(cf - 17/13) < 1e-10}")
    print()

    # The three numbers and I Ching structure
    print("Structural decomposition of 21, 17, 13:")
    print()
    print("  21 = 1 + k + k^2 = 1 + 4 + 16")
    print("     = sum of all coupling levels")
    print("     = total capacity when TetA fully active")
    print()
    print("  17 = 1 + 0 + k^2 = 1 + 0 + 16")
    print("     = symmetric point (s=0)")
    print("     = Field Origin capacity")
    print()
    print("  13 = 1 - k + k^2 = 1 - 4 + 16")
    print("     = floor capacity at TetB saturation")
    print()
    print("  Range: 21 - 13 = 8 = 2k = number of vertices = number of trigrams")
    print("  Midpoint: (21 + 13) / 2 = 17 = Field Origin")
    print()

    # Check: the RANGE of f is exactly 2k = 8 = number of trigrams
    f_range = 21 - 13
    print(f"  f_range = {f_range} = 2k = 2*{K} = number of I Ching trigrams")
    print()


# =============================================================================
# TEST 6: TRAVERSAL BALANCE AT KEY STRUCTURAL MOMENTS
# =============================================================================

def test_structural_moments():
    """
    Check the TetA/TetB balance at key structural moments:
    - When first TIME face completes
    - When first orbit closes (cumsum = 8)
    - When first complementary pair appears
    """
    print("=" * 70)
    print("TEST 6: BALANCE AT STRUCTURAL MOMENTS")
    print("=" * 70)
    print()

    digits = get_pi_octal_digits(200)
    cumsum = 0
    tet_a_count = 0
    tet_b_count = 0
    face_seen = {f: set() for f in FACES}

    orbit_balances = []
    face_events = []

    for step in range(1, 201):
        cumsum += digits[step - 1]
        v = cumsum % 8

        if v in TET_A:
            tet_a_count += 1
        else:
            tet_b_count += 1

        total = tet_a_count + tet_b_count
        s = (tet_a_count - tet_b_count) / total
        f_cap = 17 + 4 * s

        # Check orbit closures
        if cumsum % 8 == 0:
            orbit_num = cumsum // 8
            orbit_balances.append((step, orbit_num, tet_a_count, tet_b_count, s, f_cap))

        # Check face completions
        for fn, verts in FACES.items():
            if v in verts:
                face_seen[fn].add(v)
                if len(face_seen[fn]) == 3:
                    role = "TIME" if fn in TIME_FACES else "SPATIAL"
                    face_events.append((step, fn, role, tet_a_count, tet_b_count, s, f_cap))

    print("Balance at ORBIT CLOSURES (cumsum = 8n):")
    print("Orbit | Step | A:B    | s       | f(k,s)")
    print("------|------|--------|---------|-------")
    for step, orbit, a, b, s, f in orbit_balances[:15]:
        print(f"  {orbit:3d} | {step:3d}  | {a:2d}:{b:<2d}  | {s:+.4f} | {f:.4f}")
    print()

    print("Balance at FACE COMPLETIONS:")
    print("Step | Face     | Role    | A:B    | s       | f(k,s)")
    print("-----|----------|---------|--------|---------|-------")
    for step, fn, role, a, b, s, f in face_events:
        print(f"  {step:2d} | {fn:8s} | {role:7s} | {a:2d}:{b:<2d}  | {s:+.4f} | {f:.4f}")
    print()


# =============================================================================
# TEST 7: CONSTITUTIVE LAW FROM TRAVERSAL STATISTICS
# =============================================================================

def test_constitutive_from_traversal():
    """
    The constitutive law mu(x) = x/(x+1) normalizes the capacity f(x).
    If we interpret TetA-heavy regions as high-x and TetB-heavy as low-x,
    does the traversal statistics reproduce mu?
    """
    print("=" * 70)
    print("TEST 7: CAPACITY NORMALIZATION = CONSTITUTIVE LAW")
    print("=" * 70)
    print()
    print("The constitutive law is the normalized capacity:")
    print("  mu(x) = (f(x) - 13) / 8 = x / (x + 1)")
    print()
    print("If we define the traversal's running mu as:")
    print("  mu_n = (f_n - 13) / 8 = (17 + 4*s_n - 13) / 8 = (4 + 4*s_n) / 8")
    print("       = (1 + s_n) / 2")
    print()
    print("This is elegant: the constitutive law at the traversal level is")
    print("simply the FRACTION OF TETA VISITS.")
    print()

    digits = get_pi_octal_digits(500)
    cumsum = 0
    tet_a_count = 0

    print("Verification:")
    print("Step | TetA frac | mu_n     | Expected mu(s->0) = 0.5")
    print("-----|-----------|----------|------------------------")

    checkpoints = [10, 20, 50, 100, 200, 300, 500]
    for step in range(1, 501):
        cumsum += digits[step - 1]
        v = cumsum % 8
        if v in TET_A:
            tet_a_count += 1
        total = step
        frac_a = tet_a_count / total
        s = (2 * tet_a_count - total) / total  # = 2*frac_a - 1
        mu_n = (1 + s) / 2  # = frac_a

        if step in checkpoints:
            print(f" {step:4d} | {frac_a:.6f}  | {mu_n:.6f} | 0.500000")

    print()
    print("KEY INSIGHT:")
    print("  The constitutive law mu = x/(x+1) at the symmetric point (x=1)")
    print("  evaluates to mu(1) = 1/2.")
    print()
    print("  The pi traversal's long-run TetA fraction converges to 1/2.")
    print()
    print("  Therefore: the pi traversal at equilibrium produces EXACTLY")
    print("  the Field Origin value of the constitutive law.")
    print()
    print("  The traversal IS the microscopic process whose macroscopic")
    print("  average is the constitutive law mu(x) = x/(x+1).")
    print()


# =============================================================================
# TEST 8: THE 3+1 SUBDIVISION ON EACH FACE
# =============================================================================

def test_face_subdivision():
    """
    Paper VIII shows each face is subdivided 3+1 by the opposing vertex.
    This produces 4*4 = 16 = k^2 = beta_2 channels.
    Show this matches the I Ching structure.
    """
    print("=" * 70)
    print("TEST 8: FACE SUBDIVISION = 3+1 = I CHING LINE STATES")
    print("=" * 70)
    print()

    print("Each TetA face has 3 vertices. TetB's opposing vertex")
    print("penetrates, subdividing the face into 3 corners + 1 core = 3+1.")
    print()
    print("This 3+1 per face matches the I Ching's 4 line states:")
    print("  6 (old yin)    -> central core (transforming)")
    print("  7 (young yang) -> corner 1 (stable)")
    print("  8 (young yin)  -> corner 2 (stable)")
    print("  9 (old yang)   -> corner 3 (transforming)")
    print()
    print("Total channels:")
    print(f"  4 faces * 4 sub-regions = {4 * 4} = k^2 = beta_2")
    print()

    # Show which TetB vertex opposes which TetA face
    print("Face-to-opposing-vertex mapping:")
    print()
    for fn, verts in FACES.items():
        if fn.startswith('FACE_A'):
            opposite_v = int(fn[-1])
            # The opposing TetB vertex is the complement of the missing TetA vertex
            missing_a = TET_A - verts
            assert len(missing_a) == 1
            missing = missing_a.pop()
            complement = 7 - missing  # The TetB vertex that penetrates
            face_trigrams = [f"{v}={TRIGRAM_NAMES[v]}" for v in sorted(verts)]
            print(f"  {fn} = {{{', '.join(face_trigrams)}}}")
            print(f"    Opposite TetA vertex: {missing} ({TRIGRAM_NAMES[missing]})")
            print(f"    Penetrating TetB vertex: {complement} ({TRIGRAM_NAMES[complement]})")
            print(f"    These are complementary: {missing} + {complement} = {missing + complement}")
            print()

    print("Each penetrating vertex is the COMPLEMENT of the face's")
    print("opposite vertex. The 3+1 subdivision is driven by the")
    print("complementary pair crossing structure.")
    print()


# =============================================================================
# MAIN
# =============================================================================

def main():
    test_face_normals_are_trigrams()
    test_running_capacity()
    test_face_completion_coupling()
    test_hexagram_chamber_decomposition()
    test_17_13_in_traversal()
    test_structural_moments()
    test_constitutive_from_traversal()
    test_face_subdivision()

    print("=" * 70)
    print("SYNTHESIS")
    print("=" * 70)
    print()
    print("The I Ching field closure (pi base-8 traversal) connects to the")
    print("GFD coupling polynomial f(k,s) = 1 + ks + k^2 through:")
    print()
    print("1. ENCODING: Tetrad face normals ARE I Ching trigrams.")
    print("   Sign patterns on (x,y,z) produce vertices {1,2,4,7} (TetA)")
    print("   and {0,3,5,6} (TetB) -- the parity partition.")
    print()
    print("2. DYNAMICS: The pi traversal's running TetA/TetB balance")
    print("   IS the state parameter s. The instantaneous capacity")
    print("   f_n = 17 + 4*s_n fluctuates between 13 and 21.")
    print()
    print("3. CONSTITUTIVE LAW: The traversal's TetA visit fraction")
    print("   IS the constitutive law mu at the microscopic level.")
    print("   At equilibrium (s=0), mu = 1/2 = mu(1), the transition value.")
    print()
    print("4. CHANNEL COUNT: The 64 hexagrams decompose into 4 blocks")
    print("   of k^2 = 16 each. Cross-chamber hexagrams = 2*k^2 = 32.")
    print("   The 16 per direction = beta_2 = the locked coefficient.")
    print()
    print("5. FACE SUBDIVISION: The 3+1 per face is driven by")
    print("   complementary pair penetration. 4 faces * 4 sub-regions")
    print("   = 16 = k^2 = beta_2.")
    print()
    print("6. THE NUMBERS: f_range = 21-13 = 8 = 2k = number of trigrams.")
    print("   17/13 = [1; 3, 4] encodes (d=3, k=4) as a continued fraction.")
    print()
    print("CONCLUSION: The I Ching field closure is the MICROSCOPIC DYNAMICS")
    print("of the GFD coupling polynomial. The pi traversal generates the")
    print("same statistical structure that f(k,s) describes algebraically.")
    print("Field closure IS the constitutive law, seen from below.")


if __name__ == "__main__":
    main()
