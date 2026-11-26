"""Verify: the root exchange on the graded read space and on the address tree.

Checks the abstract algebra of ROOT_EXCHANGE_ON_THE_ADDRESS_TREE.md:
  1. On 1 + V + V(x)V the leg-sign involution has traces 21,17,13.
  2. In PG(2,4), rotation and field conjugation constrain a projective flag.
  3. The constructed projective sign operator has the prescribed grades on
     the time-adapted frequency tree. This does not derive physical exchange.
  4. Cube inversion reverses four odd Walsh characters. The prefix permutation
     tree has invariant contrast dimensions 1,4,16. This is an abstract
     permutation test, not a derivation of the physical sign operator or an
     identification of each contrast with a particular reader.

See recursive-triforce-geometry for actual medial refinement, the spatial
rotation obstruction, the pointing-parity compression and the weighted read.

Run: python verify_root_exchange_tree.py   (NumPy, SymPy)
"""
import itertools
import numpy as np
import sympy as sp

checks = []


def check(name, ok):
    checks.append((name, bool(ok)))
    print(("PASS " if ok else "FAIL ") + name)


# ---------------------------------------------------------------- Part 1
K = 4
dims = [1, K, K * K]
Pi_R = np.diag(sum(([(-1) ** d] * n for d, n in enumerate(dims)), []))
I21 = np.eye(sum(dims))
check("root exchange is an involution on 1+V+V(x)V", np.allclose(Pi_R @ Pi_R, I21))
for s in (1, 0, -1):
    Is = (1 + s) / 2 * I21 + (1 - s) / 2 * Pi_R
    check(f"tr I_s = f(4,{s:+d}) = {1 + s*K + K*K}", round(np.trace(Is)) == 1 + s * K + K * K)
ev = np.linalg.eigvalsh(Pi_R)
check("+1 eigenspace has dimension E = 1+K^2 = 17", int((ev > 0).sum()) == 17)
check("-1 eigenspace has dimension O = K = 4", int((ev < 0).sum()) == 4)
check("tr(root exchange) = 13", round(np.trace(Pi_R)) == 13)
k, s = sp.symbols("K s")
check("for general K: ((1+s)f(K,1)+(1-s)f(K,-1))/2 = 1+sK+K^2",
      sp.expand(((1 + s) * (1 + k + k**2) + (1 - s) * (1 - k + k**2)) / 2 - (1 + s * k + k**2)) == 0)
tau = np.zeros((16, 16))
for i in range(4):
    for j in range(4):
        tau[4 * j + i, 4 * i + j] = 1
check("swap on V(x)V has trace K (it fixes the K self-pairs)", round(np.trace(tau)) == K)
for s in (1, 0, -1):
    C = np.zeros((17, 17)); C[0, 0] = 1; C[1:, 1:] = np.eye(16) + s * tau
    check(f"swap realization tr(1 + (I + s tau)) = f(4,{s:+d})", round(np.trace(C)) == 1 + s * K + K * K)

# ---------------------------------------------------------------- Part 2
MUL = [[0, 0, 0, 0], [0, 1, 2, 3], [0, 2, 3, 1], [0, 3, 1, 2]]  # GF(4): 0,1,w,w^2
add = lambda a, b: a ^ b
mul = lambda a, b: MUL[a][b]
INV = {1: 1, 2: 3, 3: 2}


def norm(v):
    for x in v:
        if x:
            return tuple(mul(INV[x], y) for y in v)


dot = lambda u, v: add(add(mul(u[0], v[0]), mul(u[1], v[1])), mul(u[2], v[2]))
pts = sorted({norm(v) for v in itertools.product(range(4), repeat=3) if any(v)})
check("PG(2,4) has 21 points = 1+K+K^2", len(pts) == 21)
lines = {L: [q for q in pts if dot(L, q) == 0] for L in pts}
rot = lambda v: norm((v[2], v[0], v[1]))                  # 120 degrees about (1,1,1)
conj = lambda v: norm(tuple(mul(x, x) for x in v))        # w <-> w^2
fixP = [q for q in pts if rot(q) == q]
check("rotation fixes exactly 3 points", len(fixP) == 3)
time_pts = [q for q in fixP if conj(q) == q]
check("only the time point (1,1,1) is also fixed by conjugation", time_pts == [(1, 1, 1)])
p = (1, 1, 1)
through = [L for L in pts if rot(L) == L and p in lines[L]]
check("exactly two rotation-fixed lines pass through the time point", len(through) == 2)
check("conjugation swaps those two lines (vortex <-> antivortex)", conj(through[0]) == through[1])


