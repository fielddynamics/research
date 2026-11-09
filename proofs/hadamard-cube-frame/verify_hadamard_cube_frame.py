"""Machine checks for every step of
'The Stellated Octahedron, the Cube and the Hadamard Matrix'.
Exhaustive where the space is finite and small; integer arithmetic throughout.
Run: python verify_hadamard_cube_frame.py"""
import itertools, math
import numpy as np

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

def is_cube_simplex(M):
    K = M.shape[1]
    cols = [tuple(M[:, j]) for j in range(K)]
    if len(set(cols)) < K: return False
    d = {int(np.sum((M[:, i] - M[:, j])**2)) for i in range(K) for j in range(i + 1, K)}
    return len(d) == 1
def conditions(M):
    D, K = M.shape
    a = is_cube_simplex(M)
    b = (M.T @ M == K * np.eye(K, dtype=int) - np.ones((K, K), dtype=int)).all()
    H = np.vstack([np.ones(K, dtype=int), M])
    c = (H.T @ H == K * np.eye(K, dtype=int)).all()
    d = (M.sum(axis=1) == 0).all() and (M @ M.T == K * np.eye(D, dtype=int)).all()
    return a, b, c, d

# ---- Theorem 1, exhaustive for D = 1, 2, 3
for D in (1, 2, 3):
    K = D + 1; agree = True; n_simp = 0
    for bits in itertools.product([-1, 1], repeat=D * K):
        M = np.array(bits, dtype=int).reshape(D, K)
        a, b, c, d = conditions(M)
        agree &= (a == b == c == d); n_simp += a
    check(f"Theorem 1: (a)<=>(b)<=>(c)<=>(d) on all {2**(D*K)} sign matrices with D = {D} ({n_simp} cube simplices)", agree)
# D = 7: Sylvester and random sign matrices
H2 = np.array([[1, 1], [1, -1]])
H8 = np.kron(np.kron(H2, H2), H2)
check("Theorem 1: D = 7, the normalised Sylvester H8 gives a cube simplex and all four conditions hold",
      all(conditions(H8[1:])))
rng = np.random.default_rng(0)
agree = True
for _ in range(20000):
    M = rng.choice([-1, 1], size=(7, 8)); r = conditions(M); agree &= len(set(r)) == 1
    Mp = H8[1:][:, rng.permutation(8)] * rng.choice([-1, 1], size=(7, 1)); r = conditions(Mp); agree &= all(r)
check("Theorem 1: D = 7, conditions agree on 20000 random sign matrices and hold on 20000 row-signed, column-permuted Sylvester frames", agree)
import sympy as sp
al, be = sp.symbols('alpha beta', real=True); Dk = sp.Symbol('D', positive=True)
check("Theorem 1 proof: alpha + beta = D and alpha + (D+1) beta = 0 give beta = -1, alpha = D + 1",
      sp.solve([al + be - Dk, al + (Dk + 1) * be], [al, be], dict=True) == [{al: Dk + 1, be: -1}])
# normalisation: negating columns of any Hadamard matrix to first row ones gives a cube simplex
Hrand = H8[rng.permutation(8)][:, rng.permutation(8)] * rng.choice([-1, 1], size=(1, 8)) * rng.choice([-1, 1], size=(8, 1))
Hn = Hrand * Hrand[0]
check("Remark: negating columns normalises a Hadamard matrix; its remaining rows give a cube simplex",
      (Hn.T @ Hn == 8 * np.eye(8)).all() and (Hn[0] == 1).all() and is_cube_simplex(Hn[1:]))

# ---- Lemma (Hadamard) and Corollary 1
def has_hadamard(n):
    for bits in itertools.product([-1, 1], repeat=(n - 1) * (n - 1)):
        H = np.ones((n, n), dtype=int); H[1:, 1:] = np.array(bits).reshape(n - 1, n - 1)
        if (H @ H.T == n * np.eye(n, dtype=int)).all(): return True
    return False
check("Lemma: no Hadamard matrix of order 3 or 5 (exhaustive over normalised matrices)",
      not has_hadamard(3) and not has_hadamard(5))
check("Lemma: Hadamard matrices exist at orders 2 and 4", has_hadamard(2) and has_hadamard(4))
# the counting identity: three linear equations force n++ = n+- = n-+ = n--
import sympy as sp
a1, a2, a3, a4 = sp.symbols('npp npm nmp nmm')
sol = sp.solve([a1 + a2 - a3 - a4, a1 + a3 - a2 - a4, a1 + a4 - a2 - a3], [a2, a3, a4], dict=True)[0]
check("Lemma: the three orthogonality equations force all four counts equal", sol == {a2: a1, a3: a1, a4: a1})
check("Corollary 1: no cube simplex for D = 2 (exhaustive) and one for D = 3",
      not any(is_cube_simplex(np.array(b).reshape(2, 3)) for b in itertools.product([-1, 1], repeat=6)) and
      is_cube_simplex(np.array([[1, 1, -1, -1], [1, -1, 1, -1], [1, -1, -1, 1]])))

