#!/usr/bin/env python3
"""
GFD Shell Decomposition — 4-Panel Chart
=========================================
Shows how the SST walk partitions nucleons into shells
via packing algebra magic numbers.

M(n) = 2[T(n) - G(n)]
T(n) = n(n+1)(n+2)/6
G(n) = (n-1)n/2 for n >= K=4, else 0

Magic numbers: 2, 8, 20, 28, 50, 82, 126

4 elements on letter size, white background, journal-ready.

Stephen Nelson — Gravity Field Dynamics
"""

import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

K = 4; D = 3; KD = K**D

def mu_sst(x):
    if x <= 0: return 0
    return ((2*x + 1) - math.sqrt(4*x + 1)) / (2*x)

SUM64 = sum(mu_sst(i*i) for i in range(1, KD+1))
SCALE = 8.756 * KD / SUM64

# Packing algebra
def T(n): return n*(n+1)*(n+2)//6
def G(n): return (n-1)*n//2 if n >= K else 0
def M(n): return 2*(T(n) - G(n))

# Shell boundaries (cumulative magic numbers)
SHELLS = []
for n in range(1, 8):
    SHELLS.append({
        'n': n,
        'magic': M(n),
        'capacity': M(n) - (M(n-1) if n > 1 else 0),
        'start': (M(n-1) if n > 1 else 0) + 1,
        'end': M(n),
    })

MAGIC_NUMBERS = [M(n) for n in range(1, 8)]  # 2, 8, 20, 28, 50, 82, 126

# Pastel shell colors (print-safe, distinguishable)
SHELL_COLORS = [
    '#e8b4b8',  # shell 1: soft rose
    '#b4d4e8',  # shell 2: soft blue
    '#b8e8b4',  # shell 3: soft green
    '#e8d4b4',  # shell 4: soft amber
    '#d4b4e8',  # shell 5: soft purple
    '#b4e8d8',  # shell 6: soft teal
    '#e8e4b4',  # shell 7: soft gold
]

SHELL_LABELS = ['1s', '1p', '1d', '2s', '2p+1f', '2d+1g', '3s+2f+1h']

# Stronger dot colors (saturated, for scatter points)
SHELL_DOT_COLORS = [
    '#e05070',  # shell 1: rose
    '#e0a020',  # shell 2: gold/amber
    '#40b040',  # shell 3: green
    '#e08020',  # shell 4: orange
    '#3090d0',  # shell 5: blue
    '#20b0a0',  # shell 6: teal
    '#9060c0',  # shell 7: purple
]
SHELL_DOT_EDGES = [
    '#b03050',
    '#b08010',
    '#208020',
    '#b06010',
    '#2070a0',
    '#108880',
    '#6840a0',
]

# 4 key elements
ELEMENTS = [
    ('O',   16,  8, 7.976),   # doubly magic 8 — 2 full shells
    ('Ca',  40, 20, 8.551),   # doubly magic 20 — 3 full shells 
    ('Ni',  58, 28, 8.732),   # magic 28 — 4 full shells
    ('Zn',  64, 30, 8.756),   # K^D = 64 — all shells, full closure
]


