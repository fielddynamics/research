"""
GFD prediction for wide binary stars in the solar neighbourhood, from the covariant action's field equation.

Inputs (none fitted):
  a0  = 1.2e-10 m/s^2                       (the archive's acceleration scale)
  g_e = v_c^2 / R0, v_c = 229.0 km/s, R0 = 8.122 kpc   (Eilers et al. 2019)  ->  1.744 a0
        bracketed by 1.6 a0 and 1.9 a0 to show the sensitivity
  M   = 1.0, 1.5, 2.0 solar masses          (typical total binary masses)

Outputs:
  gamma(s): orientation-averaged internal gravity at separation s, relative to Newton
  R:        the pre-registered statistic, median v_tilde for projected separations 10-30 kau
            divided by median v_tilde for 1-2 kau, where v_tilde = v_p / sqrt(G M / s_p)

Run: python wide_binary_prediction.py      (about 2 minutes)
"""
import numpy as np
from gfd_field_solver import Solver

GM_SUN, AU, A0 = 1.32712440018e20, 1.495978707e11, 1.2e-10
KM, KPC = 1e3, 3.0856775814913673e19
G_E = (229.0 * KM) ** 2 / (8.122 * KPC) / A0                   # = 1.744
SEPS = [1, 2, 3, 5, 7, 10, 15, 20, 30]                          # kau
DEPROJECT = 4 / np.pi                                           # mean 3D / projected separation, isotropic orbits


def curve(g_e):
    S = Solver(g_e=g_e, NR=240, NZ=481); S.iterate()
    ss = np.geomspace(0.02, 40, 140)
    return ss, np.array([S.internal_radial(s)[0] * s * s for s in ss])


def gamma_at(s_kau, M, ss, gam):
    rM = np.sqrt(M * GM_SUN / A0) / AU / 1e3
    return np.interp(np.log(np.asarray(s_kau) / rM), np.log(ss), gam)


def R_statistic(M, ss, gam):
    """sqrt of the ratio of mean gamma over log-uniform projected separations in the two bins."""
    lo = np.geomspace(1, 2, 200) * DEPROJECT; hi = np.geomspace(10, 30, 200) * DEPROJECT
    return np.sqrt(gamma_at(hi, M, ss, gam).mean() / gamma_at(lo, M, ss, gam).mean())


if __name__ == "__main__":
    print(f"external field g_e = {G_E:.3f} a0 = {G_E * A0:.3e} m/s^2\n")
    curves = {ge: curve(ge) for ge in (1.6, G_E, 1.9)}
    ss, gam = curves[G_E]
    print("gravity boost gamma(s) = g / g_Newton, at the measured external field")
    print(f"{'M (Msun)':>9} " + " ".join(f"{s:>6}" for s in SEPS) + "   (kau)")
    for M in (1.0, 1.5, 2.0):
        print(f"{M:9.1f} " + " ".join(f"{g:6.3f}" for g in gamma_at(SEPS, M, ss, gam)))
    print("\nvelocity boost sqrt(gamma), M = 1.5 Msun:")
    print(f"{'':9s} " + " ".join(f"{np.sqrt(g):6.3f}" for g in gamma_at(SEPS, 1.5, ss, gam)))
    print(f"\nplateau (s >= 20 kau): gamma = {gamma_at(30, 1.5, ss, gam):.3f}, velocity boost = {np.sqrt(gamma_at(30, 1.5, ss, gam)):.3f}")
    print("\npre-registered statistic R = median v_tilde (s_p 10-30 kau) / median v_tilde (s_p 1-2 kau)")
    Rs = {(ge, M): R_statistic(M, *curves[ge]) for ge in curves for M in (1.0, 1.5, 2.0)}
    for (ge, M), R in Rs.items():
        print(f"  g_e = {ge:.3f} a0, M = {M:.1f}:  R = {R:.3f}")
    print(f"\n  central (g_e = {G_E:.3f} a0, M = 1.5):  R = {Rs[(G_E, 1.5)]:.3f}")
    print(f"  range over g_e 1.6-1.9 a0, M 1-2 Msun:  {min(Rs.values()):.3f} - {max(Rs.values()):.3f}")
    print("  Newtonian gravity:  R = 1.000")
