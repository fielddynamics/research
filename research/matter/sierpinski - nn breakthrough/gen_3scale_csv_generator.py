#!/usr/bin/env python3
"""
Generate 3-scale Sierpiński vectors for each element.

From the 256-dim walk vector, produce:
  - Vec256:   256-dim binary string (subchannel input, NN3)
  - 64-dim:   256 grouped into 64 groups of 4 → fill ratio (channel input, NN2)
  - 16-dim:   256 grouped into 16 groups of 16 → fill ratio (face input, NN1)

The grouping is consecutive chunking of the 256 vector:
  - Groups of 4:  [0:4], [4:8], ..., [252:256]  → 64 values
                   = 16 channels × 4 shells, each channel's 4 subchannels
  - Groups of 16: [0:16], [16:32], ..., [240:256] → 16 values
                   = 4 faces × 4 shells, each face's 16 positions

This PRESERVES shell structure. Shell 0 channels are groups 0-15,
shell 1 channels are groups 16-31, etc.

Fill ratio = sum of group / group size → 0.0 to 1.0
"""

import csv

ELEMENTS = [
    (1,'H',1),(2,'He',4),(3,'Li',7),(4,'Be',9),(5,'B',11),(6,'C',12),
    (7,'N',14),(8,'O',16),(9,'F',19),(10,'Ne',20),(11,'Na',23),(12,'Mg',24),
    (13,'Al',27),(14,'Si',28),(15,'P',31),(16,'S',32),(17,'Cl',35),(18,'Ar',40),
    (19,'K',39),(20,'Ca',40),(21,'Sc',45),(22,'Ti',48),(23,'V',51),(24,'Cr',52),
    (25,'Mn',55),(26,'Fe',56),(27,'Co',59),(28,'Ni',58),(29,'Cu',63),(30,'Zn',64),
    (31,'Ga',69),(32,'Ge',74),(33,'As',75),(34,'Se',80),(35,'Br',79),(36,'Kr',84),
    (37,'Rb',85),(38,'Sr',88),(39,'Y',89),(40,'Zr',90),(41,'Nb',93),(42,'Mo',98),
    (43,'Tc',98),(44,'Ru',102),(45,'Rh',103),(46,'Pd',106),(47,'Ag',107),
    (48,'Cd',114),(49,'In',115),(50,'Sn',120),(51,'Sb',121),(52,'Te',130),
    (53,'I',127),(54,'Xe',132),(55,'Cs',133),(56,'Ba',138),(57,'La',139),
    (58,'Ce',140),(59,'Pr',141),(60,'Nd',142),(61,'Pm',145),(62,'Sm',152),
    (63,'Eu',153),(64,'Gd',158),(65,'Tb',159),(66,'Dy',164),(67,'Ho',165),
    (68,'Er',166),(69,'Tm',169),(70,'Yb',174),(71,'Lu',175),(72,'Hf',180),
    (73,'Ta',181),(74,'W',184),(75,'Re',187),(76,'Os',192),(77,'Ir',193),
    (78,'Pt',195),(79,'Au',197),(80,'Hg',202),(81,'Tl',205),(82,'Pb',208),
    (83,'Bi',209),
]

KNOWN_BA = {
    1:0.000,2:7.074,3:5.332,4:6.463,5:6.928,6:7.680,7:7.476,8:7.976,
    9:6.258,10:8.032,11:8.114,12:8.261,13:8.332,14:8.448,15:8.481,16:8.520,
    17:8.521,18:8.595,19:8.557,20:8.551,21:8.619,22:8.660,23:8.683,24:8.720,
    25:8.702,26:8.790,27:8.745,28:8.732,29:8.752,30:8.756,31:8.715,32:8.727,
    33:8.719,34:8.710,35:8.696,36:8.717,37:8.690,38:8.695,39:8.668,40:8.671,
    41:8.645,42:8.642,43:8.616,44:8.607,45:8.586,46:8.570,47:8.553,48:8.540,
    49:8.514,50:8.504,51:8.484,52:8.470,53:8.445,54:8.428,55:8.404,56:8.393,
    57:8.372,58:8.361,59:8.340,60:8.331,61:8.310,62:8.303,63:8.283,64:8.275,
    65:8.252,66:8.246,67:8.229,68:8.218,69:8.199,70:8.195,71:8.173,72:8.166,
    73:8.149,74:8.146,75:8.130,76:8.126,77:8.110,78:8.105,79:8.088,80:8.083,
    81:8.063,82:8.058,83:8.041,
}

def build_256(A):
    """Build 256-dim binary fill vector."""
    a64 = A % 64 if A > 64 else A
    if a64 == 0: a64 = 64
    nc = (A - a64) // 64
    total_filled = nc * 64 + a64
    return [1 if i < total_filled else 0 for i in range(256)]


