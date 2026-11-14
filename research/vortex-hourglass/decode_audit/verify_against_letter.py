"""
A8: cross-check of the audit's dex against the decoding-mass letter's own validations.

Runs the letter's generate_letter_figures.py (in a scratch directory, so its figures are not
overwritten) to get its data, mass models and decode, then:
  1. reproduces the reference values printed by the letter's run_all_validations.py, in dex;
  2. scores the letter's four galaxies (MW, M33, NGC 3198, CamB) with the audit's area metric;
  3. compares, radius by radius, the letter's profiles with the audit's SPARC profiles for the
     two galaxies in both (NGC 3198, CamB).

Usage: python verify_against_letter.py RESULTS_DIR
"""
from __future__ import annotations

import contextlib
import csv
import io
import os
import runpy
import shutil
import sys
import tempfile

import matplotlib

matplotlib.use("Agg")
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LETTER = os.path.normpath(os.path.join(
    HERE, "../../../papers/letter-decoding-mass-from-rotation-curves/research/generate_letter_figures.py"))
TAU = 0.15
# Reference values printed by the letter's run_all_validations.py (section 3.2)
REF = {"MW": (25.0, 6.58e10, 7.31e10), "M33": (17.0, 1.38e10, 6.85e9), "NGC3198": (30.0, 2.60e10, 3.30e10)}
GAL = {"MW": ("mw_r_obs", "mw_v_obs", "mw_e_obs", "mw_M_enc"),
       "M33": ("m33_r_obs", "m33_v_obs", "m33_e_obs", "m33_M_enc"),
       "NGC3198": ("ngc3198_r_obs", "ngc3198_v_obs", "ngc3198_e_obs", "ngc3198_M_enc"),
       "CamB": ("camb_r_obs", "camb_v_obs", "camb_e_obs", "camb_M_enc")}


def run_letter():
    tmp = tempfile.mkdtemp()
    shutil.copy(LETTER, tmp)
    cwd = os.getcwd()
    try:
        os.chdir(tmp)
        with contextlib.redirect_stdout(io.StringIO()):
            return runpy.run_path(os.path.join(tmp, os.path.basename(LETTER)))
    finally:
        os.chdir(cwd)
        shutil.rmtree(tmp, ignore_errors=True)


def main(results):
    ns = run_letter()
    KPC, MSUN = ns["KPC"], ns["MSUN"]
    prof = {}
    print("1. The letter's reference values (run_all_validations.py, section 3.2), in dex")
    for k, (r, v, e, m) in GAL.items():
        R, V, E = (np.asarray(ns[x], float) for x in (r, v, e))
        vs = ns["diffraction_smooth"](R, V, frac=0.062)
        _, Md = ns["velocity_decode"](R, vs, R)
        _, lo, hi = ns["M_dec_bounds"](R, vs, E)
        Mp = ns[m](R * KPC)
        prof[k] = (R, Md / MSUN, Mp / MSUN, lo, hi, Mp)
        if k in REF:
            r0, dref, pref = REF[k]
            md, mp = np.interp(r0, R, Md / MSUN), np.interp(r0, R, Mp / MSUN)
            ok = f"{md:.2e}" == f"{dref:.2e}" and f"{mp:.2e}" == f"{pref:.2e}"
            print(f"   {k:8s} r = {r0:4.0f} kpc  M_dec {md:.3e} (ref {dref:.2e})  M_phot {mp:.3e} (ref {pref:.2e})  "
                  f"dex {np.log10(md / mp):+.3f} (ref {np.log10(dref / pref):+.3f})  {'PASS' if ok else 'FAIL'}")

    print("\n2. The letter's four galaxies, scored with the audit's area metric")
    for k, (R, Md, Mp, lo, hi, Mpk) in prof.items():
        D = np.log10(Md / Mp)
        lr = np.log(R)
        trap = lambda y: float(np.sum(0.5 * (y[1:] + y[:-1]) * np.diff(lr)) / (lr[-1] - lr[0]))
        Ap, Am = trap(np.maximum(D, 0)), trap(np.maximum(-D, 0))
        fp, fm = float(np.mean(lo > Mpk)), float(np.mean(hi < Mpk))
        A = Ap - Am
        cls = ("mixed" if Ap > TAU and Am > TAU else "drive" if A > TAU and fp >= .5
               else "brake" if A < -TAU and fm >= .5 else "quiet")
        print(f"   {k:8s} {R[0]:5.2f}-{R[-1]:5.1f} kpc  outermost {D[-1]:+.3f} dex  "
              f"A+ {Ap:.3f}  A- {Am:.3f}  A {A:+.3f}  f+ {fp:.2f}  f- {fm:.2f}  -> {cls}")

    print("\n3. Galaxies in both: the letter's profile against the audit's SPARC profile")
    S = {}
    for r in csv.DictReader(open(os.path.join(results, "profiles.csv"))):
        S.setdefault(r["galaxy"], []).append(r)
    summ = {r["galaxy"]: r for r in csv.DictReader(open(os.path.join(results, "galaxy_summary.csv")))}
    for g in ("NGC3198", "CamB"):
        R, Md, Mp = prof[g][:3]
        P = S[g]
        Rs = np.array([float(p["r_kpc"]) for p in P])
        col = lambda key: np.array([float(p[key]) for p in P])
        print(f"   {g}: letter {len(R)} points, SPARC {len(Rs)} points")
        print(f"     {'r':>5s} {'M_dec letter':>12s} {'SPARC':>10s} {'M_phot letter':>13s} {'SPARC':>10s} {'dex letter':>10s} {'SPARC':>7s}")
        for r in R:
            if Rs[0] <= r <= Rs[-1]:
                print(f"     {r:5.2f} {np.interp(r, R, Md):12.3e} {np.interp(r, Rs, col('M_dec')):10.3e} "
                      f"{np.interp(r, R, Mp):13.3e} {np.interp(r, Rs, col('M_phot')):10.3e} "
                      f"{np.log10(np.interp(r, R, Md) / np.interp(r, R, Mp)):+10.3f} {np.interp(r, Rs, col('Delta_dex')):+7.3f}")
        print(f"     SPARC audit: A {float(summ[g]['A_net']):+.3f}, class {summ[g]['cls']}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "results"))
