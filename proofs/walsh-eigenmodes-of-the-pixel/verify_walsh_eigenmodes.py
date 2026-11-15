#!/usr/bin/env python3
"""
Verification: The Walsh Eigenmodes of the Pixel, and What Closure Reads
========================================================================

Every statement of the proof is checked here, exactly (sympy, in all
parameters, or exhaustively over finite sets), except Part E, which runs the
archive's octahedral resonance node itself and checks identities of its code.

  A. The Walsh functions are the cube's eigenmodes (Theorem 1).
  B. The pixel's symmetry T_d pairs the Walsh grades (Theorem 2).
  C. The vortices are built from the direction modes (Corollary 1, Proposition 1).
  D. Closure reads exactly the direction modes (Theorem 3).
  E. What the oscillator node's closure reads (Theorem 4).

Run: python verify_walsh_eigenmodes.py
"""
import itertools, os, sys
import sympy as sp

PASS = FAIL = 0
def check(name, ok):
    global PASS, FAIL
    ok = bool(ok)
    PASS += ok; FAIL += (not ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")

# ---------------------------------------------------------------- the cube
CORNERS = [s for s in itertools.product((1, -1), repeat=3)]          # 8 corners (+-1,+-1,+-1)
idx = {s: k for k, s in enumerate(CORNERS)}
TETA = [s for s in CORNERS if s[0] * s[1] * s[2] == 1]              # TetA: xyz = +1
TETB = [s for s in CORNERS if s[0] * s[1] * s[2] == -1]
SUBSETS = [S for r in range(4) for S in itertools.combinations(range(3), r)]
def walsh(S):
    return sp.Matrix([sp.prod([s[d] for d in S]) if S else 1 for s in CORNERS])
W = {S: walsh(S) for S in SUBSETS}
grade = {S: len(S) for S in SUBSETS}
NAME = {(): "1", (0,): "x", (1,): "y", (2,): "z", (1, 2): "yz", (0, 2): "xz", (0, 1): "xy", (0, 1, 2): "xyz"}

def perm_matrix(g):
    """Corner permutation induced by a 3x3 signed permutation g: (P psi)[g s] = psi[s]."""
    P = sp.zeros(8, 8)
    for s in CORNERS:
        gs = tuple(sum(g[i][j] * s[j] for j in range(3)) for i in range(3))
        P[idx[gs], idx[s]] = 1
    return P

def signed_perms():
    out = []
    for p in itertools.permutations(range(3)):
        for sg in itertools.product((1, -1), repeat=3):
            g = [[0] * 3 for _ in range(3)]
            for i in range(3):
                g[i][p[i]] = sg[i]
            out.append(g)
    return out

OH = signed_perms()
maps_to = lambda g, s: tuple(sum(g[i][j] * s[j] for j in range(3)) for i in range(3))
TD = [g for g in OH if all(maps_to(g, s) in TETA for s in TETA)]
FLIPS = [[[a, 0, 0], [0, b, 0], [0, 0, c]] for a, b, c in itertools.product((1, -1), repeat=3)]

print("=" * 78)
print("A. The Walsh functions are the cube's eigenmodes")
print("=" * 78)
check("the 8 Walsh functions are orthogonal, w_S . w_T = 8 delta_ST",
      all((W[S].T * W[T])[0] == (8 if S == T else 0) for S in SUBSETS for T in SUBSETS))
check("each is a character of the bit-flip group Z2^3 (sign flips of the coordinates): F w_S = chi_S(F) w_S",
      all(perm_matrix(F) * W[S] == sp.prod([F[d][d] for d in S] or [1]) * W[S] for F in FLIPS for S in SUBSETS))
# general symmetric operator commuting with all bit flips
hs = sp.symbols("h0:36")
Hg = sp.zeros(8, 8); c = 0
for i in range(8):
    for j in range(i, 8):
        Hg[i, j] = Hg[j, i] = hs[c]; c += 1
eqs = []
for F in FLIPS:
    P = perm_matrix(F); eqs += list(P * Hg - Hg * P)
sol = sp.solve(eqs, hs, dict=True)[0]
Hc = Hg.subs(sol)
free = sorted(Hc.free_symbols, key=str)
diag_ok = all(sp.simplify((W[S].T * Hc * W[T])[0]) == 0 for S in SUBSETS for T in SUBSETS if S != T)
check(f"an operator commutes with every bit flip iff it is diagonal in the Walsh basis: "
      f"{len(free)} free parameters (one eigenvalue per Walsh function), all off-diagonal Walsh entries vanish",
      len(free) == 8 and diag_ok)
Acube = sp.zeros(8, 8)
for s in CORNERS:
    for t in CORNERS:
        if sum(a != b for a, b in zip(s, t)) == 1:
            Acube[idx[s], idx[t]] = 1
check("cube graph: A w_S = (3 - 2|S|) w_S and the Laplacian L = 3I - A has L w_S = 2|S| w_S (O'Donnell 2014)",
      all(Acube * W[S] == (3 - 2 * grade[S]) * W[S] for S in SUBSETS)
      and all((3 * sp.eye(8) - Acube) * W[S] == 2 * grade[S] * W[S] for S in SUBSETS))

print()
print("=" * 78)
print("B. The pixel's symmetry T_d pairs the Walsh grades")
print("=" * 78)
check(f"T_d (signed permutations keeping TetA) has 24 elements, and keeps TetB; O_h = T_d x {{I, -I}} has 48",
      len(TD) == 24 and all(maps_to(g, s) in TETB for g in TD for s in TETB) and len(OH) == 48
      and all([[-e for e in row] for row in g] not in TD for g in TD))
def cls_of(g):
    M = sp.Matrix(g); return {(3, 1): "E", (0, 1): "C3", (-1, 1): "C2", (-1, -1): "S4", (1, -1): "sd"}[(M.trace(), M.det())]
IRR = {"A1": dict(E=1, C3=1, C2=1, S4=1, sd=1), "A2": dict(E=1, C3=1, C2=1, S4=-1, sd=-1),
       "E": dict(E=2, C3=-1, C2=2, S4=0, sd=0), "T1": dict(E=3, C3=0, C2=-1, S4=1, sd=-1),
       "T2": dict(E=3, C3=0, C2=-1, S4=-1, sd=1)}
CL = [cls_of(g) for g in TD]
def decompose(chars):
    return {k: sp.Rational(sum(c * v[x] for c, x in zip(chars, CL)), 24) for k, v in IRR.items()}
def span_char(vecs, g):
    """character of g on the span of vecs (assumed invariant)."""
    B = sp.Matrix.hstack(*vecs); P = perm_matrix(g)
    X = (B.T * B).inv() * B.T * P * B
    return X.trace()
corner_dec = decompose([perm_matrix(g).trace() for g in TD])
check("the 8 corners carry 2A1 + 2T2 under T_d", corner_dec == {"A1": 2, "A2": 0, "E": 0, "T1": 0, "T2": 2})
check("grades 0 and 3 (1 and xyz) are each T_d-invariant: they span the A1 part",
      all(perm_matrix(g) * W[S] == W[S] for g in TD for S in [(), (0, 1, 2)]))
g1 = [W[(0,)], W[(1,)], W[(2,)]]; g2 = [W[(1, 2)], W[(0, 2)], W[(0, 1)]]
inv_span = lambda vecs: all(sp.Matrix.hstack(*vecs, perm_matrix(g) * v).rank() == len(vecs) for g in TD for v in vecs)
check("grade 1 (x, y, z) and grade 2 (yz, xz, xy) are each T_d-invariant and each carries T2",
      inv_span(g1) and inv_span(g2)
      and decompose([span_char(g1, g) for g in TD])["T2"] == 1 and decompose([span_char(g2, g) for g in TD])["T2"] == 1)
check("multiplying by xyz maps grade 1 onto grade 2 (x -> yz, y -> xz, z -> xy) and commutes with T_d",
      all(sp.matrix_multiply_elementwise(W[(0, 1, 2)], W[(d,)]) == W[tuple(sorted(set(range(3)) - {d}))] for d in range(3))
      and all(perm_matrix(g) * sp.diag(*W[(0, 1, 2)]) == sp.diag(*W[(0, 1, 2)]) * perm_matrix(g) for g in TD))
check("with full cube symmetry O_h the four grades are four different representations (spatial inversion "
      "-I gives grade |S| the sign (-1)^|S|), so no O_h-invariant operator mixes grades",
      all(perm_matrix([[-1, 0, 0], [0, -1, 0], [0, 0, -1]]) * W[S] == (-1) ** grade[S] * W[S] for S in SUBSETS))

# the general T_d-invariant real symmetric operator on the corners
pair_orbits = {}
for a in range(8):
    for b in range(a + 1, 8):
        key = frozenset(frozenset((idx[maps_to(g, CORNERS[a])], idx[maps_to(g, CORNERS[b])])) for g in TD)
        pair_orbits.setdefault(key, []).append((a, b))
def orbit_name(pairs):
    a, b = pairs[0]; s, t = CORNERS[a], CORNERS[b]
    d2 = sum((x - y) ** 2 for x, y in zip(s, t)); inA = s in TETA
    return {8: "h_AA" if inA else "h_BB", 4: "h_e", 12: "h_d"}[d2]
eA, eB = sp.symbols("epsilon_A epsilon_B", real=True)
hn = {n: sp.Symbol(n, real=True) for n in ("h_AA", "h_BB", "h_e", "h_d")}
H = sp.zeros(8, 8)
for s in CORNERS:
    H[idx[s], idx[s]] = eA if s in TETA else eB
for key, pairs in pair_orbits.items():
    for (a, b) in pairs:
        H[a, b] = H[b, a] = hn[orbit_name(pairs)]
check(f"the most general T_d-invariant real symmetric operator on the corners has 6 parameters: corner energies "
      f"eps_A, eps_B; couplings h_AA, h_BB (face diagonals in a chamber), h_e (cube edges), h_d (body diagonals)",
      len(pair_orbits) == 4 and sorted(orbit_name(p) for p in pair_orbits.values()) == ["h_AA", "h_BB", "h_d", "h_e"]
      and all(perm_matrix(g) * H == H * perm_matrix(g) for g in TD))
# chamber basis
uA = sp.Matrix([1 if s in TETA else 0 for s in CORNERS]) / 2
uB = sp.Matrix([1 if s in TETB else 0 for s in CORNERS]) / 2
fA = [sp.Matrix([s[d] if s in TETA else 0 for s in CORNERS]) / 2 for d in range(3)]
fB = [sp.Matrix([s[d] if s in TETB else 0 for s in CORNERS]) / 2 for d in range(3)]
Q = sp.Matrix.hstack(uA, uB, *[v for d in range(3) for v in (fA[d], fB[d])])
blocks = (Q.T * H * Q).applyfunc(sp.expand)
alphaA, alphaB, beta = eA + 3 * hn["h_AA"], eB + 3 * hn["h_BB"], 3 * hn["h_e"] + hn["h_d"]
gammaA, gammaB, delta = eA - hn["h_AA"], eB - hn["h_BB"], hn["h_e"] - hn["h_d"]
Bexp = sp.diag(sp.Matrix([[alphaA, beta], [beta, alphaB]]), *[sp.Matrix([[gammaA, delta], [delta, gammaB]])] * 3)
check("Q orthonormal, and in the chamber basis H = [[eps_A + 3h_AA, 3h_e + h_d], [3h_e + h_d, eps_B + 3h_BB]] on A1 "
      "plus three copies of [[eps_A - h_AA, h_e - h_d], [h_e - h_d, eps_B - h_BB]] on T2",
      Q.T * Q == sp.eye(8) and (blocks - Bexp).applyfunc(sp.expand) == sp.zeros(8, 8))
check("Walsh grades in the chamber basis: 1 = sqrt2 (uA + uB), xyz = sqrt2 (uA - uB), x = fA_x + fB_x, yz = fA_x - fB_x",
      W[()] == 2 * (uA + uB) and W[(0, 1, 2)] == 2 * (uA - uB) and W[(0,)] == 2 * (fA[0] + fB[0])
      and W[(1, 2)] == 2 * (fA[0] - fB[0]))
# iff condition for Walsh eigenmodes
conds = []
for S in SUBSETS:
    v = W[S]; lam = (v.T * H * v)[0] / 8
    conds += [sp.expand(e) for e in (H * v - lam * v)]
conds = [e for e in conds if e != 0]
solW = sp.solve(conds, [eB, hn["h_BB"]], dict=True)
check("every Walsh function is an eigenmode of H iff eps_A = eps_B and h_AA = h_BB (TetA and TetB alike); "
      "the A-B couplings h_e, h_d are unrestricted",
      solW == [{eB: eA, hn["h_BB"]: hn["h_AA"]}])
check("and then the eigenvalues are: 1 -> alpha + beta, xyz -> alpha - beta, grade 1 -> gamma + delta, "
      "grade 2 -> gamma - delta (alpha = eps + 3h_AA, beta = 3h_e + h_d, gamma = eps - h_AA, delta = h_e - h_d)",
      all(sp.expand((H * W[S] - lam * W[S]).subs(solW[0])) == sp.zeros(8, 1) for S, lam in
          [((), alphaA + beta), ((0, 1, 2), alphaA - beta), ((0,), gammaA + delta), ((1, 2), gammaA - delta)]))
th = sp.Symbol("theta", real=True)
a_, b_, c_ = sp.symbols("a b c", real=True)
M2 = sp.Matrix([[a_, c_], [c_, b_]])
vth = sp.Matrix([sp.cos(th), sp.sin(th)])
resid = sp.simplify((M2 * vth)[1] * vth[0] - (M2 * vth)[0] * vth[1])
check("mixing: (cos t, sin t) in the chamber basis is an eigenvector of [[a, c], [c, b]] iff "
      "(b - a) sin 2t / 2 + c cos 2t = 0, i.e. tan 2t = 2c/(a - b); Walsh content: weight of 1 (resp. x) "
      "is (cos t + sin t)^2/2", sp.simplify(resid - ((b_ - a_) * sp.sin(2 * th) / 2 + c_ * sp.cos(2 * th))) == 0)
# grade pairing when TetA != TetB, generic mixing
val = {eA: 0, eB: 1, hn["h_AA"]: sp.Rational(1, 3), hn["h_BB"]: sp.Rational(-1, 5), hn["h_e"]: 1, hn["h_d"]: sp.Rational(1, 2)}
Hn = H.subs(val)
mixes = [sp.simplify((W[()].T * Hn * W[(0, 1, 2)])[0]) != 0, sp.simplify((W[(0,)].T * Hn * W[(1, 2)])[0]) != 0]
cross = [sp.simplify((W[S].T * Hn * W[T])[0]) for S in SUBSETS for T in SUBSETS
         if S != T and not ({grade[S], grade[T]} in ({0, 3}, {1, 2}) and (len(S) + len(T) == 3) and
                            set(S) | set(T) == {0, 1, 2} and not set(S) & set(T))]
check("when TetA and TetB differ, H mixes exactly the pairs 1 <-> xyz and x <-> yz, y <-> xz, z <-> xy "
      "(the pairs related by multiplying by xyz) and nothing else (exact point)",
      all(mixes) and all(cv == 0 for cv in cross))

print()
print("=" * 78)
print("C. The vortices are built from the direction modes")
print("=" * 78)
# the 15-site pixel: O, octahedron vertices, corners
OCT = [tuple(v) for v in ([1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1])]
PIX = [(0, 0, 0)] + OCT + CORNERS
pidx = {s: k for k, s in enumerate(PIX)}
def pperm(g):
    P = sp.zeros(15, 15)
    for s in PIX:
        P[pidx[maps_to(g, s)], pidx[s]] = 1
    return P
pix_dec = decompose([pperm(g).trace() for g in TD])
oct_dec = decompose([sum(1 for s in OCT if maps_to(g, s) == s) for g in TD])
check("the octahedron's six vertices carry A1 + E + T2, and the 15-site pixel carries 4A1 + E + 3T2 "
      "(two T2 copies on the corners, one on the octahedron)",
      oct_dec == {"A1": 1, "A2": 0, "E": 1, "T1": 0, "T2": 1}
      and pix_dec == {"A1": 4, "A2": 0, "E": 1, "T1": 0, "T2": 3})
S4 = [[0, -1, 0], [1, 0, 0], [0, 0, -1]]
PS = pperm(S4)
Vi = (PS - sp.I * sp.eye(15)).nullspace()
def iso_projector(name):
    chi = IRR[name]
    return sum((sp.Rational(chi["E"], 24) * chi[cls_of(g)] * pperm(g) for g in TD), sp.zeros(15, 15))
PT2, PA1, PE = iso_projector("T2"), iso_projector("A1"), iso_projector("E")
check("the rotoreflection S has eigenvalue +i only in the T2 part: V_{+i} has dimension 3, lies in the T2 "
      "isotypic part, and A1 and E contain no +i vector (S acts on them with eigenvalues 1 and +-1)",
      len(Vi) == 3 and all((PT2 * v - v).applyfunc(sp.simplify) == sp.zeros(15, 1) for v in Vi)
      and (PS * PA1 - PA1).applyfunc(sp.simplify) == sp.zeros(15, 15)
      and ((PS * PS - sp.eye(15)) * PE).applyfunc(sp.simplify) == sp.zeros(15, 15))
corner_rows = [pidx[s] for s in CORNERS]
check("so on the corners every winding state (hence every vortex) has no grade-0 or grade-3 component: "
      "its corner part is a combination of the direction modes x, y, z, yz, xz, xy",
      all(sp.simplify((W[S].T * sp.Matrix([v[r] for r in corner_rows]))[0]) == 0 for v in Vi for S in [(), (0, 1, 2)]))
# Proposition: on the bare cube the degenerate grade-1 modes combine into a circulating state
t_ = sp.Symbol("t", positive=True)
Hcube = t_ * Acube
psi = W[(0,)] + sp.I * W[(1,)]
C4 = [[0, -1, 0], [1, 0, 0], [0, 0, 1]]
def flux_phys(H_, psi_, edges, u):
    """total physical flow through the half-plane {z-axis, direction u}, right-handed about +z."""
    tot = 0
    for (a, b) in edges:
        pa, pb = CORNERS[a], CORNERS[b]
        sa = -u[1] * pa[0] + u[0] * pa[1]; sb = -u[1] * pb[0] + u[0] * pb[1]   # side of the plane spanned by z, u
        assert sa != 0 and sb != 0
        if sa * sb < 0:
            tt = sp.Rational(sa, sa - sb)
            xp = [pa[k] + tt * (pb[k] - pa[k]) for k in range(3)]
            if u[0] * xp[0] + u[1] * xp[1] > 0:
                i, j = (a, b) if sa < 0 else (b, a)                             # crossing i -> j in the positive sense
                tot += 2 * sp.im(sp.conjugate(psi_[j]) * H_[j, i] * psi_[i])
    return sp.simplify(tot)
cube_edges = [(a, b) for a in range(8) for b in range(a + 1, 8) if Acube[a, b]]
fl = [flux_phys(Hcube, psi, cube_edges, u) for u in ((2, 1), (1, 3), (-1, 2))]
check("Proposition 1: on the cube graph (H = t A, full cube symmetry), x + i y is an eigenmode at the doubly "
      "degenerate grade-1 energy t, winds under the quarter turn C4 about z (C4 psi = -i psi), and carries the "
      f"same nonzero current {fl[0]} through three half-planes; x and y alone carry none",
      (Hcube * psi - t_ * psi).expand() == sp.zeros(8, 1) and (perm_matrix(C4) * psi + sp.I * psi).expand() == sp.zeros(8, 1)
      and fl[0] != 0 and fl[0] == fl[1] == fl[2]
      and all(flux_phys(Hcube, W[(d,)], cube_edges, (2, 1)) == 0 for d in (0, 1)))

print()
print("=" * 78)
print("D. Closure reads exactly the direction modes")
print("=" * 78)
rs = sp.symbols("r0:12")
R = sp.Matrix(3, 4, rs)
def tet_perm(g, T):
    P = sp.zeros(4, 4)
    for k, s in enumerate(T):
        P[T.index(maps_to(g, s)), k] = 1
    return P
eqsR = []
for g in TD:
    eqsR += list(R * tet_perm(g, TETA) - sp.Matrix(g) * R)
solR = sp.solve(eqsR, rs, dict=True)[0]
Rg = R.subs(solR)
frame = sp.Matrix.hstack(*[sp.Matrix(s) for s in TETA])          # Letter 1's legs v_1..v_4 as columns
free_R = sorted(Rg.free_symbols, key=str)
check("Theorem 3: every T_d-equivariant linear map from TetA's four corner amplitudes to a 3-vector is a "
      "multiple of the frame readout psi -> sum_i psi_i v_i (one free constant, Schur)",
      len(free_R) == 1 and Rg[0, 0] != 0
      and (Rg - (Rg[0, 0] / frame[0, 0]) * frame).applyfunc(sp.simplify) == sp.zeros(3, 4))
check("the frame readout annihilates the uniform mode exactly because of closure v1 + v2 + v3 + v4 = 0, and is "
      "injective on the sum-zero (T2) modes: it reads those and only those",
      frame * sp.ones(4, 1) == sp.zeros(3, 1) and frame.rank() == 3)
check("on TetA the direction modes are the Walsh functions: the frame's rows are x, y, z on TetA, and there "
      "x = yz, y = xz, z = xy (the collapse of the Hadamard cube frame proof)",
      all(frame[d, k] == TETA[k][d] for d in range(3) for k in range(4))
      and all(s[0] == s[1] * s[2] and s[1] == s[0] * s[2] and s[2] == s[0] * s[1] for s in TETA))
rs8 = sp.symbols("q0:24"); R8 = sp.Matrix(3, 8, rs8)
eqs8 = []
for g in TD:
    eqs8 += list(R8 * perm_matrix(g) - sp.Matrix(g) * R8)
R8g = R8.subs(sp.solve(eqs8, rs8, dict=True)[0])
grade1_read = sp.Matrix([[s[d] for s in CORNERS] for d in range(3)])
grade2_read = sp.Matrix([[s[d] * s[0] * s[1] * s[2] for s in CORNERS] for d in range(3)])
check("on all eight corners the T_d-equivariant direction readouts form a 2-dimensional space, spanned by the "
      "grade-1 readout (sum psi_k s_k) and the grade-2 readout (sum psi_k xyz(s_k) s_k), i.e. by the TetA "
      "and TetB frames",
      len(R8g.free_symbols) == 2 and
      all(any(sp.solve(list(R8g - grade1_read * a1 - grade2_read * a2), list(R8g.free_symbols), dict=True)) for a1, a2 in [(1, 0), (0, 1)]))
check("both readouts vanish on the A1 modes (1 and xyz) and are blind to them; every T_d-equivariant scalar "
      "readout, conversely, sees only 1 and xyz (it is constant on each chamber)",
      grade1_read * W[()] == sp.zeros(3, 1) and grade1_read * W[(0, 1, 2)] == sp.zeros(3, 1)
      and grade2_read * W[()] == sp.zeros(3, 1) and grade2_read * W[(0, 1, 2)] == sp.zeros(3, 1)
      and len(sp.Matrix(1, 8, sp.symbols("z0:8")).subs(sp.solve(
          sum((list(sp.Matrix(1, 8, sp.symbols("z0:8")) * perm_matrix(g) - sp.Matrix(1, 8, sp.symbols("z0:8"))) for g in TD), []),
          sp.symbols("z0:8"), dict=True)[0]).free_symbols) == 2)

print()
print("=" * 78)
print("E. What the oscillator node's closure reads (research/universe-is-pixelated/octahedral_node.py)")
print("=" * 78)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "research", "universe-is-pixelated"))
import octahedral_node as on
import random, math
check("the node's corner order and Walsh table match: its TetA indices [0,3,5,6] are the xyz = +1 corners and "
      "its 8 Walsh columns are 1, x, y, z, xy, xz, yz, xyz",
      [k for k, s in enumerate(on.SIGNS) if s[0] * s[1] * s[2] == 1] == on.TETA_IDX
      and all(on.H[k] == [1, s[0], s[1], s[2], s[0] * s[1], s[0] * s[2], s[1] * s[2], s[0] * s[1] * s[2]]
              for k, s in enumerate(on.SIGNS)))
