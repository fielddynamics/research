#!/usr/bin/env python3
"""
Network constitutive laws: GFD's mu(x) as a circuit, and what a Sierpinski
network does to it.

Construction. A network of unit series edges with a shunt impedance x from
every node to ground. Drive one corner node through a unit source resistance.
The voltage left after the source resistance is

    mu(x) = Z / (1 + Z),

where Z is the driving-point impedance seen at the corner.

    single node              ->  Z = x,                    mu = x/(1+x)   (N = 1)
    semi-infinite chain      ->  Z = x || (1 + Z),         mu = eq. 23    (N = 2)
    Sierpinski gasket        ->  exact self-similar decimation, k = 3
    Sierpinski tetrahedron   ->  exact self-similar decimation, k = 4

Checks (all exact or high precision):
  A. Transmission-line dictionary: s = (x-1)/(x+1) is the reflection
     coefficient; mu = (1+s)/2; 4 mu(1-mu) = 1 - s^2; x -> 1/x sends s -> -s.
  B. The chain reproduces the paper's N = 2 law; mu(1) = 1/phi^2.
  C. Decimation agrees with brute-force meshes to machine precision.
  D. Deep field: mu = x - c x^2 with c = 1 + (edges at the corner).
  E. Newtonian side: Z ~ x^(1 - d_s/2), d_s the spectral dimension.
  F. Upper bound: Z <= x, so mu_net(x) <= x/(1+x); Rayleigh ordering.
  G. Fit to the empirical radial acceleration relation; excess at Saturn.

Writes network_constitutive_laws.png.

Stephen Nelson, Gravity Field Dynamics
"""
import itertools as it
import sys

import mpmath as mp
import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spla
import sympy as sp
from scipy.interpolate import interp1d
from scipy.optimize import brentq, minimize_scalar

PASS = FAIL = 0


def check(name, ok, detail=""):
    global PASS, FAIL
    PASS += bool(ok)
    FAIL += not ok
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"\n         {detail}" if detail else ""))


def mu1(x):
    return x / (1 + x)


def mu2(x):
    u = np.sqrt(1 + 4 * x)
    return (u - 1) / (u + 1)


# ---------------------------------------------------------------- meshes
def gasket_edges(n):
    E = set()

    def tri(a, b, s):
        if s == 1:
            p = [(a, b), (a + 1, b), (a, b + 1)]
            for i, j in ((0, 1), (0, 2), (1, 2)):
                E.add(tuple(sorted((p[i], p[j]))))
            return
        h = s // 2
        tri(a, b, h); tri(a + h, b, h); tri(a, b + h, h)

    tri(0, 0, 2 ** n)
    return E


def tetra_edges(n):
    E = set()

    def tet(a, b, c, s):
        if s == 1:
            p = [(a, b, c), (a + 1, b, c), (a, b + 1, c), (a, b, c + 1)]
            for i, j in it.combinations(range(4), 2):
                E.add(tuple(sorted((p[i], p[j]))))
            return
        h = s // 2
        for o in ((0, 0, 0), (h, 0, 0), (0, h, 0), (0, 0, h)):
            tet(a + o[0], b + o[1], c + o[2], h)

    tet(0, 0, 0, 2 ** n)
    return E


def chain_edges(n):
    return {((i,), (i + 1,)) for i in range(n)}


class Mesh:
    def __init__(self, E, corner):
        nodes = sorted({u for e in E for u in e})
        idx = {u: i for i, u in enumerate(nodes)}
        r, c = [], []
        for u, v in E:
            r += [idx[u], idx[v]]
            c += [idx[v], idx[u]]
        A = sps.csr_matrix((np.ones(len(r)), (r, c)), shape=(len(nodes),) * 2)
        self.L = (sps.diags(np.asarray(A.sum(1)).ravel()) - A).tocsc()
        self.N, self.k = len(nodes), idx[corner]

    def Z(self, x):
        M = (self.L + sps.identity(self.N, format="csc") / x).tocsc()
        b = np.zeros(self.N)
        b[self.k] = 1.0
        return spla.spsolve(M, b)[self.k]


# ---------------------------------------------------------------- decimation
def _schur(M, keep, inv):
    drop = [i for i in range(len(M)) if i not in keep]
    A = [[M[i][j] for j in keep] for i in keep]
    B = [[M[i][j] for j in drop] for i in keep]
    C = [[M[i][j] for j in drop] for i in drop]
    return inv(A, B, C)


