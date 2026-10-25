#!/usr/bin/env python3
"""
Nuclear Magic Numbers Pipeline
================================
Step-by-step derivation of the seven nuclear magic numbers from
the Sierpinski walk packing algebra.

Each function maps directly to a step in magic_numbers_pipeline.md.
Run this script to reproduce every number in the pipeline document.

Inputs:
  - K = 4, D = 3
  - T(n) = n(n+1)(n+2)/6
  - G(n) = (n-1)n/2 for n >= K, else 0
  - M(n) = 2[T(n) - G(n)]

Outputs:
  - Magic numbers: 2, 8, 20, 28, 50, 82, 126
  - Shell capacities: 2, 6, 12, 8, 22, 32, 44
  - Gate exclusion activates at n = K = 4

No field equation is used. This is pure combinatorics on K and D.

Stephen Nelson — Gravity Field Dynamics
"""

# =====================================================================
# INPUTS
# =====================================================================

K = 4       # branching factor (faces per level)
D = 3       # depth (levels of subdivision)
KD = K**D   # 64 positions per face

print("=" * 70)
print("INPUTS")
print("=" * 70)
print(f"  K = {K} (branching factor)")
print(f"  D = {D} (depth)")
print(f"  K^D = {KD} (positions per face)")
print(f"  Total hierarchy capacity = K * K^D = {K * KD} (4 faces)")
print(f"")
print(f"  Closure condition: 2(D+1) = 2^D")
print(f"    LHS = 2({D}+1) = {2*(D+1)}")
print(f"    RHS = 2^{D} = {2**D}")
print(f"    Match: {2*(D+1) == 2**D}")


# =====================================================================
# STEP 1: WALK HIERARCHY
# =====================================================================

print(f"\n{'=' * 70}")
print("STEP 1: Walk hierarchy")
print("=" * 70)
print(f"  Three-level hierarchy:")
print(f"    Level 1 (faces):        K = {K}")
print(f"    Level 2 (channels):     K = {K} per face")
print(f"    Level 3 (sub-channels): K = {K} per channel")
print(f"    Total: {K} x {K} x {K} = {KD} positions")
print(f"")
print(f"  Addressing: each position has a 3-digit base-{K} address")
print(f"  Example addresses:")
for f in range(K):
    print(f"    Face {f}: ({f},0,0) to ({f},{K-1},{K-1})"
          f"  = {K*K} positions"
          f"  {'<-- gate face' if f == K-1 else ''}")


# =====================================================================
# STEP 2: GATE FACE
# =====================================================================

print(f"\n{'=' * 70}")
print("STEP 2: Gate face")
print("=" * 70)
print(f"  At each level, face index {K-1} (the {K}-th face) is the gate face.")
print(f"  The gate face is the boundary where the structure folds back.")
print(f"  Positions on the gate face are excluded from the shell count.")
print(f"")
print(f"  Gate activation threshold: n = K = {K}")
print(f"  For n < {K}, the packing has not reached the gate boundary.")
print(f"  For n >= {K}, the gate boundary has (n-1)*n/2 positions to exclude.")


# =====================================================================
# STEP 3: CONCENTRIC SHELL LAYERS
# =====================================================================

def T(n):
    """Tetrahedral number: cumulative position count for K-fold branching.

    T(n) = n(n+1)(n+2)/6

    Counts the number of objects in a tetrahedron of side n.
    This is the natural packing geometry for K = 4 branching.
    """
    return n * (n + 1) * (n + 2) // 6


print(f"\n{'=' * 70}")
print("STEP 3: Concentric shell layers (tetrahedral numbers)")
print("=" * 70)
print(f"  T(n) = n(n+1)(n+2)/6")
print(f"")
print(f"  {'n':>3}  {'T(n)':>6}  {'Layer size':>11}  {'Layer = n(n+1)/2':>18}")

prev_T = 0
for n in range(1, 8):
    t = T(n)
    layer = t - prev_T
    triangular = n * (n + 1) // 2
    print(f"  {n:>3}  {t:>6}  {layer:>11}  {triangular:>18}"
          f"  {'<-- 28 = stellated octahedron elements' if n == 7 else ''}")
    prev_T = t


# =====================================================================
# STEP 4: GATE EXCLUSION
# =====================================================================

def G(n):
    """Gate exclusion: positions on the gate face boundary.

    G(n) = (n-1)*n/2 for n >= K, else 0.

    The gate face is the K-th face. It first contributes at shell n = K.
    The excluded count is the triangular number for side (n-1): the
    number of positions on the triangular gate boundary at that shell.
    """
    if n < K:
        return 0
    return (n - 1) * n // 2


