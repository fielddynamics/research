"""
Decode audit and full-profile drive/brake for SPARC, per CRITERIA.md (fixed beforehand).

The decode functions and constants are not re-typed: they are loaded from the letter's own
script, papers/letter-decoding-mass-from-rotation-curves/research/generate_letter_figures.py,
by extracting their source with ast. The M33 data are taken from the same file.

Usage:
  python decode_audit.py ROTMOD_DIR TABLE1_PATH [OUT_DIR]
Writes OUT_DIR/galaxy_summary.csv, OUT_DIR/profiles.csv, OUT_DIR/profile_atlas.pdf.
"""
from __future__ import annotations

import ast
import csv
import glob
import os
import sys

import numpy as np
from scipy.ndimage import gaussian_filter1d

HERE = os.path.dirname(os.path.abspath(__file__))
LETTER = os.path.normpath(os.path.join(
    HERE, "../../../papers/letter-decoding-mass-from-rotation-curves/research/generate_letter_figures.py"))
TAU = 0.15
rng = np.random.default_rng(2026)


# ------------------------------------------------------------------ load the letter's code
def load_letter():
    src = open(LETTER).read()
    tree = ast.parse(src)
    want_fn = {"diffraction_smooth", "velocity_decode", "M_dec_bounds", "forward_gfd", "decoded_M_single"}
    want_var = {"G", "A0", "MSUN", "KPC", "m33_r_obs", "m33_v_obs", "m33_e_obs"}
    ns = {"np": np, "gaussian_filter1d": gaussian_filter1d}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in want_fn:
            exec(compile(ast.Module([node], []), LETTER, "exec"), ns)
        elif isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in want_var for t in node.targets):
            exec(compile(ast.Module([node], []), LETTER, "exec"), ns)
    missing = (want_fn | want_var) - set(ns)
    if missing:
        raise SystemExit(f"could not load from the letter: {sorted(missing)}")
    return ns


L = load_letter()
G, A0, MSUN, KPC = L["G"], L["A0"], L["MSUN"], L["KPC"]


def mdec_closed(r_kpc, v_kms):
    """The decode as written in the letter, Eq. (Mdec): r v^4 / [G (a0 r + v^2)]."""
    r, v = np.asarray(r_kpc) * KPC, np.asarray(v_kms) * 1e3
    return r * v ** 4 / (G * (A0 * r + v ** 2))


def enclosed_light(R_kpc, SB):
    Rpc = R_kpc * 1e3
    out = np.empty_like(Rpc)
    out[0] = np.pi * Rpc[0] ** 2 * SB[0]
    f = 2 * np.pi * Rpc * SB
    out[1:] = out[0] + np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(Rpc))
    return out


def crossing(R, f):
    for i in range(len(R) - 1):
        if f[i] > 0 >= f[i + 1]:
            t = f[i] / (f[i] - f[i + 1])
            return float(np.exp(np.log(R[i]) + t * (np.log(R[i + 1]) - np.log(R[i]))))
    return None


def areas(R, D):
    lr = np.log(R)
    span = lr[-1] - lr[0]
    trap = lambda y: float(np.sum(0.5 * (y[1:] + y[:-1]) * np.diff(lr)) / span)
    return trap(np.maximum(D, 0)), trap(np.maximum(-D, 0))


def classify(Ap, Am, fp, fm):
    A = Ap - Am
    if Ap > TAU and Am > TAU:
        return "mixed"
    if A > TAU and fp >= 0.5:
        return "drive"
    if A < -TAU and fm >= 0.5:
        return "brake"
    return "quiet"


def spearman(a, b, n_perm=20000):
    from scipy.stats import rankdata
    ra, rb = rankdata(a), rankdata(b)  # average ranks for ties
    rho = np.corrcoef(ra, rb)[0, 1]
    perm = np.array([np.corrcoef(ra, rng.permutation(rb))[0, 1] for _ in range(n_perm)])
    return float(rho), float((np.sum(perm >= rho) + 1) / (n_perm + 1))


