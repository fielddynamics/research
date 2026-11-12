"""13. Target #1 of the BIMOND x GFD intersection: irreducible decomposition of the 64-component connection difference N_abc
(indices lowered with eta), split as C (symmetric in b,c: 40) + T (antisymmetric in b,c: 24).

Checks, all exact or to machine precision on integer data:
 A. GL(4) split: C = Sym^3 (20) + hook_C (20);  T = Lambda^3 (4) + hook_T (20)
 B. Lorentz split with eta: Sym^3 = 16 + 4, hook_C = 16 + 4, hook_T = 16 + 4 (vector), Lambda^3 = 4 (axial)
 C. Lorentz types by Casimirs (j1, j2)
 D. The Gram index grid's diagonal 16: S4-invariant, not Lorentz-invariant; same for the 24 upper triangle
 E. S4 characters of C, diagonal 16, T
 F. Where BIMOND's slow-motion component C^i_00 lies
 G. The contorsion map T -> symmetric part of K (lands in C): kernel, image, and how much of C^i_00 it reaches
"""
import itertools
import numpy as np

np.set_printoptions(precision=4, suppress=True)
ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

n = 4
eta = np.diag([-1.0, 1, 1, 1])
D = n ** 3
idx = lambda a, b, c: (a * n + b) * n + c
def T3(f):                                  # build a 64x64 matrix from a map on index triples
    M = np.zeros((D, D))
    for a, b, c in itertools.product(range(n), repeat=3):
        for (a2, b2, c2), w in f(a, b, c):
            M[idx(a2, b2, c2), idx(a, b, c)] += w
    return M

perm = lambda p: T3(lambda a, b, c: [(tuple((a, b, c)[i] for i in p), 1.0)])
I = np.eye(D)
Sbc = (I + perm((0, 2, 1))) / 2
Abc = (I - perm((0, 2, 1))) / 2
P3 = list(itertools.permutations(range(3)))
sgn3 = lambda p: round(np.linalg.det(np.eye(3)[list(p)]))
Sym3 = sum(perm(p) for p in P3) / 6
Alt3 = sum(sgn3(p) * perm(p) for p in P3) / 6
rank = lambda M: np.linalg.matrix_rank(M, tol=1e-9)
def basis(M):                                # orthonormal basis of the column space
    u, s, _ = np.linalg.svd(M); return u[:, :int((s > 1e-9).sum())]

C, T = basis(Sbc), basis(Abc)
Sy, Hc = basis(Sym3), basis(Sbc - Sym3)
Al, Ht = basis(Alt3), basis(Abc - Alt3)
check("A. 64 = C 40 + T 24", (C.shape[1], T.shape[1]) == (40, 24))
check("A. C = Sym^3 (20) + hook_C (20); T = Lambda^3 (4) + hook_T (20)",
      (Sy.shape[1], Hc.shape[1], Al.shape[1], Ht.shape[1]) == (20, 20, 4, 20))

# ---- B: eta-traces. trace on (b,c): t_a = eta^{bc} N_abc ; trace on (a,b): s_c = eta^{ab} N_abc
ei = np.linalg.inv(eta)
tr_bc = np.zeros((n, D)); tr_ab = np.zeros((n, D))
for a, b, c in itertools.product(range(n), repeat=3):
    tr_bc[a, idx(a, b, c)] += ei[b, c]; tr_ab[c, idx(a, b, c)] += ei[a, b]
tr = np.vstack([tr_bc, tr_ab])
def split_trace(B):
    """kernel of the traces inside span(B) (the traceless part) and its dimension"""
    K = B @ basis(np.eye(B.shape[1]) - np.linalg.pinv(tr @ B) @ (tr @ B))
    return K
Sy0, Hc0, Ht0 = split_trace(Sy), split_trace(Hc), split_trace(Ht)
check("B. traceless parts: Sym^3 -> 16, hook_C -> 16, hook_T -> 16 (traces 4 each)",
      (Sy0.shape[1], Hc0.shape[1], Ht0.shape[1]) == (16, 16, 16))
check("B. Lambda^3 is already traceless (the axial 4)", np.allclose(tr @ Al, 0))

# cleaner: build the two vector channels explicitly
E1 = np.zeros((D, n)); E2 = np.zeros((D, n))           # E1: eta_bc v_a ; E2: eta_ab v_c + eta_ac v_b
for v in range(n):
    for a, b, c in itertools.product(range(n), repeat=3):
        E1[idx(a, b, c), v] = eta[b, c] * (a == v)
        E2[idx(a, b, c), v] = eta[a, b] * (c == v) + eta[a, c] * (b == v)
