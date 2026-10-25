"""
GFD Galactic Vortex — Three-Panel Chart
============================================================

Generates a publication-quality PNG with three panels:
  Panel 1: Milky Way
  Panel 2: M33
  Panel 3: NGC 6503

Each panel shows:
  - TetB (left, subspace interior) and TetA (right, our spacetime)
  - Smooth vortex model curve (solid)
  - Direct observation-mapped curve (thin, through every data point)
  - Observation points with error bars
  - Field Origin boundary (FO) and Horizon (H) markers
  - Interior field stats: boost/brake and % contribution

Requirements: matplotlib, numpy, scipy

    pip install matplotlib numpy scipy
    python gfd_vortex_panels.py

Author: Stephen Nelson / Field Dynamics Research
Date:   February 2026
"""

import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from scipy.optimize import curve_fit

# =============================================================================
# CONSTANTS
# =============================================================================

G = 4.3009e-3    # kpc (km/s)² / M_sun
A0 = 3703.0       # (km/s)²/kpc
D = 3

# =============================================================================
# GFD FUNCTIONS
# =============================================================================

def mass_decode(r, v):
    return r * v**4 / (G * (A0 * r + v**2))

def v_from_gN(r, gN):
    if r <= 0.001 or gN <= 0:
        return 0.0
    gr = gN * r
    return math.sqrt((gr + math.sqrt(gr**2 + 4 * gN * r**2 * A0)) / 2)

def boost_factor(r, v):
    """B = 1/x = a₀·r/v². Field-to-baryon acceleration ratio."""
    x = (v**2 / r) / A0
    return 1.0 / x if x > 0 else float('inf')

def field_fraction(r, v):
    """F = 1-μ = 1/(x+1). Fraction of acceleration from the field."""
    x = (v**2 / r) / A0
    return 1.0 / (x + 1)

# Mass models
def single_comp_mass(r, Mt, rs, alpha):
    return Mt * r**alpha / (r**alpha + rs**alpha)

def exp_disk_mass(r, Mt, Rd):
    return Mt * (1 - (1 + r / Rd) * np.exp(-r / Rd))

def two_comp_mass(r, Mb, rb, Md, Rd):
    bulge = Mb * r**2 / (r**2 + rb**2)
    disk = Md * (1 - (1 + r / Rd) * np.exp(-r / Rd))
    return bulge + disk

# =============================================================================
# GALAXY DATA
# =============================================================================

galaxies = [
    {
        'name': 'Milky Way',
        'color': '#47b8e8',
        'color_dim': '#47b8e840',
        'data': [
            (0.5,115,20),(1,200,15),(1.5,215,12),(2,218,10),(2.5,222,10),
            (3,220,8),(4,225,8),(5,228,7),(6,224,7),(7,220,6),(8,220,5),
            (9,218,5),(10,220,5),(12,218,6),(14,220,6),(16,222,7),
            (18,220,8),(20,220,10),(22,218,12),(25,215,15),(28,212,18),(30,210,20)
        ],
    },
    {
        'name': 'M33',
        'color': '#e87247',
        'color_dim': '#e8724740',
        'data': [
            (0.3,20,8),(0.5,35,7),(0.8,50,6),(1,60,5),(1.5,75,5),
            (2,85,5),(2.5,92,4),(3,100,4),(3.5,104,4),(4,107,4),
            (5,110,4),(6,112,4),(7,115,5),(8,118,5),(9,120,5),
            (10,122,5),(11,124,6),(12,126,6),(13,128,7),(14,130,7),(15,131,8)
        ],
    },
    {
        'name': 'NGC 6503',
        'color': '#6be847',
        'color_dim': '#6be84740',
        'data': [
            (0.5,30,5),(1,55,4),(1.5,72,4),(2,85,3),(2.5,94,3),
            (3,100,3),(3.5,104,3),(4,108,3),(5,113,3),(6,116,3),
            (7,118,3),(8,119,3),(9,120,3),(10,121,3),(11,121,4),
            (12,120,4),(13,120,5),(14,119,5),(15,118,6)
        ],
    },
]


