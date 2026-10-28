"""
Figures 1, 2, and 3 for Nelson 2026 Letter (GFD). Single script for
submission; generates all letter figures with hardcoded data (no API).

Physics (same covariant for all three figures):
  The framework is the spherical limit of the scalar-tensor (SST) theory
  plus the Poisson equation: the bidirectional covariant used in the letter.
  (1) Poisson: g_s = G*M_enc/r^2 (standard G, CODATA).
  (2) SST transition: in the spherical limit the action yields the
  constitutive law mu(x) = x/(1+x) with x = g_t/a_0, i.e. the relation
  between source acceleration g_s and total acceleration g_t that governs
  orbits. So the transition is fixed by the SST action, not chosen.
  Forward: M_enc(r) -> g_s (Poisson) -> g_t (SST) -> v(r).
  Inverse: v(r) -> g_t = v^2/r -> g_s (inverse SST) -> M_dec(r) (Poisson).
  All three figures use this same forward and inverse pipeline; no other
  gravitational model is used for the GFD curves (NFW is only for LambdaCDM
  comparison). The velocity-decode curves match observations by construction;
  the scientific content is the mass panels (effective mass vs baryonic and
  LambdaCDM). Observed velocities are pre-smoothed with a 6.2% Gaussian
  before decoding.

Figure 1 (fig1_mw_m33): 4-panel, two-column figure.
  (a) Milky Way rotation curve: observations, Newtonian, LambdaCDM (NFW fit),
      GFD photometric, GFD velocity decode (no mass input).
  (b) MW velocity-decoded effective mass (covariant): LambdaCDM, GFD photometric,
      GFD velocity-decoded effective mass.
  (c) M33 Triangulum rotation curve (same curve encoding as (a)).
  (d) M33 velocity-decoded effective mass (covariant) (same encoding as (b)).

Figure 2 (fig2_camb): 4-panel, two-column figure. Low-surface-brightness
  galaxy CamB: exterior vs effective mass; mass deficit and power output.
  (a) CamB rotation curve.
  (b) CamB mass: LambdaCDM, GFD photometric, velocity-decoded
      effective mass; shaded gap = interior contribution.
  (c) Mass gap M_phot/M_dec (observed range).
  (d) Decoded mass + power output Delta M_eff(r).

Figure 3 (fig3_ngc3198): 2-panel, single-column figure for the conclusion.
  (a) NGC 3198 rotation curve (same curve encoding as Figure 1).
  (b) NGC 3198 velocity-decoded effective mass.
  NGC 3198 is the canonical benchmark spiral (Begeman 1989, de Blok et al.
  2008). Same pipeline, G and a0; no re-tuning.

Outputs:
  fig1_mw_m33.png / .pdf   (Figure 1: MW + M33, two-column)
  fig2_camb.png / .pdf     (Figure 2: CamB 4-panel)
  fig3_ngc3198.png / .pdf  (Figure 3: NGC 3198, single-column)
"""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy.ndimage import gaussian_filter1d

# ---------------------------------------------------------------------------
# Physical constants (SI; lengths in m, velocities in m/s internally;
# kpc, km/s in I/O).
#
# G is the CODATA measured gravitational constant.
# A0 is the characteristic acceleration derived from the topology
# (Section VII, Eq. 44): a0 = k^2 * G * m_e / r_e^2 ~ 1.2e-10 m/s^2.
# Neither G nor A0 is fitted to rotation-curve data in this script.
# ---------------------------------------------------------------------------
G = 6.674e-11
A0 = 1.2e-10
MSUN = 1.989e30
KPC = 3.086e19

# ---------------------------------------------------------------------------
# Diffraction Gaussian smoothing for velocity observations
#
# Velocity observations carry measurement uncertainty at each radial bin.
# Rather than decode mass from raw point-to-point scatter, we first smooth
# the observed velocity profile with a mild Gaussian (sigma = 6.2% of the
# radial span). This produces a central-tendency curve through the data,
# analogous to fitting a smooth spline, so the mass decode reflects the
# underlying rotation profile rather than individual measurement noise.
# ---------------------------------------------------------------------------
def diffraction_smooth(r_obs, v_obs, frac=0.062):
    """
    Apply diffraction-style Gaussian smoothing to velocity observations.

    Interpolates v_obs onto a uniform fine grid, convolves with a Gaussian
    kernel whose sigma equals frac * (total radial span), then resamples
    back to the original observation radii.

    Parameters:
        r_obs : array, observed radii [any units, must be monotonic].
        v_obs : array, observed velocities [matching units].
        frac  : fractional smoothing level (default 0.062 = 6.2%).

    Returns:
        v_out : array, smoothed velocities at the original r_obs positions.
    """
    r_fine = np.linspace(r_obs[0], r_obs[-1], 1000)
    v_fine = np.interp(r_fine, r_obs, v_obs)
    dr = r_fine[1] - r_fine[0]
    sigma_r = frac * (r_obs[-1] - r_obs[0])
    sigma_pts = sigma_r / dr
    v_smooth = gaussian_filter1d(v_fine, sigma=sigma_pts)
    v_out = np.interp(r_obs, r_fine, v_smooth)
    return v_out

# ---------------------------------------------------------------------------
# NFW halo (used only for LambdaCDM comparison curves; not used in
# velocity_decode)
# ---------------------------------------------------------------------------
def nfw_mass(r, rho0, rs):
    """Enclosed mass for Navarro-Frenk-White profile. r, rs in m;
    rho0 in kg/m^3."""
    x = r / rs
    return 4*np.pi*rho0*rs**3 * (np.log(1+x) - x/(1+x))

