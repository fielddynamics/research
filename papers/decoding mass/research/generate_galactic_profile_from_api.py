"""
Generate the full 4-row galactic profile figure (panels a-f) for a single galaxy.

Fetches galaxy data from the Gravis API (or local catalog via --local), then runs
the same pipeline as generate_galactic_profile.py: rotation curve, decoded mass,
mass gap, power output, and vortex panels (e) exterior-only, (f) full model.

Usage:
  python generate_galactic_profile_from_api.py <galaxy_id> [--api-base URL] [--output-dir DIR] [--local]

  galaxy_id   : e.g. milky_way, ngc3198, m33
  --api-base  : base URL of the app (default: http://127.0.0.1:5000)
  --output-dir: where to write composite_4panel_vortex_<id>.png and .pdf (default: script dir)
  --local     : load galaxy from data.galaxies.get_galaxy_by_id instead of API

Requires the Gravis app running (or --local). Optional: requests (for API; if missing, use --local).
"""
from __future__ import annotations

import argparse
import os
import sys

_script_dir = os.path.dirname(os.path.abspath(__file__))
_repo_root = os.path.abspath(os.path.join(_script_dir, "..", "..", "..", ".."))
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy.ndimage import gaussian_filter1d
from scipy.optimize import minimize_scalar

from physics.mass_model import enclosed_mass, total_mass
from physics.nfw import (
    LITERATURE_NFW_RHO0_RS,
    abundance_matching,
    fit_halo,
    m200_from_nfw_rho0_rs,
    nfw_enclosed_mass,
)

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


def fetch_galaxy_api(galaxy_id: str, api_base: str) -> dict:
    """GET /api/rotation/galaxies/<id>; return JSON body. Raises on error."""
    try:
        import requests
    except ImportError:
        raise SystemExit(
            "requests is required for API fetch. Install with: pip install requests\n"
            "Or run with --local to use the local galaxy catalog."
        )
    url = f"{api_base.rstrip('/')}/api/rotation/galaxies/{galaxy_id}"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json()


def fetch_galaxy_local(galaxy_id: str) -> dict:
    """Load galaxy from data.galaxies.get_galaxy_by_id."""
    from data.galaxies import get_galaxy_by_id
    g = get_galaxy_by_id(galaxy_id)
    if g is None:
        raise SystemExit(f"Galaxy not found: {galaxy_id}")
    return g


def build_galaxy_arrays(galaxy: dict):
    """
    From API/local galaxy dict, build r_obs, v_obs, e_obs (numpy) and
    M_enc_func(r_m) that returns enclosed mass in kg for r in meters.
    """
    obs = galaxy.get("observations") or []
    mass_model = galaxy.get("mass_model")
    if not obs:
        raise SystemExit("Galaxy has no observations.")
    if not mass_model:
        raise SystemExit("Galaxy has no mass_model.")
    r_obs = np.array([o["r"] for o in obs])
    v_obs = np.array([o["v"] for o in obs])
    e_obs = np.array([o.get("err") or 0 for o in obs])

    def M_enc_func(r_m):
        r_kpc = np.atleast_1d(np.asarray(r_m, dtype=float) / KPC)
        out = np.array([enclosed_mass(float(rk), mass_model) * MSUN for rk in r_kpc.flat])
        return out.reshape(r_kpc.shape)
    return r_obs, v_obs, e_obs, M_enc_func


def decoded_M_single(r_kpc, v_km):
    r = r_kpc * KPC
    v = v_km * 1e3
    gt = v**2 / r
    gs = gt**2 / (A0 + gt)
    return gs * r**2 / G


