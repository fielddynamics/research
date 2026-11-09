"""Machine checks for every step of
'The Torsion Sector of the Tetrad Connection as the Regular Representation of S4'.
Integer arithmetic throughout; exact ranks via sympy.
Run: python verify_torsion_regular_representation.py"""
import itertools, math
from fractions import Fraction
import numpy as np
import sympy as sp

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

K = 4
P = list(itertools.permutations(range(K)))
def sgn(p): return int(round(np.linalg.det(np.eye(len(p))[list(p)])))
def compose(p, q): return tuple(p[q[i]] for i in range(len(q)))   # (p o q)(i) = p(q(i))
def rank(M): return sp.Matrix(M.astype(int)).rank()
I64 = np.eye(64, dtype=int)
def idx(a, b, c): return a * 16 + b * 4 + c

# S4 acting on all three indices of Gamma^a_bc (V* ~ V: the dual basis is permuted the same way)
def act(p):
    M = np.zeros((64, 64), dtype=int)
    for a in range(4):
        for b in range(4):
            for c in range(4):
                M[idx(p[a], p[b], p[c]), idx(a, b, c)] = 1
    return M
A = {p: act(p) for p in P}
Sw = np.zeros((64, 64), dtype=int)
for a in range(4):
    for b in range(4):
        for c in range(4):
            Sw[idx(a, c, b), idx(a, b, c)] = 1
Ttor2, Tchr2 = I64 - Sw, I64 + Sw          # 2 x projectors (integer)
def t(a, b, c):                            # basis vector f_a (x) f_b ^ f_c
    v = np.zeros(64, dtype=int); v[idx(a, b, c)] += 1; v[idx(a, c, b)] -= 1; return v
classes = {"e": (0, 1, 2, 3), "(ab)": (1, 0, 2, 3), "(ab)(cd)": (1, 0, 3, 2), "(abc)": (1, 2, 0, 3), "(abcd)": (1, 2, 3, 0)}
sizes = {"e": 1, "(ab)": 6, "(ab)(cd)": 3, "(abc)": 8, "(abcd)": 6}
irreps = {"1": [1, 1, 1, 1, 1], "sgn": [1, -1, 1, 1, -1], "[2,2]": [2, 0, 2, -1, 0],
          "std": [3, 1, -1, 0, -1], "sgn x std": [3, -1, -1, 0, 1]}
