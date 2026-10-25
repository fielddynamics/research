#!/usr/bin/env python3
"""
Nuclear Binding Energy Pipeline
================================
Step-by-step implementation of the SST quadratic binding energy construction.

Each function maps directly to a step in nuclear_binding_pipeline.md.
Run this script to reproduce every number in the pipeline document.

Inputs:
  - mu_SST(x) = [(2x+1) - sqrt(4x+1)] / 2x
  - K = 4, D = 3, K^D = 64
  - B/A(Zn-64) = 8.756 MeV

Outputs:
  - Magic numbers: 2, 8, 20, 28, 50, 82, 126
  - Binding energy curve from He to Pb at MAE = 95 keV
  - Ceiling sequence governed by mu_SST(2) = 1/2

Stephen Nelson — Gravity Field Dynamics
"""

import math

# =====================================================================
# INPUTS
# =====================================================================

K = 4       # branching factor
D = 3       # depth
KD = K**D   # 64 positions per face

BA_ZN = 8.756  # B/A(Zn-64) in MeV — the single calibration point


def mu_sst(x):
    """SST quadratic: bound-state constitutive law.

    The self-consistent solution of x(1-mu)^2 = mu.
    Physical root satisfying 0 < mu < 1 for x > 0.
    """
    if x <= 0:
        return 0.0
    return ((2*x + 1) - math.sqrt(4*x + 1)) / (2*x)


# =====================================================================
# STEP 1: THE COUPLING SUM
# =====================================================================

def coupling_sum(A):
    """Sum of mu_SST(i^2) from i=1 to A.

    Each walk position i contributes mu_SST(i^2) to the collective binding.
    x = i^2 maps position to acceleration ratio (Jacobian: dx = 2i di).
    """
    return sum(mu_sst(i*i) for i in range(1, A + 1))


# Face maximum: sum over all 64 positions
SUM_KD = coupling_sum(KD)  # 59.928

print("=" * 70)
print("STEP 1: Coupling sum")
print("=" * 70)
print(f"  SUM_KD = sum(mu_SST(i^2), i=1..64) = {SUM_KD:.4f}")
print(f"  Individual values:")
for i in [1, 2, 4, 8, 16, 32, 64]:
    print(f"    mu_SST({i}^2) = mu_SST({i*i}) = {mu_sst(i*i):.6f}")


# =====================================================================
# STEP 2: THE RISING CURVE (SST_1)
# =====================================================================

def sst_curve(A):
    """Rising SST curve: B/A(Zn) * (K^D / A) * (sum_A / sum_KD).

    Three terms:
      B/A(Zn)          — energy scale (MeV)
      K^D / A          — sharing factor (64 positions among A nucleons)
      sum_A / sum_KD   — coupling fraction (how full is the face)

    At A = 64, both ratios = 1 and the result = B/A(Zn) by construction.
    """
    if A < 1:
        return 0.0
    sum_A = coupling_sum(A)
    return BA_ZN * (KD / A) * (sum_A / SUM_KD)


def sst_local(n):
    """SST curve for a walk restarted from position 1, covering n positions.

    Identical to sst_curve(n) — a fresh walk always starts from position 1.
    Named separately for clarity when used in sector-crossing reflections.
    """
    return sst_curve(n)


print(f"\n{'=' * 70}")
print("STEP 2: Rising curve (SST_1)")
print("=" * 70)
print(f"  SST_1(A) = B/A(Zn) * (K^D / A) * (sum_A / sum_KD)")
print(f"")
test_A = [4, 12, 28, 56, 64, 100, 128, 192, 208]
for A in test_A:
    sum_A = coupling_sum(A)
    frac = sum_A / SUM_KD
    share = KD / A
    val = sst_curve(A)
    print(f"  A={A:>3}:  sum={sum_A:>7.3f}  frac={frac:.4f}  "
          f"share={share:.4f}  SST_1 = {val:.4f} MeV")


# =====================================================================
# STEP 5: CEILING SEQUENCE (computed before Step 4 for use there)
# =====================================================================

# One formula for every ceiling:
#   CEIL = BA_ZN + prev - mu_SST(2) * (BA_ZN - prev)
# where prev = B/A at the sector boundary from all previously established sectors.

MU_HALF = mu_sst(2)  # exactly 0.5