Sy1 = basis(Sym3 @ np.hstack([E1, E2]))
Hc1 = basis((Sbc - Sym3) @ np.hstack([E1, E2]))
E3 = np.zeros((D, n))                                     # torsion vector: eta_ab v_c - eta_ac v_b
for v in range(n):
    for a, b, c in itertools.product(range(n), repeat=3):
        E3[idx(a, b, c), v] = eta[a, b] * (c == v) - eta[a, c] * (b == v)
Ht1 = basis(E3)
check("B. one vector (4) in each of Sym^3, hook_C, hook_T", (Sy1.shape[1], Hc1.shape[1], Ht1.shape[1]) == (4, 4, 4))
pieces = {"Sym3_16": Sy0, "Sym3_vec": Sy1, "hookC_16": Hc0, "hookC_vec": Hc1,
          "hookT_16": Ht0, "hookT_vec": Ht1, "axial": Al}
allB = np.hstack(list(pieces.values()))
check("B. the seven pieces are independent and span all 64", rank(allB) == 64)

# ---- C: Lorentz generators on lowered indices, invariance and Casimirs
def gen(i, j, boost=False):
    X = np.zeros((n, n))
    if boost: X[0, i] = X[i, 0] = 1.0            # boost along i
    else: X[i, j], X[j, i] = -1.0, 1.0           # rotation in (i,j)
    return -X.T                                  # action on a lower index
def lift(X):
    return T3(lambda a, b, c: [((d, b, c), X[d, a]) for d in range(n)] +
                               [((a, d, c), X[d, b]) for d in range(n)] +
                               [((a, b, d), X[d, c]) for d in range(n)])
J = [lift(gen(2, 3)), lift(gen(3, 1)), lift(gen(1, 2))]
K = [lift(gen(i, 0, True)) for i in (1, 2, 3)]
def invariant(B, gens):
    return all(rank(np.hstack([B, G @ B])) == B.shape[1] for G in gens)
check("C. each of the seven pieces is Lorentz-invariant", all(invariant(B, J + K) for B in pieces.values()))
A = [(J[k] + 1j * K[k]) / 2 for k in range(3)]; Bm = [(J[k] - 1j * K[k]) / 2 for k in range(3)]
A2 = sum(a @ a for a in A); B2 = sum(b @ b for b in Bm)
def casimirs(B):
    Bp = np.linalg.pinv(B)
    ea = np.round(np.linalg.eigvals(Bp @ A2 @ B).real, 6); eb = np.round(np.linalg.eigvals(Bp @ B2 @ B).real, 6)
    j = lambda e: sorted(set(round((-1 + np.sqrt(1 + 4 * abs(x))) / 2, 3) for x in e))
    return j(ea), j(eb)
types = {k: casimirs(B) for k, B in pieces.items()}
for k, v in types.items(): print(f"     {k:10s} dim {pieces[k].shape[1]:2d}   j1 in {v[0]}   j2 in {v[1]}")
check("C. Sym3_16 is (3/2,3/2); both hook 16s are (3/2,1/2)+(1/2,3/2); vectors and axial are (1/2,1/2)",
      types["Sym3_16"] == ([1.5], [1.5]) and types["hookC_16"] == types["hookT_16"] == ([0.5, 1.5], [0.5, 1.5])
      and all(types[k] == ([0.5], [0.5]) for k in ("Sym3_vec", "hookC_vec", "hookT_vec", "axial")))

# ---- D: the Gram index grid (coordinate components Gamma^l_{mn}); lowering with diagonal eta keeps the grid
diag16 = basis(np.array([np.eye(D)[:, idx(l, m, m)] for l in range(n) for m in range(n)]).T)
upper24 = basis(np.array([np.eye(D)[:, idx(l, m, k)] for l in range(n) for m in range(n) for k in range(n) if m < k]).T)
S4 = [perm_ for perm_ in itertools.permutations(range(n))]
def leg(p):
    return T3(lambda a, b, c: [((p[a], p[b], p[c]), 1.0)])
