#!/usr/bin/env python3
"""
GFD Nuclear Binding Energy, Single Field Closure
===================================================
Publication chart: SST binding energy curve vs experimental data.

One field closure. One curve shape, the SST quadratic summed along the
Sierpinski walk, plotted and inverted at each K^D boundary.

  Round 1 (A = 0 to 64):
    SST_1      : rising curve, walk fills from position 1
    SST_1_inv  : CEIL_1 - SST_1, first reflection at K^D = 64

  Round 2 (A = 64 onward):
    SST_2_inv  : CEIL_2 - SST_local(A-64), walk restarts at A = 64

  Round 3 (A = 128 onward):
    SST_3_inv  : CEIL_3 - SST_local(A-128), walk restarts at A = 128

B/A = min(active curves)

Ceiling rule (structural, from constitutive law)
-------------------------------------------------
  The constitutive law μ(x) = x/(x+1) governs the ceiling drops.
  Each Sierpinski sector reflection absorbs (1 - μ(n)) from the
  energy budget, counting down from n=2.

  CEIL_1 = F₀ + m_e - μ(0)               = 17.511  (μ(0) = 0)
  CEIL_2 = CEIL_1 - (1 - μ(2))           = 17.178  (drop = 1/3)
  CEIL_3 = CEIL_2 - (1 - μ(1))           = 16.678  (drop = 1/2)

  F₀ = f(K,0) = K² + 1 = 17   (vortex throat)
  m_e = 0.51100 MeV            (electron mass, one closure revolution)

  Zero free parameters.

Stephen Nelson, Gravity Field Dynamics
"""

import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from plasmapy.particles import nuclear_binding_energy


def observed_be_per_nucleon(symbol, a):
    """Return observed BE/A in MeV from PlasmaPy (AME2020 mass tables)."""
    if a < 2:
        return 0.0
    total = nuclear_binding_energy(f"{symbol}-{a}")
    return float(total.to("MeV").value) / a

# =====================================================================
# STRUCTURAL CONSTANTS
# =====================================================================
K = 4; D = 3; KD = K**D  # 64

F_ZERO = K**2 + 1         # 17
F_PLUS = K**2 + K + 1     # 21
F_MINUS = K**2 - K + 1    # 13
M_E = 0.51100              # electron mass (MeV)

def mu(x):
    """Constitutive law: μ(x) = x/(x+1)"""
    return x / (x + 1) if x > 0 else 0.0

def mu_sst(x):
    """SST quadratic: bound-state constitutive law."""
    if x <= 0: return 0
    return ((2*x + 1) - math.sqrt(4*x + 1)) / (2*x)

# =====================================================================
# ENERGY SCALE -- calibrated from Zn-64 (full Sierpinski fill)
# =====================================================================
BA_ZN = 8.756  # framework value: full Sector 0 Sierpinski walk
SUM_KD = sum(mu_sst(i*i) for i in range(1, KD + 1))  # 59.928

def sst_curve(A):
    """Rising SST curve: B/A(Zn) * (K^D / A) * (sum_A / sum_KD)."""
    if A < 1: return 0
    sum_A = sum(mu_sst(i*i) for i in range(1, A + 1))
    return BA_ZN * (KD / A) * (sum_A / SUM_KD)

def sst_local(n):
    """SST curve for a walk restarted from position 1, covering n positions."""
    if n < 1: return 0
    sum_n = sum(mu_sst(i*i) for i in range(1, n + 1))
    return BA_ZN * (KD / n) * (sum_n / SUM_KD)

# =====================================================================
# CEILING DERIVATION (structural, from constitutive law)
# =====================================================================
#
# μ(x) = x/(x+1), so 1 - μ(x) = 1/(x+1)
#
# Sector 0: no drop.       μ(0) = 0,  drop = 0
# Sector 1: first drop.    1 - μ(2) = 1/3
# Sector 2: second drop.   1 - μ(1) = 1/2
#
# The constitutive law unwinds from deepest crossing (n=2) to origin.

DROP_1 = 1 - mu(2)   # 1/3
DROP_2 = 1 - mu(1)   # 1/2

CEIL_1 = F_ZERO + M_E               # 17.511
CEIL_2 = CEIL_1 - DROP_1            # 17.178
CEIL_3 = CEIL_2 - DROP_2            # 16.678

