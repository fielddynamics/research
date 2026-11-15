"""Exact checks for PROOF.md: each Triforce face is a vortex about its leg.

Sites (33): the Field Origin; the 8 central tiles (medial triangles of the 8 tetrahedron faces,
which are the octahedron's faces); the 24 outer tiles (3 per face, which are the exposed faces of
the 8 star points). Position of a tile = its centroid. Two tiles couple if they share an edge;
each central tile couples to the Field Origin (the leg through it). Couplings and on-site energies
are one free symbol per Td-orbit, so H is the most general Td-invariant model of this kind
(TetA and TetB may differ: any x). Axis: the leg n = (1,1,1)/sqrt3; C3 = rotation by 120 degrees about it.
Run: python verify_triforce_vortex.py
"""
import itertools
import numpy as np
import sympy as sp

passed = failed = 0
def check(label, ok):
    global passed, failed
    passed += bool(ok); failed += (not ok)
    print(("PASS " if ok else "FAIL ") + label)

R = sp.Rational
TA = [sp.Matrix(v) for v in [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]]
TB = [-v for v in TA]
key = lambda m: tuple(sp.nsimplify(c) for c in m)

tiles = []          # (kind, chamber, vertices as tuple of keys)
for name, T in (("A", TA), ("B", TB)):
    for i in range(4):
        f = [T[j] for j in range(4) if j != i]
        mids = [(f[a] + f[b]) / 2 for a, b in ((0, 1), (1, 2), (0, 2))]
        tiles.append(("central", name, tuple(sorted(key(m) for m in mids))))
        for k in range(3):
            v = f[k]; o = [f[j] for j in range(3) if j != k]
            tiles.append(("outer", name, tuple(sorted([key(v), key((v + o[0]) / 2), key((v + o[1]) / 2)]))))
sites = [("origin", "-", ((0, 0, 0),))] + tiles
n = len(sites)
cent = [sp.Matrix([sum(sp.Matrix(p)[c] for p in s[2]) / len(s[2]) for c in range(3)]) for s in sites]
cent[0] = sp.zeros(3, 1)
octv = {key(sp.Matrix(v)) for v in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]}
check("G1 33 sites: origin, 8 central tiles, 24 outer tiles", n == 33
      and sum(s[0] == "central" for s in sites) == 8 and sum(s[0] == "outer" for s in sites) == 24)
check("G1 every central tile is an octahedron face (its vertices are cube face centres)",
      all(set(s[2]) <= octv for s in sites if s[0] == "central"))
pen = lambda i: [v for v in (TB if sites[i][1] == "A" else TA)
                 if sp.Matrix(v).cross(cent[i]) == sp.zeros(3, 1) and (sp.Matrix(v).T * cent[i])[0] > 0]
check("G1 each central tile's centroid is 1/3 of the penetrating vertex: it lies on the leg through the Field Origin",
      all(len(pen(i)) == 1 and cent[i] == pen(i)[0] / 3 for i in range(n) if sites[i][0] == "central"))

# adjacency: share an edge (two vertices); central tiles to the origin (the legs)
adj = []
for i in range(1, n):
    for j in range(i + 1, n):
        if len(set(sites[i][2]) & set(sites[j][2])) == 2:
            adj.append((i, j))
adj += [(0, i) for i in range(1, n) if sites[i][0] == "central"]

# Td as signed permutations preserving TetA
def act(Rm, s):
    if s[0] == "origin":
        return s
    vs = tuple(sorted(key(Rm * sp.Matrix(p)) for p in s[2]))
    return (s[0], s[1], vs)
Td = []
for p in itertools.permutations(range(3)):
    for sg in itertools.product((1, -1), repeat=3):
        Rm = sp.zeros(3)
        for r_ in range(3):
            Rm[r_, p[r_]] = sg[r_]
        if {key(Rm * v) for v in TA} == {key(v) for v in TA}:
            Td.append(Rm)
index = {s: i for i, s in enumerate(sites)}
def perm_of(Rm):
    out = []
    for s in sites:
        t = act(Rm, s)
        t = next(u for u in sites if u[0] == t[0] and u[2] == t[2])
        out.append(index[t])
    return out
perms = [perm_of(Rm) for Rm in Td]
check("G2 Td (24 elements) permutes the 33 sites", len(Td) == 24 and all(sorted(pm) == list(range(n)) for pm in perms))

# one symbol per Td-orbit of sites and of bonds
site_orb, bond_orb = {}, {}
for i in range(n):
    o = frozenset(pm[i] for pm in perms); site_orb.setdefault(o, sp.Symbol(f"e{len(site_orb)}", real=True))
bset = {frozenset(b) for b in adj}
for b in adj:
    o = frozenset(frozenset((pm[b[0]], pm[b[1]])) for pm in perms); bond_orb.setdefault(o, sp.Symbol(f"t{len(bond_orb)}", real=True))
H = sp.zeros(n)
for o, sym in site_orb.items():
    for i in o:
        H[i, i] = sym
for o, sym in bond_orb.items():
    for b in o:
        i, j = tuple(b); H[i, j] = H[j, i] = -sym