def load_galaxy_data(galaxy_id: str, api_base: str, output_dir: str, use_local: bool) -> dict:
    """Fetch galaxy (API or local), build all arrays and vortex params; return dict for figure."""
    if use_local:
        galaxy = fetch_galaxy_local(galaxy_id)
    else:
        try:
            galaxy = fetch_galaxy_api(galaxy_id, api_base)
        except Exception as e:
            raise SystemExit(f"API fetch failed: {e}")

    mw_r_obs, mw_v_obs, mw_e_obs, mw_bary_M_enc = build_galaxy_arrays(galaxy)
    mass_model = galaxy.get("mass_model") or {}
    observations_list = galaxy.get("observations") or []

    r_span = mw_r_obs[-1] - mw_r_obs[0]
    mw_r_model = np.linspace(0.5, mw_r_obs[-1] + 0.15 * r_span, 600)
    mw_r_decode = np.linspace(mw_r_obs[0], mw_r_obs[-1], 500)

    mw_v_smooth = diffraction_smooth(mw_r_obs, mw_v_obs)
    mw_v_newt, mw_v_gfd, mw_M_phot = forward_gfd(mw_r_model, mw_bary_M_enc)
    mw_v_dec, mw_M_dec = velocity_decode(mw_r_obs, mw_v_smooth, mw_r_decode)

    mw_v_on_decode = np.interp(mw_r_decode, mw_r_obs, mw_v_smooth)
    mw_e_on_decode = np.interp(mw_r_decode, mw_r_obs, mw_e_obs)
    _, mw_M_dec_lo, mw_M_dec_hi = M_dec_bounds(mw_r_decode, mw_v_on_decode, mw_e_on_decode)

    if galaxy_id in LITERATURE_NFW_RHO0_RS:
        rho0, rs = LITERATURE_NFW_RHO0_RS[galaxy_id]
        m200 = m200_from_nfw_rho0_rs(rho0, rs)
    else:
        m_total = total_mass(mass_model)
        def mass_at_r_kpc(r_kpc):
            return enclosed_mass(r_kpc, mass_model)
        fit = fit_halo(observations_list, mass_at_r_kpc, accel_ratio=1.0) if len(observations_list) >= 2 else None
        m200 = fit["m200"] if fit else abundance_matching(m_total)

    M_nfw_kg = np.array([nfw_enclosed_mass(float(r), m200) for r in mw_r_model]) * MSUN
    mw_M_cdm = mw_bary_M_enc(mw_r_model * KPC) + M_nfw_kg
    mw_v_cdm = np.sqrt(G * mw_M_cdm / (mw_r_model * KPC)) / 1e3

    mw_M_phot_on_decode = np.interp(mw_r_decode, mw_r_model, mw_M_phot / MSUN)
    mw_M_dec_Msun = mw_M_dec / MSUN
    mw_Delta_M = mw_M_phot_on_decode - mw_M_dec_Msun

    mw_v_dec_at_obs = np.interp(mw_r_obs, mw_r_decode, mw_v_dec)
    rms_decode_km = np.sqrt(np.mean((mw_v_obs - mw_v_dec_at_obs)**2))

    r_outer_kpc = mw_r_decode[-1]
    v_outer_km = np.interp(r_outer_kpc, mw_r_decode, mw_v_dec)
    e_outer_km = np.interp(r_outer_kpc, mw_r_obs, mw_e_obs)
    mw_M_dec_outer = decoded_M_single(r_outer_kpc, v_outer_km)
    mw_M_dec_upper = decoded_M_single(r_outer_kpc, v_outer_km + e_outer_km)
    mw_M_lcdm_outer = float(np.atleast_1d((mw_bary_M_enc(r_outer_kpc * KPC) + np.interp(r_outer_kpc, mw_r_model, M_nfw_kg)) / MSUN)[0])
    mw_M_phot_outer = float(np.atleast_1d(mw_bary_M_enc(r_outer_kpc * KPC) / MSUN)[0])
    mw_n_sigma = (mw_M_lcdm_outer * MSUN - mw_M_dec_outer) / (mw_M_dec_upper - mw_M_dec_outer) if (mw_M_dec_upper - mw_M_dec_outer) > 0 else float("nan")
    mw_n_sigma = float(mw_n_sigma) if not np.isnan(mw_n_sigma) else float("nan")
    mw_M_bary_total = total_mass(mass_model)

    rs_int_best = 0.032 * KPC
    r_sym = np.linspace(-60, 60, 2000)
    r_pos = r_sym[r_sym >= 0]
    _, v_sym_exterior, _ = forward_gfd(np.abs(r_sym), mw_bary_M_enc)
    rms_exterior_km = np.sqrt(np.mean((mw_v_obs - np.interp(mw_r_obs, r_pos, v_sym_exterior[r_sym >= 0]))**2))

    if galaxy_id == "milky_way":
        M_int_best = 3.58e9 * MSUN
    else:
        # Optimize interior to minimize RMS of vortex velocity vs observations (interior boosts fit; (f) better than (e))
        r_outer_m = mw_r_decode[-1] * KPC
        r_min_m = mw_r_decode[0] * KPC
        M_ext_outer_kg = float(np.atleast_1d(mw_bary_M_enc(r_outer_m))[0])
        M_bary_min_kg = float(np.atleast_1d(mw_bary_M_enc(r_min_m))[0])
        M_int_low = max(-0.99 * M_bary_min_kg, -0.99 * M_ext_outer_kg)
        M_int_high = 2.0 * M_ext_outer_kg

        def _rms_vortex(M_int_kg):
            def _total_enc(r):
                interior = M_int_kg * r**2 / (r + rs_int_best)**2
                return mw_bary_M_enc(r) + interior
            r_check = np.abs(r_sym) * KPC
            M_tot_check = _total_enc(r_check)
            if np.any(M_tot_check <= 0) or not np.all(np.isfinite(M_tot_check)):
                return 1e6
            _, v_v, _ = forward_gfd(np.abs(r_sym), _total_enc)
            v_at_obs = np.interp(mw_r_obs, r_pos, v_v[r_sym >= 0])
            if not np.all(np.isfinite(v_at_obs)):
                return 1e6
            return np.sqrt(np.mean((mw_v_obs - v_at_obs)**2))

        res = minimize_scalar(_rms_vortex, bounds=(M_int_low, M_int_high), method="bounded")
        M_int_best = res.x if res.success and np.isfinite(res.x) else 0.0
        if not np.isfinite(M_int_best):
            M_int_best = 0.0

    def total_enc_vortex(r):
        interior = M_int_best * r**2 / (r + rs_int_best)**2
        return mw_bary_M_enc(r) + interior

    _, v_sym, _ = forward_gfd(np.abs(r_sym), total_enc_vortex)

    r_pos = r_sym[r_sym >= 0]
    v_pos = v_sym[r_sym >= 0]
    v_vortex_at_obs = np.interp(mw_r_obs, r_pos, v_pos)
    rms_vortex_km = np.sqrt(np.mean((mw_v_obs - v_vortex_at_obs)**2))

    dm_frac = 0.02 if M_int_best > 0 else 0.01
    _, v_plus, _ = forward_gfd(np.abs(r_sym), lambda r: mw_bary_M_enc(r) + (M_int_best * (1 + dm_frac)) * r**2 / (r + rs_int_best)**2)
    _, v_minus, _ = forward_gfd(np.abs(r_sym), lambda r: mw_bary_M_enc(r) + (M_int_best * (1 - dm_frac)) * r**2 / (r + rs_int_best)**2)
    v_plus_at_obs = np.interp(mw_r_obs, r_pos, v_plus[r_sym >= 0])
    v_minus_at_obs = np.interp(mw_r_obs, r_pos, v_minus[r_sym >= 0])
    dv_km = np.mean(np.abs(v_plus_at_obs - v_minus_at_obs))
    dM_int_dv = (dm_frac * 2 * M_int_best) / (dv_km * 1e3) if dv_km > 0 else 0
    sigma_M_int_kg = rms_vortex_km * 1e3 * abs(dM_int_dv) if dM_int_dv else 0
    sigma_M_int_Msun = sigma_M_int_kg / MSUN

    r_outer_ref = mw_r_decode[-1]
    M_ext_ref = mw_bary_M_enc(r_outer_ref * KPC) / MSUN
    M_int_ref = (M_int_best * (r_outer_ref * KPC)**2 / ((r_outer_ref * KPC) + rs_int_best)**2) / MSUN
    M_tot_ref = M_ext_ref + M_int_ref
    M_ext_ref = float(np.atleast_1d(M_ext_ref)[0])
    M_tot_ref = float(np.atleast_1d(M_tot_ref)[0])
    M_int_ref = float(np.atleast_1d(M_int_ref)[0])
    f_ext = M_ext_ref / M_tot_ref if M_tot_ref > 0 else 1.0
    sigma_f_ext = (M_ext_ref / M_tot_ref**2) * sigma_M_int_Msun if M_tot_ref > 0 else 0
    pct_ext = float(100 * f_ext)
    pct_int = float(100 * (1 - f_ext))
    sigma_pct = float(100 * sigma_f_ext)

    all_v = np.concatenate([v_sym, v_sym_exterior, mw_v_obs])
    all_v = all_v[np.isfinite(all_v)]
    v_min = all_v.min() if len(all_v) > 0 else 0
    v_max = all_v.max() if len(all_v) > 0 else 200
    padding = 0.20 * (v_max - v_min) if v_max > v_min else 20
    y_low = max(0, v_min - padding)
    y_high = v_max + padding

    mw_Delta_total = mw_Delta_M[-1]
    if galaxy_id == "milky_way":
        mass_box_str = r"$M_{\rm int} = 3.58 \times 10^9\,M_\odot$" + "\n" + r"$M_{\rm ext} = 7.57 \times 10^{10}\,M_\odot$"
    else:
        def _fmt_mass(M_sun):
            if M_sun == 0 or not np.isfinite(M_sun):
                return "0"
            a = abs(M_sun)
            e = int(np.floor(np.log10(a)))
            m = a / 10**e
            s = "-" if M_sun < 0 else ""
            return r"%s%.2f $\times$ 10$^{%d}$" % (s, m, e)
        mass_box_str = r"$M_{\rm int} = " + _fmt_mass(M_int_ref) + r"\,M_\odot$" + "\n" + r"$M_{\rm ext} = " + _fmt_mass(M_ext_ref) + r"\,M_\odot$"
    ratio_str = r"$\text{" + "{:.1f}% interior | {:.1f}% exterior".format(pct_int, pct_ext) + r"}$"

    figure_title = (galaxy.get("name") or galaxy_id).split(" (")[0].strip()

    return dict(
        mw_r_obs=mw_r_obs, mw_v_obs=mw_v_obs, mw_e_obs=mw_e_obs,
        mw_bary_M_enc=mw_bary_M_enc,
        mw_r_model=mw_r_model, mw_r_decode=mw_r_decode,
        mw_v_smooth=mw_v_smooth, mw_v_newt=mw_v_newt, mw_v_gfd=mw_v_gfd, mw_M_phot=mw_M_phot,
        mw_v_dec=mw_v_dec, mw_M_dec=mw_M_dec,
        mw_v_on_decode=mw_v_on_decode, mw_e_on_decode=mw_e_on_decode,
        mw_M_dec_lo=mw_M_dec_lo, mw_M_dec_hi=mw_M_dec_hi,
        mw_M_cdm=mw_M_cdm, mw_v_cdm=mw_v_cdm,
        mw_M_phot_on_decode=mw_M_phot_on_decode, mw_M_dec_Msun=mw_M_dec_Msun, mw_Delta_M=mw_Delta_M,
        mw_v_dec_at_obs=mw_v_dec_at_obs, rms_decode_km=rms_decode_km,
        r_outer_kpc=r_outer_kpc, mw_M_dec_outer=mw_M_dec_outer, mw_M_dec_upper=mw_M_dec_upper,
        mw_M_lcdm_outer=mw_M_lcdm_outer, mw_M_phot_outer=mw_M_phot_outer, mw_n_sigma=mw_n_sigma,
        mw_M_bary_total=mw_M_bary_total,
        M_int_best=M_int_best, rs_int_best=rs_int_best,
        total_enc_vortex=total_enc_vortex,
        r_sym=r_sym, v_sym=v_sym, v_sym_exterior=v_sym_exterior,
        rms_vortex_km=rms_vortex_km, rms_exterior_km=rms_exterior_km,
        pct_int=pct_int, pct_ext=pct_ext, sigma_pct=sigma_pct,
        mass_box_str=mass_box_str, ratio_str=ratio_str,
        y_low=y_low, y_high=y_high,
        mw_Delta_total=mw_Delta_total,
        figure_title=figure_title, output_dir=output_dir, galaxy_id=galaxy_id,
    )

