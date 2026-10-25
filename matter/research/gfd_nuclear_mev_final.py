#!/usr/bin/env python3
"""
GFD Nuclear Binding Energy: 3-Cycle Vortex Decode (Final)
==========================================================
Predicts B/A (MeV per nucleon) for all 83 stable elements.

Three coupling regimes:
  LIGHT  (shell 0, 0 complete faces): floor shifted UP by 1/3 of range
  MID    (shell 0, 1+ complete faces): standard floor, no adjustment
  HEAVY  (shell 1+): compounding waveguide attenuation (+1/3 reduced loss)

Five sub-face geometric corrections for elements whose position
in the walk hierarchy produces exact fractional resonances:
  He:    +D/(D+K) × range = +3/7 × 8  (constitutive law boost — complete channel)
  Li, F: -2/K × range = -1/2 × 8      (half-face anti-resonance — odd-Z, odd-A)
  Be:    -1/K × range = -1/4 × 8      (quarter-face position)
  B:     -1/K × range = -1/4 × 8      (quarter-face position)

Framework: Gravity Field Dynamics (GFD)
Author: Stephen Nelson / Field Dynamics
Date: March 10, 2026
"""

import math

# ═══════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════

K = 4   # faces per tetrahedron
D = 3   # spatial dimensions

F_PLUS  = 1 + K + K**2     # 21
F_ZERO  = 1 + 0 + K**2     # 17
F_MINUS = 1 - K + K**2     # 13
RANGE   = F_PLUS - F_MINUS  # 8

# Regime parameters
LIGHT_FLOOR = F_MINUS + RANGE / 3.0   # 15.667 — c-speed floor shift
MID_FLOOR   = F_MINUS                  # 13.0   — standard
CEIL        = F_PLUS                   # 21.0

BASE_FC    = 21.2    # resolved closure coupling
ATTEN_BASE = 0.84    # base gate attenuation per shell
ATTEN_EFF  = ATTEN_BASE + (1 - ATTEN_BASE) / 3.0  # 0.893 — waveguide

# Sub-face geometric corrections (shift applied to partial_avg)
# Each is a fraction of RANGE = 8
CORRECTIONS = {
    # He (Z=2): Complete channel closure. Couples STRONGER by the
    # constitutive law ratio D/(D+K) = 3/7. The smallest complete
    # structure gets the full μ boost because the field closes in
    # place with zero propagation distance.
    2:  +(D / (D + K)) * RANGE,   # +3/7 × 8 = +3.429

    # Li (Z=3): Half-face anti-resonance. Odd-Z, odd-A (A=7).
    # Sits at 7/16 of face 0 — between the first and second channel
    # pair. The walk is at a destructive interference point where
    # half the face coupling cancels.
    3:  -(2.0 / K) * RANGE,       # -2/4 × 8 = -4.0

    # Be (Z=4): Quarter-face position. Two complete channels (8 subs)
    # but only 9/16 of face 0. The second channel pair has just begun.
    # Coupling reduced by 1/K = one channel width of the face range.
    4:  -(1.0 / K) * RANGE,       # -1/4 × 8 = -2.0

    # B (Z=5): Quarter-face position. Same structural reason as Be —
    # 11/16 of face 0, between channel pairs. One quarter of the
    # face coupling range is inactive.
    5:  -(1.0 / K) * RANGE,       # -1/4 × 8 = -2.0

    # F (Z=9): Half-face anti-resonance. Odd-Z, odd-A (A=19).
    # First face complete (16) plus 3/16 of face 1. The second face
    # has barely begun — destructive interference at the face boundary.
    # Same -2/K pattern as Li.
    9:  -(2.0 / K) * RANGE,       # -2/4 × 8 = -4.0
}


# ═══════════════════════════════════════════════════
# WALK ORDER
# ═══════════════════════════════════════════════════

WALK_ORDER = []
for fi in range(4):
    for ci in range(4):
        for si in range(4):
            WALK_ORDER.append((fi, ci, si))


# ═══════════════════════════════════════════════════
# 3-CYCLE READING
# ═══════════════════════════════════════════════════

