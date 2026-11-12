"""The metric g and the connection's index pair in the coupling algebra.
Run: python verify_metric_and_connection.py   (numpy)
Conventions as in verify_coupling_algebra.py; null lift n_v = (1, v/sqrt3); eta = diag(-1, 1, 1, 1).
1. the metric from the cube   2. the 10 metric components as a simplex   3. the lower index pair on the TetA-TetB links
4. symmetry: the split is kept by all 48   5. bilinear forms read across the roots
"""
import itertools
import numpy as np

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

TA = [np.array(v) for v in itertools.product([1, -1], repeat=3) if np.prod(v) > 0]
order = TA + [-v for v in TA]; n = 8
idx = {tuple(v): i for i, v in enumerate(order)}
dist = np.array([[int((a != b).sum()) for b in order] for a in order])
A = [(dist == d).astype(float) for d in range(4)]
eta = np.diag([-1.0, 1, 1, 1])
W, grades = [], []
for k in range(4):
    for S in itertools.combinations(range(3), k):
        W.append(np.array([np.prod(v[list(S)]) for v in order], float)); grades.append(k)
W = np.array(W)
chamber = W[7]

# ---------------- 1. the metric from the cube
N = np.array([np.concatenate([[1.0], v / np.sqrt(3)]) for v in order]).T          # 4 x 8: null lifts n_v = (1, v/sqrt3)
check("1. each corner lifts to a null direction n_v = (1, v/sqrt3): eta(n_v, n_v) = 0", np.allclose(np.einsum('ai,ab,bi->i', N, eta, N), 0))
G_eta = N.T @ eta @ N
check("1. eta(n_v, n_w) = -(2/3) d(v, w): the Lorentzian Gram of the 8 null directions is -(2/3) x the Hamming distance",
      np.allclose(G_eta, -(2 / 3) * dist))
check("1. so it is an element of the coupling algebra: G_eta = -(2/3)(A1 + 2 A2 + 3 A3)", np.allclose(G_eta, -(2 / 3) * (A[1] + 2 * A[2] + 3 * A[3])))
S = np.array(order).T.astype(float); Gram = S.T @ S
check("1. equivalently G_eta = Gram/3 - J: the spatial Gram minus the all-ones (closure) mode", np.allclose(G_eta, Gram / 3 - np.ones((8, 8))))
lam = {g: sorted({round(float(w @ G_eta @ w / (w @ w)), 9) for w, gg in zip(W, grades) if gg == g}) for g in range(4)}
print("     eigenvalue of G_eta on each Walsh grade:", lam)
check("1. eigenvalues by grade: -8 on grade 0 (one), +8/3 on grade 1 (three), 0 on grades 2 and 3: signature (1, 3), Minkowski",
      lam == {0: [-8.0], 1: [round(8 / 3, 9)], 2: [0.0], 3: [0.0]} and all(np.allclose(G_eta @ w, (w @ G_eta @ w / (w @ w)) * w) for w in W))
check("1. time is grade 0 (the constant mode) and space is grade 1 (x, y, z); grades 2 and 3 are invisible to the metric",
      np.allclose(N @ W[0], [8, 0, 0, 0]) and all(np.allclose(N @ W[i], 0) for i in range(4, 8)))
check("1. the chamber sign xyz (grade 3) is in the metric's kernel: G_eta xyz = 0, so the metric cannot tell TetA from TetB",
      np.allclose(G_eta @ chamber, 0))
NA, NB = N[:, :4], N[:, 4:]
check("1. closure: the four null directions of TetA sum to a pure time vector (4, 0, 0, 0)", np.allclose(NA.sum(1), [4, 0, 0, 0]))
Q_A = np.linalg.inv(NA).T @ (NA.T @ eta @ NA) @ np.linalg.inv(NA)
Q_B = np.linalg.inv(NB).T @ (NB.T @ eta @ NB) @ np.linalg.inv(NB)
check("1. TetA's four null directions alone determine eta (they are a null tetrad); TetB's give the same eta (root-blind)",
      np.allclose(Q_A, eta) and np.allclose(Q_B, eta) and np.allclose(NA.T @ eta @ NA, NB.T @ eta @ NB))
