#!/usr/bin/env python3
"""
GFD Three-Scale Nuclear Binding Energy
========================================

Predicts nuclear binding energy per nucleon (B/A) for any element
using the gate depth decomposition of the coupling polynomial
f(K,s) = 1 + Ks + K^2 at K = 4.

The nuclear binding energy distributes across K^D = 64 walk positions,
grouped by gate depth into [27, 27, 9, 1] positions. Each group carries
a distinct energy per position:

    B/A = 27*a(A) + 27*b + 9*c(Z,A)

    gd=0 (27 positions): a(A)   spatial energy, depends on A (topology)
    gd=1 (27 positions): b      gate coupling, universal constant
    gd=2 ( 9 positions): c(Z,A) closure energy, depends on Z and A
    gd=3 ( 1 position):  absorbed into constants (negligible)

The spatial energy a(A) reads the Sierpinski walk fill through A:

    a(A) = b * [3 + (9/K) * ln(1 + A / K^3)]

The closure energy c(Z,A) starts from a ceiling and is reduced by three
corrections that the 9 closure positions absorb:

    c(Z,A) = c_max(A) - c_surf(A) - c_coul(Z,A) - c_asym(Z,A) + c_pair(Z,A)

Every constant in the formula derives from:
    K = 4, D = 3, m_e = 0.51100 MeV, F+ = 21, F0 = 17, F- = 13, eps = 2/17
    b = m_e / (F0 - 1/2) = 0.03097 MeV

Zero fitted parameters.

Performance (78 core elements, Z=6 to Z=83):
    MAPE = 1.58%,  40/78 within 1%

Usage:
    python gfd_3scale_binding.py                # full validation
    python gfd_3scale_binding.py 26 56          # predict Iron-56
    python gfd_3scale_binding.py 92 238         # predict Uranium-238

License:
    MIT (code), CC BY 4.0 (documentation). Attributed to Stephen Nelson.
"""

import math
import csv
import sys


# =====================================================================
# Section 1: Framework Constants
# =====================================================================
#
# K = 4 is the unique integer satisfying 2(D+1) = 2^D.
# The coupling polynomial f(K,s) = 1 + Ks + K^2 evaluated at three
# structural states gives the energy scales of the framework.

K       = 4                          # branching factor
D       = 3                          # spatial dimensions

F_PLUS  = K*K + K + 1               # 21  (full coupling, s = +1)
F_ZERO  = K*K + 1                   # 17  (gate threshold, s = 0)
F_MINUS = K*K - K + 1               # 13  (deep field, s = -1)

M_E     = 0.51099895                 # electron mass (MeV): closure energy per 2pi
b       = M_E / (F_ZERO - 0.5)      # gate coupling: m_e / (F0 - 1/2) = m_e / 16.5

EPS     = 2.0 / F_ZERO              # 2/17  gate loss per crossing
SHELL   = K**D                       # 64    walk positions per shell


# =====================================================================
# Section 2: Gate Depth Distribution
# =====================================================================
#
# The 64 walk positions are distributed across four gate depths by the
# binomial expansion (3+1)^3 = 27 + 27 + 9 + 1:
#
#   gd=0: C(3,0) * 3^3 = 27 positions  (pure spatial, no gate crossing)
#   gd=1: C(3,1) * 3^2 = 27 positions  (one gate crossing in 3 levels)
#   gd=2: C(3,2) * 3^1 =  9 positions  (two gate crossings)
#   gd=3: C(3,3) * 3^0 =  1 position   (triple gate, negligible)
#
# Each depth carries a different role in the binding energy:
#   gd=0 reads the topology through the walk fill (depends on A)
#   gd=1 carries the generator constant (universal)
#   gd=2 carries the closure and absorbs all Z-dependent corrections

GD0_COUNT = 27                       # spatial positions
GD1_COUNT = 27                       # generator positions
GD2_COUNT = 9                        # closure positions
GD3_COUNT = 1                        # deep gate (absorbed)