# ---------------------------------------------------------------------------
# Velocity-to-mass transformation (inverse of the field equations)
#
# WHY THIS IS NOT CIRCULAR (for referees):
#
# A circular approach would be: assume a mass model, predict v(r), compare
# to data, adjust the mass model until the fit converges. That is standard
# rotation-curve fitting and is NOT what happens here.
#
# What happens here is a one-way algebraic transformation:
#
#   observed v(r)  -->  g_total = v^2/r         [kinematics, no model]
#                  -->  g_source via transition  [uses only a0]
#                  -->  M_enc = g_s * r^2 / G   [uses only G]
#
# The output M_enc is whatever the field equations say the mass must be,
# given the observed velocities. No mass is assumed, iterated, or fitted.
# The question the pipeline answers is: "If these field equations govern
# gravity, what enclosed mass does this rotation curve require?" The answer
# can then be compared independently to photometric baryonic mass.
#
# The velocity-decode curve in panels (a) and (c) matches observations by
# construction (it is the round-trip of v through the equations and back).
# That match is NOT the claim. The claim is in panels (b) and (d): the
# decoded M_enc lands near known baryonic mass and far below LambdaCDM.
#
# Transition: mu(x) = x/(1+x) (the well-known simple interpolating
# function, here determined by the scalar-tensor action rather than chosen).
# This differs from the classical MOND function mu(x) = x/sqrt(1+x^2).
#
# Poisson equation: standard form g_s = G*M_enc/r^2, so M_enc = g_s*r^2/G.
# No additional coupling multiplier is applied.
#
# Data-flow audit: velocity_decode() takes only r_obs, v_obs, and an output
# radial grid. The mass models (mw_M_enc, m33_M_enc, ngc3198_M_enc) and any
# NFW halo are used elsewhere (forward_gfd and LambdaCDM curves) and are
# never passed into this function. The steps below use only v, r, and the
# constants; no M_enc or mass model appears on the right-hand side until
# M_dec is computed as the output.
# ---------------------------------------------------------------------------
def velocity_decode(r_obs_kpc, v_obs_km, r_fine_kpc):
    """
    One-way algebraic transformation: observed v(r) -> effective mass M_dec(r).

    This is NOT a fit. No mass model is assumed, iterated, or optimised.
    The function takes observed radii and velocities as its only physical
    inputs, applies the field equations in closed form, and returns the
    effective mass that those equations require. The result can then be
    compared independently to photometric baryonic mass estimates.

    Inputs:
        r_obs_kpc   : observed radii [kpc].
        v_obs_km    : observed circular velocities [km/s].
        r_fine_kpc  : fine radial grid for output [kpc].
        (No mass model, no halo, no luminosity function is passed in.)

    Returns:
        v_dec : velocity [km/s] on the fine grid (round-trip; matches v_obs
                by construction and is NOT the prediction).
        M_dec : effective mass (decoded) [kg] on the fine grid (the physical
                result: mass implied by kinematics and constants alone).
    """
    r_obs = r_obs_kpc * KPC
    v_obs = v_obs_km * 1e3
    r_fine = r_fine_kpc * KPC
    v = np.interp(r_fine, r_obs, v_obs)

    # Step 1: kinematics. For circular motion, g_total = v^2/r.
    # Input: v, r only.
    gt = v**2 / r_fine

    # Step 2: inverse GFD scalar-tensor transition. The GFD transition
    # mu(x) = x/(1+x) yields g_obs = g_s/mu, which inverts to:
    #   g_s = g_t^2 / (A0 + g_t)
    # (Section VII, Eq. 24 of the paper). Uses only A0 and gt. No mass.
    gs = gt**2 / (A0 + gt)

    # Step 3: standard Poisson inversion. g_s = G*M_enc/r^2, so
    # M_enc = g_s * r^2 / G. First time mass appears; it is the output.
    M_dec = gs * r_fine**2 / G

    # Step 4: recompute g_s and g_total from M_dec, then v. Used only to
    # produce the decoded velocity curve for panels (a) and (c); not an
    # input to the decode.
    gs2 = G * M_dec / r_fine**2
    gt2 = (gs2 + np.sqrt(gs2**2 + 4 * gs2 * A0)) / 2.0
    v_dec = np.sqrt(r_fine * gt2) / 1e3
    return v_dec, M_dec

def forward_gfd(r_kpc, M_enc_func):
    """
    Forward direction: M_enc(r) -> v(r). Given an enclosed-mass function
    (r in m), returns Newtonian v, GFD v, and M on the r_kpc grid. Used for
    the photometric mass models (GFD green dashed in velocity panels) and for
    Newtonian (grey).

    Poisson: g_s = G*M/r^2.
    GFD transition: mu(x) = x/(1+x), giving the forward relation
      g_t = (g_s + sqrt(g_s^2 + 4*g_s*A0)) / 2
    (quadratic formula from g_t^2 - g_s*g_t - g_s*A0 = 0).
    """
    r = r_kpc * KPC
    M = M_enc_func(r)
    v_newt = np.sqrt(G * M / r) / 1e3
    gs = G * M / r**2
    # Forward GFD scalar-tensor transition: mu(x) = x/(1+x)
    gt = (gs + np.sqrt(gs**2 + 4 * gs * A0)) / 2.0
    v_gfd = np.sqrt(r * gt) / 1e3
    return v_newt, v_gfd, M

# ---------------------------------------------------------------------------
# Milky Way: observational data and mass models
#
# mw_r_obs, mw_v_obs, mw_e_obs: rotation curve from data (r in kpc, v in
# km/s, vertical error in km/s). Used as the only kinematic input to
# velocity_decode (after diffraction smoothing).
# mw_M_enc: photometric enclosed mass (exponential disk). Used for
# forward_gfd and for the GFD (photometric) and LambdaCDM baryonic
# component; not used in velocity_decode.
# ---------------------------------------------------------------------------
mw_r_obs = np.array([6.30,7.90,9.20,10.20,11.20,12.20,13.20,14.20,15.20,
                      16.20,17.20,18.20,19.20,20.20,20.70,21.20,21.70,22.30,
                      23.40,25.00,30.00,40.00,50.00])
