#!/usr/bin/env python3
"""
Drive and brake by radius in eight classical dwarfs (method fixed in PROFILE_PREREGISTRATION.md).

  python profile_study.py GRAVSPHERE_DIR    (writes profile_bins.csv and prints the results)

GRAVSPHERE_DIR is a checkout of github.com/justinread/gravsphere (commit 09fa555), whose
Data/Walker_dwarfs/ holds Walker et al.'s star-by-star velocities and photometric members.
"""
import sys

import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar

G_PC = 4.30091e-3                    # pc (km/s)^2 / Msun
A0_PC = 1.2e-10 * 3.0857e16 / 1e6    # (km/s)^2 / pc
M_MW = 6e10
ARCMIN = np.pi / (180 * 60)
# file stem, catalogue name, distance used in gravsphere (kpc)
GALAXIES = [("for", "Fornax", 138.0), ("scl", "Sculptor", 86.0), ("car", "Carina", 105.0),
            ("sex", "Sextans", 86.0), ("dra", "Draco", 76.0), ("umi", "Ursa Minor", 76.0),
            ("leo1", "Leo I", 254.0), ("leo2", "Leo II", 233.0)]
CATALOGUE = "decode_sample.csv"
MIN_PER_BIN, MAX_BINS, NBOOT = 60, 10, 200
RNG = np.random.default_rng(2026)


def ml_dispersion(v, e, w):
    """weighted maximum-likelihood dispersion, mean fixed at the weighted mean"""
    vbar = np.sum(w * v) / np.sum(w)

    def nll(s):
        var = s * s + e * e
        return np.sum(w * (0.5 * np.log(var) + 0.5 * (v - vbar) ** 2 / var))

    return minimize_scalar(nll, bounds=(0.01, 60.0), method="bounded").x


def observed_profile(R, v, e, w):
    order = np.argsort(R)
    R, v, e, w = R[order], v[order], e[order], w[order]
    neff = w.sum()
    nb = int(min(MAX_BINS, max(3, np.floor(neff / MIN_PER_BIN))))
    cw = np.cumsum(w)
    edges_idx = [0] + [int(np.searchsorted(cw, neff * k / nb)) for k in range(1, nb)] + [len(R)]
    rows = []
    for a, b in zip(edges_idx[:-1], edges_idx[1:]):
        sl = slice(a, b)
        Rb, vb, eb, wb = R[sl], v[sl], e[sl], w[sl]
        s = ml_dispersion(vb, eb, wb)
        boots = []
        for _ in range(NBOOT):
            i = RNG.integers(0, len(Rb), len(Rb))
            boots.append(ml_dispersion(vb[i], eb[i], wb[i]))
        rows.append((np.sum(wb * Rb) / np.sum(wb), s, np.std(boots), wb.sum()))
    return pd.DataFrame(rows, columns=["R", "sigma", "err", "neff"])


def nu_law(y):
    return 0.5 + np.sqrt(0.25 + 1.0 / y)