# =====================================================================
# Section 3: Spatial Energy a(A) -- gd=0 positions
# =====================================================================
#
# The 27 spatial positions each carry an energy a(A) that grows
# logarithmically with A. The logarithm is the Field Origin term of
# the energy functional F(y) = y - 2*sqrt(y) + 2*ln(1+sqrt(y)),
# evaluated at sqrt(y) = A/K^3.
#
# The three structural constants in the formula:
#   3       = closure cycle count (Sierpinski generator depth)
#   9/K     = 2.25 = closure-to-coupling ratio (gd=2 count / K)
#   K^3     = 64 = shell capacity (walk positions per cycle)

def compute_a(A):
    """
    Spatial energy per gd=0 position.

    This is the topological contribution: it reads how many nucleons
    fill the Sierpinski walk, independently of their composition.

    Parameters
    ----------
    A : int   Mass number

    Returns
    -------
    float     Energy in MeV per gd=0 position
    """
    return b * (3 + (GD2_COUNT / K) * math.log(1 + A / SHELL))


# =====================================================================
# Section 4: Closure Energy c(Z,A) -- gd=2 positions
# =====================================================================
#
# The 9 closure positions absorb all Z-dependent physics. Their energy
# per position starts from a ceiling and is reduced by three corrections.
#
# The ceiling is what c would be if the nucleus were infinite, symmetric
# (N = Z), and uncharged. The three corrections account for:
#
#   Surface:   nucleons at the nuclear boundary have fewer neighbours.
#              The boundary is where the Sierpinski walk terminates,
#              which is why this correction lands on the closure positions
#              rather than the spatial or generator positions.
#
#   Coulomb:   protons repel each other across the nuclear radius.
#              The Z-dependence of this interaction means it enters
#              through the closure positions, which are the only ones
#              that respond to composition.
#
#   Asymmetry: nuclei with N != Z are less stable due to Pauli exclusion.
#              This is a composition effect, carried by closure.
#
#   Pairing:   even-even nuclei gain a small binding bonus.
#              Odd-odd nuclei pay a small penalty.
#
# The structural constants for each correction:
#
#   c_max uses: F+ * D/(D+K) * sqrt(D) = 15.588 (the volume ceiling)
#
#   Surface uses: F_ZERO * (1 + eps^2) = 17.235
#       The gate threshold F_ZERO sets the base surface energy.
#       The eps^2 correction accounts for additional gate exposure
#       at the nuclear boundary (codimension-1 surface, two transverse
#       gate crossings at rate eps each).
#
#   Coulomb uses: b * (F+ + F-/K - 1) = 0.707
#       The polynomial spread (F+ to F-) sets the Coulomb scale,
#       weighted by the gate coupling b.
#
#   Asymmetry uses: F+ + F-/K - 1 = 23.25
#       The same polynomial spread, without the b factor.
#
#   Pairing uses: D * K = 12
#       Spatial dimensions times branching factor.

# Pre-computed structural constants
VOLUME_CEILING = F_PLUS * D / (D + K) * math.sqrt(D)    # 15.588
SURF_COEFF     = F_ZERO * (1 + EPS**2)                   # 17.235
COUL_COEFF     = b * (F_PLUS + F_MINUS/K - 1)            #  0.707
ASYM_COEFF     = F_PLUS + F_MINUS/K - 1                  # 23.250
PAIR_COEFF     = D * K                                    # 12.000