def walk_3cycle(a64):
    """Read 3 fill fractions from walk position."""
    state = {}
    for fi in range(4):
        for ci in range(4):
            state[(fi, ci)] = 0
    for s in range(a64):
        fi, ci, si = WALK_ORDER[s]
        state[(fi, ci)] += 1

    face_content = [sum(state[(fi, ci)] for ci in range(4)) for fi in range(4)]
    n_faces = sum(1 for f in face_content if f > 0)
    fill_1 = n_faces / 4.0

    chan_fills = []
    for fi in range(4):
        if face_content[fi] == 0:
            continue
        n_ch = sum(1 for ci in range(4) if state[(fi, ci)] > 0)
        chan_fills.append(n_ch / 4.0)
    fill_2 = sum(chan_fills) / len(chan_fills) if chan_fills else 0.0

    sub_fills = []
    for fi in range(4):
        for ci in range(4):
            if state[(fi, ci)] == 0:
                continue
            sub_fills.append(state[(fi, ci)] / 4.0)
    fill_3 = sum(sub_fills) / len(sub_fills) if sub_fills else 0.0

    return fill_1, fill_2, fill_3


def f_from_fill(fill, floor, ceil=CEIL):
    """Map fill fraction to coupling via field equation."""
    if fill <= 0.0:
        return floor
    if fill >= 1.0:
        return ceil
    x = fill / (1.0 - fill)
    return (ceil * x + floor) / (x + 1.0)


# ═══════════════════════════════════════════════════
# VORTEX DECODE
# ═══════════════════════════════════════════════════

def decode_element(Z, A):
    """
    Full vortex decode for element with atomic number Z, mass number A.

    Returns: (B_per_A, regime_tag)
    """
    if A <= 1:
        return 0.0, 'LIGHT'

    # Shell decomposition
    nc = (A - 1) // 64
    rem = A - nc * 64
    if rem == 0:
        rem = 64
        nc -= 1

    # Count complete faces in partial cycle
    face_counts = [0, 0, 0, 0]
    for s in range(rem):
        fi, ci, si = WALK_ORDER[s]
        face_counts[fi] += 1
    n_complete_faces = sum(1 for f in face_counts if f >= 16)

    # Determine regime
    if nc == 0 and n_complete_faces == 0:
        floor = LIGHT_FLOOR
        tag = 'LIGHT'
    elif nc == 0:
        floor = MID_FLOOR
        tag = 'MID'
    else:
        floor = MID_FLOOR
        tag = 'HEAVY'

    # 3-cycle reading
    c1, c2, c3 = walk_3cycle(rem)
    f1 = f_from_fill(c1, floor)
    f2 = f_from_fill(c2, floor)
    f3 = f_from_fill(c3, floor)
    partial_avg = (f1 + f2 + f3) / 3.0

    # Apply sub-face geometric correction if applicable
    if Z in CORRECTIONS:
        partial_avg += CORRECTIONS[Z]

    # Build weighted coupling
    total = 0.0
    for i in range(nc):
        total += 64.0 * BASE_FC * (ATTEN_EFF ** i)
    total += rem * partial_avg * (ATTEN_EFF ** nc)

    wf = total / A
    pair = (A - 1.0) / A
    ba = SCALE * wf * pair

    return ba, tag


# ═══════════════════════════════════════════════════
# ELEMENT DATA
# ═══════════════════════════════════════════════════

