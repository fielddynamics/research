"""
run_all_validations.py -- Standard submission process for Nelson 2026 letter.

Runs every validation required before submission: every equation (Framework),
every number stated in the letter (Demonstration, footnote, Conclusions),
and every figure and panel (Fig 1a-1d, Fig 2a-2d, Fig 3a-3b) with figure
number and panel letter. Output is organized section-by-section; use it as
the source of truth to check the letter. No automatic comparison to
letter.tex; you verify each section yourself.

Usage:
  From submission - v2:  python run_all_validations.py
  Or from repo root:    python "papers/nelson-2026/submission - v2/run_all_validations.py"

Requires: numpy. Runs figures/generate_letter_figures.py for Section 3.2 (key
  numbers). Sensitivity footnote (Section 3.3) is computed inside this script
  using the same physics and mass models; no dependent scripts needed.
"""

from __future__ import print_function

import os
import re
import subprocess
import sys

try:
    import numpy as np
except ImportError:
    print("ERROR: numpy required. Install with: pip install numpy", file=sys.stderr)
    sys.exit(1)

# Paths: this script lives in submission - v2
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FIGURES_DIR = os.path.join(SCRIPT_DIR, "figures")
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", ".."))

# Constants (letter Section 2 / Introduction)
G = 6.674e-11
A0 = 1.2e-10
MSUN = 1.989e30
KPC = 3.086e19


def nfw_mass(r, rho0, rs):
    """NFW enclosed mass. r, rs in m; rho0 in kg/m^3. Same as generate_letter_figures.py."""
    x = r / rs
    return 4 * np.pi * rho0 * rs**3 * (np.log(1 + x) - x / (1 + x))


def decoded_M_single(r_kpc, v_km):
    """Decoded effective mass at single (r, v). Letter Eq. 5. r in kpc, v in km/s; returns M in kg."""
    r = r_kpc * KPC
    v = v_km * 1e3
    gt = v**2 / r
    gs = gt**2 / (A0 + gt)
    return gs * r**2 / G


def compute_sensitivity_footnote():
    """
    Compute footnote sigmas at outermost MW and M33 radii. Uses same mass models
    and NFW parameters as figures/generate_letter_figures.py (MW: bulge+disk+gas
    from data/galaxies.py; M33: bulge+disk+gas from Corbelli00).
    Returns (sigma_mw, sigma_m33).
    """
    # MW: bulge + disk + gas (match generate_letter_figures.py / data/galaxies.py)
    MW_bulge_M = 1.5e10 * MSUN
    MW_bulge_a = 0.6 * KPC
    MW_disk_M = 4.57e10 * MSUN
    MW_disk_Rd = 2.2 * KPC
    MW_gas_M = 1.5e10 * MSUN
    MW_gas_Rd = 7.0 * KPC

    def mw_M_enc(r):
        b = MW_bulge_M * r**2 / (r + MW_bulge_a)**2
        xd = r / MW_disk_Rd
        d = MW_disk_M * (1 - (1 + xd) * np.exp(-xd))
        xg = r / MW_gas_Rd
        g = MW_gas_M * (1 - (1 + xg) * np.exp(-xg))
        return b + d + g

    mw_nfw_rho0 = 1.826e-21
    mw_nfw_rs = 9.3 * KPC

    # MW outermost: 50 kpc, v=180 km/s, +/- 32 km/s
    mw_r, mw_v, mw_err = 50.0, 180.0, 32.0
    mw_M_dec = decoded_M_single(mw_r, mw_v)
    mw_M_dec_upper = decoded_M_single(mw_r, mw_v + mw_err)
    mw_delta_M = mw_M_dec_upper - mw_M_dec
    mw_M_lcdm = mw_M_enc(mw_r * KPC) + nfw_mass(mw_r * KPC, mw_nfw_rho0, mw_nfw_rs)
    sigma_mw = (mw_M_lcdm - mw_M_dec) / mw_delta_M if mw_delta_M > 0 else float('nan')

    # M33: bulge + disk + gas (match generate_letter_figures.py)
    M33_bulge_M = 0.4e9 * MSUN
    M33_bulge_a = 0.18 * KPC
    M33_disk_M = 3.5e9 * MSUN
    M33_disk_Rd = 1.6 * KPC
    M33_gas_M = 3.2e9 * MSUN
    M33_gas_Rd = 4.0 * KPC

    def m33_M_enc(r):
        b = M33_bulge_M * r**2 / (r + M33_bulge_a)**2
        xd = r / M33_disk_Rd
        d = M33_disk_M * (1 - (1 + xd) * np.exp(-xd))
        xg = r / M33_gas_Rd
        g = M33_gas_M * (1 - (1 + xg) * np.exp(-xg))
        return b + d + g

    m33_nfw_rho0 = 2.924e-23
    m33_nfw_rs = 101.5 * KPC

    # M33 outermost: 17 kpc, v=130 km/s, +/- 8 km/s
    m33_r, m33_v, m33_err = 17.0, 130.0, 8.0
    m33_M_dec = decoded_M_single(m33_r, m33_v)
    m33_M_dec_upper = decoded_M_single(m33_r, m33_v + m33_err)
    m33_delta_M = m33_M_dec_upper - m33_M_dec
    m33_M_lcdm = m33_M_enc(m33_r * KPC) + nfw_mass(m33_r * KPC, m33_nfw_rho0, m33_nfw_rs)
    sigma_m33 = (m33_M_lcdm - m33_M_dec) / m33_delta_M if m33_delta_M > 0 else float('nan')

    return sigma_mw, sigma_m33, (
        (mw_r, mw_v, mw_err, mw_M_dec, mw_M_lcdm, mw_delta_M),
        (m33_r, m33_v, m33_err, m33_M_dec, m33_M_lcdm, m33_delta_M),
    )


