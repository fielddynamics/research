"""
verify_octahedral_connection.py
===============================

Exact checks for Part II of INTERSECTION_ALGEBRA.md:

  F. An explicit isomorphism PSL2(Z/4) -> O (rotations of the octahedron),
     and where the t-bit states x = 0, 1, infinity land on it.
  G. The 64 connection components as cochains on the level-4 octahedron:
         Gamma = R[D] + 4 R[E] + C^1,   Christoffel = R[D] + 3 R[E],
         torsion = R[E] + C^1,
     with the Hodge split of C^1 and the parity detector as a curl.
  H. The double cover SL2(Z/4) -> S4 that separates 21 from 13: its
     extension class, its character (the multiplier of eta^6), the trace
     table, and the sign-twisted equivariance of the 21/13 labelling.

Requires numpy and sympy (mpmath ships with sympy).  Prints PASS/FAIL per claim.
"""
from __future__ import annotations

import itertools
import math
from collections import Counter

import numpy as np
import mpmath as mp

RESULTS = []


def check(name, cond):
    RESULTS.append((name, bool(cond)))
    print(f"[{'PASS' if cond else 'FAIL'}] {name}")


# ---------------------------------------------------------------------------
# Level-4 modular data
# ---------------------------------------------------------------------------
N = 4
UNITS = [1, 3]


def mm(A, B):
    return ((A[0] * B[0] + A[1] * B[2]) % N, (A[0] * B[1] + A[1] * B[3]) % N,
            (A[2] * B[0] + A[3] * B[2]) % N, (A[2] * B[1] + A[3] * B[3]) % N)


def det(m):
    return (m[0] * m[3] - m[1] * m[2]) % N


def inv(m):  # inverse of an SL2 matrix
    return (m[3], (-m[1]) % N, (-m[2]) % N, m[0])


def proj(m):
    return min(tuple((u * v) % N for v in m) for u in UNITS)


ID = (1, 0, 0, 1)
SL = [m for m in itertools.product(range(N), repeat=4) if det(m) == 1]
PSL = sorted(set(map(proj, SL)))
PGL = sorted(set(proj(m) for m in itertools.product(range(N), repeat=4) if det(m) in UNITS))
PTS = sorted(set(min(((u * p) % N, (u * q) % N) for u in UNITS)
                 for p in range(N) for q in range(N) if math.gcd(math.gcd(p, q), N) == 1))
NAME = {(0, 1): "0", (1, 0): "inf", (1, 1): "1", (1, 3): "-1", (2, 1): "2", (1, 2): "1/2"}


def act(m, pt):
    p, q = pt
    v = ((m[0] * p + m[1] * q) % N, (m[2] * p + m[3] * q) % N)
    return min(((u * v[0]) % N, (u * v[1]) % N) for u in UNITS)


def cusp_perm(m):
    return tuple(PTS.index(act(m, p)) for p in PTS)


def order_sl(m):
    k, c = 1, m
    while c != ID:
        c, k = mm(c, m), k + 1
    return k


# ---------------------------------------------------------------------------
# The octahedron and its rotation group O
# ---------------------------------------------------------------------------
VERTS = [tuple(int(v) for v in r) for r in np.vstack([np.eye(3), -np.eye(3)]).astype(int)]
ROT = [M for M in (np.array(p) for p in itertools.product([-1, 0, 1], repeat=9))
       if True]
ROT = []
for perm in itertools.permutations(range(3)):
    for signs in itertools.product([1, -1], repeat=3):
        M = np.zeros((3, 3), dtype=int)
        for i, j in enumerate(perm):
            M[j, i] = signs[i]
        if round(np.linalg.det(M)) == 1:
            ROT.append(M)
REFL = []  # full O_h
for perm in itertools.permutations(range(3)):
    for signs in itertools.product([1, -1], repeat=3):
        M = np.zeros((3, 3), dtype=int)
        for i, j in enumerate(perm):
            M[j, i] = signs[i]
        REFL.append(M)


def vperm(M):
    return tuple(VERTS.index(tuple(int(c) for c in M @ np.array(v))) for v in VERTS)