def char2(Pr2): return [int(np.trace(A[p] @ Pr2)) // 2 for p in classes.values()]   # trace of projector
def mult(ch, irr): return Fraction(sum(sizes[k] * ch[i] * irr[i] for i, k in enumerate(classes)), 24)

# ---- Setting
eta = np.diag([-1, 1, 1, 1])
check("Setting: |eta| = I is invariant under all 24 permutations", all((np.eye(4)[list(p)] @ np.abs(eta) @ np.eye(4)[list(p)].T == np.abs(eta)).all() for p in P))
check("Setting: dim C = 40, dim T = 24", rank(Tchr2) == 40 and rank(Ttor2) == 24)
check("Setting: C and T are S4-submodules (projectors commute with the action)",
      all((A[p] @ Ttor2 == Ttor2 @ A[p]).all() for p in P))
check("Setting: sigma t_{a;bc} = t_{sigma a; sigma b sigma c}",
      all((A[p] @ t(a, b, c) == t(p[a], p[b], p[c])).all() for p in P for a in range(4) for b in range(4) for c in range(4)))

# ---- Lemma
lines = [(a, (b, c)) for a in range(4) for b in range(4) for c in range(b + 1, 4)]
def line_act(p, L):
    a, (b, c) = L; B, C = p[b], p[c]
    return (p[a], (min(B, C), max(B, C))), (1 if B < C else -1)
def orbit(L): return {line_act(p, L)[0] for p in P}
inc = [L for L in lines if L[0] in L[1]]; non = [L for L in lines if L[0] not in L[1]]
check("Lemma: incident lines form one orbit of 12", orbit((0, (0, 1))) == set(inc) and len(inc) == 12)
check("Lemma: non-incident lines form one orbit of 12", orbit((0, (2, 3))) == set(non) and len(non) == 12)
st1 = [(p, line_act(p, (0, (0, 1)))[1]) for p in P if line_act(p, (0, (0, 1)))[0] == (0, (0, 1))]
st2 = [(p, line_act(p, (0, (2, 3)))[1]) for p in P if line_act(p, (0, (2, 3)))[0] == (0, (2, 3))]
tau = (0, 1, 3, 2)
check("Lemma: stabiliser of t_{0;01} is H = <(23)>, acting by +1", st1 == [((0, 1, 2, 3), 1), (tau, 1)])
check("Lemma: stabiliser of t_{0;23} is H = <(23)>, acting by -1", st2 == [((0, 1, 2, 3), 1), (tau, -1)])

# ---- Theorem 1
xi = t(0, 0, 1) + t(0, 2, 3)
X = np.array([A[p] @ xi for p in P]).T
check("Theorem 1: tau xi = t_{0;01} - t_{0;23}", (A[tau] @ xi == t(0, 0, 1) - t(0, 2, 3)).all())
check("Theorem 1: sigma xi +/- sigma tau xi = 2 sigma t_{0;01}, 2 sigma t_{0;23}",
      all((A[p] @ xi + A[compose(p, tau)] @ xi == 2 * A[p] @ t(0, 0, 1)).all() and
          (A[p] @ xi - A[compose(p, tau)] @ xi == 2 * A[p] @ t(0, 2, 3)).all() for p in P))
check("Theorem 1: the 24 vectors sigma xi are a basis of T (exact rank 24, all in T)",
      rank(X) == 24 and ((Ttor2 @ X) == 2 * X).all())
check("Theorem 1: Phi(rho sigma) = rho Phi(sigma)",
      all((A[compose(r, s)] @ xi == A[r] @ (A[s] @ xi)).all() for r in P for s in P))

# ---- Corollary 1
chT = char2(Ttor2)
check("Corollary 1: character of T is (24,0,0,0,0)", chT == [24, 0, 0, 0, 0])
check("Corollary 1: each irreducible occurs with multiplicity = dimension",
      [mult(chT, v) for v in irreps.values()] == [1, 1, 2, 3, 3])
Pinc2 = np.diag([1 if (i // 16) in ((i // 4) % 4, i % 4) else 0 for i in range(64)]) @ Ttor2
Pnon2 = Ttor2 - Pinc2
check("Corollary 1: chi_inc = (12,2,0,0,0) = Ind_H 1, chi_non = (12,-2,0,0,0) = Ind_H eps",
      char2(Pinc2) == [12, 2, 0, 0, 0] and char2(Pnon2) == [12, -2, 0, 0, 0])
def ind_char(chi):   # induced character from H = <(23)>: (1/|H|) sum_g chi(g^-1 p g) over g with g^-1 p g in H
    Hchar = {(0, 1, 2, 3): chi[0], tau: chi[1]}
    out = []
    for p in classes.values():
        tot = Fraction(0)
        for g in P:
            ginv = tuple(int(i) for i in np.argsort(g))
            conj = compose(compose(ginv, p), g)
            tot += Hchar.get(conj, 0)
        out.append(tot / 2)
    return [int(x) for x in out]
check("Corollary 1: Frobenius formula gives the same induced characters",
      ind_char([1, 1]) == [12, 2, 0, 0, 0] and ind_char([1, -1]) == [12, -2, 0, 0, 0])

# ---- Theorem 2
chC = char2(Tchr2)
check("Theorem 2: sgn occurs once in T and not in C (C character (40,8,0,1,0))",
      mult(chT, irreps["sgn"]) == 1 and mult(chC, irreps["sgn"]) == 0 and chC == [40, 8, 0, 1, 0])
cbasis = [(a, (b, c)) for a in range(4) for b in range(4) for c in range(b, 4)]
def corb(L): return {(p[L[0]], tuple(sorted((p[L[1][0]], p[L[1][1]])))) for p in P}
orbs = []
for L in cbasis:
    if not any(L in o for o in orbs): orbs.append(corb(L))
stab_has_transposition = all(any(sum(1 for i in range(4) if p[i] != i) == 2 and
                                 (p[L[0]], tuple(sorted((p[L[1][0]], p[L[1][1]])))) == L for p in P)
                             for L in [next(iter(o)) for o in orbs])
check("Theorem 2: C has orbits of sizes 4,12,12,12, each stabiliser containing a transposition",
      sorted(len(o) for o in orbs) == [4, 12, 12, 12] and stab_has_transposition)
def eps(*ix): return 0 if len(set(ix)) < 4 else sgn(ix)
omega = np.array([sum(eps(a, b, c, d) for d in range(4)) for a in range(4) for b in range(4) for c in range(4)])
check("Theorem 2: omega != 0, lies in T, transforms by sgn",
      omega.any() and ((Ttor2 @ omega) == 2 * omega).all() and all((A[p] @ omega == sgn(p) * omega).all() for p in P))
check("Theorem 2: omega lies in T_non (vanishes unless a,b,c distinct)", ((Pnon2 @ omega) == 2 * omega).all())

# ---- Theorem 3
Tv = np.array([[(a == b) * (c == k) - (a == c) * (b == k) for a in range(4) for b in range(4) for c in range(4)] for k in range(4)]).T
Tax = np.array([[eps(a, b, c, d) for a in range(4) for b in range(4) for c in range(4)] for d in range(4)]).T
check("Theorem 3: T_v (dim 4) lies in T_inc", rank(Tv) == 4 and ((Pinc2 @ Tv) == 2 * Tv).all())
check("Theorem 3: T_ax (dim 4) lies in T_non", rank(Tax) == 4 and ((Pnon2 @ Tax) == 2 * Tax).all())
def proj(B):
    Bf = B.astype(float); return Bf @ np.linalg.pinv(Bf)
PV, PA = proj(Tv), proj(Tax)
Tin, Tout = Pinc2 / 2 - PV, Pnon2 / 2 - PA
def charf(Pr): return [int(round(np.trace(A[p] @ Pr))) for p in classes.values()]
check("Theorem 3: chi(T_v) = chi_V = (4,2,0,1,0); chi(T_ax) = sgn chi_V = (4,-2,0,1,0)",
      charf(PV) == [4, 2, 0, 1, 0] and charf(PA) == [4, -2, 0, 1, 0])
check("Theorem 3: each tensor half has character (8,0,0,-1,0) = [2,2] + std + sgn x std",
      charf(Tin) == [8, 0, 0, -1, 0] and charf(Tout) == [8, 0, 0, -1, 0] and
      [mult([8, 0, 0, -1, 0], v) for v in irreps.values()] == [0, 0, 1, 1, 1])
trace = np.array([[1 if (b == a and c == k) else 0 for a in range(4) for b in range(4) for c in range(4)] for k in range(4)])  # v_k = T^a_{ak}
Alt = np.zeros((64, 64))
for a, b, c in itertools.product(range(4), repeat=3):
    for q in itertools.permutations(range(3)):
        ijk = [(a, b, c)[q[0]], (a, b, c)[q[1]], (a, b, c)[q[2]]]
        Alt[idx(*ijk), idx(a, b, c)] += sgn(q) / 6
check("Theorem 3: trace vanishes on T_non and on the incident tensor half; Alt vanishes on T_inc and on the non-incident tensor half",
      np.allclose(trace @ Pnon2, 0) and np.allclose(trace @ Tin, 0) and np.allclose(Alt @ Pinc2, 0) and np.allclose(Alt @ Tout, 0))
check("Theorem 3: T_v is the image of the adjoint of the trace (on T)",
      np.linalg.matrix_rank(np.hstack([Tv, (Ttor2 @ trace.T)])) == 4)
Ptor = Ttor2 / 2
kernel_rank = np.linalg.matrix_rank(np.vstack([trace @ Ptor, Alt @ Ptor, np.eye(64) - Ptor]))
check("Theorem 3: torsion that is trace-free with no totally antisymmetric part has dimension 16 = 8 + 8",
      64 - kernel_rank == 16 and round(np.trace(Tin)) == 8 and round(np.trace(Tout)) == 8)
check("Theorem 3: with |eta| the axial subspace is S4-invariant",
      all(np.linalg.matrix_rank(np.hstack([Tax, A[p] @ Tax])) == 4 for p in P))
D = np.diag([(-1 if a == 0 else 1) for a in range(4) for b in range(4) for c in range(4)])   # raise index 0 with eta
Tax_eta = D @ Tax
check("Theorem 3: with eta the axial subspace is not S4-invariant",
      not all(np.linalg.matrix_rank(np.hstack([Tax_eta, A[p] @ Tax_eta])) == 4 for p in P))
s01 = (1, 0, 2, 3)
img = A[s01] @ (D @ np.array([eps(a, b, c, 2) for a in range(4) for b in range(4) for c in range(4)]))
lowered = D @ img
check("Theorem 3: (01) sends the eta-axial tensor eps_{abc2} to lowered T_013 = -1, T_301 = +1",
      lowered[idx(0, 1, 3)] == -1 and lowered[idx(3, 0, 1)] == 1)

# ---- Proposition
sols = [k for k in range(1, 31) if k * math.comb(k, 2) == math.factorial(k)]
check("Proposition: K * C(K,2) = K! only for K in {2,4} (K <= 30)", sols == [2, 4])
check("Proposition: for 5 <= K <= 30, (K-2)! >= (K-2)(K-3) >= 2(K-2) > K/2",
      all(math.factorial(k - 2) >= (k - 2) * (k - 3) >= 2 * (k - 2) > k / 2 for k in range(5, 31)))
# K = 2: T = V (x) Lambda^2 V for S2, computed directly
def torsion_char(Kk):
    Pk = list(itertools.permutations(range(Kk))); res = []
    for p in Pk:
        tr = 0
        for a in range(Kk):
            for b in range(Kk):
                for c in range(b + 1, Kk):
                    B, C = p[b], p[c]
                    if p[a] == a and {B, C} == {b, c}:
                        tr += 1 if B < C else -1
        res.append(tr)
    return res
check("Proposition: at K = 2 the torsion character is (2,0), the regular character of S2",
      torsion_char(2) == [2, 0])
check("Proposition: at K = 3 the torsion (dim 9) is not regular (|S3| = 6)",
      torsion_char(3)[0] == 9)

# ---- Scope
check("Scope: sgn(sigma) = det P_sigma for all sigma", all(sgn(p) == round(np.linalg.det(np.eye(4)[list(p)])) for p in P))
par = np.diag([1, -1, -1, -1])
check("Scope: spatial parity has det -1 and is not a permutation matrix",
      round(np.linalg.det(par)) == -1 and not any((np.eye(4)[list(p)] == par).all() for p in P))

print(f"\n{sum(ok)}/{len(ok)} checks passed")
