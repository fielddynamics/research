"""
verify_intersection.py
======================

Exact checks for INTERSECTION_ALGEBRA.md: where the framework's separate
algebras (coupling polynomial, Clifford closure algebra, t-bit Moebius gates,
S4 torsion sector, stellated octahedron) turn out to be one object.

Every claim prints PASS or FAIL.  Claims that were tested and REJECTED are
printed as "REJECTED (as expected)" -- they are kept so the negative results
are reproducible too.

Requires: numpy, sympy.   Run:  python verify_intersection.py
"""
from __future__ import annotations

import itertools
import math
from fractions import Fraction

import numpy as np
import sympy as sp

RESULTS = []


def check(name, cond):
    RESULTS.append((name, bool(cond)))
    print(f"[{'PASS' if cond else 'FAIL'}] {name}")


K, s, x, t = sp.symbols("K s x t", real=True)


def Phi(n, var=K):
    return sp.cyclotomic_poly(n, var)


# ---------------------------------------------------------------------------
# Part A. The spinor norm form (Cl(3,0) realised by Pauli matrices)
# ---------------------------------------------------------------------------
print("\n=== A. Spinor norm form in Cl(3,0) ===")
I2 = np.eye(2, dtype=complex)
s1 = np.array([[0, 1], [1, 0]], dtype=complex)
s2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
s3 = np.array([[1, 0], [0, -1]], dtype=complex)
E = [s1, s2, s3]
Ips = s1 @ s2 @ s3                       # pseudoscalar, = i * 1
T1 = s1 + s2 + s3                        # body-diagonal vector d
nhat = T1 / np.sqrt(3)
R = (I2 - Ips @ T1) / 2                  # rotor for 120 deg about (1,1,1)


def rev(X):                              # reversion = Hermitian conjugate in this rep
    return X.conj().T


def is_scalar(M):
    return np.allclose(M, M[0, 0] * I2)


check("I^2 = -1 (pseudoscalar is the Gaussian unit)", np.allclose(Ips @ Ips, -I2))
check("R is a unit rotor: R R~ = 1", np.allclose(R @ rev(R), I2))
check("R^3 = -1, R^6 = +1 (order 6 in Spin(3))",
      np.allclose(np.linalg.matrix_power(R, 3), -I2) and np.allclose(np.linalg.matrix_power(R, 6), I2))
check("-R has order 3", np.allclose(np.linalg.matrix_power(-R, 3), I2))
cyc = all(np.allclose(R @ E[i] @ rev(R), E[(i + 1) % 3]) for i in range(3))
check("Ad_R is the closure operator Omega: e1->e2->e3->e1", cyc)
check("R lies in the Omega-fixed (axial) subalgebra: Omega(R) = R", np.allclose(R @ R @ rev(R), R))


def spinor_norm(Kv, X):
    M = (Kv * I2 - X) @ rev(Kv * I2 - X)
    return M


for Kv in range(2, 9):
    vals = [spinor_norm(Kv, X) for X in (-R, Ips, R)]
    ok = all(is_scalar(v) for v in vals) and [round(v[0, 0].real) for v in vals] == [
        Kv * Kv + Kv + 1, Kv * Kv + 1, Kv * Kv - Kv + 1]
    if not ok:
        break
check("N_K(X) = (K-X)(K-X)~ is scalar and equals Phi3, Phi4, Phi6 at X = -R, I, R (K=2..8)", ok)
v4 = [round(spinor_norm(4, X)[0, 0].real) for X in (-R, Ips, R)]
check(f"At K = 4: N_4(-R), N_4(I), N_4(R) = {v4} = [21, 17, 13]", v4 == [21, 17, 13])

zeta12 = (T1 + Ips) / 2
check("zeta12 = (d + I)/2 has order 12", np.allclose(np.linalg.matrix_power(zeta12, 12), I2)
      and not np.allclose(np.linalg.matrix_power(zeta12, 6), I2))
