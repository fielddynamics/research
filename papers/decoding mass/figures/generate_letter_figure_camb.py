"""
Four-panel CamB figure (Figure 2): rotation curve, enclosed mass, mass deficit,
and power output. Hardcoded CamB data from SPARC Lelli+2016.

For submission, Figure 2 is generated together with Figures 1 and 3 by
generate_letter_figures.py. This script remains available for standalone
regeneration of the CamB figure only.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy.ndimage import gaussian_filter1d

# ---------------------------------------------------------------------------
# Physical constants (SI)
# ---------------------------------------------------------------------------
G = 6.674e-11
A0 = 1.2e-10
MSUN = 1.989e30
KPC = 3.086e19

# ---------------------------------------------------------------------------
# CamB data (SPARC Lelli+2016)
# ---------------------------------------------------------------------------
r_obs = np.array([0.16, 0.41, 0.57, 0.73, 0.90, 1.06, 1.22, 1.47, 1.79])
v_obs = np.array([1.99, 4.84, 6.79, 8.87, 10.9, 12.9, 14.7, 16.8, 20.1])
e_obs = np.array([1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5])

# Mass model: disk + gas (bulge M=0)
DISK_M = 3.75e7 * MSUN;  DISK_Rd = 1.0 * KPC
GAS_M  = 6.251e8 * MSUN;  GAS_Rd  = 26.48 * KPC

def camb_M_enc(r):
    """Enclosed mass for CamB: exponential disk + gas. r in metres."""
    # Exponential disk
    xd = r / DISK_Rd
    m_disk = DISK_M * (1 - (1 + xd) * np.exp(-xd))
    # Exponential gas disk
    xg = r / GAS_Rd
    m_gas = GAS_M * (1 - (1 + xg) * np.exp(-xg))
    return m_disk + m_gas

# ---------------------------------------------------------------------------
# NFW halo for ΛCDM comparison (abundance matching for low-mass galaxy)
# ---------------------------------------------------------------------------
def abundance_matching_simple(m_bary_msun):
    """Simple Behroozi-style abundance matching: M200 from baryonic mass."""
    # For a ~6.6e8 Msun baryonic galaxy, M200 ~ 2e10 Msun is reasonable
    log_mb = np.log10(m_bary_msun)
    # Approximate relation
    log_m200 = 1.5 * (log_mb - 10.0) + 12.0
    log_m200 = max(log_m200, log_mb + 1.0)  # at least 10x baryonic
    return 10**log_m200

def nfw_enclosed_mass_simple(r_kpc, m200_msun):
    """NFW enclosed mass given M200 in Msun. Returns mass in kg."""
    # Concentration from Dutton-Maccio 2014
    log_c = 0.905 - 0.101 * (np.log10(m200_msun) - 12.0)
    c = 10**log_c
    # r200 from M200
    rho_crit = 1.27e-26  # kg/m^3 (z=0)
    M200_kg = m200_msun * MSUN
    r200 = (3 * M200_kg / (4 * np.pi * 200 * rho_crit))**(1.0/3.0)
    rs = r200 / c
    rho0 = M200_kg / (4 * np.pi * rs**3 * (np.log(1 + c) - c / (1 + c)))
    r_m = r_kpc * KPC
    x = r_m / rs
    return 4 * np.pi * rho0 * rs**3 * (np.log(1 + x) - x / (1 + x))

m_bary_total = (3.75e7 + 6.251e8)  # Msun
m200 = abundance_matching_simple(m_bary_total)

# ---------------------------------------------------------------------------
# Physics pipeline (same as generate_fig2_galaxy.py)
# ---------------------------------------------------------------------------
def diffraction_smooth(r_obs, v_obs, frac=0.062):
    r_fine = np.linspace(r_obs[0], r_obs[-1], 1000)
    v_fine = np.interp(r_fine, r_obs, v_obs)
    dr = r_fine[1] - r_fine[0]
    sigma_r = frac * (r_obs[-1] - r_obs[0])
    sigma_pts = sigma_r / dr
    v_smooth = gaussian_filter1d(v_fine, sigma=sigma_pts)
    return np.interp(r_obs, r_fine, v_smooth)

def velocity_decode(r_obs_kpc, v_obs_km, r_fine_kpc):
    r_o = r_obs_kpc * KPC
    v_o = v_obs_km * 1e3
    r_fine = r_fine_kpc * KPC
    v = np.interp(r_fine, r_o, v_o)
    gt = v**2 / r_fine
    gs = gt**2 / (A0 + gt)
    M_dec = gs * r_fine**2 / G
    gs2 = G * M_dec / r_fine**2
    gt2 = (gs2 + np.sqrt(gs2**2 + 4 * gs2 * A0)) / 2.0
    v_dec = np.sqrt(r_fine * gt2) / 1e3
    return v_dec, M_dec

def forward_gfd(r_kpc, M_enc_func):
    r = r_kpc * KPC
    M = M_enc_func(r)
    v_newt = np.sqrt(G * M / r) / 1e3
    gs = G * M / r**2
    gt = (gs + np.sqrt(gs**2 + 4 * gs * A0)) / 2.0
    v_gfd = np.sqrt(r * gt) / 1e3
    return v_newt, v_gfd, M

# ---------------------------------------------------------------------------
# Compute all curves
# ---------------------------------------------------------------------------
r_span = r_obs[-1] - r_obs[0]
r_model = np.linspace(0.1, r_obs[-1] + 0.15 * r_span, 600)
r_decode = np.linspace(r_obs[0], r_obs[-1], 500)

v_newt, v_gfd, M_phot = forward_gfd(r_model, camb_M_enc)
v_smooth = diffraction_smooth(r_obs, v_obs, frac=0.062)
v_dec, M_dec = velocity_decode(r_obs, v_smooth, r_decode)

# CDM curve
M_nfw = np.array([nfw_enclosed_mass_simple(float(rk), m200) for rk in r_model])
M_cdm = camb_M_enc(r_model * KPC) + M_nfw
v_cdm = np.sqrt(G * M_cdm / (r_model * KPC)) / 1e3

# Power output / mass deficit — observation-based only
M_phot_on_decode = np.interp(r_decode, r_model, M_phot / MSUN)
M_dec_Msun = M_dec / MSUN
Delta_M = M_phot_on_decode - M_dec_Msun  # Equation from the letter

# ---------------------------------------------------------------------------
# Figure: 4-panel (2x2)
# ---------------------------------------------------------------------------
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 9,
    "axes.labelsize": 10,
    "legend.fontsize": 6.5,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "figure.dpi": 300,
    "savefig.dpi": 300,
})

fig = plt.figure(figsize=(8.5, 6.0))
gs = GridSpec(2, 2, hspace=0.36, wspace=0.36,
              left=0.10, right=0.96, top=0.94, bottom=0.08)

# =========================================================================
# Panel (a): Rotation curve
# =========================================================================
ax1 = fig.add_subplot(gs[0, 0])
ax1.plot(r_model, v_newt, "--", color="0.6", lw=1.2,
         label=r"Newtonian (standard $G$)")
ax1.plot(r_model, v_cdm, ":", color="C3", lw=1.5, alpha=0.8,
         label=r"$\Lambda$CDM (NFW halo fit)")
ax1.plot(r_model, v_gfd, "--", color="C2", lw=1.5, alpha=0.8,
         label="GFD (photometric)")
ax1.plot(r_decode, v_dec, "-", color="C2", lw=2.0,
         label="GFD velocity decode (no mass input)")
ax1.errorbar(r_obs, v_obs, yerr=e_obs, fmt="o", ms=3, color="k",
             ecolor="0.4", elinewidth=0.7, capsize=1.5, capthick=0.7,
             zorder=5, label="CamB observations")
ax1.set_xlabel(r"$r$ [kpc]")
ax1.set_ylabel(r"$v$ [km s$^{-1}$]")
ax1.set_xlim(0, r_model[-1])
ax1.set_ylim(0, max(v_obs) * 1.15)
ax1.legend(loc="lower right", framealpha=0.9, fontsize=5.8)
ax1.text(0.0, 1.05, "(a) CamB rotation curve",
         transform=ax1.transAxes, fontweight="bold", fontsize=9)
ax1.grid(True, alpha=0.2)

# =========================================================================
# Panel (b): Enclosed mass (log scale)
# =========================================================================
ax2 = fig.add_subplot(gs[0, 1])
ax2.semilogy(r_model, M_cdm / MSUN, ":", color="C3", lw=1.2, alpha=0.7,
             label=r"$\Lambda$CDM (baryons + NFW)")
ax2.semilogy(r_model, M_phot / MSUN, "--", color="C2", lw=1.2, alpha=0.8,
             label="GFD (photometric)")
ax2.semilogy(r_decode, M_dec_Msun, "-", color="C2", lw=2.0,
             label=r"$M_{\rm dec}$ (velocity decoded = effective mass)")

# Shade the gap between photometric and decoded
ax2.fill_between(r_decode, M_dec_Msun, M_phot_on_decode,
                 alpha=0.15, color="C0",
                 label=r"$\Delta M_{\rm enc}$ (interior contribution)")
ax2.set_xlabel(r"$r$ [kpc]")
ax2.set_ylabel(r"$M_{\rm enc}$ [$M_\odot$]")
ax2.set_xlim(0, r_model[-1])
ax2.set_ylim(1e4, 1e10)
ax2.legend(loc="lower right", framealpha=0.9, fontsize=5.8)
ax2.text(0.0, 1.05, "(b) CamB velocity-decoded effective mass",
         transform=ax2.transAxes, fontweight="bold", fontsize=9)
ax2.grid(True, alpha=0.2, which="both")

# =========================================================================
# Panel (c): Log mass ratio — observed range only
# Only plotted where velocity observations exist (0.16–1.79 kpc).
# =========================================================================
ax3 = fig.add_subplot(gs[1, 0])

# Observation-based log ratio
mask_valid = (M_dec_Msun > 0) & (M_phot_on_decode > 0)
r_valid = r_decode[mask_valid]
log_ratio_gap = np.log10(M_phot_on_decode[mask_valid] / M_dec_Msun[mask_valid])

# Create histogram-style bars
n_bars = 40
r_bar = np.linspace(r_valid[2], r_valid[-2], n_bars)
gap_bar = np.interp(r_bar, r_valid, log_ratio_gap)
bar_width = (r_bar[-1] - r_bar[0]) / (n_bars * 1.15)

# Color gradient: deeper blue = larger gap
max_gap = np.max(gap_bar)
colors = [plt.cm.Blues(0.3 + 0.6 * g / max_gap) for g in gap_bar]

ax3.bar(r_bar, gap_bar, width=bar_width, color=colors,
        alpha=0.9, edgecolor='none', zorder=3)

ax3.axhline(0, color="k", lw=0.8, ls="--", alpha=0.5,
            label="$M_{\\rm phot} = M_{\\rm dec}$")
ax3.set_xlabel(r"$r$ [kpc]")
ax3.set_ylabel(r"$\log_{10}(M_{\rm phot}\,/\,M_{\rm dec})$  [decades]")
ax3.set_xlim(0, r_model[-1])

# Right-hand axis: multiplicative factor
ax3r = ax3.twinx()
ax3r.set_ylim(ax3.get_ylim())
ax3r.set_yticks([0, 0.5, 1.0, 1.5, 2.0])
ax3r.set_yticklabels(["1×", "3×", "10×", "30×", "100×"], fontsize=7)
# No label on twin axis: 1x-100x scale is implicit; omit to avoid collision with panel (d)
ax3r.set_ylabel("")

# Annotate key points
r_inner = 0.25
gap_inner = np.interp(r_inner, r_valid, log_ratio_gap)
ax3.annotate(
    f"$r = {r_inner}$ kpc\n${10**gap_inner:.0f}\\times$ gap",
    xy=(r_inner, gap_inner),
    xytext=(0.32, 0.88), textcoords="axes fraction",
    fontsize=7, color="#2166ac",
    ha="center",
    arrowprops=dict(arrowstyle="->", color="#2166ac", lw=0.8),
    bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#2166ac", alpha=0.8),
)

r_outer_ann = 1.5
gap_outer = np.interp(r_outer_ann, r_valid, log_ratio_gap)
ax3.annotate(
    f"$r = {r_outer_ann}$ kpc\n${10**gap_outer:.1f}\\times$ gap",
    xy=(r_outer_ann, gap_outer),
    xytext=(0.82, 0.45), textcoords="axes fraction",
    fontsize=7, color="#2166ac",
    ha="center",
    arrowprops=dict(arrowstyle="->", color="#2166ac", lw=0.8),
    bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#2166ac", alpha=0.8),
)

ax3.legend(loc="upper right", framealpha=0.9, fontsize=5.8)
ax3.text(0.0, 1.05,
         r"(c) Mass gap $M_{\rm phot}\,/\,M_{\rm dec}$ (observed range)",
         transform=ax3.transAxes, fontweight="bold", fontsize=9)
ax3.grid(True, alpha=0.2)

# =========================================================================
# Panel (d): Decoded mass + power output (observed range only)
# M_dec(r) + Delta_M(r) reconstructs M_phot(r) over 0.16–1.79 kpc.
# =========================================================================
ax4 = fig.add_subplot(gs[1, 1])

# Boosted decoded mass: observation range
M_boosted_Msun = M_dec_Msun + Delta_M

# Total power output at outermost observed radius
Delta_total = Delta_M[-1]
r_outer_val = r_decode[-1]

# Reference curves (full model range for context)
ax4.semilogy(r_model, M_cdm / MSUN, ":", color="C3", lw=1.2, alpha=0.7,
             label=r"$\Lambda$CDM (baryons + NFW)")
ax4.semilogy(r_model, M_phot / MSUN, "--", color="C2", lw=1.5, alpha=0.8,
             label="GFD (photometric)")
ax4.semilogy(r_decode, M_dec_Msun, "-", color="C2", lw=2.0, alpha=0.5,
             label=r"$M_{\rm dec}$ (velocity decoded = effective mass)")

# The boosted curve: observation range only
ax4.semilogy(r_decode, M_boosted_Msun, "-", color="C0", lw=2.5,
             label=r"$M_{\rm dec} + \Delta M_{\rm enc}(r)$")

# Shade the power output region
ax4.fill_between(r_decode, M_dec_Msun, M_boosted_Msun,
                 alpha=0.18, color="C0",
                 label=r"$\Delta M_{\rm enc}(r)$ (power output)")

ax4.set_xlabel(r"$r$ [kpc]")
ax4.set_ylabel(r"$M_{\rm enc}$ [$M_\odot$]")
ax4.set_xlim(0, r_model[-1])
ax4.set_ylim(1e4, 1e10)
ax4.legend(loc="lower right", framealpha=0.9, fontsize=5.5)

# Display equation and total (observed range only, no extrapolation)
exp = int(np.floor(np.log10(Delta_total)))
mantissa = Delta_total / 10**exp
ax4.text(0.04, 0.93,
         f"$\\Delta M_{{\\rm enc}}(r) = M_{{\\rm phot}}(r) - M_{{\\rm dec}}(r)$",
         transform=ax4.transAxes, fontsize=8, color="#2166ac", va="top")
ax4.text(0.04, 0.84,
         f"Over observed $r = {r_decode[0]:.2f}$–${r_outer_val:.2f}$ kpc:",
         transform=ax4.transAxes, fontsize=7, color="#1a5276", va="top")
ax4.text(0.04, 0.77,
         f"$\\Delta M_{{\\rm enc}} = {mantissa:.2f} \\times 10^{exp}\\;M_\\odot$",
         transform=ax4.transAxes, fontsize=9, fontweight="bold",
         color="#2166ac", va="top",
         bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#2166ac", alpha=0.85))

ax4.text(0.0, 1.05,
         r"(d) Decoded mass + power output $\Delta M_{\rm enc}(r)$",
         transform=ax4.transAxes, fontweight="bold", fontsize=9)
ax4.grid(True, alpha=0.2, which="both")

# =========================================================================
# Save fig2_camb in same folder as this .py file (for letter.tex)
# =========================================================================
import os
this_dir = os.path.dirname(os.path.abspath(__file__))
plt.savefig(os.path.join(this_dir, "fig2_camb.png"), dpi=300, bbox_inches="tight")
plt.savefig(os.path.join(this_dir, "fig2_camb.pdf"), bbox_inches="tight")
plt.close()
print("Saved: fig2_camb.png")
print("Saved: fig2_camb.pdf")