print(f"=== Ceiling derivation (constitutive law) ===")
print(f"")
print(f"  F₀   = {F_ZERO}")
print(f"  m_e  = {M_E}")
print(f"  μ(x) = x/(x+1)")
print(f"")
print(f"  CEIL_1 = F₀ + m_e - μ(0)       = {CEIL_1:.4f}  (drop = 0)")
print(f"  CEIL_2 = CEIL_1 - (1-μ(2))     = {CEIL_2:.4f}  (drop = 1/3 = {DROP_1:.4f})")
print(f"  CEIL_3 = CEIL_2 - (1-μ(1))     = {CEIL_3:.4f}  (drop = 1/2 = {DROP_2:.4f})")
print(f"")

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
_ISOTOPES = [
    ( 1,"H",    1),( 2,"He",  4),( 3,"Li",  7),( 4,"Be",  9),
    ( 5,"B",  11),( 6,"C",  12),( 7,"N",  14),( 8,"O",  16),
    ( 9,"F",  19),(10,"Ne", 20),(11,"Na", 23),(12,"Mg", 24),
    (13,"Al", 27),(14,"Si", 28),(15,"P",  31),(16,"S",  32),
    (17,"Cl", 35),(18,"Ar", 40),(19,"K",  39),(20,"Ca", 40),
    (21,"Sc", 45),(22,"Ti", 48),(23,"V",  51),(24,"Cr", 52),
    (25,"Mn", 55),(26,"Fe", 56),(27,"Co", 59),(28,"Ni", 58),
    (29,"Cu", 63),(30,"Zn", 64),(31,"Ga", 69),(32,"Ge", 74),
    (33,"As", 75),(34,"Se", 80),(35,"Br", 79),(36,"Kr", 84),
    (37,"Rb", 85),(38,"Sr", 88),(39,"Y",  89),(40,"Zr", 90),
    (41,"Nb", 93),(42,"Mo", 98),(43,"Tc", 98),(44,"Ru",102),
    (45,"Rh",103),(46,"Pd",106),(47,"Ag",107),(48,"Cd",114),
    (49,"In",115),(50,"Sn",120),(51,"Sb",121),(52,"Te",128),
    (53,"I", 127),(54,"Xe",132),(55,"Cs",133),(56,"Ba",138),
    (57,"La",139),(58,"Ce",140),(59,"Pr",141),(60,"Nd",142),
    (61,"Pm",145),(62,"Sm",152),(63,"Eu",153),(64,"Gd",158),
    (65,"Tb",159),(66,"Dy",164),(67,"Ho",165),(68,"Er",166),
    (69,"Tm",169),(70,"Yb",174),(71,"Lu",175),(72,"Hf",180),
    (73,"Ta",181),(74,"W", 184),(75,"Re",187),(76,"Os",192),
    (77,"Ir",193),(78,"Pt",195),(79,"Au",197),(80,"Hg",202),
    (81,"Tl",205),(82,"Pb",208),
]

print("Loading AME2020 data...")
AME = [(z, sym, a, observed_be_per_nucleon(sym, a)) for z, sym, a in _ISOTOPES]

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

A_data  = np.array([a for _, _, a, ba in AME if a >= 4])
BA_data = np.array([ba for _, _, a, ba in AME if a >= 4])
BA_pred = np.array([envelope(a) for a in A_data])

# =====================================================================
# STATISTICS
# =====================================================================
mask = BA_data > 0
r2_full = 1 - np.sum((BA_pred[mask] - BA_data[mask])**2) / \
              np.sum((BA_data[mask] - BA_data[mask].mean())**2)
mae_full = np.mean(np.abs(BA_pred[mask] - BA_data[mask])) * 1000

mask64 = (A_data >= 4) & (A_data <= 64) & (BA_data > 0)
r2_r1 = 1 - np.sum((BA_pred[mask64] - BA_data[mask64])**2) / \
            np.sum((BA_data[mask64] - BA_data[mask64].mean())**2)
mae_r1 = np.mean(np.abs(BA_pred[mask64] - BA_data[mask64])) * 1000

mask_post = (A_data > 64) & (BA_data > 0)
r2_post = 1 - np.sum((BA_pred[mask_post] - BA_data[mask_post])**2) / \
              np.sum((BA_data[mask_post] - BA_data[mask_post].mean())**2)
mae_post = np.mean(np.abs(BA_pred[mask_post] - BA_data[mask_post])) * 1000

print(f"\n=== Key closure points ===")
print(f"  A=64:  B/A = {envelope(64):.4f} MeV")
print(f"  A=128: B/A = {envelope(128):.4f} MeV")
print(f"  A=192: B/A = {envelope(192):.4f} MeV")
print(f"  A=208: B/A = {envelope(208):.4f} MeV")
print(f"  A=256: B/A = {envelope(256):.4f} MeV")