def orbit_sizes(S, f):
    S = set(S); out = []
    while S:
        q = S.pop(); o = {q}; r = f(q)
        while r not in o:
            o.add(r); r = f(r)
        S -= o; out.append(len(o))
    return sorted(out)


tet = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
perm = [tet.index((v[2], v[0], v[1])) for v in tet]
tet_legs = orbit_sizes(range(4), lambda i: perm[i])
tet_pairs = orbit_sizes(range(16), lambda ij: 4 * perm[ij // 4] + perm[ij % 4])
for L in through:
    legs = [q for q in lines[L] if q != p]
    rest = [q for q in pts if q not in lines[L]]
    check(f"flag split is 1 + {len(legs)} + {len(rest)}", (len(legs), len(rest)) == (4, 16))
    check("rotation orbits on the 4 match the tetrad legs (1 fixed + 3 cycled)", orbit_sizes(legs, rot) == tet_legs)
    check("rotation orbits on the 16 match the tetrad leg pairs (1 + five 3-cycles)", orbit_sizes(rest, rot) == tet_pairs)

# ---------------------------------------------------------------- Part 3
V = list(itertools.product(range(4), repeat=3))
ix = {v: i for i, v in enumerate(V)}
TR = {0: 0, 1: 0, 2: 1, 3: 1}                             # absolute trace GF(4) -> GF(2)
X = np.array([[(-1) ** TR[dot(u, v)] for v in V] for u in V]) / 8.0
check("Walsh characters of GF(4)^3 are orthonormal", np.allclose(X @ X.T, np.eye(64)))
R = np.zeros((64, 64))
for v in V:
    R[ix[(v[2], v[0], v[1])], ix[v]] = 1
Tm = np.zeros((64, 64))
for v in V:
    Tm[ix[tuple(mul(2, x) for x in v)], ix[v]] = 1
Q = (np.eye(64) + Tm + Tm @ Tm) / 3


def matvec(g, v):
    return tuple(add(add(mul(g[r][0], v[0]), mul(g[r][1], v[1])), mul(g[r][2], v[2])) for r in range(3))


def inverse(g):
    for h in itertools.product(range(4), repeat=9):
        H = [h[0:3], h[3:6], h[6:9]]
        if all(matvec(H, matvec(g, e)) == e for e in [(1, 0, 0), (0, 1, 0), (0, 0, 1)]):
            return H


transpose = lambda g: [[g[c][r] for c in range(3)] for r in range(3)]


def tree(H):
    """Tree whose frequency basis has columns H (coarse, middle, fine)."""
    gi = inverse(transpose(inverse(H)))
    dig = lambda v: matvec(gi, v)
    Ps = []
    for k_ in range(4):
        M = np.zeros((64, 64))
        for v in V:
            grp = [u for u in V if dig(u)[:k_] == dig(v)[:k_]]
            for u in grp:
                M[ix[v], ix[u]] = 1 / len(grp)
        Ps.append(M)
    return Ps


def exchange(legs):
    lv = {tuple(mul(c, x) for x in q) for q in legs for c in (1, 2, 3)}
    return X.T @ np.diag([-1.0 if u in lv else 1.0 for u in V]) @ X


def level_spectra(Ps, Pi):
    out = []
    for k_ in (1, 2, 3):
        U, sv, _ = np.linalg.svd(Q @ (Ps[k_] - Ps[k_ - 1]))
        r = int((sv > 1e-9).sum()); B = U[:, :r]
        out.append((r, sorted(set(np.round(np.linalg.eigvalsh(B.T @ Pi @ B), 9)))))
    return out


xaxis = tree([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
Pi0 = exchange([q for q in lines[through[0]] if q != p])
check("x-axis tree levels do NOT all commute with the rotation", not all(np.allclose(R @ P, P @ R) for P in xaxis))
check("x-axis tree: exchange is NOT +1,-1,+1 on its levels",
      [e for _, e in level_spectra(xaxis, Pi0)] != [[1.0], [-1.0], [1.0]])
for name, L in (("vortex", through[0]), ("antivortex", through[1])):
    legs = [q for q in lines[L] if q != p]
    axial = [q for q in legs if rot(q) == q][0]
    Pi = exchange(legs)
    check(f"{name}: exchange commutes with the rotation", np.allclose(R @ Pi, Pi @ R))
    good = True; rotok = True; first = None
    for off in [q for q in pts if q not in lines[L]]:
        Ps = tree([[p[r], axial[r], off[r]] for r in range(3)])
        spec = level_spectra(Ps, Pi)
        good &= spec == [(1, [1.0]), (4, [-1.0]), (16, [1.0])]
        rotok &= all(np.allclose(R @ P, P @ R) for P in Ps)
        if first is None:
            first = Ps
        else:
            good &= all(np.allclose(a, b) for a, b in zip(first, Ps))
    check(f"{name}: time-adapted tree levels commute with the rotation (all 16 third vectors)", rotok)
    check(f"{name}: exchange is exactly +1, -1, +1 on the 1, 4, 16 levels (all 16 third vectors, same tree)", good)

# ---------------------------------------------------------------- Part 4
# Grounding: the root exchange is the cube's central inversion, and the physical
# face -> tile -> subchannel tree carries the grading with no flag choice.
verts = [np.array(v) for v in itertools.product((1, -1), repeat=3)]
chars = {"1": lambda v: 1, "x": lambda v: v[0], "y": lambda v: v[1], "z": lambda v: v[2],
         "xy": lambda v: v[0] * v[1], "yz": lambda v: v[1] * v[2], "zx": lambda v: v[2] * v[0],
         "xyz": lambda v: v[0] * v[1] * v[2]}
odd = [k_ for k_, f in chars.items() if all(f(-v) == -f(v) for v in verts)]
check("cube inversion is -1 on exactly four characters: x, y, z, xyz (K = 4 legs)",
      sorted(odd) == sorted(["x", "y", "z", "xyz"]))
Sv = [np.array(v) for v in tet]
Ut = np.array([[1] * 4] + [[s_[a] for s_ in Sv] for a in range(3)]) / 2
UA = np.array([[chars[k_](s_) for s_ in Sv] for k_ in ["xyz", "x", "y", "z"]]) / 2
UB = np.array([[chars[k_](-s_) for s_ in Sv] for k_ in ["xyz", "x", "y", "z"]]) / 2
check("the odd characters on TetA are the Triforce read's Hadamard legs U", np.allclose(UA, Ut))
check("on TetB the same characters are -U: inversion reverses all four legs", np.allclose(UB, -Ut))
check("Triforce TetB read diag(1,-1,-1,-1)U = the same legs with time row -xyz (not time reversal)",
      np.allclose(np.diag([-1, 1, 1, 1]) @ UB, np.diag([1, -1, -1, -1]) @ Ut))
cent = lambda i, j: (-Sv[i] / 3 if i == j else (3 * Sv[j] - Sv[i]) / 6)
Rg = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
pm = [next(k_ for k_ in range(4) if np.allclose(Rg @ Sv[i], Sv[k_])) for i in range(4)]
check("120-degree rotation about s_0 = (1,1,1) fixes leg 0 and cycles legs 1, 2, 3", pm[0] == 0 and sorted(pm[1:]) == [1, 2, 3])
check("it maps Triforce tile (i,j) to tile (pi i, pi j) exactly",
      all(np.allclose(Rg @ cent(i, j), cent(pm[i], pm[j])) for i in range(4) for j in range(4)))
idx3 = list(itertools.product(range(4), repeat=3)); ix3 = {v: n_ for n_, v in enumerate(idx3)}
Mp = np.zeros((64, 64))
for v in idx3:
    Mp[ix3[tuple(pm[d] for d in v)], ix3[v]] = 1
Pp = []
for k_ in range(4):
    A_ = np.zeros((64, 64))
    for v in idx3:
        grp = [u for u in idx3 if u[:k_] == v[:k_]]
        for u in grp:
            A_[ix3[v], ix3[u]] = 1 / len(grp)
    Pp.append(A_)
check("recursive prefix permutation model: every level commutes with the rotation", all(np.allclose(Mp @ P_, P_ @ Mp) for P_ in Pp))
Qp = (np.eye(64) + Mp + Mp @ Mp) / 3
check("its invariant contrast ranks are 1, 4, 16 (not individual reader identities)",
      [int(round(np.trace(Qp @ (Pp[k_] - Pp[k_ - 1])))) for k_ in (1, 2, 3)] == [1, 4, 16])

n = len(checks); ok = sum(c for _, c in checks)
print(f"\n{ok}/{n} checks passed")
raise SystemExit(0 if ok == n else 1)