def ceiling(prev):
    """Unified ceiling formula. Applied identically at every sector boundary.

    CEIL = B/A(Zn) + prev - mu_SST(2) * [B/A(Zn) - prev]

    prev = B/A at the sector boundary from all previously established sectors.
    mu_SST(2) = 1/2 is the bound-state field origin.
    """
    return BA_ZN + prev - MU_HALF * (BA_ZN - prev)


# CEIL_1: sector 0 just filled. prev = B/A(Zn) = 8.756 (no prior sector, no impedance)
prev_1 = BA_ZN
CEIL_1 = ceiling(prev_1)

# CEIL_2: sector 0 established. prev = SST_1_inv(128) from sector 0
sst1_inv_128 = CEIL_1 - sst_curve(128)
prev_2 = sst1_inv_128
CEIL_2 = ceiling(prev_2)

# CEIL_3: sectors 0+1 established. prev = envelope at A=128 updated by sector 1
#   SST_2_inv(128) = CEIL_2 - sst_local(64) = CEIL_2 - BA_ZN
sst2_inv_128 = CEIL_2 - BA_ZN
prev_3 = min(sst1_inv_128, sst2_inv_128)  # sector 1 has taken over
CEIL_3 = ceiling(prev_3)

# Base gap (for reference)
delta = CEIL_1 - CEIL_2

print(f"\n{'=' * 70}")
print("STEP 5: Ceiling sequence")
print("=" * 70)
print(f"  One formula: CEIL = B/A(Zn) + prev - mu_SST(2) * [B/A(Zn) - prev]")
print(f"  mu_SST(2) = {MU_HALF:.4f} (bound-state field origin)")
print(f"")
print(f"  Sector 0:")
print(f"    prev = B/A(Zn) = {prev_1:.4f} MeV  (no prior sector, no impedance)")
print(f"    correction = mu_SST(2) * [{BA_ZN:.3f} - {prev_1:.3f}] = {MU_HALF} * {BA_ZN - prev_1:.4f} = {MU_HALF*(BA_ZN - prev_1):.4f}")
print(f"    CEIL_1 = {BA_ZN:.3f} + {prev_1:.3f} - {MU_HALF*(BA_ZN - prev_1):.3f} = {CEIL_1:.4f} MeV")
print(f"")
print(f"  Sector 1:")
print(f"    SST_1(128)     = {sst_curve(128):.4f} MeV")
print(f"    prev = SST_1_inv(128) = {CEIL_1:.3f} - {sst_curve(128):.3f} = {prev_2:.4f} MeV")
print(f"    correction = mu_SST(2) * [{BA_ZN:.3f} - {prev_2:.3f}] = {MU_HALF} * {BA_ZN - prev_2:.4f} = {MU_HALF*(BA_ZN - prev_2):.4f}")
print(f"    CEIL_2 = {BA_ZN:.3f} + {prev_2:.3f} - {MU_HALF*(BA_ZN - prev_2):.3f} = {CEIL_2:.4f} MeV")
print(f"")
print(f"  Sector 2:")
print(f"    SST_2_inv(128) = CEIL_2 - B/A(Zn) = {CEIL_2:.3f} - {BA_ZN:.3f} = {sst2_inv_128:.4f} MeV")
print(f"    prev = min({sst1_inv_128:.4f}, {sst2_inv_128:.4f}) = {prev_3:.4f} MeV  (sector 1 has taken over)")
print(f"    correction = mu_SST(2) * [{BA_ZN:.3f} - {prev_3:.3f}] = {MU_HALF} * {BA_ZN - prev_3:.4f} = {MU_HALF*(BA_ZN - prev_3):.4f}")
print(f"    CEIL_3 = {BA_ZN:.3f} + {prev_3:.3f} - {MU_HALF*(BA_ZN - prev_3):.3f} = {CEIL_3:.4f} MeV")
print(f"")
print(f"  Summary:")
print(f"  {'Sector':<8} {'prev (MeV)':>12} {'Correction':>12} {'Ceiling (MeV)':>14}")
print(f"  {'0':<8} {prev_1:>12.4f} {MU_HALF*(BA_ZN-prev_1):>12.4f} {CEIL_1:>14.4f}  (no impedance)")
print(f"  {'1':<8} {prev_2:>12.4f} {MU_HALF*(BA_ZN-prev_2):>12.4f} {CEIL_2:>14.4f}")
print(f"  {'2':<8} {prev_3:>12.4f} {MU_HALF*(BA_ZN-prev_3):>12.4f} {CEIL_3:>14.4f}")