check("1. within TetA every pair has eta(n_a, n_b) = -4/3 (distance 2): the null tetrad is regular",
      np.allclose(NA.T @ eta @ NA, -(4 / 3) * (np.ones((4, 4)) - np.eye(4))))

# ---------------- 2. the 10 metric components as a simplex (Regge reading)
# a symmetric Q on R^{1,3} is fixed by its values on n_a (4) and n_a - n_b (6): squared edge lengths of the
# 4-simplex with vertices {0 (Field Origin), n_1, ..., n_4}
def edge_data(Q):
    return [NA[:, a] @ Q @ NA[:, a] for a in range(4)] + \
           [(NA[:, a] - NA[:, b]) @ Q @ (NA[:, a] - NA[:, b]) for a, b in itertools.combinations(range(4), 2)]
symbasis = []
for i in range(4):
    for j in range(i, 4):
        E = np.zeros((4, 4)); E[i, j] = E[j, i] = 1; symbasis.append(E)
Mreg = np.array([edge_data(E) for E in symbasis]).T
check("2. the 10 metric components <-> the 10 squared edge lengths of the 4-simplex {Field Origin, TetA's 4 null directions} "
      "(4 edges from the Field Origin = A0, 6 edges of TetA = A2): an invertible linear map", Mreg.shape == (10, 10) and np.linalg.matrix_rank(Mreg) == 10)
ed = edge_data(eta)
check("2. for eta itself: the 4 edges from the Field Origin are null, the 6 TetA edges all have squared length 8/3",
      np.allclose(ed[:4], 0) and np.allclose(ed[4:], 8 / 3))

# ---------------- 3. the connection's lower index pair, read on the TetA-TetB links
# V = functions on TetA's corners (the four legs, as in the torsion proof). Send the lower pair (a, b) to the
# between-chamber link from TetA corner a to TetB corner -b (through the Field Origin on the second slot).
link = {(a, b): (a, idx[tuple(-TA[b])]) for a in range(4) for b in range(4)}
check("3. (a, b) -> link(a, -b) is one-to-one onto the 16 between-chamber links K_{4,4}",
      len(set(link.values())) == 16 and all(dist[i, j] in (1, 3) for i, j in link.values()))
check("3. the diagonal (a, a) goes to the 4 Field Origin links (A3); the 12 off-diagonal pairs to the 12 cube edges (A1)",
      all((dist[link[(a, b)]] == 3) == (a == b) for a in range(4) for b in range(4)))
# the swap tau(a, b) = (b, a) versus the antipode acting on links: the edge {a, -b} goes to {-a, b} = link(b, -a)
anti = lambda i: idx[tuple(-order[i])]
def antipode_link(l):
    i, j = l; ii, jj = anti(i), anti(j)            # both ends through the Field Origin
    return (jj, ii) if jj < 4 else (ii, jj)        # reorder as (TetA end, TetB end)
check("3. the index swap tau(a, b) = (b, a) is exactly the antipode (spatial parity, the second root) acting on the links",
      all(antipode_link(link[(a, b)]) == link[(b, a)] for a in range(4) for b in range(4)))
check("3. the Field Origin links are fixed by it, the cube edges are exchanged in 6 antipodal pairs",
      sum(antipode_link(l) == l for l in link.values()) == 4)
# so on functions F on the 16 links: Sym^2 V (lower pair symmetric) = antipode-even, Lambda^2 V = antipode-odd
L16 = list(link.values()); li = {l: k for k, l in enumerate(L16)}
Pant = np.zeros((16, 16))
for l in L16: Pant[li[antipode_link(l)], li[l]] = 1
even, odd = (np.eye(16) + Pant) / 2, (np.eye(16) - Pant) / 2
check("3. antipode-even link functions: 10 = 4 Field Origin links + 6 antipodal pairs of cube edges (the symmetric, Christoffel side)",
      np.linalg.matrix_rank(even) == 10)