print("\n=== F. An explicit isomorphism PSL2(Z/4) -> O, and the t-bit states on it ===")
check("|O| = 24, |O_h| = 48", len(ROT) == 24 and len(REFL) == 48)
target = set(vperm(M) for M in ROT)
target_h = set(vperm(M) for M in REFL)
beta = None
for b in itertools.permutations(range(6)):        # b[i] = vertex index of cusp i
    binv = [0] * 6
    for i, j in enumerate(b):
        binv[j] = i
    conj = lambda cp: tuple(b[cp[binv[j]]] for j in range(6))
    if set(conj(cusp_perm(m)) for m in PSL) == target and set(conj(cusp_perm(m)) for m in PGL) == target_h:
        beta = b
        break
check("A bijection cusps -> octahedron vertices carries PSL2(Z/4) onto O and PGL2(Z/4) onto O_h", beta is not None)
binv = [0] * 6
for i, j in enumerate(beta):
    binv[j] = i
conj = lambda cp: tuple(beta[cp[binv[j]]] for j in range(6))
VP = {vperm(M): M for M in REFL}
RHO = {m: VP[conj(cusp_perm(m))] for m in PGL}   # PGL2(Z/4) -> O_h, a group isomorphism
check("The map is a homomorphism", all(np.array_equal(RHO[proj(mm(a, b_))], RHO[a] @ RHO[b_])
                                       for a in PGL for b_ in PGL))
check("... and PSL2(Z/4) lands exactly on the rotations (det +1)",
      all((round(np.linalg.det(RHO[m])) == 1) == (m in PSL) for m in PGL))
vec = {NAME[p]: np.array(VERTS[beta[i]]) for i, p in enumerate(PTS)}
axis_pairs = [("0", "2"), ("inf", "1/2"), ("1", "-1")]
check("Antipodal cusps: 0 <-> 2, inf <-> 1/2, 1 <-> -1  (the three octahedral axes)",
      all(np.array_equal(vec[a], -vec[b_]) for a, b_ in axis_pairs))
face_A = vec["0"] + vec["inf"] + vec["1"]
face_B = vec["2"] + vec["1/2"] + vec["-1"]
check("The t-bit states {0, 1, inf} (deep field, balanced, Newtonian) are the three corners of ONE face = one tip",
      all(abs(c) == 1 for c in face_A))
check("Its antipodal face is the harmonic cross-ratio triple {-1, 2, 1/2}", np.array_equal(face_B, -face_A))
tet = lambda c: int(np.prod(np.sign(c)))   # 2-colouring of faces: sign product of the tip direction
check("The two triples lie in OPPOSITE tetrahedra of the stellated octahedron", tet(face_A) == -tet(face_B))
Pm = proj((0, 1, 1, 0))
check("The exchange P: x -> 1/x maps the face {0,1,inf} to itself (swaps 0, inf; fixes 1): a mirror of that tip",
      np.array_equal(RHO[Pm] @ face_A, face_A) and round(np.linalg.det(RHO[Pm])) == -1)
stab = [m for m in PGL if np.array_equal(RHO[m] @ face_A, face_A)]
check("Stabiliser of the tip {0,1,inf} in PGL2(Z/4) is the anharmonic group S3 = <x->1/x, x->1-x>",
      len(stab) == 6 and proj((3, 1, 0, 1)) in stab and Pm in stab)
L = proj((1, 0, 1, 1))
T = proj((1, 1, 0, 1))
fixes = lambda m, a: np.array_equal(RHO[m] @ vec[a], vec[a])
check("The constitutive law L is the quarter-turn about the axis through x = 0 (deep field) and x = 2",
      fixes(L, "0") and fixes(L, "2") and order_sl(L) in (4, 2) and
      not np.array_equal(RHO[proj(mm(L, L))], np.eye(3, dtype=int)))
check("The threshold shift T is the quarter-turn about the axis through x = inf (Newtonian) and x = 1/2",
      fixes(T, "inf") and fixes(T, "1/2"))
check("The Field Origin x = 1 lies on the third axis, fixed by the mirror P", fixes(Pm, "1"))

# ---------------------------------------------------------------------------
print("\n=== G. The connection as cochains on the octahedron ===")
LEGS = [np.array(v) for v in [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]]  # TetA tips = tetrad legs