vs = sp.symbols("v0:8")
coef = [sum(on.H[k][cc] * vs[k] for k in range(8)) / 8 for cc in range(8)]
mu_node = (1 + coef[7] / coef[0]) / 2
SA = sum(vs[k] for k in on.TETA_IDX); SB = sum(vs[k] for k in on.TETB_IDX)
check("Theorem 4(i): the node's mu = (1 + c_xyz / c_1)/2 is the TetA share S_A/(S_A + S_B) of the vertex state",
      sp.simplify(mu_node - SA / (SA + SB)) == 0)
dirs = sp.symbols("d0:6")
shift = [sum(dirs[i] * on.H[k][1 + i] for i in range(6)) for k in range(8)]
check("so mu reads only the A1 modes (grades 0 and 3): adding any combination of the six direction modes "
      "x, y, z, xy, xz, yz to the vertex state leaves mu unchanged, so mu is blind to every vortex",
      sp.simplify(mu_node.subs({vs[k]: vs[k] + shift[k] for k in range(8)}, simultaneous=True) - mu_node) == 0)
check("Theorem 4(ii), Parseval: the energy sum_k v_k^2 that drives the closure equals 8 sum_c c_c^2, the total "
      "Walsh power",
      sp.expand(sum(v ** 2 for v in vs) - 8 * sum(cc ** 2 for cc in coef)) == 0)
