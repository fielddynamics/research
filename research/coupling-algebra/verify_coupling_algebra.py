"""Verification for research/coupling-algebra: how TetA and TetB couple, as algebra on the cube.

Conventions (Gram paper, Letter 1, chiral-holonomy proof): corners v in {+-1}^3, TetA = {v1 v2 v3 = +1},
TetB = -TetA (spatial parity, the second root), M1 = TetA's corners as columns, M2 = -M1.
A_d (d = 0..3) = the corners at Hamming distance d. Run: python verify_coupling_algebra.py
"""
import itertools
import math
import numpy as np

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)
def section(t): print(f"\n--- {t}")

TA = [np.array(v) for v in itertools.product([1, -1], repeat=3) if np.prod(v) > 0]
order = TA + [-v for v in TA]                     # TetA first, TetB in antipodal order
n = 8
idx = {tuple(v): i for i, v in enumerate(order)}
dist = np.array([[int((order[i] != order[j]).sum()) for j in range(n)] for i in range(n)])
A = [(dist == d).astype(int) for d in range(4)]
I8, J8, J4, I4 = np.eye(n, dtype=int), np.ones((n, n), int), np.ones((4, 4)), np.eye(4)
chamber = np.array([1] * 4 + [-1] * 4)
same = np.equal.outer(chamber, chamber)
M1 = np.array(TA).T; M2 = -M1; S = np.hstack([M1, M2])
fmt = lambda c: " + ".join((f"{k}" if k != 1 else "") + f"A{d}" for d, k in enumerate(c) if k) or "0"

# ======================================================================= 1
section("1. The four relations on the eight corners")
check("1a. A0 + A1 + A2 + A3 = J: every pair of corners is 0, 1, 2 or 3 steps apart", np.array_equal(sum(A), J8))
check("1b. A1 = the cube's 12 edges, all between the chambers", A[1].sum() == 24 and not (A[1] & same).any())
check("1c. A2 = the two tetrahedra, 6 + 6 edges, all within a chamber", A[2].sum() == 24 and (A[2] <= same).all())
check("1d. A3 = the 4 body diagonals, between the chambers, each through the centre (the Field Origin)",
      A[3].sum() == 8 and not (A[3] & same).any()
      and all(np.allclose(order[i] + order[j], 0) for i in range(n) for j in range(n) if A[3][i, j]))
check("1e. A3 is the antipode v -> -v: spatial parity, which sends each root to the other",
      all(order[int(np.argmax(A[3][i]))].tolist() == (-order[i]).tolist() for i in range(n)))

# ======================================================================= 2
section("2. Symmetry forces the algebra")
mats = []
for perm in itertools.permutations(range(3)):
    for sg in itertools.product([1, -1], repeat=3):
        R = np.zeros((3, 3), int); R[range(3), perm] = sg; mats.append(R)
pm = lambda R: np.array([[1 if idx[tuple(R @ order[j])] == i else 0 for j in range(n)] for i in range(n)])
G_full = [pm(R) for R in mats]
G_rot = [pm(R) for R in mats if round(np.linalg.det(R)) == 1]
G_Td = [pm(R) for R in mats if all(idx[tuple(R @ v)] < 4 for v in TA)]
def commutant_dim(G, odd_only=False):
    rows = [np.kron(P.T, np.eye(n)) - np.kron(np.eye(n), P) for P in G]
    if odd_only:
        for i in range(n):
            for j in range(n):
                if same[i, j]:
                    r = np.zeros(n * n); r[j * n + i] = 1; rows.append(r[None, :])
    return n * n - np.linalg.matrix_rank(np.vstack(rows))
check("2a. the cube has 48 symmetries (signed permutations, O_h); each A_d commutes with all of them",
      len(G_full) == 48 and all(np.array_equal(P @ a, a @ P) for P in G_full for a in A))
check("2b. the couplings that commute with all 48 form a space of dimension exactly 4, spanned by A0..A3",
      commutant_dim(G_full) == 4)
check("2c. the 24 proper rotations alone force the same 4 (some rotations already exchange the chambers)",
      commutant_dim(G_rot) == 4)
check("2d. so TetA and TetB can couple through exactly two channels: the vector links A1 and the Field Origin A3",
      commutant_dim(G_full, odd_only=True) == 2 and commutant_dim(G_rot, odd_only=True) == 2)
check("2e. keeping the chambers distinct (the 24 that fix TetA, S4) allows 8: A->A, B->B, A->B, B->A for each relation",
      commutant_dim(G_Td) == 8)