def leg_perm(M):
    out, sg = [], []
    for t in LEGS:
        w = M @ t
        for j, u in enumerate(LEGS):
            if np.array_equal(w, u) or np.array_equal(w, -u):
                out.append(j)
                sg.append(1 if np.array_equal(w, u) else -1)
    return tuple(out), sg


def perm_sign(p):
    s, p = 1, list(p)
    for i in range(len(p)):
        while p[i] != i:
            j = p[i]
            p[i], p[j] = p[j], p[i]
            s = -s
    return s


SIG = [leg_perm(M)[0] for M in ROT]
check("O permutes the 4 body diagonals (legs) faithfully: O = S4", len(set(SIG)) == 24)
check("A rotation is odd on the legs iff it swaps TetA and TetB tips",
      all((perm_sign(leg_perm(M)[0]) == -1) == all(s == -1 for s in leg_perm(M)[1]) and
          (perm_sign(leg_perm(M)[0]) == 1) == all(s == 1 for s in leg_perm(M)[1]) for M in ROT))
# Representations
idx3 = list(itertools.product(range(4), repeat=3))


def rep_connection(M):
    p = leg_perm(M)[0]
    R = np.zeros((64, 64))
    for i, (a, b_, c) in enumerate(idx3):
        R[idx3.index((p[a], p[b_], p[c])), i] = 1
    return R


tors_basis, chr_basis = [], []
for a in range(4):
    for b_, c in itertools.combinations(range(4), 2):
        v = np.zeros(64)
        v[idx3.index((a, b_, c))], v[idx3.index((a, c, b_))] = 1, -1
        tors_basis.append(((a, b_, c), v / np.sqrt(2)))
    for b_, c in itertools.combinations_with_replacement(range(4), 2):
        v = np.zeros(64)
        v[idx3.index((a, b_, c))] += 1
        v[idx3.index((a, c, b_))] += 1
        chr_basis.append(((a, b_, c), v / np.linalg.norm(v)))


def restrict(basis, R):
    B = np.array([v for _, v in basis]).T
    return B.T @ R @ B


inc = [e for e in tors_basis if e[0][0] in e[0][1:]]
non = [e for e in tors_basis if e[0][0] not in e[0][1:]]
EDGES = [(i, j) for i, j in itertools.combinations(range(6), 2) if not np.array_equal(VERTS[i], [-c for c in VERTS[j]])]
FACES = [tuple(sorted(VERTS.index(tuple(s * np.eye(3, dtype=int)[k])) for k, s in enumerate(sg)))
         for sg in itertools.product([1, -1], repeat=3)]


def face_normal(f):
    return sum(np.array(VERTS[i]) for i in f)


def oriented_face(f):  # counter-clockwise seen from outside
    a, b_, c = f
    n = face_normal(f)
    if np.dot(np.cross(np.array(VERTS[b_]) - VERTS[a], np.array(VERTS[c]) - VERTS[a]), n) < 0:
        b_, c = c, b_
    return (a, b_, c)


def rep_vertices(M):
    p = vperm(M)
    R = np.zeros((6, 6))
    for i in range(6):
        R[p[i], i] = 1
    return R


def rep_edges(M, oriented):
    p = vperm(M)
    R = np.zeros((12, 12))
    for k, (i, j) in enumerate(EDGES):
        a, b_ = p[i], p[j]
        if (a, b_) in EDGES:
            R[EDGES.index((a, b_)), k] = 1
        else:
            R[EDGES.index((b_, a)), k] = -1 if oriented else 1
    return R


def rep_faces(M):
    p = vperm(M)
    R = np.zeros((8, 8))
    for k, f in enumerate(FACES):
        R[FACES.index(tuple(sorted(p[i] for i in f))), k] = 1
    return R


def rep_diag(M):
    p = leg_perm(M)[0]
    R = np.zeros((4, 4))
    for i in range(4):
        R[p[i], i] = 1
    return R


def blockdiag(*Ms):
    n = sum(M.shape[0] for M in Ms)
    out, k = np.zeros((n, n)), 0
    for M in Ms:
        d = M.shape[0]
        out[k:k + d, k:k + d] = M
        k += d
    return out


