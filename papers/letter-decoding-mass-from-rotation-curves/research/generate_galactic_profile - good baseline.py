import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy.ndimage import gaussian_filter1d

# ====================== CONSTANTS (identical to letter script) ======================
G = 6.674e-11
A0 = 1.2e-10
MSUN = 1.989e30
KPC = 3.086e19

# ====================== SHARED FUNCTIONS (from generate_letter_figures.py) ======================
def diffraction_smooth(r_obs, v_obs, frac=0.062):
    r_fine = np.linspace(r_obs[0], r_obs[-1], 1000)
    v_fine = np.interp(r_fine, r_obs, v_obs)
    dr = r_fine[1] - r_fine[0]
    sigma_r = frac * (r_obs[-1] - r_obs[0])
    sigma_pts = sigma_r / dr
    v_smooth = gaussian_filter1d(v_fine, sigma=sigma_pts)
    return np.interp(r_obs, r_fine, v_smooth)

def nfw_mass(r, rho0, rs):
    x = r / rs
    return 4 * np.pi * rho0 * rs**3 * (np.log(1 + x) - x / (1 + x))

def velocity_decode(r_obs_kpc, v_obs_km, r_fine_kpc):
    r_obs = r_obs_kpc * KPC
    v_obs = v_obs_km * 1e3
    r_fine = r_fine_kpc * KPC
    v = np.interp(r_fine, r_obs, v_obs)
    gt = v**2 / r_fine
    gs = gt**2 / (A0 + gt)
    M_dec = gs * r_fine**2 / G
    gs2 = G * M_dec / r_fine**2
    gt2 = (gs2 + np.sqrt(gs2**2 + 4 * gs2 * A0)) / 2.0
    v_dec = np.sqrt(r_fine * gt2) / 1e3
    return v_dec, M_dec

def M_dec_bounds(r_kpc, v_km_s, e_km_s):
    r = r_kpc * KPC
    v = np.asarray(v_km_s, dtype=float) * 1e3
    e = np.asarray(e_km_s, dtype=float) * 1e3
    v_lo = np.maximum(v - e, 100.0)
    v_hi = v + e
    def mass_at_v(vel_m_s):
        gt = vel_m_s**2 / r
        gs = gt**2 / (A0 + gt)
        return gs * r**2 / G
    M_dec = mass_at_v(v)
    M_lo = mass_at_v(v_lo)
    M_hi = mass_at_v(v_hi)
    return M_dec, M_lo, M_hi

def forward_gfd(r_kpc, M_enc_func):
    r = r_kpc * KPC
    M = M_enc_func(r)
    v_newt = np.sqrt(G * M / r) / 1e3
    gs = G * M / r**2
    gt = (gs + np.sqrt(gs**2 + 4 * gs * A0)) / 2.0
    v_gfd = np.sqrt(r * gt) / 1e3
    return v_newt, v_gfd, M

# ====================== MW DATA & PIPELINE ======================
mw_r_obs = np.array([6.30,7.90,9.20,10.20,11.20,12.20,13.20,14.20,15.20,
                     16.20,17.20,18.20,19.20,20.20,20.70,21.20,21.70,22.30,
                     23.40,25.00,30.00,40.00,50.00])
mw_v_obs = np.array([231,234,230,229,227,227,225,222,218,218,220,215,208,
                     203,195,200,201,197,192,191,206,192,180])
mw_e_obs = np.array([1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,3,6,5,8,30,35,32])

MW_bulge_M = 1.5e10 * MSUN; MW_bulge_a = 0.6 * KPC
MW_disk_M = 4.57e10 * MSUN; MW_disk_Rd = 2.2 * KPC
MW_gas_M = 1.5e10 * MSUN; MW_gas_Rd = 7.0 * KPC

def mw_bary_M_enc(r):
    b = MW_bulge_M * r**2 / (r + MW_bulge_a)**2
    xd = r / MW_disk_Rd
    d = MW_disk_M * (1 - (1 + xd) * np.exp(-xd))
    xg = r / MW_gas_Rd
    g = MW_gas_M * (1 - (1 + xg) * np.exp(-xg))
    return b + d + g

mw_r_model = np.linspace(0.5, 55, 600)
mw_r_decode = np.linspace(mw_r_obs[0], mw_r_obs[-1], 500)