thp = sp.Symbol("theta", positive=True); xg = sp.Symbol("x", positive=True)
modeA1 = sp.cos(thp) * uA + sp.sin(thp) * uB
vals = {vs[k]: modeA1[idx[tuple(on.SIGNS[k])]] for k in range(8)}
mu_mode = sp.simplify(mu_node.subs(vals))
check("for an eigenmode (cos t, sin t) of the A1 block the node's mu is 1/(1 + tan t); hence mu = x/(1 + x) "
      "exactly when tan t = 1/x (the test linking the A1 mixing angle to the constitutive law)",
      sp.simplify(mu_mode - 1 / (1 + sp.tan(thp))) == 0
      and sp.simplify((1 / (1 + sp.tan(thp))).subs(thp, sp.atan(1 / xg)) - xg / (1 + xg)) == 0)
random.seed(7)
ok_target = ok_contract = ok_parseval = True; ticks = 0
for standing in (True, False):
    node = on.OctahedralNode(standing=standing)
    for n_ in range(400):
        node.inject([random.uniform(-1, 1) for _ in range(3)])
        a0 = list(node.amp_a); b0 = list(node.amp_b); r = node.closure_rate
        node.tick(); ticks += 1
        mean_e = (node.energy_a + node.energy_b) / (2 * on.N)
        fw = [sum(on.H[k][cc] * node.forward_mix[k] for k in range(8)) / 8 for cc in range(8)]
        bw = [sum(on.H[k][cc] * node.backward_mix[k] for k in range(8)) / 8 for cc in range(8)]
        ok_parseval &= abs(mean_e - (8 * sum(x * x for x in fw) + 8 * sum(x * x for x in bw)) / (2 * on.N)) < 1e-9 * max(1, mean_e)
        rr = math.sqrt(max(mean_e, 1e-12))
        tgt = rr / (1 + rr) if standing else min(rr, 5.0)
        unclamped = all(0.01 < x < 5.0 for x in node.amp_a + node.amp_b)
        if unclamped:
            ok_target &= all(abs(node.amp_a[k] - (a0[k] + r * (tgt - a0[k]))) < 1e-12 for k in range(8))
            ok_contract &= all(abs((node.amp_a[k] - node.amp_a[0]) - (1 - r) * (a0[k] - a0[0])) < 1e-12 for k in range(8))