def intertwiner(rep1, rep2, seed=0):
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((rep2(ROT[0]).shape[0], rep1(ROT[0]).shape[0]))
    A = sum(rep2(M) @ X @ np.linalg.inv(rep1(M)) for M in ROT) / 24
    return A


def isomorphic(rep1, rep2):
    A = intertwiner(rep1, rep2)
    ok = A.shape[0] == A.shape[1] and np.linalg.matrix_rank(A, tol=1e-8) == A.shape[0]
    ok = ok and all(np.allclose(rep2(M) @ A, A @ rep1(M)) for M in ROT)
    return ok, A


RE = lambda M: rep_edges(M, False)
C1 = lambda M: rep_edges(M, True)
ok_inc, _ = isomorphic(lambda M: restrict(inc, rep_connection(M)), RE)
check("Incident torsion T^a_[ab] (12)  =  functions on the 12 edges, R[E]  (explicit invertible intertwiner)", ok_inc)
ok_non, A_non = isomorphic(lambda M: restrict(non, rep_connection(M)), C1)
check("Non-incident torsion T^a_[bc] (12)  =  oriented 1-cochains on the octahedron, C^1", ok_non)
ok_chr, _ = isomorphic(lambda M: restrict(chr_basis, rep_connection(M)),
                       lambda M: blockdiag(rep_diag(M), RE(M), RE(M), RE(M)))
check("Christoffel sector (40)  =  R[D] + 3 R[E]  (4 body diagonals + three copies of the edges)", ok_chr)
ok_all, _ = isomorphic(rep_connection,
                       lambda M: blockdiag(rep_diag(M), RE(M), RE(M), RE(M), RE(M), C1(M)))
check("Whole connection (64)  =  R[D] + 4 R[E] + C^1: only C^1 carries orientation", ok_all)

# Hodge decomposition of C^1
d0 = np.zeros((12, 6))
for k, (i, j) in enumerate(EDGES):
    d0[k, j], d0[k, i] = 1, -1
d1 = np.zeros((8, 12))
for r, f in enumerate(FACES):
    a, b_, c = oriented_face(f)
    for u, v in ((a, b_), (b_, c), (c, a)):
        if (u, v) in EDGES:
            d1[r, EDGES.index((u, v))] += 1
        else:
            d1[r, EDGES.index((v, u))] -= 1
check("d1 d0 = 0 (cochain complex of the octahedron)", np.allclose(d1 @ d0, 0))
rk0, rk1 = np.linalg.matrix_rank(d0), np.linalg.matrix_rank(d1)
check(f"C^1 = exact (rank d0 = {rk0}) + co-exact (rank d1 = {rk1}) = 5 + 7 = 12: H^1 = 0, the curve is a sphere",
      rk0 == 5 and rk1 == 7)


def char(rep):
    return Counter()


def multiplicities(rep):
    # characters of S4 irreps on cycle types, via leg permutations
    def ctype(p):
        seen, lens = set(), []
        for i in range(4):
            if i not in seen:
                L_, j = 0, i
                while j not in seen:
                    seen.add(j)
                    j = p[j]
                    L_ += 1
                lens.append(L_)
        return tuple(sorted(lens))
    table = {  # (1,1,1,1) (1,1,2) (2,2) (1,3) (4)
        "1": [1, 1, 1, 1, 1], "sgn": [1, -1, 1, 1, -1], "E": [2, 0, 2, -1, 0],
        "3": [3, 1, -1, 0, -1], "3'": [3, -1, -1, 0, 1]}
    order_ = [(1, 1, 1, 1), (1, 1, 2), (2, 2), (1, 3), (4,)]
    out = {}
    for nm, ch in table.items():
        s = sum(np.trace(rep(M)) * ch[order_.index(ctype(leg_perm(M)[0]))] for M in ROT) / 24
        out[nm] = int(round(s))
    return {k: v for k, v in out.items() if v}


ex = multiplicities(rep_vertices)
fa = multiplicities(rep_faces)
c1 = multiplicities(C1)
check(f"C^0 (6 cusps) = {ex};  C^2 (8 tips) = {fa}", ex == {"1": 1, "E": 1, "3'": 1}
      and fa == {"1": 1, "sgn": 1, "3": 1, "3'": 1})