check("N_4(zeta12) is NOT scalar (degree-4 state needs a second norm)", not is_scalar(spinor_norm(4, zeta12)))
check("Its full norm |det(4 - zeta12)|^2 = Phi12(4) = 241",
      abs(abs(np.linalg.det(4 * I2 - zeta12)) ** 2 - 241) < 1e-9)

# Pole splitting
Pp, Pm = (I2 + nhat) / 2, (I2 - nhat) / 2
check("P+ and P- are orthogonal idempotents summing to 1",
      np.allclose(Pp @ Pp, Pp) and np.allclose(Pm @ Pm, Pm) and np.allclose(Pp @ Pm, 0 * I2)
      and np.allclose(Pp + Pm, I2))
# Bloch vectors of P+-: tr(P sigma_i)
bloch = lambda P: np.real([np.trace(P @ e) for e in E])
check("P+ projects on the (+,+,+) cube vertex, P- on (-,-,-): one apex of each tetrahedron",
      np.allclose(bloch(Pp), [1 / np.sqrt(3)] * 3) and np.allclose(bloch(Pm), [-1 / np.sqrt(3)] * 3))
check("R P+ = e^{-i pi/3} P+ and R P- = e^{+i pi/3} P-",
      np.allclose(R @ Pp, np.exp(-1j * np.pi / 3) * Pp) and np.allclose(R @ Pm, np.exp(1j * np.pi / 3) * Pm))

# Spin-sheet theorem (symbolic in K, for any unit q with real part a)
a = sp.symbols("a", real=True)
Nq = K**2 - 2 * K * a + 1
Nmq = K**2 + 2 * K * a + 1
check("Sheet average: [N(K-q) + N(K+q)]/2 = K^2 + 1 = Phi4(K) for every unit q",
      sp.simplify((Nq + Nmq) / 2 - Phi(4)) == 0)
check("Sheet difference: N(K+q) - N(K-q) = 4Ka; = 2K = 2^D at |2a| = 1, K = 4 gives 8",
      sp.simplify(Nmq - Nq - 4 * K * a) == 0 and (Nmq - Nq).subs({K: 4, a: sp.Rational(1, 2)}) == 8)
check("q -> -q (kernel of Spin(3) -> SO(3)) is s -> -s: Phi3 <-> Phi6",
      sp.expand(Nq.subs(a, -sp.Rational(1, 2)) - Phi(3)) == 0 and sp.expand(Nq.subs(a, sp.Rational(1, 2)) - Phi(6)) == 0)

# ---------------------------------------------------------------------------
# Part B. Moebius / Lorentz reading of the state map
# ---------------------------------------------------------------------------
print("\n=== B. Moebius-Lorentz reading of s(x) and mu(x) ===")
xp = sp.symbols("x", positive=True)
s_of_x = (xp - 1) / (xp + 1)
f = 1 + s * K + K**2
f_lo, f_hi = f.subs(s, -1), f.subs(s, 1)
mu_from_f = sp.simplify((f - f_lo) / (f_hi - f_lo))
check("CRITICAL: (f - f(-1)) / (f(+1) - f(-1)) = (1 + s)/2 for EVERY K (K drops out)",
      sp.simplify(mu_from_f - (1 + s) / 2) == 0)
check("Hence mu(x) = (1 + s(x))/2 = x/(x+1) with no input from K = 4",
      sp.simplify((1 + s_of_x) / 2 - xp / (xp + 1)) == 0)
check("s(x) = tanh(eta), eta = (1/2) ln x  (s is a velocity, ln x a rapidity)",
      sp.simplify(sp.tanh(sp.log(xp) / 2).rewrite(sp.exp) - s_of_x) == 0)
al, xq = sp.symbols("alpha y", positive=True)
s_a = (al - 1) / (al + 1)
s_y = (xq - 1) / (xq + 1)
lhs = ((al * xq) - 1) / ((al * xq) + 1)
check("Dilation gate D_alpha acts on s by relativistic velocity addition (s_a + s)/(1 + s_a s)",
      sp.simplify(lhs - (s_a + s_y) / (1 + s_a * s_y)) == 0)
