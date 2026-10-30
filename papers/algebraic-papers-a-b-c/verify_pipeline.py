#!/usr/bin/env python3
"""
Checks for algebraic_pipeline_of_reality.md
===========================================

Verifies every algebraic statement in the pipeline document:

  1. 2(D+1) = 2^D has the unique solution D = 3
  2. TetA = odd-parity corners, TetB = even-parity corners
  3. The cocycle twist sigma(a,b) = (-1)^{sum_{i>j} a_i b_j} turns the group
     algebra of Z_2^3 into Cl(3,0): e_i^2 = +1, anticommutation, associativity,
     I central with I^2 = -1
  4. Omega (e1 -> e2 -> e3) is an automorphism; its vertex orbits are the two
     poles and the two triangles; its fixed subspace has dimension 4
  5. 21, 17, 13 are the norms N(4 - w), N(4 - i), N(4 + w)
  6. 64 = 24 + 16 + 24; 40 Christoffel + 24 torsion
  7. Among K >= 3, K*C(K,2) = K! and K*C(K,2) = 2^(K-1)(K-1) only at K = 4
  8. Torsion V (x) L^2 V is the regular representation of S_4; the sign
     representation occurs once in torsion and never in V (x) S^2 V
  9. u(x) = x/(1+x): reciprocity, boundary values, logistic derivative
 10. F(y) ~ (2/3) y^(3/2) for small y
 11. alpha_G = (17/13) alpha^21 (1 + alpha/2pi) against CODATA

Python 3.8+, standard library only.

    python verify_pipeline.py
"""
import itertools
import math
from fractions import Fraction

results = []


