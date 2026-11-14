"""
SPARC checks for the hourglass reading of Letter 3's figure.

Hypotheses fixed before the data were examined:
  H1  The white ring (x = g_obs/a0 = 1) is the bulge-disk boundary: in galaxies with a
      bulge, the radius where bulge and disk contribute equally to g_bar lies at the ring.
      Pass: median |log10(R_bd/R_ring)| < 0.15 dex, and the ring predicts R_bd better than
      the baseline R_bd = 2.2 R_disk (the peak of an exponential disk's rotation curve).
  H2  Drive and brake follow the bulge: the more of the galaxy lies inside the ring, the
      more it drives. Drive/brake measure as in research/bimond-gfd/04: median over the
      outer half of log10(M_dec/M_bar) with g_dec = g_obs^2/(a0 + g_obs).
      Pass: positive rank correlation with the inside-ring mass fraction, p < 0.01,
      and it survives removing galaxies with bulges (the fixed bulge M/L could fake it).

Data: SPARC mass models (Lelli, McGaugh & Schombert 2016), one *_rotmod.dat per galaxy,
and SPARC table1 for quality, inclination and disk scale length.
Usage: python check_ring_bulge_sparc.py ROTMOD_DIR TABLE1_PATH
Stellar M/L: 0.5 (disk) and 0.7 (bulge) at 3.6 micron, as in the RAR letter.
"""
from __future__ import annotations

import glob
import os
import sys

import numpy as np

A0 = 1.2e-10
KPC = 3.0857e19
UPS_D, UPS_B = 0.5, float(os.environ.get("UPS_BULGE", 0.7))
rng = np.random.default_rng(2026)


def load(rotmod_dir, table1):
    T = {}
    for line in open(table1):
        p = line.split()
        if len(p) > 17:
            T[p[0]] = dict(inc=float(p[5]), Rdisk=float(p[11]), Q=int(p[17]))
    G = {}
    for f in sorted(glob.glob(os.path.join(rotmod_dir, "*_rotmod.dat"))):
        name = os.path.basename(f)[:-len("_rotmod.dat")]
        d = np.loadtxt(f, comments="#", ndmin=2)
        R, Vo, Vg, Vd, Vb = d[:, 0], d[:, 1], d[:, 3], d[:, 4], d[:, 5]
        r = R * KPC
        G[name] = dict(R=R, gobs=(Vo * 1e3) ** 2 / r,
                       gg=np.abs(Vg) * Vg * 1e6 / r, gd=UPS_D * Vd ** 2 * 1e6 / r,
                       gb=UPS_B * Vb ** 2 * 1e6 / r, meta=T.get(name))
    return G


def crossing(R, f):
    """First radius where f changes sign from + to - (log-linear interpolation in R)."""
    for i in range(len(R) - 1):
        if f[i] > 0 >= f[i + 1]:
            t = f[i] / (f[i] - f[i + 1])
            return float(np.exp(np.log(R[i]) + t * (np.log(R[i + 1]) - np.log(R[i]))))
    return None


def spearman(a, b, n_perm=20000):
    ra, rb = np.argsort(np.argsort(a)), np.argsort(np.argsort(b))
    rho = np.corrcoef(ra, rb)[0, 1]
    perm = np.array([np.corrcoef(ra, rng.permutation(rb))[0, 1] for _ in range(n_perm)])
    return rho, (np.sum(perm >= rho) + 1) / (n_perm + 1)


