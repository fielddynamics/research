#!/usr/bin/env python3
"""
Nuclear Magic Numbers and Shell Structure Pipeline
=====================================================
Part 1 (Steps 1-8): Derivation of the seven nuclear magic numbers from
the Sierpinski walk packing algebra. Pure combinatorics on K and D.

Part 2 (Steps 9-10): Valence shell filling for every element Z=1..82.
Uses mu_SST thresholds at magic number boundaries to assign walk
positions to shells, then computes per-shell energy decomposition and
validates predicted B/A against AME2020 experimental data via PlasmaPy.

Each function maps directly to a step in magic_numbers_pipeline.md.
Run this script to reproduce every number in the pipeline document.

Inputs:
  - K = 4, D = 3
  - T(n) = n(n+1)(n+2)/6
  - G(n) = (n-1)n/2 for n >= K, else 0
  - M(n) = 2[T(n) - G(n)]
  - mu_SST(x) = [(2x+1) - sqrt(4x+1)] / 2x
  - B/A(Zn-64) from PlasmaPy AME2020

Outputs:
  - Magic numbers: 2, 8, 20, 28, 50, 82, 126
  - Shell capacities: 2, 6, 12, 8, 22, 32, 44
  - Gate exclusion activates at n = K = 4
  - Valence shell filling for 82 elements (Z=1..82)
  - Per-shell energy decomposition with experimental validation

Stephen Nelson, Gravity Field Dynamics
"""

import math
from plasmapy.particles import nuclear_binding_energy


def observed_be_per_nucleon(symbol, a):
    """Return observed BE/A in MeV from PlasmaPy (AME2020 mass tables)."""
    if a < 2:
        return 0.0
    total = nuclear_binding_energy(f"{symbol}-{a}")
    return float(total.to("MeV").value) / a


# =====================================================================
# INPUTS
# =====================================================================

K = 4       # branching factor (faces per level)
D = 3       # depth (levels of subdivision)
KD = K**D   # 64 positions per face


# =====================================================================
# SST FUNCTION AND SHELL ASSIGNMENT (used in Steps 9-10)
# =====================================================================

def mu_sst(x):
    """SST quadratic: bound-state constitutive law.

    mu_SST(x) = [(2x+1) - sqrt(4x+1)] / 2x
    Physical root satisfying 0 < mu < 1 for x > 0.
    """
    if x <= 0:
        return 0.0
    return ((2 * x + 1) - math.sqrt(4 * x + 1)) / (2 * x)


MAGIC = [2, 8, 20, 28, 50, 82, 126]
SHELL_THRESH = [mu_sst(m * m) for m in MAGIC]

# Energy scale: calibrate from Zn-64 (one complete Sierpinski walk)
BA_ZN = 8.756  # framework value: full Sector 0 Sierpinski walk
SUM_KD = sum(mu_sst(i * i) for i in range(1, KD + 1))
SCALE = BA_ZN * KD / SUM_KD


def get_shell(i):
    """Shell index (1-based) for walk position i.

    Position i belongs to the lowest shell n such that
    mu_SST(i^2) <= mu_SST(M_n^2), where M_n is the n-th magic number.
    """
    mu = mu_sst(i * i)
    for n, thresh in enumerate(SHELL_THRESH):
        if mu <= thresh:
            return n + 1
    return len(SHELL_THRESH) + 1


def shell_capacity(n):
    """Number of nucleons shell n can hold (within one sector)."""
    prev = MAGIC[n - 2] if n >= 2 else 0
    return MAGIC[n - 1] - prev


def local_walk_position(global_pos):
    """Convert global nucleon position to local walk position (1-based).

    The walk restarts at each Sierpinski sector boundary (multiples of KD).
    Position 1-64 -> local 1-64 (sector 0)
    Position 65-128 -> local 1-64 (sector 1)
    etc.
    """
    return ((global_pos - 1) % KD) + 1


def element_shell_structure(A):
    """Compute shell filling for an element with mass number A.

    Returns a list of dicts, one per occupied shell, each with:
      n        : shell number (1-based)
      count    : nucleons in this shell (summed over all sectors)
      capacity : max nucleons per sector in this shell
      energy   : total binding energy contribution (MeV)
      sectors  : number of sectors that contribute to this shell
    """
    shells = {}
    total_energy = 0.0
    for pos in range(1, A + 1):
        local = local_walk_position(pos)
        sh = get_shell(local)
        mu = mu_sst(local * local)
        e = SCALE * mu
        total_energy += e
        if sh not in shells:
            shells[sh] = {"n": sh, "count": 0, "energy": 0.0}
        shells[sh]["count"] += 1
        shells[sh]["energy"] += e

    n_sectors = (A - 1) // KD + 1
    result = []
    for sh in sorted(shells.keys()):
        d = shells[sh]
        d["capacity"] = shell_capacity(sh)
        d["sectors"] = n_sectors
        result.append(d)
    return result, total_energy


