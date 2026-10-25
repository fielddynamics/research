"""
GFD Stellar Field Configuration — Three-Panel Chart
============================================================

Plots the gravitational field "rotation curve" for three stars:
  Panel 1: The Sun (G2V, 1 Msun)
  Panel 2: Proxima Centauri (M5V, 0.122 Msun)
  Panel 3: Sirius A (A1V, 2.063 Msun)

Shows:
  - TetB (left, subspace) and TetA (right, our spacetime)
  - Keplerian velocity (Newtonian, no field)
  - GFD velocity (with field contribution)
  - Field Origin boundary (FO) and Horizon (H)
  - Wide binary detection threshold
  - Interior field boost stats

Requirements: matplotlib, numpy

    pip install matplotlib numpy
    python gfd_stellar_panels.py

Author: Stephen Nelson / Field Dynamics Research
Date:   February 2026
"""

import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# =============================================================================
# CONSTANTS (SI)
# =============================================================================

G_SI = 6.674e-11       # m³/(kg·s²)
A0_SI = 1.2e-10         # m/s²
M_SUN = 1.989e30        # kg
R_SUN = 6.957e8          # m
AU = 1.496e11            # m
LY = 9.461e15            # m
PC = 3.086e16            # m

# =============================================================================
# GFD FUNCTIONS
# =============================================================================

def g_newton(r_m, M_kg):
    """Newtonian gravitational acceleration at distance r from mass M."""
    if r_m <= 0:
        return 0
    return G_SI * M_kg / r_m**2

def g_total(r_m, M_kg):
    """GFD total acceleration: solves the constitutive law."""
    gN = g_newton(r_m, M_kg)
    if gN <= 0:
        return 0
    return (gN + math.sqrt(gN**2 + 4 * gN * A0_SI)) / 2

def v_kepler(r_m, M_kg):
    """Keplerian orbital velocity."""
    if r_m <= 0:
        return 0
    return math.sqrt(G_SI * M_kg / r_m)

def v_gfd(r_m, M_kg):
    """GFD orbital velocity (including field contribution)."""
    if r_m <= 0:
        return 0
    gt = g_total(r_m, M_kg)
    return math.sqrt(gt * r_m)

def x_at_r(r_m, M_kg):
    """GFD state parameter x = g_t / a₀."""
    gt = g_total(r_m, M_kg)
    return gt / A0_SI

def mu_at_r(r_m, M_kg):
    x = x_at_r(r_m, M_kg)
    return x / (x + 1)

def field_frac_at_r(r_m, M_kg):
    return 1 - mu_at_r(r_m, M_kg)

def R_field_origin(M_kg):
    """Radius where g_N = a₀/2 (the Field Origin boundary)."""
    return math.sqrt(2 * G_SI * M_kg / A0_SI)

def R_horizon(M_kg):
    """Radius of the full gravitational influence (D × R_FO)."""
    return 3 * R_field_origin(M_kg)


# =============================================================================
# STAR DATA
# =============================================================================

stars = [
    {
        'name': 'The Sun',
        'spectral': 'G2V',
        'M': 1.0 * M_SUN,
        'R': 1.0 * R_SUN,
        'T_eff': 5778,
        'color': '#FFD700',
        'note_objects': [
            (0.39 * AU, 'Mercury'),
            (1.0 * AU, 'Earth'),
            (5.2 * AU, 'Jupiter'),
            (30.1 * AU, 'Neptune'),
            (50 * AU, 'Kuiper'),
            (2000 * AU, 'Oort inner'),
        ],
    },
    {
        'name': 'Proxima Centauri',
        'spectral': 'M5.5Ve',
        'M': 0.122 * M_SUN,
        'R': 0.154 * R_SUN,
        'T_eff': 3042,
        'color': '#FF4444',
        'note_objects': [
            (0.0485 * AU, 'Prox b'),
            (0.229 * AU, 'Prox d'),
            (1.489 * AU, 'Prox c'),
        ],
    },
    {
        'name': 'Sirius A',
        'spectral': 'A1V',
        'M': 2.063 * M_SUN,
        'R': 1.711 * R_SUN,
        'T_eff': 9940,
        'color': '#88BBFF',
        'note_objects': [
            (20 * AU, 'Sirius B orbit'),
        ],
    },
]


# =============================================================================
# PLOTTING
# =============================================================================

plt.rcParams.update({
    'figure.facecolor': '#0a0c14',
    'axes.facecolor': '#10131f',
    'axes.edgecolor': '#2a2d3a',
    'axes.labelcolor': '#8890a0',
    'text.color': '#c8ccd4',
    'xtick.color': '#6b7084',
    'ytick.color': '#6b7084',
    'grid.color': '#1a1d2a',
    'grid.alpha': 0.6,
    'font.family': 'monospace',
    'font.size': 9,
})

fig, axes = plt.subplots(1, 3, figsize=(20, 7.5), dpi=150)
fig.subplots_adjust(left=0.05, right=0.97, top=0.88, bottom=0.12, wspace=0.24)