def quiet_profile(Rs, M, a, beta=0.0, gNe=0.0):
    """projected isotropic-or-constant-beta Jeans dispersion for a Plummer tracer of mass M, scale a,
    in the quiet GFD field g = nu((g_N + g_Ne)/a0) g_N"""
    r = np.logspace(np.log10(a) - 3, np.log10(a) + 3, 3000)
    nu_r = 3 / (4 * np.pi * a ** 3) * (1 + (r / a) ** 2) ** -2.5
    gN = G_PC * M * r / (r * r + a * a) ** 1.5
    g = nu_law((gN + gNe) / A0_PC) * gN
    integrand = r ** (2 * beta) * nu_r * g
    # nu sigma_r^2 (r) = r^-2beta int_r^inf r'^2beta nu g dr'
    cum = np.concatenate([np.cumsum(((integrand[1:] + integrand[:-1]) / 2 * np.diff(r))[::-1])[::-1], [0.0]])
    nus2 = cum * r ** (-2 * beta)
    out = []
    for R in Rs:
        m = r > R * (1 + 1e-9)
        rr = r[m]
        f = (1 - beta * R * R / (rr * rr)) * nus2[m] * rr / np.sqrt(rr * rr - R * R)
        Sig = 1 / (np.pi * a * a) * (1 + (R / a) ** 2) ** -2
        # the integrable singularity at r = R: substitute r = R cosh t on a fine grid
        t = np.linspace(1e-6, np.arccosh(rr.max() / R), 4000)
        rt = R * np.cosh(t)
        nus2_t = np.interp(rt, r, nus2)
        ft = (1 - beta / np.cosh(t) ** 2) * nus2_t * R * np.cosh(t)
        val = 2 * np.trapezoid(ft, t)
        out.append(np.sqrt(val / Sig))
    return np.array(out)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    gdir = sys.argv[1]
    cat = pd.read_csv(CATALOGUE)
    allbins = []
    print("Delta(R) = log10[sigma_obs^4 / sigma_quiet^4]: positive = drive, negative = brake")
    print("Shape fit Delta = c0 + c1 log10(R/R_h); H (drain in the core): c1 < 0\n")
    summary = []
    for stem, name, D in GALAXIES:
        k = np.genfromtxt(f"{gdir}/Data/Walker_dwarfs/{stem}_justin1_spec.dat")
        got = k[:, 6] != 0
        R = k[got, 4] * D * 1000 * ARCMIN
        v, e, w = k[got, 6], k[got, 7], k[got, 15]
        keep = w > 0.05
        prof = observed_profile(R[keep], v[keep], e[keep], w[keep])
        row = cat[cat["name"] == name].iloc[0]
        L = 10 ** (-0.4 * (row["M_V"] - 4.83))
        a = row["rhalf_sph_physical"]
        gNe = G_PC * M_MW / (row["distance_host"] * 1000) ** 2
        res = {"name": name}
        for label, ml, beta, ge in (("own", 2.0, 0.0, 0.0), ("host", 2.0, 0.0, gNe), ("own ML1", 1.0, 0.0, 0.0),
                                    ("own ML3", 3.0, 0.0, 0.0), ("own b-0.3", 2.0, -0.3, 0.0),
                                    ("own b+0.3", 2.0, 0.3, 0.0)):
            sq = quiet_profile(prof["R"].values, ml * L, a, beta, ge)
            delta = 4 * np.log10(prof["sigma"].values / sq)
            derr = 4 * prof["err"].values / prof["sigma"].values / np.log(10)
            x = np.log10(prof["R"].values / a)
            W = 1 / derr ** 2
            A = np.vstack([np.ones_like(x), x]).T
            cov = np.linalg.inv(A.T @ (A * W[:, None]))
            c = cov @ (A.T @ (W * delta))
            res[label] = (c[0], c[1], np.sqrt(cov[1, 1]))
            if label == "own":
                for i in range(len(prof)):
                    allbins.append((name, prof["R"][i], prof["R"][i] / a, prof["sigma"][i], prof["err"][i],
                                    prof["neff"][i], sq[i], delta[i], derr[i]))
                print(f"{name}: L = {L:.2e} Lsun, R_h = {a:.0f} pc, {len(prof)} bins")
                print(f"   {'R [pc]':>7s} {'R/R_h':>6s} {'sig_obs':>8s} {'+-':>5s} {'sig_quiet':>9s} {'Delta':>6s} {'+-':>5s}")
                for i in range(len(prof)):
                    print(f"   {prof['R'][i]:7.0f} {prof['R'][i] / a:6.2f} {prof['sigma'][i]:8.2f} {prof['err'][i]:5.2f} "
                          f"{sq[i]:9.2f} {delta[i]:+6.2f} {derr[i]:5.2f}")
        summary.append(res)
        c0, c1, s1 = res["own"]
        print(f"   shape: c0 = {c0:+.2f}, c1 = {c1:+.2f} +- {s1:.2f}\n")
    print("Summary of the slope c1 (H: c1 < 0)")
    print(f"   {'galaxy':12s} " + " ".join(f"{k:>15s}" for k in ("own", "host", "own ML1", "own ML3", "own b-0.3", "own b+0.3")))
    for res in summary:
        print(f"   {res['name']:12s} " + " ".join(f"{res[k][1]:+6.2f} +- {res[k][2]:4.2f}" for k in
                                                ("own", "host", "own ML1", "own ML3", "own b-0.3", "own b+0.3")))
    for k in ("own", "host", "own b-0.3", "own b+0.3"):
        neg = sum(r_[k][1] + 2 * r_[k][2] < 0 for r_ in summary)
        nonneg = sum(r_[k][1] - 2 * r_[k][2] >= 0 for r_ in summary)
        print(f"   {k:10s}: c1 < 0 at 2 sigma in {neg}/8; c1 >= 0 at 2 sigma in {nonneg}/8")
    pd.DataFrame(allbins, columns=["galaxy", "R_pc", "R_over_Rh", "sigma_obs", "sigma_err", "neff", "sigma_quiet",
                                   "Delta", "Delta_err"]).to_csv("profile_bins.csv", index=False)


if __name__ == "__main__":
    main()