check("Exchange P: x -> 1/x acts as s -> -s (boost reversal)",
      sp.simplify(s_of_x.subs(xp, 1 / xp) + s_of_x) == 0)
eta = sp.symbols("eta", real=True)
check("Logistic law d mu / d ln x = mu (1 - mu)  <=>  ds/d eta = 1 - s^2",
      sp.simplify(sp.diff(sp.tanh(eta), eta) - (1 - sp.tanh(eta) ** 2)) == 0)
# Continuous capacity on the unit circle
th = sp.symbols("theta", real=True)
cont = sp.expand((K - sp.cos(th)) ** 2 + sp.sin(th) ** 2)
check("f(K,s) = |K - e^{i theta}|^2 with s = -2 cos theta",
      sp.simplify(cont - f.subs(s, -2 * sp.cos(th))) == 0)
fx = sp.simplify(f.subs(s, s_of_x).subs(K, 4))
check("f(4, s(x)) = (21x + 13)/(x + 1), the repo's continuous capacity",
      sp.simplify(fx - (21 * xp + 13) / (xp + 1)) == 0)
# arc: theta(x) runs from pi/3 (x->0, TetB) through pi/2 (x=1) to 2pi/3 (x->inf, TetA)
cos_th = -s_of_x / 2
check("x -> 0: theta -> pi/3 (zeta6, TetB); x = 1: theta = pi/2 (i, Field Origin); x -> inf: 2pi/3 (zeta3, TetA)",
      sp.limit(cos_th, xp, 0) == sp.Rational(1, 2) and cos_th.subs(xp, 1) == 0
      and sp.limit(cos_th, xp, sp.oo) == -sp.Rational(1, 2))

# ---------------------------------------------------------------------------
# Part C. The modular group at level K = 4
# ---------------------------------------------------------------------------
print("\n=== C. The modular group: SL2(Z) elliptic elements and PSL2(Z/4) = S4 ===")
S = sp.Matrix([[0, -1], [1, 0]])
T = sp.Matrix([[1, 1], [0, 1]])
ST = S * T
L = sp.Matrix([[1, 0], [1, 1]])
P = sp.Matrix([[0, 1], [1, 0]])
cp = lambda M: sp.expand((K * sp.eye(2) - M).det())
check("det(K - S) = Phi4(K)  (S has order 4 in SL2(Z))", sp.expand(cp(S) - Phi(4)) == 0)
check("det(K - ST) = Phi6(K)  (ST has order 6)", sp.expand(cp(ST) - Phi(6)) == 0)
check("det(K - (ST)^2) = Phi3(K)  ((ST)^2 has order 3)", sp.expand(cp(ST**2) - Phi(3)) == 0)
check("f(K,s) = det(K - M) with s = -tr M: the three states are the elliptic classes of SL2(Z)",
      all(sp.expand(cp(M) - f.subs(s, -M.trace())) == 0 for M in (S, ST, ST**2)))


def mob(M):
    return lambda z: (M[0, 0] * z + M[0, 1]) / (M[1, 0] * z + M[1, 1])


check("The constitutive law is a modular matrix: mu = L = [[1,0],[1,1]] = P T P",
      L == P * T * P and sp.simplify(mob(L)(xp) - xp / (xp + 1)) == 0)
check("Its complement 1 - mu = P T: x -> 1/(x+1)", sp.simplify(mob(P * T)(xp) - 1 / (xp + 1)) == 0)
check("L = S T^-1 S^-1 (the constitutive law is conjugate to the cusp generator)",
      L == S * T.inv() * S.inv())
check("L^K = [[1,0],[K,1]]: L has order K = 4 modulo 4",
      L**4 == sp.Matrix([[1, 0], [4, 1]]))
check("mu composed n times: x/(n x + 1)",
      all(sp.simplify(mob(L**n)(xp) - xp / (n * xp + 1)) == 0 for n in range(1, 7)))

N = 4


