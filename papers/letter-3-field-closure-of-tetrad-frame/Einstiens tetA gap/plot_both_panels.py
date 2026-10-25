"""
Two figures that tell the complete story.

Panel A: Einstein's equation IS the TetA partition (μ=1).
         Same curve. Identical. GR was always μ·g = GM/r².

Panel B: Unfreeze μ. The GFD equation peels away from GR.
         The gap is TetB — the "missing mass."
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['font.size'] = 12

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.5))

# ── Shared x-axis: dimensionless observed acceleration ──
x = np.logspace(-2, 3, 1000)  # g_t / a_0

# ==============================================================
# PANEL A: Einstein = TetA partition (μ = 1)
# ==============================================================

# Einstein: g_s = g_t  (the 1:1 line)
g_s_einstein = x

# TetA partition with μ = 1:  μ · g_t = g_t  (same line)
mu_frozen = 1.0
g_s_tetA = mu_frozen * x

ax1.loglog(x, g_s_einstein, 'b-', linewidth=4, alpha=0.5,
           label=r"Einstein:  $g_s = g_t$")
ax1.loglog(x, g_s_tetA, 'r--', linewidth=2.5,
           label=r"TetA partition:  $\mu \cdot g_t = g_t$"
                 r"$\;\;(\mu = 1)$")

ax1.set_xlabel(r'$g_t\,/\,a_0$ (observed acceleration)', fontsize=13)
ax1.set_ylabel(r'$g_s\,/\,a_0$ (baryonic source)', fontsize=13)
ax1.set_title(
    r"$\mathbf{A.}$  Einstein's equation IS the TetA partition",
    fontsize=13, loc='left')
ax1.legend(fontsize=11, loc='upper left', framealpha=0.9)

ax1.annotate(
    "Identical.\n"
    "Same curve.\n\n"
    r"$g = GM/r^2$" + "\n"
    r"$= \;\mu \cdot g\;$ when $\;\mu = 1$" + "\n\n"
    "GR was always the\n"
    r"TetA partition with $\mu$ frozen.",
    xy=(50, 0.08), fontsize=11,
    bbox=dict(boxstyle='round,pad=0.6', facecolor='#f5f5f5',
              edgecolor='#aaaaaa', alpha=0.9))

ax1.set_xlim(0.01, 1000)
ax1.set_ylim(0.01, 1000)
ax1.grid(True, alpha=0.15, which='both')

# ==============================================================
# PANEL B: Unfreeze μ — the gap is TetB
# ==============================================================

# Einstein (μ = 1): g_s = g_t
g_s_GR = x

# GFD (μ varies): g_s = μ · g_t = g_t²/(g_t + a₀)
mu = x / (x + 1)
g_s_GFD = mu * x  # = x²/(x+1)

ax2.loglog(x, g_s_GR, 'b--', linewidth=2, alpha=0.7,
           label=r'GR:  $g_s = g_t\;\;(\mu = 1)$')
ax2.loglog(x, g_s_GFD, 'r-', linewidth=2.5,
           label=r'GFD:  $g_s = \mu \cdot g_t = g_t^2/(g_t + a_0)$')

# Shade the gap
ax2.fill_between(x, g_s_GFD, g_s_GR, alpha=0.12, color='purple',
                 label=r'$(1-\mu)\,g_t$ — TetB: the "missing mass"')

# MOND ring
ax2.axvline(x=1, color='gray', linewidth=0.8, alpha=0.4, linestyle=':')
ax2.annotate(r'$x = 1$' + '\n(MOND ring)',
             xy=(1.3, 0.025), fontsize=10, color='gray')

ax2.annotate('GR accurate\nhere',
             xy=(150, 80), fontsize=10,
             color='blue', alpha=0.6, ha='center')
ax2.annotate(r'"Missing mass"' + '\nappears here',
             xy=(0.06, 0.25), fontsize=10,
             color='purple', alpha=0.8, ha='center')

ax2.set_xlabel(r'$g_t\,/\,a_0$ (observed acceleration)', fontsize=13)
ax2.set_ylabel(r'$g_s\,/\,a_0$ (baryonic source)', fontsize=13)
ax2.set_title(
    r"$\mathbf{B.}$  Unfreeze $\mu$: the gap is TetB",
    fontsize=13, loc='left')
ax2.legend(fontsize=11, loc='upper left', framealpha=0.9)

ax2.set_xlim(0.01, 1000)
ax2.set_ylim(0.01, 1000)
ax2.grid(True, alpha=0.15, which='both')

plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/einstein_tetA_and_gap.png', dpi=200,
            bbox_inches='tight', facecolor='white')
plt.savefig('/mnt/user-data/outputs/einstein_tetA_and_gap.pdf',
            bbox_inches='tight', facecolor='white')
print("Done")
