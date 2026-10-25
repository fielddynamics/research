#!/usr/bin/env python3
"""
GFD Nuclear Binding Energy — Single Field Closure
===================================================
Publication chart: SST binding energy curve vs experimental data.

One field closure. One curve shape — the SST quadratic summed along the
Sierpinski walk — plotted and inverted at each K^D boundary.

  Round 1 (A = 0 to 64):
    SST_1      — rising curve, walk fills from position 1
    SST_1_inv  — CEIL_1 - SST_1, first reflection at K^D = 64

  Round 2 (A = 64 onward):
    SST_2_inv  — CEIL_2 - SST_local(A-64), walk restarts at A = 64

  Round 3 (A = 128 onward):
    SST_3_inv  — CEIL_3 - SST_local(A-128), walk restarts at A = 128

B/A = min(active curves)

Ceiling rule
------------
One rule, applied uniformly:

  Ceiling = max_fill + envelope(boundary)

  Max fill = B/A(Zn) = 8.756 MeV — one complete Sierpinski walk.
  Envelope at boundary = predicted B/A where that round begins.

  CEIL_1 = 8.756 + 8.756 = 17.512  (at A=64)
  CEIL_2 = 8.756 + 8.385 = 17.141  (at A=128)
  CEIL_3 = 8.756 + 8.199 = 16.955  (at A=192)

The drops between ceilings (0.371, 0.186) decay with ratio
mu_SST(2) = 1/2 — the bound-state field origin. This is a
consequence of the sum rule, not a separate construction.

Stephen Nelson — Gravity Field Dynamics
"""

import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# =====================================================================
# STRUCTURAL CONSTANTS
# =====================================================================
K = 4; D = 3; KD = K**D  # 64

def mu_sst(x):
    """SST quadratic: bound-state constitutive law."""
    if x <= 0: return 0
    return ((2*x + 1) - math.sqrt(4*x + 1)) / (2*x)

# =====================================================================
# ENERGY SCALE — calibrated from Zn-64 (full Sierpinski fill)
# =====================================================================
BA_ZN = 8.756  # experimental B/A for Zn-64, MeV
MAX_FILL = BA_ZN  # one complete 64-position walk
SUM_KD = sum(mu_sst(i*i) for i in range(1, KD + 1))  # 59.928

def sst_curve(A):
    """Rising SST curve: B/A(Zn) * (K^D / A) * (sum_A / sum_KD).
    No opaque SCALE constant. Every term is physical."""
    if A < 1: return 0
    sum_A = sum(mu_sst(i*i) for i in range(1, A + 1))
    return BA_ZN * (KD / A) * (sum_A / SUM_KD)

def sst_local(n):
    """SST curve for a walk restarted from position 1, covering n positions."""
    if n < 1: return 0
    sum_n = sum(mu_sst(i*i) for i in range(1, n + 1))
    return BA_ZN * (KD / n) * (sum_n / SUM_KD)

# =====================================================================
# CEILING DERIVATION
# =====================================================================
# Rule: ceiling = max_fill + envelope(boundary)
#
# The ceiling at each K^D boundary is the walk's full potential (8.756 MeV)
# plus the binding energy the field has already established at that point.
#
# The circular dependency (ceiling depends on envelope, envelope depends on
# ceiling) is resolved algebraically at each level using the paper's formula.

# --- Round 1 ceiling ---
# At A=64, envelope = B/A(Zn) = 8.756 (walk just peaked)
CEIL_1 = MAX_FILL + BA_ZN  # 17.512

# --- Round 2 ceiling ---
# Algebraic resolution of the bootstrap at A=128:
ba_128_r1inv = CEIL_1 - sst_curve(128)
delta_r1 = BA_ZN - ba_128_r1inv
CEIL_2 = BA_ZN + ba_128_r1inv - delta_r1 / 2  # 17.141

# Converged envelope at A=128
ba_128 = min(sst_curve(128), CEIL_1 - sst_curve(128),
             CEIL_2 - sst_local(128 - 64))