def main(rotmod_dir, table1):
    G = load(rotmod_dir, table1)
    good = {k: g for k, g in G.items() if g["meta"] and g["meta"]["Q"] <= 2
            and g["meta"]["inc"] >= 30 and len(g["R"]) >= 5}
    print(f"Galaxies: {len(G)} total, {len(good)} with Q <= 2, inc >= 30 deg, >= 5 points\n")

    # ---------------- H1
    print("H1  ring (g_obs = a0) versus bulge-disk boundary (g_bulge = g_disk)")
    rows = []
    for k, g in good.items():
        if not np.any(g["gb"] > 0):
            continue
        Rbd = crossing(g["R"], np.log(np.maximum(g["gb"], 1e-30)) - np.log(np.maximum(g["gd"], 1e-30)))
        Rring = crossing(g["R"], np.log(g["gobs"] / A0))
        rows.append((k, Rbd, Rring, 2.2 * g["meta"]["Rdisk"]))
    both = [r for r in rows if r[1] and r[2]]
    print(f"  galaxies with a bulge: {len(rows)}; with both crossings inside the data: {len(both)}")
    print(f"  no bulge-disk crossing in data: {sum(1 for r in rows if not r[1])}; "
          f"no ring in data: {sum(1 for r in rows if not r[2])}")
    if both:
        lr = np.array([np.log10(r[1] / r[2]) for r in both])
        lb = np.array([np.log10(r[1] / r[3]) for r in both])
        print(f"  log10(R_bd / R_ring):      median {np.median(lr):+.2f}, median |.| {np.median(np.abs(lr)):.2f} dex")
        print(f"  log10(R_bd / 2.2 R_disk):  median {np.median(lb):+.2f}, median |.| {np.median(np.abs(lb)):.2f} dex")
        for k, Rbd, Rring, Rb in sorted(both, key=lambda r: r[2]):
            print(f"    {k:12s} R_bd = {Rbd:6.2f} kpc   R_ring = {Rring:6.2f} kpc   2.2 R_d = {Rb:6.2f} kpc")
        h1 = np.median(np.abs(lr)) < 0.15 and np.median(np.abs(lr)) < np.median(np.abs(lb))
        print(f"  H1: {'PASS' if h1 else 'FAIL'}\n")

    # ---------------- H2
    print("H2  drive/brake versus share of the galaxy inside the ring")
    L, fin, hasb = [], [], []
    for k, g in good.items():
        gbar = g["gg"] + g["gd"] + g["gb"]
        if np.any(gbar <= 0):
            continue
        n = len(g["R"])
        outer = np.argsort(g["R"])[n // 2:]
        gdec = g["gobs"] ** 2 / (A0 + g["gobs"])
        L.append(np.median(np.log10(gdec[outer] / gbar[outer])))
        Mbar = gbar * (g["R"] * KPC) ** 2                     # G M_bar(<r), spherical estimate
        Rring = crossing(g["R"], np.log(g["gobs"] / A0))
        if Rring is None:
            fin.append(1.0 if g["gobs"][-1] > A0 else 0.0)
        else:
            fin.append(float(np.interp(Rring, g["R"], Mbar) / Mbar[-1]))
        hasb.append(bool(np.any(g["gb"] > 0)))
    L, fin, hasb = np.array(L), np.clip(np.array(fin), 0, 1), np.array(hasb)
    print(f"  N = {len(L)}; median log10(M_dec/M_bar) = {np.median(L):+.3f}; "
          f"drives (> +0.1 dex) {np.mean(L > 0.1):.2f}, brakes (< -0.1 dex) {np.mean(L < -0.1):.2f}")
    for lab, sel in [("all", np.ones_like(hasb)), ("no bulge", ~hasb), ("with bulge", hasb)]:
        if sel.sum() >= 8:
            rho, p = spearman(fin[sel], L[sel])
            print(f"  {lab:10s} N = {sel.sum():3d}  Spearman rho(f_in, drive) = {rho:+.2f}  one-sided p = {p:.4f}")
    rho_all, p_all = spearman(fin, L)
    rho_nb, p_nb = spearman(fin[~hasb], L[~hasb])
    h2 = rho_all > 0 and p_all < 0.01 and rho_nb > 0 and p_nb < 0.01
    print(f"  H2: {'PASS' if h2 else 'FAIL'}")
    for lab, s in [("no ring in data, all outside (f_in = 0)", fin == 0),
                   ("ring inside the data, 0 < f_in < 1", (fin > 0) & (fin < 1)),
                   ("all inside the ring (f_in = 1)", fin == 1)]:
        if s.sum():
            print(f"    {lab:42s} N = {s.sum():3d}, median drive {np.median(L[s]):+.3f}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
