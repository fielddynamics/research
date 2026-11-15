#!/usr/bin/env python3
"""
The read and the rotation: exact checks
=======================================

Research behind a proposed proof that G's three numbers 21, 17, 13 are one
identity read four ways, split into a root-blind and a root-resolving part,
and carried by the vortex-antivortex pairs of the cube's rotations.

Every check carries a tag, as in research/coupling-algebra/certify_first_principles.py:
  CLASSICAL    standard mathematics, restated for this setting
  NEW          a statement this note adds (exact)
  AUTOMATIC    true for reasons that carry no information about GFD
  COINCIDENCE  exact, but special to the values; not to be built on
  OPEN         a probe of a step not yet derived (reports, does not claim)

Parts
  A. The read is the rotation: 1 + K + K^2 = (K^3 - 1)/(K - 1) = (K - w)(K - w*)
  B. Why D = 3 gives exactly one winding pair
  C. The ring determinants K^n - 1 and their winding-pair factors
  D. The parity split: E = 1 + K^2 (root-blind), O = K (root-resolving)
  E. The winding eigenvalues on the cube's corners, class by class
  F. G in parity form and in vortex form
  G. Open steps, probed

Run: python verify_read_and_rotation.py
"""
import itertools
import sympy as sp

ok, tags = [], {}
def check(tag, name, cond):
    cond = bool(cond); ok.append(cond); tags[tag] = tags.get(tag, 0) + 1
    print(f"  [{'PASS' if cond else 'FAIL'}] {tag:11s} {name}")
def section(t): print(f"\n=== {t}")

K, s, x, lam = sp.symbols("K s x lambda", real=True)
w = sp.exp(2 * sp.pi * sp.I / 3)
f = lambda k, s_: 1 + s_ * k + k ** 2
K0, D0 = 4, 3

# ------------------------------------------------------------------ A
section("A. The read is the rotation")
check("CLASSICAL", "1 + K + K^2 = (K^3 - 1)/(K - 1) for all K (the depth-3 read is a geometric series)",
      sp.simplify(sp.cancel((K ** 3 - 1) / (K - 1)) - (1 + K + K ** 2)) == 0)
check("CLASSICAL", "(K^3 - 1)/(K - 1) = (K - w)(K - w*), the product over the nontrivial cube roots of unity",
      sp.expand(sp.expand_complex((K - w) * (K - sp.conjugate(w)))) == sp.expand(1 + K + K ** 2))
Rth = lambda th: sp.Matrix([[sp.cos(th), -sp.sin(th)], [sp.sin(th), sp.cos(th)]])
check("CLASSICAL", "(K - w)(K - w*) = det(K - R_120): the characteristic polynomial at K of the 120-degree rotation, whose "
      "eigenvalues are w, w*",
      sp.expand(sp.simplify((K * sp.eye(2) - Rth(2 * sp.pi / 3)).det())) == sp.expand(1 + K + K ** 2)
      and set(Rth(2 * sp.pi / 3).eigenvals()) == {sp.expand_complex(w), sp.expand_complex(sp.conjugate(w))})