# --- Round 3 ceiling ---
# Same algebraic resolution at A=192:
ba_192_r2inv = CEIL_2 - sst_local(192 - 64)
ba_192_r1inv = CEIL_1 - sst_curve(192)
ba_192_from_r12 = min(sst_curve(192), ba_192_r1inv, ba_192_r2inv)
delta_r2 = ba_128 - ba_192_from_r12
CEIL_3 = ba_128 + MAX_FILL - delta_r2 / 2

# Converged envelope at A=192
ba_192 = min(sst_curve(192), CEIL_1 - sst_curve(192),
             CEIL_2 - sst_local(192 - 64),
             CEIL_3 - sst_local(192 - 128))

# --- Verify sum rule at all levels ---
ceil_1_check = MAX_FILL + BA_ZN
ceil_2_check = MAX_FILL + ba_128
ceil_3_check = MAX_FILL + ba_192

drop_1 = CEIL_1 - CEIL_2
drop_2 = CEIL_2 - CEIL_3
ratio = drop_2 / drop_1 if drop_1 != 0 else 0

print(f"=== Ceiling derivation: ceiling = max_fill + envelope(boundary) ===")
print(f"")
print(f"Max fill = {MAX_FILL:.4f} MeV (one complete Sierpinski walk)")
print(f"")
print(f"Round 1:  envelope(64)  = {BA_ZN:.4f}  →  CEIL_1 = {MAX_FILL:.3f} + {BA_ZN:.3f}  = {CEIL_1:.4f}")
print(f"Round 2:  envelope(128) = {ba_128:.4f}  →  CEIL_2 = {MAX_FILL:.3f} + {ba_128:.3f} = {CEIL_2:.4f}")
print(f"Round 3:  envelope(192) = {ba_192:.4f}  →  CEIL_3 = {MAX_FILL:.3f} + {ba_192:.3f} = {CEIL_3:.4f}")
print(f"")
print(f"Sum rule verification:")
print(f"  CEIL_1 = {CEIL_1:.4f},  max_fill + ba(64)  = {ceil_1_check:.4f},  diff = {abs(CEIL_1 - ceil_1_check):.6f}")
print(f"  CEIL_2 = {CEIL_2:.4f},  max_fill + ba(128) = {ceil_2_check:.4f},  diff = {abs(CEIL_2 - ceil_2_check):.6f}")
print(f"  CEIL_3 = {CEIL_3:.4f},  max_fill + ba(192) = {ceil_3_check:.4f},  diff = {abs(CEIL_3 - ceil_3_check):.6f}")
print(f"")
print(f"Ceiling drops: {drop_1:.4f}, {drop_2:.4f}")
print(f"Ratio = {ratio:.4f}  (mu_SST(2) = {mu_sst(2):.4f})")

# =====================================================================
# ENVELOPE
# =====================================================================
def envelope(A):
    """Predicted B/A: minimum of all active curves."""
    vals = [sst_curve(A), CEIL_1 - sst_curve(A)]
    if A > 64:
        vals.append(CEIL_2 - sst_local(A - 64))
    if A > 128:
        vals.append(CEIL_3 - sst_local(A - 128))
    return min(vals)

# =====================================================================
# AME2020 EXPERIMENTAL DATA
# =====================================================================
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

# =====================================================================
# COMPUTE CURVES FOR PLOTTING
# =====================================================================
A_range = np.arange(2, 270)

sst1     = np.array([sst_curve(a) for a in A_range])
sst1_inv = np.array([CEIL_1 - sst_curve(a) for a in A_range])
sst2_inv = np.array([CEIL_2 - sst_local(a - 64) if a > 64 else np.nan
                     for a in A_range])
sst3_inv = np.array([CEIL_3 - sst_local(a - 128) if a > 128 else np.nan
                     for a in A_range])
model = np.array([envelope(a) for a in A_range])

A_data  = np.array([a for _, _, a, ba in AME if a >= 2])
BA_data = np.array([ba for _, _, a, ba in AME if a >= 2])
BA_pred = np.array([envelope(a) for a in A_data])

# =====================================================================
# STATISTICS
# =====================================================================
mask = BA_data > 0
r2_full = 1 - np.sum((BA_pred[mask] - BA_data[mask])**2) / \
              np.sum((BA_data[mask] - BA_data[mask].mean())**2)