print(f"     model: {len(site_orb)} site orbits, {len(bond_orb)} bond orbits ({len(adj)} bonds), all free symbols")
P = lambda pm: sp.Matrix(n, n, lambda a, b: 1 if pm[b] == a else 0)
check("G2 H commutes with all 24 elements of Td, for every value of the parameters",
      all(P(pm) * H == H * P(pm) for pm in perms))

# C3 about (1,1,1)
C3 = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
check("G3 the 120-degree rotation about the leg (1,1,1) is in Td: a proper rotation, a symmetry for every x",
      any(C3 == Rm for Rm in Td) and C3.det() == 1)
Cp = P(perm_of(C3))
w = sp.exp(2 * sp.pi * sp.I / 3)
proj = lambda lam: sp.simplify(sum((lam ** (-k) * Cp ** k for k in range(3)), sp.zeros(n)) / 3)
Pw = proj(w)
ax = sp.Matrix([1, 1, 1]) / sp.sqrt(3)
on_axis = [i for i in range(n) if cent[i].cross(ax) == sp.zeros(3, 1)]
names = lambda idx: [f"{sites[i][0]}{sites[i][1]}@{tuple(cent[i])}" for i in idx]
print("     sites on the leg:", names(on_axis))
check("G3 the leg passes through the origin and through exactly two central tiles (one TetA face, one TetB face)",
      len(on_axis) == 3 and sorted(sites[i][1] for i in on_axis if sites[i][0] == "central") == ["A", "B"])
check("L1 the winding space (rotation eigenvalue e^{2 pi i/3}) has dimension 10", Pw.rank() == 10)
Pw = Pw.applyfunc(lambda z: sp.nsimplify(sp.expand_complex(z)))
check("L1 every winding state vanishes on the leg: at the origin and at both central tiles on it (the eye)",
      all(Pw[i, j] == 0 for i in on_axis for j in range(n)))
starA = [i for i in range(n) if sites[i][0] == "outer" and key(TA[0]) in sites[i][2]]
check("L1 the three outer tiles at the TetA vertex (1,1,1), the Triforce corners around this leg, form one ring of the rotation",
      len(starA) == 3 and sorted(perm_of(C3)[i] for i in starA) == sorted(starA))

# Theorem: stationary vortices that circulate about the leg, with the star point's ring turning
Hf = sp.lambdify(list(site_orb.values()) + list(bond_orb.values()), H, "numpy")
Pwf = np.array(Pw.evalf(), dtype=complex)
U, sv, _ = np.linalg.svd(Pwf); Bw = U[:, :10]
axn = np.array([1, 1, 1]) / np.sqrt(3)
pos = np.array([[float(c) for c in v] for v in cent])
rng = np.random.default_rng(11)
ok_stat = ok_L = ok_ring = ok_anti = True
nsym = len(site_orb) + len(bond_orb)
for trial in range(20):
    pr = rng.normal(size=nsym)
    Hn = np.array(Hf(*pr), dtype=float)
    Hb = Bw.conj().T @ Hn @ Bw
    E, W = np.linalg.eigh(Hb)
    for k in range(10):
        psi = Bw @ W[:, k]
        ok_stat &= np.allclose(Hn @ psi, E[k] * psi, atol=1e-9)
        def circ(ps):
            return sum(2 * np.imag(np.conj(ps[a]) * Hn[a, b] * ps[b]) * np.dot(np.cross(pos[a], pos[b]), axn)
                       for a in range(n) for b in range(a + 1, n) if Hn[a, b] != 0)
        L = circ(psi); Lc = circ(psi.conj())
        ok_L &= abs(L) > 1e-9
        ok_anti &= abs(L + Lc) < 1e-9
        ok_ring &= np.linalg.norm(psi[starA]) > 1e-9
check("T1 every winding eigenvector of the 10x10 block is a stationary state of the full 33-tile model (20 random parameter sets)", ok_stat)
check("T1 each carries a nonzero current circulating about the leg (sum J_ij (r_i x r_j) . n != 0)", ok_L)
check("T1 its complex conjugate is an antivortex: same energy, opposite circulation", ok_anti)
check("T1 and the three outer tiles of the star point at (1,1,1) turn in every one", ok_ring)

# the TetA and TetB strands about an octahedron axis are not linked
def gauss_link(Pp, Qq, N=300):
    def seg(poly):
        pts, tans = [], []
        for a, b in zip(poly, poly[1:] + poly[:1]):
            for t in (np.arange(N) + .5) / N:
                pts.append(a + (b - a) * t); tans.append((b - a) / N)
        return np.array(pts), np.array(tans)
    p_, dp = seg(Pp); q_, dq = seg(Qq); Lk = 0.0
    for i in range(len(p_)):
        rr = p_[i] - q_
        Lk += np.sum(np.einsum("ij,ij->i", np.cross(dp[i], dq), rr) / np.linalg.norm(rr, axis=1) ** 3)
    return Lk / (4 * np.pi)
S4 = lambda v: np.array([-v[1], v[0], -v[2]])
A_ = [np.array([1., 1, 1])]; B_ = [np.array([-1., -1, -1])]
for _ in range(3):
    A_.append(S4(A_[-1])); B_.append(S4(B_[-1]))
check("B1 the TetA and TetB strands that wind about an octahedron axis have linking number 0: they do not braid",
      abs(gauss_link(A_, B_)) < 1e-3)

print(f"\n{passed}/{passed + failed} checks passed")
raise SystemExit(failed)