# =====================================================================
# STEP 4: FACE-BY-FACE CONSTRUCTION
# =====================================================================

def sst1(A):
    """Sector 0: rising curve."""
    return sst_curve(A)


def sst1_inv(A):
    """Sector 0: inverse (reflection from CEIL_1)."""
    return CEIL_1 - sst_curve(A)


def sst2_inv(A):
    """Sector 1: inverse (reflection from CEIL_2, walk restarts at A=64)."""
    if A <= 64:
        return float('inf')
    return CEIL_2 - sst_local(A - 64)


def sst3_inv(A):
    """Sector 2: inverse (reflection from CEIL_3, walk restarts at A=128)."""
    if A <= 128:
        return float('inf')
    return CEIL_3 - sst_local(A - 128)


print(f"\n{'=' * 70}")
print("STEP 4: Sector-by-sector construction")
print("=" * 70)
print(f"  {'A':>5}  {'SST_1':>8}  {'SST1inv':>8}  {'SST2inv':>8}  {'SST3inv':>8}  {'governs':>10}")
for A in [32, 56, 64, 80, 100, 110, 128, 150, 192, 208]:
    s1 = sst1(A)
    s1i = sst1_inv(A)
    s2i = sst2_inv(A)
    s3i = sst3_inv(A)
    vals = {'SST_1': s1, 'SST1inv': s1i}
    if A > 64:
        vals['SST2inv'] = s2i
    if A > 128:
        vals['SST3inv'] = s3i
    gov = min(vals, key=vals.get)
    s2i_str = f"{s2i:8.4f}" if A > 64 else "     n/a"
    s3i_str = f"{s3i:8.4f}" if A > 128 else "     n/a"
    print(f"  {A:>5}  {s1:8.4f}  {s1i:8.4f}  {s2i_str}  {s3i_str}  {gov:>10}")


# =====================================================================
# STEP 6: THE ENVELOPE
# =====================================================================

def envelope(A):
    """Predicted B/A: minimum of all active curves at mass number A."""
    vals = [sst1(A), sst1_inv(A)]
    if A > 64:
        vals.append(sst2_inv(A))
    if A > 128:
        vals.append(sst3_inv(A))
    return min(vals)


print(f"\n{'=' * 70}")
print("STEP 6: Envelope (predicted B/A)")
print("=" * 70)
print(f"  B/A(A) = min(SST_1, SST_1_inv, SST_2_inv, SST_3_inv)")
print(f"")
for A in [4, 12, 28, 56, 64, 80, 100, 120, 128, 150, 192, 208]:
    print(f"  A={A:>3}:  B/A = {envelope(A):.4f} MeV")


# =====================================================================
# STEP 7: VERIFICATION
# =====================================================================

