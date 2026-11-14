"""
Decode audit, version 2: the photometric mass exactly as the decoding-mass letter's pipeline builds it.

The letter's general script (research/generate_from_api_galaxy.py) takes each galaxy's
observations and mass_model from the Gravis catalogue and computes
M_phot(r) = physics.mass_model.enclosed_mass(r, mass_model): Hernquist bulge + exponential
disk + exponential gas. For SPARC galaxies Gravis builds the mass_model from SPARC table1
(data/build_sparc_sources.py): disk M = 0.5 L[3.6], Rd = R_disk; gas M = 1.33 M_HI, Rd = R_HI/3;
bulge M = 0.15 M_disk (Vbul,max/Vdisk,max)^2, a = 0.3 kpc.

Here the observations, mass models and enclosed_mass are taken from Gravis unchanged; the
decode, smoothing and bounds from the letter's own script; the metric, classes and H3 from
CRITERIA.md. Nothing in M_phot is built by this audit.

Usage: python decode_audit_paper_mphot.py GRAVIS_DIR [OUT_DIR]
"""
from __future__ import annotations

import csv
import glob
import importlib.util
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import decode_audit as da  # noqa: E402  (letter functions, metric, classes, statistics)

L, G, A0, MSUN, KPC = da.L, da.G, da.A0, da.MSUN, da.KPC


def normalize_id(raw_name):
    """Gravis's own id rule (data/build_sparc_sources.py, _normalize_id)."""
    import re
    lower = (raw_name or "").strip().lower().replace(" ", "")
    m = re.match(r"(ngc|ugc|ddo|ic|pgc)(0+)(\d+)$", lower)
    if m:
        return m.group(1) + m.group(3)
    m = re.match(r"(ugca)(0*)(\d+)$", lower)
    if m:
        return m.group(1) + (m.group(3) or "")
    return lower.replace("-", "_")


def load_gravis(gravis_dir):
    spec = importlib.util.spec_from_file_location("gravis_mass_model", os.path.join(gravis_dir, "physics", "mass_model.py"))
    mm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mm)
    gals = {}
    for f in sorted(glob.glob(os.path.join(gravis_dir, "data", "sparc_sources", "*.json"))):
        g = json.load(open(f))
        if g.get("observations") and g.get("mass_model"):
            gals[g["id"]] = g
    return mm.enclosed_mass, gals