def section(title, char="="):
    """Print a section header."""
    print()
    print(char * 72)
    print(title)
    print(char * 72)


def subsection(title):
    """Print a subsection header."""
    print()
    print("-" * 72)
    print(title)
    print("-" * 72)


# =============================================================================
# SECTION 1: CONSTANTS (Letter: Introduction, Framework)
# =============================================================================
def validate_constants():
    section("SECTION 1: CONSTANTS (Letter Sec 1-2)", "=")
    print("Letter states: G (CODATA), a_0 = 1.2e-10 m/s^2 (standard value, Milgrom83).")
    print()
    print("  G  = {:.3e} m^3 kg^-1 s^-2  (CODATA)".format(G))
    print("  a0 = {:.3e} m/s^2".format(A0))
    print()
    print("CHECK: Letter Introduction and Framework use these values only.")


# =============================================================================
# SECTION 2: FRAMEWORK EQUATIONS (Letter Section 2)
# =============================================================================
def validate_equations():
    section("SECTION 2: FRAMEWORK EQUATIONS (Letter Section 2)", "=")

    # Eq. Poisson: g_s = G*M/r^2 (spherical). Spot check: M and r -> g_s
    subsection("Eq. Poisson (letter Eq. 1) and g_s = G*M/r^2")
    r_m = 25.0 * KPC
    M_kg = 7.0e10 * MSUN
    gs = G * M_kg / r_m**2
    print("  Test: r = 25 kpc, M = 7e10 M_sun -> g_s = G*M/r^2 = {:.3e} m/s^2".format(gs))
    print("  CHECK: Letter Eq. 1 (Poisson) and text use this relation.")

    # Eq. transition: g_s = g_t^2/(a0 + g_t) and g_t = (g_s + sqrt(g_s^2+4*g_s*a0))/2
    subsection("Eq. Transition (letter Eq. 3-4)")
    gs_test = 1e-10
    gt_forward = (gs_test + np.sqrt(gs_test**2 + 4 * gs_test * A0)) / 2.0
    gs_inverse = gt_forward**2 / (A0 + gt_forward)
    print("  Forward:  g_s = {:.3e} -> g_t = {:.3e}".format(gs_test, gt_forward))
    print("  Inverse:  g_t -> g_s = {:.3e}  (should match g_s)".format(gs_inverse))
    print("  CHECK: Letter Eq. 3-4 (transition) and inverse g_s = g_t^2/(a0+g_t).")

    # Eq. 5: M_dec(r) = r*v^4 / (G*(a0*r + v^2))
    subsection("Eq. 5 M_dec (letter Eq. 5)")
    r_kpc, v_km = 25.0, 200.0
    r_m = r_kpc * KPC
    v_ms = v_km * 1e3
    gt = v_ms**2 / r_m
    gs = gt**2 / (A0 + gt)
    M_dec_kg = gs * r_m**2 / G
    M_dec_msun = M_dec_kg / MSUN
    # Closed form: M_dec = r*v^4/(G*(a0*r+v^2))
    v_si = v_km * 1e3
    r_si = r_kpc * KPC
    M_closed = (r_si * v_si**4) / (G * (A0 * r_si + v_si**2))
    print("  At r = {} kpc, v = {} km/s:".format(r_kpc, v_km))
    print("    M_dec (from g_t -> g_s -> M) = {:.3e} M_sun".format(M_dec_kg / MSUN))
    print("    M_dec (closed form r*v^4/(G*(a0*r+v^2))) = {:.3e} M_sun".format(M_closed / MSUN))
    print("  CHECK: Letter Eq. 5 and Conclusions display this formula.")


