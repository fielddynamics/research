"""
================================================================================
Dual Tetrad Gravity And The Field Origin
Deriving Fundamental Equations With (3+1)^2 Topology
================================================================================

Figure 3: The Dark Matter Corrective Lens

This script generates the four-panel figure showing the dark matter resolution
from the (3+1)^2 framework. The panels are:

    Top left:     Rotation curves (Newton vs topology vs deep-MOND asymptote)
    Top right:    Correction factor mu(x) = x/(1+x) with regime shading
    Bottom left:  Force law transition from 1/r^2 to 1/r on log-log axes
    Bottom right: Apparent dark matter fraction vs radius

All calculations use CODATA 2022 fundamental constants.
Galaxy model: 10^11 solar masses, point-mass approximation.

Requirements: Python 3.6+, numpy, matplotlib
Author: Stephen Nelson
Date: February 2026
"""

import os
import numpy as np
import matplotlib.pyplot as plt


# =============================================================================
# FUNDAMENTAL CONSTANTS (CODATA 2022)
# =============================================================================

G = 6.67430e-11          # Gravitational constant [m^3/(kg*s^2)]
m_e = 9.1093837139e-31   # Electron mass [kg]
r_e = 2.8179403205e-15   # Classical electron radius [m]
c = 299792458            # Speed of light [m/s] (exact)
M_sun = 1.98892e30       # Solar mass [kg]


# =============================================================================
# TOPOLOGICAL PARAMETERS
# =============================================================================

k = 4                    # Simplex faces (d+1 for d=3)
k_squared = k ** 2       # Isotropic coupling channels = 16


# =============================================================================
# DERIVED SCALES
# =============================================================================

# Characteristic acceleration from (3+1)^2 topology
# Eq. (a0-dm) in the paper: a_0 = k^2 * G * m_e / r_e^2
a_0_derived = k_squared * G * m_e / r_e ** 2

# Empirical MOND acceleration scale (Milgrom 1983)
a_0_obs = 1.22e-10  # Empirical MOND acceleration scale [m/s^2]

# Agreement between derived and empirical
a_0_match = abs(a_0_derived - a_0_obs) / a_0_obs * 100


# =============================================================================
# GALAXY MODEL
# =============================================================================

M_galaxy = 1e11 * M_sun                     # 10^11 solar masses
r_kpc = np.linspace(1, 100, 200)             # Radius array [kpc]
r_m = r_kpc * 3.086e19                       # Convert kpc to meters


# =============================================================================
# PHYSICS CALCULATIONS
# =============================================================================

def compute_newtonian(r, M):
    """Compute Newtonian gravitational acceleration and circular velocity."""
    g = G * M / r ** 2
    v = np.sqrt(G * M / r) / 1000  # km/s
    return g, v


def compute_mu(g, a0):
    """
    Compute the correction factor mu(x) = x/(1+x).

    Derived from detailed balance in the (3+1)^2 closure model:
        Resolution rate:  W+ = kappa * x * (1 - epsilon)
        Relaxation rate:  W- = kappa * epsilon
        Equilibrium:      epsilon = x / (1 + x)

    Parameters
    ----------
    g : array_like
        Newtonian gravitational acceleration [m/s^2]
    a0 : float
        Characteristic acceleration scale [m/s^2]

    Returns
    -------
    x : array_like
        Dimensionless acceleration ratio g/a_0
    mu : array_like
        Correction factor, range (0, 1)
    """
    x = g / a0
    mu = x / (1 + x)
    return x, mu


def compute_corrected(g_newton, mu_values, r):
    """
    Compute corrected (actual) gravity and circular velocity.

    The effective gravity is g_eff = g_Newton / mu(x).
    In the deep-MOND regime (x << 1): g_eff = sqrt(g_Newton * a_0) ~ 1/r.
    In the Newtonian regime (x >> 1): g_eff = g_Newton ~ 1/r^2.
    """
    g_corrected = g_newton / mu_values
    v_corrected = np.sqrt(g_corrected * r) / 1000  # km/s
    return g_corrected, v_corrected