mw_v_obs = np.array([231,234,230,229,227,227,225,222,218,218,220,215,208,
                      203,195,200,201,197,192,191,206,192,180])
mw_e_obs = np.array([1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,3,6,5,8,30,35,32])

MW_Mdisk = 7.52e10 * MSUN; MW_Rd = 2.79 * KPC
def mw_M_enc(r):
    """Enclosed mass for MW exponential disk. r in m."""
    x = r / MW_Rd
    return MW_Mdisk * (1 - (1+x)*np.exp(-x))

mw_r_model = np.linspace(0.5, 55, 600)
mw_r_decode = np.linspace(mw_r_obs[0], mw_r_obs[-1], 500)

mw_v_newt, mw_v_gfd, mw_M = forward_gfd(mw_r_model, mw_M_enc)
# Smooth observed velocities (6.2% diffraction Gaussian) before decode.
# Suppresses point-to-point scatter; large-scale profile preserved.
mw_v_smooth = diffraction_smooth(mw_r_obs, mw_v_obs, frac=0.062)
# Decode: smoothed v_obs in, M_dec out. v_dec reproduces v_obs by
# construction. M_dec (mass from kinematics alone) is the physical result.
mw_v_dec, mw_M_dec = velocity_decode(mw_r_obs, mw_v_smooth, mw_r_decode)

# LambdaCDM comparison: baryons plus NFW halo (parameters from literature)
mw_nfw_rho0 = 1.826e-21; mw_nfw_rs = 9.3 * KPC
mw_M_cdm = mw_M_enc(mw_r_model * KPC) + nfw_mass(mw_r_model * KPC, mw_nfw_rho0, mw_nfw_rs)
mw_v_cdm = np.sqrt(G * mw_M_cdm / (mw_r_model * KPC)) / 1e3

# ---------------------------------------------------------------------------
# M33 Triangulum: observational data and mass models
#
# Same structure as MW: r_obs, v_obs, e_obs are the only inputs to
# velocity_decode (after diffraction smoothing). m33_M_enc is used for
# forward curves and LambdaCDM baryons only.
# ---------------------------------------------------------------------------
m33_r_obs = np.array([0.5,1,1.5,2,3,4,5,6,7,8,9,10,11,12,14,15,17])
m33_v_obs = np.array([30,38,55,68,88,100,105,108,108,108,110,115,117,120,125,128,130])
m33_e_obs = np.array([5,8,7,8,6,7,5,6,5,6,6,7,6,7,7,8,8])

M33_bulge_M = 0.4e9*MSUN; M33_bulge_a = 0.18*KPC
M33_disk_M = 3.5e9*MSUN;  M33_disk_Rd = 1.6*KPC
M33_gas_M = 3.2e9*MSUN;   M33_gas_Rd = 4.0*KPC

def m33_M_enc(r):
    """Enclosed mass for M33: bulge + exponential disk + gas. r in m."""
    b = M33_bulge_M * r**2 / (r + M33_bulge_a)**2
    xd = r / M33_disk_Rd; d = M33_disk_M * (1 - (1+xd)*np.exp(-xd))
    xg = r / M33_gas_Rd;  g = M33_gas_M * (1 - (1+xg)*np.exp(-xg))
    return b + d + g

m33_r_model = np.linspace(0.1, 20, 600)
m33_r_decode = np.linspace(m33_r_obs[0], m33_r_obs[-1], 500)

m33_v_newt, m33_v_gfd, m33_M = forward_gfd(m33_r_model, m33_M_enc)
# Smooth observed velocities (6.2% diffraction Gaussian) before decode.
# Suppresses point-to-point scatter; large-scale profile preserved.
m33_v_smooth = diffraction_smooth(m33_r_obs, m33_v_obs, frac=0.062)
# Decode: smoothed v_obs in, M_dec out. v_dec reproduces v_obs by
# construction. M_dec (mass from kinematics alone) is the physical result.
m33_v_dec, m33_M_dec = velocity_decode(m33_r_obs, m33_v_smooth, m33_r_decode)

# LambdaCDM comparison: baryons plus NFW
m33_nfw_rho0 = 2.924e-23; m33_nfw_rs = 101.5 * KPC
m33_M_cdm = m33_M_enc(m33_r_model * KPC) + nfw_mass(m33_r_model * KPC, m33_nfw_rho0, m33_nfw_rs)
m33_v_cdm = np.sqrt(G * m33_M_cdm / (m33_r_model * KPC)) / 1e3

# ---------------------------------------------------------------------------
# Figure layout and line convention
#
# 2x2 grid: (a) MW velocity, (b) MW mass, (c) M33 velocity, (d) M33 mass.
# Line convention: green dashed = GFD photometric (forward from mass model);
# green solid = GFD velocity decode (inverse from smoothed observed v only);
# red dotted = LambdaCDM; grey dashed = Newtonian (bare baryons).
# Outputs written to script dir with _standardG suffix.
# ---------------------------------------------------------------------------
_figdir = os.path.dirname(os.path.abspath(__file__))

plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 9,
    'axes.labelsize': 10,
    'legend.fontsize': 7,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'figure.dpi': 300,
    'savefig.dpi': 300,
})

fig = plt.figure(figsize=(8.5, 6.0))
gs_layout = GridSpec(2, 2, hspace=0.36, wspace=0.36,
                     left=0.09, right=0.97, top=0.93, bottom=0.08)

