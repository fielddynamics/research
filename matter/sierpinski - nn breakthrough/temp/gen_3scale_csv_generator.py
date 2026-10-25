#!/usr/bin/env python3
"""
Generate 3-scale Sierpiński vectors for each element.
Uses periodictable library for binding energy data.

python -m pip install periodictable
"""

import csv
import periodictable

U_TO_MEV = 931.494
M_H = 1.00782503207
M_N = 1.00866491588

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


def get_ba(Z, A):
    """Get BE/A in MeV from periodictable isotope mass."""
    el = periodictable.elements[Z]
    iso = el[A]
    if iso.mass is None:
        return None
    N = A - Z
    BE = (Z * M_H + N * M_N - iso.mass) * U_TO_MEV
    return BE / A


def build_256(A):
    """Build 256-dim binary fill vector."""
    a64 = A % 64 if A > 64 else A
    if a64 == 0:
        a64 = 64
    nc = (A - a64) // 64
    total_filled = nc * 64 + a64
    return [1 if i < total_filled else 0 for i in range(256)]


def build_vectors(v256):
    """
    From 256-dim vector, build:
      - chan64: 64 groups of 4 consecutive → fill ratio
      - face16: 16 groups of 16 consecutive → fill ratio
    """
    chan64 = []
    for g in range(64):
        start = g * 4
        total = sum(v256[start:start + 4])
        chan64.append(total / 4.0)

    face16 = []
    for g in range(16):
        start = g * 16
        total = sum(v256[start:start + 16])
        face16.append(total / 16.0)

    return face16, chan64


out = 'gfd_3scale_vectors.csv'
with open(out, 'w', newline='') as f:
    w = csv.writer(f)
    header = (
        ['Sym', 'A', 'BA_MeV', 'Shell', 'Vec256'] +
        [f'face_{i}' for i in range(16)] +
        [f'chan_{i}' for i in range(64)]
    )
    w.writerow(header)

    for Z, sym, A in ELEMENTS:
        ba = get_ba(Z, A)
        if ba is None or ba <= 0:
            print(f"  SKIP {sym} (Z={Z}, A={A}): no mass data")
            continue

        v256 = build_256(A)
        face16, chan64 = build_vectors(v256)

        a64 = A % 64 if A > 64 else A
        if a64 == 0:
            a64 = 64
        nc = (A - a64) // 64

        vec256_str = ''.join(str(b) for b in v256)

        w.writerow(
            [sym, A, f'{ba:.4f}', nc, vec256_str] +
            [f'{v:.4f}' for v in face16] +
            [f'{v:.4f}' for v in chan64]
        )

        print(f"  {sym:>3} Z={Z:>2} A={A:>3}  BE/A = {ba:.4f} MeV")

print(f"\nWritten {out}")