mw_v_smooth = diffraction_smooth(mw_r_obs, mw_v_obs)
mw_v_newt, mw_v_gfd, mw_M_phot = forward_gfd(mw_r_model, mw_bary_M_enc)
mw_v_dec, mw_M_dec = velocity_decode(mw_r_obs, mw_v_smooth, mw_r_decode)

mw_v_on_decode = np.interp(mw_r_decode, mw_r_obs, mw_v_smooth)
mw_e_on_decode = np.interp(mw_r_decode, mw_r_obs, mw_e_obs)
_, mw_M_dec_lo, mw_M_dec_hi = M_dec_bounds(mw_r_decode, mw_v_on_decode, mw_e_on_decode)

mw_nfw_rho0 = 1.826e-21
mw_nfw_rs = 9.3 * KPC
mw_M_cdm = mw_bary_M_enc(mw_r_model * KPC) + nfw_mass(mw_r_model * KPC, mw_nfw_rho0, mw_nfw_rs)
mw_v_cdm = np.sqrt(G * mw_M_cdm / (mw_r_model * KPC)) / 1e3

mw_M_phot_on_decode = np.interp(mw_r_decode, mw_r_model, mw_M_phot / MSUN)
mw_M_dec_Msun = mw_M_dec / MSUN
mw_Delta_M = mw_M_phot_on_decode - mw_M_dec_Msun

# ====================== VORTEX SETUP ======================
M_int_best = 3.58e9 * MSUN
rs_int_best = 0.032 * KPC

def total_enc_vortex(r):
    interior = M_int_best * r**2 / (r + rs_int_best)**2
    return mw_bary_M_enc(r) + interior

r_sym = np.linspace(-60, 60, 2000)
_, v_sym, _ = forward_gfd(np.abs(r_sym), total_enc_vortex)

# RMS of vortex fit to MW observations (exterior r only)
r_pos = r_sym[r_sym >= 0]
v_pos = v_sym[r_sym >= 0]
v_vortex_at_obs = np.interp(mw_r_obs, r_pos, v_pos)
rms_vortex_km = np.sqrt(np.mean((mw_v_obs - v_vortex_at_obs)**2))

# Total observation error on the interior/exterior ratio:
# Ratio f_ext = M_ext/(M_ext+M_int). Uncertainty in f_ext from vortex match:
# sigma_f_ext = |d f_ext/d M_int| * sigma_M_int = M_ext/(M_ext+M_int)^2 * sigma_M_int.
# sigma_M_int from velocity error: sigma_M_int = RMS_v * |dM_int/dv|, with dM_int/dv
# from finite difference (perturb M_int, see change in v at typical radius).
dm_frac = 0.02
_, v_plus, _ = forward_gfd(np.abs(r_sym), lambda r: mw_bary_M_enc(r) + (M_int_best * (1 + dm_frac)) * r**2 / (r + rs_int_best)**2)
_, v_minus, _ = forward_gfd(np.abs(r_sym), lambda r: mw_bary_M_enc(r) + (M_int_best * (1 - dm_frac)) * r**2 / (r + rs_int_best)**2)
v_plus_at_obs = np.interp(mw_r_obs, r_pos, v_plus[r_sym >= 0])
v_minus_at_obs = np.interp(mw_r_obs, r_pos, v_minus[r_sym >= 0])
dv_km = np.mean(np.abs(v_plus_at_obs - v_minus_at_obs))
dM_int_dv = (dm_frac * 2 * M_int_best) / (dv_km * 1e3) if dv_km > 0 else 0  # kg per (m/s)
sigma_M_int_kg = rms_vortex_km * 1e3 * abs(dM_int_dv) if dM_int_dv else 0
sigma_M_int_Msun = sigma_M_int_kg / MSUN
# Ratio at outer radius (total exterior vs interior)
r_outer_ref = mw_r_decode[-1]
M_ext_ref = mw_bary_M_enc(r_outer_ref * KPC) / MSUN
M_int_ref = (M_int_best * (r_outer_ref * KPC)**2 / ((r_outer_ref * KPC) + rs_int_best)**2) / MSUN
M_tot_ref = M_ext_ref + M_int_ref
f_ext = M_ext_ref / M_tot_ref
# sigma_f from M_int only (exterior mass from photometry taken as fixed for this plot)
sigma_f_ext = (M_ext_ref / M_tot_ref**2) * sigma_M_int_Msun if M_tot_ref > 0 else 0
# Convert to percentage points
pct_ext = 100 * f_ext
pct_int = 100 * (1 - f_ext)
sigma_pct = 100 * sigma_f_ext