# Isotope list: most abundant stable isotope per element, Z=1..82
_ISOTOPES = [
    ( 1, "H",    1), ( 2, "He",   4), ( 3, "Li",   7), ( 4, "Be",   9),
    ( 5, "B",   11), ( 6, "C",   12), ( 7, "N",   14), ( 8, "O",   16),
    ( 9, "F",   19), (10, "Ne",  20), (11, "Na",  23), (12, "Mg",  24),
    (13, "Al",  27), (14, "Si",  28), (15, "P",   31), (16, "S",   32),
    (17, "Cl",  35), (18, "Ar",  40), (19, "K",   39), (20, "Ca",  40),
    (21, "Sc",  45), (22, "Ti",  48), (23, "V",   51), (24, "Cr",  52),
    (25, "Mn",  55), (26, "Fe",  56), (27, "Co",  59), (28, "Ni",  58),
    (29, "Cu",  63), (30, "Zn",  64), (31, "Ga",  69), (32, "Ge",  74),
    (33, "As",  75), (34, "Se",  80), (35, "Br",  79), (36, "Kr",  84),
    (37, "Rb",  85), (38, "Sr",  88), (39, "Y",   89), (40, "Zr",  90),
    (41, "Nb",  93), (42, "Mo",  98), (43, "Tc",  98), (44, "Ru", 102),
    (45, "Rh", 103), (46, "Pd", 106), (47, "Ag", 107), (48, "Cd", 114),
    (49, "In", 115), (50, "Sn", 120), (51, "Sb", 121), (52, "Te", 128),
    (53, "I",  127), (54, "Xe", 132), (55, "Cs", 133), (56, "Ba", 138),
    (57, "La", 139), (58, "Ce", 140), (59, "Pr", 141), (60, "Nd", 142),
    (61, "Pm", 145), (62, "Sm", 152), (63, "Eu", 153), (64, "Gd", 158),
    (65, "Tb", 159), (66, "Dy", 164), (67, "Ho", 165), (68, "Er", 166),
    (69, "Tm", 169), (70, "Yb", 174), (71, "Lu", 175), (72, "Hf", 180),
    (73, "Ta", 181), (74, "W",  184), (75, "Re", 187), (76, "Os", 192),
    (77, "Ir", 193), (78, "Pt", 195), (79, "Au", 197), (80, "Hg", 202),
    (81, "Tl", 205), (82, "Pb", 208),
]

# Load experimental B/A for all isotopes
AME = [(z, sym, a, observed_be_per_nucleon(sym, a))
       for z, sym, a in _ISOTOPES]


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
          f"  {cap:>5}  {obs:>10}  {'  YES' if match else '   NO':>6}")
    prev_M = m

print(f"")
print(f"  All seven magic numbers reproduced: {all_match}")
predicted = [M(n) for n in range(1, 8)]
print(f"  Predicted: {predicted}")
print(f"  Observed:  {OBSERVED_MAGIC}")


# =====================================================================
# STEP 6: THE 20 -> 28 ANOMALY
# =====================================================================

print(f"\n{'=' * 70}")
print("STEP 6: The 20 -> 28 anomaly")
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
    print(f"  {n:>6}  {cap:>11}  {std:>10}{note}  {'  YES' if match else '   NO':>6}")
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


# =====================================================================
# PART 2: VALENCE SHELL STRUCTURE
# =====================================================================
# The magic numbers above define WHERE shells close. The remaining
# steps show HOW nucleons fill those shells for every element, using
# mu_SST thresholds to assign walk positions to shells and computing
# per-shell energy decomposition validated against AME2020 data.
# =====================================================================


# =====================================================================
# STEP 9: SHELL BOUNDARIES FROM mu_SST
# =====================================================================

print(f"\n{'=' * 70}")
print("STEP 9: Shell boundaries from mu_SST thresholds")
print("=" * 70)
print(f"  Each walk position i belongs to a shell based on mu_SST(i^2).")
print(f"  The boundary for shell n is mu_SST(M_n^2), where M_n is the")
print(f"  n-th magic number. Position i is in the lowest shell n such")
print(f"  that mu_SST(i^2) <= mu_SST(M_n^2).")
print(f"")
print(f"  {'Shell':>6}  {'Magic M':>8}  {'Threshold':>12}  {'MeV/pos':>10}"
      f"  {'Positions':>12}")

