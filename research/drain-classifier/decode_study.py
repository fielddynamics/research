#!/usr/bin/env python3
"""
Decode study: drained dwarfs read as quiet, drive or brake; undrained clusters must be Newtonian.

Following the decoding-mass letter (papers/letter-decoding-mass-from-rotation-curves):
  1. Decode each drained system from its kinematics alone: M_dec = r v^4 / [G (a0 r + v^2)], with the
     circular speed at the 3D half-light radius from the dispersion, v^2 = 3 sigma^2, r = r_1/2 = 4 R_e/3
     (Wolf et al. 2010).
  2. Compare with the photometric mass inside the same radius, M_phot = (M/L_V) L_V / 2.
  3. Read log10(M_dec/M_phot): quiet within +-0.2 dex (the M/L uncertainty), drive above, brake below.
  A system with no drain has no interior: its Newtonian dynamical mass 3 sigma^2 r_1/2/G must equal M_phot.

  python decode_study.py LVDB_DATA_DIR       (writes decode_sample.csv)
  python decode_study.py --from-csv decode_sample.csv
"""
import sys

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

G_PC = 4.30091e-3               # pc (km/s)^2 / Msun
A0_PC = 1.2e-10 * 3.0857e16 / 1e6   # (km/s)^2 / pc
ML_V = 2.0
QUIET = 0.2                     # dex
# baryonic masses of the drained hosts (catalogue host codes); the LMC and M33 are drained spirals too
M_HOST = {"mw": 6e10, "m_031": 1.0e11, "m_033": 1.0e10, "lmc": 3e9}
M_MW = 6e10
EXCLUDE = {"LMC", "SMC", "Sagittarius", "Palomar 5"}   # rotating or tidally disrupting
TABLES = ["dwarf_mw", "dwarf_m31", "dwarf_local_field", "gc_harris", "gc_mw_new", "gc_ambiguous"]
COLS = ["name", "host", "distance_host", "distance_gc", "M_V", "rhalf_sph_physical", "vlos_sigma", "vlos_sigma_em",
        "vlos_sigma_ep", "vlos_sigma_ul", "mass_HI", "metallicity_spectroscopic_sigma"]
# Remote clusters whose dispersions are not in the catalogue, from the original papers
# (name, M_V-equivalent mass [Msun], R_e [pc], D [kpc], sigma, err)
LITERATURE_CLUSTERS = [
    ("Palomar 14 (Jordi+2009)", 1.2e4, 26.0, 71.0, 0.38, 0.12),
    ("Palomar 4 (Frank+2012)", 2.98e4, 18.4, 103.0, 0.87, 0.18),
]


def mu(x):
    return x / (1 + x)


def F(gN):
    return 0.5 * (gN + np.sqrt(gN * gN + 4 * gN * A0_PC))


def load(lvdb_dir):
    frames = []
    for t in TABLES:
        d = pd.read_csv(f"{lvdb_dir}/{t}.csv")
        d = d[[c for c in COLS if c in d.columns]].copy()
        d["table"] = t
        frames.append(d)
    d = pd.concat(frames, ignore_index=True)
    ok = (d["vlos_sigma"].notna() & d["vlos_sigma_ul"].isna() & d["vlos_sigma_em"].notna()
          & d["M_V"].notna() & d["rhalf_sph_physical"].notna() & ~d["name"].isin(EXCLUDE))
    d = d[ok]
    d = d[d["host"] != "sagittarius_1"]                                # clusters of the disrupting Sgr dwarf
    known = d["host"].isin(list(M_HOST))
    d = d[(known & d["distance_host"].notna()) | ~known]               # other hosts: treated as field
    return d.reset_index(drop=True)