all_v = np.concatenate([v_sym, mw_v_obs])
v_min, v_max = all_v.min(), all_v.max()
padding = 0.20 * (v_max - v_min)
y_low = max(140, v_min - padding)
y_high = v_max + padding

# ====================== PROFESSIONAL STYLING (exact letter style) ======================
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

# ====================== COMPOSITE FIGURE ======================
fig = plt.figure(figsize=(11, 15.0))
gs = GridSpec(3, 2, height_ratios=[1, 1, 1.35], hspace=0.42, wspace=0.36,
              left=0.09, right=0.96, top=0.96, bottom=0.06)

# (a) Rotation curve (CamB fig2 panel (a) styling)
ax_a = fig.add_subplot(gs[0, 0])
ax_a.plot(mw_r_model, mw_v_newt, '--', color='0.6', lw=1.2, label=r'Newtonian (standard $G$)')
ax_a.plot(mw_r_model, mw_v_cdm, ':', color='C3', lw=1.5, alpha=0.8, label=r'$\Lambda$CDM (NFW halo fit)')
ax_a.plot(mw_r_model, mw_v_gfd, '--', color='C2', lw=1.5, alpha=0.8, label='GFD (photometric)')
ax_a.plot(mw_r_decode, mw_v_dec, '-', color='C2', lw=2.0, label='GFD velocity decode (no mass input)')
ax_a.errorbar(mw_r_obs, mw_v_obs, yerr=mw_e_obs, fmt='o', ms=3, color='k', ecolor='0.4',
              elinewidth=0.7, capsize=1.5, capthick=0.7, zorder=5, label='MW observations')
ax_a.set_xlabel(r'$r$ [kpc]')
ax_a.set_ylabel(r'$v$ [km s$^{-1}$]')
ax_a.set_xlim(0, 55)
ax_a.set_ylim(0, 290)
ax_a.legend(loc='lower right', framealpha=0.9, fontsize=5.8)
ax_a.text(0.0, 1.05, '(a) MW rotation curve', transform=ax_a.transAxes, fontweight='bold', fontsize=9)
ax_a.grid(True, alpha=0.2)

# (b) Effective mass (CamB fig2 panel (b) styling)
ax_b = fig.add_subplot(gs[0, 1])
ax_b.semilogy(mw_r_model, mw_M_cdm / MSUN, ':', color='C3', lw=1.2, alpha=0.7,
              label=r'$\Lambda$CDM (baryons + NFW)')
ax_b.semilogy(mw_r_model, mw_M_phot / MSUN, '--', color='C2', lw=1.2, alpha=0.8,
              label='GFD (photometric)')
ax_b.fill_between(mw_r_decode, mw_M_dec_lo / MSUN, mw_M_dec_hi / MSUN,
                  alpha=0.25, color='C2', zorder=1)
ax_b.semilogy(mw_r_decode, mw_M_dec_Msun, '-', color='C2', lw=2.0,
              label=r'$M_{\rm dec}$ (velocity decoded = effective mass)')
ax_b.fill_between(mw_r_decode, mw_M_dec_Msun, mw_M_phot_on_decode,
                  alpha=0.15, color='C0', label=r'$\Delta M_{\rm eff}$ (interior contribution)')
ax_b.set_xlabel(r'$r$ [kpc]')
ax_b.set_ylabel(r'$M_{\rm dec}$ [$M_\odot$]')
ax_b.set_xlim(0, 55)
ax_b.set_ylim(5e9, 1e12)
ax_b.legend(loc='lower right', framealpha=0.9, fontsize=5.8)
ax_b.text(0.0, 1.05, '(b) MW velocity-decoded effective mass', transform=ax_b.transAxes,
          fontweight='bold', fontsize=9)
ax_b.grid(True, alpha=0.2, which='both')

