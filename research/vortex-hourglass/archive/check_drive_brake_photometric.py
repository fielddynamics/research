"""
Drive / brake per galaxy, decoded as in the decoding-mass letter, against the ring.

Method (letter-decoding-mass-from-rotation-curves):
  M_dec(r)  = r v^4 / [G (a0 r + v^2)]                     velocity decode, no mass model
  M_phot(r) = enclosed photometric baryonic mass             SPARC surface photometry
  Drive: M_dec > M_phot (stars faster than the visible matter explains).
  Brake: M_dec < M_phot.  Quiet: within a factor of order unity.
  (Drive/brake as in EINSTEIN_TETA_PARTITION.md; Delta M_eff = M_phot - M_dec is
  negative for a drive and positive for a brake.)

M_phot(r): stars = Upsilon x integral of 2 pi R SB(R) dR over SPARC's SBdisk (0.5) and
SBbul (0.7, projected) profiles, constant SB inside the first point; gas = 1.33 x HI as
|Vgas| Vgas r / G (spherical estimate; SPARC gives no gas surface density profile).

Hypothesis H2' (H2 re-run with the letter's decode, fixed before running):
  the share of the galaxy inside the ring (x = g_obs/a0 = 1) correlates positively with
  drive, log10(M_dec/M_phot) at the outermost point; pass at one-sided p < 0.01,
  in all galaxies and in galaxies without bulges.

Usage: python check_drive_brake_photometric.py ROTMOD_DIR TABLE1_PATH
"""
from __future__ import annotations

import glob
import os
import sys

import numpy as np

G = 6.674e-11
A0 = 1.2e-10
KPC = 3.0857e19
MSUN = 1.989e30
UPS_D, UPS_B = 0.5, 0.7
rng = np.random.default_rng(2026)


def enclosed_light(R_kpc, SB):
    """Cumulative luminosity (L_sun) within each R from a surface-brightness profile (L_sun/pc^2)."""
    Rpc = R_kpc * 1e3
    L = np.empty_like(Rpc)
    L[0] = np.pi * Rpc[0] ** 2 * SB[0]
    f = 2 * np.pi * Rpc * SB
    L[1:] = L[0] + np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(Rpc))
    return L


def crossing(R, f):
    for i in range(len(R) - 1):
        if f[i] > 0 >= f[i + 1]:
            t = f[i] / (f[i] - f[i + 1])
            return float(np.exp(np.log(R[i]) + t * (np.log(R[i + 1]) - np.log(R[i]))))
    return None


def spearman(a, b, n_perm=20000):
    from scipy.stats import rankdata
    ra, rb = rankdata(a), rankdata(b)  # average ranks for ties
    rho = np.corrcoef(ra, rb)[0, 1]
    perm = np.array([np.corrcoef(ra, rng.permutation(rb))[0, 1] for _ in range(n_perm)])
    return rho, (np.sum(perm >= rho) + 1) / (n_perm + 1)


