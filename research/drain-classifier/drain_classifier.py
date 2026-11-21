#!/usr/bin/env python3
"""
Drain-classifier study: the analysis fixed in PREREGISTRATION.md.

  python drain_classifier.py LVDB_DATA_DIR      (writes lvdb_sample.csv and prints the results)
  python drain_classifier.py --from-csv lvdb_sample.csv

LVDB_DATA_DIR is the data/ folder of github.com/apace7/local_volume_database (CC0), commit f0b7356.
"""
import math
import sys

import numpy as np
import pandas as pd

G_PC = 4.30091e-3               # pc (km/s)^2 / Msun
A0 = 1.2e-10                    # m/s^2
A0_PC = A0 * 3.0857e16 / 1e6    # (km/s)^2 / pc   (= 3.70)
M_HOST = {"mw": 6e10, "m31": 1.0e11}
ML_V = 2.0
MODEL_ERR = 0.20
R_CRIT = 20.0                   # pc, C1
FE_CRIT = 0.10                  # dex, C2
EXCLUDE = {"LMC", "SMC", "Sagittarius"}   # the catalogue's names for the LMC, SMC and Sagittarius dSph
TABLES = ["dwarf_mw", "dwarf_m31", "dwarf_local_field", "gc_harris", "gc_mw_new", "gc_ambiguous"]
COLS = ["name", "host", "distance_host", "M_V", "rhalf_sph_physical", "vlos_sigma", "vlos_sigma_em",
        "vlos_sigma_ep", "vlos_sigma_ul", "metallicity_spectroscopic_sigma",
        "metallicity_spectroscopic_sigma_ul"]


def mu(x):
    return x / (1 + x)


def F(gN):
    """the drained law: g_t from g_N (any units, a0 in the same units)"""
    return 0.5 * (gN + np.sqrt(gN * gN + 4 * gN * A0_PC))


def nu(y):
    return 0.5 + np.sqrt(0.25 + 1 / y)


def load(lvdb_dir):
    frames = []
    for t in TABLES:
        d = pd.read_csv(f"{lvdb_dir}/{t}.csv")
        d = d[[c for c in COLS if c in d.columns]].copy()
        d["table"] = t
        frames.append(d)
    d = pd.concat(frames, ignore_index=True)
    ok = (d["vlos_sigma"].notna() & d["vlos_sigma_ul"].isna() & d["vlos_sigma_em"].notna()
          & d["M_V"].notna() & d["rhalf_sph_physical"].notna())
    d = d[ok & ~d["name"].isin(EXCLUDE)]
    has_host = d["host"].isin(["mw", "m31"])
    d = d[~has_host | d["distance_host"].notna()]                     # hosted objects need a distance
    d = d[d["host"].isna() | has_host]                                # field (no host) or MW/M31
    return d.reset_index(drop=True)


def predict(d, ml=ML_V):
    L = 10 ** (-0.4 * (d["M_V"] - 4.83))
    M = ml * L
    Re = d["rhalf_sph_physical"]
    sN = np.sqrt(G_PC * M / (8 * Re))
    D = d["distance_host"].fillna(np.inf) * 1000.0                    # pc
    Mh = d["host"].map(M_HOST).fillna(0.0)
    gNe = np.where(np.isfinite(D), G_PC * Mh / np.where(np.isfinite(D), D, 1.0) ** 2, 0.0)
    ge = F(gNe)
    ge_N = np.where(ge > 0, ge * mu(ge / A0_PC), 0.0)                  # = gNe, its Newtonian equivalent
    gin = G_PC * (M / 2) / (4 * Re / 3) ** 2
    y = (ge_N + gin) / A0_PC
    sG = sN * np.sqrt(nu(y))
    return sN, sG, nu(y), ge / A0_PC


def classify(d):
    c1 = d["rhalf_sph_physical"] >= R_CRIT
    fe = d["metallicity_spectroscopic_sigma"]
    fe_ul = d["metallicity_spectroscopic_sigma_ul"].notna()
    c2 = pd.Series(np.where(fe.notna() & ~fe_ul, np.where(fe >= FE_CRIT, 1.0, 0.0), np.nan), index=d.index)
    c2[fe_ul] = 0.0                                                    # an upper limit = no resolved spread
    return c1, c2