def compute_c(Z, A):
    """
    Closure energy per gd=2 position.

    This carries all Z-dependent physics: surface, Coulomb, asymmetry,
    and pairing corrections are distributed across the 9 closure positions.

    Parameters
    ----------
    Z : int   Atomic number
    A : int   Mass number

    Returns
    -------
    dict with:
        c        : float  Net closure energy per position
        c_max    : float  Ceiling (infinite symmetric drop)
        c_surf   : float  Surface cost per position
        c_coul   : float  Coulomb cost per position
        c_asym   : float  Asymmetry cost per position
        c_pair   : float  Pairing contribution per position
    """
    N = A - Z
    face = GD0_COUNT * compute_a(A)
    chan = GD1_COUNT * b

    # Ceiling: what c would be without any corrections
    c_max = (VOLUME_CEILING - face - chan) / GD2_COUNT

    # Surface: boundary deficit, distributed across 9 closure positions
    c_surf = SURF_COEFF / (GD2_COUNT * A**(1.0/3))

    # Coulomb: proton repulsion, distributed across 9 closure positions
    c_coul = COUL_COEFF * Z * (Z - 1) / (GD2_COUNT * A**(4.0/3))

    # Asymmetry: N != Z penalty, distributed across 9 closure positions
    c_asym = ASYM_COEFF * (N - Z)**2 / (GD2_COUNT * A**2)

    # Pairing: even-even bonus, odd-odd penalty, odd-A zero
    if A % 2 == 1:
        c_pair = 0.0
    elif Z % 2 == 0 and N % 2 == 0:
        c_pair = PAIR_COEFF / (GD2_COUNT * A)
    else:
        c_pair = -PAIR_COEFF / (GD2_COUNT * A)

    c = c_max - c_surf - c_coul - c_asym + c_pair

    return {
        'c': c, 'c_max': c_max,
        'c_surf': c_surf, 'c_coul': c_coul,
        'c_asym': c_asym, 'c_pair': c_pair,
    }


# =====================================================================
# Section 5: The Complete Prediction
# =====================================================================

def predict(Z, A):
    """
    Predict B/A and decompose into Face, Chan, Sub from Z and A alone.

    Parameters
    ----------
    Z : int   Atomic number
    A : int   Mass number

    Returns
    -------
    dict with all computed quantities
    """
    if A <= 0:
        return {k: 0 for k in [
            'ba','face','chan','sub','a','c','c_max',
            'c_surf','c_coul','c_asym','c_pair',
            'fc','fs','cs',
        ]}

    # gd=0: spatial energy
    a = compute_a(A)
    face = GD0_COUNT * a

    # gd=1: generator energy
    chan = GD1_COUNT * b

    # gd=2: closure energy
    cr = compute_c(Z, A)
    sub = GD2_COUNT * cr['c']

    # Total
    ba = face + chan + sub

    # Three ratios
    fc = face / chan
    fs = face / sub if sub > 0.001 else float('inf')
    cs = chan / sub if sub > 0.001 else float('inf')

    return {
        'ba': ba,
        'face': face, 'chan': chan, 'sub': sub,
        'a': a, **cr,
        'fc': fc, 'fs': fs, 'cs': cs,
    }


# =====================================================================
# Section 6: Element Data (Z=2 to Z=92, CODATA B/A values)
# =====================================================================

