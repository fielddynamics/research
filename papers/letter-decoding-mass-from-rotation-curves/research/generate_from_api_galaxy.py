"""
Generate Figure 2 only for a single galaxy: rotation curve + velocity-decoded mass.

Fetches galaxy photometric and observational data from the Gravis API, then runs
the same two-panel pipeline as in generate_letter_figures.py (Fig 2): (a) rotation
curve with observations, Newtonian, LambdaCDM if available, GFD photometric, GFD
velocity decode; (b) velocity-decoded mass vs LambdaCDM and GFD photometric.

Usage:
  python generate_fig2_galaxy.py <galaxy_id> [--api-base URL] [--output-dir DIR] [--local]

  galaxy_id   : e.g. ngc3198, milky_way, m33
  --api-base  : base URL of the app (default: http://127.0.0.1:5000)
  --output-dir: where to write fig2_<id>.png and .pdf (default: script dir)
  --local     : load galaxy from data.galaxies.get_galaxy_by_id instead of API

Requires the Gravis app running (or --local) and numpy, matplotlib, scipy.
Optional: requests (for API fetch; if missing, use --local).
"""
from __future__ import annotations

import argparse
import os
import sys

# Repo root so we can import physics and data
_script_dir = os.path.dirname(os.path.abspath(__file__))
_repo_root = os.path.abspath(os.path.join(_script_dir, "..", "..", ".."))
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy.ndimage import gaussian_filter1d

from physics.mass_model import enclosed_mass, total_mass
from physics.nfw import (
    LITERATURE_NFW_RHO0_RS,
    abundance_matching,
    fit_halo,
    m200_from_nfw_rho0_rs,
    nfw_enclosed_mass,
)

# ---------------------------------------------------------------------------
# Physical constants (SI; same as generate_letter_figures.py)
# ---------------------------------------------------------------------------
G = 6.674e-11
A0 = 1.2e-10
MSUN = 1.989e30
KPC = 3.086e19


def diffraction_smooth(r_obs, v_obs, frac=0.062):
    """Gaussian smooth velocity profile; sigma = frac * radial span."""
    r_fine = np.linspace(r_obs[0], r_obs[-1], 1000)
    v_fine = np.interp(r_fine, r_obs, v_obs)
    dr = r_fine[1] - r_fine[0]
    sigma_r = frac * (r_obs[-1] - r_obs[0])
    sigma_pts = sigma_r / dr
    v_smooth = gaussian_filter1d(v_fine, sigma=sigma_pts)
    return np.interp(r_obs, r_fine, v_smooth)


def nfw_mass(r, rho0, rs):
    """Enclosed mass for NFW profile. r, rs in m; rho0 in kg/m^3."""
    x = r / rs
    return 4 * np.pi * rho0 * rs**3 * (np.log(1 + x) - x / (1 + x))


def velocity_decode(r_obs_kpc, v_obs_km, r_fine_kpc):
    """Observed v(r) -> M_enc(r) via GFD inverse. Returns v_dec (km/s), M_dec (kg)."""
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


def forward_gfd(r_kpc, M_enc_func):
    """M_enc(r) -> v(r). Returns v_newt, v_gfd, M (kg) on r_kpc grid."""
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

    # Enclosed mass in SI: M_enc(r_m) = enclosed_mass(r_kpc, mass_model) * MSUN
    # Vectorized so it accepts arrays (forward_gfd passes r = r_kpc * KPC).
    def M_enc_func(r_m):
        r_kpc = np.atleast_1d(np.asarray(r_m, dtype=float) / KPC)
        out = np.array([enclosed_mass(float(rk), mass_model) * MSUN for rk in r_kpc.flat])
        return out.reshape(r_kpc.shape)

    return r_obs, v_obs, e_obs, M_enc_func