prev_magic = 0
for n in range(1, 8):
    mc = MAGIC[n - 1]
    thresh = SHELL_THRESH[n - 1]
    mev = SCALE * thresh
    cap = mc - prev_magic
    lo = prev_magic + 1
    hi = mc
    print(f"  {n:>6}  {mc:>8}  {thresh:>12.6f}  {mev:>10.4f}"
          f"  {lo:>4} -> {hi:>4}  ({cap} positions)")
    prev_magic = mc

print(f"")
print(f"  Energy scale: SCALE = B/A(Zn) * K^D / sum_KD = {SCALE:.4f}")
print(f"  B/A(Zn-64) = {BA_ZN:.4f} MeV (framework, Sector 0)")
print(f"")
print(f"  Sector rule: for A > K^D = {KD}, the walk restarts at each")
print(f"  sector boundary. Positions 65-128 use local walk positions")
print(f"  1-64, so the shell structure repeats per Sierpinski sector.")


# =====================================================================
# STEP 10: SHELL FILLING ACROSS THE PERIODIC TABLE
# =====================================================================

print(f"\n{'=' * 70}")
print("STEP 10: Shell filling across the periodic table")
print("=" * 70)

# Detailed breakdown for key elements
KEY_ELEMENTS = [
    ( 2, "He",   4, "doubly magic, shell 1 closure"),
    ( 8, "O",   16, "shell 2 closure"),
    (20, "Ca",  40, "doubly magic, shell 3 closure"),
    (26, "Fe",  56, "peak B/A, mid-shell 5"),
    (28, "Ni",  58, "near shell 4 closure"),
    (30, "Zn",  64, "K^D boundary, calibration point"),
    (50, "Sn", 120, "shell 5 closure region, sector 1"),
    (82, "Pb", 208, "doubly magic, heaviest stable"),
]

for Z, sym, A, note in KEY_ELEMENTS:
    ba_exp = observed_be_per_nucleon(sym, A)
    shells, B_total = element_shell_structure(A)
    ba_pred = B_total / A
    err_keV = (ba_pred - ba_exp) * 1000

    n_sectors = (A - 1) // KD + 1
    print(f"\n  --- {sym}-{A} (Z={Z}): {note} ---")
    print(f"  Sectors: {n_sectors}   Experimental B/A: {ba_exp:.4f} MeV"
          f"   Predicted B/A: {ba_pred:.4f} MeV   Error: {err_keV:+.0f} keV")
    print(f"  {'Shell':>6}  {'Nucleons':>9}  {'Capacity':>9}"
          f"  {'Status':>10}  {'Energy (MeV)':>13}  {'Per nucleon':>12}")

    for sh in shells:
        total_cap = sh["capacity"] * n_sectors
        if sh["count"] >= total_cap:
            status = "FULL"
        elif sh["count"] > 0:
            status = f"{sh['count']}/{total_cap}"
        else:
            status = "empty"
        per_n = sh["energy"] / sh["count"] if sh["count"] > 0 else 0
        print(f"  {sh['n']:>6}  {sh['count']:>9}  {total_cap:>9}"
              f"  {status:>10}  {sh['energy']:>13.3f}  {per_n:>12.4f}")

    print(f"  {'':>6}  {A:>9}  {'':>9}  {'':>10}  {B_total:>13.3f}"
          f"  {ba_pred:>12.4f}")


# Full summary table for all 82 elements
print(f"\n\n  Full element summary (Z=1..82):")
print(f"  {'Z':>3} {'El':<3} {'A':>4}  {'Sec':>4}  {'Shells used':>12}"
      f"  {'B/A pred':>9}  {'B/A exp':>9}  {'Err keV':>8}"
      f"  {'Valence':>10}")

for Z, sym, A, ba_exp in AME:
    if ba_exp <= 0:
        continue
    shells, B_total = element_shell_structure(A)
    ba_pred = B_total / A
    err_keV = (ba_pred - ba_exp) * 1000
    n_sectors = (A - 1) // KD + 1

    max_shell = max(sh["n"] for sh in shells)
    valence = shells[-1]
    total_cap = valence["capacity"] * n_sectors
    valence_str = f"n={valence['n']} {valence['count']}/{total_cap}"

    shell_list = ",".join(str(sh["n"]) for sh in shells)
    print(f"  {Z:>3} {sym:<3} {A:>4}  {n_sectors:>4}  {shell_list:>12}"
          f"  {ba_pred:>9.4f}  {ba_exp:>9.4f}  {err_keV:>+8.0f}"
          f"  {valence_str:>10}")


# =====================================================================
# STEP 11: VALIDATION
# =====================================================================