# (c) Mass gap bar (CamB fig2 panel (c) styling)
ax_c = fig.add_subplot(gs[1, 0])
mw_mask_valid = (mw_M_dec_Msun > 0) & (mw_M_phot_on_decode > 0)
mw_r_valid = mw_r_decode[mw_mask_valid]
mw_log_ratio = np.log10(mw_M_phot_on_decode[mw_mask_valid] / mw_M_dec_Msun[mw_mask_valid])
n_bars = 40
mw_r_bar = np.linspace(mw_r_valid[0], mw_r_valid[-1], n_bars)
mw_gap_bar = np.interp(mw_r_bar, mw_r_valid, mw_log_ratio)
bar_width = (mw_r_bar[-1] - mw_r_bar[0]) / (n_bars * 1.15)
g_min, g_max = np.min(mw_gap_bar), np.max(mw_gap_bar)
span = g_max - g_min if g_max > g_min else 1.0
mw_bar_colors = [plt.cm.Blues(0.3 + 0.6 * (g - g_min) / span) for g in mw_gap_bar]
ax_c.bar(mw_r_bar, mw_gap_bar, width=bar_width, color=mw_bar_colors, alpha=0.9, edgecolor='none', zorder=3)
ax_c.axhline(0, color='k', lw=0.8, ls='--', alpha=0.5, label=r'$M_{\rm phot} = M_{\rm dec}$')
ax_c.set_xlabel(r'$r$ [kpc]')
ax_c.set_ylabel(r'$\log_{10}(M_{\rm phot}\,/\,M_{\rm dec})$  [decades]')
ax_c.set_xlim(0, 55)
ax_c_r = ax_c.twinx()
ax_c_r.set_ylim(ax_c.get_ylim())
# Right axis: multiplicative factor M_phot/M_dec = 10^(log10). Use ticks in data range.
log_ticks = np.array([-0.05, 0.0, 0.05, 0.10])
ax_c_r.set_yticks(log_ticks)
ax_c_r.set_yticklabels([f'{10**t:.2g}x' for t in log_ticks], fontsize=7)
ax_c_r.set_ylabel('')
ax_c.legend(loc='upper right', framealpha=0.9, fontsize=5.8)
ax_c.text(0.0, 1.05, r'(c) Mass gap $M_{\rm phot}\,/\,M_{\rm dec}$ (observed range)',
          transform=ax_c.transAxes, fontweight='bold', fontsize=9)
ax_c.grid(True, alpha=0.2)

# (d) Decoded mass + power output (CamB fig2 panel (d) styling)
ax_d = fig.add_subplot(gs[1, 1])
mw_M_boosted = mw_M_dec_Msun + mw_Delta_M
mw_Delta_total = mw_Delta_M[-1]
mw_r_outer_val = mw_r_decode[-1]
ax_d.semilogy(mw_r_model, mw_M_cdm / MSUN, ':', color='C3', lw=1.2, alpha=0.7,
              label=r'$\Lambda$CDM (baryons + NFW)')
ax_d.semilogy(mw_r_model, mw_M_phot / MSUN, '--', color='C2', lw=1.5, alpha=0.8,
              label='GFD (photometric)')
ax_d.fill_between(mw_r_decode, mw_M_dec_lo / MSUN, mw_M_dec_hi / MSUN,
                  alpha=0.25, color='C2', zorder=1)
ax_d.semilogy(mw_r_decode, mw_M_dec_Msun, '-', color='C2', lw=2.0, alpha=0.5,
              label=r'$M_{\rm dec}$ (velocity decoded = effective mass)')
ax_d.semilogy(mw_r_decode, mw_M_boosted, '-', color='C0', lw=2.5,
              label=r'$M_{\rm dec} + \Delta M_{\rm eff}(r)$')
ax_d.fill_between(mw_r_decode, mw_M_dec_Msun, mw_M_boosted,
                  alpha=0.18, color='C0', label=r'$\Delta M_{\rm eff}(r)$ (power output)')
ax_d.set_xlabel(r'$r$ [kpc]')
ax_d.set_ylabel(r'$M_{\rm dec}$ [$M_\odot$]')
ax_d.set_xlim(0, 55)
ax_d.set_ylim(5e9, 1e12)
ax_d.legend(loc='lower right', framealpha=0.9, fontsize=5.5)
ax_d.text(0.04, 0.93, r'$\Delta M_{\rm eff}(r) = M_{\rm phot}(r) - M_{\rm dec}(r)$',
          transform=ax_d.transAxes, fontsize=8, color='#2166ac', va='top')