S4m = [leg(p) for p in S4]
check("D. index-grid diagonal 16 is S4-invariant", invariant(diag16, S4m))
check("D. index-grid diagonal 16 is NOT Lorentz-invariant (a boost moves it)", not invariant(diag16, K))
check("D. index-grid diagonal 16 is NOT rotation-invariant either", not invariant(diag16, J))
check("D. index-grid upper 24 is not even S4-invariant (a leg swap moves it to the lower triangle)", not invariant(upper24, S4m))
for k, B in pieces.items():
    inter = 16 + B.shape[1] - rank(np.hstack([diag16, B]))
    print(f"     dim(diag16 ∩ {k}) = {inter}")

# ---- E: S4 characters (classes e, (01), (01)(23), (012), (0123))
reps = [(0, 1, 2, 3), (1, 0, 2, 3), (1, 0, 3, 2), (1, 2, 0, 3), (1, 2, 3, 0)]
sizes = np.array([1, 6, 3, 8, 6])
table = {"1": [1, 1, 1, 1, 1], "sgn": [1, -1, 1, 1, -1], "[2,2]": [2, 0, 2, -1, 0],
         "std": [3, 1, -1, 0, -1], "sgn*std": [3, -1, -1, 0, 1]}
def char(B):
    Bp = np.linalg.pinv(B); return np.array([round(np.trace(Bp @ leg(p) @ B)) for p in reps])
def decomp(ch):
    return {k: int(round((sizes * ch * np.array(v)).sum() / 24)) for k, v in table.items()}
for name, B in [("C (40)", C), ("diag16", diag16), ("C ⊖ diag16 (24)", basis(Sbc - diag16 @ diag16.T)), ("T (24)", T)]:
    ch = char(B); print(f"     {name:16s} char {ch}  = {decomp(ch)}")
dC = decomp(char(C)); dT = decomp(char(T)); dS = decomp(char(basis(Sbc - diag16 @ diag16.T)))
check("E. S4: T is regular (1,1,2,3,3); C contains no sgn", dT == {"1": 1, "sgn": 1, "[2,2]": 2, "std": 3, "sgn*std": 3} and dC["sgn"] == 0)
check("E. S4: the symmetric off-diagonal 24 of C is NOT isomorphic to T (no sgn, not regular)", dS != dT)

# ---- F: BIMOND's slow-motion component C^i_00 (lowered: N_{i00}), i spatial
def comps(vec):
    coef = np.linalg.lstsq(allB, vec, rcond=None)[0]; out = {}; s = 0
    for k, B in pieces.items():
        part = B @ coef[s:s + B.shape[1]]; s += B.shape[1]; out[k] = part
    return out
v = np.zeros(D); v[idx(1, 0, 0)] = 1.0                      # N_{x00} = 1 (Newtonian pull along x)
parts = comps(v)
nz = [k for k, p in parts.items() if np.linalg.norm(p) > 1e-9]
print("     C^x_00 has components in:", nz)
check("F. C^x_00 lies in C only (Sym3 and hook_C pieces), none in torsion", set(nz) <= {"Sym3_16", "Sym3_vec", "hookC_16", "hookC_vec"} and not np.allclose(parts["hookC_16"], 0))
check("F. C^x_00 lies in the index-grid diagonal 16", rank(np.hstack([diag16, v[:, None]])) == 16)
check("F. C^x_00 = (sum of its parts)", np.allclose(sum(parts.values()), v))

# ---- G: contorsion. T_abc antisym in (b,c), lowered on a. K_abc = 1/2 (T_abc + T_bac + T_cab)?  use the probe's convention:
# K^l_mn = 1/2 (T^l_mn + T_m^l_n + T_n^l_m); lower l: K_lmn = 1/2 (T_lmn + T_mln + T_nlm)
Kmat = np.zeros((D, D))
for l, m, k in itertools.product(range(n), repeat=3):          # K_lmk = 1/2 (T_lmk + T_mlk + T_klm)
    Kmat[idx(l, m, k), idx(l, m, k)] += 0.5
    Kmat[idx(l, m, k), idx(m, l, k)] += 0.5
    Kmat[idx(l, m, k), idx(k, l, m)] += 0.5
KS = Sbc @ Kmat @ (T @ T.T)                                     # T -> symmetric (b,c) part of the contorsion
rT = rank(KS)
kerT = basis(T @ basis(np.eye(24) - np.linalg.pinv(KS @ T) @ (KS @ T)))
Kall = (Kmat @ T).T.reshape(-1, n, n, n)                        # one contorsion per torsion basis vector
check("G. contorsion is antisymmetric in its outer pair, K_lmk = -K_kml (metric compatibility), for all 24 torsions",
      np.allclose(Kall, -np.einsum('slmk->skml', Kall)))