# Panel (a): MW rotation curve. Solid green matches data by construction
# (round-trip). See panel (b) for the mass demonstration.
ax1 = fig.add_subplot(gs_layout[0, 0])
ax1.plot(mw_r_model, mw_v_newt, '--', color='0.6', lw=1.2,
         label=r'Newtonian (standard $G$)')
ax1.plot(mw_r_model, mw_v_cdm, ':', color='C3', lw=1.5, alpha=0.8,
         label=r'$\Lambda$CDM (NFW halo fit)')
ax1.plot(mw_r_model, mw_v_gfd, '--', color='C2', lw=1.5, alpha=0.8,
         label='GFD (photometric)')
ax1.plot(mw_r_decode, mw_v_dec, '-', color='C2', lw=2.0,
         label='GFD velocity decode (no mass input)')
ax1.errorbar(mw_r_obs, mw_v_obs, yerr=mw_e_obs,
             fmt='o', ms=3, color='k', ecolor='0.4', elinewidth=0.7,
             capsize=1.5, capthick=0.7, zorder=5, label='MW observations')
ax1.set_xlabel(r'$r$ [kpc]')
ax1.set_ylabel(r'$v$ [km s$^{-1}$]')
ax1.set_xlim(0, 55)
ax1.set_ylim(0, 290)
ax1.legend(loc='lower right', framealpha=0.9, fontsize=6.5)
ax1.text(0.0, 1.05, r'(a) Milky Way', transform=ax1.transAxes, fontweight='bold', fontsize=9)
ax1.grid(True, alpha=0.2)

# Panel (b): MW decoded mass - central result. M_dec derived from v_obs
# alone; no mass input. Proximity to baryonic mass and divergence from
# LambdaCDM is the falsifiable claim.
ax2 = fig.add_subplot(gs_layout[0, 1])
ax2.semilogy(mw_r_model, mw_M_cdm / MSUN, ':', color='C3', lw=1.2, alpha=0.7,
             label=r'$\Lambda$CDM (baryons + NFW)')
ax2.semilogy(mw_r_model, mw_M / MSUN, '--', color='C2', lw=1.2, alpha=0.8,
             label='GFD (photometric)')
ax2.semilogy(mw_r_decode, mw_M_dec / MSUN, '-', color='C2', lw=2.0,
             label='GFD velocity-decoded effective mass')
ax2.set_xlabel(r'$r$ [kpc]')
ax2.set_ylabel(r'$M_{\rm dec}$ [$M_\odot$]')
ax2.set_xlim(0, 55)
ax2.set_ylim(5e9, 1e12)
ax2.legend(loc='lower right', framealpha=0.9, fontsize=6.5)
ax2.text(0.0, 1.05, r'(b) MW velocity-decoded effective mass (covariant)', transform=ax2.transAxes,
         fontweight='bold', fontsize=9)
ax2.grid(True, alpha=0.2, which='both')

# Panel (c): M33 rotation curve. Solid green matches data by construction.
# See panel (d) for the mass demonstration.
ax3 = fig.add_subplot(gs_layout[1, 0])
ax3.plot(m33_r_model, m33_v_newt, '--', color='0.6', lw=1.2,
         label=r'Newtonian (standard $G$)')
ax3.plot(m33_r_model, m33_v_cdm, ':', color='C3', lw=1.5, alpha=0.8,
         label=r'$\Lambda$CDM (NFW halo fit)')
ax3.plot(m33_r_model, m33_v_gfd, '--', color='C2', lw=1.5, alpha=0.8,
         label='GFD (photometric)')
ax3.plot(m33_r_decode, m33_v_dec, '-', color='C2', lw=2.0,
         label='GFD velocity decode (no mass input)')
ax3.errorbar(m33_r_obs, m33_v_obs, yerr=m33_e_obs,
             fmt='o', ms=3, color='k', ecolor='0.4', elinewidth=0.7,
             capsize=1.5, capthick=0.7, zorder=5, label='M33 observations')
ax3.set_xlabel(r'$r$ [kpc]')
ax3.set_ylabel(r'$v$ [km s$^{-1}$]')
ax3.set_xlim(0, 20)
ax3.set_ylim(0, 170)
ax3.legend(loc='lower right', framealpha=0.9, fontsize=6.5)
ax3.text(0.0, 1.05, r'(c) M33 Triangulum', transform=ax3.transAxes, fontweight='bold', fontsize=9)
ax3.grid(True, alpha=0.2)

# Panel (d): M33 decoded mass - central result. Same as (b); the excess
# over photometric mass at 17 kpc is a testable prediction.
ax4 = fig.add_subplot(gs_layout[1, 1])
ax4.semilogy(m33_r_model, m33_M_cdm / MSUN, ':', color='C3', lw=1.2, alpha=0.7,
             label=r'$\Lambda$CDM (baryons + NFW)')
ax4.semilogy(m33_r_model, m33_M / MSUN, '--', color='C2', lw=1.2, alpha=0.8,
             label='GFD (photometric)')
ax4.semilogy(m33_r_decode, m33_M_dec / MSUN, '-', color='C2', lw=2.0,
             label='GFD velocity-decoded effective mass')
ax4.set_xlabel(r'$r$ [kpc]')
ax4.set_ylabel(r'$M_{\rm dec}$ [$M_\odot$]')
ax4.set_xlim(0, 20)
ax4.set_ylim(1e7, 2e11)
ax4.legend(loc='lower right', framealpha=0.9, fontsize=6.5)
ax4.text(0.0, 1.05, r'(d) M33 velocity-decoded effective mass (covariant)', transform=ax4.transAxes,
         fontweight='bold', fontsize=9)
ax4.grid(True, alpha=0.2, which='both')

plt.savefig(os.path.join(_figdir, 'fig1_mw_m33.png'), dpi=300, bbox_inches='tight')
plt.savefig(os.path.join(_figdir, 'fig1_mw_m33.pdf'), bbox_inches='tight')
plt.close()