# ---- Theorem 2
M = np.array([[1, 1, -1, -1], [1, -1, 1, -1], [1, -1, -1, 1]])
V = {tuple(M[:, j]) for j in range(4)}; nV = {tuple(-M[:, j]) for j in range(4)}
Q3 = set(itertools.product([-1, 1], repeat=3))
check("Theorem 2: V and -V are disjoint and V u -V = Q3", V.isdisjoint(nV) and V | nV == Q3)
check("Theorem 2: 2(D+1) = 2^D only at D = 3 (D = 1..200)", [D for D in range(1, 201) if 2 * (D + 1) == 2**D] == [3])
check("Theorem 2: 2^D > 2(D+1) for 4 <= D <= 200", all(2**D > 2 * (D + 1) for D in range(4, 201)))
sets = set()
for bits in itertools.product([-1, 1], repeat=12):
    MM = np.array(bits).reshape(3, 4)
    if is_cube_simplex(MM): sets.add(frozenset(tuple(MM[:, j]) for j in range(4)))
check("Theorem 2: Q3 has exactly two cube simplices, the parity classes x1x2x3 = +1 and -1",
      len(sets) == 2 and {frozenset({int(np.prod(v)) for v in s}) for s in sets} == {frozenset({1}), frozenset({-1})})
check("Theorem 2: inner product -1 in Q3 means the points differ in exactly two coordinates",
      all((np.dot(u, v) == -1) == (sum(x != y for x, y in zip(u, v)) == 2) for u in Q3 for v in Q3))
disj = True
for D in (3, 7):
    K = D + 1
    Hs = np.array([[1]])
    while Hs.shape[0] < K: Hs = np.kron(H2, Hs)
    Ms = Hs[1:]
    S = {tuple(Ms[:, j]) for j in range(K)}; nS = {tuple(-Ms[:, j]) for j in range(K)}
    disj &= S.isdisjoint(nS) and len(S | nS) == 2 * K and (len(S | nS) == 2**D) == (D == 3)
check("Theorem 2: for D = 3 and D = 7 the simplex and its image are disjoint; only D = 3 fills the cube", disj)

# ---- Theorem 3
pts = [tuple(M[:, j]) for j in range(4)] + [tuple(-M[:, j]) for j in range(4)]
chars = [(), (1, 2), (0, 2), (0, 1), (0, 1, 2), (0,), (1,), (2,)]
W = np.array([[int(np.prod([p[i] for i in S])) if S else 1 for p in pts] for S in chars])
Hhat = np.vstack([np.ones(4, dtype=int), M])
check("Theorem 3: W = H2 (x) Hhat in the stated ordering", (W == np.kron(H2, Hhat)).all())
check("Theorem 3: chi_S(-x) = (-1)^|S| chi_S(x) on Q3",
      all(int(np.prod([-x[i] for i in S])) == (-1)**len(S) * int(np.prod([x[i] for i in S])) for x in Q3 for S in chars if S))
check("Theorem 3: on V each Walsh function equals its complement; on -V it equals minus its complement",
      all(int(np.prod([v[i] for i in S]) if S else 1) == int(np.prod([v[i] for i in range(3) if i not in S]) if len(S) < 3 else 1)
          for v in V for S in chars) and
      all(int(np.prod([v[i] for i in S]) if S else 1) == -int(np.prod([v[i] for i in range(3) if i not in S]) if len(S) < 3 else 1)
          for v in nV for S in chars))
check("Theorem 3: W is a Hadamard matrix of order 8", (W @ W.T == 8 * np.eye(8)).all())

# ---- Corollary 2
splits_ok = True
for K, Mk in [(4, M), (8, H8[1:])]:
    rows = [tuple(r) for r in Mk]
    splits = {frozenset(j for j in range(K) if r[j] == 1) for r in rows}
    canon = {min(s, frozenset(range(K)) - s, key=lambda z: sorted(z)) for s in splits}
    splits_ok &= all(sum(r) == 0 for r in rows) and len(canon) == K - 1
    splits_ok &= (len(canon) == math.comb(K, K // 2) // 2) == (K == 4)
check("Corollary 2: rows are balanced and give K-1 distinct splits; all splits only at K = 4 (checked K = 4, 8)", splits_ok)
check("Corollary 2: C(K,K/2)/2 = K-1 only for K in {2,4} (even K <= 200)",
      [K for K in range(2, 201, 2) if math.comb(K, K // 2) // 2 == K - 1] == [2, 4])
check("Corollary 2: for even K >= 6, C(K,K/2)/2 >= C(K,2)/2 > K-1",
      all(math.comb(K, K // 2) // 2 >= math.comb(K, 2) // 2 > K - 1 for K in range(6, 201, 2)))
check("Corollary 2: at K = 4 the rows of M are the three pair-splits {01|23}, {02|13}, {03|12}",
      {frozenset(j for j in range(4) if r[j] == 1) for r in M} == {frozenset({0, 1}), frozenset({0, 2}), frozenset({0, 3})})

print(f"\n{sum(ok)}/{len(ok)} checks passed")