def quantities(d, ml=ML_V):
    out = pd.DataFrame({"name": d["name"], "table": d["table"], "host": d["host"]})
    L = 10 ** (-0.4 * (d["M_V"] - 4.83))
    Re = d["rhalf_sph_physical"]
    r12 = 4 * Re / 3
    s = d["vlos_sigma"]
    err = np.where(d["vlos_sigma_ep"].notna(), 0.5 * (d["vlos_sigma_em"] + d["vlos_sigma_ep"]), d["vlos_sigma_em"])
    v2 = 3 * s ** 2
    out["L"] = L
    out["Re"] = Re
    out["M_phot"] = ml * L / 2
    out["M_dec"] = r12 * v2 ** 2 / (G_PC * (A0_PC * r12 + v2))             # the letter's decode
    out["M_newton"] = v2 * r12 / G_PC                                       # undrained: Newton
    out["dlog_err"] = 4 * err / s / np.log(10)                              # from sigma^4 (deep decode)
    out["x_obs"] = v2 / r12 / A0_PC
    # host's net field at the object (a drained host), for the variant that adds it
    D = d["distance_host"] * 1000.0
    Mh = d["host"].map(M_HOST)
    known = Mh.notna() & D.notna()
    ge = np.where(known, F(G_PC * Mh.fillna(0.0) / D.fillna(1.0) ** 2), 0.0)
    # satellites of the LMC also sit in the Milky Way's field (magnitudes added: an upper bound)
    lmc = (d["host"] == "lmc") & d["distance_gc"].notna()
    ge = ge + np.where(lmc, F(G_PC * M_MW / (d["distance_gc"].fillna(1.0) * 1000.0) ** 2), 0.0)
    out["x_host"] = ge / A0_PC
    gobs = v2 / r12
    out["M_dec_host"] = mu((gobs + ge) / A0_PC) * gobs * r12 ** 2 / G_PC     # decode with total field
    out["dist_host"] = d["distance_host"]
    out["sigma_FeH"] = d["metallicity_spectroscopic_sigma"]
    out["gas"] = d["mass_HI"].fillna(0.0) > 0
    out["surface_density"] = L / (2 * np.pi * Re ** 2)
    return out


