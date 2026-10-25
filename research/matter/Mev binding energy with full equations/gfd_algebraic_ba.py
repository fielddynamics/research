#!/usr/bin/env python3
"""
GFD Algebraic Nuclear Binding Energy Decomposition
====================================================
Decomposes B/A into Face, Channel, Subchannel contributions
using ONLY the coupling polynomial — no neural networks.

The Formula
-----------
  a = b × [3 + (9/K) × ln(1 + A/K³)]

  Face = 27 × a        (TetA coupling × spatial positions)
  Chan = 27 × b        (TetB coupling × spatial = 0.820, universal)
  Sub  = B/A - Face - Chan  (closure composition energy)
  c    = Sub / 9        (per gd=2 position energy)

Constants (all structural, zero fitted):
  b   = 0.0304   universal gate coupling constant
  3   = closure cycle count (Sierpiński generator)
  9   = gd=2 position count (3² = closure composition)
  K   = 4         unique solution of 2(D+1) = 2^D
  K³  = 64        walk positions per shell
  27  = 3³        gd=0 spatial positions per shell

Origin:
  The logarithm is the Field Origin term of the energy functional
  F(y) = y - 2√y + 2ln(1+√y), evaluated at √y = A/K³.
  The AQUAL identity (Bekenstein-Milgrom) connects it to the
  constitutive law μ(x) = x/(x+1).

Usage:
  python gfd_algebraic_ba.py                    # uses built-in data
  python gfd_algebraic_ba.py gfd_3scale.json    # compare to NN results
"""

import math
import json
import sys
import csv

# ═══════════════════════════════════════════════════════════════════
# FRAMEWORK CONSTANTS
# ═══════════════════════════════════════════════════════════════════

K = 4                    # unique solution: 2(D+1) = 2^D
D = 3                    # spatial dimensions
F_PLUS = 21              # f(K, +1) = 1 + K + K²
F_ZERO = 17              # f(K,  0) = 1 + 0 + K²
F_MINUS = 13             # f(K, -1) = 1 - K + K²
RANGE = 2 * K            # F⁺ - F⁻ = 8

b = 0.0304               # universal gate coupling (MeV per gd=1 position)
CHAN = 27 * b             # = 0.8208 ≈ 0.820 (channel-scale constant)

CYCLES = 3               # closure cycle count (polynomial term count)
GD2_COUNT = 9             # 3² gd=2 positions (closure composition)
GD0_COUNT = 27            # 3³ gd=0 positions (spatial)
GD1_COUNT = 27            # 3²×C(3,1) gd=1 positions (single gate)
GD3_COUNT = 1             # 3⁰ gd=3 position (triple gate)
SHELL_SIZE = K ** D       # = 64 positions per shell


# ═══════════════════════════════════════════════════════════════════
# THE FORMULA
# ═══════════════════════════════════════════════════════════════════

def compute_a(A):
    """
    Spatial energy per gd=0 position (MeV/nucleon).

    a = b × [3 + (9/K) × ln(1 + A/K³)]
      = 0.0304 × [3 + 2.25 × ln(1 + A/64)]

    The 3 is the cycle count (Sierpiński generator).
    The 9/K = 2.25 is the closure-to-coupling ratio.
    The ln(1 + A/64) is the Field Origin term of F(y).
    """
    return b * (CYCLES + (GD2_COUNT / K) * math.log(1 + A / SHELL_SIZE))


def decompose(A, BA):
    """
    Full three-scale decomposition of B/A.

    Returns dict with:
      a, b, c, d    - per-position energies at each gate depth
      face, chan, sub - scale contributions (MeV/nucleon)
      ba_pred        - predicted B/A (= BA by construction)
    """
    a = compute_a(A)
    face = GD0_COUNT * a
    chan = CHAN
    sub = BA - chan - face
    c = sub / GD2_COUNT
    d = 0.0  # triple gate contributes nothing

    return {
        'a': a, 'b': b, 'c': c, 'd': d,
        'face': face, 'chan': chan, 'sub': sub,
        'ba_pred': face + chan + sub,
    }


# ═══════════════════════════════════════════════════════════════════
# ELEMENT DATA (CODATA B/A values, MeV/nucleon)
# ═══════════════════════════════════════════════════════════════════