# AME2020 data — most abundant stable isotope per element
AME = [
    ( 1,'H',    1, 0.000),( 2,'He',  4, 7.074),( 3,'Li',  7, 5.606),
    ( 4,'Be',  9, 6.463),( 5,'B',  11, 6.928),( 6,'C',  12, 7.680),
    ( 7,'N',  14, 7.476),( 8,'O',  16, 7.976),( 9,'F',  19, 7.779),
    (10,'Ne', 20, 8.032),(11,'Na', 23, 8.111),(12,'Mg', 24, 8.261),
    (13,'Al', 27, 8.332),(14,'Si', 28, 8.448),(15,'P',  31, 8.481),
    (16,'S',  32, 8.493),(17,'Cl', 35, 8.520),(18,'Ar', 40, 8.595),
    (19,'K',  39, 8.557),(20,'Ca', 40, 8.551),(21,'Sc', 45, 8.619),
    (22,'Ti', 48, 8.723),(23,'V',  51, 8.742),(24,'Cr', 52, 8.776),
    (25,'Mn', 55, 8.765),(26,'Fe', 56, 8.790),(27,'Co', 59, 8.768),
    (28,'Ni', 58, 8.732),(29,'Cu', 63, 8.752),(30,'Zn', 64, 8.756),
    (31,'Ga', 69, 8.724),(32,'Ge', 74, 8.713),(33,'As', 75, 8.701),
    (34,'Se', 80, 8.711),(35,'Br', 79, 8.696),(36,'Kr', 84, 8.717),
    (37,'Rb', 85, 8.697),(38,'Sr', 88, 8.733),(39,'Y',  89, 8.714),
    (40,'Zr', 90, 8.710),(41,'Nb', 93, 8.664),(42,'Mo', 98, 8.635),
    (43,'Tc', 98, 8.610),(44,'Ru',102, 8.607),(45,'Rh',103, 8.584),
    (46,'Pd',106, 8.567),(47,'Ag',107, 8.554),(48,'Cd',114, 8.539),
    (49,'In',115, 8.516),(50,'Sn',120, 8.505),(51,'Sb',121, 8.482),
    (52,'Te',128, 8.399),(53,'I', 127, 8.445),(54,'Xe',132, 8.438),
    (55,'Cs',133, 8.410),(56,'Ba',138, 8.394),(57,'La',139, 8.378),
    (58,'Ce',140, 8.376),(59,'Pr',141, 8.354),(60,'Nd',142, 8.346),
    (61,'Pm',145, 8.318),(62,'Sm',152, 8.304),(63,'Eu',153, 8.278),
    (64,'Gd',158, 8.272),(65,'Tb',159, 8.253),(66,'Dy',164, 8.247),
    (67,'Ho',165, 8.231),(68,'Er',166, 8.226),(69,'Tm',169, 8.210),
    (70,'Yb',174, 8.206),(71,'Lu',175, 8.192),(72,'Hf',180, 8.189),
    (73,'Ta',181, 8.178),(74,'W', 184, 8.178),(75,'Re',187, 8.168),
    (76,'Os',192, 8.167),(77,'Ir',193, 8.155),(78,'Pt',195, 8.150),
    (79,'Au',197, 8.140),(80,'Hg',202, 8.135),(81,'Tl',205, 8.120),
    (82,'Pb',208, 8.120),
]

print(f"\n{'=' * 70}")
print("STEP 7: Verification against AME2020")
print("=" * 70)

# Closure points
print(f"\n  Closure point accuracy:")
print(f"  {'Point':<12} {'Element':<8} {'Predicted':>10} {'Exper.':>10} {'Residual':>10}")
closure_points = [(64, 'Zn-64', 8.756), (128, 'Te-128', 8.399), (192, 'Os-192', 8.167)]
for A, name, exp in closure_points:
    pred = envelope(A)
    res = abs(pred - exp) * 1000
    label = 'calib' if A == 64 else ''
    print(f"  K^D*{A//64:<5}={A:<4} {name:<8} {pred:>10.4f} {exp:>10.4f} {res:>8.1f} keV  {label}")

# Element-by-element
print(f"\n  Element-by-element (selected):")
print(f"  {'Z':>3} {'El':<3} {'A':>4}  {'Predicted':>10} {'Exper.':>10} {'Residual':>10}")
selected_Z = [2, 6, 8, 14, 26, 28, 30, 50, 52, 56, 76, 82]
for Z, sym, A, ba_exp in AME:
    if Z in selected_Z and ba_exp > 0:
        pred = envelope(A)
        res = (pred - ba_exp) * 1000
        print(f"  {Z:>3} {sym:<3} {A:>4}  {pred:>10.4f} {ba_exp:>10.4f} {res:>+8.1f} keV")

# Global statistics
print(f"\n  Global statistics:")
n_total = 0
sum_sq = 0.0
sum_abs = 0.0
sum_exp = 0.0
sum_exp_sq = 0.0
ba_mean = 0.0

# First pass: compute mean
data = [(A, ba) for _, _, A, ba in AME if ba > 0]
ba_mean = sum(ba for _, ba in data) / len(data)

for A, ba_exp in data:
    pred = envelope(A)
    err = pred - ba_exp
    sum_sq += err**2
    sum_abs += abs(err)
    sum_exp_sq += (ba_exp - ba_mean)**2
    n_total += 1

mae = sum_abs / n_total * 1000
r2 = 1 - sum_sq / sum_exp_sq

# By region
n_r1 = 0; ss_r1 = 0; sa_r1 = 0; se_r1 = 0
n_post = 0; ss_post = 0; sa_post = 0; se_post = 0

data_r1 = [(A, ba) for A, ba in data if 12 <= A <= 64]
data_post = [(A, ba) for A, ba in data if A > 64]

mean_r1 = sum(ba for _, ba in data_r1) / len(data_r1)
mean_post = sum(ba for _, ba in data_post) / len(data_post)

for A, ba_exp in data_r1:
    err = envelope(A) - ba_exp
    ss_r1 += err**2
    sa_r1 += abs(err)
    se_r1 += (ba_exp - mean_r1)**2
    n_r1 += 1