# ======================================================================= 3
section("3. The multiplication table and the chamber grading")
basis = np.array([a.ravel() for a in A]).T.astype(float)
prod = {}
for i in range(4):
    for j in range(4):
        c = np.round(np.linalg.lstsq(basis, (A[i] @ A[j]).ravel().astype(float), rcond=None)[0]).astype(int)
        prod[(i, j)] = c
check("3a. every product A_i A_j is an integer combination of A0..A3, and the products commute",
      all(np.array_equal(sum(k * a for k, a in zip(prod[(i, j)], A)), A[i] @ A[j]) and np.array_equal(A[i] @ A[j], A[j] @ A[i])
          for i in range(4) for j in range(4)))
for i, j in [(1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3)]:
    print(f"     A{i} A{j} = {fmt(prod[(i, j)])}")
check("3b. A1 A3 = A2: a vector link followed by the Field Origin is a within-chamber link", list(prod[(1, 3)]) == [0, 0, 1, 0])
check("3c. A2 A3 = A1 and A3 A3 = A0: the Field Origin link is an involution exchanging A1 and A2",
      list(prod[(2, 3)]) == [0, 1, 0, 0] and list(prod[(3, 3)]) == [1, 0, 0, 0])
check("3d. graded by chamber: within = {A0, A2} (even), between = {A1, A3} (odd); even.even, odd.odd -> even; even.odd -> odd",
      all((prod[(i, j)][[1, 3]] == 0).all() if i % 2 == j % 2 else (prod[(i, j)][[0, 2]] == 0).all() for i in range(4) for j in range(4)))

# ======================================================================= 4
section("4. The Walsh grades diagonalise everything")
W, grades = [], []
for k in range(4):
    for Sx in itertools.combinations(range(3), k):
        W.append(np.array([np.prod(v[list(Sx)]) for v in order])); grades.append(k)
W = np.array(W, float)
P = np.zeros((4, 4), int)
for d in range(4):
    for w, g in zip(W, grades):
        P[g, d] = round((w @ A[d] @ w) / (w @ w))
print("     eigenvalue matrix P[grade, distance]:\n", P)
check("4a. every Walsh function is an eigenvector of every A_d; the common eigenspaces are the grades, sizes 1, 3, 3, 1",
      all(np.allclose(A[d] @ w, P[g, d] * w) for d in range(4) for w, g in zip(W, grades))
      and len({tuple(r) for r in P}) == 4 and sorted(np.bincount(grades)) == [1, 1, 3, 3])
check("4b. P is the Krawtchouk matrix: P[w, d] = sum_j (-1)^j C(w, j) C(3 - w, d - j)",
      all(P[w, d] == sum((-1) ** j * int(math.comb(w, j)) * int(math.comb(3 - w, d - j)) for j in range(0, d + 1) if d - j <= 3 - w)
          for w in range(4) for d in range(4)))
check("4c. P @ P = 8 I: the scheme is self-dual", np.array_equal(P @ P, 8 * np.eye(4, dtype=int)))
check("4d. the chamber sign (+1 on TetA, -1 on TetB) is the grade-3 Walsh function xyz; on A_d it reads +1, -3, +3, -1",
      np.allclose(W[7], chamber) and list(P[3]) == [1, -3, 3, -1])

# ======================================================================= 5
section("5. The objects GFD already uses, as elements of the algebra")
Gram = S.T @ S
L_K4 = 3 * I4 - (J4 - I4); L_K2 = np.array([[1, -1], [-1, 1]])
items = [
    ("Gram matrix of the stellated octahedron, S^T S (Gram paper)", Gram, [3, 1, -1, -3]),
    ("cube graph Q3 (universe-is-pixelated, chiral holonomy)", A[1], [0, 1, 0, 0]),
    ("Paper IX 'coupling graph' = complement of Q3 = triforce face graph", J8 - I8 - A[1], [0, 0, 1, 1]),
    ("between-chamber coupling graph K_{4,4}", A[1] + A[3], [0, 1, 0, 1]),
    ("the two chambers (block of ones on each)", np.kron(np.eye(2, dtype=int), np.ones((4, 4), int)), [1, 0, 1, 0]),
]
for name, M, c in items:
    c = np.array(c)
    check(f"5. {name} = {fmt(c)}; eigenvalues on grades 0..3: {[int(e) for e in P @ c]}",
          np.array_equal(M, sum(k * a for k, a in zip(c, A))))
check("5a. the Gram matrix is 8 x the projector onto grade 1: it sees only the three vector Walsh modes x, y, z",
      list(P @ np.array([3, 1, -1, -3])) == [0, 8, 0, 0] and np.allclose(S, W[1:4]))