# ------------------------------------------------------------------ audit
def audit(G_all, table):
    print("AUDIT")
    ok = {}
    allr, allv = np.concatenate([g["R"] for g in G_all.values()]), np.concatenate([g["vs"] for g in G_all.values()])
    worst = 0.0
    for g in G_all.values():
        _, Mdl = L["velocity_decode"](g["R"], g["vs"], g["R"])
        worst = max(worst, float(np.max(np.abs(Mdl / mdec_closed(g["R"], g["vs"]) - 1))))
    ok["A1"] = worst < 1e-10
    print(f"  A1 closed form = letter's velocity_decode at all {len(allr)} points: max rel diff {worst:.1e}  {'PASS' if ok['A1'] else 'FAIL'}")
    M = mdec_closed(allr, allv)
    gs = G * M / (allr * KPC) ** 2
    gt = (gs + np.sqrt(gs ** 2 + 4 * gs * A0)) / 2
    vback = np.sqrt(allr * KPC * gt) / 1e3
    rt = float(np.max(np.abs(vback / allv - 1)))
    ok["A2"] = rt < 1e-10
    print(f"  A2 round trip M_dec -> forward relation -> v: max rel diff {rt:.1e}  {'PASS' if ok['A2'] else 'FAIL'}")
    vs = L["diffraction_smooth"](L["m33_r_obs"], L["m33_v_obs"], frac=0.062)
    rdec = np.linspace(L["m33_r_obs"][0], L["m33_r_obs"][-1], 500)
    _, Mm33 = L["velocity_decode"](L["m33_r_obs"], vs, rdec)
    m33 = Mm33[-1] / MSUN
    ok["A3"] = f"{m33:.2e}" == "1.38e+10"
    print(f"  A3 M33 at 17 kpc from the letter's data and code path: {m33:.3e} Msun (published 1.38e10)  {'PASS' if ok['A3'] else 'FAIL'}")
    ok["A4"] = (G, A0, KPC, MSUN) == (6.674e-11, 1.2e-10, 3.086e19, 1.989e30)
    print(f"  A4 constants G={G}, a0={A0}, kpc={KPC}, Msun={MSUN}  {'PASS' if ok['A4'] else 'FAIL'}")
    lc = np.array([np.log10(g["Lstar"] / table[k]["L36"]) for k, g in G_all.items() if k in table])
    ok["A5"] = abs(np.median(lc)) < 0.05
    print(f"  A5 integrated 3.6um light / SPARC L[3.6]: median {np.median(lc):+.3f} dex (N={len(lc)})  {'PASS' if ok['A5'] else 'FAIL'}")
    ok["A6"] = True
    print("  A6 smoothing: the letter's diffraction_smooth, frac = 0.062, loaded from its source  PASS")
    return all(ok.values())