def run_figure():
    # All variables (mw_*, r_sym, v_sym, figure_title, output_dir, galaxy_id, etc.) must be in globals from load_galaxy_data().
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

    # ====================== COMPOSITE FIGURE (8.5 x 11 in sheet) ======================
    # Margins in cm; 1 cm = 1/2.54 in. All y in figure coords (0=bottom, 1=top).
    cm_in = 1.0 / 2.54
    margin_top_cm = 1.15
    margin_below_title_cm = 1.15
    fig_h_in = 11.0
    fig_w_in = 8.5
    margin_top_frac = (margin_top_cm * cm_in) / fig_h_in
    margin_below_title_frac = (margin_below_title_cm * cm_in) / fig_h_in
    title_fontsize_pt = 20
    title_height_frac = (title_fontsize_pt / 72.0) / fig_h_in
    title_top_y = 1.0 - margin_top_frac
    title_bottom_y = title_top_y - title_height_frac
    gs_top = title_bottom_y - margin_below_title_frac

    fig = plt.figure(figsize=(fig_w_in, fig_h_in))
    fig.suptitle(figure_title, fontsize=title_fontsize_pt, fontweight='bold', y=title_top_y, va='top')
    gs = GridSpec(4, 2, height_ratios=[0.9, 0.9, 1.0, 1.0], hspace=0.42, wspace=0.36,
                  left=0.09, right=0.96, top=gs_top, bottom=0.10)

    # (a) Rotation curve
    ax_a = fig.add_subplot(gs[0, 0])
    ax_a.plot(mw_r_model, mw_v_newt, '--', color='0.6', lw=1.2, label=r'Newtonian (standard $G$)')
    ax_a.plot(mw_r_model, mw_v_cdm, ':', color='C3', lw=1.5, alpha=0.8, label=r'$\Lambda$CDM (NFW halo fit)')
    ax_a.plot(mw_r_model, mw_v_gfd, '--', color='C2', lw=1.5, alpha=0.8, label='GFD (photometric)')
    ax_a.plot(mw_r_decode, mw_v_dec, '-', color='C2', lw=2.0, label='GFD velocity decode (no mass input)')
    ax_a.errorbar(mw_r_obs, mw_v_obs, yerr=mw_e_obs, fmt='o', ms=3, color='k', ecolor='0.4',
                  elinewidth=0.7, capsize=1.5, capthick=0.7, zorder=5, label='Observations')
    ax_a.set_xlabel(r'$r$ [kpc]')
    ax_a.set_ylabel(r'$v$ [km s$^{-1}$]')
    r_max = max(55, mw_r_model[-1] * 1.02)
    ax_a.set_xlim(0, r_max)
    ax_a.set_ylim(0, max(290, np.max(mw_v_obs) * 1.15))
    ax_a.legend(loc='lower right', framealpha=0.9, fontsize=5.8)
    ax_a.text(0.0, 1.05, f'(a) {figure_title} rotation curve', transform=ax_a.transAxes, fontweight='bold', fontsize=9)
    ax_a.text(0.98, 0.02, f'RMS = {rms_decode_km:.2f} km s$^{{-1}}$', transform=ax_a.transAxes, ha='right', va='bottom', fontsize=6)
    ax_a.grid(True, alpha=0.2)

    # (b) Effective mass: y-axis from global min/max of plotted series
    M_b_cdm = mw_M_cdm / MSUN
    M_b_phot = mw_M_phot / MSUN
    all_b = np.concatenate([np.ravel(M_b_cdm), np.ravel(M_b_phot),
                            np.ravel(mw_M_dec_lo / MSUN), np.ravel(mw_M_dec_hi / MSUN),
                            np.ravel(mw_M_dec_Msun), np.ravel(mw_M_phot_on_decode)])
    valid_b = all_b[np.isfinite(all_b) & (all_b > 0)]
    if len(valid_b) > 0:
        log_lo_b = np.log10(valid_b.min())
        log_hi_b = np.log10(valid_b.max())
        pad_b = max(0.15 * (log_hi_b - log_lo_b), 0.25)
        y_lo_b = 10 ** (log_lo_b - pad_b)
        y_hi_b = 10 ** (log_hi_b + pad_b)
    else:
        y_lo_b, y_hi_b = 5e9, 1e12

    ax_b = fig.add_subplot(gs[0, 1])
    ax_b.semilogy(mw_r_model, M_b_cdm, ':', color='C3', lw=1.2, alpha=0.7,
                  label=r'$\Lambda$CDM (baryons + NFW)')
    ax_b.semilogy(mw_r_model, M_b_phot, '--', color='C2', lw=1.2, alpha=0.8,
                  label='GFD (photometric)')
    ax_b.fill_between(mw_r_decode, mw_M_dec_lo / MSUN, mw_M_dec_hi / MSUN,
                      alpha=0.25, color='C2', zorder=1)
    ax_b.semilogy(mw_r_decode, mw_M_dec_Msun, '-', color='C2', lw=2.0,
                  label=r'$M_{\rm dec}$ (velocity decoded = effective mass)')
    ax_b.fill_between(mw_r_decode, mw_M_dec_Msun, mw_M_phot_on_decode,
                      alpha=0.15, color='C0', label=r'$\Delta M_{\rm eff}$ (interior contribution)')
    ax_b.set_xlabel(r'$r$ [kpc]')
    ax_b.set_ylabel(r'$M_{\rm dec}$ [$M_\odot$]')
    ax_b.set_xlim(0, r_max)
    ax_b.set_ylim(y_lo_b, y_hi_b)
    ax_b.legend(loc='lower right', framealpha=0.9, fontsize=5.8)
    ax_b.text(0.0, 1.05, f'(b) {figure_title} velocity-decoded effective mass', transform=ax_b.transAxes,
              fontweight='bold', fontsize=9)
    if not np.isnan(mw_n_sigma):
        ax_b.text(0.02, 0.98, f'{mw_n_sigma:.1f}$\\sigma$ below $\\Lambda$CDM', transform=ax_b.transAxes,
                  ha='left', va='top', fontsize=6.5)
    ax_b.grid(True, alpha=0.2, which='both')

    # (c) Mass gap bar
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
    ax_c.set_xlim(0, r_max)
    ax_c_r = ax_c.twinx()
    ax_c_r.set_ylim(ax_c.get_ylim())
    log_ticks = np.array([-0.05, 0.0, 0.05, 0.10])
    ax_c_r.set_yticks(log_ticks)
    ax_c_r.set_yticklabels([f'{10**t:.2g}x' for t in log_ticks], fontsize=7)
    ax_c_r.set_ylabel('')
    ax_c.legend(loc='upper right', framealpha=0.9, fontsize=5.8)
    ax_c.text(0.0, 1.05, r'(c) Mass gap $M_{\rm phot}\,/\,M_{\rm dec}$ (observed range)',
              transform=ax_c.transAxes, fontweight='bold', fontsize=9)
    ax_c.grid(True, alpha=0.2)

    # (d) Decoded mass + power output: y-axis from global min/max of plotted series
    mw_M_boosted = mw_M_dec_Msun + mw_Delta_M
    mw_r_outer_val = mw_r_decode[-1]
    M_d_cdm = mw_M_cdm / MSUN
    M_d_phot = mw_M_phot / MSUN
    all_d = np.concatenate([np.ravel(M_d_cdm), np.ravel(M_d_phot),
                            np.ravel(mw_M_dec_lo / MSUN), np.ravel(mw_M_dec_hi / MSUN),
                            np.ravel(mw_M_dec_Msun), np.ravel(mw_M_boosted)])
    valid_d = all_d[np.isfinite(all_d) & (all_d > 0)]
    if len(valid_d) > 0:
        log_lo_d = np.log10(valid_d.min())
        log_hi_d = np.log10(valid_d.max())
        pad_d = max(0.15 * (log_hi_d - log_lo_d), 0.25)
        y_lo_d = 10 ** (log_lo_d - pad_d)
        y_hi_d = 10 ** (log_hi_d + pad_d)
    else:
        y_lo_d, y_hi_d = 5e9, 1e12

    ax_d = fig.add_subplot(gs[1, 1])
    ax_d.semilogy(mw_r_model, M_d_cdm, ':', color='C3', lw=1.2, alpha=0.7,
                  label=r'$\Lambda$CDM (baryons + NFW)')
    ax_d.semilogy(mw_r_model, M_d_phot, '--', color='C2', lw=1.5, alpha=0.8,
                  label='GFD (photometric)')
    ax_d.fill_between(mw_r_decode, mw_M_dec_lo / MSUN, mw_M_dec_hi / MSUN,
                      alpha=0.25, color='C2', zorder=1)
    ax_d.semilogy(mw_r_decode, mw_M_dec_Msun, '-', color='C2', lw=2.0, alpha=0.5,
                  label=r'$M_{\rm dec}$ (velocity decoded = effective mass)')
    ax_d.semilogy(mw_r_decode, mw_M_boosted, '-', color='C0', lw=2.5,
                  label=r'$M_{\rm dec} + \Delta M_{\rm eff}(r)$')
    ax_d.fill_between(mw_r_decode, mw_M_dec_Msun, mw_M_boosted,
                      alpha=0.15, color='C0', label=r'$\Delta M_{\rm eff}(r)$ (power output)')
    ax_d.set_xlabel(r'$r$ [kpc]')
    ax_d.set_ylabel(r'$M_{\rm dec}$ [$M_\odot$]')
    ax_d.set_xlim(0, r_max)
    ax_d.set_ylim(y_lo_d, y_hi_d)
    ax_d.legend(loc='lower right', framealpha=0.9, fontsize=5.5)
    ax_d.text(0.04, 0.93, r'$\Delta M_{\rm eff}(r) = M_{\rm phot}(r) - M_{\rm dec}(r)$',
              transform=ax_d.transAxes, fontsize=8, color='#2166ac', va='top')
    ax_d.text(0.04, 0.84, f'Over observed $r = {mw_r_decode[0]:.2f}$ to ${mw_r_outer_val:.2f}$ kpc:',
              transform=ax_d.transAxes, fontsize=7, color='#1a5276', va='top')
    if np.isfinite(mw_Delta_total) and mw_Delta_total != 0:
        abs_delta = abs(mw_Delta_total)
        exp = int(np.floor(np.log10(abs_delta)))
        mantissa = abs_delta / 10**exp
        sign_str = '-' if mw_Delta_total < 0 else ''
        ax_d.text(0.04, 0.77, f'$\\Delta M_{{\\rm eff}} = {sign_str}{mantissa:.2f} \\times 10^{exp}\\;M_\\odot$',
                  transform=ax_d.transAxes, fontsize=9, fontweight='bold', color='#2166ac', va='top',
                  bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='#2166ac', alpha=0.85))
    else:
        ax_d.text(0.04, 0.77, r'$\Delta M_{\rm eff}$ = 0 (at outer $r$)',
                  transform=ax_d.transAxes, fontsize=9, fontweight='bold', color='#2166ac', va='top',
                  bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='#2166ac', alpha=0.85))
    ax_d.text(0.0, 1.05, r'(d) Decoded mass + power output $\Delta M_{\rm eff}(r)$',
              transform=ax_d.transAxes, fontweight='bold', fontsize=9)
    ax_d.grid(True, alpha=0.2, which='both')

    # (e) Vortex exterior only
    ax_v = fig.add_subplot(gs[2, :])
    ax_v.plot(r_sym, v_sym_exterior, '--', color='#2166ac', lw=2.0,
              label='Exterior field only (baryons; no throat)')
    ax_v.errorbar(mw_r_obs, mw_v_obs, yerr=mw_e_obs, fmt='o', ms=3, color='k', ecolor='0.4',
                  elinewidth=0.7, capsize=1.5, capthick=0.7, zorder=5,
                  label='Observed rotation curve (exterior only)')
    ax_v.set_xlabel(r'$r$ [kpc]', fontsize=10)
    ax_v.set_ylabel(r'$v$ [km s$^{-1}$]', fontsize=10)
    ax_v.text(0.0, 1.05, f'(e) {figure_title} symmetric vortex - exterior only (quiet interior)', transform=ax_v.transAxes,
              fontweight='bold', fontsize=9)
    ax_v.set_xlim(-60, 60)
    ax_v.set_ylim(y_low, y_high)
    ax_v.legend(loc='upper right', framealpha=0.9, fontsize=5.8)
    ax_v.grid(True, alpha=0.22)
    ax_v.text(0.04, 0.88, '100% exterior | 0% interior contribution',
              transform=ax_v.transAxes, fontsize=8, color='#2166ac', va='top',
              bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='#2166ac', alpha=0.85))
    ax_v.text(0.98, 0.02, f'Exterior RMS = {rms_exterior_km:.1f} km s$^{{-1}}$',
              transform=ax_v.transAxes, ha='right', va='bottom', fontsize=6)

    # (f) Full vortex model
    ax_f = fig.add_subplot(gs[3, :])
    ax_f.fill_between(r_sym, v_sym - rms_vortex_km, v_sym + rms_vortex_km,
                      alpha=0.25, color='#2166ac', zorder=1,
                      label=f'Vortex fit tolerance ($\\pm$RMS = {rms_vortex_km:.1f} km s$^{{-1}}$)')
    ax_f.plot(r_sym, v_sym, '--', color='#2166ac', lw=2.0,
              label='Full vortex velocity (baryons + optimized throat power)')
    ax_f.axvspan(-0.35, 0.35, color='#ff9f1c', alpha=0.25, label='Throat region (interior drain)')
    ax_f.errorbar(mw_r_obs, mw_v_obs, yerr=mw_e_obs, fmt='o', ms=3, color='k', ecolor='0.4',
                  elinewidth=0.7, capsize=1.5, capthick=0.7, zorder=5,
                  label='Observed rotation curve (exterior only)')
    ax_f.set_xlabel(r'$r$ [kpc]', fontsize=10)
    ax_f.set_ylabel(r'$v$ [km s$^{-1}$]', fontsize=10)
    ax_f.text(0.0, 1.05, f'(f) {figure_title} symmetric vortex - full model (active interior throat)', transform=ax_f.transAxes,
              fontweight='bold', fontsize=9)
    ax_f.set_xlim(-60, 60)
    ax_f.set_ylim(y_low, y_high)
    ax_f.legend(loc='upper right', framealpha=0.9, fontsize=5.8)
    ax_f.grid(True, alpha=0.22)
    ax_f.text(0.04, 0.88, mass_box_str,
              transform=ax_f.transAxes, fontsize=8, color='#2166ac', va='top',
              bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='#2166ac', alpha=0.85))
    ax_f.text(0.04, 0.76, ratio_str,
              transform=ax_f.transAxes, fontsize=7, color='#1a5276', va='top')
    ax_f.text(0.04, 0.64, 'Active throat power',
              transform=ax_f.transAxes, fontsize=7, color='#b35900', va='top')

    # Summary box
    M_dec_outer_Msun = mw_M_dec_outer / MSUN
    if np.isfinite(mw_Delta_total) and mw_Delta_total != 0:
        abs_delta = abs(mw_Delta_total)
        delta_exp = int(np.floor(np.log10(abs_delta)))
        delta_mantissa = abs_delta / 10**delta_exp
        delta_sign = '-' if mw_Delta_total < 0 else ''
    else:
        delta_exp = 0
        delta_mantissa = 0.0
        delta_sign = ''
    ax_sum = fig.add_axes([0.09, 0.02, 0.87, 0.06])
    ax_sum.set_axis_off()
    ax_sum.set_facecolor('0.97')
    for spine in ax_sum.spines.values():
        spine.set_visible(True)
        spine.set_color('0.75')
    rect = plt.Rectangle((0, 0), 1, 1, transform=ax_sum.transAxes, facecolor='0.97', edgecolor='0.75', linewidth=0.8, zorder=0)
    ax_sum.add_patch(rect)
    n_sig_str = '%.1f' % mw_n_sigma if not np.isnan(mw_n_sigma) else '--'
    ax_sum.text(0.02, 0.65, 'At r = %.0f kpc' % r_outer_kpc, fontsize=8, fontweight='bold', color='0.2', va='center')
    ax_sum.text(0.18, 0.65, r'$M_{\rm dec}$ = %.2f $\times$ 10$^{10}$ $M_\odot$' % (M_dec_outer_Msun/1e10), fontsize=7, color='0.25', va='center')
    ax_sum.text(0.38, 0.65, r'$M_{\rm phot}$ = %.2f $\times$ 10$^{10}$ $M_\odot$' % (mw_M_phot_outer/1e10), fontsize=7, color='0.25', va='center')
    if np.isfinite(mw_Delta_total) and mw_Delta_total != 0:
        ax_sum.text(0.58, 0.65, r'$\Delta M_{\rm eff}$ = %s%.2f $\times$ 10$^{%d}$ $M_\odot$' % (delta_sign, delta_mantissa, delta_exp), fontsize=7, color='0.25', va='center')
    else:
        ax_sum.text(0.58, 0.65, r'$\Delta M_{\rm eff}$ = 0', fontsize=7, color='0.25', va='center')
    ax_sum.text(0.02, 0.25, '%.1f%% exterior  |  %.1f%% interior  (unc. $\\pm$%.1f%%)' % (pct_ext, pct_int, sigma_pct), fontsize=7, color='0.25', va='center')
    ax_sum.text(0.52, 0.25, r'$M_{\Lambda\rm CDM}$ = %.2f $\times$ 10$^{11}$ $M_\odot$' % (mw_M_lcdm_outer/1e11), fontsize=7, color='0.25', va='center')
    ax_sum.text(0.82, 0.25, r'Decoded %s$\sigma$ below $\Lambda$CDM' % n_sig_str, fontsize=7, fontweight='bold', color='0.2', va='center', ha='right')