print(f"\n=== Statistics ===")
print(f"  Round 1 (A <= 64):  R2 = {r2_r1:.4f}  MAE = {mae_r1:.0f} keV")
print(f"  Post-64 (A > 64):   R2 = {r2_post:.4f}  MAE = {mae_post:.0f} keV")
print(f"  Full (A = 4-208):   R2 = {r2_full:.4f}  MAE = {mae_full:.0f} keV")

# =====================================================================
# PER-ELEMENT TABLE
# =====================================================================
print(f"\n=== Per-element results ===")
print(f"  {'Sym':>3} {'Z':>3} {'A':>3}  {'Known':>7} {'Pred':>7} {'Δ keV':>7}")
print(f"  {'─'*3} {'─'*3} {'─'*3}  {'─'*7} {'─'*7} {'─'*7}")
for z, sym, a, ba in AME:
    if a >= 4 and ba > 0:
        pred = envelope(a)
        delta = (pred - ba) * 1000
        flag = " *" if abs(delta) < 50 else ""
        print(f"  {sym:>3} {z:>3} {a:>3}  {ba:>7.3f} {pred:>7.3f} {delta:>+7.1f}{flag}")

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
for A_mark, label_text, y_off in [
    (64,  'K$^D$=64\nZn-64',   -26),
    (128, '2K$^D$=128\nTe-128', -26),
    (192, '3K$^D$=192\nOs-192',  10),
    (256, '4K$^D$=256',         -20),
]:
    ax1.scatter([A_mark], [envelope(A_mark)], s=70, facecolors='none',
                edgecolors='#c8a020', linewidth=2, zorder=6)
    ax1.annotate(label_text, (A_mark, envelope(A_mark)),
                 textcoords='offset points', xytext=(6, y_off),
                 fontsize=7, color='#806010', ha='left')

# Axes
ax1.set_xlim(0, 270); ax1.set_ylim(4.5, 10)
ax1.set_ylabel('B/A (MeV)', fontsize=9, color='#333333')
ax1.xaxis.set_major_locator(MultipleLocator(20))
ax1.set_xticklabels([])
ax1.grid(True, alpha=0.15, color='#aaaaaa')
ax1.legend(loc='upper right', fontsize=6.5, facecolor='white', edgecolor='#cccccc',
           labelcolor='#333333', framealpha=0.9)

# Equations on chart
ax1.text(0.98, 0.38,
         r'$\mu(x) = \frac{x}{x+1}$',
         transform=ax1.transAxes, fontsize=10, color='#00887080',
         va='bottom', ha='right')
ax1.text(0.98, 0.28,
         r'$\mathrm{CEIL}_n = F_0 + m_e - \sum_{k} (1 - \mu(k))$',
         transform=ax1.transAxes, fontsize=9, color='#00887080',
         va='bottom', ha='right')
ax1.text(0.98, 0.20,
         r'$\mathrm{SST}(A) = \frac{B}{A}(\mathrm{Zn})'
         r'\cdot\frac{K^D}{A}\cdot\frac{\Sigma_A}{\Sigma_{K^D}}$',
         transform=ax1.transAxes, fontsize=10, color='#c8a02080',
         va='bottom', ha='right')

# Stats box
stats = (f'Round 1 (A <= 64):  R2 = {r2_r1:.3f}  MAE = {mae_r1:.0f} keV\n'
         f'Post-64 (A > 64):   R2 = {r2_post:.3f}  MAE = {mae_post:.0f} keV\n'
         f'Full (A = 4-208):   R2 = {r2_full:.3f}  MAE = {mae_full:.0f} keV')
ax1.text(0.98, 0.04, stats, transform=ax1.transAxes, fontsize=7,
         va='bottom', ha='right', color='#555555', fontfamily='monospace',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='#f8f8f8', edgecolor='#cccccc'))

ax1.set_title('Nuclear Binding Energy from Bidirectional SST\n'
              r'Ceilings from $\mu(x) = x/(x+1)$: drops = $1-\mu(2)$, $1-\mu(1)$',
              fontsize=11, color='#222222', pad=10, fontfamily='serif')

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
         r'$K\!=\!4,\ D\!=\!3$ | $F_0 = 17,\ m_e = 0.511$ MeV | '
         r'Ceiling drops: $1-\mu(2) = \frac{1}{3}$, $1-\mu(1) = \frac{1}{2}$ | '
         r'Zero free parameters',
         ha='center', fontsize=7, color='#666666', style='italic')

plt.savefig('gfd_binding_energy_mu.png', dpi=300,
            bbox_inches='tight', facecolor=fig.get_facecolor())

print(f"\nChart saved: gfd_binding_energy_mu.png")