print(f"\n{'=' * 70}")
print("STEP 4: Gate exclusion")
print("=" * 70)
print(f"  G(n) = (n-1)*n/2 for n >= K = {K}, else 0")
print(f"")
print(f"  {'n':>3}  {'G(n)':>6}  {'Status':>20}  {'Calculation':>20}")

for n in range(1, 8):
    g = G(n)
    if n < K:
        status = "gate inactive"
        calc = f"n < K = {K}"
    elif n == K:
        status = "gate ACTIVATES"
        calc = f"({n-1}*{n})/2 = {g}"
    else:
        status = "gate active"
        calc = f"({n-1}*{n})/2 = {g}"
    print(f"  {n:>3}  {g:>6}  {status:>20}  {calc:>20}")

print(f"")
print(f"  Note: G(7) = {G(7)} = 1 + K + K^2 = 1 + {K} + {K**2}"
      f" = {1 + K + K**2} (coupling polynomial at s=+1)")


# =====================================================================
# STEP 5: SHELL CLOSURES AND MAGIC NUMBERS
# =====================================================================

def M(n):
    """Cumulative shell closure.

    M(n) = 2[T(n) - G(n)]

    Factor of 2 accounts for proton and neutron orientations
    (isospin degeneracy, or equivalently, the two tetrahedra
    of the dual structure).
    """
    return 2 * (T(n) - G(n))


OBSERVED_MAGIC = [2, 8, 20, 28, 50, 82, 126]

print(f"\n{'=' * 70}")
print("STEP 5: Shell closures and magic numbers")
print("=" * 70)
print(f"  M(n) = 2[T(n) - G(n)]")
print(f"")
print(f"  {'n':>3}  {'T(n)':>6}  {'G(n)':>6}  {'T-G':>6}  {'M(n)':>6}"
      f"  {'Cap':>5}  {'Observed':>10}  {'Match':>6}")

prev_M = 0
all_match = True
for n in range(1, 8):
    t = T(n)
    g = G(n)
    m = M(n)
    cap = m - prev_M
    obs = OBSERVED_MAGIC[n - 1]
    match = m == obs
    if not match:
        all_match = False
    print(f"  {n:>3}  {t:>6}  {g:>6}  {t-g:>6}  {m:>6}"
          f"  {cap:>5}  {obs:>10}  {'  ✓' if match else '  ✗':>6}")
    prev_M = m

print(f"")
print(f"  All seven magic numbers reproduced: {all_match}")
predicted = [M(n) for n in range(1, 8)]
print(f"  Predicted: {predicted}")
print(f"  Observed:  {OBSERVED_MAGIC}")


# =====================================================================
# STEP 6: THE 20 → 28 ANOMALY
# =====================================================================

print(f"\n{'=' * 70}")
print("STEP 6: The 20 → 28 anomaly")
print("=" * 70)

# Without gate exclusion
M4_no_gate = 2 * T(4)
cap_no_gate = M4_no_gate - M(3)

# With gate exclusion
M4_with_gate = M(4)
cap_with_gate = M4_with_gate - M(3)

print(f"  At n = 4 = K, the gate face activates.")
print(f"")
print(f"  Without gate exclusion:")
print(f"    T(4) = {T(4)}")
print(f"    M(4) = 2 * {T(4)} = {M4_no_gate}")
print(f"    Capacity = {M4_no_gate} - {M(3)} = {cap_no_gate}")
print(f"")
print(f"  With gate exclusion:")
print(f"    T(4) = {T(4)}, G(4) = {G(4)}")
print(f"    T(4) - G(4) = {T(4)} - {G(4)} = {T(4) - G(4)}")
print(f"    M(4) = 2 * {T(4) - G(4)} = {M4_with_gate}")
print(f"    Capacity = {M4_with_gate} - {M(3)} = {cap_with_gate}")
print(f"")
print(f"  The gate exclusion reduces the capacity from {cap_no_gate} to {cap_with_gate}.")
print(f"  G(4) = ({K}-1)*{K}/2 = {G(4)} positions excluded.")
print(f"  This is computed from K = {K} alone. It is not a parameter.")
print(f"")
print(f"  The standard nuclear shell model requires spin-orbit coupling")
print(f"  (a phenomenological term with adjustable strength) to achieve")
print(f"  the same capacity of {cap_with_gate} at the fourth shell.")
print(f"  The Sierpinski walk produces it from geometry.")


# =====================================================================
# STEP 7: SHELL CAPACITIES VS. STANDARD MODEL
# =====================================================================

print(f"\n{'=' * 70}")
print("STEP 7: Shell capacities comparison")
print("=" * 70)

# Standard model capacities (with spin-orbit)
standard_caps = [2, 6, 12, 8, 22, 32, 44]

