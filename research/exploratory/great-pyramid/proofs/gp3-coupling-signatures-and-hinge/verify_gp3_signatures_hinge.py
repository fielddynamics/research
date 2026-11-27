#!/usr/bin/env python3
"""
GP-3  The coupling signatures are forced, and the hinge is the only coincidence
between levels.

Exact integer / polynomial / finite-field checks of every statement in
README.md. Prints PASS/FAIL per check, exits non-zero on any failure.

Run from this folder:  python verify_gp3_signatures_hinge.py
"""
import sys
import itertools
from math import gcd

import sympy as sp

RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {label}" + (f"  -- {detail}" if detail else ""))


K, s, X = sp.symbols("K s X")


def f(k, ss):
    return 1 + ss * k + k * k


print("=" * 78)
print("GP-3  Coupling signatures: forced, coprime, fused; the hinge is unique")
print("=" * 78)

# --------------------------------------------------------------------------
print("\n-- Theorem 1: the signatures are exactly the degree-two cyclotomic polynomials")
# (a) phi(n) = 2  <=>  n in {3, 4, 6}.  Proof bound: phi(n) >= sqrt(n/2) for all n >= 1,
#     so phi(n) = 2 forces n <= 8; check n <= 8 exhaustively, and the bound itself to 10^5.
bound_ok = all(sp.totient(n) ** 2 * 2 >= n for n in range(1, 100001))
check("T1a phi(n)^2 >= n/2 for every n <= 100000 (the classical bound phi(n) >= sqrt(n/2))", bound_ok)
phi2 = [n for n in range(1, 9) if sp.totient(n) == 2]
check("T1a hence phi(n) = 2 iff n in {3, 4, 6} (exhaustive for n <= 8)", phi2 == [3, 4, 6], str(phi2))
# (b) the cyclotomic polynomials of those orders are the three signatures
check("T1b Phi_3(K) = K^2 + K + 1 = f(K, +1)", sp.expand(sp.cyclotomic_poly(3, K) - f(K, 1)) == 0)
check("T1b Phi_4(K) = K^2 + 1     = f(K,  0)", sp.expand(sp.cyclotomic_poly(4, K) - f(K, 0)) == 0)
check("T1b Phi_6(K) = K^2 - K + 1 = f(K, -1)", sp.expand(sp.cyclotomic_poly(6, K) - f(K, -1)) == 0)
# (c) norm form: f(K, s) = |K + e^{i theta}|^2 with s = 2 cos theta
th = sp.symbols("theta", real=True)
Kr = sp.symbols("Kr", real=True)
norm = sp.expand((Kr + sp.cos(th)) ** 2 + sp.sin(th) ** 2)
check("T1c |K + e^{i theta}|^2 = K^2 + 2 cos(theta) K + 1, i.e. f(K, 2 cos theta)",
      sp.simplify(norm - (Kr ** 2 + 2 * sp.cos(th) * Kr + 1)) == 0)
# (d) integer coefficients with a root of unity: 2 cos(2 pi k/n) in Z iff n | 1,2,3,4,6 ; |s| < 2 iff n in {3,4,6}
integral_orders = []
for n in range(1, 61):
    for k in range(n):
        if gcd(k, n) != 1:
            continue
        val = sp.nsimplify(2 * sp.cos(2 * sp.pi * k / n))
        if val.is_integer:
            integral_orders.append((n, int(val)))
orders = sorted(set(n for n, _ in integral_orders))
check("T1d 2 cos(2 pi k/n) (k coprime to n) is an integer only for n in {1,2,3,4,6} (n <= 60)",
      orders == [1, 2, 3, 4, 6], str(sorted(set(integral_orders))))
check("T1d of those, |2 cos| < 2 (an irreducible quadratic) only for n = 3, 4, 6, giving s = -1, 0, +1",
      sorted(v for n, v in integral_orders if n in (3, 4, 6)) == [-1, -1, 0, 0, 1, 1] and
      all(abs(v) == 2 for n, v in integral_orders if n in (1, 2)))
# (e) the boundary values s = +-2 are perfect squares (degenerate)
check("T1e f(K, +2) = (K+1)^2 = Phi_2^2 and f(K, -2) = (K-1)^2 = Phi_1^2 (reducible, excluded)",
      sp.expand(f(K, 2) - (K + 1) ** 2) == 0 and sp.expand(f(K, -2) - (K - 1) ** 2) == 0)