fig.text(0.5, 0.95, 'GFD Stellar Field Configuration — Velocity vs Radius',
         ha='center', va='center', fontsize=16, fontweight='bold',
         color='white', fontfamily='serif')
fig.text(0.5, 0.915,
         'TetB (subspace)  ←  Field Origin  →  TetA (our spacetime)  |  '
         'Keplerian (dashed) vs GFD (solid)',
         ha='center', va='center', fontsize=9, color='#6b7084',
         fontfamily='monospace')

for idx, (ax, star) in enumerate(zip(axes, stars)):
    M = star['M']
    color = star['color']

    R_FO = R_field_origin(M)
    R_H = R_horizon(M)

    # Plot range: from 1 AU to 2× R_horizon, in AU
    r_min_au = 0.5
    r_max_au = 2 * R_H / AU
    r_plot_max = r_max_au

    # Symmetric axis: -r_plot_max to +r_plot_max
    # Use log scale for radius (distances span many orders of magnitude)
    # We'll use a custom approach: plot log10(r) on x-axis

    # Generate radii (log-spaced)
    r_au_array = np.logspace(np.log10(r_min_au), np.log10(r_max_au), 400)
    r_m_array = r_au_array * AU

    # Compute velocities
    v_kep_array = np.array([v_kepler(r, M) for r in r_m_array])
    v_gfd_array = np.array([v_gfd(r, M) for r in r_m_array])

    # Convert to m/s
    # Use log10(r/AU) as x-axis
    log_r = np.log10(r_au_array)
    log_r_neg = -log_r[::-1]  # mirror for TetB

    # Y axis: velocity in m/s (or km/s for readability)
    v_kep_plot = v_kep_array  # m/s
    v_gfd_plot = v_gfd_array  # m/s

    # Determine good y units
    v_max = max(v_gfd_plot) * 1.15
    if v_max > 5000:
        v_scale = 1000
        v_unit = 'km/s'
    else:
        v_scale = 1
        v_unit = 'm/s'

    v_kep_plot = v_kep_plot / v_scale
    v_gfd_plot = v_gfd_plot / v_scale
    v_max = v_max / v_scale

    # Region shading
    ax.axvspan(0, max(log_r) * 1.1, color='#47b8e8', alpha=0.012)
    ax.axvspan(-max(log_r) * 1.1, 0, color='#e87247', alpha=0.012)

    # Grid
    ax.grid(True, alpha=0.25, linewidth=0.5)

    # Center line (Field Origin at r = 0 in log space is misleading,
    # let's put it at log10(R_FO/AU))
    log_R_FO = math.log10(R_FO / AU)
    log_R_H = math.log10(R_H / AU)

    # Field Origin boundary
    ax.axvline(0, color='#e8c547', linewidth=1, linestyle='--', alpha=0.3)

    # FO and H markers
    ax.axvline(log_R_FO, color=color, linewidth=1.2, linestyle=':', alpha=0.5)
    ax.axvline(-log_R_FO, color=color, linewidth=1.2, linestyle=':', alpha=0.3)
    ax.axvline(log_R_H, color=color, linewidth=1, linestyle='-.', alpha=0.35)
    ax.axvline(-log_R_H, color=color, linewidth=1, linestyle='-.', alpha=0.2)

    # Labels for FO and H
    ax.text(log_R_FO, v_max * 0.97, 'FO', ha='center', va='top',
            fontsize=8, color=color, fontweight='bold', alpha=0.8)
    ax.text(log_R_H, v_max * 0.97, 'H', ha='center', va='top',
            fontsize=8, color=color, fontweight='bold', alpha=0.6)
    ax.text(-log_R_FO, v_max * 0.97, 'FO', ha='center', va='top',
            fontsize=8, color=color, fontweight='bold', alpha=0.5)
    ax.text(-log_R_H, v_max * 0.97, 'H', ha='center', va='top',
            fontsize=8, color=color, fontweight='bold', alpha=0.35)

    # --- KEPLERIAN CURVE (dashed, dimmer) ---
    ax.plot(log_r, v_kep_plot, color='#888888', linewidth=1.5,
            linestyle='--', alpha=0.5, label='Keplerian (Newton)', zorder=4)
    ax.plot(-log_r[::-1], v_kep_plot[::-1], color='#888888', linewidth=1,
            linestyle='--', alpha=0.2, zorder=4)

    # --- GFD CURVE (solid, bright) ---
    ax.plot(log_r, v_gfd_plot, color=color, linewidth=2.5,
            alpha=0.9, label='GFD vortex field', zorder=5)
    ax.plot(-log_r[::-1], v_gfd_plot[::-1], color=color, linewidth=2,
            linestyle='--', alpha=0.35, zorder=5)

    # --- DIFFERENCE SHADING between Kepler and GFD ---
    ax.fill_between(log_r, v_kep_plot, v_gfd_plot,
                    color=color, alpha=0.08, zorder=3)

    # --- NOTABLE OBJECTS ---
    for r_obj, obj_name in star.get('note_objects', []):
        log_r_obj = math.log10(r_obj / AU)
        if log_r_obj > min(log_r) and log_r_obj < max(log_r):
            v_obj_gfd = v_gfd(r_obj, M) / v_scale
            ax.plot(log_r_obj, v_obj_gfd, 'o', color=color, markersize=4,
                    zorder=7, markeredgecolor='#0a0c14', markeredgewidth=0.5)
            ax.annotate(obj_name, (log_r_obj, v_obj_gfd),
                       textcoords="offset points", xytext=(5, 5),
                       fontsize=6, color='#8890a0', alpha=0.8,
                       fontfamily='monospace')

    # --- WIDE BINARY DETECTION THRESHOLD ---
    # Mark where Δv > 100 m/s (Gaia detectable)
    for i in range(len(r_au_array)):
        dv = (v_gfd_array[i] - v_kep_array[i])  # m/s
        if dv > 100:
            log_r_detect = log_r[i]
            ax.axvline(log_r_detect, color='#44ff44', linewidth=0.8,
                      linestyle=':', alpha=0.3)
            ax.text(log_r_detect, v_max * 0.06, 'Gaia\nΔv>100m/s',
                   ha='center', fontsize=5.5, color='#44ff44', alpha=0.6)
            break

    # --- AXIS LABELS ---
    ax.set_xlabel('log₁₀(r / AU)', fontsize=9, labelpad=6)
    if idx == 0:
        ax.set_ylabel(f'v  ({v_unit})', fontsize=9, labelpad=6)

    ax.set_xlim(-max(log_r) * 1.05, max(log_r) * 1.05)
    ax.set_ylim(0, v_max)

    # Galaxy name
    ax.text(0.5, 1.02, f"{star['name']}  ({star['spectral']}, {star['M']/M_SUN:.3f} Msun)",
            transform=ax.transAxes, ha='center', va='bottom',
            fontsize=12, fontweight='bold', color=color, fontfamily='serif')

    # --- STATS BOX ---
    R_FO_au = R_FO / AU
    R_H_au = R_H / AU
    R_FO_ly = R_FO / LY
    R_H_ly = R_H / LY

    # Field fractions at notable radii
    # At Oort Cloud distance (or equivalent for other stars)
    r_test = R_FO  # at the field origin
    F_at_FO = field_frac_at_r(R_FO, M) * 100
    F_at_H = field_frac_at_r(R_H, M) * 100

    # Velocity anomaly at R_FO
    dv_at_FO = v_gfd(R_FO, M) - v_kepler(R_FO, M)

    stats_text = (
        f"Interior: BOOST\n"
        f"R_FO: {R_FO_au:.0f} AU ({R_FO_ly:.3f} ly)\n"
        f"R_H:  {R_H_au:.0f} AU ({R_H_ly:.3f} ly)\n"
        f"─────────────\n"
        f"Field at FO: {F_at_FO:.0f}%\n"
        f"Field at H:  {F_at_H:.0f}%\n"
        f"Δv at FO: {dv_at_FO:.0f} m/s"
    )

    props = dict(boxstyle='round,pad=0.5', facecolor='#0a0c14',
                 edgecolor=color, alpha=0.85, linewidth=0.8)
    ax.text(0.03, 0.97, stats_text, transform=ax.transAxes,
            fontsize=6.5, verticalalignment='top', fontfamily='monospace',
            color='#c8ccd4', bbox=props)

    # Region labels
    ax.text(0.15, 0.02, '◄ TetB', transform=ax.transAxes,
            fontsize=7, ha='center', color='#e87247', alpha=0.4)
    ax.text(0.85, 0.02, 'TetA ►', transform=ax.transAxes,
            fontsize=7, ha='center', color='#47b8e8', alpha=0.4)

    # Legend
    leg = ax.legend(loc='upper right', fontsize=6, framealpha=0.5,
                    facecolor='#10131f', edgecolor='#2a2d3a',
                    labelcolor='#8890a0')

# Bottom annotation
fig.text(0.5, 0.02,
         'Solid = GFD (with field)  |  Dashed gray = Keplerian (Newton only)  |  '
         'Shaded area = field contribution  |  '
         'FO = Field Origin (g_N = a₀/2)  |  H = Horizon (g_N = a₀/18)  |  '
         'Green line = Gaia detection threshold',
         ha='center', va='bottom', fontsize=6.5, color='#6b7084',
         fontfamily='monospace')

# Save
output_path = '/mnt/user-data/outputs/gfd_stellar_panels.png'
plt.savefig(output_path, dpi=150, facecolor='#0a0c14',
            edgecolor='none', bbox_inches='tight')
plt.close()

print(f"Saved: {output_path}")
print()
for star in stars:
    M = star['M']
    R_FO = R_field_origin(M)
    R_H = R_horizon(M)
    dv = v_gfd(R_FO, M) - v_kepler(R_FO, M)
    print(f"{star['name']:20s} | R_FO = {R_FO/AU:8.0f} AU ({R_FO/LY:.3f} ly) | "
          f"R_H = {R_H/AU:8.0f} AU ({R_H/LY:.3f} ly) | Δv@FO = {dv:.0f} m/s")