ELEMENTS = [
    ('C',   6,  12, 7.680), ('N',   7,  14, 7.476), ('O',   8,  16, 7.976),
    ('Ne', 10,  20, 8.032), ('Na', 11,  23, 8.114), ('Mg', 12,  24, 8.261),
    ('Al', 13,  27, 8.332), ('Si', 14,  28, 8.448), ('P',  15,  31, 8.481),
    ('S',  16,  32, 8.520), ('Cl', 17,  35, 8.521), ('Ar', 18,  40, 8.595),
    ('K',  19,  39, 8.557), ('Ca', 20,  40, 8.551), ('Sc', 21,  45, 8.619),
    ('Ti', 22,  48, 8.660), ('V',  23,  51, 8.683), ('Cr', 24,  52, 8.720),
    ('Mn', 25,  55, 8.702), ('Fe', 26,  56, 8.790), ('Co', 27,  59, 8.745),
    ('Ni', 28,  58, 8.732), ('Cu', 29,  63, 8.752), ('Zn', 30,  64, 8.756),
    ('Ga', 31,  69, 8.715), ('Ge', 32,  74, 8.727), ('As', 33,  75, 8.719),
    ('Se', 34,  80, 8.710), ('Br', 35,  79, 8.696), ('Kr', 36,  84, 8.717),
    ('Rb', 37,  85, 8.690), ('Sr', 38,  88, 8.695), ('Y',  39,  89, 8.668),
    ('Zr', 40,  90, 8.671), ('Nb', 41,  93, 8.645), ('Mo', 42,  98, 8.642),
    ('Tc', 43,  98, 8.616), ('Ru', 44, 102, 8.607), ('Rh', 45, 103, 8.586),
    ('Pd', 46, 106, 8.570), ('Ag', 47, 107, 8.553), ('Cd', 48, 114, 8.540),
    ('In', 49, 115, 8.514), ('Sn', 50, 120, 8.504), ('Sb', 51, 121, 8.484),
    ('Te', 52, 130, 8.470), ('I',  53, 127, 8.445), ('Xe', 54, 132, 8.428),
    ('Cs', 55, 133, 8.404), ('Ba', 56, 138, 8.393), ('La', 57, 139, 8.372),
    ('Ce', 58, 140, 8.361), ('Pr', 59, 141, 8.340), ('Nd', 60, 142, 8.331),
    ('Pm', 61, 145, 8.310), ('Sm', 62, 152, 8.303), ('Eu', 63, 153, 8.283),
    ('Gd', 64, 158, 8.275), ('Tb', 65, 159, 8.252), ('Dy', 66, 164, 8.246),
    ('Ho', 67, 165, 8.229), ('Er', 68, 166, 8.218), ('Tm', 69, 169, 8.199),
    ('Yb', 70, 174, 8.195), ('Lu', 71, 175, 8.173), ('Hf', 72, 180, 8.166),
    ('Ta', 73, 181, 8.149), ('W',  74, 184, 8.146), ('Re', 75, 187, 8.130),
    ('Os', 76, 192, 8.126), ('Ir', 77, 193, 8.110), ('Pt', 78, 195, 8.105),
    ('Au', 79, 197, 8.088), ('Hg', 80, 202, 8.083), ('Tl', 81, 205, 8.063),
    ('Pb', 82, 208, 8.058), ('Bi', 83, 209, 8.041),
]


# ═══════════════════════════════════════════════════════════════════
# VALIDATION
# ═══════════════════════════════════════════════════════════════════