check("5b. Gram entry for a pair at distance d is 3 - 2d, which is also the cube's eigenvalue on grade d (self-duality)",
      all(Gram[i, j] == 3 - 2 * dist[i, j] for i in range(n) for j in range(n)) and all(P[d, 1] == 3 - 2 * d for d in range(4)))
check("5c. Paper IX / triforce spectrum {+4, -2 (x3), 0 (x3), +2} on grades 0, 1, 2, 3", list(P @ np.array([0, 0, 1, 1])) == [4, -2, 0, 2])
check("5d. TetA's self-Gram M1^T M1 = 4I - J is the graph Laplacian of K4: Gram Lemma 5's {0, 4, 4, 4} is its spectrum",
      np.allclose(M1.T @ M1, L_K4) and np.allclose(sorted(np.linalg.eigvalsh(L_K4)), [0, 4, 4, 4]))
check("5e. the cross-Gram M1^T M2 = -L(K4) (Gram Lemma 2), and S^T S = L(K2) (x) L(K4)",
      np.allclose(M1.T @ M2, -L_K4) and np.allclose(Gram, np.kron(L_K2, L_K4)))
check("5f. the {1, D, D, 1} oscillator theorem (quantum compute): any symmetric operator here has at most 4 eigenvalues, "
      "with multiplicities 1, 3, 3, 1", sorted(np.bincount(grades)) == [1, 1, 3, 3] and commutant_dim(G_full) == 4)

# ======================================================================= 6
section("6. The Clifford reading, and the base point")
def blade(v, base): return frozenset(i for i in range(3) if v[i] != base[i])
def cl_mul(Sa, Tb):                              # e_S e_T = +- e_(S xor T) in Cl(3,0)
    s = sorted(Sa); sign = 1
    for t in sorted(Tb):
        sign *= (-1) ** sum(1 for x in s if x > t)
        if t in s: s.remove(t)
        else: s.append(t); s.sort()
    return sign, frozenset(s)
plus, minus = np.array([1, 1, 1]), np.array([-1, -1, -1])
check("6a. with (+,+,+) as the scalar 1: TetA = even blades {1, e12, e13, e23}, TetB = odd blades {e1, e2, e3, e123} "
      "(the bimetric-projection probe's convention)",
      all(len(blade(v, plus)) % 2 == 0 for v in TA) and all(len(blade(-v, plus)) % 2 == 1 for v in TA))
check("6b. with (-,-,-) as the scalar 1: TetA = odd blades (the algebraic pipeline's convention)",
      all(len(blade(v, minus)) % 2 == 1 for v in TA))
check("6c. the link from corner v to corner w is multiplication by e_(S xor T); its grade is the distance d for either base point",
      all(cl_mul(blade(order[i], b), blade(order[i], b) ^ blade(order[j], b))[1] == blade(order[j], b)
          and len(blade(order[i], b) ^ blade(order[j], b)) == dist[i, j] for b in (plus, minus) for i in range(n) for j in range(n)))
check("6d. so A1 = grade-1 (vector) links, A2 = grade-2 (bivector) links, A3 = grade-3 (pseudoscalar) links: base-point free",
      all(np.array_equal(A[d], np.array([[int(len(blade(order[i], b) ^ blade(order[j], b)) == d) for j in range(n)] for i in range(n)]))
          for d in range(4) for b in (plus, minus)))
check("6e. parity v -> -v is multiplication by the pseudoscalar: S -> complement, grade k -> 3 - k (the Hodge dual)",
      all(blade(-v, plus) == frozenset({0, 1, 2}) - blade(v, plus) for v in order))

# ======================================================================= 7
section("7. The second root and the sign of the legs")
def perm_sign(p): return int(round(np.linalg.det(np.eye(len(p))[list(p)])))
acts = lambda R: tuple(idx[tuple(R @ v)] for v in order)
rots = [R for R in mats if round(np.linalg.det(R)) == 1]
swap = [R for R in rots if set(acts(R)[:4]) == {4, 5, 6, 7}]
check("7a. of the 24 proper rotations, exactly 12 exchange TetA and TetB (for example a quarter turn about an axis)", len(swap) == 12)
res = []
for R in swap:
    sigma = [next(k2 for k2 in range(4) if (-M1[:, k2] == R @ M1[:, k]).all()) for k in range(4)]
    res.append((np.array_equal(R @ M1, M2[:, sigma]), perm_sign(sigma)))
check("7b. for each of them, R M1 = M2 relabelled by a permutation sigma of the legs", all(r[0] for r in res))
check("7c. every such sigma is odd: up to a proper rotation, the second root is an odd relabelling of the four legs",
      all(r[1] == -1 for r in res))