def main(rotmod_dir, table1):
    T = {}
    for line in open(table1):
        p = line.split()
        if len(p) > 17:
            T[p[0]] = dict(inc=float(p[5]), L36=float(p[7]) * 1e9, Q=int(p[17]))
    rows, lum_check = [], []
    for f in sorted(glob.glob(os.path.join(rotmod_dir, "*_rotmod.dat"))):
        name = os.path.basename(f)[:-len("_rotmod.dat")]
        m = T.get(name)
        d = np.loadtxt(f, comments="#", ndmin=2)
        R, Vo, Vg, SBd, SBb = d[:, 0], d[:, 1], d[:, 3], d[:, 6], d[:, 7]
        Lstar = enclosed_light(R, SBd) + enclosed_light(R, SBb)
        if m:
            lum_check.append(np.log10(Lstar[-1] / m["L36"]))
        if not m or m["Q"] > 2 or m["inc"] < 30 or len(R) < 5:
            continue
        r = R * KPC
        Mstar = (UPS_D * enclosed_light(R, SBd) + UPS_B * enclosed_light(R, SBb)) * MSUN
        Mgas = np.abs(Vg) * Vg * 1e6 * r / G
        Mphot = Mstar + Mgas
        v = Vo * 1e3
        Mdec = r * v ** 4 / (G * (A0 * r + v ** 2))
        if Mphot[-1] <= 0:
            continue
        drive = np.log10(Mdec[-1] / Mphot[-1])
        gobs = v ** 2 / r
        Rring = crossing(R, np.log(gobs / A0))
        if Rring is None:
            fin = 1.0 if gobs[-1] > A0 else 0.0
        else:
            fin = float(np.clip(np.interp(Rring, R, Mphot) / Mphot[-1], 0, 1))
        rows.append((name, drive, fin, bool(np.any(SBb > 0)), float(Mgas[-1] / Mphot[-1])))

    lum_check = np.array(lum_check)
    print(f"Photometry check: integrated 3.6um light / SPARC L[3.6], {len(lum_check)} galaxies: "
          f"median {np.median(lum_check):+.3f} dex, 16-84% [{np.percentile(lum_check, 16):+.3f}, "
          f"{np.percentile(lum_check, 84):+.3f}]\n")

    drive = np.array([r[1] for r in rows]); fin = np.array([r[2] for r in rows])
    hasb = np.array([r[3] for r in rows])
    print(f"Galaxies: {len(rows)} (Q <= 2, inc >= 30 deg, >= 5 points)")
    print(f"log10(M_dec/M_phot) at the last point: median {np.median(drive):+.3f}, "
          f"16-84% [{np.percentile(drive, 16):+.2f}, {np.percentile(drive, 84):+.2f}]")
    for lab, s in [("drive  (M_dec > 2 M_phot)", drive > np.log10(2)),
                   ("quiet  (within a factor 2)", np.abs(drive) <= np.log10(2)),
                   ("brake  (M_dec < M_phot / 2)", drive < -np.log10(2))]:
        print(f"  {lab:30s} {s.sum():3d}  ({s.mean():.0%})")
    print()
    for lab, sel in [("all", np.ones_like(hasb)), ("no bulge", ~hasb), ("with bulge", hasb)]:
        rho, p = spearman(fin[sel], drive[sel])
        print(f"  {lab:10s} N = {sel.sum():3d}  Spearman rho(f_in, drive) = {rho:+.2f}  one-sided p = {p:.4f}")
    rho_a, p_a = spearman(fin, drive); rho_n, p_n = spearman(fin[~hasb], drive[~hasb])
    print(f"  H2': {'PASS' if (rho_a > 0 and p_a < 0.01 and rho_n > 0 and p_n < 0.01) else 'FAIL'}")
    fgas = np.array([r[4] for r in rows])
    print("\n  Robustness to the gas estimate (gas share of M_phot at the last point):")
    for lab, sel in [("gas share < 0.3", fgas < 0.3), ("gas share < 0.5", fgas < 0.5), ("gas share >= 0.5", fgas >= 0.5)]:
        if sel.sum() >= 8:
            rho, p = spearman(fin[sel], drive[sel])
            out = sel & (fin == 0)
            print(f"    {lab:18s} N = {sel.sum():3d}  rho = {rho:+.2f}  p = {p:.4f}   all-outside: N = {out.sum():3d}, "
                  f"brakes {np.mean(drive[out] < -np.log10(2)) if out.sum() else float('nan'):.0%}")
    rho_g, p_g = spearman(fgas, -drive)
    print(f"    gas share versus brake: rho = {rho_g:+.2f}, p = {p_g:.4f}")
    print()
    for lab, s in [("no ring in data, all outside (f_in = 0)", fin == 0),
                   ("ring inside the data, 0 < f_in < 1", (fin > 0) & (fin < 1)),
                   ("all inside the ring (f_in = 1)", fin == 1)]:
        if s.sum():
            print(f"    {lab:42s} N = {s.sum():3d}, median drive {np.median(drive[s]):+.3f}, "
                  f"drives {np.mean(drive[s] > np.log10(2)):.0%}, brakes {np.mean(drive[s] < -np.log10(2)):.0%}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
