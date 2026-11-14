"""
Referee checks on the measured partition (T1-T3) and on the letter's photometric pipeline.

R1  Galaxy weighting: crossing of the shares with every galaxy weighted equally (each galaxy's
    mu_obs interpolated onto a common log10 x grid inside its own range, then the median over
    galaxies), against the point-weighted binned median.
R2  Bin placement: crossing with the bins shifted by half a bin.
R3  Smoothing: the thin-disk diagnostic with unsmoothed g_obs (as SPARC's g_bar is unsmoothed).
R4  Bulge light in the letter's pipeline (Gravis): the disk mass is 0.5 L[3.6] of the *total*
    light and a bulge is added on top; size of the double count where a bulge is present.

Usage: python referee_checks.py ROTMOD_DIR GRAVIS_DIR [RESULTS_DIR]
"""
from __future__ import annotations

import glob
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import measured_partition as mp  # noqa: E402

A0, KPC = 1.2e-10, 3.086e19
rng = np.random.default_rng(2026)


def crossing_galaxy_weighted(D, grid=np.arange(-1.0, 1.01, 0.05)):
    meds = []
    for t in grid:
        vals = []
        for d in D.values():
            o = np.argsort(d["lx"]); lx, mu = d["lx"][o], d["mu"][o]
            if lx[0] <= t <= lx[-1]:
                vals.append(np.interp(t, lx, mu))
        meds.append(np.median(vals) if len(vals) >= 15 else np.nan)
    meds = np.array(meds)
    for i in range(len(grid) - 1):
        if np.isfinite(meds[i]) and np.isfinite(meds[i + 1]) and meds[i] < 0.5 <= meds[i + 1]:
            return grid[i] + (0.5 - meds[i]) * (grid[i + 1] - grid[i]) / (meds[i + 1] - meds[i])
    return np.nan


def boot(D, fn, n=1000):
    gal = sorted(D)
    out = []
    for _ in range(n):
        b = rng.choice(len(gal), len(gal))
        out.append(fn({f"{k}_{gal[i]}": D[gal[i]] for k, i in enumerate(b)}))  # one key per draw: a true bootstrap
    out = np.array(out); out = out[np.isfinite(out)]
    return np.percentile(out, [2.5, 97.5])


def unsmoothed(D, rotmod_dir):
    out = {}
    names = {os.path.basename(f)[:-len("_rotmod.dat")]: f for f in glob.glob(os.path.join(rotmod_dir, "*_rotmod.dat"))}
    for g in D:
        if g not in names:
            continue
        a = np.loadtxt(names[g], comments="#", ndmin=2)
        R = a[:, 0] * KPC
        gobs = (a[:, 1] * 1e3) ** 2 / R
        gbar = (np.abs(a[:, 3]) * a[:, 3] + 0.5 * a[:, 4] ** 2 + 0.7 * a[:, 5] ** 2) * 1e6 / R
        out[g] = dict(lx=np.log10(gobs / A0), mu=gbar / gobs, gas=D[g]["gas"])
    return out


def main(rotmod_dir, gravis_dir, res):
    D = mp.load(res)
    T = mp.load_thin_disk(D, rotmod_dir)
    U = unsmoothed(D, rotmod_dir)
    print("Crossing of the shares (median mu_obs = 1/2), log10 x and x, 95% bootstrap over galaxies")
    for lab, DD in (("(a) letter's M_phot", D), ("(b) SPARC g_bar", T), ("(b) SPARC g_bar, unsmoothed g_obs [R3]", U)):
        allx = np.concatenate([d["lx"] for d in DD.values()]); allm = np.concatenate([d["mu"] for d in DD.values()])
        pw = mp.cross_half(allx, allm)
        lo, hi = boot(DD, lambda E: mp.cross_half(np.concatenate([d["lx"] for d in E.values()]),
                                                  np.concatenate([d["mu"] for d in E.values()])))
        gw = crossing_galaxy_weighted(DD)
        glo, ghi = boot(DD, crossing_galaxy_weighted, n=400)
        save = mp.EDGES
        mp.EDGES = save + 0.125
        sh = mp.cross_half(allx, allm)
        mp.EDGES = save
        print(f"  {lab:40s} point-weighted x = {10 ** pw:.2f} ({10 ** lo:.2f}-{10 ** hi:.2f})   "
              f"galaxy-weighted [R1] x = {10 ** gw:.2f} ({10 ** glo:.2f}-{10 ** ghi:.2f})   bins shifted [R2] x = {10 ** sh:.2f}")

    print("\nR4  bulge light in the letter's (Gravis) photometric mass")
    t1 = {}
    for line in open(os.path.join(gravis_dir, "data", "sparc_table1.dat")):
        p = line.split()
        if len(p) > 17:
            t1[p[0]] = float(p[7]) * 1e9
    rows = []
    for f in glob.glob(os.path.join(rotmod_dir, "*_rotmod.dat")):
        name = os.path.basename(f)[:-len("_rotmod.dat")]
        a = np.loadtxt(f, comments="#", ndmin=2)
        if not np.any(a[:, 7] > 0) or name not in t1:
            continue
        Rpc = a[:, 0] * 1e3

        def light(SB):
            Lc = np.empty_like(Rpc); Lc[0] = np.pi * Rpc[0] ** 2 * SB[0]
            ff = 2 * np.pi * Rpc * SB
            Lc[1:] = Lc[0] + np.cumsum(0.5 * (ff[1:] + ff[:-1]) * np.diff(Rpc))
            return Lc[-1]
        Lb, Ld = light(a[:, 7]), light(a[:, 6])
        gid = mp_normalize(name)
        js = os.path.join(gravis_dir, "data", "sparc_sources", gid + ".json")
        if not os.path.exists(js):
            continue
        mm = json.load(open(js))["mass_model"]
        stars_gravis = mm["disk"]["M"] + mm["bulge"]["M"]
        stars_sparc = 0.5 * Ld + 0.7 * Lb
        rows.append((name, Lb / (Lb + Ld), stars_gravis / stars_sparc, mm["bulge"]["M"] / (0.7 * Lb)))
    r = np.array([x[1:] for x in rows])
    print(f"  {len(rows)} galaxies with a bulge. Bulge share of 3.6um light: median {np.median(r[:, 0]):.2f}")
    print(f"  Gravis stars (0.5 L_total + bulge) / SPARC stars (0.5 L_disk + 0.7 L_bulge): median {np.median(r[:, 1]):.2f}, "
          f"range {r[:, 1].min():.2f}-{r[:, 1].max():.2f}")
    print(f"  Gravis bulge mass / SPARC bulge mass (0.7 L_bulge): median {np.median(r[:, 2]):.2f}")


def mp_normalize(raw):
    import re
    lower = raw.strip().lower().replace(" ", "")
    m = re.match(r"(ngc|ugc|ddo|ic|pgc)(0+)(\d+)$", lower)
    if m:
        return m.group(1) + m.group(3)
    m = re.match(r"(ugca)(0*)(\d+)$", lower)
    if m:
        return m.group(1) + (m.group(3) or "")
    return lower.replace("-", "_")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, "decode_audit", "results_paper_mphot"))