def reading(dlog):
    return np.where(dlog > QUIET, "drive", np.where(dlog < -QUIET, "brake", "quiet"))


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "--from-csv":
        d = pd.read_csv(sys.argv[2])
    elif len(sys.argv) >= 2:
        d = load(sys.argv[1])
        d.to_csv("decode_sample.csv", index=False)
    else:
        print(__doc__)
        sys.exit(1)
    q = quantities(d)
    dw = q[q["table"].str.startswith("dwarf")].copy()
    gc = q[q["table"].str.startswith("gc")].copy()
    print(f"sample: {len(dw)} dwarfs (drained), {len(gc)} clusters (not drained) from the catalogue")

    # ---------------- 1. drained dwarfs: decode
    dw["dlog"] = np.log10(dw["M_dec"] / dw["M_phot"])
    dw["dlog_host"] = np.log10(dw["M_dec_host"] / dw["M_phot"])
    dw["reading"] = reading(dw["dlog"])
    dw["reading_host"] = reading(dw["dlog_host"])
    print("\n1. DRAINED DWARFS, decoded (the letter's decode, own field). log10(M_dec/M_phot), quiet within +-0.2 dex")
    counts = dw["reading"].value_counts()
    print("   " + ", ".join(f"{k} {counts.get(k, 0)}" for k in ("quiet", "drive", "brake")))
    ch = dw["reading_host"].value_counts()
    print("   with the host's field added: " + ", ".join(f"{k} {ch.get(k, 0)}" for k in ("quiet", "drive", "brake")))
    for ml in (1.0, 3.0):
        dl = np.log10(dw["M_dec"] / (dw["M_phot"] * ml / ML_V))
        c = pd.Series(reading(dl)).value_counts()
        print(f"   M/L_V = {ml}: " + ", ".join(f"{k} {c.get(k, 0)}" for k in ("quiet", "drive", "brake")))
    print(f"   median log10(M_dec/M_phot) = {dw['dlog'].median():+.2f} dex")
    print(f"\n   {'dwarf':22s} {'host':6s} {'L/Lsun':>9s} {'R_e':>7s} {'x_obs':>6s} {'x_host':>6s} {'dlog':>6s} {'+-':>5s} {'read':>6s} {'dlog_h':>6s} {'read_h':>6s}")
    for _, r_ in dw.sort_values("dlog").iterrows():
        print(f"   {r_['name'][:22]:22s} {str(r_['host'])[:6]:6s} {r_['L']:9.2e} {r_['Re']:7.1f} {r_['x_obs']:6.3f} {r_['x_host']:6.3f} "
              f"{r_['dlog']:+6.2f} {r_['dlog_err']:5.2f} {r_['reading']:>6s} {r_['dlog_host']:+6.2f} {r_['reading_host']:>6s}")

    # ---------------- 2. undrained clusters: Newton
    gc["dlog_N"] = np.log10(gc["M_newton"] / gc["M_phot"])
    lit = pd.DataFrame([{"name": n, "M_phot": M / 2, "M_newton": 3 * s_ ** 2 * (4 * Re / 3) / G_PC,
                         "dlog_err": 2 * e / s_ / np.log(10), "Re": Re, "x_obs": 3 * s_ ** 2 / (4 * Re / 3) / A0_PC,
                         "sigma_N_pred": np.sqrt(G_PC * M / (8 * Re)), "sigma": s_}
                        for n, M, Re, D, s_, e in LITERATURE_CLUSTERS])
    lit["dlog_N"] = np.log10(lit["M_newton"] / lit["M_phot"])
    gc["dlog_errN"] = gc["dlog_err"] / 2                                    # Newton mass ~ sigma^2
    print("\n2. CLUSTERS (no drain, no interior): Newtonian mass must equal photometric mass")
    print(f"   catalogue clusters: {len(gc)}; median log10(M_N/M_phot) = {gc['dlog_N'].median():+.2f} dex")
    low = gc["x_obs"] < 1
    print(f"   at low acceleration (x_obs < 1): {low.sum()} clusters, median {gc.loc[low, 'dlog_N'].median():+.2f} dex")
    sigN = np.sqrt(G_PC * 2 * gc["M_phot"] / (8 * gc["Re"]))
    clean = sigN > 1.0
    print(f"   predicted sigma_N > 1 km/s (binary motions minor): {clean.sum()} clusters, "
          f"median {gc.loc[clean, 'dlog_N'].median():+.2f} dex, within +-0.3 dex: {np.mean(np.abs(gc.loc[clean, 'dlog_N']) < 0.3):.2f}")
    print(f"   predicted sigma_N < 1 km/s: {(~clean).sum()} clusters, median {gc.loc[~clean, 'dlog_N'].median():+.2f} dex")
    print(f"\n   {'cluster':24s} {'L/Lsun':>9s} {'R_e':>6s} {'x_obs':>6s} {'sig_N':>6s} {'dlog_N':>7s} {'+-':>5s}")
    for _, r_ in gc[low].sort_values("dlog_N").iterrows():
        print(f"   {r_['name'][:24]:24s} {r_['L']:9.2e} {r_['Re']:6.1f} {r_['x_obs']:6.3f} "
              f"{np.sqrt(G_PC * 2 * r_['M_phot'] / (8 * r_['Re'])):6.2f} {r_['dlog_N']:+7.2f} {r_['dlog_errN']:5.2f}")
    # what mu would give these clusters if they were drained (own field plus host), for comparison
    y = (gc["x_host"] * mu(gc["x_host"]) * A0_PC + G_PC * gc["M_phot"] / (4 * gc["Re"] / 3) ** 2) / A0_PC
    gc["pred_mu"] = np.log10(0.5 + np.sqrt(0.25 + 1 / y))
    sel = low & clean
    e = gc["dlog_errN"]
    chiN = np.mean((gc.loc[sel, "dlog_N"] / e[sel]) ** 2)
    chiM = np.mean(((gc.loc[sel, "dlog_N"] - gc.loc[sel, "pred_mu"]) / e[sel]) ** 2)
    print(f"   low acceleration and sigma_N > 1 km/s: {sel.sum()} clusters; chi2/N Newton {chiN:.1f}, mu {chiM:.1f} "
          f"(mu would put them {gc.loc[sel, 'pred_mu'].median():+.2f} dex above Newton, median)")
    print("   literature:")
    for _, r_ in lit.iterrows():
        yl = G_PC * 2 * r_["M_phot"] / (4 * r_["Re"] / 3) ** 2 / A0_PC
        print(f"   {r_['name'][:24]:24s} {'':9s} {r_['Re']:6.1f} {r_['x_obs']:6.3f} {r_['sigma_N_pred']:6.2f} "
              f"{r_['dlog_N']:+7.2f} {r_['dlog_err']:5.2f}   (mu alone would give >= {np.log10(0.5 + np.sqrt(0.25 + 1 / yl)):+.2f})")

    # ---------------- 3. do drive and brake track anything independent?
    print("\n3. DOES THE DECODED READING TRACK ANYTHING INDEPENDENT?  Spearman rank correlation with log10(M_dec/M_phot)")
    print("   (5 tests; Bonferroni threshold p < 0.01)")
    tests = [("distance to host (kpc)", dw["dist_host"]),
             ("stellar luminosity", np.log10(dw["L"])),
             ("surface density L/(2 pi R_e^2)", np.log10(dw["surface_density"])),
             ("half-light radius", np.log10(dw["Re"])),
             ("metallicity spread", dw["sigma_FeH"])]
    for label, v in tests:
        m = v.notna() & dw["dlog"].notna()
        rho, p = spearmanr(v[m], dw.loc[m, "dlog"])
        print(f"   {label:32s} N={m.sum():3d}  rho={rho:+.2f}  p={p:.1e}")
    for label, m in (("gas-rich (HI detected)", dw["gas"]), ("gas-free", ~dw["gas"])):
        print(f"   {label:32s} N={m.sum():3d}  median dlog {dw.loc[m, 'dlog'].median():+.2f}")
    lL = np.log10(dw["L"])
    coef = np.polyfit(lL, dw["dlog"], 1)
    resid = dw["dlog"] - np.polyval(coef, lL)
    print(f"\n   the reading falls with luminosity: log10(M_dec/M_phot) = {coef[0]:+.2f} log10 L {coef[1]:+.2f}")
    print("   with luminosity controlled (Spearman on the residual):")
    for label, v in (("distance to host", dw["dist_host"]), ("surface density", np.log10(dw["surface_density"])),
                     ("half-light radius", np.log10(dw["Re"])), ("gas-rich", dw["gas"].astype(float)),
                     ("metallicity spread", dw["sigma_FeH"])):
        m = v.notna()
        rho, p = spearmanr(v[m], resid[m])
        print(f"   {label:32s} N={m.sum():3d}  rho={rho:+.2f}  p={p:.1e}")
    for label, hs in (("residual, Milky Way/LMC", ("mw", "lmc")), ("residual, M31/M33", ("m_031", "m_033"))):
        m = dw["host"].isin(hs)
        print(f"   {label:32s} N={m.sum():3d}  median {resid[m].median():+.2f}")
    m = ~dw["host"].isin(list(M_HOST))
    print(f"   {'residual, field':32s} N={m.sum():3d}  median {resid[m].median():+.2f}")
    print("   without luminosity controlled:")
    for label, hs in (("satellites of the Milky Way/LMC", ("mw", "lmc")), ("satellites of M31/M33", ("m_031", "m_033"))):
        m = dw["host"].isin(hs)
        print(f"   {label:32s} N={m.sum():3d}  median dlog {dw.loc[m, 'dlog'].median():+.2f}")
    m = ~dw["host"].isin(list(M_HOST))
    print(f"   field (no host)                  N={m.sum():3d}  median dlog {dw.loc[m, 'dlog'].median():+.2f}")


if __name__ == "__main__":
    main()