check(f"C^1 = {c1} = (C^0 - 1) + (C^2 - 1): exact part E + 3', co-exact part sgn + 3 + 3'",
      c1 == {"sgn": 1, "E": 1, "3": 1, "3'": 2})
check("The rotation representation of O on R^3 is 3' (= the vector rep twisted by sign)",
      multiplicities(lambda M: M.astype(float)) == {"3'": 1})
check("Sign representation: once in torsion, never in Christoffel (the torsion-proof result, recovered)",
      multiplicities(lambda M: restrict(tors_basis, rep_connection(M))).get("sgn", 0) == 1 and
      multiplicities(lambda M: restrict(chr_basis, rep_connection(M))).get("sgn", 0) == 0)
chi = np.array([tet(face_normal(f)) for f in FACES], dtype=float)   # +1 on TetA tips, -1 on TetB tips
curl = d1.T @ chi
check("The parity detector is a curl: omega = d1^T chi_(TetA - TetB) is nonzero and spans the sign line of C^1",
      np.linalg.norm(curl) > 0 and all(np.allclose(C1(M) @ curl, perm_sign(leg_perm(M)[0]) * curl) for M in ROT))
check("omega = +-2 on every edge (adjacent tips always opposite): a uniform vortex", np.allclose(np.abs(curl), 2))
check("omega is purely co-exact (orthogonal to every gradient d0 f): not a potential flow",
      np.allclose(d0.T @ curl, 0))
check("Circulation of omega around each TetA tip = +6, around each TetB tip = -6",
      np.allclose(d1 @ curl, 6 * chi))
sgn_vec_tors = A_non @ np.linalg.lstsq(A_non, curl, rcond=None)[0]
check("Pulled back through the explicit intertwiner, omega is the unique sign vector of the non-incident torsion",
      np.allclose(sgn_vec_tors, curl))

# ---------------------------------------------------------------------------
print("\n=== H. The double cover that separates 21 from 13 ===")
cnt = Counter(order_sl(m) for m in SL)
check(f"|SL2(Z/4)| = 48 with element orders {dict(sorted(cnt.items()))}", cnt == {1: 1, 2: 7, 3: 8, 4: 24, 6: 8})
check("Not the binary octahedral group 2O (which has 1 involution and elements of order 8)",
      cnt[2] != 1 and 8 not in cnt)
check("Not GL(2,3) (13 involutions, order 8) and not split S4 x Z2 (19 involutions)",
      cnt[2] not in (13, 19))
# character phi: SL2(Z/4) -> Z/4 with phi(S) = phi(T) = 1
S_, T_ = (0, 3, 1, 0), (1, 1, 0, 1)
phi, frontier = {ID: 0}, [ID]
consistent = True
while frontier:
    g = frontier.pop()
    for h, val in ((S_, 1), (T_, 1)):
        k = mm(g, h)
        if k in phi:
            consistent &= phi[k] == (phi[g] + val) % 4
        else:
            phi[k] = (phi[g] + val) % 4
            frontier.append(k)
check("phi(S) = phi(T) = i extends to a homomorphism phi: SL2(Z/4) -> mu_4 (well defined on all 48)",
      consistent and len(phi) == 48)
check("phi(-1) = -1, so phi does not factor through PSL2", phi[(3, 0, 0, 3)] == 2)


def sl_sign(m):
    return perm_sign(leg_perm(RHO[proj(m)])[0])


check("phi^2 = sign character of S4: SL2(Z/4) = {(g, z) in S4 x mu_4 : z^2 = sgn g}",
      all(((2 * phi[m]) % 4 == 0) == (sl_sign(m) == 1) for m in SL))