def check(name, ok):
    results.append(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")


B = range(8)


def bits(a):
    return [(a >> i) & 1 for i in range(3)]


def popcount(a):
    return bin(a).count("1")


# 1-2 ------------------------------------------------------------------
check("2(D+1) = 2^D only at D = 3 (D = 0..50)", [D for D in range(51) if 2 * (D + 1) == 2 ** D] == [3])
check("TetA = odd parity {1,2,4,7}, TetB = even parity {0,3,5,6}",
      [v for v in B if popcount(v) % 2] == [1, 2, 4, 7] and [v for v in B if popcount(v) % 2 == 0] == [0, 3, 5, 6])

# 3 --------------------------------------------------------------------


def sigma(a, b):
    A, C = bits(a), bits(b)
    return (-1) ** sum(A[i] * C[j] for i in range(3) for j in range(3) if i > j)


def mul(u, v):
    w = [0] * 8
    for a in B:
        for b in B:
            if u[a] and v[b]:
                w[a ^ b] += sigma(a, b) * u[a] * v[b]
    return w


def e(a):
    return [1 if i == a else 0 for i in B]


def neg(u):
    return [-x for x in u]


gens = [e(1), e(2), e(4)]
one, I = e(0), e(7)
check("twisted product: generators square to +1", all(mul(x, x) == one for x in gens))
check("twisted product: generators anticommute",
      all(mul(gens[i], gens[j]) == neg(mul(gens[j], gens[i])) for i in range(3) for j in range(3) if i != j))
check("twisted product is associative",
      all(mul(mul(e(a), e(b)), e(c)) == mul(e(a), mul(e(b), e(c))) for a in B for b in B for c in B))
check("pseudoscalar I is central with I^2 = -1",
      mul(I, I) == neg(one) and all(mul(I, e(a)) == mul(e(a), I) for a in B))

# 4 --------------------------------------------------------------------


def rot(a):
    return ((a << 1) & 7) | (a >> 2)


def blade_sign(a):
    idx = [i for i in range(3) if (a >> i) & 1]
    new = [(i + 1) % 3 for i in idx]
    return (-1) ** sum(1 for x in range(len(new)) for y in range(x + 1, len(new)) if new[x] > new[y])


def omega(u):
    w = [0] * 8
    for a in B:
        w[rot(a)] += u[a] * blade_sign(a)
    return w


orbits = sorted({tuple(sorted({a, rot(a), rot(rot(a))})) for a in B})
check("Omega vertex orbits: poles {000}, {111}; triangles {001,010,100}, {011,101,110}",
      orbits == [(0,), (1, 2, 4), (3, 5, 6), (7,)])
check("Omega is an algebra automorphism", all(omega(mul(e(a), e(b))) == mul(omega(e(a)), omega(e(b)))
                                             for a in B for b in B))
# fixed subspace dimension = (1/3) sum over group elements of the trace
traces = []
for k in range(3):
    t = 0
    for a in B:
        v = e(a)
        for _ in range(k):
            v = omega(v)
        t += v[a]
    traces.append(t)
check("Omega fixes a 4-dimensional subspace (1, I, d, Id)", sum(traces) // 3 == 4)
d = [0, 1, 1, 0, 1, 0, 0, 0]
check("d = e1 + e2 + e3 and I d are fixed by Omega", omega(d) == d and omega(mul(I, d)) == mul(I, d))

# 5 --------------------------------------------------------------------
K = 4


def n_eis(a, b):          # N(a + b w) = a^2 - ab + b^2
    return a * a - a * b + b * b


check("21 = N(4 - w), 17 = N(4 - i), 13 = N(4 + w)",
      (n_eis(K, -1), K * K + 1, n_eis(K, 1)) == (21, 17, 13))
check("f(4, s) = Phi_3, Phi_4, Phi_6 at K = 4",
      [1 + s * K + K * K for s in (1, 0, -1)] == [K * K + K + 1, K * K + 1, K * K - K + 1])

# 6-7 ------------------------------------------------------------------
check("64 = 24 + 16 + 24 and 40 + 24", K * (K * (K - 1) // 2) == 24 and K * K == 16
      and K ** 3 == 24 + 16 + 24 and K * K * (K + 1) // 2 == 40)
check("among K >= 3, K*C(K,2) = K! only at K = 4",
      [k for k in range(3, 30) if k * k * (k - 1) // 2 == math.factorial(k)] == [4])
check("among K >= 3, K*C(K,2) = 2^(K-1)(K-1) only at K = 4",
      [k for k in range(3, 30) if k * k * (k - 1) // 2 == 2 ** (k - 1) * (k - 1)] == [4])

# 8 --------------------------------------------------------------------
perms = list(itertools.permutations(range(4)))


def fixed(p):
    return sum(1 for i in range(4) if p[i] == i)


def fixed2(p):
    return sum(1 for i in range(4) if p[p[i]] == i)


def sgn(p):
    return (-1) ** sum(1 for i in range(4) for j in range(i + 1, 4) if p[i] > p[j])


def cycle_type(p):
    seen, c = set(), []
    for i in range(4):
        if i not in seen:
            n, j = 0, i
            while j not in seen:
                seen.add(j)
                j = p[j]
                n += 1
            c.append(n)
    return tuple(sorted(c))


irreps = {
    "trivial": (1, lambda p: 1),
    "sign": (1, sgn),
    "2-dim": (2, lambda p: {(1, 1, 1, 1): 2, (1, 1, 2): 0, (2, 2): 2, (1, 3): -1, (4,): 0}[cycle_type(p)]),
    "standard": (3, lambda p: fixed(p) - 1),
    "standard x sign": (3, lambda p: (fixed(p) - 1) * sgn(p)),
}


def multiplicities(chi):
    return {k: Fraction(sum(chi(p) * g(p) for p in perms), 24) for k, (_, g) in irreps.items()}


def chi_lambda2(p):
    return (fixed(p) ** 2 - fixed2(p)) // 2


def chi_sym2(p):
    return (fixed(p) ** 2 + fixed2(p)) // 2


tors = multiplicities(lambda p: fixed(p) * chi_lambda2(p))
chris = multiplicities(lambda p: fixed(p) * chi_sym2(p))
check("torsion V (x) L^2 V is the regular representation of S_4",
      all(tors[k] == dim for k, (dim, _) in irreps.items()))
check("sign representation: once in torsion, zero times in Christoffel",
      tors["sign"] == 1 and chris["sign"] == 0)

# 9-10 -----------------------------------------------------------------


def u(x):
    return x / (1 + x)


xs = [0.01, 0.3, 1.0, 2.7, 50.0]
check("u(x) + u(1/x) = 1 and u(1) = 1/2", all(abs(u(x) + u(1 / x) - 1) < 1e-12 for x in xs) and u(1) == 0.5)
h = 1e-6
check("du/d ln x = u(1 - u)", all(abs((u(x * math.exp(h)) - u(x * math.exp(-h))) / (2 * h) - u(x) * (1 - u(x)))
                                  < 1e-8 for x in xs))


def F(y):
    t = math.sqrt(y)
    return y - 2 * t + 2 * math.log1p(t)


check("F(y) / ((2/3) y^1.5) -> 1 as y -> 0", abs(F(1e-8) / (2 / 3 * 1e-12) - 1) < 1e-3)

# 11 -------------------------------------------------------------------
alpha, hbar, c, me, G = 7.2973525643e-3, 1.054571817e-34, 299792458.0, 9.1093837139e-31, 6.67430e-11
aG = G * me ** 2 / (hbar * c)
pred = 17 / 13 * alpha ** 21 * (1 + alpha / (2 * math.pi))
ppm = 1e6 * (pred - aG) / aG
check(f"alpha_G: predicted {pred:.5e}, measured {aG:.5e}, {ppm:+.0f} ppm (G known to 22 ppm)", abs(ppm) < 22)

print(f"\n  {sum(results)}/{len(results)} checks pass")