def stats(obs, err, pred):
    z = (obs - pred) / err
    return float(np.mean(z ** 2)), float(np.mean(np.abs(z) < 3)), z


def run(d, ml=ML_V, verbose=True):
    sN, sG, nuy, xe = predict(d, ml)
    so = d["vlos_sigma"].values
    em, ep = d["vlos_sigma_em"].values, d["vlos_sigma_ep"].fillna(d["vlos_sigma_em"]).values
    c1, c2 = classify(d)
    out = {}
    for label, cls in (("C1 structural", c1.astype(float)), ("C2 chemical", c2)):
        sel = cls.notna().values
        inf = sel & (nuy > 1.5)
        res = {}
        for name, pred in (("classifier", np.where(cls.values == 1, sG, sN)), ("Newton all", sN), ("GFD all", sG)):
            # asymmetric errors: use the error on the side of the prediction
            e_obs = np.where(pred > so, ep, em)
            err = np.sqrt(e_obs ** 2 + (MODEL_ERR * pred) ** 2)
            chi_all, f_all, _ = stats(so[sel], err[sel], pred[sel])
            chi_inf, f_inf, z = stats(so[inf], err[inf], pred[inf])
            res[name] = (chi_all, f_all, chi_inf, f_inf)
        out[label] = (int(sel.sum()), int(inf.sum()), res)
        if verbose:
            print(f"\n{label}: classified {sel.sum()}, informative (nu > 1.5) {inf.sum()}, "
                  f"drained {int((cls[sel] == 1).sum())}, not drained {int((cls[sel] == 0).sum())}")
            print(f"  {'rule':12s} {'chi2/N all':>11s} {'<3sig all':>10s} {'chi2/N inf':>11s} {'<3sig inf':>10s}")
            for name, (a, b, c, e) in res.items():
                print(f"  {name:12s} {a:11.2f} {b:10.2f} {c:11.2f} {e:10.2f}")
    return out, (sN, sG, nuy, xe, c1, c2)


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "--from-csv":
        d = pd.read_csv(sys.argv[2])
    elif len(sys.argv) >= 2:
        d = load(sys.argv[1])
        d.to_csv("lvdb_sample.csv", index=False)
    else:
        print(__doc__)
        sys.exit(1)
    print(f"sample: {len(d)} objects ({(d['table'].str.startswith('gc')).sum()} cluster-table, "
          f"{(d['table'].str.startswith('dwarf')).sum()} dwarf-table)")
    out, (sN, sG, nuy, xe, c1, c2) = run(d)
    for ml in (1.0, 3.0):
        print(f"\n--- sensitivity: M/L_V = {ml}")
        run(d, ml)
    # per-object table for the informative objects
    print("\nInformative objects (nu > 1.5): name, r_h [pc], sigma[Fe/H], C1, C2, sigma_obs, sigma_N, sigma_GFD, z_N, z_GFD")
    so = d["vlos_sigma"].values
    em, ep = d["vlos_sigma_em"].values, d["vlos_sigma_ep"].fillna(d["vlos_sigma_em"]).values
    rows = []
    for i in np.where(nuy > 1.5)[0]:
        eN = math.hypot(ep[i] if sN[i] > so[i] else em[i], MODEL_ERR * sN[i])
        eG = math.hypot(ep[i] if sG[i] > so[i] else em[i], MODEL_ERR * sG[i])
        rows.append((d["rhalf_sph_physical"][i], d["name"][i], d["metallicity_spectroscopic_sigma"][i],
                     int(c1[i]), c2[i], so[i], sN[i], sG[i], (so[i] - sN[i]) / eN, (so[i] - sG[i]) / eG))
    for r_ in sorted(rows):
        rh, n, fe, a, b, s, n_, g_, zn, zg = r_
        fe_s = "  -  " if pd.isna(fe) else f"{fe:5.2f}"
        b_s = "-" if pd.isna(b) else str(int(b))
        print(f"  {n[:22]:22s} {rh:7.1f} {fe_s} {a} {b_s} {s:6.2f} {n_:6.2f} {g_:6.2f} {zn:+6.1f} {zg:+6.1f}")


if __name__ == "__main__":
    main()