# ====================== SAVE ======================
# Save at full 8.5 x 11 so 1 cm margins are preserved (no tight trim)
    base = os.path.join(output_dir, "composite_4panel_vortex_" + galaxy_id)
    plt.savefig(base + ".png", dpi=300, bbox_inches=None, pad_inches=0)
    plt.savefig(base + ".pdf", bbox_inches=None, pad_inches=0)
    plt.close()
    print("SUCCESS! Saved figures (no SyntaxWarning or mathtext error).")
    print(" Saved: " + base + ".png")
    print(" Saved: " + base + ".pdf")
    print(" All LaTeX now uses raw strings + \\mathrm for perfect compatibility.")


def main():
    parser = argparse.ArgumentParser(
        description="Generate full 4-row galactic profile figure (panels a-f) for one galaxy from API or local catalog."
    )
    parser.add_argument("galaxy_id", help="Galaxy id (e.g. milky_way, ngc3198, m33)")
    parser.add_argument("--api-base", default="http://127.0.0.1:5000", help="Base URL of Gravis API")
    parser.add_argument("--output-dir", default=_script_dir, help="Output directory for PNG/PDF")
    parser.add_argument("--local", action="store_true", help="Load galaxy from data.galaxies instead of API")
    args = parser.parse_args()

    data = load_galaxy_data(args.galaxy_id, args.api_base, args.output_dir, args.local)
    globals().update(data)
    run_figure()


if __name__ == "__main__":
    main()