def main():
    parser = argparse.ArgumentParser(
        description="Generate Figure 2 (rotation curve + decoded mass) for one galaxy from API or local catalog."
    )
    parser.add_argument("galaxy_id", help="Galaxy id (e.g. ngc3198, milky_way, m33)")
    parser.add_argument(
        "--api-base",
        default="http://127.0.0.1:5000",
        help="Base URL of Gravis API (default: http://127.0.0.1:5000)",
    )
    parser.add_argument(
        "--output-dir",
        default=_script_dir,
        help="Output directory for fig2_<id>.png and .pdf",
    )
    parser.add_argument(
        "--local",
        action="store_true",
        help="Load galaxy from data.galaxies instead of API",
    )
    args = parser.parse_args()

    if args.local:
        galaxy = fetch_galaxy_local(args.galaxy_id)
    else:
        try:
            galaxy = fetch_galaxy_api(args.galaxy_id, args.api_base)
        except Exception as e:
            raise SystemExit(f"API fetch failed: {e}")

    r_obs, v_obs, e_obs, M_enc_func = build_galaxy_arrays(galaxy)
    name = galaxy.get("name") or args.galaxy_id
    # Short display name for panel titles and legend (match letter style: e.g. "NGC 3198" not "NGC 3198 (M = ...)")
    display_name = name.split(" (")[0].strip() if " (" in name else name
    # Start model grid at center (0.1 kpc) so photometric curve is shown from low M_enc
    # up to outer radius, matching the letter script (e.g. MW 0.5 kpc, M33 0.1 kpc).
    r_span = r_obs[-1] - r_obs[0]
    r_model = np.linspace(0.1, r_obs[-1] + 0.15 * r_span, 600)
    r_decode = np.linspace(r_obs[0], r_obs[-1], 500)

    v_newt, v_gfd, M = forward_gfd(r_model, M_enc_func)
    v_smooth = diffraction_smooth(r_obs, v_obs, frac=0.062)
    v_dec, M_dec = velocity_decode(r_obs, v_smooth, r_decode)

    # CDM curve: use literature NFW when available, else fit or abundance matching
    # (same logic as rotation service) so every galaxy shows LambdaCDM.
    mass_model = galaxy.get("mass_model") or {}
    observations_list = galaxy.get("observations") or []

    if args.galaxy_id in LITERATURE_NFW_RHO0_RS:
        rho0, rs = LITERATURE_NFW_RHO0_RS[args.galaxy_id]
        m200 = m200_from_nfw_rho0_rs(rho0, rs)
    else:
        m_total = total_mass(mass_model)
        def mass_at_r_kpc(r_kpc):
            return enclosed_mass(r_kpc, mass_model)
        fit = fit_halo(observations_list, mass_at_r_kpc, accel_ratio=1.0) if len(observations_list) >= 2 else None
        m200 = fit["m200"] if fit else abundance_matching(m_total)

    r_m = r_model * KPC
    M_nfw_kg = np.array([nfw_enclosed_mass(float(r), m200) for r in r_model]) * MSUN
    M_cdm = M + M_nfw_kg
    v_cdm = np.sqrt(G * M_cdm / r_m) / 1e3

    # Power output (throat): mismatch between photometric and velocity-decoded mass
    # GFD (with power output) = decoded + throat = photometric on r_decode
    M_phot_on_decode = np.interp(r_decode, r_model, M / MSUN)
    M_dec_Msun = M_dec / MSUN
    Delta_M_Msun = M_phot_on_decode - M_dec_Msun
    M_with_power_Msun = M_phot_on_decode  # = M_dec_Msun + Delta_M_Msun

    # Plot
    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 9,
        "axes.labelsize": 10,
        "legend.fontsize": 7,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "figure.dpi": 300,
        "savefig.dpi": 300,
    })

    fig = plt.figure(figsize=(4.25, 7.4))
    gs = GridSpec(2, 1, hspace=0.45, left=0.18, right=0.95, top=0.93, bottom=0.08)

    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(r_model, v_newt, "--", color="0.6", lw=1.2, label=r"Newtonian (standard $G$)")
    ax1.plot(r_model, v_cdm, ":", color="C3", lw=1.5, alpha=0.8, label=r"$\Lambda$CDM (NFW halo fit)")
    ax1.plot(r_model, v_gfd, "--", color="C2", lw=1.5, alpha=0.8, label="GFD (photometric)")
    ax1.plot(r_decode, v_dec, "-", color="C2", lw=2.0, label="GFD velocity decode (no mass input)")
    ax1.errorbar(r_obs, v_obs, yerr=e_obs, fmt="o", ms=3, color="k", ecolor="0.4",
                 elinewidth=0.7, capsize=1.5, capthick=0.7, zorder=5, label=f"{name} observations")
    ax1.set_xlabel(r"$r$ [kpc]")
    ax1.set_ylabel(r"$v$ [km s$^{-1}$]")
    r_max = r_model[-1]
    ax1.set_xlim(0, r_max)
    ax1.set_ylim(0, max(v_obs) * 1.15 if np.all(v_obs > 0) else None)
    ax1.legend(loc="lower right", framealpha=0.9, fontsize=6.5)
    ax1.text(0.0, 1.05, f"(a) {display_name}", transform=ax1.transAxes, fontweight="bold", fontsize=9)
    ax1.grid(True, alpha=0.2)

    ax2 = fig.add_subplot(gs[1, 0])
    ax2.semilogy(r_model, M_cdm / MSUN, ":", color="C3", lw=1.2, alpha=0.7, label=r"$\Lambda$CDM (baryons + NFW)")
    ax2.semilogy(r_model, M / MSUN, "--", color="C2", lw=1.2, alpha=0.8, label="GFD (photometric)")
    ax2.semilogy(r_decode, M_dec / MSUN, "-", color="C2", lw=2.0, label="GFD velocity-decoded effective mass")
    # One new series: decoded + power output (delta) = photometric in observed range
    ax2.semilogy(r_decode, M_with_power_Msun, "-", color="C0", lw=1.5, alpha=0.9, label="GFD (with power output)")
    ax2.set_xlabel(r"$r$ [kpc]")
    ax2.set_ylabel(r"$M_{\rm enc}$ [$M_\odot$]")
    ax2.set_xlim(0, r_max)
    # Use minimum of both decoded and photometric mass so the full photometric
    # curve is visible (e.g. MW starting below 10^10 at small r, matching letter figure).
    M_dec_min = np.min(M_dec / MSUN)
    M_phot_min = np.min(M / MSUN)
    M_lo = max(1e6, min(M_dec_min, M_phot_min) * 0.5)
    M_hi = max(np.max(M_dec / MSUN) * 2, np.max(M / MSUN) * 2, np.max(M_cdm / MSUN) * 1.5)
    # Extend y-axis by one decade below and above so we show at least 3 power-of-10 ticks
    # (e.g. 10^10, 10^11, 10^12) instead of a single tick; works for any scale.
    log_lo = np.log10(max(M_lo, 1e6))
    log_hi = np.log10(M_hi)
    view_lo = int(np.floor(log_lo)) - 1
    view_hi = int(np.ceil(log_hi)) + 1
    ax2.set_ylim(10**view_lo, 10**view_hi)
    ax2.legend(loc="lower right", framealpha=0.9, fontsize=6.5)
    ax2.text(0.0, 1.05, f"(b) {display_name} velocity-decoded effective mass", transform=ax2.transAxes, fontweight="bold", fontsize=9)
    ax2.grid(True, alpha=0.2, which="both")

    os.makedirs(args.output_dir, exist_ok=True)
    base = os.path.join(args.output_dir, f"fig3_{args.galaxy_id}")
    plt.savefig(f"{base}.png", dpi=300, bbox_inches="tight")
    plt.savefig(f"{base}.pdf", bbox_inches="tight")
    plt.close()

    print(f"Figure 3 saved:")
    print(f"  {base}.png")
    print(f"  {base}.pdf")


if __name__ == "__main__":
    main()