print(f"  {'Shell':>6}  {'Sierpinski':>11}  {'Std model':>10}  {'Match':>6}")
prev_M = 0
for n in range(1, 8):
    cap = M(n) - prev_M
    std = standard_caps[n - 1]
    match = cap == std
    note = " (with spin-orbit)" if n == 4 else ""
    print(f"  {n:>6}  {cap:>11}  {std:>10}{note}  {'  ✓' if match else '  ✗':>6}")
    prev_M = M(n)

all_caps_match = True
prev_M = 0
for n in range(1, 8):
    if M(n) - prev_M != standard_caps[n - 1]:
        all_caps_match = False
    prev_M = M(n)

print(f"")
print(f"  All capacities match: {all_caps_match}")
print(f"  Sierpinski: no spin-orbit coupling, no fitted parameters.")
print(f"  Standard model: requires spin-orbit term adjusted to data.")


# =====================================================================
# STEP 8: CONNECTION TO BINDING ENERGY
# =====================================================================

print(f"\n{'=' * 70}")
print("STEP 8: Connection to binding energy curve")
print("=" * 70)
print(f"""  The shell closures and binding energy share the same walk.

  Magic numbers pipeline:
    Uses K, D, and packing geometry (T, G, M).
    Produces exact integers.
    No field equation involved.

  Binding energy pipeline:
    Uses mu_SST(i^2) at each walk position.
    Produces a continuous curve.
    Calibrated from one element (Zn-64).

  Both are outputs of the 64-position Sierpinski walk
  defined by K = {K} and D = {D}.""")


# =====================================================================
# ADDITIONAL ANALYSIS: Structural numbers in the shell sequence
# =====================================================================

print(f"\n{'=' * 70}")
print("ADDITIONAL: Structural numbers appearing in the shell sequence")
print("=" * 70)

print(f"""
  The shell sequence contains several numbers with structural significance:

  Layer sizes (triangular numbers T(n) - T(n-1)):
    n=7: layer size = 28 = 8V + 12E + 8F (stellated octahedron elements)
    n=6: layer size = 21 = 1 + K + K^2 (coupling polynomial, s=+1)

  Gate exclusion values:
    G(7) = 21 = 1 + K + K^2 (TetA coupling depth)
    G(4) = 6 = number of edges of one tetrahedron

  Shell capacities:
    Capacity at n=4 is {M(4)-M(3)} = 2^D = range of coupling polynomial
    Capacity at n=1 is {M(1)} = proton-neutron pair

  Cumulative closures:
    M(4) = 28 = geometric elements of stellated octahedron
    M(7) = 126 = T(7) - G(7) doubled = 2 * 63 = 2 * (K^D - 1)

  Total available at n=7: T(7) - G(7) = 84 - 21 = 63 = K^D - 1
    The walk fills all but one position of the face.
""")


# =====================================================================
# VERIFICATION: Alternative K values
# =====================================================================

print(f"{'=' * 70}")
print("VERIFICATION: Why K = 4 is unique")
print("=" * 70)
print(f"  Testing K = 2, 3, 4, 5, 6 against observed magic numbers {OBSERVED_MAGIC}")
print(f"")

for K_test in [2, 3, 4, 5, 6]:
    def T_test(n):
        return n * (n + 1) * (n + 2) // 6
    def G_test(n):
        if n < K_test:
            return 0
        return (n - 1) * n // 2
    def M_test(n):
        return 2 * (T_test(n) - G_test(n))

    predicted_test = [M_test(n) for n in range(1, 8)]
    matches = sum(1 for p, o in zip(predicted_test, OBSERVED_MAGIC) if p == o)
    is_k4 = " <-- UNIQUE MATCH" if matches == 7 else ""
    print(f"  K = {K_test}: {predicted_test}  ({matches}/7 match){is_k4}")


# =====================================================================
# SUMMARY
# =====================================================================

print(f"\n{'=' * 70}")
print("SUMMARY")
print("=" * 70)
print(f"""
  Inputs:
    K = {K}, D = {D} (from 2(D+1) = 2^D)

  Formulas:
    T(n) = n(n+1)(n+2)/6     (tetrahedral packing)
    G(n) = (n-1)n/2, n >= K  (gate exclusion)
    M(n) = 2[T(n) - G(n)]    (shell closure)

  Results:
    Magic numbers: {[M(n) for n in range(1, 8)]}
    Capacities:    {[M(n) - (M(n-1) if n > 1 else 0) for n in range(1, 8)]}

  The 20 -> 28 anomaly:
    Gate activates at n = K = {K}
    G({K}) = {G(K)} positions excluded
    Capacity drops from {2*T(K) - M(K-1)} to {M(K) - M(K-1)}
    No spin-orbit coupling. Pure geometry.

  K = {K} is the only integer branching factor that reproduces
  all seven observed magic numbers.
""")