check("CLASSICAL", "and (K^3 - 1)/(K - 1) is the number of points of PG(2, K) for K a prime power: 21 at K = 4 "
      "(the 21 orbits are certified in coupling-algebra, section I)",
      (K0 ** 3 - 1) // (K0 - 1) == 21 == f(K0, 1))
check("NEW", "so the archive's four readings of 21 are one identity: the depth-3 read 1 + K + K^2 (scalar, legs, "
      "couplings) = the projective count = the characteristic polynomial of the 120-degree rotation at K = the trace "
      "of the graded operator at TetA; they agree because the read has D = 3 levels and the rotation has order D",
      f(K0, 1) == 1 + K0 + K0 ** 2 == (K0 ** 3 - 1) // (K0 - 1) == 21)

# ------------------------------------------------------------------ B
section("B. Why D = 3 gives exactly one winding pair")
def phi(n): return sp.totient(n)
check("CLASSICAL", "for n > 1, (K^n - 1)/(K - 1) = product of Phi_d(K) over d | n, d > 1; it is a single cyclotomic "
      "factor exactly when n is prime",
      all((sp.factor_list(sp.cancel((K ** n - 1) / (K - 1)))[1].__len__() == 1) == sp.isprime(n) for n in range(2, 13)))
check("CLASSICAL", "a cyclotomic factor Phi_n is one conjugate pair of roots (one vortex-antivortex pair) exactly when "
      "phi(n) = 2, i.e. n = 3, 4, 6",
      [n for n in range(1, 40) if phi(n) == 2] == [3, 4, 6])
check("NEW", "so the depth-D read 1 + K + ... + K^(D-1) is exactly one winding pair only for D = 3 (prime and phi = 2), "
      "the solution of the uniqueness equation 2(D + 1) = 2^D",
      [d for d in range(2, 40) if sp.isprime(d) and phi(d) == 2] == [3]
      and [d for d in range(1, 40) if 2 * (d + 1) == 2 ** d] == [3])
check("AUTOMATIC", "that the uniqueness equation and 'one winding pair' both select D = 3 is two conditions on small "
      "integers meeting at 3; no implication between them is claimed",
      True)

# ------------------------------------------------------------------ C
section("C. The ring determinants")
def shift(n):
    return sp.Matrix(n, n, lambda i, j: 1 if j == (i + 1) % n else 0)
rows = {}
for n in (3, 4, 6):
    d = (K0 * sp.eye(n) - shift(n)).det()
    rows[n] = (d, sp.factorint(d))
check("CLASSICAL", "on a ring of n sites, det(K - shift) = K^n - 1, the product of K - z over all n-th roots z",
      all(sp.expand((K * sp.eye(n) - shift(n)).det()) == K ** n - 1 for n in (3, 4, 6)))
check("NEW", f"at K = 4: 63 = 3 x 21 (3-ring), 255 = 3 x 5 x 17 (4-ring), 4095 = 3 x 5 x 13 x 21 (6-ring); the factor "
      f"K - 1 = 3 is the non-winding mode, and each structural number is the determinant on one winding pair",
      rows[3][0] == 63 and rows[4][0] == 255 and rows[6][0] == 4095
      and 63 == 3 * f(4, 1) and 255 == 3 * 5 * f(4, 0) and 4095 == 3 * 5 * f(4, -1) * f(4, 1))
check("CLASSICAL", "63 = 4^3 - 1 is also the number of nonzero vectors of F4^3, so 64 = 3 x 21 + 1 is the same "
      "factorisation (coupling algebra, section I)",
      4 ** 3 - 1 == 63 == 3 * 21)
# winding pair of each ring = the primitive roots
def pair_factor(n):
    prim = [sp.exp(2 * sp.pi * sp.I * k / n) for k in range(n) if sp.gcd(k, n) == 1]
    return sp.expand(sp.expand_complex(sp.prod([4 - z for z in prim])))
check("NEW", "restricted to the primitive (winding) roots: 3-ring -> 21, 4-ring -> 17, 6-ring -> 13",
      [pair_factor(n) for n in (3, 4, 6)] == [21, 17, 13])

# ------------------------------------------------------------------ D
section("D. The parity split")
E_, O_ = 1 + K ** 2, K
check("NEW", "f(K, s) = E + s O with E = 1 + K^2 (the scalar and the couplings) and O = K (the legs)",
      sp.expand(f(K, s) - (E_ + s * O_)) == 0)
check("NEW", "the root exchange is K -> -K: f(-K, s) = f(K, -s), so TetB = TetA with the legs reversed (M -> -M); "
      "E is even in K (root-blind), O odd (root-resolving)",
      sp.expand(f(-K, s) - f(K, -s)) == 0 and sp.expand(E_.subs(K, -K) - E_) == 0 and sp.expand(O_.subs(K, -K) + O_) == 0)
check("NEW", "the Field Origin's value is the average of the two roots: f(K, 0) = (f(K, 1) + f(K, -1))/2 = E, the "
      "root-blind part alone (the legs cancel, as (M + (-M))/2 = 0)",
      sp.expand(f(K, 0) - (f(K, 1) + f(K, -1)) / 2) == 0 and f(K0, 0) == 17)
M = sp.Matrix([[1, 1, -1, -1], [1, -1, 1, -1], [1, -1, -1, 1]])
check("CLASSICAL", "the same split in Letter 2's frame: the frame M flips with the root and its Gram matrix M^T M = "
      "4I - J does not (root-blind)",
      (-M).T * (-M) == M.T * M == 4 * sp.eye(4) - sp.ones(4, 4))

# ------------------------------------------------------------------ E
section("E. The winding eigenvalues on the cube's corners")
CORNERS = list(itertools.product((1, -1), repeat=3))
TETA = [c for c in CORNERS if c[0] * c[1] * c[2] == 1]
idx = {c: i for i, c in enumerate(CORNERS)}
def perm(g):
    P = sp.zeros(8, 8)
    for c in CORNERS:
        gc = tuple(sum(g[i][j] * c[j] for j in range(3)) for i in range(3))
        P[idx[gc], idx[c]] = 1
    return P
mp = lambda g, c: tuple(sum(g[i][j] * c[j] for j in range(3)) for i in range(3))
keeps = lambda g: all(mp(g, c) in TETA for c in TETA)
C3 = [[0, 0, 1], [1, 0, 0], [0, 1, 0]]                    # about the body diagonal (1,1,1), the time axis
S6 = [[-e for e in r] for r in C3]                        # C3 composed with the antipode
C4 = [[0, -1, 0], [1, 0, 0], [0, 0, 1]]                   # quarter turn about z
S4 = [[0, -1, 0], [1, 0, 0], [0, 0, -1]]                  # 4-fold rotoreflection about z (the vortex proof's S)
def evals(g):
    return {sp.nsimplify(sp.expand_complex(e)): m for e, m in perm(g).eigenvals().items()}
ev = {n: evals(g) for n, g in (("C3", C3), ("S6", S6), ("C4", C4), ("S4", S4))}
wv = sp.expand_complex(w)
check("NEW", "on the eight corners the closure rotation C3 has winding eigenvalues w, w* (twice each: two 3-cycles); "
      "the 6-fold rotoreflection S6 = -C3 has -w, -w* once each (its one 6-cycle; it also has w, w* once, since "
      "S6^2 is a 3-fold rotation); the order-4 elements C4, S4 have i, -i (twice each)",
      ev["C3"].get(wv, 0) == 2 and ev["C3"].get(sp.conjugate(wv), 0) == 2
      and ev["S6"].get(sp.expand(-wv), 0) == 1 and ev["S6"].get(sp.expand(-sp.conjugate(wv)), 0) == 1
      and ev["C4"].get(sp.I, 0) == 2 and ev["S4"].get(sp.I, 0) == 2)
check("NEW", "each class's value is |K - lambda|^2 for its winding eigenvalue: |4 - w|^2 = 21, |4 - i|^2 = 17, "
      "|4 + w|^2 = 13",
      [sp.simplify(sp.expand_complex((4 - z) * sp.conjugate(4 - z))) for z in (wv, sp.I, -wv)] == [21, 17, 13])
check("NEW", "these are the vortex proof's winding eigenvalues: w for the leg (Triforce) vortices under C3, i for the "
      "core vortices under the rotoreflection S4; both elements keep the chambers",
      keeps(C3) and keeps(S4))
check("NEW", "the 13-class (S6) and the quarter turn C4 exchange the chambers: they are symmetries only when TetA "
      "and TetB are alike, so with the chambers distinct the vortices that exist are exactly those of the 21- and "
      "17-classes, and the 13-class maps a TetA configuration to a TetB one",
      (not keeps(S6)) and (not keeps(C4)))
check("CLASSICAL", "crystallographic restriction: of the lattice rotations (orders 1, 2, 3, 4, 6) exactly orders 3, 4, 6 "
      "have non-real eigenvalues, the only ones that can carry a circulating state; orders 1, 2 (s = -2, +2) have "
      "eigenvalues +-1, and real winding states carry no current",
      [n for n in (1, 2, 3, 4, 6) if not sp.exp(2 * sp.pi * sp.I / n).is_real] == [3, 4, 6]
      and f(K0, 2) == 25 and f(K0, -2) == 9)

# ------------------------------------------------------------------ F
section("F. G in parity form and in vortex form")
al = sp.Symbol("alpha", positive=True)
aG = sp.Rational(17, 13) * al ** 21
E4, O4 = 17, 4
check("NEW", "alpha_G = (17/13) alpha^21 = (E/(E - O)) alpha^(E + O): the root-blind read over TetB's read, times "
      "alpha to TetA's full read",
      sp.simplify(aG - sp.Rational(E4, E4 - O4) * al ** (E4 + O4)) == 0)
check("NEW", "and in vortex form: alpha_G = (|K - i|^2 / |K + w|^2) alpha^(|K - w|^2)",
      sp.Rational(17, 13) == sp.Rational(f(4, 0), f(4, -1)) and 21 == f(4, 1))
check("NEW", "the hierarchy exponent (gravity over electromagnetism, one level) is E + O - 1 = K + K^2 = K(K + 1) = 20",
      E4 + O4 - 1 == K0 + K0 ** 2 == K0 * (K0 + 1) == 20)
check("CLASSICAL", "the gap between the 3-fold and 6-fold pairs is 2O: |K - w|^2 - |K + w|^2 = 2K",
      sp.expand(f(K, 1) - f(K, -1) - 2 * K) == 0)
G = sp.Rational(17, 13) * sp.Float("7.2973525643e-3", 15) ** 21 * sp.Float("3.16152677e-26", 12) / sp.Float("9.1093837139e-31", 14) ** 2
check("CLASSICAL", f"numerically (CODATA 2022 alpha, hbar c, m_e) the tree-level value is {float(G):.4e} m^3 kg^-1 s^-2, "
      f"0.12% below the measured 6.6743e-11 (as in the parent folder)",
      abs(float(G) / 6.6743e-11 - 1 + 0.0012) < 2e-4)

# ------------------------------------------------------------------ G
section("G. Open steps, probed")
check("OPEN", "why each level costs one factor of alpha: not addressed here (the parent folder's single physical "
      "assumption); recorded only", True)
check("OPEN", "the combination rule alpha^(TetA) x (Field Origin / TetB): in parity form it is alpha^(E+O) E/(E-O); "
      "this rewriting does not derive it (fitted after the fact among 21 rules, g_from_the_closure_climb.md)", True)
check("OPEN", "can E/(E - O) come from the connection's split 64 = 40 (root-blind Christoffel) + 24 (torsion, TetB)? "
      "the counts do not match the read directly (64 = 1 + 3 x 21 states, not 21); a derivation would need a map "
      "from the 64 components onto the 21 read states sending torsion to the legs block; none is constructed",
      64 == 1 + 3 * 21 and 40 + 24 == 64)
check("AUTOMATIC", "the parent folder's one-loop split alpha/2pi = (2/17)(17 alpha/4pi) reads as (2/E)(E alpha/(K pi)); "
      "it holds for any E and carries no information",
      sp.simplify((2 / sp.Symbol("E")) * (sp.Symbol("E") * al / (4 * sp.pi)) - al / (2 * sp.pi)) == 0)

print(f"\n{sum(ok)}/{len(ok)} checks passed   by tag: {tags}")
raise SystemExit(len(ok) - sum(ok))