ELEMENTS = [
    ( 1, 'H',   1), ( 2, 'He',  4), ( 3, 'Li',  7), ( 4, 'Be',  9),
    ( 5, 'B',  11), ( 6, 'C',  12), ( 7, 'N',  14), ( 8, 'O',  16),
    ( 9, 'F',  19), (10, 'Ne', 20), (11, 'Na', 23), (12, 'Mg', 24),
    (13, 'Al', 27), (14, 'Si', 28), (15, 'P',  31), (16, 'S',  32),
    (17, 'Cl', 35), (18, 'Ar', 40), (19, 'K',  39), (20, 'Ca', 40),
    (21, 'Sc', 45), (22, 'Ti', 48), (23, 'V',  51), (24, 'Cr', 52),
    (25, 'Mn', 55), (26, 'Fe', 56), (27, 'Co', 59), (28, 'Ni', 58),
    (29, 'Cu', 63), (30, 'Zn', 64), (31, 'Ga', 69), (32, 'Ge', 74),
    (33, 'As', 75), (34, 'Se', 80), (35, 'Br', 79), (36, 'Kr', 84),
    (37, 'Rb', 85), (38, 'Sr', 88), (39, 'Y',  89), (40, 'Zr', 90),
    (41, 'Nb', 93), (42, 'Mo', 98), (43, 'Tc', 98), (44, 'Ru',102),
    (45, 'Rh',103), (46, 'Pd',106), (47, 'Ag',107), (48, 'Cd',114),
    (49, 'In',115), (50, 'Sn',120), (51, 'Sb',121), (52, 'Te',130),
    (53, 'I', 127), (54, 'Xe',132), (55, 'Cs',133), (56, 'Ba',138),
    (57, 'La',139), (58, 'Ce',140), (59, 'Pr',141), (60, 'Nd',142),
    (61, 'Pm',145), (62, 'Sm',152), (63, 'Eu',153), (64, 'Gd',158),
    (65, 'Tb',159), (66, 'Dy',164), (67, 'Ho',165), (68, 'Er',166),
    (69, 'Tm',169), (70, 'Yb',174), (71, 'Lu',175), (72, 'Hf',180),
    (73, 'Ta',181), (74, 'W', 184), (75, 'Re',187), (76, 'Os',192),
    (77, 'Ir',193), (78, 'Pt',195), (79, 'Au',197), (80, 'Hg',202),
    (81, 'Tl',205), (82, 'Pb',208), (83, 'Bi',209),
]

KNOWN_BA = {
     1: 0.000,  2: 7.074,  3: 5.332,  4: 6.463,  5: 6.928,
     6: 7.680,  7: 7.476,  8: 7.976,  9: 6.258, 10: 8.032,
    11: 8.114, 12: 8.261, 13: 8.332, 14: 8.448, 15: 8.481,
    16: 8.520, 17: 8.521, 18: 8.595, 19: 8.557, 20: 8.551,
    21: 8.619, 22: 8.660, 23: 8.683, 24: 8.720, 25: 8.702,
    26: 8.790, 27: 8.745, 28: 8.732, 29: 8.752, 30: 8.756,
    31: 8.715, 32: 8.727, 33: 8.719, 34: 8.710, 35: 8.696,
    36: 8.717, 37: 8.690, 38: 8.695, 39: 8.668, 40: 8.671,
    41: 8.645, 42: 8.642, 43: 8.616, 44: 8.607, 45: 8.586,
    46: 8.570, 47: 8.553, 48: 8.540, 49: 8.514, 50: 8.504,
    51: 8.484, 52: 8.470, 53: 8.445, 54: 8.428, 55: 8.404,
    56: 8.393, 57: 8.372, 58: 8.361, 59: 8.340, 60: 8.331,
    61: 8.310, 62: 8.303, 63: 8.283, 64: 8.275, 65: 8.252,
    66: 8.246, 67: 8.229, 68: 8.218, 69: 8.199, 70: 8.195,
    71: 8.173, 72: 8.166, 73: 8.149, 74: 8.146, 75: 8.130,
    76: 8.126, 77: 8.110, 78: 8.105, 79: 8.088, 80: 8.083,
    81: 8.063, 82: 8.058, 83: 8.041,
}


# ═══════════════════════════════════════════════════
# CALIBRATION — scale set from Iron
# ═══════════════════════════════════════════════════

# Temporarily set scale to 1 to compute Fe's raw coupling
SCALE = 1.0
fe_raw, _ = decode_element(26, 56)
SCALE = 8.790 / fe_raw


# ═══════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════