def mmul(A, B, n=N):
    return ((A[0] * B[0] + A[1] * B[2]) % n, (A[0] * B[1] + A[1] * B[3]) % n,
            (A[2] * B[0] + A[3] * B[2]) % n, (A[2] * B[1] + A[3] * B[3]) % n)


def det(m, n=N):
    return (m[0] * m[3] - m[1] * m[2]) % n


units = [u for u in range(N) if math.gcd(u, N) == 1]


def proj(m):
    return min(tuple((u * v) % N for v in m) for u in units)


allm = list(itertools.product(range(N), repeat=4))
GL = [m for m in allm if math.gcd(det(m), N) == 1]
SL = [m for m in GL if det(m) == 1]
PGL = sorted(set(proj(m) for m in GL))
PSL = sorted(set(proj(m) for m in SL))
check(f"|PSL2(Z/4)| = {len(PSL)} = 4! ;  |PGL2(Z/4)| = {len(PGL)} = |O_h|", len(PSL) == 24 and len(PGL) == 48)


def order(m):
    e, k, c = proj((1, 0, 0, 1)), 1, proj(m)
    while c != e:
        c, k = proj(mmul(c, m)), k + 1
    return k


ordPSL = sorted(order(m) for m in PSL)
counts = {o: ordPSL.count(o) for o in set(ordPSL)}
check(f"PSL2(Z/4) element orders {counts} = S4's {{1:1, 2:9, 3:8, 4:6}}", counts == {1: 1, 2: 9, 3: 8, 4: 6})
ordPGL = sorted(order(m) for m in PGL)
cg = {o: ordPGL.count(o) for o in set(ordPGL)}
check(f"PGL2(Z/4) element orders {cg} = O_h = S4 x Z2's {{1:1, 2:19, 3:8, 4:12, 6:8}}",
      cg == {1: 1, 2: 19, 3: 8, 4: 12, 6: 8})
# Generator orders: S order 2, ST order 3, T order 4 = K
red = lambda M: proj(tuple(int(v) % N for v in M))
check("Mod 4: S has order 2, ST order 3, T order 4 = K  -> triangle group (2, 3, 4)",
      order(red(S)) == 2 and order(red(ST)) == 3 and order(red(T)) == 4)

# Projective line over Z/4: 6 points = cusps = octahedron vertices
pts = sorted(set(min(((u * p) % N, (u * q) % N) for u in units)
                 for p in range(N) for q in range(N) if math.gcd(math.gcd(p, q), N) == 1))


def act(m, pt):
    p, q = pt
    v = ((m[0] * p + m[1] * q) % N, (m[2] * p + m[3] * q) % N)
    return min(((u * v[0]) % N, (u * v[1]) % N) for u in units)


perm = lambda m: tuple(pts.index(act(m, p)) for p in pts)
check(f"P^1(Z/4) has {len(pts)} points = 6 octahedron vertices; both groups act faithfully",
      len(pts) == 6 and len(set(perm(m) for m in PSL)) == 24 and len(set(perm(m) for m in PGL)) == 48)
# antipodal pairing: the unique perfect matching preserved by the whole group
pairs_all = list(itertools.combinations(range(6), 2))
inv = []
for match in itertools.combinations(pairs_all, 3):
    if len(set(itertools.chain(*match))) != 6:
        continue
    M = set(frozenset(p) for p in match)
    if all(set(frozenset((pm[a_], pm[b_])) for a_, b_ in match) == M for pm in map(perm, PGL)):
        inv.append(M)
check("Exactly one invariant antipodal pairing (3 axes of the octahedron)", len(inv) == 1)
axes = [tuple(sorted(p)) for p in inv[0]]
print("      axes:", [(pts[a_], pts[b_]) for a_, b_ in axes])
faces = [tuple(sorted(c)) for c in itertools.product(*axes)]
check("Faces = one point from each axis: 2^3 = 8 = cube vertices = stellated-octahedron tips", len(faces) == 8)
edges = [e for e in pairs_all if frozenset(e) not in inv[0]]
check("Edges = non-antipodal pairs: 12", len(edges) == 12)
adj = lambda f1, f2: len(set(f1) & set(f2)) == 2
colour = {faces[0]: 0}
frontier = [faces[0]]
while frontier:
    g = frontier.pop()
    for h in faces:
        if adj(g, h) and h not in colour:
            colour[h] = 1 - colour[g]
            frontier.append(h)