def fit_galaxy(gal):
    """Fit a smooth mass model to each galaxy's decoded masses."""
    data = gal['data']
    r_obs = np.array([d[0] for d in data])
    v_obs = np.array([d[1] for d in data])
    M_obs = np.array([mass_decode(r, v) for r, v in zip(r_obs, v_obs)])

    name = gal['name']

    if name == 'M33':
        # Two-component: bulge + extended disk
        try:
            p, _ = curve_fit(two_comp_mass, r_obs, M_obs,
                             p0=[5e5, 1, 2e7, 6],
                             bounds=([0, 0.1, 0, 0.5], [1e8, 10, 1e9, 50]),
                             maxfev=20000)
            gal['model'] = 'two_comp'
            gal['params'] = p
            gal['M_total'] = p[0] + p[2]
        except Exception:
            gal['model'] = 'single'
            p, _ = curve_fit(single_comp_mass, r_obs, M_obs,
                             p0=[2e7, 5, 1.5],
                             bounds=([1e5, 0.1, 0.5], [1e9, 50, 5]),
                             maxfev=20000)
            gal['params'] = p
            gal['M_total'] = p[0]
    else:
        # Single component
        try:
            p, _ = curve_fit(single_comp_mass, r_obs, M_obs,
                             p0=[M_obs[-1] * 1.2, 5, 1.5],
                             bounds=([1e5, 0.1, 0.5], [1e10, 50, 5]),
                             maxfev=20000)
            gal['model'] = 'single'
            gal['params'] = p
            gal['M_total'] = p[0]
        except Exception:
            # Fallback
            gal['model'] = 'single'
            gal['params'] = [M_obs[-1] * 1.2, 5, 1.5]
            gal['M_total'] = M_obs[-1] * 1.2


def smooth_v(gal, r):
    """Compute smooth model velocity at radius r."""
    if r <= 0.001:
        return 0.0
    r_abs = abs(r)
    if gal['model'] == 'two_comp':
        Mr = two_comp_mass(r_abs, *gal['params'])
    else:
        Mr = single_comp_mass(r_abs, *gal['params'])
    Mr = max(Mr, 1.0)
    gN = G * Mr / r_abs**2
    return v_from_gN(r_abs, gN)


def obs_v_interp(gal, r):
    """Interpolated velocity from observations (the direct pipeline)."""
    data = gal['data']
    r_abs = abs(r)
    rs = [d[0] for d in data]
    vs = [d[1] for d in data]
    if r_abs <= rs[0]:
        return vs[0] * r_abs / rs[0]
    if r_abs >= rs[-1]:
        return vs[-1]
    return float(np.interp(r_abs, rs, vs))


def compute_stats(gal):
    """Compute field contribution stats for a galaxy."""
    data = gal['data']
    inner_r, inner_v = data[0][0], data[0][1]
    outer_r, outer_v = data[-1][0], data[-1][1]

    B_inner = boost_factor(inner_r, inner_v)
    B_outer = boost_factor(outer_r, outer_v)
    F_inner = field_fraction(inner_r, inner_v)
    F_outer = field_fraction(outer_r, outer_v)

    # Average field fraction across all points
    F_avg = np.mean([field_fraction(d[0], d[1]) for d in data])

    # Is the interior boosting or braking?
    # Boost: field adds to acceleration (always true for galaxies)
    # The question is how MUCH
    if B_inner > 1:
        mode = 'BOOST'
    else:
        mode = 'BOOST'  # field always adds, never subtracts in rotation curves

    # RMS of smooth model
    residuals = []
    within_1s = 0
    for r, v, dv in data:
        vp = smooth_v(gal, r)
        residuals.append(vp - v)
        if abs(vp - v) <= dv:
            within_1s += 1
    rms = math.sqrt(sum(r**2 for r in residuals) / len(residuals))

    return {
        'B_inner': B_inner, 'B_outer': B_outer,
        'F_inner': F_inner, 'F_outer': F_outer,
        'F_avg': F_avg, 'mode': mode,
        'rms': rms, 'within_1s': within_1s, 'total': len(data),
    }