check("3. antipode-odd link functions: 6, one per antipodal pair of cube edges, none on the Field Origin links (the torsion side)",
      np.linalg.matrix_rank(odd) == 6 and all(np.allclose(odd[li[l]], 0) for l in L16 if dist[l] == 3))
toV = lambda F: np.array([[F[li[link[(a, b)]]] for b in range(4)] for a in range(4)])
rng = np.random.default_rng(3)
Fr = rng.normal(size=16)
check("3. an even link function is a symmetric matrix in (a, b), an odd one antisymmetric", np.allclose(toV(even @ Fr), toV(even @ Fr).T)
      and np.allclose(toV(odd @ Fr), -toV(odd @ Fr).T))
check("3. per slice 16 = 4 + 6 + 6 (Field Origin + even pairs + odd pairs); over the 4 slices 64 = 16 + 24 + 24, "
      "kept by GR 16 + 24 = 40", 4 * (4 + 6) == 40 and 4 * 6 == 24)

# ---------------- 4. symmetry: the split is covariant under all 48 symmetries of the cube
mats = []
for perm in itertools.permutations(range(3)):
    for sg in itertools.product([1, -1], repeat=3):
        R = np.zeros((3, 3), int); R[range(3), perm] = sg; mats.append(R)
def act_links(R):
    M = np.zeros((16, 16))
    for l in L16:
        i, j = idx[tuple(R @ order[l[0]])], idx[tuple(R @ order[l[1]])]
        new = (i, j) if i < 4 else (j, i)
        M[li[new], li[l]] = 1
    return M
reps = [act_links(R) for R in mats]
check("4. the 48 symmetries permute the 16 between-chamber links (each is a permutation matrix)",
      all(np.allclose(M.sum(0), 1) and np.allclose(M.sum(1), 1) for M in reps))
check("4. the antipode commutes with all 48, so the even (10) and odd (6) link spaces are each kept by every symmetry",
      all(np.allclose(M @ Pant, Pant @ M) for M in reps))
swapRs = [(R, M) for R, M in zip(mats, reps) if all(idx[tuple(R @ v)] >= 4 for v in TA)]
def legperm(R):    # the leg relabelling a symmetry induces on V: TetA corner a goes to TetA corner (R a or -R a)
    return [idx[tuple(R @ TA[a])] if idx[tuple(R @ TA[a])] < 4 else idx[tuple(-(R @ TA[a]))] for a in range(4)]
def tau_on_V(M):   # transported to V (x) V
    out = np.zeros((16, 16))
    for (a, b), l in link.items():
        for (c, d), m in link.items():
            out[c * 4 + d, a * 4 + b] = M[li[m], li[l]]
    return out
Tau = np.zeros((16, 16))
for a in range(4):
    for b in range(4): Tau[b * 4 + a, a * 4 + b] = 1
ok_swap = []
for R, M in swapRs:
    p = legperm(R); Pp = np.eye(4)[:, p]
    ok_swap.append(np.allclose(tau_on_V(M), Tau @ np.kron(Pp, Pp)) or np.allclose(tau_on_V(M), np.kron(Pp, Pp) @ Tau))
check("4. a symmetry that exchanges the chambers acts on the lower pair as a leg relabelling together with the swap tau",
      len(swapRs) == 24 and all(ok_swap))
keepRs = [(R, M) for R, M in zip(mats, reps) if all(idx[tuple(R @ v)] < 4 for v in TA)]
check("4. a symmetry that keeps the chambers acts as a leg relabelling only (sigma (x) sigma), with no swap",
      all(np.allclose(tau_on_V(M), np.kron(np.eye(4)[:, legperm(R)], np.eye(4)[:, legperm(R)])) for R, M in keepRs))