two_col = all(colour[g] != colour[h] for g in faces for h in faces if adj(g, h))
check("Faces 2-colour into 4 + 4 with adjacent faces opposite: the two tetrahedra (TetA, TetB)",
      two_col and sum(colour.values()) == 4)


def face_perm(m):
    pm = perm(m)
    return {g: tuple(sorted(pm[v] for v in g)) for g in faces}


def swaps(m):
    fp = face_perm(m)
    return colour[fp[faces[0]]] != colour[faces[0]]


A4 = [m for m in PSL if not swaps(m)]
check("Kernel of the TetA<->TetB swap inside PSL2(Z/4) has order 12 (A4): the sign character",
      len(A4) == 12)
check("Swap character = permutation sign: elements of order 4 and the 6 transpositions swap, order 3 do not",
      all(swaps(m) == (order(m) == 4 or (order(m) == 2 and m not in A4)) for m in PSL)
      and all(not swaps(m) for m in PSL if order(m) == 3))
Pm4 = proj((0, 1, 1, 0))
# First hypothesis tested: "x -> 1/x mod 4 is the TetA <-> TetB swap".  It is FALSE:
fixedP = [pts[i] for i, j in enumerate(perm(Pm4)) if i == j]
check("Exchange P: x -> 1/x mod 4 does NOT swap the tetrahedra: it is a mirror (orientation-reversing, "
      "order 2) fixing the cusps x = 1 and x = -1",
      not swaps(Pm4) and Pm4 not in PSL and order(Pm4) == 2 and fixedP == [(1, 1), (1, 3)])
centre = [z for z in PGL if all(proj(mmul(z, m)) == proj(mmul(m, z)) for m in PGL)]
Zc = [z for z in centre if z != proj((1, 0, 0, 1))]
check("The centre of PGL2(Z/4) is {1, Z}, Z = [[1,2],[2,3]]: the central inversion v -> -v of O_h",
      len(centre) == 2 and len(Zc) == 1 and Zc[0] == (1, 2, 2, 3))
Z4 = Zc[0]
check("Spatial parity Z swaps TetA and TetB (as the scheme proof says: three is odd)", swaps(Z4))
ZP = proj(mmul(Z4, Pm4))
check("Parity x exchange, Z.P, is a half-turn rotation (in PSL2, order 2, no fixed cusp) that swaps TetA and TetB",
      ZP in PSL and order(ZP) == 2 and swaps(ZP) and all(i != j for i, j in enumerate(perm(ZP))))
Lm4 = red(L)
check("The constitutive law L (order 4) swaps TetA and TetB, its square preserves them",
      swaps(Lm4) and not swaps(proj(mmul(Lm4, Lm4))))
STm4 = red(ST)
check("The closure rotation ST (order 3) preserves each tetrahedron", not swaps(STm4))
# Riemann-Hurwitz for X(4) -> X(1)
mu_idx, e2, e3, c = 24, 24 // 2, 24 // 3, 24 // 4
g = 1 + (-2 * mu_idx + (mu_idx - e2) + (mu_idx - e3) + (mu_idx - c)) / 2
check(f"X(4) -> X(1): fibres 12 (over i), 8 (over rho), 6 (cusps); Riemann-Hurwitz genus {g:.0f} (sphere)",
      g == 0 and (e2, e3, c) == (12, 8, 6))