# =============================================================================
# SECTION 3: DEMONSTRATION (Letter Section 3) -- numbers and footnote
# =============================================================================
def run_figure_script():
    """Run generate_letter_figures.py and return stdout. Figures written to figures/."""
    cwd = FIGURES_DIR
    script = os.path.join(cwd, "generate_letter_figures.py")
    if not os.path.isfile(script):
        return None, "Script not found: " + script
    try:
        out = subprocess.check_output(
            [sys.executable, script],
            cwd=cwd,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            timeout=120,
        )
        return out, None
    except subprocess.CalledProcessError as e:
        return e.output if e.output else "", "Exit code " + str(e.returncode)
    except Exception as e:
        return "", str(e)


def validate_demonstration():
    section("SECTION 3: DEMONSTRATION (Letter Section 3)", "=")

    subsection("3.1 Mass models and parameters (letter text)")
    print("  MW: bulge + disk + gas (data/galaxies.py), total baryonic ~7.6e10 M_sun (McMillan17, etc.).")
    print("  M33: bulge, disk, gas; total baryonic ~7e9 M_sun (Corbelli00).")
    print("  Smoothing: Gaussian 6.2% of radial span.")
    print("  CHECK: Letter Demonstration 'Forward' paragraph.")

    subsection("3.2 Key numbers at reference radii (from generate_letter_figures.py)")
    fig_out, err = run_figure_script()
    dec_25 = phot_25 = cdm_25 = None
    sigma_mw = sigma_m33 = None
    if err:
        print("  WARNING: Could not run figure script:", err)
        print("  Run manually: cd figures && python generate_letter_figures.py")
    else:
        dec_17 = cdm_17 = None
        for line in fig_out.splitlines():
            if "Decoded effective mass at 25 kpc" in line or "Photometric enclosed mass at 25" in line or "CDM enclosed mass at 25" in line:
                print("  MW 25 kpc:", line.strip())
                m = re.search(r"([\d.]+e[+-]?\d+)", line)
                if m:
                    val = float(m.group(1))
                    if "Decoded" in line:
                        dec_25 = val
                    elif "Photometric" in line:
                        phot_25 = val
                    elif "CDM" in line:
                        cdm_25 = val
            if "Decoded effective mass at 17 kpc" in line:
                print("  M33 17 kpc:", line.strip())
                m = re.search(r"([\d.]+e[+-]?\d+)", line)
                if m:
                    dec_17 = float(m.group(1))
            if "Photometric enclosed mass at 17" in line or "CDM enclosed mass at 17" in line:
                print("  M33 17 kpc:", line.strip())
                if "CDM" in line:
                    m = re.search(r"([\d.]+e[+-]?\d+)", line)
                    if m:
                        cdm_17 = float(m.group(1))
            if "Decoded effective mass at 30 kpc" in line or "Photometric enclosed mass at 30" in line or "CDM enclosed mass at 30" in line:
                print("  NGC 3198 30 kpc:", line.strip())
        print()
        print("  Letter should show (use values above):")
        print("    M33 at 17 kpc: decoded 1.38e10 M_sun; LambdaCDM total 7.2e10 M_sun; '5.2 times smaller'.")
        if dec_17 and cdm_17 and dec_17 > 0:
            print("    Ratio LambdaCDM/decoded at 17 kpc = {:.2f} (letter '5.2 times smaller')".format(cdm_17 / dec_17))
        if dec_25 is not None and phot_25 is not None and cdm_25 is not None:
            print("    MW at 25 kpc: decoded ~{:.2e} M_sun; photometric ~{:.2e} M_sun; LambdaCDM ~{:.2e} M_sun.".format(dec_25, phot_25, cdm_25))
        else:
            print("    MW at 25 kpc: decoded ~6.6e10 M_sun; photometric and LambdaCDM from figure output above.")
        print("  CHECK: Letter 'Mass comparison' paragraph.")

    subsection("3.3 Footnote 1 (sensitivity at outermost radii, computed here)")
    sigma_mw, sigma_m33, details = compute_sensitivity_footnote()
    mw_vals, m33_vals = details
    mw_r, mw_v, mw_err, mw_M_dec, mw_M_lcdm, mw_delta_M = mw_vals
    m33_r, m33_v, m33_err, m33_M_dec, m33_M_lcdm, m33_delta_M = m33_vals
    print("  MW  r={} kpc: decoded {:.3e} M_sun, LambdaCDM {:.3e} M_sun; +{} km/s -> 1-sigma {:.3e} M_sun; remains {:.1f} sigma below LambdaCDM.".format(
        mw_r, mw_M_dec/MSUN, mw_M_lcdm/MSUN, mw_err, mw_delta_M/MSUN, sigma_mw))
    print("  M33 r={} kpc: decoded {:.3e} M_sun, LambdaCDM {:.3e} M_sun; +{} km/s -> 1-sigma {:.3e} M_sun; remains {:.1f} sigma below LambdaCDM.".format(
        m33_r, m33_M_dec/MSUN, m33_M_lcdm/MSUN, m33_err, m33_delta_M/MSUN, sigma_m33))
    print()
    print("  Letter footnote should read: ... remains ${:.1f}\\sigma$ (MW, $\\pm$32~km/s) and ${:.1f}\\sigma$ (M33, $\\pm$8~km/s) below the LambdaCDM enclosed mass.".format(sigma_mw, sigma_m33))
    print("  CHECK: Letter footnote 1.")


