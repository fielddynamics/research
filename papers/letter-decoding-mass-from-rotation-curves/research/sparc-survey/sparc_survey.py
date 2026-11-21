#!/usr/bin/env python3
"""
The decoding-mass letter's pipeline, run on every SPARC galaxy.

For each galaxy:
  1. smooth the observed rotation curve exactly as the letter does (Gaussian, 6.2% of the radial span);
  2. decode the effective mass M_dec(r) = r v^4 / [G (a0 r + v^2)] over the observed range (letter Eq. 5);
  3. build the photometric enclosed mass M_phot(r) from SPARC Table 1 exactly as the letter does for
     Camelopardalis B: disk M = 0.5 L[3.6] with scale R_disk, gas M = 1.33 M_HI with scale R_HI/3,
     both exponential;
  4. measure the area between the two curves over the observed range, as a fraction of the area under
     the photometric curve: above = drive, below = brake.

The smoothing and decode functions are read directly from the letter's figures/generate_letter_figures.py,
without running that script (which would rewrite the letter's figures).

  python sparc_survey.py ROTMOD_DIR
ROTMOD_DIR holds SPARC's Rotmod_LTG files (Lelli et al. 2016; astroweb.cwru.edu/SPARC/).
"""
import ast
import csv
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LETTER = os.path.join(HERE, "..", "..")
REPO = os.path.join(LETTER, "..", "..")
FIG_SCRIPT = os.path.join(LETTER, "figures", "generate_letter_figures.py")
TABLE1 = os.path.join(REPO, "papers", "07-dual-tetrad-topology-field-origin", "v7", "python",
                      "sparc_tully_fisher_table.dat")
QUIET = 0.05            # |net area| <= 5% of the photometric area is labelled quiet (a convenience label)


def letter_functions():
    """Load the letter's constants and its smoothing and decode functions, nothing else."""
    tree = ast.parse(open(FIG_SCRIPT).read())
    keep = []
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)) and "matplotlib" not in ast.dump(node):
            keep.append(node)
        elif isinstance(node, ast.Assign) and all(isinstance(t, ast.Name) and t.id in ("G", "A0", "MSUN", "KPC")
                                                for t in node.targets):
            keep.append(node)
        elif isinstance(node, ast.FunctionDef) and node.name in ("diffraction_smooth", "velocity_decode"):
            keep.append(node)
    ns = {}
    exec(compile(ast.Module(body=keep, type_ignores=[]), FIG_SCRIPT, "exec"), ns)
    return ns


def table1():
    """SPARC Table 1 (Lelli et al. 2016): name -> (L[3.6] in Lsun, R_disk kpc, M_HI in Msun, R_HI kpc, quality)."""
    out = {}
    for line in open(TABLE1):
        p = line.split()
        if len(p) >= 18:
            out[p[0]] = (float(p[7]) * 1e9, float(p[11]), float(p[13]) * 1e9, float(p[14]), int(p[17]))
    return out


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    rot = sys.argv[1]
    L = letter_functions()
    smooth, decode, MSUN, KPC = L["diffraction_smooth"], L["velocity_decode"], L["MSUN"], L["KPC"]
    rows = []
    for name, (lum, rd, mhi, rhi, q) in sorted(table1().items()):
        f = os.path.join(rot, f"{name}_rotmod.dat")
        if not os.path.exists(f):
            continue
        a = np.loadtxt(f, comments="#")
        r, v, vbul = a[:, 0], a[:, 1], a[:, 5]
        m = (r > 0) & (v > 0)
        r, v, vbul = r[m], v[m], vbul[m]
        if len(r) < 4:
            continue
        flags = []
        if np.any(vbul > 0):
            flags.append("bulge")            # Table 1 gives only the total L[3.6]: treated as disk
        if mhi > 0 and rhi <= 0:
            flags.append("no_R_HI")          # gas cannot be built the letter's way
        mdisk, mgas = 0.5 * lum * MSUN, 1.33 * mhi * MSUN
        rgas = rhi / 3 * KPC if rhi > 0 else None

        def m_phot(rm):
            xd = rm / (rd * KPC)
            out = mdisk * (1 - (1 + xd) * np.exp(-xd))
            if mgas > 0 and rgas:
                xg = rm / rgas
                out = out + mgas * (1 - (1 + xg) * np.exp(-xg))
            return out

        rdec = np.linspace(r[0], r[-1], 500)
        _, mdec = decode(r, smooth(r, v), rdec)
        mp = m_phot(rdec * KPC)
        dm = mdec - mp
        norm = np.trapezoid(mp, rdec)
        net = np.trapezoid(dm, rdec) / norm
        rows.append({"galaxy": name, "quality": q, "flags": "+".join(flags), "n_points": len(r),
                     "r_min_kpc": round(r[0], 3), "r_max_kpc": round(r[-1], 3),
                     "area_above": round(np.trapezoid(np.clip(dm, 0, None), rdec) / norm, 4),
                     "area_below": round(np.trapezoid(np.clip(-dm, 0, None), rdec) / norm, 4),
                     "net_area": round(net, 4),
                     "Mdec_over_Mphot_outer": round(mdec[-1] / mp[-1], 4),
                     "Delta_M_eff_outer_Msun": f"{(mp[-1] - mdec[-1]) / MSUN:.4e}",
                     "reading": "drive" if net > QUIET else "brake" if net < -QUIET else "quiet"})
    with open(os.path.join(HERE, "sparc_survey_results.csv"), "w", newline="") as fo:
        w = csv.DictWriter(fo, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    def summary(sel, title):
        net = np.array([x["net_area"] for x in sel])
        c = [x["reading"] for x in sel]
        print(f"{title}\n   N = {len(sel)}: quiet {c.count('quiet')}, drive {c.count('drive')}, brake {c.count('brake')}; "
              f"median net area {np.median(net):+.1%}, 16-84%: {np.percentile(net, 16):+.1%} to {np.percentile(net, 84):+.1%}")

    camb = [x for x in rows if x["galaxy"] == "CamB"][0]
    print(f"Check against the letter: CamB Delta M_eff at the last radius = {camb['Delta_M_eff_outer_Msun']} Msun "
          f"(letter Fig. 2d: 4.03e7), net area {camb['net_area']:+.1%}\n")
    exact = [x for x in rows if not x["flags"]]
    summary(rows, "All galaxies")
    summary(exact, "The letter's recipe exactly (no bulge, R_HI catalogued)")
    summary([x for x in exact if x["quality"] <= 2], "   ... quality 1-2 only")
    summary([x for x in rows if "bulge" in x["flags"]], "Galaxies with a bulge (all L[3.6] treated as disk: approximate)")
    print(f"\nFlagged: {sum('bulge' in x['flags'] for x in rows)} with a bulge, "
          f"{sum('no_R_HI' in x['flags'] for x in rows)} without a catalogued R_HI")
    good = sorted([x for x in exact if x["quality"] <= 2], key=lambda x: x["net_area"])
    print("\nStrongest brake (letter recipe, quality 1-2): " + ", ".join(f"{x['galaxy']} {x['net_area']:+.0%}" for x in good[:8]))
    print("Strongest drive (letter recipe, quality 1-2): " + ", ".join(f"{x['galaxy']} {x['net_area']:+.0%}" for x in good[::-1][:8]))
    print("Quiet (letter recipe, quality 1-2): " + ", ".join(x["galaxy"] for x in good if x["reading"] == "quiet"))


if __name__ == "__main__":
    main()