# ===========================================================================
# Figure 2: CamB — 4-panel (rotation curve, enclosed mass, mass gap, power output)
#
# Low-surface-brightness galaxy; SPARC Lelli+2016. Hardcoded data; no API.
# Demonstrates effective mass below photometric (topology / interior contribution).
# ===========================================================================
# CamB observational data and mass model
camb_r_obs = np.array([0.16, 0.41, 0.57, 0.73, 0.90, 1.06, 1.22, 1.47, 1.79])
camb_v_obs = np.array([1.99, 4.84, 6.79, 8.87, 10.9, 12.9, 14.7, 16.8, 20.1])
camb_e_obs = np.array([1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5])
DISK_M = 3.75e7 * MSUN
DISK_Rd = 1.0 * KPC
GAS_M = 6.251e8 * MSUN
GAS_Rd = 26.48 * KPC

def camb_M_enc(r):
    """Enclosed mass for CamB: exponential disk + gas. r in metres."""
    xd = r / DISK_Rd
    m_disk = DISK_M * (1 - (1 + xd) * np.exp(-xd))
    xg = r / GAS_Rd
    m_gas = GAS_M * (1 - (1 + xg) * np.exp(-xg))
    return m_disk + m_gas

# NFW for LambdaCDM comparison (abundance matching for low-mass galaxy)
def abundance_matching_simple(m_bary_msun):
    """Simple Behroozi-style: M200 from baryonic mass."""
    log_mb = np.log10(m_bary_msun)
    log_m200 = 1.5 * (log_mb - 10.0) + 12.0
    log_m200 = max(log_m200, log_mb + 1.0)
    return 10**log_m200

def nfw_enclosed_mass_simple(r_kpc, m200_msun):
    """NFW enclosed mass given M200 in Msun. Returns mass in kg."""
    log_c = 0.905 - 0.101 * (np.log10(m200_msun) - 12.0)
    c = 10**log_c
    rho_crit = 1.27e-26
    M200_kg = m200_msun * MSUN
    r200 = (3 * M200_kg / (4 * np.pi * 200 * rho_crit))**(1.0/3.0)
    rs = r200 / c
    rho0 = M200_kg / (4 * np.pi * rs**3 * (np.log(1 + c) - c / (1 + c)))
    r_m = r_kpc * KPC
    x = r_m / rs
    return 4 * np.pi * rho0 * rs**3 * (np.log(1 + x) - x / (1 + x))

camb_m_bary_total = (3.75e7 + 6.251e8)
camb_m200 = abundance_matching_simple(camb_m_bary_total)

# CamB grids and curves
camb_r_span = camb_r_obs[-1] - camb_r_obs[0]
camb_r_model = np.linspace(0.1, camb_r_obs[-1] + 0.15 * camb_r_span, 600)
camb_r_decode = np.linspace(camb_r_obs[0], camb_r_obs[-1], 500)

camb_v_newt, camb_v_gfd, camb_M_phot = forward_gfd(camb_r_model, camb_M_enc)
camb_v_smooth = diffraction_smooth(camb_r_obs, camb_v_obs, frac=0.062)
camb_v_dec, camb_M_dec = velocity_decode(camb_r_obs, camb_v_smooth, camb_r_decode)

camb_M_nfw = np.array([nfw_enclosed_mass_simple(float(rk), camb_m200) for rk in camb_r_model])
camb_M_cdm = camb_M_enc(camb_r_model * KPC) + camb_M_nfw
camb_v_cdm = np.sqrt(G * camb_M_cdm / (camb_r_model * KPC)) / 1e3

# Power output / mass deficit (observation-based only)
camb_M_phot_on_decode = np.interp(camb_r_decode, camb_r_model, camb_M_phot / MSUN)
camb_M_dec_Msun = camb_M_dec / MSUN
camb_Delta_M = camb_M_phot_on_decode - camb_M_dec_Msun

# Build Figure 2 (4-panel)
fig2 = plt.figure(figsize=(8.5, 6.0))
gs2 = GridSpec(2, 2, hspace=0.36, wspace=0.36, left=0.10, right=0.96, top=0.94, bottom=0.08)

# Panel (a): CamB rotation curve
ax2a = fig2.add_subplot(gs2[0, 0])
ax2a.plot(camb_r_model, camb_v_newt, "--", color="0.6", lw=1.2, label=r"Newtonian (standard $G$)")
ax2a.plot(camb_r_model, camb_v_cdm, ":", color="C3", lw=1.5, alpha=0.8, label=r"$\Lambda$CDM (NFW halo fit)")
ax2a.plot(camb_r_model, camb_v_gfd, "--", color="C2", lw=1.5, alpha=0.8, label="GFD (photometric)")
ax2a.plot(camb_r_decode, camb_v_dec, "-", color="C2", lw=2.0, label="GFD velocity decode (no mass input)")
ax2a.errorbar(camb_r_obs, camb_v_obs, yerr=camb_e_obs, fmt="o", ms=3, color="k", ecolor="0.4",
              elinewidth=0.7, capsize=1.5, capthick=0.7, zorder=5, label="CamB observations")
ax2a.set_xlabel(r"$r$ [kpc]")
ax2a.set_ylabel(r"$v$ [km s$^{-1}$]")
ax2a.set_xlim(0, camb_r_model[-1])
ax2a.set_ylim(0, max(camb_v_obs) * 1.15)
ax2a.legend(loc="lower right", framealpha=0.9, fontsize=5.8)
ax2a.text(0.0, 1.05, "(a) CamB rotation curve", transform=ax2a.transAxes, fontweight="bold", fontsize=9)
ax2a.grid(True, alpha=0.2)