print(f"\n{'=' * 70}")
print("STEP 11: Validation against AME2020")
print("=" * 70)

# Shell closure verification
print(f"\n  Shell closure verification:")
print(f"  At each magic number A, confirm that the corresponding shell")
print(f"  is exactly filled in the GFD walk.")
print(f"")
print(f"  {'Magic A':>8}  {'Element':>10}  {'Shell n':>8}"
      f"  {'Filled':>7}  {'Cap':>5}  {'Exact':>6}")

magic_elements = {
    2:   ("He",  4),
    8:   ("O",  16),
    20:  ("Ca", 40),
    28:  ("Ni", 58),
    50:  ("Sn", 120),
    82:  ("Pb", 208),
}

for shell_n, mc in enumerate(MAGIC, 1):
    if mc > 126:
        continue
    if mc in magic_elements:
        sym, A = magic_elements[mc]
    else:
        continue
    shells, _ = element_shell_structure(A)
    n_sectors = (A - 1) // KD + 1
    target_shell = None
    for sh in shells:
        if sh["n"] == shell_n:
            target_shell = sh
            break
    if target_shell is None:
        exact = "N/A"
        filled = 0
        cap = shell_capacity(shell_n) * n_sectors
    else:
        cap = shell_capacity(shell_n) * n_sectors
        filled = target_shell["count"]
        exact = "YES" if filled == cap else "NO"
    print(f"  {mc:>8}  {sym + '-' + str(A):>10}  {shell_n:>8}"
          f"  {filled:>7}  {cap:>5}  {exact:>6}")


# Enhanced stability at closures
print(f"\n  Enhanced stability at shell closures:")
print(f"  Nuclei at magic numbers should have above-average B/A for")
print(f"  their mass region.")
print(f"")

# Compute B/A for magic number nuclei and their neighbours
for mc_key, (sym, A) in magic_elements.items():
    ba_exp = observed_be_per_nucleon(sym, A)
    # Find neighbours in our isotope list
    neighbours = [(z2, s2, a2, b2) for z2, s2, a2, b2 in AME
                  if abs(a2 - A) <= 6 and a2 != A and b2 > 0]
    if neighbours:
        avg_neighbour = sum(b for _, _, _, b in neighbours) / len(neighbours)
        enhancement = (ba_exp - avg_neighbour) * 1000
        print(f"  {sym + '-' + str(A):>8}:  B/A = {ba_exp:.4f} MeV,"
              f"  neighbours avg = {avg_neighbour:.4f} MeV,"
              f"  enhancement = {enhancement:+.0f} keV")


# Global accuracy statistics
print(f"\n  Prediction accuracy (mu_SST rising curve only, A=4..{KD}):")

data_r1 = [(a, ba) for _, _, a, ba in AME if 4 <= a <= KD and ba > 0]
if data_r1:
    ba_mean_r1 = sum(ba for _, ba in data_r1) / len(data_r1)
    ss_res = 0.0
    ss_tot = 0.0
    sum_abs = 0.0
    for a, ba in data_r1:
        shells, b_total = element_shell_structure(a)
        pred = b_total / a
        ss_res += (pred - ba) ** 2
        ss_tot += (ba - ba_mean_r1) ** 2
        sum_abs += abs(pred - ba)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    mae = sum_abs / len(data_r1) * 1000
    print(f"  R2 = {r2:.4f},  MAE = {mae:.0f} keV,  N = {len(data_r1)}")


# =====================================================================
# UPDATED SUMMARY
# =====================================================================

print(f"\n{'=' * 70}")
print("COMPLETE SUMMARY")
print("=" * 70)
print(f"""
  Part 1: Magic Numbers (pure combinatorics)
    Inputs: K = {K}, D = {D}
    T(n) = n(n+1)(n+2)/6, G(n) = (n-1)n/2 for n >= K
    M(n) = 2[T(n) - G(n)]
    Magic numbers: {[M(n) for n in range(1, 8)]}
    Capacities:    {[M(n) - (M(n-1) if n > 1 else 0) for n in range(1, 8)]}
    20 -> 28 anomaly: gate at n = K = {K}, no spin-orbit coupling.

  Part 2: Shell Structure (mu_SST + AME2020)
    Shell thresholds: mu_SST(M_n^2) at each magic number
    Energy scale: {SCALE:.4f} (calibrated from Zn-64)
    Elements covered: Z = 1..82 (H through Pb)
    Sector restarts: walk repeats every K^D = {KD} positions
    Experimental data: PlasmaPy AME2020 mass tables

  The magic numbers define the shell closures.
  mu_SST assigns every walk position to a shell.
  Together they produce the full valence shell structure
  for any element, validated against experimental binding energies.
""")