def compute_dark_matter_fraction(g_corrected, r, M_visible):
    """
    Compute apparent dark matter fraction.

    f_dark = 1 - mu(x) = 1/(1+x) = a_0/(g + a_0)

    This is what a Newtonian observer would attribute to invisible mass.
    """
    M_inferred = g_corrected * r ** 2 / G
    fraction = (M_inferred - M_visible) / M_inferred * 100
    return fraction


# =============================================================================
# RUN CALCULATIONS
# =============================================================================

# Newtonian baseline
g_newton, v_newton = compute_newtonian(r_m, M_galaxy)

# Structural correction
x, mu = compute_mu(g_newton, a_0_obs)

# Corrected values
g_corrected, v_corrected = compute_corrected(g_newton, mu, r_m)

# Dark matter fraction artifact
dark_matter_fraction = compute_dark_matter_fraction(g_corrected, r_m, M_galaxy)

# Deep-MOND asymptotic velocity: v = (G*M*a_0)^(1/4)
v_mond_asymptote = (G * M_galaxy * a_0_obs) ** 0.25 / 1000  # km/s


# =============================================================================
# PRINT NUMERICAL RESULTS
# =============================================================================

print("=" * 70)
print("Dual Tetrad Gravity And The Field Origin")
print("Figure 3: Dark Matter Corrective Lens")
print("=" * 70)
print()
print(f"Galaxy mass:           {M_galaxy:.2e} kg ({M_galaxy/M_sun:.0e} solar masses)")
print(f"a_0 (derived):         {a_0_derived:.6e} m/s^2")
print(f"a_0 (empirical):       {a_0_obs:.2e} m/s^2")
print(f"a_0 match:             {a_0_match:.2f}%")
print(f"MOND asymptotic v:     {v_mond_asymptote:.1f} km/s")
print()

# Print table matching paper Table (tab:darkmatter)
print(f"{'r (kpc)':>8} {'g/a_0':>8} {'mu(x)':>8} {'v_Newt':>10} {'v_actual':>10} {'DM%':>6}")
print("-" * 56)

for r_val in [5, 10, 20, 30, 50]:
    idx = np.argmin(np.abs(r_kpc - r_val))
    print(f"{r_kpc[idx]:>8.0f} {x[idx]:>8.2f} {mu[idx]:>8.2f} "
          f"{v_newton[idx]:>10.0f} {v_corrected[idx]:>10.0f} "
          f"{dark_matter_fraction[idx]:>5.0f}%")


# =============================================================================
# FIGURE GENERATION
# =============================================================================

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# -------------------------------------------------------------------------
# Panel 1 (top left): Rotation curves
# Shows: Newton (declining), Topology (rising/flat), MOND asymptote (flat)
# -------------------------------------------------------------------------
ax1 = axes[0, 0]
ax1.plot(r_kpc, v_newton, "r:", label="No Topology (Newton)", linewidth=2)
ax1.plot(r_kpc, v_corrected, "b-", label="Tetrad Topology (3+1)\u00b2", linewidth=2.5)
ax1.axhline(
    y=v_mond_asymptote, color="g", linestyle="-", label="MOND", linewidth=2
)
ax1.set_xlabel("Radius (kpc)", fontsize=12)
ax1.set_ylabel("Rotation velocity (km/s)", fontsize=12)
ax1.set_title("Rotation Curves: Structure Matters", fontsize=14)
ax1.legend(loc="upper right")
ax1.grid(True, alpha=0.3)
ax1.set_xlim(0, 100)
ax1.set_ylim(0, 700)

# -------------------------------------------------------------------------
# Panel 2 (top right): Correction factor mu(x)
# Shows: mu(x) = x/(1+x) with enhanced (red) and Newtonian (blue) regimes
# -------------------------------------------------------------------------
ax2 = axes[0, 1]
x_plot = np.logspace(-2, 2, 100)
mu_plot = x_plot / (1 + x_plot)

ax2.semilogx(x_plot, mu_plot, "k-", linewidth=2)
ax2.axhline(y=1, color="b", linestyle="--", alpha=0.5, label="Newton limit")
ax2.axvline(x=1, color="r", linestyle="--", alpha=0.5, label="Transition (g = a_0)")
ax2.fill_between(
    x_plot[x_plot < 1], 0, mu_plot[x_plot < 1],
    alpha=0.2, color="red", label="Enhanced regime"
)
ax2.fill_between(
    x_plot[x_plot > 1], 0, mu_plot[x_plot > 1],
    alpha=0.2, color="blue", label="Newtonian regime"
)
ax2.set_xlabel("x = g/a_0", fontsize=12)
ax2.set_ylabel("mu(x) = correction factor", fontsize=12)
ax2.set_title("The Corrective Lens: mu(x) = x/(1+x)", fontsize=14)
ax2.legend()
ax2.grid(True, alpha=0.3)
ax2.set_ylim(0, 1.1)