# =============================================================================
# FIT ALL GALAXIES
# =============================================================================

for gal in galaxies:
    fit_galaxy(gal)
    gal['stats'] = compute_stats(gal)

# =============================================================================
# PLOTTING
# =============================================================================

# Style
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
fig.subplots_adjust(left=0.05, right=0.97, top=0.88, bottom=0.12, wspace=0.22)

# Title
fig.text(0.5, 0.95, 'GFD Galactic Vortex — Velocity Configuration',
         ha='center', va='center', fontsize=16, fontweight='bold',
         color='white', fontfamily='serif')
fig.text(0.5, 0.915, 'TetB (subspace)  ←  Field Origin  →  TetA (our spacetime)',
         ha='center', va='center', fontsize=9, color='#6b7084',
         fontfamily='monospace')

for idx, (ax, gal) in enumerate(zip(axes, galaxies)):
    data = gal['data']
    color = gal['color']
    stats = gal['stats']
    r_max_obs = data[-1][0]
    r_max_plot = r_max_obs * 1.15
    v_max = max(d[1] + d[2] for d in data) * 1.2

    # Axis range: symmetric about 0
    ax.set_xlim(-r_max_plot, r_max_plot)
    ax.set_ylim(0, v_max)

    # Region shading
    ax.axvspan(0, r_max_plot, color='#47b8e8', alpha=0.015)
    ax.axvspan(-r_max_plot, 0, color='#e87247', alpha=0.015)

    # Grid
    ax.grid(True, alpha=0.3, linewidth=0.5)

    # Center line (Field Origin)
    ax.axvline(0, color='#e8c547', linewidth=1.2, linestyle='--', alpha=0.35, zorder=2)

    # --- FIELD ORIGIN BOUNDARY AND HORIZON ---
    M_total = gal['M_total']
    R_boundary = math.sqrt(2 * G * M_total / A0)
    R_horizon = D * R_boundary

    for R, label, ls, alpha_val in [(R_boundary, 'FO', ':', 0.4),
                                     (R_horizon, 'H', '-.', 0.25)]:
        if R < r_max_plot:
            ax.axvline(R, color=color, linewidth=1, linestyle=ls, alpha=alpha_val, zorder=2)
            ax.axvline(-R, color=color, linewidth=1, linestyle=ls, alpha=alpha_val, zorder=2)
            ax.text(R, v_max * 0.97, label, ha='center', va='top', fontsize=7,
                    color=color, fontweight='bold', alpha=0.7)
            ax.text(-R, v_max * 0.97, label, ha='center', va='top', fontsize=7,
                    color=color, fontweight='bold', alpha=0.5)

    # --- SMOOTH VORTEX MODEL CURVE ---
    r_smooth = np.linspace(0.05, r_max_obs + 2, 300)
    v_smooth_teta = [smooth_v(gal, r) for r in r_smooth]
    v_smooth_tetb = [smooth_v(gal, r) for r in r_smooth]

    # TetA side (right): solid
    ax.plot(r_smooth, v_smooth_teta, color=color, linewidth=2.2,
            alpha=0.9, zorder=5, label='Smooth vortex model')

    # TetB side (left): dashed, dimmer
    ax.plot(-r_smooth, v_smooth_tetb, color=color, linewidth=2,
            alpha=0.35, linestyle='--', zorder=5)

    # --- DIRECT OBSERVATION-MAPPED CURVE (thin, through every point) ---
    r_obs_fine = np.linspace(data[0][0], data[-1][0], 200)
    v_obs_interp = [obs_v_interp(gal, r) for r in r_obs_fine]

    # TetA
    ax.plot(r_obs_fine, v_obs_interp, color=color, linewidth=0.8,
            alpha=0.4, zorder=4, label='Observation pipeline')
    # TetB
    ax.plot(-r_obs_fine, v_obs_interp, color=color, linewidth=0.6,
            alpha=0.15, zorder=4)

    # --- OBSERVATION POINTS WITH ERROR BARS ---
    r_pts = [d[0] for d in data]
    v_pts = [d[1] for d in data]
    dv_pts = [d[2] for d in data]

    # TetA side: filled circles
    ax.errorbar(r_pts, v_pts, yerr=dv_pts, fmt='o', color=color,
                markersize=4, capsize=2, capthick=0.8, linewidth=0.8,
                ecolor=color, elinewidth=0.8, alpha=0.8, zorder=6,
                markeredgecolor='#0a0c14', markeredgewidth=0.5)

    # TetB side: hollow circles, dimmer
    ax.errorbar([-r for r in r_pts], v_pts, yerr=dv_pts, fmt='o',
                color=color, markersize=3, capsize=1.5, capthick=0.5,
                linewidth=0.5, ecolor=color, elinewidth=0.5,
                alpha=0.2, zorder=6, markerfacecolor='none',
                markeredgewidth=0.8)

    # --- LABELS ---
    ax.set_xlabel('r  (kpc)', fontsize=9, labelpad=6)
    if idx == 0:
        ax.set_ylabel('v  (km/s)', fontsize=9, labelpad=6)

    # Galaxy name
    ax.text(0.5, 1.02, gal['name'], transform=ax.transAxes,
            ha='center', va='bottom', fontsize=13, fontweight='bold',
            color=color, fontfamily='serif')

    # --- STATS BOX (top left) ---
    F_inner_pct = stats['F_inner'] * 100
    F_outer_pct = stats['F_outer'] * 100
    F_avg_pct = stats['F_avg'] * 100

    stats_text = (
        f"Interior: {stats['mode']}\n"
        f"Field contribution:\n"
        f"  inner: {F_inner_pct:.0f}%\n"
        f"  outer: {F_outer_pct:.0f}%\n"
        f"  avg:   {F_avg_pct:.0f}%\n"
        f"─────────────\n"
        f"RMS: {stats['rms']:.1f} km/s\n"
        f"1σ: {stats['within_1s']}/{stats['total']}"
    )

    # Background box
    props = dict(boxstyle='round,pad=0.5', facecolor='#0a0c14',
                 edgecolor=color, alpha=0.8, linewidth=0.8)
    ax.text(0.03, 0.97, stats_text, transform=ax.transAxes,
            fontsize=7, verticalalignment='top', fontfamily='monospace',
            color='#c8ccd4', bbox=props)

    # --- REGION LABELS at bottom ---
    ax.text(0.22, 0.02, '◄ TetB', transform=ax.transAxes,
            fontsize=7, ha='center', color='#e87247', alpha=0.4)
    ax.text(0.78, 0.02, 'TetA ►', transform=ax.transAxes,
            fontsize=7, ha='center', color='#47b8e8', alpha=0.4)

    # Legend (small, bottom right)
    leg = ax.legend(loc='lower right', fontsize=6, framealpha=0.5,
                    facecolor='#10131f', edgecolor='#2a2d3a',
                    labelcolor='#8890a0')

# Bottom annotation
fig.text(0.5, 0.02,
         'v²(r) = ½[g_N·r + √((g_N·r)² + 4·g_N·r²·a₀)]   |   '
         'FO = Field Origin boundary (g_N = a₀/2)   |   '
         'H = Horizon (g_N = a₀/18)   |   '
         'Interior field contribution = 1/(x+1) where x = v²/(r·a₀)',
         ha='center', va='bottom', fontsize=7, color='#6b7084',
         fontfamily='monospace')

# Save
output_path = '/mnt/user-data/outputs/gfd_vortex_panels.png'
plt.savefig(output_path, dpi=150, facecolor='#0a0c14',
            edgecolor='none', bbox_inches='tight')
plt.close()

print(f"Saved: {output_path}")
print()

# Print stats summary
for gal in galaxies:
    s = gal['stats']
    print(f"{gal['name']:12s} | Interior: {s['mode']:5s} | "
          f"Field: {s['F_inner']*100:.0f}% → {s['F_outer']*100:.0f}% "
          f"(avg {s['F_avg']*100:.0f}%) | "
          f"RMS: {s['rms']:.1f} km/s | "
          f"1σ: {s['within_1s']}/{s['total']}")
