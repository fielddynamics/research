"""
Siloed M33: SST+Poisson with power output from data (same as charts b, d).

  M_dec(r) = velocity decode (inverse SST) of v_obs
  M_phot(r) = baryonic enclosed mass from mass model (smooth).
  Delta_M_eff(r) = M_phot(r) - M_dec(r)   [point-wise, charts b/d]

Curves:
  (1) Exterior only: v from M_phot (garden hose, no vortex). Smooth.
  (2) Velocity match: v from M_dec; forward SST(M_dec) = v_obs (can be wobbly).
  (3) Smooth vortex: v from M_phot + P(r), where P(r) is a SMOOTH power-output
      profile (throttle). We FIT P(r) so this velocity curve matches v_obs while
      staying as smooth as the photometric curve (continuous throat to horizon).

Smooth P(r): e.g. P(r) = P0 * (1 - exp(-r/r_scale)) in M_sun (enclosed mass add).
Fit P0, r_scale to minimize RMS(v_obs, forward_SST(M_phot + P)).

No unicode (Windows charmap).
"""
from __future__ import annotations

import math
import numpy as np
from scipy.optimize import minimize
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Constants (SI; match physics.constants / letter script)
# ---------------------------------------------------------------------------
G = 6.67430e-11
MSUN = 1.98892e30
KPC = 3.0857e19
A0 = 1.2e-10
COUPLING_RATIO = 17.0 / 13.0

# ---------------------------------------------------------------------------
# M33 data (from data.galaxies PREDICTION_GALAXIES, id="m33")
# ---------------------------------------------------------------------------
M33 = {
    "id": "m33",
    "name": "M33 Triangulum (M = 7.1x10^9 M_sun, 45% gas)",
    "distance": 20,
    "galactic_radius": 17,
    "mass": 9.851,
    "accel": 1.0,
    "mass_model": {
        "bulge": {"M": 0.4e9, "a": 0.18},
        "disk":  {"M": 3.5e9, "Rd": 1.6},
        "gas":   {"M": 3.2e9, "Rd": 4.0},
    },
    "observations": [
        {"r": 0.5, "v": 30,  "err": 5},
        {"r": 1,   "v": 38,  "err": 8},
        {"r": 1.5, "v": 55,  "err": 7},
        {"r": 2,   "v": 68,  "err": 8},
        {"r": 3,   "v": 88,  "err": 6},
        {"r": 4,   "v": 100, "err": 7},
        {"r": 5,   "v": 105, "err": 5},
        {"r": 6,   "v": 108, "err": 6},
        {"r": 7,   "v": 108, "err": 5},
        {"r": 8,   "v": 108, "err": 6},
        {"r": 9,   "v": 110, "err": 6},
        {"r": 10,  "v": 115, "err": 7},
        {"r": 11,  "v": 117, "err": 6},
        {"r": 12,  "v": 120, "err": 7},
        {"r": 14,  "v": 125, "err": 7},
        {"r": 15,  "v": 128, "err": 8},
        {"r": 17,  "v": 130, "err": 8},
    ],
}

# ---------------------------------------------------------------------------
# Enclosed mass from mass model (Hernquist bulge + exponential disks)
# ---------------------------------------------------------------------------
def enclosed_mass_baryonic(r_kpc, mass_model):
    if r_kpc <= 0:
        return 0.0
    r = r_kpc
    m = 0.0
    bulge = mass_model.get("bulge")
    if bulge and bulge.get("M", 0) > 0:
        a = bulge["a"]
        m += bulge["M"] * r * r / ((r + a) * (r + a))
    disk = mass_model.get("disk")
    if disk and disk.get("M", 0) > 0:
        x = r / disk["Rd"]
        m += disk["M"] * (1.0 - (1.0 + x) * math.exp(-x))
    gas = mass_model.get("gas")
    if gas and gas.get("M", 0) > 0:
        x = r / gas["Rd"]
        m += gas["M"] * (1.0 - (1.0 + x) * math.exp(-x))
    return m


# ---------------------------------------------------------------------------
# SST + Poisson: mass -> velocity (km/s)
# g_source = (17/13)*G*M/r^2, g_total = sqrt(g_source*a0 + g_source^2), v = sqrt(r*g_total)
# ---------------------------------------------------------------------------
def g_source_from_mass(r_m, M_kg):
    if r_m <= 0:
        return 0.0
    return COUPLING_RATIO * G * M_kg / (r_m * r_m)