check(f"the node's amplitude closure, run for {ticks} ticks in both modes: every corner relaxes toward the same "
      "target, a function of the total Walsh power only (r/(1+r) bounded, min(r, 5) original; r^2 = mean power)",
      ok_target and ok_parseval)
check("so the spread between corner amplitudes contracts by exactly (1 - rate) = 0.98 per tick, whatever the "
      "signal: the closure drives the carrier toward equal amplitudes and cannot favour any Walsh mode",
      ok_contract)
node = on.OctahedralNode(standing=True)
def carrier_coeffs(a):
    node.amp_a = [a] * 8
    wave = [node.amp_a[k] * math.sin(node.freq_a[k] * 3.7 + node.phase_a[k]) for k in range(8)]
    return [sum(on.H[k][cc] * wave[k] for k in range(8)) / 8 for cc in range(8)]
c1, c2 = carrier_coeffs(0.3), carrier_coeffs(0.9)
check("at equal amplitudes a closure step rescales the carrier's whole Walsh spectrum by one factor: the 8 "
      "coefficients at amplitude 0.9 are exactly 3 times those at 0.3, so the spectrum's shape is kept",
      all(abs(y - 3 * x) < 1e-12 for x, y in zip(c1, c2)))

print()
print(f"{PASS}/{PASS + FAIL} checks passed")
raise SystemExit(FAIL)