check("Hence over A4 the cover splits: the even part is A4 x {+-1}", all(phi[m] in (0, 2) for m in SL if sl_sign(m) == 1))
# eta^6 multiplier, numerically
mp.mp.dps = 50
tau = mp.mpc("0.13", "0.91")
eta = lambda z: mp.exp(mp.pi * 1j * z / 12) * mp.qp(mp.exp(2 * mp.pi * 1j * z))
e6 = lambda z: eta(z) ** 6
check("eta(tau+1)^6 = i eta(tau)^6   (multiplier of T is i)", abs(e6(tau + 1) - 1j * e6(tau)) < 1e-20)
check("eta(-1/tau)^6 = i tau^3 eta(tau)^6   (multiplier of S is i, weight 3)",
      abs(e6(-1 / tau) - 1j * tau ** 3 * e6(tau)) < 1e-20)
check("So phi is the multiplier system of eta^6, and the sign character (phi^2) is that of eta^12",
      abs(eta(tau + 1) ** 12 + eta(tau) ** 12) < 1e-20 and abs(eta(-1 / tau) ** 12 + tau ** 6 * eta(tau) ** 12) < 1e-18)


# Trace table
def ctype_of(m):
    p = leg_perm(RHO[proj(m)])[0]
    seen, lens = set(), []
    for i in range(4):
        if i not in seen:
            L_, j = 0, i
            while j not in seen:
                seen.add(j)
                j = p[j]
                L_ += 1
            lens.append(L_)
    return tuple(sorted(lens))


traces = {}
for m in SL:
    traces.setdefault(ctype_of(m), set()).add((m[0] + m[3]) % 4)
check(f"Traces mod 4 by cycle type: {dict(sorted(traces.items()))}",
      traces == {(1, 1, 1, 1): {2}, (1, 1, 2): {0}, (2, 2): {2}, (1, 3): {1, 3}, (4,): {2}})
check("So s = -tr picks out exactly: transpositions -> s = 0 (17); 3-cycles -> s = +-1 (21 / 13); all else s = 2 (mod 4)",
      traces[(1, 1, 2)] == {0} and traces[(1, 3)] == {1, 3})
three = [m for m in SL if ctype_of(m) == (1, 3)]
check("For each 3-cycle, the lift with phi = 1 (trivial) has order 3 and trace -1 (21); its negative has order 6, trace +1 (13)",
      all((phi[m] == 0) == (order_sl(m) == 3) == ((m[0] + m[3]) % 4 == 3) for m in three))


# Tip labelling: 3-cycle = +120 deg about tip v; L(v) = 21-lift if v in TetA, 13-lift if v in TetB
def axis_ccw(M):
    w, V = np.linalg.eig(M.astype(float))
    ax = np.real(V[:, np.argmin(abs(w - 1))])
    ax = ax / np.max(np.abs(ax))
    perp = np.cross(ax, [1, 0, 0]) if abs(ax[0]) < 0.9 else np.cross(ax, [0, 1, 0])
    if np.dot(np.cross(perp, M @ perp), ax) < 0:
        ax = -ax
    return tuple(int(round(c)) for c in ax)


Lab = {}
for m in three:
    v = axis_ccw(RHO[proj(m)])
    want = 0 if tet(v) == 1 else 2
    if phi[m] == want:
        Lab[v] = m
check("Every one of the 8 tips gets exactly one lifted state: 4 TetA tips -> order-3 (21), 4 TetB tips -> order-6 (13)",
      len(Lab) == 8 and all((order_sl(m) == 3) == (tet(v) == 1) for v, m in Lab.items()))
check("Spatial parity v -> -v acts on the lifted states as M -> -M^-1, i.e. s -> -s",
      all(Lab[tuple(-c for c in v)] == tuple((-c) % 4 for c in inv(m)) for v, m in Lab.items()))
neg = lambda m: tuple((-c) % 4 for c in m)
tw = all(mm(mm(h, Lab[v]), inv(h)) == (Lab[tuple(int(c) for c in RHO[proj(h)] @ np.array(v))] if sl_sign(h) == 1
                                       else neg(Lab[tuple(int(c) for c in RHO[proj(h)] @ np.array(v))]))
         for h in SL for v in Lab)
check("Sign-twisted equivariance: h L(v) h^-1 = sgn(h) L(h v) for all 48 h and 8 tips", tw)

n_pass = sum(1 for _, ok in RESULTS if ok)
print(f"\n{n_pass}/{len(RESULTS)} checks passed")
if __name__ == "__main__":
    raise SystemExit(0 if n_pass == len(RESULTS) else 1)