def draw_shell_chart(ax, sym, A, Z, ba_known):
    """Draw μ_SST scatter chart with shell-colored dots and pastel band backgrounds."""
    
    positions = list(range(1, 65))
    mu_vals = [mu_sst(i*i) for i in positions]
    
    # SST continuous curve
    x_cont = np.linspace(1, 64, 500)
    y_cont = [mu_sst(x*x) for x in x_cont]
    ax.plot(x_cont, y_cont, color='#00b89480', linewidth=1.5, zorder=1)
    
    # Shell background bands first
    for s, shell in enumerate(SHELLS):
        if shell['start'] > 64:
            break
        x_start = shell['start']
        x_end = min(shell['end'], 64)
        ax.axvspan(x_start - 0.5, x_end + 0.5, 
                   color=SHELL_COLORS[s], alpha=0.25, zorder=0)
    
    # Shell boundaries — vertical lines at magic numbers
    for shell in SHELLS:
        m = shell['magic']
        if m <= 64:
            ax.axvline(m + 0.5, color='#444444', linewidth=0.8, 
                       linestyle='--', alpha=0.5, zorder=3)
            ax.text(m + 0.5, 1.02, str(m), ha='center', va='bottom',
                    fontsize=6, fontweight='bold', color='#333333')
    
    # Colored dots — filled positions get shell color, unfilled get grey
    for i in positions:
        shell_idx = 0
        for s, shell in enumerate(SHELLS):
            if i <= shell['magic']:
                shell_idx = s
                break
        
        mu_val = mu_sst(i*i)
        if i <= A:
            ax.scatter(i, mu_val, s=18, color=SHELL_DOT_COLORS[shell_idx],
                      edgecolors=SHELL_DOT_EDGES[shell_idx], linewidth=0.4,
                      zorder=5, alpha=0.9)
        else:
            ax.scatter(i, mu_val, s=10, color='#cccccc',
                      edgecolors='#aaaaaa', linewidth=0.3,
                      zorder=2, alpha=0.4)
    
    # Shell capacity labels at bottom
    for s, shell in enumerate(SHELLS):
        if shell['magic'] > 64:
            break
        x_start = shell['start']
        x_end = min(shell['end'], 64)
        x_mid = (x_start + x_end) / 2
        cap = shell['capacity']
        
        ax.text(x_mid, -0.08, f'{cap}',
                ha='center', va='top', fontsize=5.5, 
                color='#555555', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.15', 
                         facecolor=SHELL_COLORS[s], edgecolor='none', alpha=0.6))
    
    # Fill marker
    if A <= 64:
        ax.axvline(A + 0.5, color='#c03030', linewidth=1.2, 
                   linestyle='-', alpha=0.7, zorder=4)
        ax.text(A + 1.5, 0.5, f'A={A}', fontsize=6, color='#c03030',
                rotation=90, va='center', ha='left')
    
    # Magic number circles at shell boundaries (like the reference image)
    for shell in SHELLS:
        m = shell['magic']
        if m <= A and m <= 64:
            mu_at_m = mu_sst(m*m)
            s_idx = SHELLS.index(shell)
            ax.scatter(m, mu_at_m, s=60, facecolors='none', 
                      edgecolors=SHELL_DOT_EDGES[s_idx], linewidth=1.5, zorder=6)
    
    # B/A prediction
    ba_pred = SCALE * sum(mu_sst(i*i) for i in range(1, A+1)) / A
    err_pct = abs(ba_pred - ba_known) / ba_known * 100
    
    # Title
    ax.set_title(f'{sym}-{A}  (Z={Z})', fontsize=11, fontweight='bold',
                 color='#111111', fontfamily='serif', pad=8)
    
    # Subtitle — below x-axis
    ax.text(0.5, -0.15, f'B/A = {ba_known:.3f}     Predicted = {ba_pred:.3f}     Error = {err_pct:.2f}%',
            transform=ax.transAxes, ha='center', va='top', fontsize=6.5, color='#444444')
    
    # Check which magic numbers this element hits
    magic_hit = [m for m in MAGIC_NUMBERS if m == A]
    if magic_hit:
        ax.text(0.02, 0.95, f'Magic closure: {magic_hit[0]}',
                transform=ax.transAxes, ha='left', va='top', fontsize=6, 
                color='#c03030', fontweight='bold')
    elif A == 64:
        ax.text(0.02, 0.95, f'Sierpiński closure: K$^D$=64',
                transform=ax.transAxes, ha='left', va='top', fontsize=6,
                color='#c03030', fontweight='bold')
    
    ax.set_xlim(0, 68)
    ax.set_ylim(-0.12, 1.05)
    ax.set_ylabel(r'$\mu_{\mathrm{SST}}(i^2)$', fontsize=8, color='#333333')
    ax.set_xlabel('Walk position $i$', fontsize=8, color='#333333')
    ax.tick_params(labelsize=6, colors='#444444')
    ax.grid(True, axis='y', alpha=0.1, color='#999999')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    for spine in ax.spines.values(): spine.set_color('#cccccc')


# ═══════════════════════════════════════
# BUILD FIGURE — 2×2 grid, letter size
# ═══════════════════════════════════════

fig, axes = plt.subplots(2, 2, figsize=(8.5, 11))
fig.patch.set_facecolor('white')

fig.suptitle('Shell Structure from the Sierpiński Walk',
             fontsize=14, fontweight='bold', color='#111111',
             fontfamily='serif', y=0.97)

# Subtitle with packing algebra
fig.text(0.5, 0.945, 
         r'$M(n) = 2\,[T(n) - G(n)]$     '
         r'$T(n) = n(n\!+\!1)(n\!+\!2)/6$     '
         r'$G(n) = (n\!-\!1)n/2\ \ (n \geq K)$',
         ha='center', fontsize=8, color='#666666', style='italic')

for idx, (sym, A, Z, ba) in enumerate(ELEMENTS):
    row = idx // 2
    col = idx % 2
    ax = axes[row, col]
    draw_shell_chart(ax, sym, A, Z, ba)

# Magic numbers table at bottom
table_y = 0.025
fig.text(0.5, table_y + 0.025,
         'Shell capacities:   2  +  6  +  12  +  8  +  22  +  32  +  44',
         ha='center', fontsize=8, color='#444444', fontfamily='monospace')
fig.text(0.5, table_y + 0.008,
         'Magic numbers:    2,    8,    20,   28,   50,    82,   126',
         ha='center', fontsize=8, color='#444444', fontfamily='monospace', 
         fontweight='bold')
fig.text(0.5, table_y - 0.012,
         r'The 20$\to$28 gap emerges from gate exclusion at $n = K = 4$, without spin-orbit coupling',
         ha='center', fontsize=7, color='#888888', style='italic')

plt.subplots_adjust(left=0.08, right=0.96, top=0.91, bottom=0.13,
                    hspace=0.45, wspace=0.25)

plt.savefig('/mnt/user-data/outputs/gfd_shell_decomposition_4.png', dpi=300,
            bbox_inches='tight', facecolor='white')
plt.savefig('/mnt/user-data/outputs/gfd_shell_decomposition_4.pdf',
            bbox_inches='tight', facecolor='white')

print('Done. 4-panel shell decomposition chart saved.')
print()
print('Magic numbers from packing algebra:')
for n in range(1, 8):
    cap = M(n) - (M(n-1) if n > 1 else 0)
    gn = G(n)
    print(f'  n={n}: T={T(n):>4}  G={gn:>3}  M={M(n):>4}  capacity={cap}')