for A, ba_exp in data_post:
    err = envelope(A) - ba_exp
    ss_post += err**2
    sa_post += abs(err)
    se_post += (ba_exp - mean_post)**2
    n_post += 1

mae_r1 = sa_r1 / n_r1 * 1000
r2_r1 = 1 - ss_r1 / se_r1
mae_post = sa_post / n_post * 1000
r2_post = 1 - ss_post / se_post

print(f"  {'Region':<20} {'R²':>8} {'MAE (keV)':>10} {'N':>5}")
print(f"  {'Round 1 (A<=64)':<20} {r2_r1:>8.4f} {mae_r1:>10.0f} {n_r1:>5}")
print(f"  {'Post-64 (A>64)':<20} {r2_post:>8.4f} {mae_post:>10.0f} {n_post:>5}")
print(f"  {'Full (A=4-208)':<20} {r2:>8.4f} {mae:>10.0f} {n_total:>5}")


# =====================================================================
# MAGIC NUMBERS (from the packing algebra)
# =====================================================================

def T(n):
    """Tetrahedral number: cumulative position count for K-fold branching."""
    return n * (n + 1) * (n + 2) // 6


def G(n):
    """Gate exclusion: positions removed at the gate face boundary.
    The gate face is the K-th face; it first contributes at shell n = K."""
    if n < K:
        return 0
    return (n - 1) * n // 2


def M(n):
    """Cumulative shell closure. Factor of 2 for proton/neutron orientations."""
    return 2 * (T(n) - G(n))


print(f"\n{'=' * 70}")
print("MAGIC NUMBERS: Packing algebra")
print("=" * 70)
print(f"  T(n) = n(n+1)(n+2)/6    (tetrahedral number)")
print(f"  G(n) = (n-1)n/2 for n>=K, else 0    (gate exclusion)")
print(f"  M(n) = 2[T(n) - G(n)]   (cumulative shell closure)")
print(f"")
print(f"  {'n':>3}  {'T(n)':>6}  {'G(n)':>6}  {'M(n)':>6}  {'Capacity':>10}  {'Magic?':>8}")

observed_magic = {2, 8, 20, 28, 50, 82, 126}
prev_M = 0
for n in range(1, 8):
    m = M(n)
    cap = m - prev_M
    is_magic = "YES" if m in observed_magic else "no"
    print(f"  {n:>3}  {T(n):>6}  {G(n):>6}  {m:>6}  {cap:>10}  {is_magic:>8}")
    prev_M = m

all_match = all(M(n) in observed_magic for n in range(1, 8))
print(f"\n  All seven magic numbers reproduced: {all_match}")
print(f"  Gate activates at n = K = {K}: capacity drops from 12 to 8")
print(f"  This is the 20 -> 28 gap, without spin-orbit coupling.")


# =====================================================================
# SUMMARY
# =====================================================================

print(f"\n{'=' * 70}")
print("SUMMARY")
print("=" * 70)
print(f"""
  Inputs:
    mu_SST(x) = [(2x+1) - sqrt(4x+1)] / 2x
    K = {K}, D = {D}, K^D = {KD}
    B/A(Zn-64) = {BA_ZN} MeV

  Ceilings (one formula: CEIL = B/A(Zn) + prev - mu_SST(2) * [B/A(Zn) - prev]):
    CEIL_1 = {CEIL_1:.4f} MeV  (prev = {prev_1:.4f}, no impedance)
    CEIL_2 = {CEIL_2:.4f} MeV  (prev = {prev_2:.4f}, correction = {MU_HALF*(BA_ZN-prev_2):.4f})
    CEIL_3 = {CEIL_3:.4f} MeV  (prev = {prev_3:.4f}, correction = {MU_HALF*(BA_ZN-prev_3):.4f})

  Accuracy:
    Full range (He to Pb): R² = {r2:.4f}, MAE = {mae:.0f} keV
    Round 1 (A <= 64):     R² = {r2_r1:.4f}, MAE = {mae_r1:.0f} keV
    Post-64 (A > 64):      R² = {r2_post:.4f}, MAE = {mae_post:.0f} keV

  Magic numbers: {', '.join(str(M(n)) for n in range(1, 8))}
    All seven reproduced exactly. Zero spin-orbit coupling.

  One equation. One calibration point. One hierarchy.
""")