# ------------------------------------------------------------------ main
def main(rotmod_dir, table1, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    table = {}
    for line in open(table1):
        p = line.split()
        if len(p) > 17:
            table[p[0]] = dict(inc=float(p[5]), L36=float(p[7]) * 1e9, Q=int(p[17]))
    Gs = {}
    for f in sorted(glob.glob(os.path.join(rotmod_dir, "*_rotmod.dat"))):
        name = os.path.basename(f)[:-len("_rotmod.dat")]
        d = np.loadtxt(f, comments="#", ndmin=2)
        R, Vo, eV, Vg, SBd, SBb = d[:, 0], d[:, 1], d[:, 2], d[:, 3], d[:, 6], d[:, 7]
        vs = L["diffraction_smooth"](R, Vo, frac=0.062) if len(R) > 1 else Vo.copy()
        Gs[name] = dict(R=R, Vo=Vo, eV=eV, vs=vs, Vg=Vg, SBd=SBd, SBb=SBb,
                        Lstar=enclosed_light(R, SBd)[-1] + enclosed_light(R, SBb)[-1])
    if not audit(Gs, table):
        raise SystemExit("audit failed: no galaxies classified")

    rows, prof = [], []
    for name, g in Gs.items():
        R = g["R"]
        if len(R) < 3:
            continue
        r = R * KPC
        _, Mdec = L["velocity_decode"](R, g["vs"], R)
        Mlo_raw, Mlo, Mhi = L["M_dec_bounds"](R, g["vs"], g["eV"])
        Mgas = np.abs(g["Vg"]) * g["Vg"] * 1e6 * r / G
        res = {}
        for s in (0.8, 1.0, 1.2):
            Mstar = s * (0.5 * enclosed_light(R, g["SBd"]) + 0.7 * enclosed_light(R, g["SBb"])) * MSUN
            Mphot = Mstar + Mgas
            if np.any(Mphot <= 0):
                res[s] = None
                continue
            D = np.log10(Mdec / Mphot)
            Ap, Am = areas(R, D)
            fp, fm = float(np.mean(Mlo > Mphot)), float(np.mean(Mhi < Mphot))
            res[s] = dict(D=D, Ap=Ap, Am=Am, fp=fp, fm=fm, cls=classify(Ap, Am, fp, fm), Mphot=Mphot)
        base = res[1.0]
        if base is None:
            continue
        classes = {res[s]["cls"] if res[s] else None for s in res}
        robust = len(classes) == 1
        gobs = (g["vs"] * 1e3) ** 2 / r
        Rring = crossing(R, np.log(gobs / A0))
        Mphot = base["Mphot"]
        fin = (1.0 if gobs[-1] > A0 else 0.0) if Rring is None else float(np.clip(np.interp(Rring, R, Mphot) / Mphot[-1], 0, 1))
        inside = R < Rring if Rring else np.zeros_like(R, bool)
        m = table.get(name, {})
        rows.append(dict(galaxy=name, n=len(R), r_min=R[0], r_max=R[-1],
                         A_above=base["Ap"], A_below=base["Am"], A_net=base["Ap"] - base["Am"],
                         f_above=base["fp"], f_below=base["fm"], cls=base["cls"],
                         robust=robust, cls_robust=base["cls"] if robust else "uncertain",
                         gas_share=float(Mgas[-1] / Mphot[-1]), bulge=bool(np.any(g["SBb"] > 0)),
                         R_ring=Rring if Rring else float("nan"), f_in=fin,
                         D_in=float(np.mean(base["D"][inside])) if inside.any() else float("nan"),
                         D_out=float(np.mean(base["D"][~inside])) if (~inside).any() else float("nan"),
                         Q=m.get("Q", -1), inc=m.get("inc", float("nan"))))
        for i in range(len(R)):
            prof.append(dict(galaxy=name, r_kpc=R[i], v_obs=g["Vo"][i], v_smooth=g["vs"][i], e_v=g["eV"][i],
                             M_dec=Mdec[i] / MSUN, M_dec_lo=Mlo[i] / MSUN, M_dec_hi=Mhi[i] / MSUN,
                             M_phot=Mphot[i] / MSUN, M_gas=Mgas[i] / MSUN, Delta_dex=base["D"][i]))

    for fn, data in (("galaxy_summary.csv", rows), ("profiles.csv", prof)):
        with open(os.path.join(out_dir, fn), "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(data[0]))
            w.writeheader()
            for row in data:
                w.writerow({k: (f"{v:.6g}" if isinstance(v, float) else v) for k, v in row.items()})

    # -------------------------------------------------------------- report
    print(f"\nMEASURED: {len(rows)} galaxies, {len(prof)} radii")
    for lab, sel in (("all", rows), ("quality cut", [r for r in rows if r["Q"] in (1, 2) and r["inc"] >= 30 and r["n"] >= 5])):
        print(f"  {lab} (N={len(sel)}):")
        for c in ("drive", "quiet", "brake", "mixed"):
            n = sum(r["cls"] == c for r in sel); nr = sum(r["cls_robust"] == c for r in sel)
            print(f"    {c:6s} {n:3d} ({n / len(sel):.0%})   robust to M/L x0.8-1.2: {nr:3d}")
        print(f"    uncertain (class changes with M/L): {sum(r['cls_robust'] == 'uncertain' for r in sel)}")
        print(f"    median A_net {np.median([r['A_net'] for r in sel]):+.3f} dex, "
              f"median A_above {np.median([r['A_above'] for r in sel]):.3f}, median A_below {np.median([r['A_below'] for r in sel]):.3f}")

    q = [r for r in rows if r["Q"] in (1, 2) and r["inc"] >= 30 and r["n"] >= 5]
    print("\nH3  ring share versus net area A")
    res = {}
    for lab, sel in (("(a) all quality-cut", q), ("(b) not gas-dominated", [r for r in q if r["gas_share"] < 0.5]),
                     ("    no bulge", [r for r in q if not r["bulge"]]), ("    gas-dominated", [r for r in q if r["gas_share"] >= 0.5])):
        rho, p = spearman(np.array([r["f_in"] for r in sel]), np.array([r["A_net"] for r in sel]))
        res[lab] = (rho, p)
        print(f"  {lab:24s} N={len(sel):3d}  rho = {rho:+.2f}  one-sided p = {p:.4f}")
    h3 = all(res[k][0] > 0 and res[k][1] < 0.01 for k in ("(a) all quality-cut", "(b) not gas-dominated"))
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
    print(f"\n  Local (no pass condition): {len(loc)} galaxies contain the ring. Delta inside minus outside: "
          f"median {np.median(diff):+.3f} dex; inside higher in {np.mean(diff > 0):.0%}")

    # -------------------------------------------------------------- atlas
    try:
        import matplotlib
        import matplotlib.ticker
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_pdf import PdfPages
        byg = {}
        for p_ in prof:
            byg.setdefault(p_["galaxy"], []).append(p_)
        col = {"drive": "C2", "quiet": "0.4", "brake": "C3", "mixed": "C1"}
        with PdfPages(os.path.join(out_dir, "profile_atlas.pdf")) as pdf:
            names = [r["galaxy"] for r in rows]
            info = {r["galaxy"]: r for r in rows}
            for k in range(0, len(names), 20):
                fig, axs = plt.subplots(5, 4, figsize=(8.5, 11))
                for ax, nm in zip(axs.flat, names[k:k + 20]):
                    P = byg[nm]
                    rr = np.array([p_["r_kpc"] for p_ in P])
                    ax.loglog(rr, [p_["M_phot"] for p_ in P], "--", lw=1.2, color="k")
                    ax.loglog(rr, [p_["M_dec"] for p_ in P], "-", lw=1.2, color="C0")
                    ax.fill_between(rr, [p_["M_dec_lo"] for p_ in P], [p_["M_dec_hi"] for p_ in P], alpha=0.25)
                    i = info[nm]
                    if np.isfinite(i["R_ring"]):
                        ax.axvline(i["R_ring"], color="0.7", lw=0.8)
                    ax.set_title(f"{nm}  {i['cls']}  A={i['A_net']:+.2f}", fontsize=7, color=col[i["cls"]])
                    ax.tick_params(labelsize=5)
                    ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
                    ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
                for ax in list(axs.flat)[len(names[k:k + 20]):]:
                    ax.axis("off")
                fig.suptitle("SPARC: decoded M_dec(r) (solid, band = velocity error) vs photometric M_phot(r) (dashed); "
                             "grey line = ring x = 1", fontsize=7)
                fig.tight_layout(rect=(0, 0, 1, 0.98))
                pdf.savefig(fig)
                plt.close(fig)
        print(f"\nAtlas: {os.path.join(out_dir, 'profile_atlas.pdf')}")
    except ImportError:
        print("matplotlib not available: atlas skipped")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, "results"))