ELEMENTS = [
    (  2, 'He',   4, 7.074), (  3, 'Li',   7, 5.606),
    (  4, 'Be',   9, 6.463), (  5, 'B',   11, 6.928),
    (  6, 'C',   12, 7.680), (  7, 'N',   14, 7.476),
    (  8, 'O',   16, 7.976), (  9, 'F',   19, 7.779),
    ( 10, 'Ne',  20, 8.032), ( 11, 'Na',  23, 8.111),
    ( 12, 'Mg',  24, 8.261), ( 13, 'Al',  27, 8.332),
    ( 14, 'Si',  28, 8.448), ( 15, 'P',   31, 8.481),
    ( 16, 'S',   32, 8.493), ( 17, 'Cl',  35, 8.520),
    ( 18, 'Ar',  40, 8.595), ( 19, 'K',   39, 8.557),
    ( 20, 'Ca',  40, 8.551), ( 21, 'Sc',  45, 8.619),
    ( 22, 'Ti',  48, 8.723), ( 23, 'V',   51, 8.742),
    ( 24, 'Cr',  52, 8.776), ( 25, 'Mn',  55, 8.765),
    ( 26, 'Fe',  56, 8.790), ( 27, 'Co',  59, 8.768),
    ( 28, 'Ni',  58, 8.732), ( 29, 'Cu',  63, 8.752),
    ( 30, 'Zn',  64, 8.756), ( 31, 'Ga',  69, 8.718),
    ( 32, 'Ge',  74, 8.725), ( 33, 'As',  75, 8.701),
    ( 34, 'Se',  80, 8.711), ( 35, 'Br',  79, 8.696),
    ( 36, 'Kr',  84, 8.717), ( 37, 'Rb',  85, 8.697),
    ( 38, 'Sr',  88, 8.733), ( 39, 'Y',   89, 8.714),
    ( 40, 'Zr',  90, 8.710), ( 41, 'Nb',  93, 8.664),
    ( 42, 'Mo',  98, 8.635), ( 43, 'Tc',  98, 8.610),
    ( 44, 'Ru', 102, 8.607), ( 45, 'Rh', 103, 8.584),
    ( 46, 'Pd', 106, 8.580), ( 47, 'Ag', 107, 8.554),
    ( 48, 'Cd', 114, 8.540), ( 49, 'In', 115, 8.516),
    ( 50, 'Sn', 120, 8.504), ( 51, 'Sb', 121, 8.482),
    ( 52, 'Te', 130, 8.440), ( 53, 'I',  127, 8.445),
    ( 54, 'Xe', 132, 8.428), ( 55, 'Cs', 133, 8.410),
    ( 56, 'Ba', 138, 8.393), ( 57, 'La', 139, 8.378),
    ( 58, 'Ce', 140, 8.376), ( 59, 'Pr', 141, 8.354),
    ( 60, 'Nd', 142, 8.346), ( 61, 'Pm', 145, 8.310),
    ( 62, 'Sm', 152, 8.244), ( 63, 'Eu', 153, 8.226),
    ( 64, 'Gd', 158, 8.224), ( 65, 'Tb', 159, 8.201),
    ( 66, 'Dy', 164, 8.186), ( 67, 'Ho', 165, 8.170),
    ( 68, 'Er', 166, 8.168), ( 69, 'Tm', 169, 8.139),
    ( 70, 'Yb', 174, 8.125), ( 71, 'Lu', 175, 8.108),
    ( 72, 'Hf', 180, 8.092), ( 73, 'Ta', 181, 8.078),
    ( 74, 'W',  184, 8.065), ( 75, 'Re', 187, 8.047),
    ( 76, 'Os', 192, 8.032), ( 77, 'Ir', 193, 8.017),
    ( 78, 'Pt', 195, 8.009), ( 79, 'Au', 197, 7.992),
    ( 80, 'Hg', 202, 7.976), ( 81, 'Tl', 205, 7.960),
    ( 82, 'Pb', 208, 7.950), ( 83, 'Bi', 209, 7.933),
    ( 84, 'Po', 209, 7.924), ( 85, 'At', 210, 7.910),
    ( 86, 'Rn', 222, 7.862), ( 87, 'Fr', 223, 7.854),
    ( 88, 'Ra', 226, 7.843), ( 89, 'Ac', 227, 7.835),
    ( 90, 'Th', 232, 7.821), ( 91, 'Pa', 231, 7.817),
    ( 92, 'U',  238, 7.804),
]


# =====================================================================
# Section 7: Single Element Prediction
# =====================================================================