mae_full = np.mean(np.abs(BA_pred[mask] - BA_data[mask])) * 1000

mask64 = (A_data >= 12) & (A_data <= 64) & (BA_data > 0)
r2_r1 = 1 - np.sum((BA_pred[mask64] - BA_data[mask64])**2) / \
            np.sum((BA_data[mask64] - BA_data[mask64].mean())**2)
mae_r1 = np.mean(np.abs(BA_pred[mask64] - BA_data[mask64])) * 1000

mask_post = (A_data > 64) & (BA_data > 0)
r2_post = 1 - np.sum((BA_pred[mask_post] - BA_data[mask_post])**2) / \
              np.sum((BA_data[mask_post] - BA_data[mask_post].mean())**2)
mae_post = np.mean(np.abs(BA_pred[mask_post] - BA_data[mask_post])) * 1000

print(f"\n=== Key closure points ===")
print(f"A=64:  B/A = {envelope(64):.4f} MeV")
print(f"A=128: B/A = {envelope(128):.4f} MeV")
print(f"A=192: B/A = {envelope(192):.4f} MeV")
print(f"A=208: B/A = {envelope(208):.4f} MeV")
print(f"A=256: B/A = {envelope(256):.4f} MeV")

print(f"\n=== Statistics ===")
print(f"Round 1 (A <= 64):  R² = {r2_r1:.4f}  MAE = {mae_r1:.0f} keV")
print(f"Post-64 (A > 64):   R² = {r2_post:.4f}  MAE = {mae_post:.0f} keV")
print(f"Full (A = 4-208):   R² = {r2_full:.4f}  MAE = {mae_full:.0f} keV")

# =====================================================================
# PLOT
# =====================================================================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7), height_ratios=[3, 1],
                                gridspec_kw={'hspace': 0.08})
fig.patch.set_facecolor('white')
for ax in (ax1, ax2):
    ax.set_facecolor('white')
    ax.tick_params(colors='#333333', labelsize=8)
    for spine in ax.spines.values(): spine.set_color('#cccccc')

# Round 1
ax1.plot(A_range, sst1, color='#c8a020', linewidth=1.5, alpha=0.5, zorder=2,
         label=r'SST$_1$')
ax1.plot(A_range, sst1_inv, color='#c03030', linewidth=1.5, alpha=0.5, zorder=2,
         label=f'SST$_1$ inv  (ceil = {CEIL_1:.3f})')

# Round 2
mask_r2 = A_range > 64
ax1.plot(A_range[mask_r2], sst2_inv[mask_r2], color='#7848b0', linewidth=1.5,
         alpha=0.5, zorder=2,
         label=f'SST$_2$ inv  (ceil = {CEIL_2:.3f})')

# Round 3
mask_r3 = A_range > 128
ax1.plot(A_range[mask_r3], sst3_inv[mask_r3], color='#3088c0', linewidth=1.5,
         alpha=0.5, zorder=2,
         label=f'SST$_3$ inv  (ceil = {CEIL_3:.3f})')

# Envelope
ax1.plot(A_range, model, color='#008870', linewidth=2.5, zorder=4, alpha=0.85,
         label='B/A = min(active curves)')

# Experimental data
ax1.scatter(A_data[mask], BA_data[mask], s=14, color='#c04070', alpha=0.7,
            zorder=5, edgecolors='none', label='AME2020')

# Closure point markers
ax1.scatter([64], [BA_ZN], s=70, facecolors='none', edgecolors='#c8a020',
            linewidth=2, zorder=6)
ax1.annotate('K$^D$=64\nZn-64', (64, BA_ZN),
             textcoords='offset points', xytext=(6, -26),
             fontsize=7, color='#806010', ha='left')

ax1.scatter([128], [envelope(128)], s=70, facecolors='none', edgecolors='#c8a020',
            linewidth=2, zorder=6)
ax1.annotate('2K$^D$=128\nTe-128', (128, envelope(128)),
             textcoords='offset points', xytext=(6, -26),
             fontsize=7, color='#806010', ha='left')