# -------------------------------------------------------------------------
# Panel 3 (bottom left): Force law comparison on log-log axes
# Shows: Newton 1/r^2, MOND 1/r, and the smooth topology transition
# -------------------------------------------------------------------------
ax3 = axes[1, 0]
r_norm = r_kpc / 30  # Normalize to typical galaxy scale

# Newton: 1/r^2
g_newton_norm = 1 / r_norm ** 2
ax3.loglog(r_norm, g_newton_norm, "r:", label="No Topology (Newton 1/r\u00b2)", linewidth=2)

# Deep-MOND limit: 1/r
g_mond_limit = 1 / r_norm
ax3.loglog(r_norm, g_mond_limit, "g-", label="MOND (1/r)", linewidth=2)

# Topology: smooth transition via mu(x)
g_actual_norm = g_corrected / g_corrected[0]
ax3.loglog(r_norm, g_actual_norm, "b-", label="Tetrad Topology (3+1)\u00b2", linewidth=2.5)

ax3.axvline(x=1, color="gray", linestyle=":", alpha=0.5, label="Transition scale")
ax3.set_xlabel("Normalized radius (r/r\u2080)", fontsize=12)
ax3.set_ylabel("Normalized acceleration", fontsize=12)
ax3.set_title("How Gravity Weakens With Distance", fontsize=14)
ax3.legend(loc="lower left", fontsize=9)
ax3.grid(True, alpha=0.3)

# Regime annotations
ax3.text(0.15, 150, "1/r\u00b2 regime\n(high g)", fontsize=9, color="red", ha="center")
ax3.text(2.5, 0.6, "1/r regime\n(low g)", fontsize=9, color="green", ha="center")

# -------------------------------------------------------------------------
# Panel 4 (bottom right): Apparent dark matter fraction
# Shows: Grey area = Newtonian inference, blue line at 0 = topology answer
# -------------------------------------------------------------------------
ax4 = axes[1, 1]

# Newtonian inference (the artifact)
ax4.fill_between(r_kpc, 0, dark_matter_fraction, alpha=0.3, color="gray")
ax4.plot(
    r_kpc, dark_matter_fraction, color="gray", linestyle=":", linewidth=2.5,
    label="Newtonian gravity (1/r\u00b2)"
)

# Cited dark matter fraction
ax4.axhline(y=85, color="dimgray", linestyle="-", linewidth=2.5, label="Cited dark matter fraction (85%)")

# Corrected gravity: nothing missing
ax4.axhline(y=0, color="blue", linestyle="-", linewidth=3, label="Corrected gravity (1/r\u00b2 \u2192 1/r)")
ax4.fill_between(r_kpc, -5, 0, alpha=0.15, color="blue")

ax4.set_xlabel("Radius (kpc)", fontsize=12)
ax4.set_ylabel("Mass Unaccounted For (%)", fontsize=12)
ax4.set_title("Is Mass Really Missing?", fontsize=14)
ax4.legend(loc="center right", fontsize=10, framealpha=0.95)
ax4.grid(True, alpha=0.3)
ax4.set_xlim(0, 100)
ax4.set_ylim(-5, 100)

# Annotations
ax4.text(
    5, 97, "Newton says ~95%\nis missing",
    fontsize=9, color="gray", style="italic", va="top"
)
ax4.text(
    5, 12, "Corrected law:\nnothing is missing",
    fontsize=9, color="blue", style="italic", va="top"
)

# -------------------------------------------------------------------------
# Save figure
# -------------------------------------------------------------------------
plt.tight_layout()

# Save to current directory (Paper VII folder)
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dark_matter_corrective_lens.png")
plt.savefig(output_path, dpi=150, bbox_inches="tight")
print(f"\nFigure saved: {output_path}")

print("\nDone.")