def predict_single(Z, A):
    """Detailed breakdown for one element."""
    r = predict(Z, A)
    N = A - Z

    print()
    print(f"  Element: Z = {Z}, A = {A}, N = {N}")
    print()
    print(f"  THREE-SCALE DECOMPOSITION")
    print(f"  B/A = 27*a + 27*b + 9*c")
    print()
    print(f"    gd=0  27 positions x a = {r['a']:.4f} MeV  -->  Face = {r['face']:.4f} MeV")
    print(f"    gd=1  27 positions x b = {b:.4f} MeV  -->  Chan = {r['chan']:.4f} MeV")
    print(f"    gd=2   9 positions x c = {r['c']:.4f} MeV  -->  Sub  = {r['sub']:.4f} MeV")
    print(f"                                           B/A  = {r['ba']:.4f} MeV")
    print()
    print(f"  CLOSURE BREAKDOWN (c per gd=2 position)")
    print(f"    c_max (ceiling)     = {r['c_max']:+.4f} MeV")
    print(f"    c_surf (boundary)   = {r['c_surf']:.4f} MeV")
    print(f"    c_coul (proton rep) = {r['c_coul']:.4f} MeV")
    print(f"    c_asym (N != Z)     = {r['c_asym']:.4f} MeV")
    pr_label = "even-even" if r['c_pair'] > 0 else ("odd-odd" if r['c_pair'] < 0 else "odd A")
    print(f"    c_pair ({pr_label:>9})  = {r['c_pair']:+.4f} MeV")
    print(f"    c (net)             = {r['c']:.4f} MeV")
    print()
    print(f"  THREE RATIOS")
    print(f"    F/C = {r['fc']:.4f}")
    fs_s = f"{r['fs']:.4f}" if r['fs'] < 100 else "inf"
    cs_s = f"{r['cs']:.4f}" if r['cs'] < 100 else "inf"
    print(f"    F/S = {fs_s}")
    print(f"    C/S = {cs_s}")

    for z2, sym, a2, ba_k in ELEMENTS:
        if z2 == Z and a2 == A:
            sub_k = ba_k - r['face'] - r['chan']
            c_k = sub_k / GD2_COUNT
            print()
            print(f"  VS EXPERIMENT ({sym})")
            print(f"    B/A known  = {ba_k:.4f} MeV   error = {abs(r['ba']-ba_k):.4f} MeV ({abs(r['ba']-ba_k)/ba_k*100:.2f}%)")
            print(f"    c known    = {c_k:.4f} MeV   error = {abs(r['c']-c_k):.4f} MeV")
            break
    print()


# =====================================================================
# Section 8: Full Validation
# =====================================================================