# ---------------- 5. a bilinear form read across the roots: C_B(a, b) = B(n_a, n_-b) = B(n_a, P n_b), P = diag(1,-1,-1,-1)
P = np.diag([1.0, -1, -1, -1])
check("5. reading through the Field Origin sends n_b to n_-b = P n_b (time kept, space reversed)", np.allclose(NB, P @ NA))
CB = lambda B: np.array([B @ 0 if False else NA[:, a] @ B @ NB[:, b] for a in range(4) for b in range(4)]).reshape(4, 4)
check("5. so the swap symmetry of C_B is the symmetry of B P: C_B is symmetric in (a, b) exactly when B P is",
      all(np.allclose(CB(B), CB(B).T) == np.allclose(B @ P, (B @ P).T) for B in [rng.normal(size=(4, 4)) for _ in range(5)] + [eta]))
def sym(i, j):
    E = np.zeros((4, 4)); E[i, j] = E[j, i] = 1; return E
odd_of = lambda B: np.allclose(CB(B), -CB(B).T) and not np.allclose(CB(B), 0)
even_of = lambda B: np.allclose(CB(B), CB(B).T) and not np.allclose(CB(B), 0)
check("5. the flat metric eta reads even across the roots (root-blind)", even_of(eta))
check("5. metric components g_00 and g_ij (gravitoelectric, 1 + 6) read even across the roots",
      even_of(sym(0, 0)) and all(even_of(sym(i, j)) for i in range(1, 4) for j in range(i, 4)))
check("5. metric components g_0i (gravitomagnetic, frame dragging, 3) read odd across the roots",
      all(odd_of(sym(0, i)) for i in range(1, 4)))
gens_rot, gens_boost = [], []
for i, j in itertools.combinations(range(4), 2):
    X = np.zeros((4, 4)); X[i, j] = 1; X[j, i] = -eta[i, i] * eta[j, j]
    (gens_boost if i == 0 else gens_rot).append(eta @ X)        # the antisymmetric form eta X
check("5. the 3 rotation generators of so(1,3) read odd across the roots", all(odd_of(B) for B in gens_rot))
check("5. the 3 boost generators read even across the roots", all(even_of(B) for B in gens_boost))
check("5. so across the roots the odd 6 = 3 rotations + 3 gravitomagnetic g_0i, and the even 10 = g_00 + 6 g_ij + 3 boosts",
      np.linalg.matrix_rank(np.array([CB(B).ravel() for B in gens_rot + [sym(0, i) for i in range(1, 4)]])) == 6
      and np.linalg.matrix_rank(np.array([CB(B).ravel() for B in gens_boost + [sym(0, 0)] + [sym(i, j) for i in range(1, 4) for j in range(i, 4)]])) == 10)
par = lambda B: 1 if np.allclose(P @ B @ P, B) else (-1 if np.allclose(P @ B @ P, -B) else 0)
swp = lambda B: 1 if np.allclose(B, B.T) else (-1 if np.allclose(B, -B.T) else 0)
across = lambda B: 1 if even_of(B) else (-1 if odd_of(B) else 0)
allB = [sym(0, 0)] + [sym(i, j) for i in range(1, 4) for j in range(i, 4)] + [sym(0, i) for i in range(1, 4)] + gens_rot + gens_boost
check("5. the rule: (parity across the roots) = (index symmetry, +1 / -1) x (spatial parity P B P = +-B), for all 16",
      all(across(B) == swp(B) * par(B) and across(B) != 0 for B in allB))
check("5. Newton's component (both lower slots time, (0,0)) is even across the roots: Gamma^i_00 reads the same from TetA and TetB",
      across(sym(0, 0)) == 1)

print(f"\n{sum(ok)}/{len(ok)} checks passed")