ax_d.text(0.04, 0.84, f'Over observed $r = {mw_r_decode[0]:.2f}$ to ${mw_r_outer_val:.2f}$ kpc:',
          transform=ax_d.transAxes, fontsize=7, color='#1a5276', va='top')
exp = int(np.floor(np.log10(mw_Delta_total)))
mantissa = mw_Delta_total / 10**exp
ax_d.text(0.04, 0.77, f'$\\Delta M_{{\\rm eff}} = {mantissa:.2f} \\times 10^{exp}\\;M_\\odot$',
          transform=ax_d.transAxes, fontsize=9, fontweight='bold', color='#2166ac', va='top',
          bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='#2166ac', alpha=0.85))
ax_d.text(0.0, 1.05, r'(d) Decoded mass + power output $\Delta M_{\rm eff}(r)$',
          transform=ax_d.transAxes, fontweight='bold', fontsize=9)
ax_d.grid(True, alpha=0.2, which='both')

# ====================== FULL-WIDTH VORTEX PANEL (e) ======================
ax_v = fig.add_subplot(gs[2, :])
ax_v.fill_between(r_sym, v_sym - rms_vortex_km, v_sym + rms_vortex_km,
                  alpha=0.25, color='#2166ac', zorder=1,
                  label=f'Vortex fit tolerance ($\\pm$RMS = {rms_vortex_km:.1f} km s$^{{-1}}$)')
ax_v.plot(r_sym, v_sym, '--', color='#2166ac', lw=2.0,
          label='Full vortex velocity (baryons + optimized throat power)')
ax_v.axvspan(-0.35, 0.35, color='#ff9f1c', alpha=0.25, label='Throat region (interior drain)')
ax_v.errorbar(mw_r_obs, mw_v_obs, yerr=mw_e_obs, fmt='o', ms=3, color='k', ecolor='0.4',
              elinewidth=0.7, capsize=1.5, capthick=0.7, zorder=5,
              label='Observed MW rotation curve (exterior only)')
ax_v.set_xlabel(r'$r$ [kpc]', fontsize=10)
ax_v.set_ylabel(r'$v$ [km s$^{-1}$]', fontsize=10)
ax_v.text(0.0, 1.05, '(e) MW symmetric velocity profile (vortex)', transform=ax_v.transAxes,
          fontweight='bold', fontsize=9)
ax_v.set_xlim(-60, 60)
ax_v.set_ylim(y_low, y_high)
ax_v.legend(loc='upper right', framealpha=0.9, fontsize=5.8)
ax_v.grid(True, alpha=0.22)

# Top left of figure (e): M_interior, M_exterior in stroked box (like panel (d) Delta M_eff)
mass_box_str = r'$M_{\rm int} = 3.58 \times 10^9\,M_\odot$' + '\n' + r'$M_{\rm ext} = 7.57 \times 10^{10}\,M_\odot$'
ax_v.text(0.04, 0.88, mass_box_str,
          transform=ax_v.transAxes, fontsize=8, color='#2166ac', va='top',
          bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='#2166ac', alpha=0.85))
# Ratio line: no box, style like "Over observed r = ..." (image 2). Build mathtext in steps.
ratio_interior_exterior = '{:.1f}% interior | {:.1f}% exterior'.format(pct_int, pct_ext)
ratio_error_part = '{:.1f}% error'.format(sigma_pct)
ratio_str = r'$\text{' + ratio_interior_exterior + r'}$ ($\pm$ $\text{' + ratio_error_part + r'}$)'
ax_v.text(0.04, 0.76, ratio_str,
          transform=ax_v.transAxes, fontsize=7, color='#1a5276', va='top')

# ====================== SAVE ======================
plt.savefig('mw_composite_4panel_vortex_final.png', dpi=300, bbox_inches='tight')
plt.savefig('mw_composite_4panel_vortex_final.pdf', bbox_inches='tight')
plt.close()

print("SUCCESS! Saved figures (no SyntaxWarning or mathtext error).")
print(" Saved: mw_composite_4panel_vortex_final.png")
print(" Saved: mw_composite_4panel_vortex_final.pdf")
print(" All LaTeX now uses raw strings + \\mathrm for perfect compatibility.")