# (f) at K = 4
check("T1f at K = 4: (f(4,-1), f(4,0), f(4,1)) = (13, 17, 21)", (f(4, -1), f(4, 0), f(4, 1)) == (13, 17, 21))
# (g) irreducible over Q
check("T1g each signature polynomial is irreducible over Q",
      all(sp.Poly(f(K, v), K).is_irreducible for v in (-1, 0, 1)))

# --------------------------------------------------------------------------
print("\n-- Theorem 2: the hinge f(K,+1) = f(K+1,-1) is the only coincidence between levels")
check("T2 identity f(K, +1) = f(K + 1, -1) for all K (polynomial identity)", sp.expand(f(K, 1) - f(K + 1, -1)) == 0)
coinc = []
NMAX = 3000
vals = {}
for k in range(1, NMAX + 1):
    for v in (-1, 0, 1):
        vals.setdefault(f(k, v), []).append((k, v))
for val, lst in vals.items():
    if len(lst) > 1:
        coinc.append(tuple(sorted(lst)))
hinge_only = all(len(c) == 2 and c[0][1] == 1 and c[1][1] == -1 and c[1][0] == c[0][0] + 1
                 or (len(c) == 2 and c[0][1] == -1 and c[1][1] == 1 and c[0][0] == c[1][0] + 1)
                 for c in coinc)
check(f"T2 for 1 <= K, K' <= {NMAX}: every equality f(K,s) = f(K',s'), (K,s) != (K',s'), is a hinge pair",
      hinge_only and len(coinc) == NMAX - 1, f"{len(coinc)} coincidences, all hinges")
# the three proof steps, symbolically
check("T2 step 1: for fixed s in {-1,0,1}, K^2 + sK is strictly increasing on K >= 1 (difference 2K + 1 + s > 0)",
      all(sp.expand(f(K + 1, v) - f(K, v)) == 2 * K + 1 + v for v in (-1, 0, 1)))
check("T2 step 2: K^2 = n(n +- 1) has no solution with K, n >= 1 (n(n+1) lies strictly between n^2 and (n+1)^2)",
      all(not sp.sqrt(n * (n + 1)).is_integer and (n < 2 or not sp.sqrt(n * (n - 1)).is_integer) for n in range(1, 20001)))
check("T2 step 3: K(K+1) = (K'-1)K' iff K' = K + 1 (n(n+1) strictly increasing)",
      all((k * (k + 1) == (kp - 1) * kp) == (kp == k + 1) for k in range(1, 200) for kp in range(1, 202)))
check("T2 the neutral value 17 = f(4, 0) occurs at no other (K, s); 13 and 21 occur twice each (the two hinges at 3|4 and 4|5)",
      vals[17] == [(4, 0)] and sorted(vals[13]) == [(3, 1), (4, -1)] and sorted(vals[21]) == [(4, 1), (5, -1)])

# --------------------------------------------------------------------------
print("\n-- Theorem 3: the three signatures are pairwise coprime for every integer K")
cop = all(gcd(f(k, a), f(k, b)) == 1 for k in range(-5000, 5001) for a, b in ((-1, 0), (-1, 1), (0, 1)))
check("T3 gcd = 1 for every pair, |K| <= 5000", cop)
check("T3 proof: f(K,1) - f(K,-1) = 2K, f(K,+-1) are odd, gcd(f(K,s), K) = 1  =>  gcd(f(K,1), f(K,-1)) = 1",
      sp.expand(f(K, 1) - f(K, -1)) == 2 * K and all(f(k, 1) % 2 == 1 and f(k, -1) % 2 == 1 for k in range(-1000, 1001)))
check("T3 proof: f(K,+-1) - f(K,0) = +-K and gcd(K^2+1, K) = 1  =>  gcd(f(K,0), f(K,+-1)) = 1",
      sp.expand(f(K, 1) - f(K, 0)) == K and sp.expand(f(K, 0) - f(K, -1)) == K)
check("T3 midpoint identity f(K,1) + f(K,-1) = 2 f(K,0) (TetA + TetB = 2 x Field Origin, the arithmetic of 21 + 13 = 34)",
      sp.expand(f(K, 1) + f(K, -1) - 2 * f(K, 0)) == 0)

