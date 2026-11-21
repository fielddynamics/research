#!/usr/bin/env python3
"""
What the SPARC survey can determine: for each galaxy built exactly by the letter's recipe (no bulge,
R_HI catalogued, SPARC quality 1-2), the stellar mass-to-light ratio that would make it quiet, whether
its gas alone outweighs the decoded mass, and whether the two curves cross.

  python sparc_survey_analysis.py ROTMOD_DIR     (run sparc_survey.py first)
"""
import csv
import os
import sys

import numpy as np
from scipy.stats import spearmanr

import sparc_survey as S

HERE = os.path.dirname(os.path.abspath(__file__))
UPS_LO, UPS_HI, UPS_DRIVE = 0.2, 0.8, 1.5     # plausible stellar M/L at 3.6 um; beyond what stars supply


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    rot = sys.argv[1]
    L = S.letter_functions()
    smooth, decode, MSUN, KPC, G = L["diffraction_smooth"], L["velocity_decode"], L["MSUN"], L["KPC"], L["G"]
    t1 = S.table1()
    props = {}
    for line in open(S.TABLE1):
        p = line.split()
        if len(p) >= 18:
            props[p[0]] = dict(T=float(p[1]), D=float(p[2]), inc=float(p[5]), L=float(p[7]), SB=float(p[10]),
                               Vf=float(p[15]))
    rows = []
    for x in csv.DictReader(open(os.path.join(HERE, "sparc_survey_results.csv"))):
        if x["flags"] or int(x["quality"]) > 2:
            continue
        n = x["galaxy"]
        lum, rd, mhi, rhi, q = t1[n]
        a = np.loadtxt(os.path.join(rot, f"{n}_rotmod.dat"), comments="#")
        r, v, vg = a[:, 0], a[:, 1], a[:, 3]
        m = (r > 0) & (v > 0)
        r, v, vg = r[m], v[m], vg[m]
        rdec = np.linspace(r[0], r[-1], 500)
        _, mdec = decode(r, smooth(r, v), rdec)
        rm = rdec * KPC
        xd = rm / (rd * KPC)
        m_star_per_ups = lum * MSUN * (1 - (1 + xd) * np.exp(-xd))       # disk mass for M/L = 1
        xg = rdec / (rhi / 3)
        m_gas = 1.33 * mhi * MSUN * (1 - (1 + xg) * np.exp(-xg))         # the letter's gas recipe
        m_gas_obs = rm * np.interp(rdec, r, vg * np.abs(vg)) * 1e6 / G   # SPARC's measured gas distribution
        I = lambda f: np.trapezoid(f, rdec)
        ups_quiet = (I(mdec) - I(m_gas)) / I(m_star_per_ups)
        dm = mdec - (0.5 * m_star_per_ups + m_gas)
        s = np.sign(dm[dm != 0])
        crosses = bool(np.any(s[1:] != s[:-1]))
        robust = ("brake" if ups_quiet < UPS_LO else "drive" if ups_quiet > UPS_DRIVE else "")
        rows.append({"galaxy": n, "net_area": float(x["net_area"]), "reading": x["reading"],
                     "Upsilon_for_quiet": round(ups_quiet, 3),
                     "gas_over_decoded_recipe": round(I(m_gas) / I(mdec), 3),
                     "gas_over_decoded_measured": round(I(m_gas_obs) / I(mdec), 3),
                     "curves_cross": crosses, "robust": robust,
                     "V_flat": props[n]["Vf"], "inclination": props[n]["inc"], "SB_eff": props[n]["SB"],
                     "type": props[n]["T"]})
    with open(os.path.join(HERE, "sparc_survey_analysis.csv"), "w", newline="") as fo:
        w = csv.DictWriter(fo, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    U = np.array([x["Upsilon_for_quiet"] for x in rows])
    print(f"Galaxies (letter recipe exactly, quality 1-2): {len(rows)}")
    print(f"Upsilon_disk that makes each galaxy quiet: median {np.median(U):.2f}, 16-84%: "
          f"{np.percentile(U, 16):.2f} to {np.percentile(U, 84):.2f}")
    print(f"   within {UPS_LO}-{UPS_HI} (reading could be stellar M/L): {((U >= UPS_LO) & (U <= UPS_HI)).sum()}")
    print(f"   below {UPS_LO} (brake with little or no stars): {(U < UPS_LO).sum()}, of which below 0 "
          f"(gas alone outweighs the decoded mass): {(U < 0).sum()}")
    print(f"   above {UPS_HI}: {(U > UPS_HI).sum()}, of which above {UPS_DRIVE} (drive beyond what stars supply): "
          f"{(U > UPS_DRIVE).sum()}")
    ge = np.array([x["gas_over_decoded_recipe"] for x in rows])
    go = np.array([x["gas_over_decoded_measured"] for x in rows])
    print(f"Gas alone outweighs the decoded mass: {(ge > 1).sum()} with the letter's gas recipe, "
          f"{(go > 1).sum()} with SPARC's measured gas distribution")
    print(f"Decoded and photometric curves cross within the observed range: "
          f"{sum(x['curves_cross'] for x in rows)} of {len(rows)}")
    groups = {"robust brake": [x for x in rows if x["robust"] == "brake"],
              "robust drive": [x for x in rows if x["robust"] == "drive"],
              "the rest": [x for x in rows if not x["robust"]]}
    print("\nGroup properties (medians):")
    for k, g in groups.items():
        vf = [x["V_flat"] for x in g if x["V_flat"] > 0]
        print(f"   {k:13s} N={len(g):3d}  V_flat {np.median(vf):5.0f} km/s  inclination {np.median([x['inclination'] for x in g]):4.0f} deg  "
              f"SB_eff {np.median([x['SB_eff'] for x in g]):6.1f} Lsun/pc^2  type {np.median([x['type'] for x in g]):.0f}")
    for k in ("robust brake", "robust drive"):
        print(f"\n{k}: " + ", ".join(f"{x['galaxy']} ({x['Upsilon_for_quiet']:.2f})"
                                     for x in sorted(groups[k], key=lambda y: y["Upsilon_for_quiet"])))
    print("\nNet area against galaxy properties (Spearman, all galaxies):")
    net = np.array([x["net_area"] for x in rows])
    for lab, key in (("distance", "D"), ("inclination", "inc"), ("Hubble type", "T"), ("surface brightness", "SB"),
                     ("V_flat", "Vf")):
        vals = np.array([props[x["galaxy"]][key] for x in rows])
        msk = vals > 0 if key == "Vf" else np.isfinite(vals)
        rho, p = spearmanr(vals[msk], net[msk])
        print(f"   {lab:20s} N={msk.sum():3d}  rho={rho:+.2f}  p={p:.1e}")


if __name__ == "__main__":
    main()