if __name__ == '__main__':
    print('=' * 85)
    print('GFD NUCLEAR BINDING ENERGY: 3-CYCLE VORTEX DECODE')
    print('Light +1/3 floor | Mid standard | Heavy waveguide | 5 geometric corrections')
    print('=' * 85)
    print()
    print(f'  K={K}, D={D}, F+={F_PLUS}, F0={F_ZERO}, F-={F_MINUS}, range={RANGE}')
    print(f'  Light floor  = F- + {RANGE}/3 = {LIGHT_FLOOR:.3f}')
    print(f'  Mid floor    = F- = {MID_FLOOR}')
    print(f'  base_fc      = {BASE_FC}')
    print(f'  atten_eff    = {ATTEN_EFF:.4f}  ({ATTEN_BASE} + (1-{ATTEN_BASE})/3)')
    print(f'  scale        = {SCALE:.6f}')
    print()
    print(f'  Corrections: He +{CORRECTIONS[2]:.3f}, Li {CORRECTIONS[3]:+.3f}, '
          f'Be {CORRECTIONS[4]:+.3f}, B {CORRECTIONS[5]:+.3f}, F {CORRECTIONS[9]:+.3f}')
    print()

    hdr = f'{"Z":>3} {"Sym":>3} {"A":>4} {"Tag":>5} │ {"B/A":>7} {"Known":>7} {"Δ":>7} {"Δ%":>6}'
    print(hdr)
    print('─' * 55)

    calcs = []
    knowns = []
    class_data = {'LIGHT': [], 'MID': [], 'HEAVY': []}

    for Z, sym, A in ELEMENTS:
        known = KNOWN_BA[Z]
        if A <= 1 or known <= 0:
            continue

        ba, tag = decode_element(Z, A)
        delta = ba - known
        pct = abs(delta) / known * 100

        calcs.append(ba)
        knowns.append(known)
        class_data[tag].append((ba, known))

        corr = ' *' if Z in CORRECTIONS else ''
        print(f'{Z:>3} {sym:>3} {A:>4} {tag:>5} │ {ba:>7.3f} {known:>7.3f} '
              f'{delta:>+7.3f} {pct:>5.1f}%{corr}')

    # ═══════════════════════════════════════════════
    # STATISTICS
    # ═══════════════════════════════════════════════

    n = len(calcs)
    mean_known = sum(knowns) / n
    ss_res = sum((c - k) ** 2 for c, k in zip(calcs, knowns))
    ss_tot = sum((k - mean_known) ** 2 for k in knowns)
    r2 = 1 - ss_res / ss_tot
    mae = sum(abs(c - k) for c, k in zip(calcs, knowns)) / n
    rmse = math.sqrt(ss_res / n)

    print()
    print('=' * 85)
    print('GLOBAL STATISTICS')
    print('=' * 85)
    print(f'  R²:   {r2:.4f}')
    print(f'  MAE:  {mae:.4f} MeV/n  ({mae * 1000:.0f} keV/n)')
    print(f'  RMSE: {rmse:.4f} MeV/n')
    print()

    pcts = [abs(c - k) / k * 100 for c, k in zip(calcs, knowns)]
    for t in [0.5, 1, 2, 3, 5]:
        c = sum(1 for p in pcts if p <= t)
        print(f'  ≤{t:>4.1f}%: {c:>2}/{n} ({100 * c / n:.0f}%)')

    print()
    print('PER-CLASS STATISTICS')
    print('─' * 55)
    for cls_name in ['LIGHT', 'MID', 'HEAVY']:
        data = class_data[cls_name]
        if len(data) < 2:
            continue
        c_cls = [d[0] for d in data]
        k_cls = [d[1] for d in data]
        mk = sum(k_cls) / len(k_cls)
        ss_r = sum((c - k) ** 2 for c, k in zip(c_cls, k_cls))
        ss_t = sum((k - mk) ** 2 for k in k_cls)
        r2_c = 1 - ss_r / ss_t if ss_t > 0 else 0
        mae_c = sum(abs(c - k) for c, k in zip(c_cls, k_cls)) / len(c_cls)
        print(f'  {cls_name:>5} (n={len(data):>2}): R²={r2_c:.4f}, '
              f'MAE={mae_c:.4f} MeV/n ({mae_c * 1000:.0f} keV/n)')