def run_validation():
    """Validate across all elements."""

    print("=" * 140)
    print("  GFD THREE-SCALE NUCLEAR BINDING ENERGY")
    print("  B/A = 27*a(A) + 27*b + 9*c(Z,A)")
    print("  64 walk positions: [27 spatial, 27 generator, 9 closure, 1 gate core]")
    print("  Zero fitted parameters.")
    print("=" * 140)

    print(f"""
  STRUCTURAL CONSTANTS:
    K = {K},  D = {D},  b = {b} MeV
    F+ = {F_PLUS},  F0 = {F_ZERO},  F- = {F_MINUS}
    eps = 2/F0 = {EPS:.6f} (gate loss per crossing)
    Shell = K^D = {SHELL} (walk positions)

  CLOSURE COEFFICIENTS (all derived, zero fitted):
    Volume ceiling  = F+ x D/(D+K) x sqrt(D) = {VOLUME_CEILING:.4f} MeV
    Surface         = F0 x (1 + eps^2)        = {SURF_COEFF:.4f} MeV
    Coulomb         = b x (F+ + F-/K - 1)     = {COUL_COEFF:.5f} MeV
    Asymmetry       = F+ + F-/K - 1           = {ASYM_COEFF:.4f} MeV
    Pairing         = D x K                    = {PAIR_COEFF:.4f} MeV
""")

    # Per-element results
    print("-" * 140)
    print(f"  {'Sym':>3} {'Z':>3} {'A':>3}  "
          f"{'a':>6} {'c':>6} {'c_max':>6} {'sf/9':>6} {'cl/9':>6} {'as/9':>6} {'pr/9':>6}  "
          f"{'Face':>6} {'Chan':>5} {'Sub':>6}  "
          f"{'BA_p':>6} {'BA_k':>6} {'%err':>5}  "
          f"{'F/S':>5}")
    print("-" * 140)

    all_pcts = []; core_pcts = []; heavy_pcts = []; light_pcts = []
    sub_ok = 0

    for Z, sym, A, BA in ELEMENTS:
        r = predict(Z, A)
        pct = abs(r['ba'] - BA) / BA * 100

        all_pcts.append(pct)
        if Z >= 6 and Z <= 83:
            core_pcts.append(pct)
        elif Z <= 5:
            light_pcts.append(pct)
        else:
            heavy_pcts.append(pct)

        if r['sub'] > 0: sub_ok += 1

        fs_s = f"{r['fs']:>5.3f}" if r['fs'] < 100 else "  inf"
        flag = " *" if pct < 1 else ""

        print(f"  {sym:>3} {Z:>3} {A:>3}  "
              f"{r['a']:>6.4f} {r['c']:>6.4f} {r['c_max']:>6.4f} "
              f"{r['c_surf']:>6.4f} {r['c_coul']:>6.4f} {r['c_asym']:>6.4f} "
              f"{r['c_pair']:>+6.4f}  "
              f"{r['face']:>6.3f} {r['chan']:>5.3f} {r['sub']:>6.3f}  "
              f"{r['ba']:>6.3f} {BA:>6.3f} {pct:>4.1f}%  "
              f"{fs_s}{flag}")

    n_all = len(all_pcts)
    n_core = len(core_pcts)

    # Summary
    print()
    print("=" * 140)
    print("  RESULTS")
    print("=" * 140)

    def summarize(label, pcts):
        n = len(pcts)
        if n == 0: return
        mae_approx = sum(pcts) / n  # MAPE not MAE, but close label
        w1 = sum(1 for p in pcts if p < 1)
        w2 = sum(1 for p in pcts if p < 2)
        w5 = sum(1 for p in pcts if p < 5)
        mx = max(pcts)
        print(f"\n  {label} ({n} elements):")
        print(f"    MAPE:       {mae_approx:.3f}%")
        print(f"    Max error:  {mx:.2f}%")
        print(f"    Within 1%:  {w1}/{n} ({100*w1/n:.0f}%)")
        print(f"    Within 2%:  {w2}/{n} ({100*w2/n:.0f}%)")
        print(f"    Within 5%:  {w5}/{n} ({100*w5/n:.0f}%)")

    summarize("ALL ELEMENTS", all_pcts)
    summarize("CORE (Z=6 to Z=83)", core_pcts)
    summarize("LIGHT (Z=2 to Z=5)", light_pcts)
    summarize("HEAVY (Z=84 to Z=92)", heavy_pcts)

    print(f"\n  Sub > 0 (physical): {sub_ok}/{n_all}")

    # CSV export
    csv_path = 'gfd_3scale_binding.csv'
    with open(csv_path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow([
            'Z', 'Symbol', 'A', 'N',
            'a_gd0', 'b_gd1', 'c_gd2',
            'c_max', 'c_surf', 'c_coul', 'c_asym', 'c_pair',
            'Face', 'Chan', 'Sub',
            'BA_pred', 'BA_known', 'Error_pct',
            'F_over_C', 'F_over_S', 'C_over_S',
        ])
        for Z, sym, A, BA in ELEMENTS:
            r = predict(Z, A)
            pct = abs(r['ba'] - BA) / BA * 100
            w.writerow([
                Z, sym, A, A - Z,
                f"{r['a']:.6f}", f"{b:.6f}", f"{r['c']:.6f}",
                f"{r['c_max']:.6f}", f"{r['c_surf']:.6f}",
                f"{r['c_coul']:.6f}", f"{r['c_asym']:.6f}",
                f"{r['c_pair']:.6f}",
                f"{r['face']:.4f}", f"{r['chan']:.4f}", f"{r['sub']:.4f}",
                f"{r['ba']:.4f}", f"{BA:.3f}", f"{pct:.3f}",
                f"{r['fc']:.4f}",
                f"{r['fs']:.4f}" if r['fs'] < 100 else "inf",
                f"{r['cs']:.4f}" if r['cs'] < 100 else "inf",
            ])

    print(f"\n  Exported: {csv_path}")
    print()


# =====================================================================
# Section 9: Entry Point
# =====================================================================

if __name__ == '__main__':
    if len(sys.argv) == 3:
        predict_single(int(sys.argv[1]), int(sys.argv[2]))
    else:
        run_validation()