def build_vectors(v256):
    """
    From 256-dim vector, build:
      - chan64: 64 groups of 4 consecutive → fill ratio
      - face16: 16 groups of 16 consecutive → fill ratio

    256 layout: [shell0: 64 pos][shell1: 64 pos][shell2: 64 pos][shell3: 64 pos]
    Within each shell: pos = fi*16 + ci*4 + si

    Channel groups of 4:
      Group 0:  v256[0:4]     = shell0, F0.C0 (4 subchannels)
      Group 1:  v256[4:8]     = shell0, F0.C1
      ...
      Group 15: v256[60:64]   = shell0, F3.C3
      Group 16: v256[64:68]   = shell1, F0.C0
      ...
      Group 63: v256[252:256] = shell3, F3.C3

    Face groups of 16:
      Group 0:  v256[0:16]    = shell0, Face 0 (4 channels × 4 subs)
      Group 1:  v256[16:32]   = shell0, Face 1
      Group 2:  v256[32:48]   = shell0, Face 2
      Group 3:  v256[48:64]   = shell0, Face 3
      Group 4:  v256[64:80]   = shell1, Face 0
      ...
      Group 15: v256[240:256] = shell3, Face 3
    """

    # Channel (64-dim): consecutive groups of 4
    chan64 = []
    for g in range(64):
        start = g * 4
        total = sum(v256[start:start + 4])
        chan64.append(total / 4.0)

    # Face (16-dim): consecutive groups of 16
    face16 = []
    for g in range(16):
        start = g * 16
        total = sum(v256[start:start + 16])
        face16.append(total / 16.0)

    return face16, chan64


out = '/mnt/user-data/outputs/gfd_3scale_vectors.csv'
with open(out, 'w', newline='') as f:
    w = csv.writer(f)
    header = (
        ['Sym', 'A', 'BA_MeV', 'Shell', 'Vec256'] +
        [f'face_{i}' for i in range(16)] +
        [f'chan_{i}' for i in range(64)]
    )
    w.writerow(header)

    for Z, sym, A in ELEMENTS:
        ba = KNOWN_BA[Z]
        if A <= 1 or ba <= 0:
            continue

        v256 = build_256(A)
        face16, chan64 = build_vectors(v256)

        a64 = A % 64 if A > 64 else A
        if a64 == 0: a64 = 64
        nc = (A - a64) // 64

        vec256_str = ''.join(str(b) for b in v256)

        w.writerow(
            [sym, A, f'{ba:.3f}', nc, vec256_str] +
            [f'{v:.4f}' for v in face16] +
            [f'{v:.4f}' for v in chan64]
        )

print(f"Written {out}")

# ═══════════════════════════════════════════════════
# VERIFICATION
# ═══════════════════════════════════════════════════

print("\n" + "=" * 70)
print("  VERIFICATION")
print("=" * 70)

test_cases = [
    (2,  'He', 4),
    (6,  'C',  12),
    (26, 'Fe', 56),
    (30, 'Zn', 64),
    (31, 'Ga', 69),
    (76, 'Os', 192),
    (83, 'Bi', 209),
]

for Z, sym, A in test_cases:
    v256 = build_256(A)
    face16, chan64 = build_vectors(v256)
    ba = KNOWN_BA[Z]
    a64 = A % 64 if A > 64 else A
    if a64 == 0: a64 = 64
    nc = (A - a64) // 64

    print(f"\n  {sym} (A={A}, shell={nc}, a64={a64}, B/A={ba:.3f}):")
    print(f"    Vec256: {sum(v256)} ones / 256")

    # Face: 16 values = 4 faces × 4 shells
    print(f"    Face (16-dim) = 4 shells × 4 faces:")
    for s in range(4):
        vals = face16[s * 4:(s + 1) * 4]
        if any(v > 0 for v in vals):
            print(f"      Shell {s}: F0={vals[0]:.3f}  F1={vals[1]:.3f}  F2={vals[2]:.3f}  F3={vals[3]:.3f}")

    # Channel: 64 values = 4 shells × 16 channels
    print(f"    Chan (64-dim) = 4 shells × 16 channels:")
    for s in range(4):
        vals = chan64[s * 16:(s + 1) * 16]
        if any(v > 0 for v in vals):
            nonzero = sum(1 for v in vals if v > 0)
            partial = sum(1 for v in vals if 0 < v < 1)
            full = sum(1 for v in vals if v == 1)
            print(f"      Shell {s}: {nonzero}/16 active ({full} full, {partial} partial)")

    # Cross-check: each face value = mean of its 4 channel values
    ok = True
    for g in range(16):
        face_val = face16[g]
        ch_start = g * 4
        ch_mean = sum(chan64[ch_start:ch_start + 4]) / 4.0
        if abs(face_val - ch_mean) > 1e-10:
            print(f"    MISMATCH face group {g}: face={face_val:.4f} vs chan_mean={ch_mean:.4f}")
            ok = False
    if ok:
        print(f"    Cross-check: all 16 face groups = mean of their 4 channels ✓")
