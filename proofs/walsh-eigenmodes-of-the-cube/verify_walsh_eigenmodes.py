#!/usr/bin/env python3
"""
Verification: The Walsh Eigenmodes of the Cube, and What Field Closure Reads
=============================================================================

Every statement of the proof is checked here, exactly (sympy, in all
parameters, or exhaustively over finite sets), except Part E, which runs the
archive's octahedral resonance node itself and checks identities of its code.

  A. The Walsh functions are the cube's eigenmodes (Theorem 1).
  B. T_d pairs the Walsh grades on the cube (Theorem 2), and in the pixel (Proposition 1).
  C. The vortices are built from the T2 modes (Corollary 1, Proposition 2).
  D. What frame closure and field closure read (Theorem 3).
  E. What the oscillator node's closure rule reads (Theorem 4).
  F. mu and the mixing angle: the linear and quadratic readings (Proposition 3).

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
print("B. T_d pairs the Walsh grades: on the cube, and in the pixel")
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
print("C. The vortices are built from the T2 modes")
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
def iso_projector(name):
    chi = IRR[name]
    return sum((sp.Rational(chi["E"], 24) * chi[cls_of(g)] * pperm(g) for g in TD), sp.zeros(15, 15))
PT2, PA1, PE = iso_projector("T2"), iso_projector("A1"), iso_projector("E")
corner_rows = [pidx[s] for s in CORNERS]; rest_rows = [k for k in range(15) if k not in corner_rows]
# the pixel's Hamiltonians (the vortex proof's class, with the octahedron's edges)
pe = dict(zip(("eO", "ef", "eA", "eB", "tf", "tA", "tB", "cA", "cB", "h"),
              sp.symbols("e_O e_f e_A e_B t_f t_A t_B c_A c_B h", real=True)))
def H_pixel(p_):
    Hp = sp.zeros(15, 15); Hp[0, 0] = p_["eO"]
    for v in OCT:
        i = pidx[v]; Hp[i, i] = p_["ef"]; Hp[0, i] = Hp[i, 0] = -p_["tf"]
        for w in OCT:
            if sum(a * b for a, b in zip(v, w)) == 0:
                Hp[i, pidx[w]] = -p_["h"]
    for c_ in CORNERS:
        k = pidx[c_]; A_ = c_ in TETA
        Hp[k, k] = p_["eA"] if A_ else p_["eB"]; Hp[0, k] = Hp[k, 0] = -(p_["tA"] if A_ else p_["tB"])
        for v in OCT:
            if sum(a * b for a, b in zip(v, c_)) == 1:
                Hp[pidx[v], k] = Hp[k, pidx[v]] = -(p_["cA"] if A_ else p_["cB"])
    return Hp
Hpix = H_pixel(pe)
check("the pixel Hamiltonian (Field Origin, octahedron with its edges, corners; 10 parameters) is T_d-invariant",
      all(pperm(g) * Hpix == Hpix * pperm(g) for g in TD))
Pinv = pperm([[-1, 0, 0], [0, -1, 0], [0, 0, -1]])
Hoh = Hpix.subs({pe["eB"]: pe["eA"], pe["tB"]: pe["tA"], pe["cB"]: pe["cA"]})
Qs = {0: PA1 * (sp.eye(15) + Pinv) / 2, 3: PA1 * (sp.eye(15) - Pinv) / 2,
      1: PT2 * (sp.eye(15) - Pinv) / 2, 2: PT2 * (sp.eye(15) + Pinv) / 2}
grade_proj = {g_: sum((W[S] * W[S].T / 8 for S in SUBSETS if grade[S] == g_), sp.zeros(8, 8)) for g_ in range(4)}
pure = all((Qs[g_] * Hoh - Hoh * Qs[g_]).applyfunc(sp.expand) == sp.zeros(15, 15)
           and ((sp.eye(8) - grade_proj[g_]) * Qs[g_].extract(corner_rows, list(range(15)))).applyfunc(sp.simplify)
           == sp.zeros(8, 15) for g_ in range(4))
check("Proposition 1(i) [pixel, TetA and TetB alike]: the four projectors (T_d type x inversion parity) commute with "
      "every O_h-invariant pixel H, and the corner part of each lies in one Walsh grade (0: A1 even, 3: A1 odd, "
      "1: T2 odd, 2: T2 even); so the pixel has an eigenbasis whose corner parts are pure Walsh grades", pure)
import numpy as np
num = {pe["eO"]: 0.1, pe["ef"]: -0.2, pe["eA"]: 0.0, pe["eB"]: 1.0, pe["tf"]: 0.5, pe["tA"]: 0.7, pe["tB"]: 0.4,
       pe["cA"]: 1.0, pe["cB"]: 0.6, pe["h"]: 0.3}
Hn_pix = np.array(Hpix.subs(num).tolist(), dtype=float)
Ev, Vv = np.linalg.eigh(Hn_pix)
Wn = {S: np.array(W[S].tolist(), dtype=float).ravel() for S in SUBSETS}
PT2n = np.array(PT2.tolist(), dtype=float)
shares, eff_ok = [], True
Hcc = Hn_pix[np.ix_(corner_rows, corner_rows)]; Hcr = Hn_pix[np.ix_(corner_rows, rest_rows)]; Hrr = Hn_pix[np.ix_(rest_rows, rest_rows)]
for e_, v_ in zip(Ev, Vv.T):
    if np.linalg.norm(PT2n @ v_ - v_) < 1e-9:
        cpart = v_[corner_rows]
        w1 = sum((Wn[S] @ cpart) ** 2 for S in SUBSETS if grade[S] == 1); w2 = sum((Wn[S] @ cpart) ** 2 for S in SUBSETS if grade[S] == 2)
        shares.append(round(w1 / (w1 + w2), 4))
        Heff = Hcc + Hcr @ np.linalg.solve(e_ * np.eye(7) - Hrr, Hcr.T)
        eff_ok &= np.linalg.norm(Heff @ cpart - e_ * cpart) < 1e-9 * max(1, np.linalg.norm(cpart))
shares = sorted(set(shares))
check(f"Proposition 1(ii) [pixel, TetA and TetB differ; numerical, 1e-9]: each T2 eigenmode's corner part is an "
      f"eigenvector of the energy-dependent corner operator H_eff(E) = H_cc + H_cr (E - H_rr)^-1 H_rc, so its "
      f"grade-1/grade-2 mix depends on the mode: shares {shares} at one parameter point", eff_ok and len(shares) == 3)
Heff_sym_ok = all(np.allclose(np.array(perm_matrix(g).tolist(), dtype=float) @ (Hcc + Hcr @ np.linalg.solve(0.37 * np.eye(7) - Hrr, Hcr.T)),
                              (Hcc + Hcr @ np.linalg.solve(0.37 * np.eye(7) - Hrr, Hcr.T)) @ np.array(perm_matrix(g).tolist(), dtype=float))
                  for g in TD)
check("and H_eff(E) is T_d-invariant (it is built from T_d-invariant blocks; checked at E = 0.37), so it has the cube's block form (Theorem 2) "
      "with E-dependent entries: the pairing holds in the pixel, mode by mode", Heff_sym_ok)
S4 = [[0, -1, 0], [1, 0, 0], [0, 0, -1]]
PS = pperm(S4)
Vi = (PS - sp.I * sp.eye(15)).nullspace()
check("the rotoreflection S has eigenvalue +i only in the T2 part: V_{+i} has dimension 3, lies in the T2 "
      "isotypic part, and A1 and E contain no +i vector (S acts on them with eigenvalues 1 and +-1)",
      len(Vi) == 3 and all((PT2 * v - v).applyfunc(sp.simplify) == sp.zeros(15, 1) for v in Vi)
      and (PS * PA1 - PA1).applyfunc(sp.simplify) == sp.zeros(15, 15)
      and ((PS * PS - sp.eye(15)) * PE).applyfunc(sp.simplify) == sp.zeros(15, 15))
check("so on the corners every winding state (hence every vortex) has no grade-0 or grade-3 component: "
      "its corner part is a combination of the six T2 modes x, y, z, yz, xz, xy",
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
check("Proposition 2: on the cube graph (H = t A, full cube symmetry), x + i y is an eigenmode at the triply "
      "degenerate grade-1 energy t (x, y, z), winds under the quarter turn C4 about z (C4 psi = -i psi), and carries the "
      f"same nonzero current {fl[0]} through three half-planes; x and y alone carry none",
      (Hcube * psi - t_ * psi).expand() == sp.zeros(8, 1) and (perm_matrix(C4) * psi + sp.I * psi).expand() == sp.zeros(8, 1)
      and fl[0] != 0 and fl[0] == fl[1] == fl[2]
      and all(flux_phys(Hcube, W[(d,)], cube_edges, (2, 1)) == 0 for d in (0, 1)))

print()
print("=" * 78)
print("D. What frame closure and field closure read")
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
check("Theorem 3(i): every T_d-equivariant linear map from TetA's four corner amplitudes to a 3-vector is a "
      "multiple of the frame readout psi -> sum_i psi_i v_i (one free constant, Schur)",
      len(free_R) == 1 and Rg[0, 0] != 0
      and (Rg - (Rg[0, 0] / frame[0, 0]) * frame).applyfunc(sp.simplify) == sp.zeros(3, 4))
orbit_v1 = {maps_to(g, TETA[0]) for g in TD}
check("Theorem 3(ii): closure v1 + v2 + v3 + v4 = 0 is the same equation as the frame readout's blindness to the "
      "constant mode (frame * 1 = sum v_i); with T_d it also follows from the orbit sum (the legs are one T_d-orbit "
      "and T_d fixes no nonzero vector). The readout is injective on the sum-zero modes",
      orbit_v1 == set(TETA) and sp.Matrix.hstack(*[sp.Matrix(g) - sp.eye(3) for g in TD]).rank() == 3
      and frame * sp.ones(4, 1) == sp.zeros(3, 1) and frame.rank() == 3)
# the metric on the eight null directions n_v = (1, v/sqrt3) (coupling algebra, Result 9)
Geta = sp.Matrix(8, 8, lambda i, j: -1 + sp.Rational(1, 3) * sum(CORNERS[i][k] * CORNERS[j][k] for k in range(3)))
check("the metric read on the eight null directions has eigenvalue -8 on the constant mode (time), 8/3 on the "
      "vector modes (space) and 0 on the bivector modes and the chamber sign: the four modes it cannot see "
      "(coupling algebra, Result 9)",
      all(Geta * W[S] == {0: -8, 1: sp.Rational(8, 3), 2: 0, 3: 0}[grade[S]] * W[S] for S in SUBSETS))
# readouts of one root and of both roots, on all 8 corners
SA_row = sp.Matrix([[1 if s in TETA else 0 for s in CORNERS]]); SB_row = sp.Matrix([[1 if s in TETB else 0 for s in CORNERS]])
RA = sp.Matrix([[s[d] if s in TETA else 0 for s in CORNERS] for d in range(3)])
RB = sp.Matrix([[s[d] if s in TETB else 0 for s in CORNERS] for d in range(3)])
one_root = sp.Matrix.vstack(SA_row, RA); both = sp.Matrix.vstack(SA_row, SB_row, RA, RB)
Wmat = sp.Matrix.hstack(*[W[S] for S in SUBSETS])
check("Theorem 3(iii), one root: TetA's readouts (its sum S_A and its frame) have rank 4 on the 8 corners, kill "
      "every amplitude on TetB and cannot tell w_S from its complement (the collapse of the Hadamard cube frame "
      "proof); they read the four modes 1, x, y, z (time and space on the null cone), half of the spectrum",
      one_root.rank() == 4 and all(one_root * W[S] == one_root * W[tuple(sorted(set(range(3)) - set(S)))] for S in SUBSETS))
check("Theorem 3(iv), field closure (both roots active): S_A, S_B and the TetA and TetB frames together form an "
      "invertible 8 x 8 readout, so they read all eight Walsh functions; S_A, S_B read exactly 1 and xyz, and "
      "the two frames exactly the six T2 modes",
      both.det() != 0 and (sp.Matrix.vstack(SA_row, SB_row) * Wmat).extract([0, 1], [i for i, S in enumerate(SUBSETS) if grade[S] in (1, 2)]) == sp.zeros(2, 6)
      and (sp.Matrix.vstack(RA, RB) * Wmat).extract(list(range(6)), [i for i, S in enumerate(SUBSETS) if grade[S] in (0, 3)]) == sp.zeros(6, 2))
rs8 = sp.symbols("q0:24"); R8 = sp.Matrix(3, 8, rs8)
eqs8 = []
for g in TD:
    eqs8 += list(R8 * perm_matrix(g) - sp.Matrix(g) * R8)
R8g = R8.subs(sp.solve(eqs8, rs8, dict=True)[0])
zs = sp.symbols("z0:8"); Z = sp.Matrix(1, 8, zs)
Zg = Z.subs(sp.solve(sum((list(Z * perm_matrix(g) - Z) for g in TD), []), zs, dict=True)[0])
check("and these are all of them: the T_d-equivariant direction readouts of the 8 corners form a 2-dimensional "
      "space (spanned by the two frames) and the invariant scalar readouts a 2-dimensional space (spanned by "
      "S_A and S_B); every equivariant linear readout factors through the field-closed readout",
      len(R8g.free_symbols) == 2 and len(Zg.free_symbols) == 2
      and all(RX * perm_matrix(g) == sp.Matrix(g) * RX for RX in (RA, RB) for g in TD)
      and all(SX * perm_matrix(g) == SX for SX in (SA_row, SB_row) for g in TD)
      and sp.Matrix.vstack(RA, RB).rank() == 6 and sp.Matrix.vstack(SA_row, SB_row).rank() == 2)
vsym = sp.Matrix(sp.symbols("p0:8"))
quad = (RA * vsym).dot(RA * vsym)
check("the split into the two sectors is a property of linear readouts: a quadratic invariant such as the squared "
      "length of TetA's frame readout is a scalar that reads the T2 modes (it is not a function of S_A, S_B)",
      sp.simplify(quad.subs({vsym[k]: Wn_ for k, Wn_ in enumerate(W[(0,)])})) != 0
      and SA_row * W[(0,)] == sp.Matrix([[0]]) and SB_row * W[(0,)] == sp.Matrix([[0]]))
check("mu = S_A / (S_A + S_B) uses S_B: no readout of TetA alone determines it (two states with the same TetA "
      "readouts and different mu)",
      (one_root * sp.Matrix([1 if s in TETA else 0 for s in CORNERS])) == (one_root * sp.Matrix([1 for s in CORNERS])))

print()
print("=" * 78)
print("E. What the oscillator node's closure rule reads (research/universe-is-pixelated/octahedral_node.py)")
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
check("so mu reads only the A1 modes (grades 0 and 3): adding any combination of the six T2 modes "
      "x, y, z, xy, xz, yz to the vertex state leaves mu unchanged",
      sp.simplify(mu_node.subs({vs[k]: vs[k] + shift[k] for k in range(8)}, simultaneous=True) - mu_node) == 0)
check("Theorem 4(ii), Parseval: the quantity sum_k v_k^2 that sets the closure rule's targets equals 8 sum_c c_c^2, "
      "the total Walsh weight",
      sp.expand(sum(v ** 2 for v in vs) - 8 * sum(cc ** 2 for cc in coef)) == 0)
random.seed(7)
ok_target = ok_contract = ok_parseval = ok_out = ok_in = True; ticks = 0
for standing in (True, False):
    node = on.OctahedralNode(standing=standing)
    for n_ in range(400):
        node.inject([random.uniform(-1, 1) for _ in range(3)])
        a0 = list(node.amp_a); b0 = list(node.amp_b); co0 = list(node.coupling_out); r = node.closure_rate
        node.tick(); ticks += 1
        mean_e = (node.energy_a + node.energy_b) / (2 * on.N)
        fw = [sum(on.H[k][cc] * node.forward_mix[k] for k in range(8)) / 8 for cc in range(8)]
        bw = [sum(on.H[k][cc] * node.backward_mix[k] for k in range(8)) / 8 for cc in range(8)]
        ok_parseval &= abs(mean_e - (8 * sum(x * x for x in fw) + 8 * sum(x * x for x in bw)) / (2 * on.N)) < 1e-9 * max(1, mean_e)
        rr = math.sqrt(max(mean_e, 1e-12))
        tgt = rr / (1 + rr) if standing else min(rr, 5.0)
        unclamped = all(0.01 < x < 5.0 for x in node.amp_a + node.amp_b)
        tgt_out = 1.0 if standing else min(rr, 5.0)
        ok_out &= all(abs(node.coupling_out[k] - min(max(co0[k] + r * (tgt_out - co0[k]), 0.01), 5.0)) < 1e-12 for k in range(8))
        ok_in &= all(c == 1.0 for c in node.coupling_in)
        if unclamped:
            ok_target &= all(abs(node.amp_a[k] - (a0[k] + r * (tgt - a0[k]))) < 1e-12 for k in range(8))
            ok_contract &= all(abs((node.amp_a[k] - node.amp_a[0]) - (1 - r) * (a0[k] - a0[0])) < 1e-12 for k in range(8))
check(f"the node's closure rule has three updates. Run for {ticks} ticks in both modes: (1) every corner amplitude "
      "relaxes toward one target, a function of the total Walsh weight only (r/(1+r) bounded, min(r, 5) original; "
      "r^2 = mean square); (2) every outward coupling relaxes toward one target (1 bounded, min(r, 5) original)",
      ok_target and ok_parseval and ok_out)
random.seed(2)
node_in = on.OctahedralNode(standing=True); node_in.coupling_in = [0.5] * 8
for n_ in range(300):
    node_in.inject([random.uniform(-1, 1) for _ in range(3)]); node_in.tick()
spread_in = max(node_in.coupling_in) - min(node_in.coupling_in)
check(f"(3) the inward couplings follow c_k += rate * sign(f_k b_k) (1 - |c_k|): a corner-local, signal-dependent "
      f"rule, inert in the archive only because every c_k starts at its fixed point 1 (all stay 1 over {ticks} "
      f"ticks); started at 0.5 they spread across corners ({spread_in:.4f} after 300 ticks) while relaxing to 1",
      ok_in and spread_in > 1e-4 and min(node_in.coupling_in) > 0.99)
check("so the spread between corner amplitudes contracts by exactly (1 - rate) = 0.98 per tick, whatever the "
      "signal: the closure rule moves the carrier toward equal amplitudes and cannot favour any Walsh mode",
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
print("=" * 78)
print("F. mu and the mixing angle: the linear and quadratic readings")
print("=" * 78)
thp = sp.Symbol("theta", positive=True); xg = sp.Symbol("x", positive=True)
g_, a0_ = sp.symbols("g a_0", positive=True)
modeA1 = sp.cos(thp) * uA + sp.sin(thp) * uB
vals = {vs[k]: modeA1[idx[tuple(on.SIGNS[k])]] for k in range(8)}
mu_mode = sp.simplify(mu_node.subs(vals))
mu_other = sp.simplify(mu_node.subs({vs[k]: (sp.cos(thp) * uB - sp.sin(thp) * uA)[idx[tuple(on.SIGNS[k])]] for k in range(8)}))
check("for the bonding A1 mode (cos t, sin t), 0 < t < pi/2, the node's mu (amplitude share) is 1/(1 + tan t), in "
      "(0, 1); for the antibonding mode (-sin t, cos t) it is 1/(1 - cot t), outside [0, 1]",
      sp.simplify(mu_mode - 1 / (1 + sp.tan(thp))) == 0 and sp.simplify(mu_other - 1 / (1 - 1 / sp.tan(thp))) == 0)
amp_share = sp.cos(thp) / (sp.cos(thp) + sp.sin(thp)); prob_share = sp.cos(thp) ** 2
t_lin = sp.atan(a0_ / g_); t_quad = sp.atan(sp.sqrt(a0_ / g_))
tan2 = lambda T: 2 * T / (1 - T ** 2)          # tan 2t from tan t
check("Proposition 3(i), linear reading (corner values are field values): mu = x/(1+x) with x = g_t/a_0 iff "
      "tan t = a_0/g_t, i.e. the mode is proportional to (g_t, a_0) and the coupling ratio is "
      "beta/(alpha_A - alpha_B) = x/(x^2 - 1)",
      sp.simplify(amp_share.subs(thp, t_lin) - g_ / (g_ + a0_)) == 0
      and sp.simplify(tan2(a0_ / g_) / 2 - (g_ / a0_) / ((g_ / a0_) ** 2 - 1)) == 0)
check("Proposition 3(ii): in the linear reading the mode's two chamber parts, scaled to total g_t, are mu g_t and "
      "(1 - mu) g_t: the TetA part is the TetA partition g_s = mu g_t (Letter 3, kinematic), written out "
      "g_t^2/(g_t + a_0), and the TetB part is the TetB share",
      sp.simplify(g_ * sp.cos(t_lin) / (sp.cos(t_lin) + sp.sin(t_lin)) - (g_ / (g_ + a0_)) * g_) == 0
      and sp.simplify(g_ * sp.sin(t_lin) / (sp.cos(t_lin) + sp.sin(t_lin)) - (a0_ / (g_ + a0_)) * g_) == 0
      and sp.simplify((g_ / (g_ + a0_)) * g_ - g_ ** 2 / (g_ + a0_)) == 0)
check("Proposition 3(i), exchange: x -> 1/x sends tan t = 1/x to tan t = x, i.e. t -> pi/2 - t, swapping the two "
      "chambers' amplitudes, and the TetA share becomes 1 - mu(x) = mu(1/x)",
      sp.simplify(amp_share.subs(thp, sp.atan(xg)) - (1 - xg / (1 + xg))) == 0
      and sp.simplify(sp.cot(sp.atan(1 / xg)) - xg) == 0)
check("Proposition 3(iii), quadratic reading (the field is the intensity): mu = x/(1+x) iff tan t = sqrt(a_0/g_t), "
      "the mode proportional to (sqrt g_t, sqrt a_0), with beta/(alpha_A - alpha_B) = sqrt(x)/(x - 1): exactly the "
      "diamond lattice's bond-orbital dictionary V_3/V_2 = (x - 1)/(2 sqrt x)",
      sp.simplify(prob_share.subs(thp, t_quad) - g_ / (g_ + a0_)) == 0
      and sp.simplify(tan2(sp.sqrt(a0_ / g_)) / 2 - sp.sqrt(g_ / a0_) / (g_ / a0_ - 1)) == 0
      and sp.simplify((1 / ((xg - 1) / (2 * sp.sqrt(xg)))) / 2 - sp.sqrt(xg) / (xg - 1)) == 0)
check("the two readings cannot both hold: if the amplitude share is x/(1+x) the intensity share is x^2/(1+x^2), and "
      "they agree only at x = 1 (t = pi/4, mu = 1/2), where TetA and TetB are alike",
      sp.simplify(prob_share.subs(thp, sp.atan(1 / xg)) - xg ** 2 / (1 + xg ** 2)) == 0
      and sp.solve(sp.Eq(xg ** 2 / (1 + xg ** 2), xg / (1 + xg)), xg) == [1])

print()
print(f"{PASS}/{PASS + FAIL} checks passed")
raise SystemExit(FAIL)