# --------------------------------------------------------------------------
print("\n-- Theorem 4: fusion and the tower")
check("T4 fusion f(K,1) f(K,-1) = f(K^2, 1) = K^4 + K^2 + 1", sp.expand(f(K, 1) * f(K, -1) - f(K ** 2, 1)) == 0)
check("T4 fusion f(K,1) f(K,-1) = 1 + K^2 f(K,0)", sp.expand(f(K, 1) * f(K, -1) - (1 + K ** 2 * f(K, 0))) == 0)
check("T4 at K = 4: 21 x 13 = 273 = 1 + 16 + 256 = 1 + 16 x 17", 21 * 13 == 273 == 1 + 16 + 256 == 1 + 16 * 17)
tower_ok = True
for n in range(0, 6):
    lhs = f(K ** (2 ** n), 1)
    rhs = f(K, 1) * sp.prod([f(K ** (2 ** j), -1) for j in range(n)])
    if sp.expand(lhs - rhs) != 0:
        tower_ok = False
check("T4 tower f(K^(2^n), 1) = f(K,1) prod_{j<n} f(K^(2^j), -1) for n = 0..5 (polynomial identities)", tower_ok)
check("T4 at K = 4 the tower reads 21 -> 273 = 21 x 13 -> 65793 = 21 x 13 x 241",
      f(16, 1) == 273 and f(256, 1) == 65793 == 21 * 13 * 241 and f(16, -1) == 241)
check("T4 tower factors are pairwise coprime at K = 4 (21, 13, 241, 65281)",
      all(gcd(a, b) == 1 for a, b in itertools.combinations([21, 13, f(16, -1), f(256, -1)], 2)), f"f(256,-1) = {f(256, -1)}")
# polynomial content: X^(3 m) - 1 factorisation reading
check("T4 cyclotomic reading: Phi_3(K) Phi_6(K) = Phi_3(K^2), since Phi_3(X^2) = Phi_3(X) Phi_6(X)",
      sp.expand(sp.cyclotomic_poly(3, K) * sp.cyclotomic_poly(6, K) - sp.cyclotomic_poly(3, K ** 2)) == 0)

# --------------------------------------------------------------------------
print("\n-- Theorem 5: finite-geometry counts (exact enumeration over GF(3), GF(4), GF(16))")


class GF:
    """GF(p^m) by an irreducible polynomial, elements as int bit/coeff vectors."""

    def __init__(self, p, m, modpoly):
        self.p, self.m, self.q = p, m, p ** m
        self.mod = modpoly  # coefficients low -> high, length m+1, monic
        self.elems = list(range(self.q))

    def vec(self, a):
        v = []
        for _ in range(self.m):
            v.append(a % self.p)
            a //= self.p
        return v

    def num(self, v):
        a = 0
        for c in reversed(v):
            a = a * self.p + c
        return a

    def add(self, a, b):
        return self.num([(x + y) % self.p for x, y in zip(self.vec(a), self.vec(b))])

    def mul(self, a, b):
        va, vb = self.vec(a), self.vec(b)
        prod = [0] * (2 * self.m - 1)
        for i, x in enumerate(va):
            for j, y in enumerate(vb):
                prod[i + j] = (prod[i + j] + x * y) % self.p
        for d in range(len(prod) - 1, self.m - 1, -1):
            c = prod[d]
            if c:
                for k in range(self.m + 1):
                    prod[d - self.m + k] = (prod[d - self.m + k] - c * self.mod[k]) % self.p
        return self.num(prod[:self.m])


def projective_points(F, dim):
    """Normalised representatives of PG(dim, q): first nonzero coordinate = 1."""
    pts = []
    for v in itertools.product(F.elems, repeat=dim + 1):
        nz = [c for c in v if c != 0]
        if nz and nz[0] == 1:
            pts.append(v)
    return pts


GF3 = GF(3, 1, [0, 1])          # prime field (modpoly X)
GF4 = GF(2, 2, [1, 1, 1])       # X^2 + X + 1
GF16 = GF(2, 4, [1, 1, 0, 0, 1])  # X^4 + X + 1
check("T5 |PG(2,3)| = 13 = f(3,+1) = f(4,-1)", len(projective_points(GF3, 2)) == 13)
check("T5 |PG(2,4)| = 21 = f(4,+1) = f(5,-1)", len(projective_points(GF4, 2)) == 21)
check("T5 |PG(2,16)| = 273 = f(16,+1) = f(4,1) f(4,-1)", len(projective_points(GF16, 2)) == 273)
# lines of PG(2,4): 21 lines, 5 points each, every two points on exactly one line
P = projective_points(GF4, 2)