# Uniqueness: |(2,3,K) rotation group| = torsion count K * C(K,2) only at K = 4
order_tri = lambda k: Fraction(2, 1) / (Fraction(1, 2) + Fraction(1, 3) + Fraction(1, k) - 1)
tors = lambda k: k * k * (k - 1) // 2
hits = [k for k in range(2, 6) if order_tri(k) == tors(k)]
check(f"|Delta(2,3,K)| = K*C(K,2) (torsion count) for spherical K in 2..5 only at K = {hits}", hits == [4])
check("Equivalently K(K-1)(6-K) = 24 has the unique integer root K = 4 for 2 <= K <= 5",
      [k for k in range(2, 6) if k * (k - 1) * (6 - k) == 24] == [4])

# Stern-Brocot: words in {T, L} on x = 1 give every positive rational once
seen, frontier = {Fraction(1)}, [Fraction(1)]
for _ in range(9):
    nxt = []
    for q in frontier:
        for child in (q + 1, q / (q + 1)):
            nxt.append(child)
    frontier = nxt
    for q in frontier:
        seen.add(q)
total = 2 ** 10 - 1
check(f"Integer gates {{T: x+1, L = mu}} from the balanced state x = 1: {len(seen)} distinct rationals from {total} words (no repeats)",
      len(seen) == total)
check("... and every reduced p/q with p + q <= 11 is reached",
      all(Fraction(p, q) in seen for p in range(1, 11) for q in range(1, 11) if p + q <= 11 and math.gcd(p, q) == 1))

# ---------------------------------------------------------------------------
# Part D. The squaring ladder
# ---------------------------------------------------------------------------
print("\n=== D. The squaring (Sierpinski) ladder ===")
check("Phi3(K^2) = Phi3(K) Phi6(K): next-level TetA = TetA x TetB (273 = 21 x 13)",
      sp.expand(Phi(3).subs(K, K**2) - Phi(3) * Phi(6)) == 0 and 21 * 13 == 273)
check("Phi4(K^2) = Phi8(K) = 257 at K = 4", sp.expand(Phi(4).subs(K, K**2) - Phi(8)) == 0 and Phi(8).subs(K, 4) == 257)
check("Phi6(K^2) = Phi12(K) = 241 at K = 4", sp.expand(Phi(6).subs(K, K**2) - Phi(12)) == 0 and Phi(12).subs(K, 4) == 241)
check("Spin side: (K - X)(K + X) = K^2 - X^2 (squaring X <-> K -> K^2)",
      np.allclose((4 * I2 - R) @ (4 * I2 + R), 16 * I2 - R @ R))
ladder = [4, 16, 256, 65536]
fo = [k * k + 1 for k in ladder]
check(f"Field-Origin column K^2+1 along K -> K^2 is the Fermat sequence {fo}",
      fo == [2 ** (2 ** n) + 1 for n in (2, 3, 4, 5)])
check("17, 257, 65537 prime; F5 = 4294967297 = 641 x 6700417 composite: the ladder's primality ends at rung 4",
      all(sp.isprime(v) for v in fo[:3]) and not sp.isprime(fo[3]) and fo[3] == 641 * 6700417)

# ---------------------------------------------------------------------------
# Part E. Tested and rejected (kept for the record)
# ---------------------------------------------------------------------------
print("\n=== E. Coincidence filter (claims that should NOT survive) ===")
tot = lambda k: sum(sp.totient(int(Phi(n).subs(K, k))) for n in (3, 4, 6))
christ = lambda k: k * k * (k + 1) // 2
hits40 = [k for k in range(2, 30) if tot(k) == christ(k)]
print(f"      phi(13)+phi(17)+phi(21) = {tot(4)} = 40 Christoffel components at K = 4; matches for K in 2..29: {hits40}")
rej = hits40 == [4]
print(f"[{'REJECTED (as expected)' if rej else 'NOTE'}] Totient sum = Christoffel count holds only at K = 4 "
      "with no mechanism: a single-point coincidence, not a structural identity")

# ---------------------------------------------------------------------------
n_pass = sum(1 for _, ok in RESULTS if ok)
print(f"\n{n_pass}/{len(RESULTS)} checks passed")
if __name__ == "__main__":
    raise SystemExit(0 if n_pass == len(RESULTS) else 1)