# =============================================================================
# SECTION 4: FIGURES (Letter Figs 1, 2, 3 -- each panel)
# =============================================================================
def validate_figures():
    section("SECTION 4: FIGURES (Letter Figs 1, 2, 3)", "=")
    print("Source for all: figures/generate_letter_figures.py")
    print()

    fig_files = [
        ("fig1_mw_m33", "Figure 1", "Milky Way + M33"),
        ("fig2_camb", "Figure 2", "CamB"),
        ("fig3_ngc3198", "Figure 3", "NGC 3198"),
    ]
    for base, fig_label, name in fig_files:
        for ext in (".png", ".pdf"):
            path = os.path.join(FIGURES_DIR, base + ext)
            exists = os.path.isfile(path)
            print("  {} {} {}: {}".format(fig_label, base + ext, name, "OK" if exists else "MISSING"))

    subsection("Figure 1 (fig1_mw_m33) -- Four-panel")
    print("  Fig 1a: Milky Way rotation curve. Observations, Newtonian, LambdaCDM NFW, GFD photometric, GFD velocity-decoded.")
    print("  Fig 1b: MW mass. LambdaCDM baryons+NFW, GFD photometric, GFD velocity-decoded effective mass.")
    print("  Fig 1c: M33 rotation curve. Same convention as (a).")
    print("  Fig 1d: M33 mass. Same as (b).")
    print("  CHECK: Letter Fig 1 caption and panels (a)-(d).")

    subsection("Figure 2 (fig2_camb) -- Four-panel")
    print("  Fig 2a: CamB rotation curve. Observations, Newtonian, LambdaCDM NFW, GFD photometric, GFD velocity decode.")
    print("  Fig 2b: CamB mass. LambdaCDM, GFD photometric, velocity-decoded effective mass; shaded Delta M_eff (interior contribution).")
    print("  Fig 2c: Mass ratio M_phot/M_dec over observed range.")
    print("  Fig 2d: Decoded mass + Delta M_eff(r) matches photometric; shaded = power output from topology.")
    print("  CHECK: Letter Fig 2 caption and panels (a)-(d).")

    subsection("Figure 3 (fig3_ngc3198) -- Two-panel")
    print("  Fig 3a: NGC 3198 rotation curve. Same convention as Fig 1(a).")
    print("  Fig 3b: NGC 3198 velocity-decoded effective mass with LambdaCDM and GFD photometric.")
    print("  CHECK: Letter Fig 3 caption and panels (a)-(b).")


# =============================================================================
# SECTION 5: DISCUSSION AND CONCLUSIONS (Letter Sections 4-5)
# =============================================================================
def validate_discussion_conclusions():
    section("SECTION 5: DISCUSSION AND CONCLUSIONS (Letter Sections 4-5)", "=")
    subsection("Discussion")
    print("  Delta M_eff(r) = M_phot(r) - M_dec(r). M_dec from Eq. 5.")
    print("  CHECK: Letter Discussion and Fig 2 caption use this definition.")
    subsection("Conclusions")
    print("  Same Eq. 5, G, a_0 for all three galaxies; zero free parameters.")
    print("  SPARC: 175 disk galaxies (Lelli16).")
    print("  CHECK: Letter Conclusions and Fig 3 caption.")


# =============================================================================
# SECTION 6: DATA AND CODE (Letter Section 6)
# =============================================================================
def validate_data_code():
    section("SECTION 6: DATA AND CODE AVAILABILITY (Letter Section 6)", "=")
    print("  Code: generate_letter_figures.py (in figures/).")
    print("  Data: McMillan17 (MW), Corbelli00 (M33), Begeman91 (NGC 3198), Lelli16 (CamB).")
    path = os.path.join(FIGURES_DIR, "generate_letter_figures.py")
    print("  File exists:", os.path.isfile(path))
    print("  CHECK: Letter Data and Code section and filename with underscore.")


# =============================================================================
# MAIN
# =============================================================================
def main():
    print("Nelson 2026 Letter -- Run All Validations")
    print("Output values below are the source of truth; check letter.tex against them.")
    validate_constants()
    validate_equations()
    validate_demonstration()
    validate_figures()
    validate_discussion_conclusions()
    validate_data_code()
    section("END OF VALIDATIONS", "=")
    print()
    print("Run build_letter.bat --all to regenerate figures and build letter.pdf.")


if __name__ == "__main__":
    main()