def Z_decimated(k, x, prec=None, levels=400):
    """Driving-point impedance at a corner of the infinite Sierpinski simplex
    network (k = 3 gasket, k = 4 tetrahedron). R is the boundary matrix of a
    level-n piece without corner shunts; level n+1 glues k copies at the
    midpoints. prec=None uses float64, otherwise mpmath at that many digits."""
    if prec is None:
        lib_eye, lib_zeros = np.eye, lambda n: np.zeros((n, n))
        g = 1.0 / x
        R = k * np.eye(k) - np.ones((k, k))

        def schur(M, keep):
            drop = [i for i in range(M.shape[0]) if i not in keep]
            A, B, C = M[np.ix_(keep, keep)], M[np.ix_(keep, drop)], M[np.ix_(drop, drop)]
            return A - B @ np.linalg.solve(C, B.T)
        tol = 1e-15
    else:
        mp.mp.dps = prec
        lib_eye, lib_zeros = mp.eye, lambda n: mp.zeros(n, n)
        g = 1 / mp.mpf(x)
        R = k * mp.eye(k) - mp.ones(k, k)

        def schur(M, keep):
            drop = [i for i in range(M.rows) if i not in keep]
            A = mp.matrix([[M[i, j] for j in keep] for i in keep])
            B = mp.matrix([[M[i, j] for j in drop] for i in keep])
            C = mp.matrix([[M[i, j] for j in drop] for i in drop])
            return A - B * mp.inverse(C) * B.T
        tol = mp.mpf(10) ** (-(prec // 2))
    pairs = list(it.combinations(range(k), 2))
    mid = {p: k + i for i, p in enumerate(pairs)}
    nn = k + len(pairs)
    prev = None
    for _ in range(levels):
        M = lib_zeros(nn)
        for i in range(k):
            loc = [i] + [mid[tuple(sorted((i, j)))] for j in range(k) if j != i]
            for a, u in enumerate(loc):
                for b, v in enumerate(loc):
                    M[u, v] += R[a, b]
        for m in mid.values():
            M[m, m] += g
        R = schur(M, list(range(k)))
        Z = 1 / schur(R + g * lib_eye(k), [0])[0, 0]
        if prev is not None and abs(Z - prev) <= tol * abs(Z):
            return Z
        prev = Z
    raise RuntimeError("decimation did not converge")


def main():
    print("\nNETWORK CONSTITUTIVE LAWS\n")

    print("A. Transmission-line dictionary (symbolic)")
    x = sp.symbols("x", positive=True)
    s = (x - 1) / (x + 1)
    m = x / (x + 1)
    check("mu = (1+s)/2: the load voltage over the source EMF", sp.simplify(m - (1 + s) / 2) == 0)
    check("4 mu (1-mu) = 1 - s^2: delivered power, maximal at x = 1",
          sp.simplify(4 * m * (1 - m) - (1 - s ** 2)) == 0)
    check("x -> 1/x sends s -> -s: a quarter-wave transformer", sp.simplify(s.subs(x, 1 / x) + s) == 0)
    check("f(4,s) = 17 + 4s = (21x+13)/(x+1)", sp.simplify(17 + 4 * s - (21 * x + 13) / (x + 1)) == 0)

    print("\nB. The chain is the paper's N = 2 law")
    ch = Mesh(chain_edges(4000), (0,))
    err = max(abs(mu1(ch.Z(v)) - mu2(v)) for v in (0.01, 0.1, 1, 10, 100, 1000))
    check("chain mu equals eq. 23 to 1e-10", err < 1e-10, f"max deviation {err:.1e}")
    check("chain mu(1) = 1/phi^2", abs(mu1(ch.Z(1.0)) - (3 - 5 ** 0.5) / 2) < 1e-12)

    print("\nC. Exact decimation against brute-force meshes")
    for k, builder, corner, n in ((3, gasket_edges, (0, 0), 10), (4, tetra_edges, (0, 0, 0), 8)):
        mesh = Mesh(builder(n), corner)
        rel = max(abs(Z_decimated(k, v) / mesh.Z(v) - 1) for v in (0.1, 1, 10, 100))
        check(f"k={k}: decimation = level-{n} mesh ({mesh.N} nodes)", rel < 1e-12, f"max relative deviation {rel:.1e}")

    print("\nD. Deep field: mu = x - c x^2, c = 1 + (edges at the corner)")
    xs = 1e-4
    cs = {"single node": (mu1(xs), 1), "chain": (mu2(xs), 2)}
    for k in (3, 4):
        Z = Z_decimated(k, xs)
        cs[f"k={k}"] = (mu1(Z), k)
    for name, (mv, c) in cs.items():
        cf = (xs - mv) / xs ** 2
        check(f"{name}: c = {c}", abs(cf - c) < 0.01 * c, f"measured {cf:.4f}")

    print("\nE. Newtonian side: Z ~ x^(1 - d_s/2)  (60-digit decimation)")
    tails = {}
    grid = [mp.mpf(10) ** (e / 4) for e in range(16, 65)]
    for k, ds in ((3, 2 * np.log(3) / np.log(5)), (4, 2 * np.log(4) / np.log(6))):
        lz = np.array([float(mp.log(Z_decimated(k, v, prec=60))) for v in grid])
        lx = np.array([float(mp.log(v)) for v in grid])
        th, c0 = np.polyfit(lx, lz, 1)
        tails[k] = (th, np.exp(c0))
        check(f"k={k}: exponent {th:.5f} vs 1 - d_s/2 = {1 - ds / 2:.5f}", abs(th - (1 - ds / 2)) < 1e-4,
              f"d_s = {ds:.4f}; prefactor {np.exp(c0):.3f}")

    print("\nF. Upper bound and ordering")
    X = np.logspace(-4, 5, 200)
    Zg = np.array([Z_decimated(3, v) for v in X])
    Zt = np.array([Z_decimated(4, v) for v in X])
    mg, mt, m1, m2 = mu1(Zg), mu1(Zt), mu1(X), mu2(X)
    check("Z <= x for the gasket and the tetrahedron", (Zg <= X * (1 + 1e-12)).all() and (Zt <= X * (1 + 1e-12)).all())
    check("mu_single >= mu_chain >= mu_gasket >= mu_tetra everywhere",
          (m1 >= m2 - 1e-12).all() and (m2 >= mg - 1e-12).all() and (mg >= mt - 1e-12).all())

    print("\nG. Radial acceleration relation and Saturn")
    lxg = np.linspace(-6, 5, 441)
    laws = {"N=1 single node": mu1, "N=2 chain": mu2}
    for k, name in ((3, "gasket"), (4, "Sierpinski tetrahedron")):
        f = interp1d(lxg, np.log([Z_decimated(k, v) for v in 10 ** lxg]), kind="cubic")
        th, c = tails[k]

        def law(v, f=f, th=th, c=c):
            v = np.asarray(v, float)
            Z = np.where(v <= 1e5, np.exp(f(np.clip(np.log10(v), -6, 5))), c * v ** th)
            return Z / (1 + Z)
        laws[name] = law
    gbar = np.logspace(-12, -8.5, 120)
    gdag = 1.20e-10
    rar = gbar / (1 - np.exp(-np.sqrt(gbar / gdag)))  # McGaugh, Lelli & Schombert (2016)
    table = {}
    for name, law in laws.items():
        def gobs(a0):
            return np.array([brentq(lambda g: g * law(g / a0) - gb, gb, gb * 1e4) for gb in gbar])

        def err(la):
            return np.sqrt(np.mean((np.log10(gobs(10 ** la)) - np.log10(rar)) ** 2))
        r = minimize_scalar(err, bounds=(-11.5, -9), method="bounded")
        sat = 1 / law(6.5e-5 / 1.2e-10) - 1
        table[name] = (float(law(1.0)), 10 ** r.x, r.fun, float(sat))
        print(f"  {name:24s} mu(1)={float(law(1.0)):.4f}  best a0={10 ** r.x:.2e}  "
              f"rms vs RAR={r.fun:.3f} dex  excess at Saturn={float(sat):.1e}")
    check("RAR misfit grows with the network's spectral dimension",
          np.all(np.diff([v[2] for v in table.values()]) > 0))

    draw(X, m1, m2, mg, mt, tails)
    print(f"\n  Passed {PASS}, failed {FAIL}\n")
    return FAIL == 0


def draw(X, m1, m2, mg, mt, tails):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    col = {"m1": "#2a78d6", "m2": "#eb6834", "mg": "#1baf7a", "mt": "#6250d6"}
    lab = {"m1": "N = 1, single node", "m2": "N = 2, chain", "mg": "Sierpiński gasket",
           "mt": "Sierpiński tetrahedron"}
    sty = {"m1": "-", "m2": "--", "mg": ":", "mt": "-."}
    data = {"m1": m1, "m2": m2, "mg": mg, "mt": mt}
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.4))
    for k in data:
        ax[0].semilogx(X, data[k], sty[k], color=col[k], lw=2, label=lab[k])
        ax[1].loglog(X, 1 - data[k], sty[k], color=col[k], lw=2, label=lab[k])
    ax[0].axvline(1, color="#c3c2b7", lw=1)
    ax[0].set(xlabel="x = g / a₀", ylabel="μ(x)", ylim=(0, 1), xlim=(1e-3, 1e5),
              title="A. The four laws (all bounded above by x/(1+x))")
    ax[0].legend(frameon=False, fontsize=9, loc="upper left")
    ax[1].set(xlabel="x = g / a₀", ylabel="1 − μ(x)", xlim=(1, 1e5), ylim=(1e-5, 1.2),
              title="B. Newtonian-side tails, 1 − μ ∝ x^−(1 − d_s/2)")
    for key, xy, text in (("mt", (8e3, 0.32), f"slope −{tails[4][0]:.3f}"),
                          ("mg", (8e3, 0.03), f"slope −{tails[3][0]:.3f}"),
                          ("m2", (8e3, 0.0013), "slope −1/2"),
                          ("m1", (1.5e3, 8e-5), "slope −1")):
        ax[1].text(*xy, text, color=col[key], fontsize=9)
    for a in ax:
        a.grid(color="#e1e0d9", lw=0.6)
        for sp_ in ("top", "right"):
            a.spines[sp_].set_visible(False)
    fig.tight_layout()
    fig.savefig("network_constitutive_laws.png", dpi=160)
    print("\n  Wrote network_constitutive_laws.png")


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