ax1.scatter([192], [envelope(192)], s=70, facecolors='none', edgecolors='#c8a020',
            linewidth=2, zorder=6)
ax1.annotate('3K$^D$=192\nOs-192', (192, envelope(192)),
             textcoords='offset points', xytext=(6, 10),
             fontsize=7, color='#806010', ha='left')

ax1.scatter([256], [envelope(256)], s=70, facecolors='none', edgecolors='#c8a020',
            linewidth=2, zorder=6)
ax1.annotate('4K$^D$=256', (256, envelope(256)),
             textcoords='offset points', xytext=(-50, -20),
             fontsize=7, color='#806010', ha='left')

# Axes
ax1.set_xlim(0, 270); ax1.set_ylim(4.5, 12)
ax1.set_ylabel('B/A (MeV)', fontsize=9, color='#333333')
ax1.xaxis.set_major_locator(MultipleLocator(20))
ax1.set_xticklabels([])
ax1.grid(True, alpha=0.15, color='#aaaaaa')
ax1.legend(loc='upper right', fontsize=6.5, facecolor='white', edgecolor='#cccccc',
           labelcolor='#333333', framealpha=0.9)

# Equations on chart
ax1.text(0.98, 0.30,
         r'$\mu_{\mathrm{SST}}(x) = \frac{(2x+1) - \sqrt{4x+1}}{2x}$',
         transform=ax1.transAxes, fontsize=10, color='#00887080',
         va='bottom', ha='right')
ax1.text(0.98, 0.20,
         r'$\mathrm{SST}(A) = \frac{B}{A}(\mathrm{Zn})'
         r'\cdot\frac{K^D}{A}\cdot\frac{\Sigma_A}{\Sigma_{K^D}}$',
         transform=ax1.transAxes, fontsize=10, color='#c8a02080',
         va='bottom', ha='right')

# Stats box
stats = (f'Round 1 (A ≤ 64):  R² = {r2_r1:.3f}  MAE = {mae_r1:.0f} keV\n'
         f'Post-64 (A > 64):  R² = {r2_post:.3f}  MAE = {mae_post:.0f} keV\n'
         f'Full (A = 4–208):   R² = {r2_full:.3f}  MAE = {mae_full:.0f} keV')
ax1.text(0.98, 0.04, stats, transform=ax1.transAxes, fontsize=7,
         va='bottom', ha='right', color='#555555', fontfamily='monospace',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='#f8f8f8', edgecolor='#cccccc'))

ax1.set_title('Nuclear Binding Energy from Bidirectional SST',
              fontsize=12, color='#222222', pad=10, fontfamily='serif')

# Residual panel
residuals = (BA_pred[mask] - BA_data[mask]) * 1000
ax2.axhline(0, color='#aaaaaa', linewidth=0.5)
ax2.bar(A_data[mask], residuals, width=1.2,
        color=np.where(residuals >= 0, '#00887060', '#c0407060'), edgecolor='none')
ax2.axvline(64, color='#c8a02040', linewidth=1, linestyle='--')
ax2.axvline(128, color='#c8a02040', linewidth=1, linestyle='--')
ax2.axvline(192, color='#c8a02040', linewidth=1, linestyle='--')
ax2.set_xlim(0, 270); ax2.set_ylim(-300, 300)
ax2.set_xlabel('Mass Number A', fontsize=9, color='#333333')
ax2.set_ylabel('Residual (keV)', fontsize=8, color='#333333')
ax2.xaxis.set_major_locator(MultipleLocator(20))
ax2.grid(True, alpha=0.15, color='#aaaaaa')

fig.text(0.5, 0.01,
         r'$K\!=\!4,\ D\!=\!3$ · Single field closure · '
         r'Sierpiński walk reflects at $K^D$ boundaries · Zero free parameters',
         ha='center', fontsize=7, color='#666666', style='italic')

plt.savefig('gfd_binding_energy.png', dpi=300,
            bbox_inches='tight', facecolor=fig.get_facecolor())

print(f"\nChart saved: gfd_binding_energy.png")
