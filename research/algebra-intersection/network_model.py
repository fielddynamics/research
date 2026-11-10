"""
network_model.py
================

Computes the pre-registered junction-network model of NETWORK_MODEL_PREREG.md
exactly (sympy integers).  No parameter is chosen here; everything follows the
registration.
"""
from __future__ import annotations

import itertools
from fractions import Fraction

import numpy as np
import sympy as sp

L = np.array([[1, 0], [1, 1]])


def kron(A, n):
    out = np.array([[1]])
    for _ in range(n):
        out = np.kron(out, A)
    return out


# nodes: level 0 (), level 1 (d,), level 2 (d1, d2)
nodes = [()] + [(d,) for d in range(4)] + [(a, b) for a in range(4) for b in range(4)]
idx = {n: i for i, n in enumerate(nodes)}
N = len(nodes)


def B(s, sym=False):
    M = np.zeros((N, N), dtype=object)
    blocks = [(0, 1, kron(L, 0), 1), (1, 5, kron(L, 2), s), (5, 21, kron(L, 4), 1)]
    for lo, hi, S, w in blocks:
        S = S + S.T - np.eye(S.shape[0], dtype=int) if sym else S
        M[lo:hi, lo:hi] = w * S
    return M


def E(mode="sym"):
    M = np.zeros((N, N), dtype=object)
    for n in nodes:
        if len(n) < 2:
            for d in range(4):
                p, c = idx[n], idx[n + (d,)]
                if mode in ("sym", "down"):
                    M[c, p] = 1          # parent -> child
                if mode in ("sym", "up"):
                    M[p, c] = 1          # child -> parent
    return M


def dets(mode="sym", sym=False):
    return {s: int(sp.Matrix(B(s, sym) + E(mode)).det()) for s in (1, 0, -1)}


def ratios(d):
    out = {}
    for a, b in itertools.permutations((1, 0, -1), 2):
        out[(a, b)] = Fraction(d[a], d[b]) if d[b] != 0 else None
    return out


if __name__ == "__main__":
    a = sp.symbols("alpha")
    print("=== Primary model (as registered) ===")
    Zs = sp.expand(sp.Matrix(a * (B(1) + E())).det())
    print("Z(+1) = det(alpha (B_+1 + E)) =", sp.factor(Zs))
    d = dets()
    print("det(B_s + E) for s = +1, 0, -1:", d)
    P = Fraction(d[0], d[-1]) if d[-1] else None
    print("Prefactor P = det(B_0+E)/det(B_-1+E) =", P, " -> ", "SUCCESS (17/13)" if P == Fraction(17, 13) else "FAILURE (not 17/13)")
    r = ratios(d)
    print("All six ratios:", {k: str(v) for k, v in r.items()})
    print("Ratios equal to 17/13:", [k for k, v in r.items() if v == Fraction(17, 13)])
    print("\n=== Secondary variants (reported, not counted) ===")
    for nm, kw in (("(a) E down only", dict(mode="down")), ("(b) E up only", dict(mode="up")),
                   ("(c) symmetric Sierpinski", dict(sym=True))):
        dv = dets(**kw)
        rv = ratios(dv)
        print(f"{nm}: dets {dv}; P = {Fraction(dv[0], dv[-1]) if dv[-1] else None};"
              f" ratios = 17/13: {[k for k, v in rv.items() if v == Fraction(17, 13)]}")

    print("\n=== Pre-registration 2: antisymmetric tree coupling (NETWORK_MODEL_PREREG_2.md) ===")
    Em = E("down") - E("up")
    d2 = {s_: int(sp.Matrix(B(s_) + Em).det()) for s_ in (1, 0, -1)}
    print("det(B_s + E-) for s = +1, 0, -1:", d2)
    print("Registered prediction (6, 24) at s = 0, -1:", "SUCCESS" if (d2[0], d2[-1]) == (6, 24) else "FAILURE")
    s_ = sp.symbols("s")
    def Bsym(v):
        M = sp.zeros(N, N)
        for lo, hi, S, w in [(0, 1, kron(L, 0), 1), (1, 5, kron(L, 2), v), (5, 21, kron(L, 4), 1)]:
            M[lo:hi, lo:hi] = sp.Matrix(w * S)
        return M
    p1 = sp.expand((Bsym(s_) + sp.Matrix(Em)).det())
    p2 = sp.expand((Bsym(-s_) + sp.Matrix(E())).det())
    print("det(B_s + E-) =", sp.factor(p1), "; equals det(B_-s + E):", sp.simplify(p1 - p2) == 0)