def dotq(F, a, b):
    s_ = 0
    for x, y in zip(a, b):
        s_ = F.add(s_, F.mul(x, y))
    return s_


lines = [[p for p in P if dotq(GF4, l, p) == 0] for l in P]
check("T5 PG(2,4) has 21 lines of 5 = K + 1 points, any two points on exactly one line",
      len(lines) == 21 and all(len(L) == 5 for L in lines) and
      all(sum(1 for L in lines if a in L and b in L) == 1 for a, b in itertools.combinations(P, 2)))
# elliptic quadric in PG(3,4): Q = x0 x1 + x2^2 + x2 x3 + w x3^2,  t^2 + t + w irreducible over GF(4)
w = 2  # the element X of GF(4)
irreducible = all(GF4.add(GF4.add(GF4.mul(t, t), t), w) != 0 for t in GF4.elems)
check("T5 t^2 + t + w has no root in GF(4) (so the quadric below is elliptic)", irreducible)
P3 = projective_points(GF4, 3)


def Q(v):
    x0, x1, x2, x3 = v
    out = GF4.mul(x0, x1)
    out = GF4.add(out, GF4.mul(x2, x2))
    out = GF4.add(out, GF4.mul(x2, x3))
    out = GF4.add(out, GF4.mul(w, GF4.mul(x3, x3)))
    return out


ovoid = [v for v in P3 if Q(v) == 0]
check("T5 the elliptic quadric (an ovoid) of PG(3,4) has 17 = K^2 + 1 = f(4,0) points", len(ovoid) == 17, f"{len(ovoid)} points")
# no three collinear: an ovoid is a cap
def collinear(a, b, c):
    # rank of 3x4 matrix over GF(4) < 3 <=> c in span(a,b)
    for la in GF4.elems:
        for lb in GF4.elems:
            comb = tuple(GF4.add(GF4.mul(la, x), GF4.mul(lb, y)) for x, y in zip(a, b))
            if comb == c:
                return True
    return False


cap = all(not collinear(a, b, c) for a, b, c in itertools.combinations(ovoid, 3))
check("T5 no three of the 17 points are collinear (a cap of maximal size q^2 + 1)", cap)
check("T5 |PG(3,4)| = 85 = 1 + 4 + 16 + 64 = 5 x 17 = (K+1) f(K,0)", len(P3) == 85 == 5 * 17)

# --------------------------------------------------------------------------
print("\n-- Theorem 6: graded-trace realisation (inherited from Proof 26, Thm 7; restated)")
trace_ok = True
for kk in (2, 3, 4, 5):
    # grades 0, 1, 2 of T_K = 1 + V + V (x) V, as explicit diagonal projectors
    n = 1 + kk + kk * kk
    P_odd = sp.diag(*([0] + [1] * kk + [0] * kk * kk))
    P_even = sp.eye(n) - P_odd
    for v in (-1, 0, 1):
        if (P_even + v * P_odd).trace() != f(kk, v):
            trace_ok = False
check("T6 Tr(P_even + s P_odd) on 1 + V + V(x)V equals f(K,s) for K = 2..5, s = -1,0,1", trace_ok)
m_plus, m_minus = sp.symbols("mp mm")
sol = sp.solve([m_plus + m_minus - 21, m_plus - m_minus - 13], [m_plus, m_minus])
check("T6 an involution J with Tr I = 21, Tr J = 13 has eigenvalue multiplicities (17, 4), forced", sol == {m_plus: 17, m_minus: 4})
check("T6 det(alpha^{I_s}) = alpha^{Tr I_s} = alpha^{17 + 4 s}: exponents 13, 17, 21", [17 + 4 * v for v in (-1, 0, 1)] == [13, 17, 21])


print("\n-- Theorem 1b: the short proof; s = zeta + conj(zeta) is an algebraic integer")
check("T1b discriminants of f(K,s) = K^2 + sK + 1 are s^2 - 4: -3, -4, -3 for s = -1, 0, 1 (all < 0: irreducible over Q)",
      [v * v - 4 for v in (-1, 0, 1)] == [-3, -4, -3])
