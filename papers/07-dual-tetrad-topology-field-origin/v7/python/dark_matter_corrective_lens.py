"""
================================================================================
Dual Tetrad Topology and the Field Origin:
From Nuclear Decay to Galactic Dynamics

Bidirectional Validation of a Zero-Parameter Gravitational Field Theory
================================================================================

Figure 3: The Dark Matter Corrective Lens

This script generates the four-panel figure showing the dark matter resolution
from the (3+1)^2 framework. The panels are:

    Top left:     Rotation curves (Newton vs topology vs classical MOND)
    Top right:    Correction factor mu(x) = x/(1+x) with regime shading
    Bottom left:  Force law transition from 1/r^2 to 1/r on log-log axes
    Bottom right: Apparent dark matter fraction vs radius

All calculations use CODATA 2022 fundamental constants.

Galaxy model: Milky Way -- 3-component baryonic mass distribution
  Bulge: 1.5e10 M_sun Hernquist profile, a=0.6 kpc
         (Bland-Hawthorn & Gerhard 2016, ARAA 54, 529)
  Disk:  5.0e10 M_sun exponential, Rd=2.5 kpc
         (McMillan 2017, MNRAS 465, 76)
  Gas:   1.0e10 M_sun exponential, Rd=5.0 kpc (HI+H2+He)
         (Kalberla & Kerp 2009, ARAA 47, 27)
  Total: 7.5e10 M_sun (independently measured, not fitted)

Physics:
  - Newtonian: v_c = sqrt(G * M(<r) / r)
  - DTG (Tetrad Topology): AQUAL field equation mu(x)*x = y_N
    with mu(x) = x/(1+x) from topological closure, solved analytically
    x = (y_N + sqrt(y_N^2 + 4*y_N))/2
  - Classical MOND: AQUAL field equation with mu(x) = x/sqrt(1+x^2)
    (Bekenstein & Milgrom 1984), same a0, no dark matter
    x^2 = (y_N^2 + sqrt(y_N^4 + 4*y_N^2))/2

No dark matter halos are used anywhere. All curves derive from
baryonic mass alone plus the gravitational field equation.

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
kpc_to_m = 3.0857e19     # Kiloparsec to meters


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

# Use the topologically derived value for all calculations
a_0 = a_0_derived


# =============================================================================
# MILKY WAY BARYONIC MASS MODEL (independently measured, no dark matter)
# =============================================================================

# Component masses (solar masses)
M_bulge_solar = 1.5e10   # Stellar bulge
M_disk_solar = 5.0e10    # Stellar disk
M_gas_solar = 1.0e10     # Cold gas disk (HI + H2 + He)
M_total_solar = M_bulge_solar + M_disk_solar + M_gas_solar  # 7.5e10

# Component scale lengths (kpc)
a_bulge_kpc = 0.6        # Hernquist scale radius
Rd_disk_kpc = 2.5        # Exponential disk scale length
Rd_gas_kpc = 5.0         # Gas disk scale length (more extended)

# Convert to SI
M_bulge = M_bulge_solar * M_sun
M_disk = M_disk_solar * M_sun
M_gas = M_gas_solar * M_sun
M_total = M_total_solar * M_sun

a_bulge = a_bulge_kpc * kpc_to_m
Rd_disk = Rd_disk_kpc * kpc_to_m
Rd_gas = Rd_gas_kpc * kpc_to_m


def M_enclosed(r):
    """
    Total baryonic mass enclosed within radius r (meters).

    Three components, all independently measured:
      1. Hernquist bulge: M(<r) = M * r^2 / (r + a)^2
      2. Exponential stellar disk: M(<r) = M * [1 - (1+r/Rd)*exp(-r/Rd)]
      3. Exponential gas disk: same form, different scale length

    No dark matter. No free parameters fitted to rotation curves.
    """
    # Stellar bulge (Hernquist 1990)
    M_b_enc = M_bulge * r**2 / (r + a_bulge)**2

    # Stellar disk (exponential)
    x_d = r / Rd_disk
    M_d_enc = M_disk * (1.0 - (1.0 + x_d) * np.exp(-x_d))

    # Cold gas disk (exponential, more extended)
    x_g = r / Rd_gas
    M_g_enc = M_gas * (1.0 - (1.0 + x_g) * np.exp(-x_g))

    return M_b_enc + M_d_enc + M_g_enc


# =============================================================================
# AQUAL FIELD EQUATION SOLVERS
# =============================================================================

def solve_x_dtg(yN):
    """
    Solve AQUAL field equation for DTG: mu(x)*x = y_N with mu(x) = x/(1+x).

    The equation x^2/(1+x) = y_N has the analytic solution:
        x = (y_N + sqrt(y_N^2 + 4*y_N)) / 2

    This is the static equilibrium of the full wave equation
    Box(Phi) - nabla*[mu(|nabla Phi|/a0)*nabla Phi] = 4*pi*G*rho
    where Box = (1/c^2)*d^2/dt^2 - nabla^2 propagates at speed c.

    Parameters
    ----------
    yN : array_like
        Newtonian acceleration ratio y_N = g_N / a_0

    Returns
    -------
    x : array_like
        True acceleration ratio x = g / a_0
    """
    yN = np.asarray(yN, dtype=float)
    return np.where(
        yN < 1e-30,
        0.0,
        (yN + np.sqrt(yN * yN + 4.0 * yN)) / 2.0
    )


def solve_x_mond(yN):
    """
    Solve AQUAL field equation for classical MOND:
    mu(x)*x = y_N with mu(x) = x/sqrt(1+x^2).

    The equation x^2/sqrt(1+x^2) = y_N gives:
        x^2 = (y_N^2 + sqrt(y_N^4 + 4*y_N^2)) / 2

    Same AQUAL variational framework, different interpolating function.
    No dark matter corrections anywhere.

    Parameters
    ----------
    yN : array_like
        Newtonian acceleration ratio y_N = g_N / a_0

    Returns
    -------
    x : array_like
        True acceleration ratio x = g / a_0
    """
    yN = np.asarray(yN, dtype=float)
    y2 = yN * yN
    discriminant = y2 * y2 + 4.0 * y2
    x_squared = np.where(
        yN < 1e-30,
        0.0,
        (y2 + np.sqrt(discriminant)) / 2.0
    )
    return np.sqrt(x_squared)


def mu_dtg(x):
    """DTG constitutive law: mu(x) = x/(1+x)."""
    return x / (1.0 + x)


def mu_mond_func(x):
    """Classical MOND interpolating function: mu(x) = x/sqrt(1+x^2)."""
    return x / np.sqrt(1.0 + x * x)


# =============================================================================
# GALAXY MODEL: RADIUS ARRAY
# =============================================================================

r_kpc = np.linspace(0.5, 100, 400)    # Radius array [kpc]
r_m = r_kpc * kpc_to_m                # Convert kpc to meters


# =============================================================================
# MILKY WAY OBSERVATIONAL DATA (for rotation curve panel)
# =============================================================================
# Observed circular velocity at selected galactocentric radii.
# Compiled from three independent kinematic surveys:
#
#   1. Eilers et al. 2019, ApJ 871, 120
#      - Luminous red giant branch stars, Gaia DR2 + APOGEE
#      - Provides the 5--25 kpc range with small statistical errors
#   2. Jiao et al. 2023, A&A 678, A208
#      - Gaia DR3 astrometry, independent cross-check
#   3. Sofue 2020, Galaxies 8, 37
#      - Inner-galaxy terminal-velocity compilation (< 5 kpc)
#
# Each entry: (radius [kpc], v_c [km/s], 1-sigma error [km/s])
# These are the same data points used in the GRAVIS rotation-curve tool.
obs_r_kpc = np.array([2,   5,   8,  10,  15,  20,  25 ])   # kpc
obs_v_kms = np.array([206, 236, 230, 228, 221, 213, 200])   # km/s
obs_err   = np.array([25,  7,   3,   5,   7,   10,  15 ])   # km/s


# =============================================================================
# PHYSICS CALCULATIONS (all use distributed baryonic mass, no dark matter)
# =============================================================================

# Enclosed baryonic mass at each radius
M_enc = np.array([M_enclosed(r) for r in r_m])

# Newtonian gravitational acceleration from baryons alone
g_newton = G * M_enc / r_m ** 2

# Newtonian circular velocity (no dark matter)
v_newton = np.sqrt(G * M_enc / r_m) / 1000  # km/s

# DTG (Tetrad Topology): AQUAL solver with mu(x) = x/(1+x)
yN_dtg = g_newton / a_0
x_dtg = solve_x_dtg(yN_dtg)
g_dtg = a_0 * x_dtg
v_dtg = np.sqrt(g_dtg * r_m) / 1000  # km/s

# Classical MOND: AQUAL solver with mu(x) = x/sqrt(1+x^2)
yN_mond = g_newton / a_0
x_mond = solve_x_mond(yN_mond)
g_mond = a_0 * x_mond
v_mond = np.sqrt(g_mond * r_m) / 1000  # km/s

# DTG correction factor at each radius
mu_values_dtg = mu_dtg(x_dtg)

# Dark matter fraction: what a Newtonian observer would infer
# f_dark = 1 - M_visible / M_inferred = 1 - g_N / g_eff = 1 - mu(x)
dark_matter_fraction = (1.0 - mu_values_dtg) * 100


# =============================================================================
# PRINT NUMERICAL RESULTS
# =============================================================================

print("=" * 70)
print("Dual Tetrad Gravity And The Field Origin")
print("Figure 3: Dark Matter Corrective Lens")
print("=" * 70)
print()
print("Galaxy: Milky Way (3-component baryonic mass, no dark matter)")
print(f"  Bulge: {M_bulge_solar:.1e} M_sun (Hernquist, a={a_bulge_kpc} kpc)")
print(f"  Disk:  {M_disk_solar:.1e} M_sun (exponential, Rd={Rd_disk_kpc} kpc)")
print(f"  Gas:   {M_gas_solar:.1e} M_sun (exponential, Rd={Rd_gas_kpc} kpc)")
print(f"  Total: {M_total_solar:.1e} M_sun")
print()
print(f"a_0 (derived):         {a_0_derived:.6e} m/s^2")
print(f"a_0 (empirical):       {a_0_obs:.2e} m/s^2")
print(f"a_0 match:             {a_0_match:.2f}%")
print()

# Observational data summary
print("Observational rotation curve data (7 points):")
print(f"  {'r(kpc)':>7}  {'v_obs(km/s)':>11}  {'err(km/s)':>9}  Source")
print("  " + "-" * 55)
obs_sources = [
    "Sofue 2020 (inner region)",
    "Eilers+2019 / Sofue 2020",
    "Eilers+2019 (solar circle)",
    "Eilers+2019",
    "Eilers+2019",
    "Eilers+2019 / Jiao+2023",
    "Jiao+2023 (Gaia DR3 outer)",
]
for i in range(len(obs_r_kpc)):
    print(f"  {obs_r_kpc[i]:>7.0f}  {obs_v_kms[i]:>11.0f}  "
          f"+/-{obs_err[i]:<6.0f}  {obs_sources[i]}")
print()

# Print comparison table
print(f"{'r(kpc)':>7} {'M_enc':>11} {'g/a0':>7} {'mu_DTG':>7} "
      f"{'v_Newt':>7} {'v_DTG':>7} {'v_MOND':>7} {'DM%':>5}")
print("-" * 68)

for r_val in [1, 2, 5, 8, 10, 15, 20, 25, 30, 50, 75, 100]:
    idx = np.argmin(np.abs(r_kpc - r_val))
    m_enc_solar = M_enc[idx] / M_sun
    print(f"{r_kpc[idx]:>7.1f} {m_enc_solar:>11.2e} {x_dtg[idx]:>7.2f} "
          f"{mu_values_dtg[idx]:>7.3f} "
          f"{v_newton[idx]:>7.1f} {v_dtg[idx]:>7.1f} {v_mond[idx]:>7.1f} "
          f"{dark_matter_fraction[idx]:>5.1f}")


# =============================================================================
# FIGURE GENERATION
# =============================================================================

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# -------------------------------------------------------------------------
# Panel 1 (top left): Rotation curves with observational data
# Shows: Newton (declining), Topology (flat), Classical MOND (flat)
# All from baryonic mass alone -- no dark matter anywhere
# Observational points from Eilers+2019, Jiao+2023, Sofue 2020
# -------------------------------------------------------------------------
ax1 = axes[0, 0]
ax1.plot(r_kpc, v_newton, "r:", label="No Topology (Newton)", linewidth=2)
ax1.plot(r_kpc, v_dtg, "b-", label=r"Tetrad Topology $(3{+}1)^2$", linewidth=2.5)
ax1.plot(r_kpc, v_mond, "g-", label="MOND", linewidth=2)
ax1.errorbar(obs_r_kpc, obs_v_kms, yerr=obs_err,
             fmt="o", color="goldenrod", markersize=6, capsize=4,
             capthick=1.5, elinewidth=1.5, markeredgecolor="black",
             markeredgewidth=0.8, label="Observed (Eilers+19, Jiao+23)",
             zorder=5)
ax1.set_xlabel("Radius (kpc)", fontsize=12)
ax1.set_ylabel("Rotation velocity (km/s)", fontsize=12)
ax1.set_title("Rotation Curves: Structure Matters", fontsize=14)
ax1.legend(loc="upper right", fontsize=8)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(0, 30)
ax1.set_ylim(0, 300)

# -------------------------------------------------------------------------
# Panel 2 (top right): Correction factor mu(x)
# Shows: DTG mu(x) = x/(1+x) and MOND mu(x) = x/sqrt(1+x^2)
# with enhanced (red) and Newtonian (blue) regimes
# -------------------------------------------------------------------------
ax2 = axes[0, 1]
x_plot = np.logspace(-2, 2, 200)
mu_dtg_plot = x_plot / (1.0 + x_plot)
mu_mond_plot = x_plot / np.sqrt(1.0 + x_plot * x_plot)

ax2.semilogx(x_plot, mu_dtg_plot, "b-", linewidth=2.5,
             label="Tetrad Topology: x/(1+x)")
ax2.semilogx(x_plot, mu_mond_plot, "g-", linewidth=2,
             label="Classical MOND: x/sqrt(1+x^2)")
ax2.axhline(y=1, color="gray", linestyle="--", alpha=0.5, label="Newton limit")
ax2.axvline(x=1, color="r", linestyle="--", alpha=0.5, label="Transition (g = a_0)")
ax2.fill_between(
    x_plot[x_plot < 1], 0, mu_dtg_plot[x_plot < 1],
    alpha=0.15, color="red", label="Enhanced regime"
)
ax2.fill_between(
    x_plot[x_plot > 1], 0, mu_dtg_plot[x_plot > 1],
    alpha=0.15, color="blue", label="Newtonian regime"
)
ax2.set_xlabel("x = g/a_0", fontsize=12)
ax2.set_ylabel("mu(x) = correction factor", fontsize=12)
ax2.set_title("The Corrective Lens: mu(x) = x/(1+x)", fontsize=14)
ax2.legend(fontsize=8)
ax2.grid(True, alpha=0.3)
ax2.set_ylim(0, 1.1)

# -------------------------------------------------------------------------
# Panel 3 (bottom left): Force law comparison on log-log axes
# Shows: Newton 1/r^2, MOND 1/r, and the smooth topology transition
# All from distributed baryonic mass
# -------------------------------------------------------------------------
ax3 = axes[1, 0]
r_norm = r_kpc / 30  # Normalize to typical galaxy scale

# Newtonian effective force law (from distributed mass)
g_newton_norm = g_newton / g_newton[0]
ax3.loglog(r_norm, g_newton_norm, "r:", label=r"No Topology (Newton $1/r^2$)", linewidth=2)

# Deep-MOND asymptotic limit: 1/r
# Normalize to match at first point
g_deep_mond = 1.0 / r_norm
g_deep_mond = g_deep_mond * (g_newton_norm[0] / g_deep_mond[0])
ax3.loglog(r_norm, g_deep_mond, "g--", label="Deep MOND (1/r)", linewidth=1.5, alpha=0.7)

# Topology: effective force from AQUAL solver
g_dtg_norm = g_dtg / g_dtg[0]
ax3.loglog(r_norm, g_dtg_norm, "b-", label=r"Tetrad Topology $(3{+}1)^2$", linewidth=2.5)

ax3.axvline(x=1, color="gray", linestyle=":", alpha=0.5, label="Transition scale")
ax3.set_xlabel("Normalized radius (r/r_0)", fontsize=12)
ax3.set_ylabel("Normalized acceleration", fontsize=12)
ax3.set_title("How Gravity Weakens With Distance", fontsize=14)
ax3.legend(loc="lower left", fontsize=9)
ax3.grid(True, alpha=0.3)

# Regime annotations (use axes transform to place reliably within panel)
ax3.text(0.18, 0.72, r"$1/r^2$ regime" + "\n(high g)", fontsize=9, color="red",
         ha="center", transform=ax3.transAxes)
ax3.text(0.82, 0.32, r"$1/r$ regime" + "\n(low g)", fontsize=9, color="green",
         ha="center", transform=ax3.transAxes)

# -------------------------------------------------------------------------
# Panel 4 (bottom right): Apparent dark matter fraction
# Shows: Grey area = Newtonian inference, blue line at 0 = topology answer
# -------------------------------------------------------------------------
ax4 = axes[1, 1]

# Newtonian inference (the artifact): what you'd conclude if gravity is 1/r^2
ax4.fill_between(r_kpc, 0, dark_matter_fraction, alpha=0.3, color="gray")
ax4.plot(
    r_kpc, dark_matter_fraction, color="gray", linestyle=":", linewidth=2.5,
    label=r"Newtonian gravity ($1/r^2$)"
)

# Cited dark matter fraction
ax4.axhline(y=85, color="dimgray", linestyle="-", linewidth=2.5, label="Cited dark matter fraction (85%)")

# Corrected gravity: nothing missing
ax4.axhline(y=0, color="blue", linestyle="-", linewidth=3, label=r"Corrected gravity ($1/r^2 \to 1/r$)")
ax4.fill_between(r_kpc, -5, 0, alpha=0.15, color="blue")

ax4.set_xlabel("Radius (kpc)", fontsize=12)
ax4.set_ylabel("Mass Unaccounted For (%)", fontsize=12)
ax4.set_title("Is Mass Really Missing?", fontsize=14)
ax4.legend(loc="center right", fontsize=10, framealpha=0.95)
ax4.grid(True, alpha=0.3)
ax4.set_xlim(0, 30)
ax4.set_ylim(-5, 100)

# Annotations
ax4.text(
    5, 97, "Newton says mass\nis missing",
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