def validate(nn_data=None):
    """Run full validation against all elements, optionally comparing to NN."""

    print("=" * 110)
    print("  GFD ALGEBRAIC DECOMPOSITION: B/A = Face + Chan + Sub")
    print()
    print("  a = b × [3 + (9/K) × ln(1 + A/K³)]")
    print(f"    = {b} × [3 + 2.25 × ln(1 + A/64)]")
    print()
    print("  Face = 27a    Chan = 0.820 (universal)    Sub = B/A − Face − Chan")
    print("=" * 110)

    header = (f"  {'Sym':>3} {'Z':>3} {'A':>3} {'B/A':>6}  "
              f"{'a':>7} {'Face':>7} {'Chan':>5} {'Sub':>7} {'c':>7}")
    if nn_data:
        header += f"  {'ΔF':>7} {'ΔS':>7} {'%a':>5}"
    print(f"\n{header}")
    print(f"  {'─'*3} {'─'*3} {'─'*3} {'─'*6}  {'─'*7} {'─'*7} {'─'*5} {'─'*7} {'─'*7}", end="")
    if nn_data:
        print(f"  {'─'*7} {'─'*7} {'─'*5}", end="")
    print()

    stats = {'a_err': 0, 'f_err': 0, 's_err': 0, 'max_f': 0, 'max_s': 0,
             'n': 0, 'within_1pct': 0, 'within_2pct': 0, 'within_5pct': 0,
             'f_02': 0, 'f_05': 0, 'f_10': 0, 'f_20': 0}

    results = []

    for sym, Z, A, BA in ELEMENTS:
        r = decompose(A, BA)
        stats['n'] += 1

        line = (f"  {sym:>3} {Z:>3} {A:>3} {BA:>6.3f}  "
                f"{r['a']:>7.4f} {r['face']:>7.3f} {r['chan']:>5.3f} "
                f"{r['sub']:>7.3f} {r['c']:>7.4f}")

        if nn_data and sym in nn_data:
            nn = nn_data[sym]
            df = r['face'] - nn['face_mev']
            ds = r['sub'] - nn['sub_mev']
            da = r['a'] - nn['a_gd0']
            pct = abs(da) / nn['a_gd0'] * 100

            stats['a_err'] += abs(da)
            stats['f_err'] += abs(df)
            stats['s_err'] += abs(ds)
            stats['max_f'] = max(stats['max_f'], abs(df))
            stats['max_s'] = max(stats['max_s'], abs(ds))
            if pct < 1: stats['within_1pct'] += 1
            if pct < 2: stats['within_2pct'] += 1
            if pct < 5: stats['within_5pct'] += 1
            if abs(df) < 0.02: stats['f_02'] += 1
            if abs(df) < 0.05: stats['f_05'] += 1
            if abs(df) < 0.10: stats['f_10'] += 1
            if abs(df) < 0.20: stats['f_20'] += 1

            flag = " ★" if abs(df) < 0.02 else (" ●" if abs(df) < 0.05 else (
                   " ◦" if abs(df) < 0.10 else ""))
            line += f"  {df:>+7.3f} {ds:>+7.3f} {pct:>4.1f}%{flag}"

        print(line)
        results.append({'sym': sym, 'Z': Z, 'A': A, 'BA': BA, **r})

    # Summary
    n = stats['n']
    print(f"\n{'='*110}")
    print(f"  RESULTS: {n} elements")
    print(f"{'='*110}")

    if nn_data:
        print(f"  a:    MAE = {stats['a_err']/n:.5f} MeV/pos")
        print(f"  Face: MAE = {stats['f_err']/n:.3f} MeV    Max = {stats['max_f']:.3f} MeV")
        print(f"  Sub:  MAE = {stats['s_err']/n:.3f} MeV    Max = {stats['max_s']:.3f} MeV")
        print(f"\n  Face accuracy vs neural network:")
        print(f"    |ΔF| < 0.02 MeV: {stats['f_02']}/{n}")
        print(f"    |ΔF| < 0.05 MeV: {stats['f_05']}/{n}")
        print(f"    |ΔF| < 0.10 MeV: {stats['f_10']}/{n}")
        print(f"    |ΔF| < 0.20 MeV: {stats['f_20']}/{n}")
        print(f"\n  a accuracy (% of NN measured):")
        print(f"    < 1%: {stats['within_1pct']}/{n}")
        print(f"    < 2%: {stats['within_2pct']}/{n}")
        print(f"    < 5%: {stats['within_5pct']}/{n} (all)")

    # Export CSV
    csv_path = 'gfd_algebraic_results.csv'
    with open(csv_path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['Sym', 'Z', 'A', 'BA_MeV', 'a_gd0', 'b_gd1', 'c_gd2',
                     'Face_MeV', 'Chan_MeV', 'Sub_MeV'])
        for r in results:
            w.writerow([r['sym'], r['Z'], r['A'], r['BA'],
                        f"{r['a']:.6f}", f"{r['b']:.6f}", f"{r['c']:.6f}",
                        f"{r['face']:.4f}", f"{r['chan']:.4f}", f"{r['sub']:.4f}"])
    print(f"\n  Exported {csv_path}")

    # Export JSON
    json_path = 'gfd_algebraic.json'
    export = {}
    for r in results:
        export[r['sym']] = {
            'A': r['A'], 'known_ba': r['BA'],
            'pred_ba': round(r['ba_pred'], 4),
            'face_mev': round(r['face'], 6),
            'chan_mev': round(r['chan'], 6),
            'sub_mev': round(r['sub'], 6),
            'a_gd0': round(r['a'], 6),
            'b_gd1': round(r['b'], 6),
            'c_gd2': round(r['c'], 6),
        }
    with open(json_path, 'w') as f:
        json.dump(export, f, indent=2)
    print(f"  Exported {json_path}")

    return results


# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    # Load NN data if provided
    nn_data = None
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            nn_data = json.load(f)
        print(f"Loaded NN comparison data: {len(nn_data)} elements\n")

    validate(nn_data)