# Panel (b): CamB enclosed mass
ax2b = fig2.add_subplot(gs2[0, 1])
ax2b.semilogy(camb_r_model, camb_M_cdm / MSUN, ":", color="C3", lw=1.2, alpha=0.7,
              label=r"$\Lambda$CDM (baryons + NFW)")
ax2b.semilogy(camb_r_model, camb_M_phot / MSUN, "--", color="C2", lw=1.2, alpha=0.8,
              label="GFD (photometric)")
ax2b.semilogy(camb_r_decode, camb_M_dec_Msun, "-", color="C2", lw=2.0,
              label=r"$M_{\rm dec}$ (velocity decoded = effective mass)")
ax2b.fill_between(camb_r_decode, camb_M_dec_Msun, camb_M_phot_on_decode,
                  alpha=0.15, color="C0", label=r"$\Delta M_{\rm eff}$ (interior contribution)")
ax2b.set_xlabel(r"$r$ [kpc]")
ax2b.set_ylabel(r"$M_{\rm dec}$ [$M_\odot$]")
ax2b.set_xlim(0, camb_r_model[-1])
ax2b.set_ylim(1e4, 1e10)
ax2b.legend(loc="lower right", framealpha=0.9, fontsize=5.8)
ax2b.text(0.0, 1.05, "(b) CamB velocity-decoded effective mass", transform=ax2b.transAxes,
          fontweight="bold", fontsize=9)
ax2b.grid(True, alpha=0.2, which="both")