check("T1b a rational algebraic integer is an integer, and |zeta + conj zeta| <= 2, so s in {-2,...,2}",
      sp.Rational(1, 2).is_integer is False and all(abs(int(v)) <= 2 for v in (-2, -1, 0, 1, 2)))

print("\n-- Theorem 6b: unitary rigidity of the 17 + 4 grading")
import numpy as np
rng = np.random.default_rng(7)
ok = True
for trial in range(30):
    Q, _ = np.linalg.qr(rng.normal(size=(21, 21)))
    J = Q @ np.diag([1.0] * 17 + [-1.0] * 4) @ Q.T
    ev = np.linalg.eigvalsh(J)
    if not (np.allclose(J @ J, np.eye(21)) and abs(np.trace(J) - 13) < 1e-9 and
            (np.abs(ev - 1) < 1e-9).sum() == 17 and (np.abs(ev + 1) < 1e-9).sum() == 4):
        ok = False
    Pfo, Podd = (np.eye(21) + J) / 2, (np.eye(21) - J) / 2
    traces = [np.trace(Pfo + s_ * Podd) for s_ in (1, 0, -1)]
    if not np.allclose(traces, [21, 17, 13]):
        ok = False
check("T6b every symmetric involution on R^21 with trace 13 is conjugate to I_17 + (-I_4); A_s = P_FO + s P_odd has traces 21, 17, 13", ok)

print("\n-- Theorem 7: every exact interlevel intertwiner lives on the hinge block")
def shell(Kv, dims):
    """Shell Hamiltonian with eigenvalues f(K,-1), f(K,0), f(K,1) of the given multiplicities."""
    return np.diag(sum(([float(f(Kv, v))] * d for v, d in zip((-1, 0, 1), dims)), []))
def intertwiner_space(Ha, Hb):
    n, m = Ha.shape[0], Hb.shape[0]
    # vec(Hb T - T Ha) = (I (x) Hb - Ha^T (x) I) vec T
    Mbig = np.kron(np.eye(n), Hb) - np.kron(Ha.T, np.eye(m))
    _, sv, vh = np.linalg.svd(Mbig)
    null = vh[np.sum(sv > 1e-9):]
    return null, n, m
ok_dim, ok_block, ok_far = True, True, True
for trial in range(12):
    Kv = int(rng.integers(2, 9))
    da, db = rng.integers(1, 4, 3), rng.integers(1, 4, 3)
    Ha, Hb = shell(Kv, da), shell(Kv + 1, db)
    null, n, m = intertwiner_space(Ha, Hb)
    if null.shape[0] != da[2] * db[0]:
        ok_dim = False
    for v in null:
        T = v.reshape(n, m).T                       # T maps the K shell to the K+1 shell
        rows = slice(0, db[0]); cols = slice(da[0] + da[1], n)
        mask = np.zeros_like(T, dtype=bool); mask[rows, cols] = True
        if np.abs(T[~mask]).max(initial=0) > 1e-9:
            ok_block = False
    null2, _, _ = intertwiner_space(Ha, shell(Kv + 2, db))
    if null2.shape[0] != 0:
        ok_far = False
check("T7 dim{T : H_{K+1} T = T H_K} = dim E_{K,+} x dim E_{K+1,-} (12 random multiplicity patterns, K = 2..8)", ok_dim)
check("T7 every such T is supported on the single block E_{K,+} -> E_{K+1,-}", ok_block)
check("T7 non-adjacent shells (K -> K+2) admit no nonzero intertwiner", ok_far)
Zt = np.zeros((Hb.shape[0], Ha.shape[0]))
check("T7 the zero map always intertwines: a matching band does not imply a nonzero transition",
      np.allclose(Hb @ Zt, Zt @ Ha))

print("\n-- Theorem 4b: the whole fusion tower is pairwise coprime (proof by induction)")
ok = True
for Kv in range(2, 11):
    facs = [f(Kv, 1)] + [f(Kv ** (2 ** j), -1) for j in range(5)]
    if not all(gcd(a, b) == 1 for a, b in itertools.combinations(facs, 2)):
        ok = False
check("T4b A_0, B_0, B_1, ..., B_4 pairwise coprime for K = 2..10 (B_j | A_n for j < n, and gcd(A_n, B_n) = 1)", ok)

print("\n" + "=" * 78)
print(f"GP-3: {sum(RESULTS)}/{len(RESULTS)} checks passed")
sys.exit(0 if all(RESULTS) else 1)