def main(gravis_dir, out_dir):
    enclosed_mass, gals = load_gravis(gravis_dir)
    table1 = os.path.join(gravis_dir, "data", "sparc_table1.dat")
    T = {}
    for line in open(table1):
        p = line.split()
        if len(p) > 17:
            T[normalize_id(p[0])] = dict(name=p[0], inc=float(p[5]), Q=int(p[17]))
    os.makedirs(out_dir, exist_ok=True)
    extra = sorted(set(gals) - set(T))
    print(f"Gravis SPARC galaxies with observations and a mass model: {len(gals)}; in SPARC table1: {len(set(gals) & set(T))}"
          + (f"; not in table1 (excluded): {extra}" if extra else ""))
    gals = {k: v for k, v in gals.items() if k in T}
    print("Audit A1-A6 (decode, constants, smoothing) as in decode_audit.py: the same letter functions are used.\n")

    rows, prof = [], []
    for gid, g in gals.items():
        R = np.array([o["r"] for o in g["observations"]], float)
        V = np.array([o["v"] for o in g["observations"]], float)
        E = np.array([o.get("err") or 0.0 for o in g["observations"]], float)
        o = np.argsort(R)
        R, V, E = R[o], V[o], E[o]
        if len(R) < 3 or R[0] <= 0:
            continue
        mm = g["mass_model"]
        vs = L["diffraction_smooth"](R, V, frac=0.062)
        _, Mdec = L["velocity_decode"](R, vs, R)
        _, Mlo, Mhi = L["M_dec_bounds"](R, vs, E)
        Mphot = np.array([enclosed_mass(float(r), mm) for r in R]) * MSUN
        gas_only = dict(bulge={"M": 0, "a": 1.0}, disk={"M": 0, "Rd": 1.0}, gas=mm.get("gas", {"M": 0, "Rd": 1.0}))
        Mgas = np.array([enclosed_mass(float(r), gas_only) for r in R]) * MSUN
        if np.any(Mphot <= 0):
            continue
        res = {}
        for s in (0.8, 1.0, 1.2):
            mms = json.loads(json.dumps(mm))
            for comp in ("bulge", "disk"):
                if comp in mms:
                    mms[comp]["M"] = s * mms[comp]["M"]
            Mp = np.array([enclosed_mass(float(r), mms) for r in R]) * MSUN
            D = np.log10(Mdec / Mp)
            Ap, Am = da.areas(R, D)
            fp, fm = float(np.mean(Mlo > Mp)), float(np.mean(Mhi < Mp))
            res[s] = dict(D=D, Ap=Ap, Am=Am, fp=fp, fm=fm, cls=da.classify(Ap, Am, fp, fm))
        base = res[1.0]
        robust = len({res[s]["cls"] for s in res}) == 1
        gobs = (vs * 1e3) ** 2 / (R * KPC)
        Rring = da.crossing(R, np.log(gobs / A0))
        fin = (1.0 if gobs[-1] > A0 else 0.0) if Rring is None else float(np.clip(np.interp(Rring, R, Mphot) / Mphot[-1], 0, 1))
        inside = R < Rring if Rring else np.zeros_like(R, bool)
        m = T.get(gid, {})
        rows.append(dict(galaxy=m.get("name", gid), gravis_id=gid, n=len(R), r_min=R[0], r_max=R[-1],
                         A_above=base["Ap"], A_below=base["Am"], A_net=base["Ap"] - base["Am"],
                         f_above=base["fp"], f_below=base["fm"], cls=base["cls"], robust=robust,
                         cls_robust=base["cls"] if robust else "uncertain",
                         gas_share=float(Mgas[-1] / Mphot[-1]), bulge=bool(mm.get("bulge", {}).get("M", 0) > 0),
                         R_ring=Rring if Rring else float("nan"), f_in=fin,
                         D_in=float(np.mean(base["D"][inside])) if inside.any() else float("nan"),
                         D_out=float(np.mean(base["D"][~inside])) if (~inside).any() else float("nan"),
                         Q=m.get("Q", -1), inc=m.get("inc", float("nan"))))
        for i in range(len(R)):
            prof.append(dict(galaxy=m.get("name", gid), r_kpc=R[i], v_obs=V[i], v_smooth=vs[i], e_v=E[i],
                             M_dec=Mdec[i] / MSUN, M_dec_lo=Mlo[i] / MSUN, M_dec_hi=Mhi[i] / MSUN,
                             M_phot=Mphot[i] / MSUN, M_gas=Mgas[i] / MSUN, Delta_dex=base["D"][i]))

    for fn, data in (("galaxy_summary.csv", rows), ("profiles.csv", prof)):
        with open(os.path.join(out_dir, fn), "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(data[0]))
            w.writeheader()
            for row in data:
                w.writerow({k: (f"{v:.6g}" if isinstance(v, float) else v) for k, v in row.items()})

    print(f"MEASURED: {len(rows)} galaxies, {len(prof)} radii (photometric mass: Gravis mass_model + enclosed_mass)")
    q = [r for r in rows if r["Q"] in (1, 2) and r["inc"] >= 30 and r["n"] >= 5]
    for lab, sel in (("all", rows), ("quality cut", q)):
        print(f"  {lab} (N={len(sel)}):")
        for c in ("drive", "quiet", "brake", "mixed"):
            n = sum(r["cls"] == c for r in sel); nr = sum(r["cls_robust"] == c for r in sel)
            print(f"    {c:6s} {n:3d} ({n / len(sel):.0%})   robust to M/L x0.8-1.2: {nr:3d}")
        print(f"    uncertain: {sum(r['cls_robust'] == 'uncertain' for r in sel)};  median A_net {np.median([r['A_net'] for r in sel]):+.3f} dex")

    print("\nH3  ring share versus net area A")
    res = {}
    for lab, sel in (("(a) all quality-cut", q), ("(b) not gas-dominated", [r for r in q if r["gas_share"] < 0.5]),
                     ("    no bulge", [r for r in q if not r["bulge"]]), ("    gas-dominated", [r for r in q if r["gas_share"] >= 0.5])):
        if len(sel) < 8:
            print(f"  {lab:24s} N={len(sel):3d}  (too few)")
            continue
        rho, p = da.spearman(np.array([r["f_in"] for r in sel]), np.array([r["A_net"] for r in sel]))
        res[lab] = (rho, p)
        print(f"  {lab:24s} N={len(sel):3d}  rho = {rho:+.2f}  one-sided p = {p:.4f}")
    h3 = all(k in res and res[k][0] > 0 and res[k][1] < 0.01 for k in ("(a) all quality-cut", "(b) not gas-dominated"))
    print(f"  H3: {'PASS' if h3 else 'FAIL'}")
    for lab, s in (("all outside the ring (f_in = 0)", lambda r: r["f_in"] == 0),
                   ("ring inside the data", lambda r: 0 < r["f_in"] < 1),
                   ("all inside the ring (f_in = 1)", lambda r: r["f_in"] == 1)):
        sel = [r for r in q if s(r)]
        if sel:
            cnt = {c: sum(r["cls"] == c for r in sel) for c in ("drive", "quiet", "brake", "mixed")}
            print(f"    {lab:34s} N={len(sel):3d}  median A {np.median([r['A_net'] for r in sel]):+.3f}  {cnt}")
    loc = [r for r in q if np.isfinite(r["D_in"]) and np.isfinite(r["D_out"])]
    diff = np.array([r["D_in"] - r["D_out"] for r in loc])
    print(f"\n  Local: {len(loc)} galaxies contain the ring; Delta inside minus outside: median {np.median(diff):+.3f} dex; inside higher in {np.mean(diff > 0):.0%}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "results_paper_mphot"))