check("G. contorsion reproduces torsion: K_lmk - K_lkm = T_lmk",
      np.allclose(Kall - np.einsum('slmk->slkm', Kall), T.T.reshape(-1, n, n, n)))
print(f"     rank of T -> K_(bc): {rT};  kernel dim {kerT.shape[1]}")
check("G. kernel of T -> K_(bc) is exactly the axial 4", kerT.shape[1] == 4 and rank(np.hstack([kerT, Al])) == 4)
img = basis(KS @ T)
check("G. image of T -> K_(bc) is a 20-dim Lorentz-invariant subspace of C", img.shape[1] == 20 and invariant(img, J + K)
      and rank(np.hstack([C, img])) == 40)
check("G. image of T -> K_(bc) is exactly hook_C (20 = 16 + vector); it meets Sym^3 only in 0",
      rank(np.hstack([img, Hc])) == 20 and rank(np.hstack([img, Sy])) == 40)
# how much of C^x_00 is reachable from torsion: project v onto img vs its complement in C
reach = img @ np.linalg.lstsq(img, v, rcond=None)[0]
resid = v - reach
in_sym16 = rank(np.hstack([Sy0, resid[:, None]])) == 16
print("     reachable part of C^x_00:", {(a, b, c): round(reach[idx(a, b, c)], 4) for a, b, c in itertools.product(range(n), repeat=3) if abs(reach[idx(a, b, c)]) > 1e-9})
print("     unreachable remainder lies in Sym3 pieces only:", rank(np.hstack([Sy0, Sy1, resid[:, None]])) == 20)

# ---- H: the realistic weak static field. ds^2 = -(1+2phi)dt^2 + (1-2 gamma phi) dx^2, linear in phi,
# gradient along x: d_x phi = g. Christoffel of the first kind Gamma_abc = 1/2 (d_b h_ac + d_c h_ab - d_a h_bc).
# BIMOND's C = Gamma - Gammahat is this with phi -> phi* (each metric with gamma = 1 in Milgrom's weak field).
import sympy as sp
gam, g = sp.symbols('gamma g')
h = sp.diag(-2, -2 * gam, -2 * gam, -2 * gam)                    # h_ab / phi
dh = [sp.zeros(4, 4) for _ in range(4)]; dh[1] = h * g          # only d_x is nonzero
Gam = lambda a, b, c: sp.Rational(1, 2) * (dh[b][a, c] + dh[c][a, b] - dh[a][b, c])
def weak(gv):
    vec = np.zeros(D)
    for a, b, c in itertools.product(range(n), repeat=3):
        vec[idx(a, b, c)] = float(Gam(a, b, c).subs({gam: gv, g: 1}))
    return vec
print("     weak-field Gamma_abc (g = 1), gamma symbolic:",
      {(a, b, c): sp.simplify(Gam(a, b, c).subs(g, 1)) for a, b, c in itertools.product(range(n), repeat=3) if Gam(a, b, c) != 0})
norms = {}
for gv in [0.0, 0.5, 1.0, 2.0]:
    p = comps(weak(gv)); norms[gv] = {k: round(float(np.abs(p[k]).max()), 4) for k in p}
    print(f"     gamma = {gv}: max |component| per piece", norms[gv])
check("H. the weak-field connection lies in C only (no torsion pieces), for every gamma",
      all(norms[gv][k] == 0 for gv in norms for k in ("hookT_16", "hookT_vec", "axial")))
pg = {gv: comps(weak(gv)) for gv in (0.0, 1.0, 2.0)}
lin = all(np.allclose(pg[1.0][k], (pg[0.0][k] + pg[2.0][k]) / 2) for k in pieces)
check("H. each piece is linear (affine) in gamma", lin)
sym_x00 = sp.simplify((Gam(1, 0, 0) + Gam(0, 1, 0) + Gam(0, 0, 1)) / 3)
check("H. exact: the fully symmetric part of Gamma_x00 is (Gamma_x00 + Gamma_0x0 + Gamma_00x)/3 = -g/3 for every gamma,"
      " so the weak field always has a Sym^3 part that no torsion can supply", sym_x00 == -g / 3)
zero_at = {k: [gv for gv in (0.0, 0.5, 1.0, 2.0) if norms[gv][k] == 0] for k in ("Sym3_16", "Sym3_vec", "hookC_16", "hookC_vec")}
print("     pieces that vanish, and at which gamma:", zero_at)
print(f"\n{sum(ok)}/{len(ok)} checks passed")