def g_total_from_g_source(g_source, a0_eff):
    if g_source <= 0:
        return 0.0
    return math.sqrt(g_source * a0_eff + g_source * g_source)


def velocity_sst_km_s(r_kpc, M_enc_solar, a0_eff=A0):
    """Circular velocity (km/s) at r_kpc for enclosed mass M_enc_solar (solar masses)."""
    if r_kpc <= 0 or M_enc_solar <= 0:
        return 0.0
    r_m = r_kpc * KPC
    M_kg = M_enc_solar * MSUN
    g_s = g_source_from_mass(r_m, M_kg)
    g_t = g_total_from_g_source(g_s, a0_eff)
    v_m_s = math.sqrt(r_m * g_t)
    return v_m_s / 1000.0


# ---------------------------------------------------------------------------
# Inverse SST: velocity -> M_enc (velocity decode, same as charts b/d)
# g_total = v^2/r, g_source = (-a0 + sqrt(a0^2+4*g_total^2))/2, M = g_source*r^2/((17/13)*G)
# ---------------------------------------------------------------------------
def g_total_from_velocity(v_km_s, r_kpc):
    if r_kpc <= 0 or v_km_s <= 0:
        return 0.0
    r_m = r_kpc * KPC
    v_m_s = v_km_s * 1000.0
    return (v_m_s * v_m_s) / r_m


def g_source_from_g_total(g_total, a0_eff):
    if g_total <= 0:
        return 0.0
    disc = a0_eff * a0_eff + 4.0 * g_total * g_total
    if disc <= 0:
        return 0.0
    return (-a0_eff + math.sqrt(disc)) / 2.0


def M_enc_from_velocity_solar(v_km_s, r_kpc, a0_eff=A0):
    """Enclosed mass (solar masses) from observed velocity at r (inverse SST+Poisson)."""
    if r_kpc <= 0 or v_km_s <= 0:
        return 0.0
    g_total = g_total_from_velocity(v_km_s, r_kpc)
    g_source = g_source_from_g_total(g_total, a0_eff)
    r_m = r_kpc * KPC
    M_kg = g_source * r_m * r_m / (COUPLING_RATIO * G)
    return M_kg / MSUN


# ---------------------------------------------------------------------------
# Smooth power output (throttle): P(r) = P0 * (1 - exp(-r/r_scale))  [M_sun enclosed]
# Same smooth shape as photometric: continuous from throat to horizon.
# ---------------------------------------------------------------------------
def smooth_power_enclosed_M_sun(r_kpc, P0, r_scale_kpc):
    """Enclosed mass (M_sun) from smooth power profile. r_scale must be > 0."""
    if r_kpc <= 0 or r_scale_kpc <= 0:
        return 0.0
    return P0 * (1.0 - math.exp(-r_kpc / r_scale_kpc))