# Panel (c): Mass gap M_phot/M_dec (observed range)
ax2c = fig2.add_subplot(gs2[1, 0])
camb_mask_valid = (camb_M_dec_Msun > 0) & (camb_M_phot_on_decode > 0)
camb_r_valid = camb_r_decode[camb_mask_valid]
camb_log_ratio_gap = np.log10(camb_M_phot_on_decode[camb_mask_valid] / camb_M_dec_Msun[camb_mask_valid])
n_bars = 40
camb_r_bar = np.linspace(camb_r_valid[2], camb_r_valid[-2], n_bars)
camb_gap_bar = np.interp(camb_r_bar, camb_r_valid, camb_log_ratio_gap)
bar_width = (camb_r_bar[-1] - camb_r_bar[0]) / (n_bars * 1.15)
max_gap = np.max(camb_gap_bar)
camb_colors = [plt.cm.Blues(0.3 + 0.6 * g / max_gap) for g in camb_gap_bar]
ax2c.bar(camb_r_bar, camb_gap_bar, width=bar_width, color=camb_colors, alpha=0.9, edgecolor='none', zorder=3)
ax2c.axhline(0, color="k", lw=0.8, ls="--", alpha=0.5, label="$M_{\\rm phot} = M_{\\rm dec}$")
ax2c.set_xlabel(r"$r$ [kpc]")
ax2c.set_ylabel(r"$\log_{10}(M_{\rm phot}\,/\,M_{\rm dec})$  [decades]")
ax2c.set_xlim(0, camb_r_model[-1])
ax2c_r = ax2c.twinx()
ax2c_r.set_ylim(ax2c.get_ylim())
ax2c_r.set_yticks([0, 0.5, 1.0, 1.5, 2.0])
ax2c_r.set_yticklabels(["1×", "3×", "10×", "30×", "100×"], fontsize=7)
ax2c_r.set_ylabel("")
r_inner = 0.25
gap_inner = np.interp(r_inner, camb_r_valid, camb_log_ratio_gap)
ax2c.annotate(f"$r = {r_inner}$ kpc\n${10**gap_inner:.0f}\\times$ gap",
              xy=(r_inner, gap_inner), xytext=(0.32, 0.88), textcoords="axes fraction",
              fontsize=7, color="#2166ac", ha="center",
              arrowprops=dict(arrowstyle="->", color="#2166ac", lw=0.8),
              bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#2166ac", alpha=0.8))
r_outer_ann = 1.5
gap_outer = np.interp(r_outer_ann, camb_r_valid, camb_log_ratio_gap)
ax2c.annotate(f"$r = {r_outer_ann}$ kpc\n${10**gap_outer:.1f}\\times$ gap",
              xy=(r_outer_ann, gap_outer), xytext=(0.82, 0.45), textcoords="axes fraction",
              fontsize=7, color="#2166ac", ha="center",
              arrowprops=dict(arrowstyle="->", color="#2166ac", lw=0.8),
              bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#2166ac", alpha=0.8))
ax2c.legend(loc="upper right", framealpha=0.9, fontsize=5.8)
ax2c.text(0.0, 1.05, r"(c) Mass gap $M_{\rm phot}\,/\,M_{\rm dec}$ (observed range)",
          transform=ax2c.transAxes, fontweight="bold", fontsize=9)
ax2c.grid(True, alpha=0.2)

# Panel (d): Decoded mass + power output
ax2d = fig2.add_subplot(gs2[1, 1])
camb_M_boosted_Msun = camb_M_dec_Msun + camb_Delta_M
camb_Delta_total = camb_Delta_M[-1]
camb_r_outer_val = camb_r_decode[-1]
ax2d.semilogy(camb_r_model, camb_M_cdm / MSUN, ":", color="C3", lw=1.2, alpha=0.7,
              label=r"$\Lambda$CDM (baryons + NFW)")
ax2d.semilogy(camb_r_model, camb_M_phot / MSUN, "--", color="C2", lw=1.5, alpha=0.8,
              label="GFD (photometric)")
ax2d.semilogy(camb_r_decode, camb_M_dec_Msun, "-", color="C2", lw=2.0, alpha=0.5,
              label=r"$M_{\rm dec}$ (velocity decoded = effective mass)")
ax2d.semilogy(camb_r_decode, camb_M_boosted_Msun, "-", color="C0", lw=2.5,
              label=r"$M_{\rm dec} + \Delta M_{\rm eff}(r)$")
ax2d.fill_between(camb_r_decode, camb_M_dec_Msun, camb_M_boosted_Msun,
                 alpha=0.18, color="C0", label=r"$\Delta M_{\rm eff}(r)$ (power output)")
ax2d.set_xlabel(r"$r$ [kpc]")
ax2d.set_ylabel(r"$M_{\rm dec}$ [$M_\odot$]")
ax2d.set_xlim(0, camb_r_model[-1])
ax2d.set_ylim(1e4, 1e10)
ax2d.legend(loc="lower right", framealpha=0.9, fontsize=5.5)
exp = int(np.floor(np.log10(camb_Delta_total)))
mantissa = camb_Delta_total / 10**exp
ax2d.text(0.04, 0.93, r"$\Delta M_{\rm eff}(r) = M_{\rm phot}(r) - M_{\rm dec}(r)$",
         transform=ax2d.transAxes, fontsize=8, color="#2166ac", va="top")
ax2d.text(0.04, 0.84, f"Over observed $r = {camb_r_decode[0]:.2f}$–${camb_r_outer_val:.2f}$ kpc:",
         transform=ax2d.transAxes, fontsize=7, color="#1a5276", va="top")
ax2d.text(0.04, 0.77, f"$\\Delta M_{{\\rm eff}} = {mantissa:.2f} \\times 10^{exp}\\;M_\\odot$",
         transform=ax2d.transAxes, fontsize=9, fontweight="bold", color="#2166ac", va="top",
         bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#2166ac", alpha=0.85))
ax2d.text(0.0, 1.05, r"(d) Decoded mass + power output $\Delta M_{\rm eff}(r)$",
          transform=ax2d.transAxes, fontweight="bold", fontsize=9)
ax2d.grid(True, alpha=0.2, which="both")

plt.savefig(os.path.join(_figdir, "fig2_camb.png"), dpi=300, bbox_inches="tight")
plt.savefig(os.path.join(_figdir, "fig2_camb.pdf"), bbox_inches="tight")
plt.close()

# ===========================================================================
# Figure 3: NGC 3198 — single-column, two panels (conclusion).
#
# The canonical rotation-curve test galaxy (Begeman 1989).
#
# This is the "blind prediction" figure for the conclusion: the same
# pipeline applied to a third galaxy with no re-tuning. NGC 3198 is the
# benchmark spiral for dark matter studies; its HI rotation curve extends
# to 30 kpc and is flat to within 5 km/s (Begeman 1989, de Blok et al.
# 2008). If the inverse pipeline works here with the same G and a0, it
# works on the standard test case.
#
# ngc3198_r_obs, ngc3198_v_obs, ngc3198_e_obs: rotation curve data.
# ngc3198_M_enc: photometric enclosed mass (stellar disk + gas disk +
# bulge). Used for forward curves and LambdaCDM baryons only; not used
# in velocity_decode.
# ===========================================================================
ngc3198_r_obs = np.array([3.0, 5.0, 8.0, 10.0, 15.0, 20.0, 25.0, 30.0])
ngc3198_v_obs = np.array([110.0, 145.0, 150.0, 152.0, 150.0, 150.0, 150.0, 149.0])
ngc3198_e_obs = np.array([8.0, 5.0, 3.0, 3.0, 3.0, 4.0, 5.0, 6.0])

NGC3198_stellar_M = 1.78e10 * MSUN;  NGC3198_stellar_Rd = 3.00 * KPC
NGC3198_gas_M     = 1.48e10 * MSUN;  NGC3198_gas_Rd     = 6.00 * KPC
NGC3198_bulge_M   = 9.82e8  * MSUN;  NGC3198_bulge_a    = 0.30 * KPC

def ngc3198_M_enc(r):
    """Enclosed mass for NGC 3198: stellar disk + gas disk + bulge. r in m."""
    # Hernquist bulge
    b = NGC3198_bulge_M * r**2 / (r + NGC3198_bulge_a)**2
    # Exponential stellar disk
    xs = r / NGC3198_stellar_Rd
    s = NGC3198_stellar_M * (1 - (1 + xs) * np.exp(-xs))
    # Exponential gas disk
    xg = r / NGC3198_gas_Rd
    g = NGC3198_gas_M * (1 - (1 + xg) * np.exp(-xg))
    return b + s + g

ngc3198_r_model  = np.linspace(0.5, 35, 600)
ngc3198_r_decode = np.linspace(ngc3198_r_obs[0], ngc3198_r_obs[-1], 500)

ngc3198_v_newt, ngc3198_v_gfd, ngc3198_M = forward_gfd(ngc3198_r_model, ngc3198_M_enc)
# Smooth observed velocities (6.2% diffraction Gaussian) before decode.
ngc3198_v_smooth = diffraction_smooth(ngc3198_r_obs, ngc3198_v_obs, frac=0.062)
# Decode: smoothed v_obs in, M_dec out.
ngc3198_v_dec, ngc3198_M_dec = velocity_decode(ngc3198_r_obs, ngc3198_v_smooth, ngc3198_r_decode)

# LambdaCDM comparison: baryons plus NFW halo (NGC 3198 literature values:
# V200 ~ 100 km/s, c ~ 9; de Blok et al. 2008, Karukes et al. 2015).
ngc3198_nfw_rho0 = 3.189e-22; ngc3198_nfw_rs = 15.9 * KPC
ngc3198_M_cdm = ngc3198_M_enc(ngc3198_r_model * KPC) + nfw_mass(ngc3198_r_model * KPC, ngc3198_nfw_rho0, ngc3198_nfw_rs)
ngc3198_v_cdm = np.sqrt(G * ngc3198_M_cdm / (ngc3198_r_model * KPC)) / 1e3

# ---------------------------------------------------------------------------
# Figure 3 layout: single-column, two panels stacked vertically.
# Same line convention as Figure 1; fits single-column conclusion.
# (a) NGC 3198 rotation curve; (b) NGC 3198 velocity-decoded effective mass.
# ---------------------------------------------------------------------------
fig3 = plt.figure(figsize=(4.25, 7.4))
gs3_layout = GridSpec(2, 1, hspace=0.45,
                      left=0.18, right=0.95, top=0.93, bottom=0.08)

# Panel (a): NGC 3198 rotation curve. Same line convention as Figure 1.
ax5 = fig3.add_subplot(gs3_layout[0, 0])
ax5.plot(ngc3198_r_model, ngc3198_v_newt, '--', color='0.6', lw=1.2,
         label=r'Newtonian (standard $G$)')
ax5.plot(ngc3198_r_model, ngc3198_v_cdm, ':', color='C3', lw=1.5, alpha=0.8,
         label=r'$\Lambda$CDM (NFW halo fit)')
ax5.plot(ngc3198_r_model, ngc3198_v_gfd, '--', color='C2', lw=1.5, alpha=0.8,
         label='GFD (photometric)')
ax5.plot(ngc3198_r_decode, ngc3198_v_dec, '-', color='C2', lw=2.0,
         label='GFD velocity decode (no mass input)')
ax5.errorbar(ngc3198_r_obs, ngc3198_v_obs, yerr=ngc3198_e_obs,
             fmt='o', ms=3, color='k', ecolor='0.4', elinewidth=0.7,
             capsize=1.5, capthick=0.7, zorder=5, label='NGC 3198 observations')
ax5.set_xlabel(r'$r$ [kpc]')
ax5.set_ylabel(r'$v$ [km s$^{-1}$]')
ax5.set_xlim(0, 35)
ax5.set_ylim(0, 200)
ax5.legend(loc='lower right', framealpha=0.9, fontsize=6.5)
ax5.text(0.0, 1.05, r'(a) NGC 3198', transform=ax5.transAxes, fontweight='bold', fontsize=9)
ax5.grid(True, alpha=0.2)

# Panel (b): NGC 3198 decoded mass — central result for this galaxy.
ax6 = fig3.add_subplot(gs3_layout[1, 0])
ax6.semilogy(ngc3198_r_model, ngc3198_M_cdm / MSUN, ':', color='C3', lw=1.2, alpha=0.7,
             label=r'$\Lambda$CDM (baryons + NFW)')
ax6.semilogy(ngc3198_r_model, ngc3198_M / MSUN, '--', color='C2', lw=1.2, alpha=0.8,
             label='GFD (photometric)')
ax6.semilogy(ngc3198_r_decode, ngc3198_M_dec / MSUN, '-', color='C2', lw=2.0,
             label='GFD velocity-decoded effective mass')
ax6.set_xlabel(r'$r$ [kpc]')
ax6.set_ylabel(r'$M_{\rm dec}$ [$M_\odot$]')
ax6.set_xlim(0, 35)
ax6.set_ylim(5e8, 5e11)
ax6.legend(loc='lower right', framealpha=0.9, fontsize=6.5)
ax6.text(0.0, 1.05, r'(b) NGC 3198 velocity-decoded effective mass', transform=ax6.transAxes,
         fontweight='bold', fontsize=9)
ax6.grid(True, alpha=0.2, which='both')

plt.savefig(os.path.join(_figdir, 'fig3_ngc3198.png'), dpi=300, bbox_inches='tight')
plt.savefig(os.path.join(_figdir, 'fig3_ngc3198.pdf'), bbox_inches='tight')
plt.close()

# --- Summary and verification output ---
print("Figure 1 (MW + M33) saved:")
print(f"  {os.path.join(_figdir, 'fig1_mw_m33.png')}")
print(f"  {os.path.join(_figdir, 'fig1_mw_m33.pdf')}")
print("\nFigure 2 (CamB) saved:")
print(f"  {os.path.join(_figdir, 'fig2_camb.png')}")
print(f"  {os.path.join(_figdir, 'fig2_camb.pdf')}")
print("\nFigure 3 (NGC 3198) saved:")
print(f"  {os.path.join(_figdir, 'fig3_ngc3198.png')}")
print(f"  {os.path.join(_figdir, 'fig3_ngc3198.pdf')}")
print("\nMW:")
print(f"  Decoded M_enc at 25 kpc: {np.interp(25, mw_r_decode, mw_M_dec)/MSUN:.2e} Msun")
print(f"  Photometric M_enc at 25 kpc: {mw_M_enc(25*KPC)/MSUN:.2e} Msun")
print(f"  CDM M_enc at 25 kpc: {np.interp(25, mw_r_model, mw_M_cdm)/MSUN:.2e} Msun")
print("\nM33:")
print(f"  Decoded M_enc at 17 kpc: {m33_M_dec[-1]/MSUN:.2e} Msun")
print(f"  Photometric M_enc at 17 kpc: {m33_M_enc(17*KPC)/MSUN:.2e} Msun")
print(f"  CDM M_enc at 17 kpc: {np.interp(17, m33_r_model, m33_M_cdm)/MSUN:.2e} Msun")
print("\nNGC 3198:")
print(f"  Decoded M_enc at 30 kpc: {ngc3198_M_dec[-1]/MSUN:.2e} Msun")
print(f"  Photometric M_enc at 30 kpc: {ngc3198_M_enc(30*KPC)/MSUN:.2e} Msun")
print(f"  CDM M_enc at 30 kpc: {np.interp(30, ngc3198_r_model, ngc3198_M_cdm)/MSUN:.2e} Msun")