Om = lambda M: round(np.linalg.det(np.vstack([np.ones(M.shape[1]), M])))
check("7d. the oriented volume Omega(M) = det[1; M] = +-16 (the bordered Hadamard matrix) is unchanged by rotations "
      "and multiplied by sgn(sigma) under a relabelling of the legs",
      abs(Om(M1)) == 16 and all(Om(R @ M1) == Om(M1) for R in rots)
      and all(Om(M1[:, list(p)]) == perm_sign(p) * Om(M1) for p in itertools.permutations(range(4))))
check("7e. Omega(M2) = -Omega(M1): among rotation-invariant quantities, the sign representation of S4 detects the root",
      Om(M2) == -Om(M1))

# ======================================================================= 8
section("8. The constitutive law inside the algebra")
def Q(x):                                         # A -> B at rate 1, B -> A at rate x, on the between-chamber links
    M = (A[1] + A[3]).astype(float); M[4:, :] *= x
    return M - np.diag(M.sum(1))
for x in [0.1, 1.0, 7.0]:
    w, V = np.linalg.eig(Q(x).T); pi = np.real(V[:, np.argmin(abs(w))]); pi /= pi.sum()
    check(f"8a. x = {x}: the walk settles with TetA share {pi[:4].sum():.6f} = x/(1+x) = mu(x), uniform within each chamber",
          np.isclose(pi[:4].sum(), x / (1 + x)) and np.allclose(pi[:4], pi[0]) and np.allclose(pi[4:], pi[4]))
Qx = Q(3.0)
check("8b. it lumps exactly onto the two-state chain TetA <-> TetB (every corner has the same total rate to the other chamber)",
      len({round(Qx[i, 4:].sum(), 12) for i in range(4)}) == 1 and len({round(Qx[i, :4].sum(), 12) for i in range(4, 8)}) == 1)
check("8c. the directed walk respects S4 but not the full symmetry unless x = 1: rate asymmetry is what breaks the exchange",
      all(np.allclose(P_ @ Qx, Qx @ P_) for P_ in G_Td) and not all(np.allclose(P_ @ Qx, Qx @ P_) for P_ in G_full)
      and all(np.allclose(P_ @ Q(1.0), Q(1.0) @ P_) for P_ in G_full))
check("8d. exchanging the chambers through the Field Origin, A3 Q(x) A3 = x Q(1/x): the exchange symmetry mu(1/x) = 1 - mu(x)",
      np.allclose(A[3] @ Qx @ A[3], 3.0 * Q(1 / 3.0)))

# ======================================================================= 9
section("9. Counts the repo already uses")
pairs_by_d = [int(A[d].sum()) for d in range(4)]
check("9a. the 64 ordered pairs of corners split 8 + 24 + 24 + 8 by distance (the triforce traversal's 'Hamming spectrum')",
      pairs_by_d == [8, 24, 24, 8] and sum(pairs_by_d) == 64)
check("9b. 24 ordered vector links (between), 24 ordered bivector links (within), 16 self or antipodal pairs: 24 + 16 + 24",
      pairs_by_d[1] == 24 and pairs_by_d[2] == 24 and pairs_by_d[0] + pairs_by_d[3] == 16)
# triforce: TetA face opposite corner v, sub-channel at corner w (w != v: outer), or the central one (w = v)
bij = {}
for vi in range(4):
    for wi in range(4):
        a, b = idx[tuple(TA[wi])], idx[tuple(-TA[vi])]          # (face v, slot w) -> link from TetA corner w to TetB corner -v
        bij[(vi, wi)] = (a, b, dist[a, b])
check("9c. triforce sub-channels (face v of TetA, slot w) <-> between-chamber links (w, -v) is one-to-one onto all 16",
      len({(a, b) for a, b, _ in bij.values()}) == 16)
check("9d. under it the 12 outer sub-channels are the 12 vector links and the 4 central ones are the 4 Field Origin links",
      all((d == 3) == (vi == wi) and d in (1, 3) for (vi, wi), (_, _, d) in bij.items()))
cent = [(TA[(vi + 1) % 4] + TA[(vi + 2) % 4] + TA[(vi + 3) % 4]) / 3 for vi in range(4)]
check("9e. the centre of face v of TetA is -v/3, on the diagonal through the Field Origin to TetB's corner -v",
      all(np.allclose(cent[vi], -TA[vi] / 3) for vi in range(4)))

print(f"\n{sum(ok)}/{len(ok)} checks passed")