def main():
    mass_model = M33["mass_model"]
    obs = M33["observations"]
    r_obs = np.array([o["r"] for o in obs])
    v_obs = np.array([o["v"] for o in obs])
    a0_eff = A0 * float(M33.get("accel", 1.0))

    # Fine grid over observed range
    r_fine = np.linspace(max(0.1, r_obs.min()), r_obs.max() + 1, 400)
    v_interp = np.interp(r_fine, r_obs, v_obs)

    # M_dec(r) = velocity decode (inverse SST) at each r
    M_dec_fine = np.array([M_enc_from_velocity_solar(float(v), float(r), a0_eff) for r, v in zip(r_fine, v_interp)])
    M_phot_fine = np.array([enclosed_mass_baryonic(r, mass_model) for r in r_fine])

    # Forward: (1) v from M_phot only (exterior / garden hose), (2) v from M_dec (velocity match)
    v_from_M_phot = np.array([velocity_sst_km_s(r, M, a0_eff) for r, M in zip(r_fine, M_phot_fine)])
    v_from_M_dec = np.array([velocity_sst_km_s(r, M, a0_eff) for r, M in zip(r_fine, M_dec_fine)])

    # (3) Smooth vortex: fit P(r) = P0*(1 - exp(-r/r_scale)) so v from (M_phot + P) matches v_obs, curve stays smooth
    def rms_smooth(params):
        P0, r_scale = params[0], max(params[1], 0.1)
        v_model = np.array([
            velocity_sst_km_s(r, enclosed_mass_baryonic(r, mass_model) + smooth_power_enclosed_M_sun(r, P0, r_scale), a0_eff)
            for r in r_obs
        ])
        return np.sqrt(np.mean((v_obs - v_model) ** 2))

    # Initial guess: add mass in outskirts to lift curve; P0 ~ few e9 M_sun, r_scale ~ 5 kpc
    res = minimize(rms_smooth, x0=[2e9, 5.0], method="L-BFGS-B", bounds=[(-1e11, 1e11), (0.2, 30.0)])
    P0_opt, r_scale_opt = res.x[0], max(res.x[1], 0.1)
    rms_smooth_val = float(res.fun)

    M_phot_plus_smooth_power = np.array([
        enclosed_mass_baryonic(r, mass_model) + smooth_power_enclosed_M_sun(r, P0_opt, r_scale_opt)
        for r in r_fine
    ])
    v_smooth_vortex = np.array([velocity_sst_km_s(r, M, a0_eff) for r, M in zip(r_fine, M_phot_plus_smooth_power)])

    # RMS at obs radii
    v_dec_at_obs = np.interp(r_obs, r_fine, v_from_M_dec)
    rms_match = float(np.sqrt(np.mean((v_obs - v_dec_at_obs) ** 2)))
    v_phot_at_obs = np.interp(r_obs, r_fine, v_from_M_phot)
    rms_phot_only = float(np.sqrt(np.mean((v_obs - v_phot_at_obs) ** 2)))

    print("M33 SST+Poisson: power output from data (same as charts b, d)")
    print("  Delta_M_eff(r) = M_phot(r) - M_dec(r); total mass = M_dec gives exact velocity match.")
    print("  Exterior only (v from M_phot): RMS = {:.3f} km/s".format(rms_phot_only))
    print("  M_dec (velocity match): RMS = {:.3f} km/s".format(rms_match))
    print("  Smooth vortex (M_phot + P(r), P(r)=P0*(1-exp(-r/r_s))): P0 = {:.3e}, r_scale = {:.2f} kpc, RMS = {:.3f} km/s".format(
        P0_opt, r_scale_opt, rms_smooth_val))
    r_outer = r_obs[-1]
    M_dec_outer = np.interp(r_outer, r_fine, M_dec_fine)
    M_phot_outer = enclosed_mass_baryonic(r_outer, mass_model)
    Delta_outer = M_phot_outer - M_dec_outer
    print("  At r = {:.1f} kpc: M_dec = {:.3e}, M_phot = {:.3e}, Delta_M_eff = {:.3e} M_sun".format(
        r_outer, M_dec_outer, M_phot_outer, Delta_outer))

    # Plot: observations; smooth photometric (green); smooth vortex = M_phot + P(r) (black); M_dec match (blue)
    e_obs = np.array([o.get("err", 0) for o in obs])
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(r_fine, v_smooth_vortex, "-", color="k", lw=2.5,
            label="M_phot + smooth power (vortex throttle); RMS = {:.2f} km/s".format(rms_smooth_val))
    ax.plot(r_fine, v_from_M_phot, "--", color="C2", lw=1.5, label="Exterior only (v from M_phot); RMS = {:.2f} km/s".format(rms_phot_only))
    ax.plot(r_fine, v_from_M_dec, "-", color="C0", lw=1.5, label="M_dec (velocity match); RMS = {:.2f} km/s".format(rms_match))
    ax.errorbar(r_obs, v_obs, yerr=e_obs, fmt="o", ms=4, color="k", ecolor="0.4", capsize=2, capthick=1, label="M33 observations")
    ax.set_xlabel(r"$r$ [kpc]")
    ax.set_ylabel(r"$v$ [km s$^{-1}$]")
    ax.set_title("M33: Smooth vortex (M_phot + P(r)) fits v_obs; same smoothness as photometric")
    ax.legend(loc="lower right", fontsize=8)
    ax.set_xlim(0, r_fine[-1])
    y_max = max(v_obs.max() * 1.15, np.nanmax(v_from_M_dec) * 1.05, np.nanmax(v_smooth_vortex) * 1.05) if np.any(np.isfinite(v_from_M_dec)) else 150
    ax.set_ylim(0, y_max)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    out_png = "m33_sst_fit.png"
    out_pdf = "m33_sst_fit.pdf"
    fig.savefig(out_png, dpi=150)
    fig.savefig(out_pdf)
    plt.close(fig)
    print("  Saved: {}  {}".format(out_png, out_pdf))


if __name__ == "__main__":
    main()
